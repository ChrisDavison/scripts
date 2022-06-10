#!/usr/bin/env python3
from datetime import date, timedelta
from argparse import ArgumentParser
import pathlib
import re


RE_DATE = re.compile("([0-9]{4})-([0-9]{2})-([0-9]{2}).*")

parser = ArgumentParser("lastndays")
parser.add_argument("directory", type=pathlib.Path,
                    help="Directory with dated journal files.")
parser.add_argument("-d", "--days", type=int, help="How many days", default=7)
parser.add_argument("--name-only", action="store_true",
                    help="Only print the matching filenames")
args = parser.parse_args()

date_threshold = date.today() - timedelta(days=args.days)

files_and_match = ((f, RE_DATE.match(f.stem)) for f in args.directory.rglob("*.md"))

dated_files = ((f, date(int(m.group(1)), int(m.group(2)), int(m.group(3))))
               for f, m in files_and_match
               if m)

matching_files = (f for f, f_date in dated_files if f_date > date_threshold)

for f in matching_files:
    if args.name_only:
        print(f)
        continue
    else:
        print(f"===== {f} =====\n")
        print(f.read_text())

