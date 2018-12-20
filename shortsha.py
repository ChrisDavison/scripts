#!/usr/bin/env python
"""Get the sha256 hash of a file, up to a certain number of bytes."""
import hashlib
import sys

if len(sys.argv) < 2:
    print("usage: shortsha <file> [<N>]")
    sys.exit(-1) 

digest = hashlib.md5(open(sys.argv[1], "rb").read()).hexdigest()
if len(sys.argv) > 2:
    digest = digest[:int(sys.argv[2])]
print(digest)
