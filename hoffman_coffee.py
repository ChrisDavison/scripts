#!/usr/bin/env python3
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("-v", "--volume", type=int, default=300)
parser.add_argument("-r", "--ratio", type=int, help="Grams per litre", default=60)
args = parser.parse_args()

ml = args.volume
grams = args.ratio * ml / 1000
bloom = grams * 2
first = ml * 0.6
second = ml * 0.4

print(f"Hoffman v60 Method - {ml}ml of coffee ({args.volume / grams:.1f}:1)")
print(f"Coffee: {grams}g (then zero/tare)")
print(f"Bloom & swirl: {bloom}ml")
print(f"1st pour: up to {first}ml")
print(f"2nd pour: another {second}ml")
