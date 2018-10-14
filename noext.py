#!/usr/bin/env python
"""Simple wrapper to remove file extension.

Mainly to avoid using bash for removing file extensions.

usage: noext <filename>...
"""
import os
import sys


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: noext <filename>...")
    else:
        for filename in sys.argv[1:]:
            print(os.path.splitext(filename)[0])
