from mido import Message, MidiFile, tick2second

from tones import Note, get_enum_string


mid = MidiFile("./Mario.mid")

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
            tick2second(curr.time, ticks_per_beat, tempo) * 1_000
        )
        all_notes.append(piano[curr.note])

all_notes = [n for n in all_notes if n.length > 0]
all_notes = sorted(all_notes, key=lambda x: x.start_time)

i = 0
while i < len(all_notes) - 1:
    curr_end = all_notes[i].start_time + all_notes[i].length
    next_start = all_notes[i + 1].start_time
    if curr_end < next_start:
        all_notes.insert(i + 1, Note("NOTE_NONE", curr_end, next_start - curr_end))
        i += 1
    i += 1

print("\n".join([i.to_note_command("mot1") for i in all_notes]))

