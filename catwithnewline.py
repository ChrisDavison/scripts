#!/usr/bin/env python3
from pathlib import Path
from argparse import ArgumentParser


def main(output_filename, files):
    contents = []
    for file in files:
        contents.append(file.read_text())
        contents.append('\n')
    Path(output_filename).write_text('\n'.join(contents))


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--filename", type=Path, required=True)
    parser.add_argument("files", nargs="+", type=Path)
    args = parser.parse_args()
    main(args.filename, args.files)
