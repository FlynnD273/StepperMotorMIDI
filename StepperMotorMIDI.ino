#include "lib/tones.h"

#define PIN_ENABLE 8
motor motors[] = {
  Motor(3, 6),
  Motor(2, 5),
  Motor(4, 7),
  Motor(12, 13),
};

void init_motor(motor *mot) {
  pinMode(mot->stepPin, OUTPUT);
  pinMode(mot->dirPin, OUTPUT);
  (*mot).period = 0;
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


void perform_motor_tick(motor *mot, unsigned long now) {
  if (mot->period > 0 && now > mot->next_step) {
    digitalWrite(mot->stepPin, HIGH);
    digitalWrite(mot->stepPin, LOW);
    (*mot).next_step = now + mot->period * 2;
  }
}

unsigned char index;
unsigned short period;
unsigned char s_note[sizeof(index) + sizeof(period)];

void loop() {
  unsigned long now = micros();
  while (Serial.available() >= sizeof(s_note)) {
    Serial.readBytes(s_note, sizeof(s_note));

    index = s_note[0];
    period = s_note[1] | (s_note[2] << 8);// | (s_note[3] << 8*2) | (s_note[4] << 8*3);
    motors[index].period = period;
    // notes[index].pitch = pitch;
    // if (pitch != NOTE_NONE) {
    //   motor *mot = &motors[index];
    //   mot->curr_dir++;
    //   mot->curr_dir %= 4;
    //   digitalWrite(mot->dirPin, (mot->curr_dir < 2) ? LOW : HIGH);
    // }
  }
  for (unsigned char i = 0; i < sizeof(motors) / sizeof(motor); i++) {
    perform_motor_tick(&motors[i], now);
  }
}
