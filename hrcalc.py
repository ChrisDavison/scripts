#!/usr/bin/env python3
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("--age", default=30, type=int)
parser.add_argument("-rhr", default=64, type=int)
parser.add_argument("-l", "--lower", required=True, type=int)
parser.add_argument("-u", "--upper", required=True, type=int)

args = parser.parse_args()

whr = 220 - args.age - args.rhr
targetLow = whr * (args.lower / 100.0) + args.rhr
targetHigh = whr * (args.upper / 100.0) + args.rhr

print(f"Working Heartrate: {whr}bpm")
print(f"  {args.lower} % to {args.upper} %")
print(f"  {targetLow} bpm to {targetHigh} bpm")
