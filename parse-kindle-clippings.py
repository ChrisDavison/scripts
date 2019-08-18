#!/usr/bin/env python3
import argparse
import codecs
import itertools
import pathlib
import re


def tidy(note):
    replaces = [("“", '"'), ("”", '"'), ("’", "'"), ("—", "--")]
    note = note.decode()
    for (old, new) in replaces:
        note = note.replace(old, new)
    return note.encode()


def read_notes(filepath):
    contents = pathlib.Path(filepath).read_bytes().replace(codecs.BOM_UTF8, b"")
    chunks = re.split(b"==========\r\n", contents)
    notes = []
    for chunk in chunks:
        if b"Your Highlight" in chunk or b"Your Note" in chunk:
            notes.append(re.split(b"\r\n", chunk))
    return sorted(notes)


def make_note_file(outdir, filename, notes):
    contents = [n[3] for n in notes]
    print(filename)
    filename = ''.join([ch for ch in filename if ch not in "(),:"])
    filename = filename.replace(" ", "-")
    outfile = outdir / f"{filename}.md"
    valid_notes = b"\n".join([b"- " + tidy(n) for n in contents if n])
    data = f"**{filename}**\n\n".encode() + valid_notes + b"\n"
    outfile.write_bytes(data)


def main():
    parser = argparse.ArgumentParser(description="Create a markdown file of highlights for every book in kindle clippings")
    parser.add_argument("clippings", help="'My Clippings.txt' file")
    parser.add_argument("outdir", help="Directory for note output")
    parser.add_argument("-p", help="File of filenames to ignore")
    args = parser.parse_args()

    outdir = pathlib.Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    ignores = []
    if args.p:
        ignores = pathlib.Path(args.p).read_text().splitlines()

    notes = read_notes(args.clippings)
    for filename, notes_for_file in itertools.groupby(notes, lambda x: x[0]):
        filename = filename.strip()
        decoded_filename = filename.decode("utf-8")
        if decoded_filename in ignores:
            print("IGNORING", decoded_filename)
        else:
            make_note_file(outdir, decoded_filename, notes_for_file)


if __name__ == "__main__":
    main()
