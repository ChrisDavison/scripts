#!/usr/bin/env python3
"""
Print passed string/filename without extension.
"""
from pathlib import Path
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("file", type=Path)
filename = parser.parse_args().file

print(filename.stem)
