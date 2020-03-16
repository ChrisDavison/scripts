#!/usr/bin/env python3
"""Show the largest notes under a directory."""
from argparse import ArgumentParser
from pathlib import Path

import pandas as pd

from terminalstyle import Style


def get_kb(path):
    """Stat the file and get filesize in kb"""
    return int(path.stat().st_size / 1024)


def matches_any(queries, path):
    """Check if a path matches any of a list of queries."""
    return any([query in str(path) for query in queries])


def main():
    """Find largest markdown files under current directory"""
    parser = ArgumentParser("bignotes")
    parser.add_argument("-n", type=int, default=10, help="Number of notes to list")
    parser.add_argument("-i", help="Query to ignore", nargs="+", default=["zzzzz"])
    parser.add_argument("-q", help="Query to find", nargs="+", default=[""])
    parser.add_argument("-f", help="File with processed files")
    args = parser.parse_args()

    queries_to_ignore = args.i
    if args.f:
        queries_to_ignore.extend(Path(args.f).read_text().splitlines())
    files = [
        f
        for f in Path(".").rglob("*")
        if f.suffix in [".txt", ".md", ".org"] and matches_any(args.q, f) and not matches_any(queries_to_ignore, f)
    ]
    files = pd.DataFrame(files, columns=["path"])
    files["kb"] = files["path"].apply(get_kb)
    files = files.sort_values(by="kb", ascending=False)
    for _, row in files.iloc[: args.n].iterrows():
        print(f"{row.kb:3d} kb\t{row.path.parent}/{Style.red(row.path.name)}")


if __name__ == "__main__":
    main()
