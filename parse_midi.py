from typing import List
from mido import Message, MidiFile, tick2second

from tones import Note, get_enum_string


# mid = MidiFile("./midi_export.mid")
mid = MidiFile("/home/flynn/Downloads/Artist_ Stromae & Pomme - Ma Meilleure Ennemie.mid")
# mid = MidiFile("Mario.mid")
SEMITONE_SHIFT = 0

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
all_notes = all_notes[:300]

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

for motor_idx, old_notes in enumerate(motor_notes):
    notes = [old_notes[0].clone()]
    for i in range(1, len(old_notes)):
        note = old_notes[i].clone()
        note.time = note.time - (old_notes[i - 1].time + old_notes[i - 1].length)
        notes.append(note)
    motor_notes[motor_idx] = notes

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

