#!/usr/bin/env python3
"""
Precision of a floating point number.
"""
import math
import argparse


def main(num, double_precision=False):
    mantissa_bits = 52 if double_precision else 23
    lower = 2**math.floor(math.log2(num))
    upper = lower * 2
    n_vals = math.pow(2, mantissa_bits)
    print((upper - lower) / n_vals)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--double", help="Use double-precision", action="store_true")
    parser.add_argument("num", type=float)
    args = parser.parse_args()
    main(args.num, args.double)
