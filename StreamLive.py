from typing import List
import mido
from tones import Note, Pitches, get_enum_string
import struct
import serial
import time
import signal
import sys


class LiveMotor:
    index: int = 0
    playing: bool = False
    start_time: float = 0
    note: int = 0

    def __init__(self, index: int) -> None:
        self.index = index


def stream_live(args):
    motors = [LiveMotor(i) for i in range(3)]
    with serial.Serial("/dev/ttyACM0", 115200) as ser:

        def stop_all():
            for i in range(len(motors)):
                ser.write(struct.pack(">BH", i, 0))
                ser.flush()

        def signal_handler(sig, frame):
            stop_all()
            ser.close()
            sys.exit(0)

        signal.signal(signal.SIGINT, signal_handler)
        time.sleep(2)
        print("Ready.")
        with mido.open_input(args.device) as port:  # type: ignore
            while True:
                msg = port.receive()
                if msg.type != "note_on" and msg.type != "note_off":
                    continue

                curr_time = time.time()
                if msg.type == "note_on" and msg.velocity == 0:
                    msg = Message("note_off", note=msg.note, velocity=msg.velocity)  # type: ignore

                if msg.type == "note_off":
                    for motor in motors:
                        if motor.note == msg.note:
                            motor.playing = False
                            ser.write(struct.pack(">BH", motor.index, 0))
                            ser.flush()
                else:
                    earliest_motor = None
                    for i in range(len(motors)):
                        if not motors[i].playing and (
                            earliest_motor is None
                            or motors[i].start_time <= earliest_motor.start_time
                        ):
                            earliest_motor = motors[i]

                    if earliest_motor is None:
                        for i in range(len(motors)):
                            if (
                                earliest_motor is None
                                or motors[i].start_time <= earliest_motor.start_time
                            ):
                                earliest_motor = motors[i]

                    pitch_str = get_enum_string(msg.note + args.transpose)
                    if pitch_str in Pitches and earliest_motor is not None:
                        earliest_motor.playing = True
                        earliest_motor.start_time = curr_time
                        earliest_motor.note = msg.note
                        ser.write(
                            struct.pack(">BH", earliest_motor.index, Pitches[pitch_str])
                        )
                        ser.flush()

