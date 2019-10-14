#!/usr/bin/env python3
import os
import sys
from argparse import ArgumentParser
from pathlib import Path

parser = ArgumentParser('budget')
parser.add_argument('directory', nargs='?', help="Directory with costs")
parser.add_argument('-v', '--verbose', help="Show all costs", action='store_true')
args = parser.parse_args()

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


if not args.directory:
    args.directory = os.environ['FINANCES']
    for path in Path(args.directory).glob('*'):
        if path.is_dir():
            process_dir(path)
else:
    process_dir(args.directory)
