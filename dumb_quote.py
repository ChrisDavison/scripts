#!/usr/bin/env python

from argparse import ArgumentParser
import fileinput
import re
import sys
import shutil


parser = ArgumentParser("dumbquote")
parser.add_argument("--stream", help="Operate line-by-line")
parser.add_argument("files", nargs="+", help="Files to operate on")
args = parser.parse_args()

singles = re.compile("""[‘’]""")
doubles = re.compile("""[“”]""")

def streaming_mode(filename, outpath):
    with open(filename, "r") as f_in:
        with open(outpath, "w") as f_out:
            for line in f_in:
                f_out.write(doubles.sub('"', singles.sub("'", line)))


def all_in_one_mode(filename, outpath):
    contents = open(filename).read()
    with open(outpath, "w") as f_out:
        f_out.write(doubles.sub('"', singles.sub("'", contents)))


for filename in args.files:
    outpath = filename + ".dumbquote"
    if args.stream:
        streaming_mode(filename, outpath)
    else:
        all_in_one_mode(filename, outpath)
    shutil.move(outpath, filename)
