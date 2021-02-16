#!/usr/bin/env python3
from pathlib import Path
from dateutil.parser import parse as dateparse
from argparse import ArgumentParser
import datetime
import sys


parser = ArgumentParser()
parser.add_argument('directory')
args = parser.parse_args()

path = Path(args.directory)
if not path.is_dir():
    print("Couldn't find path. Must be a full path")
    sys.exit(1)

files = list(Path(args.directory).resolve().glob('*.md'))

today = datetime.datetime.today()
last_week = today - datetime.timedelta(days=7)

last_weeks_journals = sorted([
        j for j in files
        if dateparse(j.stem) >= last_week
])

for file in last_weeks_journals:
    data = file.read_text()
    print(file.stem)
    print()
    print(data)
    print()
    print("=" * 40)
