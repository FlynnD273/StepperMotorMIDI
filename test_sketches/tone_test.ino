#include "lib/tones.h"

#define PIN_ENABLE 8
const motor mot1 = Motor(3, 6);
const int stepXPin = 2;  //X.STEP
const int dirXPin = 5;   // X.DIR
const int stepYPin = 3;  //Y.STEP
const int dirYPin = 6;   // Y.DIR
const int stepZPin = 4;  //Z.STEP
const int dirZPin = 7;   // Z.DIR

int stepPin = stepYPin;
int dirPin = dirYPin;

const int stepsPerRev = 200;
int pulseWidthMicros = 220;  // microseconds
int millisBtwnSteps = 220;

void setup() {
  Serial.begin(9600);
  pinMode(PIN_ENABLE, OUTPUT);
  digitalWrite(PIN_ENABLE, LOW);
  pinMode(stepPin, OUTPUT);
  pinMode(dirPin, OUTPUT);

  digitalWrite(dirPin, HIGH);
  Serial.println(F("CNC Shield Initialized"));
}

void loop() {
  play_note(mot1, Note(NOTE_A4, 1000));
  play_note(mot1, Note(NOTE_NONE, 1000));
}
