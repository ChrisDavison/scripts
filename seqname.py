#!/usr/bin/env python
from pathlib import Path
from argparse import ArgumentParser
from tempfile import TemporaryFile


def generate_new_name(prefix, suffix, keep_filename):
    """Closure that handles the prefix and suffix logic up front.

    Returns a function that takes a filepath and index, 
    and returns a new filename."""
    prefix = prefix + "--" if prefix else ""
    suffix = "--" + suffix if suffix else ""
    def _renamer(filepath, index):
        stem = filepath.stem if keep_filename else ""
        return f"{prefix}{index:04d}{stem}{suffix}{filepath.suffix}"
    return _renamer


def move_via_temp(renaming_map, dryrun, verbose):
    """Incase we are renaming a directory that has already been seqnamed
    move each file to something with a temporary suffix, then move them back.
    
    e.g. if I already have PREFIX--1.png, but file2.png wants to be renamed 
    to PREFIX--1.png (if the sort or access time differs, or I've moved another
    file into the folder), this ensures the files wont get clobbered."""
    if dryrun or verbose:
        for old, new in renaming_map:
            print(old, " -> ", new)

    if dryrun:
        return

    # first pass, move them all with temporary filenames
    for old, new in renaming_map:
        old.rename("_temprename" + new)

    # second pass, move to the true filename
    for old, new in renaming_map:
        Path("_temprename" + new).rename(new)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('--prefix', type=str, required=False)
    parser.add_argument('--suffix', type=str, required=False)
    parser.add_argument('--keep-filename', action='store_true', required=False)
    parser.add_argument('--sort', type=str, required=False, choices=["accessed", "modified", "name"], default="name")
    parser.add_argument('-d', '--dryrun', action='store_true', required=False)
    parser.add_argument('-v', '--verbose', action='store_true', required=False)
    args = parser.parse_args()
    print(args)

    files = [f for f in Path('.').glob('*') if f.is_file()]
    if args.sort == "name":
        files = sorted(files)
    elif args.sort == "accessed":
        files = sorted(files, key=lambda x: x.stat().st_atime)
    else:
        files = sorted(files, key=lambda x: x.stat().st_mtime)

    renamed = generate_new_name(args.prefix, args.suffix, args.keep_filename)

    rename_map = [(file, renamed(file, i)) 
            for (i, file) in enumerate(files)]

    move_via_temp(rename_map, args.dryrun, args.verbose)
