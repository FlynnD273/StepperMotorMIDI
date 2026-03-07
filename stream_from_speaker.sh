#! /bin/env bash

parec -d alsa_output.usb-Synaptics_CX31993_384Khz_HIFI_AUDIO-00.analog-stereo.monitor --format=s16le --rate=48000 --channels=1 --latency-msec=1 | ./stream_midi.py pipe $1
