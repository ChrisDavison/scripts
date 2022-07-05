#!/usr/bin/env python3
from argparse import ArgumentParser


def pressure(weight, tyre_width, front_wheel_load=0.45):
    # Weight should be weight of rider + bike + extras (water bottles etc)
    weight_front = weight * front_wheel_load
    weight_rear = weight * (1 - front_wheel_load)

    psi_front = (338.14 * weight_front / tyre_width ** 1.5785) - 7.1685
    psi_rear = (338.14 * weight_rear / tyre_width ** 1.5785) - 7.1685

    print(f"Front: {int(psi_front)} psi\nRear: {int(psi_rear)} psi")


parser = ArgumentParser()
parser.add_argument("-w", "--weight", type=float, help="Weight of bike+rider+gear")
parser.add_argument("-t", "--tyre-width", type=float)
parser.add_argument("-l", "--front-tyre-load", type=float, default=0.45)
args = parser.parse_args()

weight = args.weight if args.weight else float(input("System weight (kg): "))
tyrewidth = args.tyre_width if args.tyre_width else float(input("Tyre width (mm): "))

pressure(
    weight=weight,  # bike, me, water
    tyre_width=tyrewidth,
    front_wheel_load=args.front_tyre_load
)
