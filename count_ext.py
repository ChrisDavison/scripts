#!/usr/bin/env python3
from pathlib import Path
from collections import Counter

excluded_dirs = ['.git', 'target']

suffixes = [
    p.suffix for p in Path('.').rglob('*')
    if p.is_file and 
    not any([d in list(p.parent.parts) for d in excluded_dirs])
]

for suffix, count in Counter(suffixes).most_common():
    print(f"{count} {suffix}")
