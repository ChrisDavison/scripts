#!/usr/bin/env python
from pathlib import Path

notes = list((Path('~').expanduser() / 'Dropbox' / 'notes').glob('*.org'))

filter_words = ['book-', 'logbook', 'asmr', 'gaming', 'programming']

min_count = 5

def header_count(note):
    note_text = note.read_bytes().split(b'\n')
    return len([l for l in note_text if l.startswith(b'*')])

notes_and_count = [(header_count(n), n.stem) for n in notes]
sorted_notes = sorted(notes_and_count, reverse=True)

for note in sorted_notes:
    if any([p in note[1] for p in filter_words]):
        continue
    if note[0] < min_count:
        continue
    print(note[0], '\t', note[1])
