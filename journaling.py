#!/usr/bin/env python
import os
import re
import sys
from pathlib import Path

def get_journals():
    p = Path('~/Dropbox/notes/journal/').expanduser()
    return list(p.glob('*.md'))


def main(keyword):
    for journal in get_journals():
        should_print = False
        for line in journal.read_text().splitlines():
            if line.startswith('#'):
                print(line)
            if line.lower().startswith(keyword.lower()):
                should_print=True
            if should_print and line == "":
                break
            if should_print:
                print('\t', line)


def keywords():
    words = set()
    for journal in get_journals():
        for line in journal.read_text().splitlines():
            first_word = line.split(' ')[0]
            if first_word and first_word[-1] == ':':
                words.add(first_word[:-1])
    return words


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('usage: journaling <KEYWORD>')
        print(f'\nKEYWORDS: {", ".join(sorted(keywords()))}')
        sys.exit(1)
    keyword = sys.argv[1]
    sys.exit(main(keyword))
