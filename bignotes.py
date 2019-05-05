#!/usr/bin/env python3
import sys
from argparse import ArgumentParser
from pathlib import Path
from functools import partial
from toolz.functoolz import *


def main():
    parser = ArgumentParser("bignotes")
    parser.add_argument("-n", type=int, default=10, help="Number of notes to list")
    parser.add_argument("-i", type=str, help="Query to ignore", nargs="+")
    parser.add_argument("-q", type=str, help="Query to find", nargs="+")
    args = parser.parse_args()

    files = Path(".").rglob("*.md")

    if args.i:
        files = filter(lambda f: not any([ignore in str(f) for ignore in args.i]), files)
    if args.q:
        files = filter(lambda f: any([query in str(f) for query in args.q]), files)

    sized_files = ((f, f.stat().st_size / 1024) for f in files)
    sorted_files = sorted(sized_files, key=lambda x: x[1], reverse=True)[: args.n]
    for fn, size in sorted_files:
        print(f"{size:4.2f} kb -- {fn}")


if __name__ == "__main__":
    main()
