#!/usr/bin/env python3
from argparse import ArgumentParser

parser = ArgumentParser()
group = parser.add_mutually_exclusive_group()
group.add_argument("-v", metavar="VOLUME", type=int)
group.add_argument("-g", metavar="GRAMS", type=int)
parser.add_argument("-r", metavar="ML_PER_GRAM", type=int, default=16.7)
args = parser.parse_args()

print(f"Hoffman v60 Method")
if args.volume:
    ml = round(args.volume, 2)
    grams = int(ml / args.ratio)
elif args.grams:
    grams = args.grams
    ml = int(args.ratio * grams)
else:
    ml = 300
    grams = 18

bloom = grams * 2
first = ml * 0.6
second = ml * 0.4

print(f"{ml:.0f}ml → {grams}g ({ml / grams:.1f}:1)\n")
print(f"Bloom & swirl  {bloom:.0f}ml")
print(f"1st pour       {bloom:.0f} → {first:.0f}ml")
print(f"2nd pour       {first:.0f} → {first+second:.0f}ml")
