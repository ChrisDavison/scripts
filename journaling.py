#!/usr/bin/env python3
"""
usage: 
    journaling.py show [-s] KEYWORD
    journaling.py keywords|kw

Display all journal entries that are based on KEYWORD,
or list all possible keywords.

options:
    -h --help    Show this message
    -s           Step through entries [default: False]
"""
import os
import re
import shutil
import sys
import textwrap
from pathlib import Path
from docopt import docopt


JOURNALPATH = Path('~/Dropbox/notes/journal/').expanduser()


def paragraphs(data):
    """Split text into paragraphs.

    Join consecutive lines of text, 
    yielding text whenever there is a newline"""
    paragraph = ''
    for line in data:
        if line:
            paragraph += f" {line}"
        else:
            yield paragraph.lstrip()
            paragraph = ''
    if paragraph:
        yield paragraph


def display_matching_section(keyword):
    """Display header'd paragraph containing keyword"""
    low = keyword.lower()
    cols = shutil.get_terminal_size()[0] - 4
    def display(path):
        """Returns None if no section matched, or True on success"""
        text = path.read_text().splitlines()
        section = ' '.join([p for p in paragraphs(text)
                if p.lower().startswith(keyword.lower())])
        if not section:
            return None
        displayname = ' '.join(path.stem.split('-'))
        header = str(displayname).center(cols, ' ')
        overline = "="*len(header)
        underline = "-"*len(header)
        content = textwrap.fill(section, cols)
        msg = f"{overline}\n{header}\n{underline}\n{content}\n"
        print(msg)
        return True
    return display


def keywords():
    kw = set()
    for journal in list(JOURNALPATH.glob('*.md')):
        data = journal.read_text()
        m = re.findall('\n([a-zA-Z\-]+):', data)
        for match in m:
            kw.add(match)
    print(', '.join(sorted(kw)))


def main(keyword, incremental=False):
    """Print all journals matching keyword"""
    os.system('clear')
    display_keyword = display_matching_section(keyword)
    for journal in list(JOURNALPATH.glob('*.md')):
        displayed = display_keyword(journal)
        if incremental and displayed:
            input()
            os.system('clear')


if __name__ == "__main__":
    args = docopt(__doc__)
    incremental = args['-s']
    if args['keywords'] or args['kw']:
        keywords()
    else:
        main(args['KEYWORD'], incremental)
