#!/usr/bin/env python3
from datetime import date, timedelta
from argparse import ArgumentParser
import pathlib


parser = ArgumentParser("last7days")
parser.add_argument("directory", type=pathlib.Path,
        help="Directory with dated journal files.")
args = parser.parse_args()

last_week = date.today() - timedelta(days=7)
files = args.directory.rglob("*.md")

for f in files:
    yyyy, mm, dd, *other = f.stem.split("-")
    date_of_file = date(int(yyyy), int(mm), int(dd))
    if date_of_file > last_week:
        print(f.read_text())
        print("=" * 80)
