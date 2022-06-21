#!/usr/bin/env python
from argparse import ArgumentParser


parser = ArgumentParser()
parser.add_argument('mpg', type=float)
parser.add_argument('cost_per_litre', type=float)
args = parser.parse_args()

LITRES_IN_GAL = 4.55

cost_per_gallon = args.cost_per_litre * LITRES_IN_GAL
print(f"{args.mpg:.0f}mpg at £{args.cost_per_litre:.2f}/l => £{cost_per_gallon / args.mpg:.2f}/mi")
