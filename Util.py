from serial import Serial
import struct
import signal
import sys
import time

MOTOR_COUNT = 4


def get_serial(port: str) -> Serial:
    return Serial(port, 115200)


last_sent = [0] * MOTOR_COUNT


def send_note(ser: Serial, motor: int, period: int):
    if motor < 0 or motor >= MOTOR_COUNT or last_sent[motor] == period:
        return
    UPPER = 2**16
    if not (0 <= period < UPPER):
        print(f"{period} not in range [0, {UPPER}]")
        period = 0
    ser.write(struct.pack("<BH", motor, period))
    ser.flush()
    last_sent[motor] = period


def stop_all(ser):
    for i in range(MOTOR_COUNT):
        send_note(ser, i, 0)


def setup_exit_handler(ser: Serial):
    def signal_handler(ser):
        print("Exiting...")
        stop_all(ser)
        ser.close()
        sys.exit(0)

    signal.signal(signal.SIGINT, lambda _a, _b: signal_handler(ser))
    time.sleep(3)
    print("Ready.")

