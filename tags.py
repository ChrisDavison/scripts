#!/usr/bin/env python3
import os
import re
import sys

from collections import defaultdict
from pathlib import Path


try:
    notesdir = os.environ['NOTESDIR']
except KeyError:
    print("Expected NOTESDIR env var")
    sys.exit(1)
files = list(Path(notesdir).rglob('*.md'))

def get_tags_and_filenames(files):
    tags = defaultdict(list)
    keyword = re.compile(b'#[a-zA-Z0-9]+')

    for filepath in files:
        data = filepath.read_bytes()
        m = keyword.findall(data)
        if m:
            for word in m:
                tags[word.decode('utf-8')[1:]].append(filepath)

    counted_tags = [(kw, len(vals), vals) for kw, vals in tags.items()]
    sorted_tags = sorted(counted_tags, key=lambda x: x[1], reverse=True)
    return sorted_tags


if __name__ == "__main__":
    notesdir_fixed = str(Path(notesdir))
    for tag, count, vals in get_tags_and_filenames(files):
        if len(sys.argv) > 1:
            if tag in sys.argv:
                for filename in sorted(vals):
                    print(str(filename).replace(notesdir_fixed, '')[1:])
        else:
            print(count, tag)
