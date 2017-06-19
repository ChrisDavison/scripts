#! /usr/bin/env python3
"""Weight converter.

Given a weight in either kilogram, pound, or St, or StLb,
show weight in all other units.

Usage:
    conv.py WEIGHT

Options:
    -h --help     Show this message.
    -v --version  Show version.

Examples:
    conv.py 17.4stlb =>
    conv.py 99.2kilogram =>
"""
import re
from docopt import docopt


def from_kg(value):
    """Convert a weight from kilogram to other options"""
    kilogram = '{:.2f}kg'.format(value)
    pound = '{:.2f}lb'.format(value * 2.205)
    stone_int = int(value * 0.157)
    lb_after_stone = int(((value * 0.157) - stone_int)*14)
    stone_lb = '{}st{}lb'.format(stone_int, lb_after_stone)
    print("{} {} {}".format(kilogram, pound, stone_lb))

def stone_to_kg(value):
    """Convert a weight from stone to kilogram"""
    full = value
    fraction = 0
    if '.' in str(value):
        full, fraction = str(value).split('.')
    return float(full) * 6.350 + (float(fraction) * .6350)

def lb_to_kg(value):
    """Convert a weight from pound to kilogram"""
    if not isinstance(value, (int, float)):
        return None
    if value <= 0:
        return None
    return value * 0.454


def stonelb_to_kg(value):
    """Convert a weight from stone+pound to kilogram"""
    if value <= 0:
        return None
    st_kg = stone_to_kg(int(value))
    lb_kg = lb_to_kg(10 * (value - int(value)))
    return st_kg + lb_kg


def main(weight):
    """Run the weight conversion program"""
    value, unit = re.match(r'([.0-9]+)(\D+)', weight.groups())
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


if __name__ == "__main__":
    ARGS = docopt(__doc__, version="0.0.1")
    main(ARGS['WEIGHT'])
