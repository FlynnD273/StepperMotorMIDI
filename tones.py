class Note:
    def __init__(self, pitch: str, start_time: int, length: int):
        self.pitch = pitch
        self.start_time = start_time
        self.length = length

    def __str__(self) -> str:
        return f"{self.pitch} [{self.start_time}, {self.length}]"

    def to_note_command(self, motor: str) -> str:
        return f"play_note({motor}, Note({self.pitch}, {self.length}));"

    def clone(self):
        return Note(self.pitch, self.start_time, self.length)


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

