#include "lib/tones.h"
#include "song.h"

#define PIN_ENABLE 8
motor mot1 = Motor(3, 6);
const int stepXPin = 2;  // X.STEP
const int dirXPin = 5;   // X.DIR
const int stepYPin = 3;  // Y.STEP
const int dirYPin = 6;   // Y.DIR
const int stepZPin = 4;  // Z.STEP
const int dirZPin = 7;   // Z.DIR

void setup() {
  // Serial.begin(9600);
  pinMode(PIN_ENABLE, OUTPUT);
  digitalWrite(PIN_ENABLE, LOW);
  pinMode(mot1.stepPin, OUTPUT);
  pinMode(mot1.dirPin, OUTPUT);

  digitalWrite(mot1.dirPin, HIGH);
}

unsigned int motorr1_notes_len = sizeof(motor1_notes) / sizeof(note);

void loop() {
  if (mot1.note_index < motorr1_notes_len) {
    if (motor1_notes[mot1.note_index].millis * 1000 <= mot1.note_played_duration) {
      mot1.note_index++;
      mot1.note_played_duration = 0;
      if (motor1_notes[mot1.note_index].pitch != NOTE_NONE) {
        mot1.curr_dir++;
        mot1.curr_dir %= 4;
        digitalWrite(mot1.dirPin, (mot1.curr_dir < 2) ? LOW : HIGH);
      }
    }
    if (motor1_notes[mot1.note_index].pitch != NOTE_NONE) {
      if (mot1.note_played_duration % motor1_notes[mot1.note_index].pitch == 0) {
        digitalWrite(mot1.stepPin, (mot1.note_played_duration % (motor1_notes[mot1.note_index].pitch * 2))
                                     ? LOW
                                     : HIGH);
      }
    }
  }
  unsigned int mot1_delay = 1000000;
  if (mot1.note_index < motorr1_notes_len) {
    if (motor1_notes[mot1.note_index].pitch != NOTE_NONE) {
      mot1_delay =
        motor1_notes[mot1.note_index].pitch - (mot1.note_played_duration % motor1_notes[mot1.note_index].pitch);
    } else {
      mot1_delay = motor1_notes[mot1.note_index].millis;
    }
  }
  unsigned int min_delay = mot1_delay;
  delayMicroseconds(min_delay);
  mot1.note_played_duration += min_delay;
}
