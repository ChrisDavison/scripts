#!/usr/bin/env python
from argparse import ArgumentParser
from pathlib import Path
import re

parser = ArgumentParser()
parser.add_argument('files', help='files to count headers in', nargs='+')
parser.add_argument('--sym', help='header symbol', default=b'#', type=bytes)
args = parser.parse_args()


notes = [Path(f) for f in args.files]

filter_words = ['book-', 'logbook', 'asmr', 'gaming', 'programming']

min_count = 5

def header_count(note, symbol):
    re_header = re.compile(symbol + b"+ ")
    note_text = note.read_bytes().split(b'\n')
    lines_with_headers = sum(1 for line in note_text if re_header.match(line))
    return lines_with_headers

notes_and_count = [(header_count(n, args.sym), n.stem) for n in notes]
sorted_notes = sorted(notes_and_count, reverse=True)

for note in sorted_notes:
    if any([p in note[1] for p in filter_words]):
        continue
    if note[0] < min_count:
        continue
    print(note[0], '\t', note[1])
