#!/usr/bin/env python3
import argparse
import sys

from biblio import bibliography

# Regex
parser = argparse.ArgumentParser()

# Prefer this method, as the add_argument function gets ugly and unclear
args = [['-s', '--search',   'Search within bibliography'],
        ['-f', '--filename', 'Bibliography filename'],
        ['-p', '--print',    'Print default bibliography',   'store_true'],
        ['-i', '--doi',      'Get a bib entry from DOI'],
        ['-a', '--add',      'Add an entry to the bib',      'store_true'],
        ['-d', '--delete',   'Remove an entry from the bib', 'store_true'],
        ['-e', '--edit',     'Edit a bib entry',             'store_true']]

for arg in args:
    if len(arg) < 3:
        parser.add_argument(arg[0], arg[1], help=arg[2], action=arg[3])
    else:
        parser.add_argument(arg[0], arg[1], help=arg[2])

args = parser.parse_args()


def main():
    if not args.filename:
        fn = "library.bib"
    else:
        fn = args.filename

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
