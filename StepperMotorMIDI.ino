#include "lib/tones.h"
#include "song.h"

#define MIN(a,b) ((a) < (b) ? (a) : (b))

#define PIN_ENABLE 8
motor mot1 = Motor(3, 6);
motor mot2 = Motor(2, 5);
motor mot3 = Motor(4, 7);
motor mot4 = Motor(12, 13);

void setup() {
  // Serial.begin(9600);
  pinMode(PIN_ENABLE, OUTPUT);
  digitalWrite(PIN_ENABLE, LOW);
  pinMode(mot1.stepPin, OUTPUT);
  pinMode(mot1.dirPin, OUTPUT);
  pinMode(mot2.stepPin, OUTPUT);
  pinMode(mot2.dirPin, OUTPUT);
  pinMode(mot3.stepPin, OUTPUT);
  pinMode(mot3.dirPin, OUTPUT);
}



void perform_motor_tick(motor *mot, note notes[], unsigned int notes_len, unsigned long now) {
  if (mot->note_index >= notes_len) return;

  note curr_note = notes[mot->note_index];

  if (now >= (curr_note.start_millis + curr_note.millis) * 1000) {
    (*mot).note_index++;
    if (mot->note_index >= notes_len) return;
    curr_note = notes[mot->note_index];
    (*mot).next_step = curr_note.start_millis * 1000;
    if (curr_note.pitch != NOTE_NONE) {
      (*mot).curr_dir++;
      (*mot).curr_dir %= 4;
      digitalWrite(mot->dirPin, (mot->curr_dir < 2) ? LOW : HIGH);
    }
  }
  if (curr_note.pitch != NOTE_NONE && mot->next_step < now) {
    digitalWrite(mot->stepPin, HIGH);
    digitalWrite(mot->stepPin, LOW);
    (*mot).next_step = now + curr_note.pitch * 2;
  }
}

void loop() {
  unsigned long now = micros();
  perform_motor_tick(&mot1, motor1_notes, motor1_notes_len, now);
  perform_motor_tick(&mot2, motor2_notes, motor2_notes_len, now);
  perform_motor_tick(&mot3, motor3_notes, motor3_notes_len, now);
}
