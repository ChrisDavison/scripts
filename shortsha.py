#!/usr/bin/env python
"""Get the sha256 hash of a file, up to a certain number of bytes."""
import hashlib
import sys
from argparse import ArgumentParser

if __name__ == "__main__":
    parser = ArgumentParser("shortsha")
    parser.add_argument("filename")
    parser.add_argument("-n", help="Number of bytes", required=False, type=int)
    args = parser.parse_args()
    digest = hashlib.md5(open(args.filename, "rb").read()).hexdigest()
    if args.n:
        digest = digest[: args.n]
    print(digest)
