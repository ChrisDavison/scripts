#!/usr/bin/env python
from pathlib import Path
from datetime import date
from argparse import ArgumentParser

parser = ArgumentParser("books_read")
parser.add_argument("-n", "--no-print-titles", action="store_true",
                    help="Don't print the titles of each book")
args = parser.parse_args()

booklist = Path("~/src/github.com/ChrisDavison/knowledge/books-ive-read.md").expanduser()
data = booklist.read_text().splitlines()
headers = [l for l in data if l.startswith('#')]
this_year = date.today().year
next_year = this_year + 1

start = False
read = 0
for header in headers:
    if str(this_year) in header:
        start = True
        continue
    if start:
        read += 1
        if not args.no_print_titles:
            print(" ".join(header.split(" ")[1:]))
    if str(next_year) in header:
        break

pct_passed = (date.today() - date(this_year, 1, 1)).days / 365
prediction = read / pct_passed
print(f"Books read in {this_year} = {read}. Predict {int(prediction)}.")
