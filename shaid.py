#!/usr/bin/env python
"""Generate sha256 sums of a file, or stdin."""
from hashlib import sha256
import sys

def main():
    """Get a shortened hexdigest of the sha256 sum of a file or stdin."""
    if len(sys.argv) == 1:
        data = ''.join(sys.stdin)
    else:
        data = open(sys.argv[1]).read()

    hasher = sha256()
    hasher.update(data.encode())
    digest = hasher.hexdigest()[:16]
    print(f"@{digest[:4]}-{digest[4:8]}-{digest[8:12]}-{digest[12:]}")

if __name__ == "__main__":
    main()
