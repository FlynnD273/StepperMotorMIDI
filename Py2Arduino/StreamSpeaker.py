import time
import sys
from scipy.signal import find_peaks
import numpy as np

from Util import get_serial, send_note, setup_exit_handler, stop_all


def stream_speaker(args):
    BLOCKSIZE = 2**11
    motor_count = 3

    with get_serial(args.port) as ser:
        setup_exit_handler(ser, motor_count)
        time.sleep(2)
        print("Ready.")
        while True:
            raw = sys.stdin.buffer.read(BLOCKSIZE * 2)
            if len(raw) < BLOCKSIZE * 2:
                break

            mono = np.frombuffer(raw, dtype=np.int16)

            spectrum = np.fft.rfft(mono * np.hanning(len(mono)))
            magnitude = np.abs(spectrum)
            freqs = np.fft.rfftfreq(BLOCKSIZE, d=1 / args.samplerate)
            peaks, _ = find_peaks(magnitude, prominence=5000, width=[0, 4])
            peak_indexes = peaks[np.argsort(magnitude[peaks])[-motor_count:]]

            for i, peak in enumerate(peak_indexes):
                if magnitude[peak] < 50000:
                    send_note(ser, i, 0)
                else:
                    send_note(ser, i, int(1000000 / freqs[peak]))
            for i in range(len(peak_indexes), motor_count):
                send_note(ser, i, 0)
            ser.flush()

