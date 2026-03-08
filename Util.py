from serial import Serial
import struct
import signal
import sys


def get_serial(port: str) -> Serial:
    return Serial(port, 115200)


def send_note(ser: Serial, motor: int, period: int):
    if not (0 <= period <= 65535):
        print(f"{period} not in range [0, 54435]")
        period = 0
    ser.write(struct.pack("<BH", motor, period))
    ser.flush()


def stop_all(ser, count: int):
    for i in range(count):
        send_note(ser, i, 0)
        ser.flush()


def setup_exit_handler(ser: Serial, count: int):
    def signal_handler(ser, count: int):
        stop_all(ser, count)
        ser.close()
        sys.exit(0)

    signal.signal(signal.SIGINT, lambda _a, _b: signal_handler(ser, count))

