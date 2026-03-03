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

  play_note(mot1, Note(NOTE_E5, 124));
play_note(mot1, Note(NOTE_NONE, 1));
play_note(mot1, Note(NOTE_E5, 249));
play_note(mot1, Note(NOTE_NONE, 1));
play_note(mot1, Note(NOTE_E5, 124));
play_note(mot1, Note(NOTE_NONE, 126));
play_note(mot1, Note(NOTE_C5, 124));
play_note(mot1, Note(NOTE_NONE, 1));
play_note(mot1, Note(NOTE_E5, 124));
play_note(mot1, Note(NOTE_NONE, 126));
play_note(mot1, Note(NOTE_G5, 249));
play_note(mot1, Note(NOTE_NONE, 251));
play_note(mot1, Note(NOTE_G4, 249));
play_note(mot1, Note(NOTE_NONE, 251));
play_note(mot1, Note(NOTE_C5, 249));
play_note(mot1, Note(NOTE_NONE, 126));
play_note(mot1, Note(NOTE_G4, 249));
play_note(mot1, Note(NOTE_NONE, 126));
play_note(mot1, Note(NOTE_E4, 249));
play_note(mot1, Note(NOTE_NONE, 126));
play_note(mot1, Note(NOTE_A4, 249));
play_note(mot1, Note(NOTE_NONE, 1));
play_note(mot1, Note(NOTE_B4, 249));
play_note(mot1, Note(NOTE_NONE, 1));
play_note(mot1, Note(NOTE_AA4, 124));
play_note(mot1, Note(NOTE_NONE, 1));
play_note(mot1, Note(NOTE_A4, 124));
play_note(mot1, Note(NOTE_NONE, 126));
play_note(mot1, Note(NOTE_G4, 166));
play_note(mot1, Note(NOTE_NONE, 1));
play_note(mot1, Note(NOTE_E5, 166));
play_note(mot1, Note(NOTE_G5, 166));
play_note(mot1, Note(NOTE_NONE, 1));
play_note(mot1, Note(NOTE_A5, 249));
play_note(mot1, Note(NOTE_NONE, 1));
play_note(mot1, Note(NOTE_F5, 124));
play_note(mot1, Note(NOTE_NONE, 1));
play_note(mot1, Note(NOTE_G5, 124));
play_note(mot1, Note(NOTE_NONE, 126));
play_note(mot1, Note(NOTE_E5, 249));
play_note(mot1, Note(NOTE_NONE, 1));
play_note(mot1, Note(NOTE_C5, 124));
play_note(mot1, Note(NOTE_NONE, 1));
play_note(mot1, Note(NOTE_D5, 124));
play_note(mot1, Note(NOTE_NONE, 1));
play_note(mot1, Note(NOTE_B4, 124));
play_note(mot1, Note(NOTE_NONE, 251));
play_note(mot1, Note(NOTE_C5, 249));
play_note(mot1, Note(NOTE_NONE, 126));
play_note(mot1, Note(NOTE_G4, 249));
play_note(mot1, Note(NOTE_NONE, 126));
play_note(mot1, Note(NOTE_E4, 249));
play_note(mot1, Note(NOTE_NONE, 126));
play_note(mot1, Note(NOTE_A4, 249));
play_note(mot1, Note(NOTE_NONE, 1));
play_note(mot1, Note(NOTE_B4, 249));
play_note(mot1, Note(NOTE_NONE, 1));
play_note(mot1, Note(NOTE_AA4, 124));
play_note(mot1, Note(NOTE_NONE, 1));
play_note(mot1, Note(NOTE_A4, 124));
play_note(mot1, Note(NOTE_NONE, 126));
play_note(mot1, Note(NOTE_G4, 166));
play_note(mot1, Note(NOTE_NONE, 1));
play_note(mot1, Note(NOTE_E5, 166));
play_note(mot1, Note(NOTE_G5, 166));
play_note(mot1, Note(NOTE_NONE, 1));
play_note(mot1, Note(NOTE_A5, 249));
play_note(mot1, Note(NOTE_NONE, 1));
play_note(mot1, Note(NOTE_F5, 124));
play_note(mot1, Note(NOTE_NONE, 1));
play_note(mot1, Note(NOTE_G5, 124));
play_note(mot1, Note(NOTE_NONE, 126));
play_note(mot1, Note(NOTE_E5, 249));
play_note(mot1, Note(NOTE_NONE, 1));
play_note(mot1, Note(NOTE_C5, 124));
play_note(mot1, Note(NOTE_NONE, 1));
play_note(mot1, Note(NOTE_D5, 124));
play_note(mot1, Note(NOTE_NONE, 1));
play_note(mot1, Note(NOTE_B4, 124));

play_note(mot1, Note(NOTE_NONE, 2000));
}
