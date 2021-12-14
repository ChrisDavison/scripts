#!/usr/bin/env python3
from argparse import ArgumentParser
import edifice as ed
from edifice import Label, TextInput, View


def pressure(weight, tyre_width, front_wheel_load=0.45):
    # Weight should be weight of rider + bike + extras (water bottles etc)
    weight_front = weight * front_wheel_load
    weight_rear = weight * (1 - front_wheel_load)

    psi_front = (338.14 * weight_front / tyre_width ** 1.5785) - 7.1685
    psi_rear = (338.14 * weight_rear / tyre_width ** 1.5785) - 7.1685

    print(f"Front: {int(psi_front)} psi\nRear: {int(psi_rear)} psi")


parser = ArgumentParser()
parser.add_argument("--bodyweight", type=float)
parser.add_argument("--bike-weight", type=float)
parser.add_argument("--tyre-width", type=float)
args = parser.parse_args()

bodyweight = args.bodyweight if args.bodyweight else float(
    input("Bodyweight (kg): "))
bikeweight = args.bike_weight if args.bike_weight else float(
    input("Bike weight (kg): "))
tyrewidth = args.tyre_width if args.tyre_width else float(
    input("Tyre width (mm): "))

pressure(
    weight=bodyweight + bikeweight,  # bike, me, water
    tyre_width=tyrewidth,
)

# pressure(
#     weight=15 + 80 + 1,  # bike, me, water
#     tyre_width=25,
# )
