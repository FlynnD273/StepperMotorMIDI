class Note:
    def __init__(self, pitch: str, time: int, length: int):
        self.pitch = pitch
        self.time = time
        self.length = length

    def __str__(self) -> str:
        return f"{self.pitch} [{self.time}, {self.length}]"

    def to_note_command(self) -> str:
        return f"Note({self.pitch}, {self.time}, {self.length}),"

    def clone(self):
        return Note(self.pitch, self.time, self.length)


def get_enum_string(note: int) -> str:
    labels = [
        "NOTE_C",
        "NOTE_CC",
        "NOTE_D",
        "NOTE_DD",
        "NOTE_E",
        "NOTE_F",
        "NOTE_FF",
        "NOTE_G",
        "NOTE_GG",
        "NOTE_A",
        "NOTE_AA",
        "NOTE_B",
    ]
    note -= 2 * 12
    return labels[note % len(labels)] + str(note // len(labels))

