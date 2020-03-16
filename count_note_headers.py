#!/usr/bin/env python3
import re
from os.path import basename, splitext
from argparse import ArgumentParser

SYMBOLS = {'md': b'#', 'txt': b'#', 'org': b'*'}


def count_headers(filename):
    extension = splitext(filename)[1][1:]
    symbol = SYMBOLS[extension]
    rx = re.compile(b"^"  + symbol)
    data = open(filename, 'rb').read().split(b"\n")
    headers = [line for line in data if rx.match(line)]
    return (len(headers), filename)


if __name__ == '__main__':
    PARSER = ArgumentParser()
    PARSER.add_argument("files", nargs='+')
    PARSER.add_argument("--min-count", default=0, type=int)
    ARGS = PARSER.parse_args()

    counted = [count_headers(filename) for filename in ARGS.files]
    
    for (count, filename) in sorted(counted)[::-1]:
        if count >= ARGS.min_count:
            print("{:10} {}".format(count, basename(filename)))
            
