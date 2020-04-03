#!/usr/bin/env python3
"""Get backlinks for notes

With no arguments, will count the 'backlinks' to each note for each note in 
the current directory.

With filenames, will show the specific notes that link to each of the given
filenames.
"""
import os
import re
from collections import defaultdict
from argparse import ArgumentParser
from pathlib import Path


def get_links_in_file(filename):
    re_file_link = re.compile(r"\((?:\./)*([a-zA-Z0-9\-_]*?\.md)")
    contents = open(filename).read().lower()
    return [m.group(1) 
            for m in re_file_link.finditer(contents)]


def print_forwardlinks(files):
    for filename in files:
        links = get_links_in_file(filename)
        if not links:
            continue
        print(filename)
        for link in links:
            print("  >", link)


def print_backlinks(files):
    backlinks = get_all_backlinks()
    for filename in files:
        links = backlinks[str(filename)]
        if not links:
            continue
        print(filename)
        for link in links:
            print("  ^", link)


def print_counted_backlinks(files):
    backlinks = get_all_backlinks()
    files_and_links = [(f, backlinks[f]) for f in backlinks if backlinks[f]]
    files_and_links = sorted(files_and_links, key=lambda x: len(x[1]), reverse=True)
    for (filename, links) in files_and_links:
        print("{:5} {}".format(len(links), filename))


def print_orphans(files):
    backlinks = get_all_backlinks()
    for f in files:
        if not backlinks[str(f)]:
            print(f)


def get_all_backlinks():
    backlinks = defaultdict(list)
    for filename in os.listdir():
        if not filename.endswith('.md'):
            continue
        for link in get_links_in_file(filename):
            backlinks[link].append(filename)
    return backlinks


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("files", nargs="*")
    parser.add_argument("-c", "--count", action="store_true")
    parser.add_argument("-o", "--orphaned", 
            help="Show files that are not linked to", action="store_true")
    parser.add_argument("-f", "--forward", 
            help="Show forward-links (links FROM files) instead",
            action="store_true")
    args = parser.parse_args()
    files = files if args.files else sorted(list(Path('.').rglob('*.md')))
    if args.orphaned:
        print_orphans(files)
    elif args.forward:
        print_forwardlinks(files)
    elif args.count:
        print_counted_backlinks(files)
    else:
        print_backlinks(files)


