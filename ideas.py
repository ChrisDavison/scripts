#!/usr/bin/env python3
from pathlib import Path
import re
from argparse import ArgumentParser
from collections import defaultdict


parser = ArgumentParser('ideas')
parser.add_argument('headline', nargs="?", help='Headline to show ideas for')
args = parser.parse_args()

filepath = Path('~/Dropbox/notes/idea-index.md').expanduser()
contents = filepath.read_text().splitlines()

headline = args.headline[0].lower() if args.headline else None

headline_and_contents = defaultdict(list)
header = None
for line in contents:
    re_header = re.match(r'#+\s+(.*)', line)
    re_line = re.match(r'-\s+(.*)', line)
    if re_header:
        header = re_header.group(1).lower()
    elif header and re_line:
        headline_and_contents[header].append(re_line.group(1))

if headline and headline in headline_and_contents.keys():
    for entry in headline_and_contents[headline]:
        print(f"- {entry}")
else:
    print("SECTIONS AVAILABLE")
    print("==================")
    print('\n'.join(sorted(headline_and_contents.keys())))
