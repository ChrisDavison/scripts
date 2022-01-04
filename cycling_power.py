#!/usr/bin/env python3
from argparse import ArgumentParser


def main(ftp, weight):
    norm_ftp = ftp / 100

    print(f"Power zones at {ftp:.0f}W FTP")
    print(f"    Recovery       {norm_ftp * 0:3.0f} to {norm_ftp * 55:3.0f}W")
    print(f"    Endurance      {norm_ftp * 55:3.0f} to {norm_ftp * 75:3.0f}W")
    print(f"    Sweetspot      {norm_ftp * 75:3.0f} to {norm_ftp * 90:3.0f}W")
    print(f"    Threshold      {norm_ftp * 90:3.0f} to {norm_ftp * 105:3.0f}W")
    print(f"    VO2Max         {norm_ftp * 105:3.0f} to {norm_ftp * 120:3.0f}W")
    print(f"    Anaerobic      {norm_ftp * 120:3.0f} to {norm_ftp * 150:3.0f}W")
    print(f"    Neuromuscular  >{norm_ftp * 150:3.0f}W")

    print(f"\nTheoretical W/kg ")
    print(f"    NOW {ftp / weight:.1f} W/kg")
    print(f"    for 4   W/kg, need {4 * weight:.0f} W")
    print(f"    for 3.5 W/kg, need {3.5 * weight:.0f} W")
    print(f"    for 3   W/kg, need {3 * weight:.0f} W")


if __name__ == "__main__":
    parser = ArgumentParser("cycling power")
    parser.add_argument("--ftp", type=float, required=True)
    parser.add_argument("--weight", type=float, help="Weight in kg", required=True)
    args = parser.parse_args()

    main(args.ftp, args.weight)


