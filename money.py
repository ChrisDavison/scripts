#!/usr/bin/env python3
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("--savings", type=float)
parser.add_argument("--monthly", type=float)
parser.add_argument("--out", type=float)
parser.add_argument("--inheritance", type=float)
args = vars(parser.parse_args())

def get_or_ask(name, msg):
    if args[name]:
        return args[name]
    else:
        response = input(msg + ": ")
        if response:
            return float(response)
        return 0

monthly = get_or_ask("monthly", "Monthly income")
out = get_or_ask("out", "Monthly outgoings")
savings = get_or_ask("savings", "Savings")
inheritance = get_or_ask("inheritance", "Inheritance")

print(f"After 12 months")
yearly_in = monthly * 12
yearly_delta = yearly_in - (out * 12)
final = savings + yearly_delta + inheritance 
print(f"{savings} + ({monthly} * 12) = {savings + yearly_in}")
print(f"- {out}/mo = {savings + yearly_delta}")
print(f"\nWith inheritance: {final}")
