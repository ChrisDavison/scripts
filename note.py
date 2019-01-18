#!/usr/bin/env python3
"""Command-line Notetaking

usage:
    note find QUERY
    note tags [DIR]
    note tag QUERY
    note ls [FILES...]
"""
    # note add TEXT...
import os
import re
import sys

from docopt import docopt
from collections import defaultdict
from pathlib import Path


try:
    notesdir = Path(os.environ['NOTESDIR'])
except KeyError:
    print("Expected NOTESDIR env var")
    sys.exit(1)
files = list(notesdir.rglob('*.md'))


def tags_for_file(filepath):
    keyword = re.compile(b'#[a-zA-Z0-9]+')
    data = filepath.read_bytes().splitlines()
    if len(data) < 2:
        return []
    m = keyword.findall(data[-1])
    if m and data[-1].startswith(b'`'):
        return m
    return []


def get_tags_and_filenames(files):
    tags = defaultdict(list)

    for filepath in files:
        for word in tags_for_file(filepath):
            tags[word.decode('utf-8')[1:]].append(filepath)

    counted_tags = [(kw, len(vals), vals) for kw, vals in tags.items()]
    sorted_tags = sorted(counted_tags, key=lambda x: x[1], reverse=True)
    return sorted_tags


def print_tags(DIR):
    notes = files
    gf DIR:
        notes = Path(DIR).rglob('*.md')
    for tag, count, vals in get_tags_and_filenames(notes):
        print(count, tag)


def list_notes_for_tag(tag_wanted):
    for tag, count, vals in get_tags_and_filenames(files):
        if tag in tag_wanted:
            for filename in sorted(vals):
                print(filename.relative_to(notesdir, ''))


def list_tags_for_files(filenames):
    for filename in filenames:
        tags = tags_for_file(filename)
        if tags:
            tagstr = ', '.join([t.decode()[1:] for t in sorted(tags)])
            fn = str(filename.relative_to(notesdir))
            if len(fn) > 50:
                fn = fn[:47]+'...'
            print(f"{fn:60s}", "\t", tagstr)


def find_in_files(query):
    color = {'RED': "\033[0;31m", "YELLOW": "\033[1;33m", "NONE": '\033[0m'}
    print(f"{color['RED']}F --> in filename\n{color['YELLOW']}C --> In contents {color['NONE']}")
    print('-'*20)
    for filepath in files:
        if args['QUERY'] in str(filepath).lower():
            print(f"{color['RED']}F :: {color['NONE']}{str(filepath)}")
        if query.encode('utf-8') in filepath.read_bytes():
            print(f"{color['YELLOW']}C :: {color['NONE']}{str(filepath)}")


if __name__ == "__main__":
    args = docopt(__doc__)
    if args['tags']:
        print_tags(args['DIR'])
    elif args['tag']:
        list_notes_for_tag(args['QUERY'])
    elif args['find']:
        find_in_files(args['QUERY'])
    elif args['ls']:
        if args['FILES']:
            files = [Path(f) for f in args['FILES']]
        list_tags_for_files(files)


