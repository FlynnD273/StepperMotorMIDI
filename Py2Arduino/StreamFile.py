from typing import List
from mido import Message, MidiFile, tick2second
from tones import Note, Pitches, get_enum_string, Motor
import time
from Util import get_serial, send_note, setup_exit_handler, stop_all


def stream_file(args):
    mid = MidiFile(args.file)
    SEMITONE_SHIFT = args.transpose

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
    total_time = 0
    for i in range(len(all_messages)):
        curr = all_messages[i]
        total_time += curr.time
        if curr.type == "note_on":
            piano[curr.note] = Note(
                piano[curr.note].pitch,
                round(tick2second(total_time, ticks_per_beat, tempo) * 1_000),
                0,
            )
        elif curr.type == "note_off":
            piano[curr.note].length = round(
                tick2second(total_time, ticks_per_beat, tempo) * 1_000
                - piano[curr.note].time
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

    motors = [Motor() for _ in motor_notes]
    with get_serial(args.port) as ser:
        setup_exit_handler(ser, len(motors))
        time.sleep(2)
        print("Ready.")
        try:
            time_offset = time.time_ns() // 1_000_000
            while True:
                total_time = time.time_ns() // 1_000_000 - time_offset
                skipped = 0
                for i, (motor, notes) in enumerate(zip(motors, motor_notes)):
                    if motor.index >= len(notes):
                        skipped += 1
                        continue
                    if not motor.playing and total_time > notes[motor.index].time:
                        motor.playing = True
                        send_note(ser, i, Pitches[notes[motor.index].pitch])
                    if motor.playing and total_time > motor.end_time:
                        motor.index += 1
                        if motor.index >= len(notes):
                            motor.playing = False
                            send_note(ser, i, 0)
                            continue
                        motor.end_time = (
                            notes[motor.index].time + notes[motor.index].length
                        )
                        motor.playing = False
                        if notes[motor.index].time > 0:
                            send_note(ser, i, 0)
                if skipped == len(motors):
                    break
        except Exception as e:
            stop_all(ser, len(motors))
            raise e

        print("Done.")
        stop_all(ser, len(motors))

