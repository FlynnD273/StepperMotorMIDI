import time
import sys
from scipy.signal import find_peaks
import numpy as np

from Util import get_serial, send_note, setup_exit_handler, MOTOR_COUNT


def stream_speaker(args):
    WINDOW = 2**12
    HOP = 64
    buffer = np.zeros(WINDOW)

    N = np.hamming(WINDOW)
    bias = np.exp(np.linspace(-2, 0, WINDOW))
    window = N * bias
    window /= max(window)

    with get_serial(args.port) as ser:
        setup_exit_handler(ser)
        time.sleep(2)
        print("Ready.")
        while True:
            raw = np.frombuffer(sys.stdin.buffer.read(HOP * 2), dtype=np.int16)
            buffer[:-HOP] = buffer[HOP:]
            buffer[-HOP:] = raw

            spectrum = np.fft.rfft(buffer * window)
            magnitude = np.abs(spectrum)
            freqs = np.fft.rfftfreq(WINDOW, d=1 / args.samplerate)
            peaks, _ = find_peaks(magnitude, prominence=5000, width=[0, 4])
            # peaks, _ = find_peaks(magnitude)
            potential_peak_indexes = peaks[np.argsort(magnitude[peaks])[::-1]]
            peak_indexes = []

            for i in potential_peak_indexes:
                is_rejected = magnitude[i] < max(magnitude[0] * 0.75, 50000)
                if not is_rejected:
                    is_rejected = freqs[i] < 100 or freqs[i] > 12000
                if not is_rejected:
                    for j in peak_indexes:
                        ratio = freqs[i] / freqs[j]
                        if ratio >= 2 and (ratio % 1) < 0.2:
                            is_rejected = True
                            break
                if not is_rejected:
                    peak_indexes.append(i)

            # peak_indexes = potential_peak_indexes

            for i, peak in enumerate(peak_indexes[:MOTOR_COUNT]):
                send_note(ser, i, int(1000000 / freqs[peak]))
            if len(peak_indexes) < MOTOR_COUNT:
                for i in range(len(peak_indexes), MOTOR_COUNT):
                    send_note(ser, i, 0)

