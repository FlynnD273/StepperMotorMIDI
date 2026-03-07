#! /bin/env python
import argparse
import mido
from StreamFile import stream_file
from StreamLive import stream_live
from StreamSpeaker import stream_speaker
import pulsectl

parser = argparse.ArgumentParser()
parser.add_argument(
    "-t", "--transpose", help="Transpose by semitones", default=0, type=int
)
parser.add_argument(
    "-p", "--port", help="Path to TTY stream", default="/dev/ttyACM0", type=str
)
subparsers = parser.add_subparsers()
file_parser = subparsers.add_parser("file", help="Stream a MIDI file")
file_parser.add_argument("file", help="Path to MIDI file to stream")
file_parser.set_defaults(func=stream_file)
midi_parser = subparsers.add_parser(
    "live", help="Stream MIDI events from a MIDI controller"
)
output_names = mido.get_input_names()
midi_parser.add_argument(
    "-d",
    "--device",
    help=f"Device name",
    choices=output_names,
    default="" if not not output_names else output_names[0],
)
midi_parser.set_defaults(func=stream_live)
speaker_parser = subparsers.add_parser("pipe", help="Stream raw audio bytes from stdio")
speaker_parser.add_argument(
    "-s",
    "--samplerate",
    default=48000,
)
speaker_parser.set_defaults(func=stream_speaker)

args = parser.parse_args()
args.func(args)

