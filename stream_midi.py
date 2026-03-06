#! /bin/env python
from typing import List
from mido import Message, MidiFile, tick2second
from tones import Note, Pitches, get_enum_string
import struct
import serial
from time import sleep, time_ns
import signal
import sys

mid = MidiFile(sys.argv[1])
SEMITONE_SHIFT = 0 if len(sys.argv) < 3 else int(sys.argv[2])

ticks_per_beat = mid.ticks_per_beat
tempo = 500000

all_messages = []

for track in mid.tracks:
    for msg in track:
        if msg.type == "note_on" or msg.type == "note_off":
            if msg.type == "note_on" and msg.velocity == 0:
                msg = Message(
                    "note_off", note=msg.note, velocity=msg.velocity, time=msg.time
                )
            all_messages.append(msg)  # type: ignore
        elif msg.type == "set_tempo":
            tempo = msg.tempo

piano = [Note(get_enum_string(i + SEMITONE_SHIFT + 12), 0, 0) for i in range(128)]
all_notes = []
time = 0
for i in range(len(all_messages)):
    curr = all_messages[i]
    time += curr.time
    if curr.type == "note_on":
        piano[curr.note] = Note(
            piano[curr.note].pitch,
            round(tick2second(time, ticks_per_beat, tempo) * 1_000),
            0,
        )
    elif curr.type == "note_off":
        piano[curr.note].length = round(
            tick2second(time, ticks_per_beat, tempo) * 1_000 - piano[curr.note].time
        )
        all_notes.append(piano[curr.note].clone())

all_notes = [n for n in all_notes if n.length > 0]
all_notes = sorted(all_notes, key=lambda x: x.time)

motor_notes: List[List[Note]] = [[] for _ in range(3)]

for note in all_notes:
    earliest_end = note.time + 99999
    earliest_index = -1
    for i, motor in enumerate(motor_notes):
        if len(motor) == 0:
            earliest_index = i
            earliest_end = 0
            break
        end = motor[-1].time + motor[-1].length
        if end < earliest_end and note.time > motor[-1].time:
            earliest_index = i
            earliest_end = end

    if earliest_index != -1:
        early = motor_notes[earliest_index]
        early.append(note)
        if len(early) > 1 and early[-2].time + early[-2].length > early[-1].time:
            early[-2].length = early[-1].time - early[-2].time
    else:
        print("Skipping note", note)


class Motor:
    index: int = 0
    end_time: int = 0
    playing: bool = False


motors = [Motor() for _ in motor_notes]
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
    sleep(2)
    try:
        time_offset = time_ns() // 1000000
        while True:
            time = time_ns() // 1000000 - time_offset
            skipped = 0
            for i, (motor, notes) in enumerate(zip(motors, motor_notes)):
                if motor.index >= len(notes):
                    skipped += 1
                    continue
                if not motor.playing and time > notes[motor.index].time:
                    motor.playing = True
                    ser.write(struct.pack(">BH", i, Pitches[notes[motor.index].pitch]))
                    ser.flush()
                if time > motor.end_time:
                    motor.index += 1
                    if motor.index >= len(notes):
                        ser.write(struct.pack(">BH", i, 0))
                        ser.flush()
                        continue
                    motor.end_time = notes[motor.index].time + notes[motor.index].length
                    motor.playing = False
                    if notes[motor.index].time > 0:
                        ser.write(struct.pack(">BH", i, 0))
                        ser.flush()
            if skipped == len(motors):
                break
    except Exception as e:
        stop_all()
        raise e

    print("Done")
    stop_all()

