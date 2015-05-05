#!/usr/bin/env python3
import argparse
import sys

from biblio import *

# Regex
# Instead, a list of keywords, which I prepend onto the regex
# and then search with this?
parser = argparse.ArgumentParser()
parser.add_argument('--search', help='Search within bibliography')
parser.add_argument('--print', help='Print default bibliography', action='store_true')
parser.add_argument('--doi', help='Get a bib entry from DOI')
args = parser.parse_args()


def main():
    try:
        mybib = bibliography("library.bib")
    except Exception as E:
        sys.exit(E)  # Fail if we can't read the bib

    if args.search:
        mybib.search(args.search)
    elif args.print:
        print(mybib)
    elif args.doi:
        mybib.from_doi(args.doi)
    else:
        parser.print_help()
    mybib.write("library.bib")

if __name__ == "__main__":
    main()
