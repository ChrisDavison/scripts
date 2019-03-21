#!/usr/bin/env python3
"""
usage: journaling.py KEYWORD

Display all journal entries that are based on KEYWORD.
Keywords: strength, life, fitness, diet, self-improvement

options:
    -h --help  Show this message
"""
import os
import re
import sys
import textwrap
from pathlib import Path
from docopt import docopt

def get_journals():
    p = Path('~/Dropbox/notes/journal/').expanduser()
    return list(p.glob('*.md'))


def main(keyword):
    header = f"Journals about {keyword.lower()}"
    print(header)
    print('='*len(header))
    for journal in get_journals():
        should_print = False
        paragraph = ""
        for line in journal.read_text().splitlines():
            if line.startswith('#'):
                paragraph = line + "\n"
            if line.lower().startswith(keyword.lower()):
                should_print=True
            if should_print and line == "":
                break
            if should_print:
                paragraph += line + "\n"
        print(paragraph)


if __name__ == "__main__":
    args = docopt(__doc__)
    main(args['KEYWORD'])
