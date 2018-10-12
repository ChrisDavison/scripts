#!/usr/bin/env python
import os
import sys


def main(filenames):
    for filename in filenames:
        fn, _ = os.path.splitext(filename)
        print(fn)
    

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("usage: noext <filename>...")
    else:
        filenames = sys.argv[1:]
        main(filenames)
