#!/usr/bin/env python3
"""
Calculate the precision of a floating point number (either single- or
double-precision). It determines how many values the mantissa can represent,
and then calculates the bin size for the power-of-2 window that NUM falls into.
"""
import math
import argparse


def main(num, double_precision=False, verbose=False):
    mantissa_bits = 52 if double_precision else 23
    power = math.floor(math.log2(num))
    exponent = power + 127
    lower = 2**power
    upper = lower * 2
    mantissa = math.ceil(2**mantissa_bits * ((num - lower) / (upper - lower)))
    n_vals = math.pow(2, mantissa_bits)
    sign = 0 if num > 0 else 1
    if verbose:
        prec = 'double' if double_precision else 'single'
        print(f"{num} falls in range {lower}..{upper}")
        print(f"{prec}-precision => {int(n_vals)} bins")
        print("giving precision ", end="")
    print((upper - lower) / n_vals)
    # if verbose:
    #     print(f"S{sign} E{exponent} M{mantissa}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-d", "--double", help="Use double-precision", action="store_true")
    parser.add_argument("-v", "--verbose", help="Show more information", action="store_true")
    parser.add_argument("NUM", type=float)
    args = parser.parse_args()
    main(args.NUM, args.double, args.verbose)
