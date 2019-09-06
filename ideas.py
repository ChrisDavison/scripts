#!/usr/bin/env python
import os
import re
from argparse import ArgumentParser


def yield_sections(filepath):
    sections_started = False
    contents = ""
    for line in open(filepath):
        if line.startswith("#"):
            sections_started = True
            if contents:
                yield (header, contents)
                contents = ""
            header = " ".join(line.split(" ")[1:]).strip()
        else:
            if not sections_started:
                continue
            contents += line
    if contents:
        yield (header, contents)


parser = ArgumentParser("ideas")
parser.add_argument("headline", nargs="*", help="Headline to show ideas for")
args = parser.parse_args()

filepath = os.path.expanduser("~/Dropbox/notes/idea-index.md")

headline = " ".join(args.headline).lower() if args.headline else None
for header, contents in yield_sections(filepath):
    if not headline:
        print(header)
    elif headline.lower() in header.lower():
        joined_lines = re.sub("\n    ", " ", contents)
        no_dashes = re.sub("-\s+", "", joined_lines)
        print(no_dashes.strip())
