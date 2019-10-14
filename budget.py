#!/usr/bin/env python3
import os
import sys
from argparse import ArgumentParser
from pathlib import Path


def process_dir(path):
    files = [f for f in path.glob('*')
        if f.is_file()
    ]
    summed = 0
    output = ""
    for file in files:
        data = file.read_text().split('\n')
        name = [line[6:] for line in data if line.startswith('name: ')][0]
        cost = sum([float(line[6:]) for line in data if line.startswith('cost: ')])
        summed += cost
        output += f"{cost:8.0f}\t{name:10s}\n"
    print(f"TOTAL for {path.stem} -- {summed:.1f}")
    if args.verbose:
        print(output)


parser = ArgumentParser('budget')
parser.add_argument('directory', nargs='?', help="Directory with costs")
parser.add_argument('-v', '--verbose', help="Show all costs", action='store_true')
args = parser.parse_args()

root = os.environ['FINANCES']
if args.directory:
    root = args.directory
elif root:
    dirs = [d for d in Path(root).glob('*') if d.is_dir()]
else:
    print("Must provide DIRECTORY arg, or set FINANCES env var.")
    sys.exit(1)

for direc in dirs:
    process_dir(direc)
