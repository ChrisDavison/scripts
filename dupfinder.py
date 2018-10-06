#!/usr/bin/env python3
"""Find duplicates based on file hash"""
import glob
import hashlib
import os
import sys
from collections import defaultdict
from itertools import chain


def find_dups(folders, blocksize):
    """Find files with duplicate hashes"""
    files = []
    for folder in folders:
        files.extend(glob.glob(f"{folder}/**.*", recursive=True))
    hashes = defaultdict(lambda: [])
    for path in set(files):
        hashes[filehash(path, blocksize)].append(path)
    hasdups = [ls for _, ls in hashes.items() if len(ls) > 1]
    if not hasdups:
        return
    print("These files have identical content")
    for paths in hasdups:
        print('=' * 40)
        for p in sorted(paths):
            print(f"\t{p}")


def filehash(path, blocksize):
    """Get MD5 hash of a file"""
    hasher = hashlib.md5()
    with open(path, "rb") as f:
        buf = f.read(blocksize)
        while buf:
            hasher.update(buf)
            buf = f.read(blocksize)
    return hasher.hexdigest()


if __name__ == "__main__":
    args = list(sys.argv[1:])
    if args:
        find_dups(set(args), blocksize=65536)
    else:
        print("usage: dupfinder.py <dir>...")
