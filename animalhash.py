#!/usr/bin/env python3
import os
import os.path as op
import sys
from random import choice
from pathlib import Path


def main():
    script_path = Path(op.dirname(op.realpath(__file__)))
    word_path = script_path / "words"
    animals = (word_path / "animals.txt").resolve().read_text().splitlines()
    adjectives = (word_path / "adjectives.txt").resolve().read_text().splitlines()
    colours = (word_path / "colours.txt").resolve().read_text().splitlines()
    print("-".join([choice(adjectives), choice(colours), choice(animals)]))


if __name__ == "__main__":
    sys.exit(main())
