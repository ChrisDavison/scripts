#!/usr/bin/env python3
import codecs
import itertools
import pathlib
import re
import sys


def tidy(note):
    return (
        note.decode()
        .replace("“", '"')
        .replace("”", '"')
        .replace("’", "'")
        .replace("—", "--")
        .encode()
    )

args = sys.argv[1:]
if len(args) < 2:
    print("usage: parse-kindle-clippings <clippings> <outdir>")
    sys.exit(1)
filename = args[0]
outdir = pathlib.Path(args[1])
if not outdir.exists():
    outdir.mkdir(parents=True)

contents = pathlib.Path(filename).read_bytes().replace(codecs.BOM_UTF8, b"")
chunks = re.split(b"==========\s+", contents)
notes = [re.split(b"\r\n", note) for note in chunks if b"Your Highlight" in note]
grouped = itertools.groupby(notes, lambda x: x[0])

files_and_contents = dict()
for (filename, notes_for_file) in grouped:
    files_and_contents[filename.decode("utf-8")] = [n[3] for n in notes_for_file]

for filename, contents in files_and_contents.items():
    print(filename.strip())
    outfile = outdir / f"{filename}.org"
    valid_notes = b"\n".join([b"- " + tidy(n) for n in contents if n])
    data = f"#+TITLE: {filename}\n\n".encode() + valid_notes + b"\n"
    outfile.write_bytes(data)
