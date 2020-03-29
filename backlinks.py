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


parser = ArgumentParser()
parser.add_argument("files", nargs="*")
parser.add_argument("-c", "--count", action="store_true")
parser.add_argument("-f", "--forward", 
        help="Show forward-links (links FROM files) instead",
        action="store_true")
args = parser.parse_args()



def get_links_in_file(filename):
    re_file_link = re.compile(r"\((?:\./)*([a-zA-Z0-9\-_]*?\.md)")
    if not filename.endswith(".md"):
        return []
    contents = open(filename).read().lower()
    return [m.group(1) 
            for m in re_file_link.finditer(contents)]


def print_forwardlinks(filename):
    links = []
    for link in get_links_in_file(filename):
        links.append(link)
    if links:
        print(filename)
        for link in links:
            print("  >", link)


def get_all_backlinks(files):
    backlinks = defaultdict(list)
    for filename in files:
        for link in get_links_in_file(filename):
            backlinks[link].append(filename)
    return backlinks


all_files = [f for f in os.listdir() if f.endswith(".md")]
if args.files:
    files = args.files
else:
    files = all_files

if args.forward:
    for filename in files:
        print_forwardlinks(filename)
else:
    backlinks = get_all_backlinks(all_files)
    for filename in files:
        links = set(backlinks[filename])
        if not links:
            continue
        if args.count:
            print("{:5} {}".format(len(links), filename))
        else:
            print(filename)
            for link in links:
                print("  ^", link)
