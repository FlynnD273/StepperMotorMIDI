#pragma once

// enum Pitch {
//   NOTE_C1 = 30581,
//   NOTE_CC1 = 28868,
//   NOTE_D1 = 27248,
//   NOTE_DD1 = 25707,
//   NOTE_E1 = 24272,
//   NOTE_F1 = 22904,
//   NOTE_FF1 = 21626,
//   NOTE_G1 = 20408,
//   NOTE_GG1 = 19260,
//   NOTE_A1 = 18182,
//   NOTE_AA1 = 17159,
//   NOTE_B1 = 16197,
//   NOTE_C2 = 15291,
//   NOTE_CC2 = 14430,
//   NOTE_D2 = 13620,
//   NOTE_DD2 = 12857,
//   NOTE_E2 = 12136,
//   NOTE_F2 = 11455,
//   NOTE_FF2 = 10811,
//   NOTE_G2 = 10204,
//   NOTE_GG2 = 9632,
//   NOTE_A2 = 9091,
//   NOTE_AA2 = 8581,
//   NOTE_B2 = 8098,
//   NOTE_C3 = 7644,
//   NOTE_CC3 = 7215,
//   NOTE_D3 = 6810,
//   NOTE_DD3 = 6428,
//   NOTE_E3 = 6067,
//   NOTE_F3 = 5727,
//   NOTE_FF3 = 5405,
//   NOTE_G3 = 5102,
//   NOTE_GG3 = 4816,
//   NOTE_A3 = 4545,
//   NOTE_AA3 = 4290,
//   NOTE_B3 = 4050,
//   NOTE_C4 = 3822,
//   NOTE_CC4 = 3608,
//   NOTE_D4 = 3405,
//   NOTE_DD4 = 3214,
//   NOTE_E4 = 3034,
//   NOTE_F4 = 2864,
//   NOTE_FF4 = 2703,
//   NOTE_G4 = 2551,
//   NOTE_GG4 = 2408,
//   NOTE_A4 = 2273,
//   NOTE_AA4 = 2145,
//   NOTE_B4 = 2025,
//   NOTE_C5 = 1911,
//   NOTE_CC5 = 1804,
//   NOTE_D5 = 1703,
//   NOTE_DD5 = 1607,
//   NOTE_E5 = 1517,
//   NOTE_F5 = 1432,
//   NOTE_FF5 = 1351,
//   NOTE_G5 = 1276,
//   NOTE_GG5 = 1204,
//   NOTE_A5 = 1136,
//   NOTE_AA5 = 1073,
//   NOTE_B5 = 1012,
//   NOTE_C6 = 956,
//   NOTE_CC6 = 902,
//   NOTE_D6 = 851,
//   NOTE_DD6 = 804,
//   NOTE_E6 = 758,
//   NOTE_F6 = 716,
//   NOTE_FF6 = 676,
//   NOTE_G6 = 638,
//   NOTE_GG6 = 602,
//   NOTE_A6 = 568,
//   NOTE_AA6 = 536,
//   NOTE_B6 = 506,
//   NOTE_C7 = 478,
//   NOTE_CC7 = 451,
//   NOTE_D7 = 426,
//   NOTE_DD7 = 402,
//   NOTE_E7 = 379,
//   NOTE_F7 = 358,
//   NOTE_FF7 = 338,
//   NOTE_G7 = 319,
//   NOTE_GG7 = 301,
//   NOTE_A7 = 284,
//   NOTE_AA7 = 268,
//   NOTE_B7 = 253,
//   NOTE_C8 = 239,
//   NOTE_CC8 = 225,
//   NOTE_D8 = 213,
//   NOTE_DD8 = 201,
//   NOTE_E8 = 190,
//   NOTE_F8 = 179,
//   NOTE_FF8 = 169,
//   NOTE_G8 = 159,
//   NOTE_GG8 = 150,
//   NOTE_A8 = 142,
//   NOTE_AA8 = 134,
//   NOTE_B8 = 127,
//   NOTE_C9 = 119,
//   NOTE_CC9 = 113,
//   NOTE_D9 = 106,
//   NOTE_DD9 = 100,
//   NOTE_E9 = 95,
//   NOTE_F9 = 89,
//   NOTE_FF9 = 84,
//   NOTE_G9 = 80,
//   NOTE_GG9 = 75,
//   NOTE_A9 = 71,
//   NOTE_AA9 = 67,
//   NOTE_B9 = 64,
//   NOTE_NONE = 0,
// };

typedef struct note {
  unsigned short pitch;
  unsigned int delay_millis;
  unsigned int millis;
} note;

#define Note(pitch, delay_millis, millis)                                      \
  ((note){(pitch), (delay_millis), (millis)})

typedef struct motor {
  unsigned char stepPin;
  unsigned char dirPin;
  char curr_dir;
  char last_write_high;
  unsigned int period;
  unsigned long next_step;
  unsigned long note_end_time;
} motor;

#define Motor(stepPin, dirPin) ((motor){(stepPin), (dirPin), 0, 0, 0, 0, 0})

void play_note(motor motor, note note);
