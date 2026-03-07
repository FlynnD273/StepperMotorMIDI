import mido
import struct
import serial
import time
import signal
import sys
from scipy.signal import find_peaks
import numpy as np


def stream_speaker(args):
    BLOCKSIZE = 1024
    motor_count = 3

    with serial.Serial(args.port, 115200) as ser:
        def stop_all():
            for i in range(motor_count):
                ser.write(struct.pack(">BH", i, 0))
                ser.flush()

        def signal_handler(sig, frame):
            stop_all()
            ser.close()
            sys.exit(0)

        signal.signal(signal.SIGINT, signal_handler)
        time.sleep(2)
        print("Ready.")
        while True:
            # Read raw PCM data
            raw = sys.stdin.buffer.read(BLOCKSIZE * 2)
            if len(raw) < BLOCKSIZE * 2:
                break

            audio = np.frombuffer(raw, dtype=np.int16)
            audio = audio.reshape(-1, 1)
            mono = audio.mean(axis=1)

            spectrum = np.fft.rfft(mono * np.hanning(len(mono)))
            magnitude = np.abs(spectrum)
            freqs = np.fft.rfftfreq(BLOCKSIZE, d=1 / args.samplerate)
            peaks, _ = find_peaks(magnitude, height=0)
            peak_indexes = peaks[np.argsort(magnitude[peaks])[-motor_count:]][::-1]

            for i, peak in enumerate(peak_indexes):
                if magnitude[peak] < 50000:
                    ser.write(
                        struct.pack(">BH", i, 0)
                    )
                else:
                    ser.write(
                        struct.pack(">BH", i, int(1000000 / freqs[peak]))
                    )
            for i in range(len(peak_indexes), motor_count):
                ser.write(
                    struct.pack(">BH", i, 0)
                )
            ser.flush()
