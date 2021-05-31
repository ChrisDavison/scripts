#!/usr/bin/env python3
import os
import sys

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


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(f"usage: {os.path.basename(sys.argv[0])} <value> <lb|st|kg>")
        sys.exit(1)

    kg = parse_weight(float(sys.argv[1]), sys.argv[2])
    df = pd.DataFrame([kg], columns=["kg"])
    df["lb"] = df["kg"] * 2.2
    df["st"] = df["lb"] / 14
    df["lost (kg)"] = 117.0 - df["kg"]
    print(df)
