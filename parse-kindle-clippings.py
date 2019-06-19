#!/usr/bin/env python3
import codecs
import itertools
import pathlib
import re
import sys

args = sys.argv[1:]
if len(args) < 2:
    print("usage: parse-kindle-clippings <clippings> <outdir>")
    sys.exit(1)
filename = args[0]
outdir = pathlib.Path(args[1])
if not outdir.exists():
    outdir.mkdir(parents=True)

contents = pathlib.Path(filename).read_bytes()
chunks = re.split(b'==========\s+', contents)
notes = [re.split(b'\r\n', note) for note in chunks if b'Your Highlight' in note]
title_and_contents = [(n[0].replace(codecs.BOM_UTF8, b'').strip(), n[3].strip()) for n in notes]
grouped = itertools.groupby(title_and_contents, lambda x: x[0])
files_and_contents = {filename.decode('utf-8'): list(notes) for filename, notes in grouped}

for filename in files_and_contents.keys():
    print(filename.strip())
    outfile = outdir / f"{filename}.org"
    with outfile.open("w") as f:
        print(f"#+TITLE: {filename}\n", file=f)
        for _, note in files_and_contents[filename]:
            if not note:
                continue
            print("-", note.decode(), file=f)
