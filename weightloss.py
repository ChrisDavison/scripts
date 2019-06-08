#!/usr/bin/env python
import sys
start_kg = 115

def from_kg(kg):
    convert_from_kg(kg)


def from_stone(stone):
    convert_from_kg(stone * 14 / 2.2)


def from_pound(lb):
    convert_from_kg(lb / 2.2)


def convert_from_kg(kg):
    lb = kg * 2.2
    stone = lb / 14
    lost_kg = start_kg - kg
    print_weights(kg, lost_kg, stone, lb)

def print_weights(kg, lost_kg, stone, lb, divider="  "):
    kg_str = f"{kg:.1f}kg"
    stone_str = f"{stone:.1f}st"
    lb_str = f"{lb:.1f}lb"
    lost_str = f"Δ{lost_kg:.1f}kg"
    print(divider.join([kg_str, stone_str, lb_str, lost_str]))


usage = """weightloss (kg|st|lb) <value>"""
if len(sys.argv) < 3:
    print(usage)
    sys.exit(1)
cmd = sys.argv[1]
val = float(sys.argv[2])
if cmd == "kg":
    from_kg(val)
elif cmd in ("st", "stone"):
    from_stone(val)
elif cmd in ("kg", "kilograms"):
    from_kg(val)
else:
    print(usage)
