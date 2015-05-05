#!/usr/bin/env python3
import argparse
import sys

from biblio import bibliography

# Regex
parser = argparse.ArgumentParser()
parser.add_argument('--search',
                    help='Search within bibliography')
parser.add_argument('--print', action='store_true',
                    help='Print default bibliography')
parser.add_argument('--doi', help='Get a bib entry from DOI')
parser.add_argument('--add', action='store_true',
                    help='Add an entry to the Bib')
parser.add_argument('--delete', action='store_true',
                    help='Remove an entry from the Bib')
parser.add_argument('--edit', action='store_true',
                    help='Edit a Bib entry')
args = parser.parse_args()


def main():
    fn = "library.bib"
    try:
        mybib = bibliography(fn)
    except Exception as E:
        sys.exit(E)  # Fail if we can't read the bib

    if args.search:
        mybib.search(args.search)
    elif args.print:
        print(mybib)
    elif args.doi:
        mybib.from_doi(args.doi)
    elif args.add:
        mybib.add()
    elif args.delete:
        mybib.delete()
    elif args.edit:
        mybib.edit()
    else:
        parser.print_help()
        print("\nPrecedence: Search, print, doi, add, delete, edit\n")
    mybib.write(fn + ".bak")

if __name__ == "__main__":
    main()
else:
    parser.print_help()
