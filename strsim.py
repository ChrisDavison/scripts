#!/usr/bin/env python
import sys
import textdistance
from pathlib import Path
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('-n', help='number of results', type=int, default=10)
parser.add_argument('-t', help='string similarity threshold', type=float, default=0.8)
parser.add_argument('reference', help='string for comparison')
parser.add_argument('strings', help='strings to compare (or stem if paths)', nargs='+')
args = parser.parse_args()

sims = []
for string in args.strings:
    if Path(string).exists():
        string = Path(string).stem
    dist = textdistance.jaro_winkler(args.reference, string)
    sims.append((dist, string))

for dist, string in sorted(sims, reverse=True)[:args.n]:
    if dist > args.t:
        print(f"{dist:.3f}\t{string}")
