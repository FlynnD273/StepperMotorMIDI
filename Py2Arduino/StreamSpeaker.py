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

    freqs = np.fft.rfftfreq(WINDOW, d=1 / args.samplerate)

    with get_serial(args.port) as ser:
        setup_exit_handler(ser)
        while True:
            raw = np.frombuffer(sys.stdin.buffer.read(HOP * 2), dtype=np.int16)
            buffer[:-HOP] = buffer[HOP:]
            buffer[-HOP:] = raw

            spectrum = np.fft.rfft(buffer * window)
            magnitude = np.abs(spectrum)
            peaks, _ = find_peaks(magnitude, prominence=5000, width=[0, 4])
            potential_peak_indexes = peaks[np.argsort(magnitude[peaks])[::-1]]
            potential_peak_indexes = potential_peak_indexes[: MOTOR_COUNT * 3]
            peak_indexes = []

            for i in potential_peak_indexes:
                is_rejected = freqs[i] < 100 or freqs[i] > 12000
                if not is_rejected:
                    for j in peak_indexes:
                        for mult in range(2, 6):
                            f = freqs[j] * mult
                            if abs(f - freqs[i]) < 10:
                                is_rejected = True
                                break
                        if is_rejected:
                            break
                if not is_rejected:
                    peak_indexes.append(i)

            if len(peak_indexes) > 0:
                level_threshold = max(np.max(magnitude[peak_indexes]) * 0.5, 50000)
                peak_indexes = [
                    i for i in peak_indexes if magnitude[i] > level_threshold
                ]

            # peak_indexes = potential_peak_indexes

            for i, peak in enumerate(peak_indexes[:MOTOR_COUNT]):
                send_note(ser, i, int(1000000 / freqs[peak]))
            if len(peak_indexes) < MOTOR_COUNT:
                for i in range(len(peak_indexes), MOTOR_COUNT):
                    send_note(ser, i, 0)

