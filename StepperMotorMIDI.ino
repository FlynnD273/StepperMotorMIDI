#include "lib/tones.h"

#define PIN_ENABLE 8
motor motors[] = {
  Motor(3, 6),
  Motor(2, 5),
  Motor(4, 7),
};
motor mot4 = Motor(12, 13);

note notes[3];

void init_motor(motor *mot) {
  pinMode(mot->stepPin, OUTPUT);
  pinMode(mot->dirPin, OUTPUT);
  (*mot).note_index = 0;
  (*mot).curr_dir = 0;
  (*mot).next_step = 0;
}

void setup() {
  Serial.begin(115200);
  pinMode(PIN_ENABLE, OUTPUT);
  digitalWrite(PIN_ENABLE, LOW);
  for (unsigned char i = 0; i < sizeof(motors) / sizeof(motor); i++) {
    init_motor(&motors[i]);
  }
}


void perform_motor_tick(motor *mot, note curr_note, unsigned long now) {
  if (curr_note.pitch != NOTE_NONE && now > mot->next_step) {
    digitalWrite(mot->stepPin, HIGH);
    digitalWrite(mot->stepPin, LOW);
    (*mot).next_step = now + curr_note.pitch * 2;
  }
}

unsigned char s_note[3];

void loop() {
  unsigned long now = micros();
  while (Serial.available() >= 3) {
    Serial.readBytes(s_note, sizeof(s_note));

    unsigned char index = s_note[0];
    Pitch pitch = (Pitch)((s_note[1] << 8) | s_note[2]);
    notes[index].pitch = pitch;
    // if (pitch != NOTE_NONE) {
    //   motor *mot = &motors[index];
    //   mot->curr_dir++;
    //   mot->curr_dir %= 4;
    //   digitalWrite(mot->dirPin, (mot->curr_dir < 2) ? LOW : HIGH);
    // }
  }
  for (unsigned char i = 0; i < sizeof(motors) / sizeof(motor); i++) {
    perform_motor_tick(&motors[i], notes[i], now);
  }
}
