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


CASSETTE_GRAVEL = np.array([11, 13, 15, 17, 19, 21, 23, 25, 27, 30, 34])
CASSETTE_FIXIE = np.array([16])

CHAINRING_ROAD = np.array([52, 36]).reshape((2, 1))
CHAINRING_GRAVEL = np.array([46, 30]).reshape((2, 1))
CHAINRING_FIXIE = np.array([44])

GI_GRAVEL = gearinches(CHAINRING_GRAVEL, CASSETTE_GRAVEL)
GI_ROAD = gearinches(CHAINRING_ROAD, CASSETTE_GRAVEL)
GI_FIXIE = gearinches(CHAINRING_FIXIE, CASSETTE_FIXIE)


def main(which):
    cassette = None
    chainring = None
    if which == 'gravel':
        cassette = CASSETTE_GRAVEL
        chainring = CHAINRING_GRAVEL
    elif which == 'fixie':
        cassette = CASSETTE_FIXIE
        chainring = CHAINRING_FIXIE
    else: #which == 'road'
        cassette = CASSETTE_GRAVEL
        chainring = CHAINRING_ROAD

    gear_inches = gearinches(chainring, cassette)
    def as_ints(xs):
        if not any([isinstance(xs, list), isinstance(xs, np.ndarray)]):
            xs = [xs]
        return ' '.join(f"{x:4.1f}" for x in xs)

    combined_gearinches = sorted([
        (f"{str(int(val)):>4}", i) for i, row in enumerate(gear_inches) for val in row
    ])
    print(f"Gearinches of {which} bike")
    for i, teeth in enumerate(chainring):
        gi_for_teeth = [gi if j == i else '  --' for gi, j in combined_gearinches][::-1]
        if isinstance(teeth, np.int64):
            teeth = [teeth]
        median = np.abs(np.median(np.diff([int(val.strip()) for val in gi_for_teeth if val != '  --'])))
        stats = f"Median gap: {median}"
        print(f"  {teeth[0]}t: {''.join(gi_for_teeth)} ({stats})")

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('which', choices=['gravel', 'fixie', 'road'])
    args = parser.parse_args()
    main(args.which)

