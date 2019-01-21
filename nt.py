#!/usr/bin/env python3
"""Command-line Notetaking

By default, will list all tags for given dir, or files, or $NOTESDIR.

usage:
    nt [FILES...]
    nt -t TAG [FILES...]
    nt -l [FILES...]

options:
    -h       Display help
    -t TAG   Show files with tag TAG
    -l       List files and their tags

optional args:
    FILES  Specific files to get data from

    If FILES is given, is length 1, and is a directory, will read all notes from that directory.
"""
import os
import re
import sys

from collections import defaultdict
from pathlib import Path
from docopt import docopt


class Color:
    """Create coloured output"""
    @staticmethod
    def red(text):
        """Make text red"""
        return f"\033[0;31m{text}\033[0m"

    @staticmethod
    def yellow(text):
        """Make text yellow"""
        return f"\033[1;33m{text}\033[0m"

    @staticmethod
    def green(text):
        """Make text green"""
        return f"\033[00;32m{text}\033[0m"


def get_tags(data):
    """Get all tag-like words from the end of a file"""
    keyword = re.compile(b'#([a-zA-Z0-9]+)')
    data = [line for line in data.splitlines() if line != b'']
    while data[-1] == b"":
        data = data[:-1]
    if len(data) < 2:
        return []
    all_matches = []
    for line in data:
        matches = keyword.findall(line)
        if matches and line.startswith(b'`'):
            all_matches.extend(matches)
    return all_matches


def read_tags_for_files(notesdir):
    """Get dicts of filename:tags and tag:filenames"""
    files_and_keywords = dict()
    for filepath in notesdir.rglob('*.md'):
        tags = get_tags(filepath.read_bytes())
        rel_name = filepath.relative_to(notesdir)
        files_and_keywords[rel_name] = tags
    return files_and_keywords


def get_notesdir():
    """Get the note directory from environment, or exit program"""
    try:
        notesdir = Path(os.environ['NOTESDIR'])
    except KeyError:
        print("Expected NOTESDIR env var")
        sys.exit(1)
    return notesdir


def display_keywords(keywords_and_files):
    if not keywords_and_files:
        print("No keywords")
        return
    longest_keyword = max([len(s) for s in keywords_and_files])
    sorted_kw = sorted(keywords_and_files.keys(), key=lambda x: len(keywords_and_files[x]))
    for keyword in sorted_kw[::-1]:
        vals = keywords_and_files[keyword]
        print(f"{len(vals):4d} {keyword:{longest_keyword}s}")


def filename_tags_to_tag_filenames(files_and_keywords):
    keywords_and_files = defaultdict(list)
    for filename, tags in files_and_keywords.items():
        for tag in tags:
            keywords_and_files[tag.decode()].append(filename)
    return keywords_and_files


def main():
    """Main does the actual CLI"""
    args = docopt(__doc__, version="0.1.0")
    notesdir = get_notesdir()
    files_and_keywords = read_tags_for_files(notesdir)
    if args['FILES']:
        files_and_keywords = dict()
        for filename in args['FILES']:
            filepath = Path(filename)
            if not filepath.exists():
                continue
            elif filepath.is_dir():
                files_and_keywords.update(read_tags_for_files(filepath))
            else:
                files_and_keywords.update({filepath: get_tags(filepath.read_bytes())})
    keywords_and_files = filename_tags_to_tag_filenames(files_and_keywords)

    if not keywords_and_files:
        print("No files.  Exiting.")
        sys.exit(0)

    msg = f"Files: {len(files_and_keywords.keys())}"
    if args['-t']:
        for filename in keywords_and_files[args['-t']]:
            print(filename)
        msg = f"Files: {len(keywords_and_files[args['-t']])}"
    elif args['-l']:
        unique_keywords = set()
        for filename, keyword in files_and_keywords.items():
            tagstr = ', '.join([t.decode() for t in sorted(keyword)])
            print(f"{str(filename)[:60]:60s} {tagstr}")
            unique_keywords.update(keyword)
        msg = f"Files: {len(files_and_keywords.keys())}, Keywords: {len(unique_keywords)}"
    else:
        display_keywords(keywords_and_files)
        msg = f"Files: {len(files_and_keywords.keys())}, Keywords: {len(keywords_and_files.keys())}"
    print(f"\n{msg}")



if __name__ == "__main__":
    main()
