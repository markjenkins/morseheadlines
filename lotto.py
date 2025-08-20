#!/usr/bin/env python3

# Conduct a daily fake morse lottery to test your number skills
#
# Copyright (c) 2025 Mark Jenkins <mark@markjenkins.ca>
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from io import StringIO

from datetime import date
from os.path import splitext

# note, this is not cryptographically strong, don't conduct a real
# lotto with this!
#
# for strong crypto random use random.SystemRandom
from random import sample

# the cduck_morse code doesn't come as an installable package
# my version with workableAsLibrary branch
# https://github.com/markjenkins/cduck_morse/tree/workableAsLibrary
# works by including an __init__.py and changing the import statements
#
# name the directory cduck_morse and make available the python path
# My version is also available in this project as a sub-module
from cduck_morse.play import FREQ, main as cduck_play_main
from cduck_morse.morseTable import forwardTable as MORSE_TABLE

# eventually there will be multiple output speeds that can be chosen
from morsegendefaults import DEFAULT_WPM, DEFAULT_FS

BALLS=10
FIRST_BALL=0

PICKED_BALLS=3

DRAWN_BALLS=4

AVAIL_BALLS = tuple(str(i) for i in range(FIRST_BALL, FIRST_BALL+BALLS))

BALL_SEP = " " #

NUM_DRAWS = 3

def conduct_draw(avail_balls, picked, drawn, output):
    p_sample = sample(avail_balls, picked)
    output.write("ur n ")
    output.write( BALL_SEP.join(p_sample) )
    output.write("\n=\n")
    dr_sample = sample(avail_balls, drawn)
    output.write("drawn ")
    output.write( BALL_SEP.join(dr_sample) )
    output.write("\n=\n")
    overlap = set(p_sample).intersection(set(dr_sample))
    if len(overlap)==0:
        print("nm", file=output)
    else:
        output.write("m ")
        print(BALL_SEP.join(overlap), file=output)

def conduct_day_of_lotto_draws(draws, avail_balls, picked, drawn):
    sio = StringIO()
    today = date.today()

    print(
        ("Your daily morse lottery for %d %02d %02d" % (today.year, today.month, today.day) ), file=sio)
    for i in range(1, draws+1):
        print("= Draw %d" % i, file=sio)
        conduct_draw(avail_balls, picked, drawn, sio)
    return sio.getvalue()

def main():
    from sys import argv
    lotto_text = conduct_day_of_lotto_draws(
        NUM_DRAWS, AVAIL_BALLS, PICKED_BALLS, DRAWN_BALLS)

    file_argument_without_suffix, suffix = splitext(argv[1])
    if suffix.lower() == ".wav":
        file_w_wav_suffix = argv[1]
    else:
        file_w_wav_suffix = file_argument_without_suffix + ".wav"

    cduck_play_main(lotto_text, # message
                    FREQ, # freq
                    DEFAULT_WPM, # wpm
                    DEFAULT_FS, # fs
                    None, # prompt
                    file_w_wav_suffix) # outFile output filename

    with open(file_argument_without_suffix + '.txt', 'w') as f:
        f.write(lotto_text)

if __name__ == "__main__":
    main()
