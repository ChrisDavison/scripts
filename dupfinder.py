#!/usr/bin/env python3
"""Find duplicates based on file hash"""
import glob
import hashlib
import os
import sys
from multiprocessing.pool import Pool
from collections import defaultdict
   

class Dupfinder:
    def __init__(self, folders, blocksize):
        self.blocksize = blocksize
        self.files = []
        for folder in folders:
            paths = glob.glob(f"{folder}/**/*", recursive=True)
            self.files.extend(p for p in paths if not os.path.isdir(p))

    def run(self):
        path_and_hash = Pool().map(self.hash, set(self.files))
        hashes = defaultdict(lambda: [])
        for path, hash in path_and_hash:
            hashes[hash].append(path)
        self.hasdups = [ls for _, ls in hashes.items() if len(ls) > 1]
        if not self.hasdups:
            return
        self.display()

    def display(self):
        for paths in self.hasdups:
            print('=' * 40)
            for p in sorted(paths):
                print(f"\t{p}")
    
    def hash(self, filename):
        """Get MD5 hash of a file"""
        hasher = hashlib.md5()
        with open(filename, "rb") as f:
            buf = f.read(self.blocksize)
            while buf:
                hasher.update(buf)
                buf = f.read(self.blocksize)
        return filename, hasher.hexdigest()


if __name__ == "__main__":
    args = list(sys.argv[1:])
    if args:
        Dupfinder(set(args), blocksize=65536).run()
    else:
        print("usage: dupfinder.py <dir>...")
