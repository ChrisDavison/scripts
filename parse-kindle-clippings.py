#!/usr/bin/env python3
import argparse
import codecs
import itertools
import pathlib
import re
import sys


def tidy(note):
    replaces = [("“", '"'), ("”", '"'), ("’", "'"), ("—", "--")]
    note = note.decode()
    for (old, new) in replaces:
        note = note.replace(old, new)
    return note.encode()


parser = argparse.ArgumentParser(description="Create an org file of highlights for every book in kindle clippings")
parser.add_argument("clippings", help="'My Clippings.txt' file")
parser.add_argument("outdir", help="Directory for note output")
args = parser.parse_args()

outdir = pathlib.Path(args.outdir)
outdir.mkdir(parents=True, exist_ok=True)

contents = pathlib.Path(args.clippings).read_bytes().replace(codecs.BOM_UTF8, b"")
chunks = re.split(b"==========\s+", contents)
notes = [re.split(b"\r\n", note) for note in chunks if b"Your Highlight" in note or "Your Note" in note]
grouped = itertools.groupby(notes, lambda x: x[0])

for filename, notes_for_file in grouped:
    filename = filename.decode("utf-8")
    contents = [n[3] for n in notes_for_file]
    print(filename.strip())
    outfile = outdir / f"{filename}.org"
    valid_notes = b"\n".join([b"- " + tidy(n) for n in contents if n])
    data = f"#+TITLE: {filename}\n\n".encode() + valid_notes + b"\n"
    outfile.write_bytes(data)
