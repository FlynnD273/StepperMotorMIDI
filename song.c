#include "song.h"

const note motor2_notes[] = {
    Note(NOTE_C5, 500),  Note(NOTE_D5, 1000), Note(NOTE_E5, 500),
    Note(NOTE_F5, 1000), Note(NOTE_G5, 500),  Note(NOTE_A5, 1000),
    Note(NOTE_B5, 500),  Note(NOTE_C6, 1000),
};
const note motor1_notes[] = {
    Note(NOTE_C5, 1000), Note(NOTE_D5, 500),  Note(NOTE_E5, 1000),
    Note(NOTE_F5, 500),  Note(NOTE_G5, 1000), Note(NOTE_A5, 500),
    Note(NOTE_B5, 1000), Note(NOTE_C6, 500),
};

// const note motor1_notes[] = {
//     Note(NOTE_E5, 124),   Note(NOTE_NONE, 1),   Note(NOTE_E5, 249),
//     Note(NOTE_NONE, 1),   Note(NOTE_E5, 124),   Note(NOTE_NONE, 126),
//     Note(NOTE_C5, 124),   Note(NOTE_NONE, 1),   Note(NOTE_E5, 124),
//     Note(NOTE_NONE, 126), Note(NOTE_G5, 249),   Note(NOTE_NONE, 251),
//     Note(NOTE_G4, 249),   Note(NOTE_NONE, 251), Note(NOTE_C5, 249),
//     Note(NOTE_NONE, 126), Note(NOTE_G4, 249),   Note(NOTE_NONE, 126),
//     Note(NOTE_E4, 249),   Note(NOTE_NONE, 126), Note(NOTE_A4, 249),
//     Note(NOTE_NONE, 1),   Note(NOTE_B4, 249),   Note(NOTE_NONE, 1),
//     Note(NOTE_AA4, 124),  Note(NOTE_NONE, 1),   Note(NOTE_A4, 124),
//     Note(NOTE_NONE, 126), Note(NOTE_G4, 166),   Note(NOTE_NONE, 1),
//     Note(NOTE_E5, 166),   Note(NOTE_G5, 166),   Note(NOTE_NONE, 1),
//     Note(NOTE_A5, 249),   Note(NOTE_NONE, 1),   Note(NOTE_F5, 124),
//     Note(NOTE_NONE, 1),   Note(NOTE_G5, 124),   Note(NOTE_NONE, 126),
//     Note(NOTE_E5, 249),   Note(NOTE_NONE, 1),   Note(NOTE_C5, 124),
//     Note(NOTE_NONE, 1),   Note(NOTE_D5, 124),   Note(NOTE_NONE, 1),
//     Note(NOTE_B4, 124),   Note(NOTE_NONE, 251), Note(NOTE_C5, 249),
//     Note(NOTE_NONE, 126), Note(NOTE_G4, 249),   Note(NOTE_NONE, 126),
//     Note(NOTE_E4, 249),   Note(NOTE_NONE, 126), Note(NOTE_A4, 249),
//     Note(NOTE_NONE, 1),   Note(NOTE_B4, 249),   Note(NOTE_NONE, 1),
//     Note(NOTE_AA4, 124),  Note(NOTE_NONE, 1),   Note(NOTE_A4, 124),
//     Note(NOTE_NONE, 126), Note(NOTE_G4, 166),   Note(NOTE_NONE, 1),
//     Note(NOTE_E5, 166),   Note(NOTE_G5, 166),   Note(NOTE_NONE, 1),
//     Note(NOTE_A5, 249),   Note(NOTE_NONE, 1),   Note(NOTE_F5, 124),
//     Note(NOTE_NONE, 1),   Note(NOTE_G5, 124),   Note(NOTE_NONE, 126),
//     Note(NOTE_E5, 249),   Note(NOTE_NONE, 1),   Note(NOTE_C5, 124),
//     Note(NOTE_NONE, 1),   Note(NOTE_D5, 124),   Note(NOTE_NONE, 1),
//     Note(NOTE_B4, 124),
// };
