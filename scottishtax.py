#!/usr/bin/env python3
import sys
import numpy as np
from collections import namedtuple
from argparse import ArgumentParser

from numpy.core.numeric import Infinity


rate = namedtuple("rate", "name limit rate")


def scottish_tax_calculator(wage, verbose=True):
    original_wage = wage
    outstr = ""
    rates = sorted(
        [
            rate("ZERO", 0, 0),
            rate("personal", 12500, 0),
            rate("starter", 14585, 0.19),
            rate("basic", 25158, 0.2),
            rate("intermediate", 43430, 0.21),
            rate("higher", 150000, 0.41),
            rate("final", np.Infinity, 0.46),
        ],
        key=lambda x: x.limit,
    )
    total_paid = 0
    for rate_l, rate_h in zip(rates[:-1], rates[1:]):
        ratepct = int(100 * rate_h.rate)
        band = rate_h.limit - rate_l.limit
        paid = rate_h.rate * np.min([band, wage])
        outstr += f"{rate_l.limit:7.0f} to {rate_h.limit:7.0f} ({band:5.0f}) at {ratepct:3d}%\n"

        total_paid += paid
        if band > wage:
            if verbose:
                outstr += "...taxed all taxable wages\n"
            break
        wage -= band

    effective_rate = total_paid / original_wage
    outstr += "\n"
    outstr += f"From {original_wage}, ~{total_paid:.0f} was paid in tax\n"
    outstr += f"    effective rate {100 * effective_rate:.0f}%\n"
    outstr += "\n"
    outstr += f"Take home: ~{original_wage - total_paid:.0f} / yr\n"
    outstr += f"           ~{(original_wage - total_paid) / 12:.0f} / mo"
    if verbose:
        print(outstr)
    else:
        print(f"Pay £{total_paid:.02f}")


parser = ArgumentParser("scottishtax")
parser.add_argument("-v", "--verbose", action="store_true", default=False)
parser.add_argument("wage", type=int)
args = parser.parse_args()

wage = args.wage if args.wage else int(input("Wage? "))
scottish_tax_calculator(wage, args.verbose)
