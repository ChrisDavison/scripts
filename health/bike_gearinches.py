#!/usr/bin/env python3
import numpy as np
from argparse import ArgumentParser


def gearinches(chainring, cassette_range, wheel_diameter_inch=26.5):
    """Convert gear ratios into gearinches"""
    return chainring / cassette_range * wheel_diameter_inch

def cadence_to_speed(cadence, ratio, wheel_diameter_inch=26.5):
    """Calculate approximate speed for a given cadence, gear ratio, and wheel size

    This is an approximation that does not consider tyre size, however it
    shouldn't be too far off.

    Arguments
    ---------
    cadence - pedaling rate in rpm
    ratio - gear ratio (i.e. chainring / cassette)
    wheel_diameter_inch - diameter of the wheel
        default = 26.5 (700c wheel), which doesn't include tyre

    Returns
    -------
    speed - bike speed in mph
    """
    diam_mile = wheel_diameter_inch * 2.54 / 100 / 1600
    dist_per_durn = diam_mile * ratio * np.pi
    turns_per_hour = cadence * 60
    speed = dist_per_durn * turns_per_hour
    return speed

def speed_to_cadence(speed, ratio, wheel_diameter_inch=26.5):
    """Calculate approximate cadence for a given speed, gear ratio, and wheel size

    This is an approximation that does not consider tyre size, however it
    shouldn't be too far off.

    Arguments
    ---------
    speed - bike speed in mph
    ratio - gear ratio (i.e. chainring / cassette)
    wheel_diameter_inch - diameter of the wheel
        default = 26.5 (700c wheel), which doesn't include tyre

    Returns
    -------
    cadence - pedaling rate in rpm
    """
    diam_mile = wheel_diameter_inch * 2.54 / 100 / 1600
    dist_per_turn = diam_mile * ratio * np.pi
    turns_per_hour = speed / dist_per_turn
    cadence = turns_per_hour / 60
    return cadence


CASSETTES = {
    "11-28": np.array([11, 12, 13, 14, 15, 17, 19, 21, 23, 25, 28]),
    "11-30": np.array([11, 12, 13, 14, 15, 17, 19, 21, 24, 27, 30]),
    "11-32": np.array([11, 12, 13, 14, 16, 18, 20, 22, 25, 28, 32]),
    "11-34": np.array([11, 13, 15, 17, 19, 21, 23, 25, 27, 30, 34]),
    "12-25": np.array([12, 13, 14, 15, 16, 17, 18, 19, 21, 23, 25]),
    "fixie": np.array([16])
}

CHAINRINGS = {
    'large':   np.array([53, 39]).reshape((2, 1)),
    'road':    np.array([52, 36]).reshape((2, 1)),
    'compact': np.array([50, 34]).reshape((2, 1)),
    'gravel':  np.array([46, 30]).reshape((2, 1)),
    'fixie':   np.array([44])
}

def main(chainring, cassette):
    cassette = CASSETTES[cassette]
    chainring = CHAINRINGS[chainring]

    gear_inches = gearinches(chainring, cassette)

    combined_gearinches = sorted([
        (f"{str(int(val)):>4}", i) for i, row in enumerate(gear_inches) for val in row
    ])
    low = min(cassette)
    high = max(cassette)
    print(f"Chainring: {[v for x in chainring.tolist() for v in x]}")
    print(f"Cassette:  {low}..{high}")
    print()
    for i, teeth in enumerate(chainring):
        gi_for_teeth = [gi if j == i else '  --' for gi, j in combined_gearinches][::-1]
        if isinstance(teeth, np.int64):
            teeth = [teeth]
        print(f"{''.join(gi_for_teeth)}")

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('chainring', choices=[k for k in CHAINRINGS.keys()])
    parser.add_argument('cassette', choices=[k for k in CASSETTES.keys()])
    args = parser.parse_args()
    main(args.chainring, args.cassette)

