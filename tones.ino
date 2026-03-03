#include "lib/tones.h"

void play_note(motor motor, note note) {
  if (note.pitch == 0) {
    delay(note.millis);
    return;
  }
  unsigned long total_time = 0;
  while (total_time < note.millis) {
    digitalWrite(motor.step, HIGH);
    delayMicroseconds(note.pitch);
    digitalWrite(motor.step, LOW);
    delayMicroseconds(note.pitch);
    total_time += note.pitch * 2 / 1000;
  }
}
