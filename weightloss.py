#!/usr/bin/env python3
import os
import sys
from pathlib import Path

import click

@click.group()
def cli():
    pass

@cli.command("kg")
@click.argument("kg", nargs=1, type=float)
def from_kg(kg):
    lb = kg * 2.2
    stone = lb / 14
    print(f"{kg:.1f}kg\t{stone:.1f}st\t{lb:.1f}lb")


@cli.command("st")
@click.argument("stone", nargs=1, type=float)
def from_stone(stone):
    lb = stone * 14
    kg = lb / 2.2
    print(f"{kg:.1f}kg\t{stone:.1f}st\t{lb:.1f}lb")


@cli.command("lb")
@click.argument("lb", nargs=1, type=float)
def from_pound(lb):
    stone = lb / 14
    kg = lb / 2.2
    print(f"{kg:.1f}kg\t{stone:.1f}st\t{lb:.1f}lb")


cli()
