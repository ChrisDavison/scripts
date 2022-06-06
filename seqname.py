#!/usr/bin/env python
from pathlib import Path
import click
from argparse import ArgumentParser
from tempfile import TemporaryFile
import re


SEPARATOR = "--"


def partition(iterator, tester):
    trues, falses = [], []
    for item in iterator:
        if tester(item):
            trues.append(item)
        else:
            falses.append(item)
    return trues, falses

def generate_new_name(prefix, suffix, keep_filename):
    """Closure that handles the prefix and suffix logic up front.

    Returns a function that takes a filepath and index,
    and returns a new filename."""
    prefix = prefix + SEPARATOR if prefix else ""
    suffix = SEPARATOR + suffix if suffix else ""
    def _renamer(filepath, index):
        stem = filepath.stem if keep_filename else ""
        return f"{prefix}{index:04d}{stem}{suffix}{filepath.suffix}"
    return _renamer

def name_matches_pattern_tester(prefix, suffix, keep_filename):
    prefix = prefix + SEPARATOR if prefix else ""
    suffix = SEPARATOR + suffix if suffix else ""
    def _tester(filepath):
        has_prefix = False
        has_suffix = False

        filepath = filepath.stem
        # print(filepath)
        if prefix and filepath.startswith(prefix):
            has_prefix = True
            filepath =  filepath[len(prefix):]
            # print("->", filepath)

        if suffix and filepath.endswith(suffix):
            has_suffix = True
            filepath = filepath[:-len(suffix)]
            # print("->", filepath)

        if (has_prefix or not prefix) and (has_suffix or not suffix):
            return True
        else:
            return False
    return _tester

def largest_matching_index(files):
    largest = 0
    for file in files:
        m = re.search("([0-9]+)", file.stem)
        if m:
            idx = int(m.group(1))
            if idx > largest:
                largest = idx
    return largest


@click.command()
@click.option("--prefix", type=str, default="")
@click.option("--suffix", type=str, default="")
@click.option("--keep-filename", is_flag=True)
@click.option("--sort", type=click.Choice(["accessed", "modified", "name"]), default="modified")
@click.option("--dryrun", "-d", is_flag=True)
@click.option("--verbose", "-v", is_flag=True)
@click.option("--separator", "-s", default="--")
def main(prefix, suffix, keep_filename, sort, dryrun, verbose, separator):
    global SEPARATOR
    SEPARATOR = separator
    files = [f for f in Path('.').glob('*') if f.is_file()]
    if sort == "name":
        files = sorted(files)
    elif sort == "accessed":
        files = sorted(files, key=lambda x: x.stat().st_atime)
    else:
        files = sorted(files, key=lambda x: x.stat().st_mtime)

    renamer = generate_new_name(prefix, suffix, keep_filename)
    name_matches_pattern = name_matches_pattern_tester(prefix, suffix, keep_filename)

    files_matching = (f for f in files if name_matches_pattern(f))
    files_not_matching =(f for f in files if not name_matches_pattern(f))

    mover = lambda old, new: None
    if not dryrun:
        mover = lambda old, new: old.rename(new)

    printer = lambda old, new: None
    if verbose:
        printer = lambda old, new: print(old, "->", new)

    idx = largest_matching_index(files_matching) + 1
    for file in files_not_matching:
        new_name = renamer(file, idx)
        printer(file, new_name)
        mover(file, new_name)
        idx += 1

if __name__ == "__main__":
    main()



