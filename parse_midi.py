from typing import List
from mido import Message, MidiFile, tick2second

from tones import Note, get_enum_string


# mid = MidiFile("./midi_export.mid")
mid = MidiFile("./Mario Bros. - Super Mario Bros. Theme.mid")
# mid = MidiFile("Mario.mid")

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

piano = [Note(get_enum_string(i + 12), 0, 0) for i in range(128)]
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
all_notes = all_notes[:165]

motor_notes: List[List[Note]] = [[] for _ in range(3)]

last_added = -1

for note in all_notes:
    last_added += 1
    last_added = last_added % len(motor_notes)

    should_skip = False
    old_val = last_added
    while (
        motor_notes[last_added]
        and motor_notes[last_added][-1].time + motor_notes[last_added][-1].length
        >= note.time
    ):
        last_added += 1
        last_added = last_added % len(motor_notes)
        if last_added == old_val:
            should_skip = True
            break

    if should_skip:
        print("Skipped note", note)
    else:
        motor_notes[last_added].append(note)

with open("song.c", "w") as file:
    lines = ['#include "song.h"', ""]
    for i, notes in enumerate(motor_notes):
        body = "\n".join(["  " + i.to_note_command() for i in notes])
        lines.append(f"const note motor{i+1}_notes[] = {{\n{body}\n}};")
    file.write("\n".join(lines))

with open("song.h", "w") as file:
    lines = ["#ifndef SONG_H", "#define SONG_H", '#include "lib/tones.h"', ""]
    for i, notes in enumerate(motor_notes):
        lines.append(f"extern const note motor{i+1}_notes[{len(notes)}];")
        lines.append(f"const unsigned int motor{i+1}_notes_len = {len(notes)};")
    lines.append("#endif")
    file.write("\n".join(lines))

