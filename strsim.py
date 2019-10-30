#!/usr/bin/env python
import sys
import textdistance
from pathlib import Path

if len(sys.argv) < 3:
    print("usage: strsim <REFERENCE> <strings>...")
    sys.exit(1)
location_of_n = -1
if '-n' in sys.argv:
    location_of_n = sys.argv.index('-n')
num = 10
if location_of_n > 0:
    num = int(sys.argv[location_of_n+1])
    sys.argv.pop(location_of_n+1)
    sys.argv.pop(location_of_n)
REFERENCE = sys.argv[1]
strings = sys.argv[2:]

print(REFERENCE)
sims = []
for string in strings:
    if Path(string).exists():
        string = Path(string).stem
    dist = textdistance.jaro_winkler(REFERENCE, string)
    sims.append((dist, string))

for dist, string in sorted(sims, reverse=True)[:num]:
    print(f"{dist:.3f}\t{string}")
