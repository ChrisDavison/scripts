#! /usr/bin/env python3
"""Weight converter.

Given a weight in either Kg, Lb, or St, or StLb,
show weight in all other units.

Usage:
    conv.py WEIGHT

Options:
    -h --help     Show this message.
    -v --version  Show version.

Examples:
    conv.py 17.4stlb =>
    conv.py 99.2kg =>
"""
from docopt import docopt
import re

def from_kg(value):
    kg = '{:.2f}kg'.format(value)
    lb = '{:.2f}lb'.format(value * 2.205)
    kg_int = int(value)
    kg_frac = (value - int(value))
    stone_int = int(value * 0.157)
    lb_after_stone = int(((value * 0.157) - stone_int)*14)
    stone_lb = '{}st{}lb'.format(stone_int, lb_after_stone)
    print("{} {} {}".format(kg, lb, stone_lb))

def stone_to_kg(value):
    full = value
    fraction = 0
    if '.' in str(value):
        full, fraction = str(value).split('.')
    return float(full) * 6.350 + (float(fraction) * .6350)

def lb_to_kg(value):
    if type(value) not in [int, float]:
        return None
    if value <= 0:
        return None
    return value * 0.454


def stonelb_to_kg(value):
    if value <= 0:
        return None
    st_kg = stone_to_kg(int(value))
    lb_kg = lb_to_kg(10 * (value - int(value)))
    return st_kg + lb_kg


if __name__ == "__main__":
    args = docopt(__doc__, version="0.0.1")

    units = ['kg', 'lb', 'st', 'stlb']
    value, unit = re.match('([.0-9]+)(\D+)', args['WEIGHT']).groups()
    unit = unit.lower()
    value = float(value)
    if unit == 'kg':
        print(from_kg(value))
    elif unit == 'lb':
        from_kg(lb_to_kg(value))
    elif unit == 'st':
        from_kg(stone_to_kg(value))
    elif unit == 'stlb':
        stonelb_to_kg(value)
    else:
        print("Unit not supported")
