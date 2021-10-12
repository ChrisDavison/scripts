#!/usr/bin/env python3
import numpy as np


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


def main():
    print("Gearinches of gravel bike\n")
    as_ints = lambda xs: list(map(int, xs))
    print("46t -- ", as_ints(GI_GRAVEL[0][:-2]))
    print("30t -- ", as_ints(GI_GRAVEL[1][2:]))

    # print()
    # print("Gearinches for 'road' chainrings")
    # print("46t -- ", as_ints(GI_ROAD[0][:-2]))
    # print("30t -- ", as_ints(GI_ROAD[1][2:]))


if __name__ == "__main__":
    main()

