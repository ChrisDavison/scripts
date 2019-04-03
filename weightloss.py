#!/usr/bin/env python3
import os
import sys
from pathlib import Path

import click
start_kg = 115

@click.group()
def cli():
    """Print weight in kg, stone, and lb, and weightloss in kg"""
    pass

@cli.command("kg", short_help="Convert from kg")
@click.argument("kg", nargs=1, type=float)
def from_kg(kg):
    convert_from_kg(kg)


@cli.command("st", short_help="Convert from stone")
@click.argument("stone", nargs=1, type=float)
def from_stone(stone):
    convert_from_kg(stone * 14 / 2.2)


@cli.command("lb", short_help="Convert from lb")
@click.argument("lb", nargs=1, type=float)
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

cli()
