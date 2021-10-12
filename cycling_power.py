#!/usr/bin/env python3
from argparse import ArgumentParser


def main(ftp, weight):
    print(f"Power zones for ftp of {ftp:.0f}W")
    def pct_range(ftp, pct1, pct2):
        lower = int(ftp * pct1 / 100)
        upper = int(ftp * pct2 / 100)
        return f"{lower:3d}W to {upper:3d}W ({pct1} to {pct2} %)"
    print(f"     Recovery    {pct_range(ftp, 0, 55)}")
    print(f"     Endurance   {pct_range(ftp, 55, 75)}")
    print(f"     Sweetspot   {pct_range(ftp, 75, 90)}")
    print(f"     Threshold   {pct_range(ftp, 90, 105)}")
    print(f"     VO2Max      {pct_range(ftp, 105, 120)}")

    print(f"\nTheoretical W/kg")
    print(f"    Current -- {ftp / weight:.1f} W/kg")
    print()
    print(f"    for 4   W/kg, need {4 * weight:.0f} W")
    print(f"    for 3.5 W/kg, need {3.5 * weight:.0f} W")
    print(f"    for 3   W/kg, need {3 * weight:.0f} W")


if __name__ == "__main__":
    parser = ArgumentParser("cycling power")
    parser.add_argument("--ftp", type=float, required=True)
    parser.add_argument("--weight", type=float, help="Weight in kg", required=True)
    args = parser.parse_args()

    main(args.ftp, args.weight)


