#include "lib/tones.h"
#include "song.h"

#define MIN(a,b) ((a) < (b) ? (a) : (b))

#define PIN_ENABLE 8
motor mot1 = Motor(3, 6);
motor mot2 = Motor(2, 5);
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
  pinMode(mot2.stepPin, OUTPUT);
  pinMode(mot2.dirPin, OUTPUT);
}



unsigned int perform_motor_tick(motor *mot, note notes[], unsigned int notes_len) {
  motor stack_mot;
  memcpy(&stack_mot, mot, sizeof(motor));
  note curr_note = notes[stack_mot.note_index];
  if (stack_mot.note_index >= notes_len) {
    return 1000000;
  }

  if (curr_note.millis * 1000 <= stack_mot.note_played_duration) {
    (*mot).note_index++;
    stack_mot.note_index = mot->note_index;
    (*mot).note_played_duration = 0;
    stack_mot.note_played_duration = mot->note_played_duration;
    if (curr_note.pitch != NOTE_NONE) {
      (*mot).curr_dir++;
      (*mot).curr_dir %= 4;
      stack_mot.curr_dir = mot->curr_dir;
      digitalWrite(stack_mot.dirPin, (stack_mot.curr_dir < 2) ? LOW : HIGH);
    }
  }
  curr_note = notes[stack_mot.note_index];
  unsigned int delay_dur = 1000000;
  if (stack_mot.note_index < notes_len) {
    if (curr_note.pitch != NOTE_NONE) {
      if (stack_mot.note_played_duration % curr_note.pitch == 0) {
        digitalWrite(stack_mot.stepPin, (stack_mot.note_played_duration % (curr_note.pitch * 2))
                                     ? LOW
                                     : HIGH);
      }
    }

    if (curr_note.pitch != NOTE_NONE) {
      delay_dur =
        curr_note.pitch - (stack_mot.note_played_duration % curr_note.pitch);
    } else {
      delay_dur = curr_note.millis * 1000;
    }
  }
  return delay_dur;
}

void loop() {
  unsigned int min_delay = MIN(perform_motor_tick(&mot1, motor1_notes,motor1_notes_len), perform_motor_tick(&mot2, motor2_notes,motor2_notes_len));
  delayMicroseconds(min_delay);
  mot1.note_played_duration += min_delay;
  mot2.note_played_duration += min_delay;
}
