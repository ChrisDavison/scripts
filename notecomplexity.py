#!/usr/bin/env python
from pathlib import Path
import sys

notes = Path(sys.argv[1]).rglob('*.org')

def note_complexity(notepath):
    contents = notepath.read_bytes().split(b'\n')
    complexity = 0
    for line in contents:
        first_word = line.split(b' ')[0]
        chars_in_first_word = list(set(first_word))
        if list(chars_in_first_word) == [ord('*')]:
            complexity += len(first_word)
    return complexity

notes_and_complexity = sorted([(note_complexity(n), n) for n in notes], reverse=True)
for note in notes_and_complexity:
    print(f"{note[0]:4d}\t{note[1]}")
