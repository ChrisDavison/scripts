#!/usr/bin/env python3
from argparse import ArgumentParser
from pathlib import Path
from functools import partial

import pandas as pd
from toolz.functoolz import *


def get_parents(path):
    return '/'.join([str(s) for s in path.parents][::-1][1:])


def get_kb(path):
    return int(path.stat().st_size / 1024)


def main():
    """Find largest markdown files under current directory"""
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
    files = pd.DataFrame(files, columns=['path'])

    files['stem'] = files['path'].apply(lambda x: x.stem)
    files['parents'] = files['path'].apply(get_parents)
    files['kb'] = files['path'].apply(get_kb)
    blank = [''] * len(files)
    files = files.sort_values(by='kb', ascending=False)
    files.index = blank
    print(files[['kb', 'stem', "parents"]].head(args.n))


if __name__ == "__main__":
    main()
