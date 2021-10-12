#!/usr/bin/env python3
import os
import sys
from argparse import ArgumentParser

import pandas as pd


def parse_weight(value, unit):
    if unit == "st":
        return value * 14.0 / 2.2
    elif unit == "lb":
        return value / 2.2
    else:
        return value


def display(now_kg, start_kg=117):
    start_kg = 117.0
    value_st = now_kg * 2.2 / 14
    diff = start_kg - now_kg
    pct = now_kg / start_kg * 100
    pct_lost = 100 - pct

    print(now_kg, end="\t")
    print(f"({value_st}st)")
    print(f"LOST {diff}kg\n\t{pct_lost}%")


def main():
    parser = ArgumentParser("Weightloss calculator")
    parser.add_argument("value", type=float)
    parser.add_argument("unit", help="The unit of the value given (lb|st|kg)")
    args = parser.parse_args()

    start_weight = 117
    kg = parse_weight(args.value, args.unit)
    df = pd.DataFrame([kg], columns=["kg"])
    height_ft = (5,9)
    height_m = (12 * height_ft[0] + height_ft[1]) * 2.54 / 100
    df["lb"] = df["kg"] * 2.2
    df["st"] = df["lb"] / 14
    df["lost (kg)"] = start_weight - df["kg"]
    df["bmi"] = df["kg"] / (height_m ** 2)
    print(df.to_markdown(index=False, floatfmt=".2f"))

if __name__ == "__main__":
    main()
