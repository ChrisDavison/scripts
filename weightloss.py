#!/usr/bin/env python3

import os
import sys

if len(sys.argv) < 3:
    print("usage: {basename} <value> <lb|st|kg>".format(basename=os.path.basename(sys.argv[0])))
    sys.exit(1)

weight = int(sys.argv[1])
unit = sys.argv[2]

if unit == "st":
    value_kg = weight * 14.0 / 2.2
elif unit == "lb":
    value_kg = weight / 2.2
else:
    value_kg = weight

START = 117.0
value_st = value_kg * 2.2 / 14
value_lb = value_kg * 2.2

print("{:.1f}kg {:.1f}st {:.1f}lb (lost {:.1f}kg)".format(value_kg, value_st, value_lb, START-value_kg))
