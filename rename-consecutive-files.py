#!/usr/bin/env python3
from pathlib import Path
from shutil import move

if len(sys.argv) < 2:
    print("usage: rename-consecutive-files.py <DIR>"
    sys.exit(1)
dir = sys.argv[1]
for i, p in enumerate(Path(dir).glob('*')):
    new = p.parent / f"{i:02d}{p.suffix}"
    move(p, new)
