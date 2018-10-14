#!/usr/bin/env python3
"""Find duplicates based on file hash.

Usage:
    dupfinder.py [-o OUTPUT] [-b BLOCKSIZE] [-h|--help] <folders>...

Positional Arguments:
    folders...                  Folders to glob for files

Options:
    -o --output OUTPUT          File for output (default: sys.stdout)
    -b --blocksize BLOCKSIZE    Blocksize to iterate over when generating MD5 (default: 65536)
    -h --help                   Display this message
"""
import glob
import hashlib
import os
import sys
from typing import Dict, List, Tuple, Set
from multiprocessing.pool import Pool
from collections import defaultdict
from docopt import docopt


BLOCKSIZE = 0


def get_md5_hash_of_file(filename: str) -> Tuple[str, str]:
    """Read a file and return the filename and MD5 hash."""
    with open(filename, "rb") as f_in:
        hasher = hashlib.md5()
        buf = f_in.read(BLOCKSIZE)
        while buf:
            hasher.update(buf)
            buf = f_in.read(BLOCKSIZE)
    return filename, hasher.hexdigest()


def find_duplicates(folders: Set[str]) -> List[List[str]]:
    """Get MD5 hash of files in folders, and group by hash."""
    files: List[str] = []
    for folder in folders:
        paths = glob.glob(f"{folder}/**/*", recursive=True)
        files.extend(p for p in paths if not os.path.isdir(p))
    path_and_hash = Pool().map(get_md5_hash_of_file, set(files))
    # Rather than a dict comprehension, iterate so that we can get a list of filenames
    # for each file hash
    hashes: Dict[str, List[str]] = defaultdict(list)
    for path, hash_of_file in path_and_hash:
        hashes[hash_of_file].append(path)
    return [ls for _, ls in hashes.items() if len(ls) > 1]


def display_duplicates(duplicates: List[List[str]], file):
    """Display any duplicate files found, grouped."""
    for paths in duplicates:
        print("=" * 40, file=file)
        for path in sorted(paths):
            print(f"\t{path}", file=file)


def __main(folders: List[str], file):
    duplicates = find_duplicates(set(folders))
    display_duplicates(duplicates, file)


if __name__ == "__main__":
    ARGS = docopt(__doc__, version="0.1.0")
    BLOCKSIZE = ARGS.get("--blocksize", 65536)
    FILE = ARGS.get("--output", sys.stdout)
    sys.exit(__main(ARGS["<folders>"], FILE))
