#!/usr/bin/env python3
from math import floor
import sys


WIDTH = 74
if len(sys.argv) > 1:
    text = ' '.join(sys.argv[1:])
else:
    text = ''.join(l.strip() for l in sys.stdin if l.strip())
n_dashes = floor((WIDTH - len(text)) / 2)
dashes = "-" * n_dashes
print(f"**{dashes} {text} {dashes}**")
