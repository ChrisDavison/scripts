#!/usr/bin/env python

# By Gary Bernhardt.
# Dotfiles at: https://github.com/garybernhardt/dotfiles

import sys
import zlib
import bz2

def main():
    data = file_data()
    size = len(data)
    print(f'file size {size}')
    gzip_size = len(zlib.compress(data))
    print(f'gzip size {gzip_size} ({percent(gzip_size, size)}%)')
    bz2_size = len(bz2.compress(data))
    print(f'bz2 size {bz2_size} ({percent(bz2_size, size)}%)')

def file_data():
    files = map(open, sys.argv[1:])
    if not files:
        files = [sys.stdin]
    return b''.join(f.read().encode() for f in files)

def percent(part, whole):
    return int(100.0 * part / (whole + 0.000000001))

if __name__ == '__main__':
    main()
