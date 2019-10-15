#!/usr/bin/env python3
import os
import sys
from argparse import ArgumentParser
from pathlib import Path


def parse_file(filename):
    name, cost = None, 0.0
    if not filename.is_file():
        return name, cost
    for line in filename.read_text().splitlines():
        if line.startswith('name: ') and not name:
            name = line[6:]
        if line.startswith('cost: ') and not cost:
            cost += float(line[6:])
    return name, int(cost)


def process_dir(path):
    summed = 0
    output = ""
    for file in path.glob('*'):
        name, cost = parse_file(file)
        summed += cost
        output += f"{int(cost):>8d} -- {name}\n"
    print(f"{path.stem:8s} ~ {int(summed)}")
    if args.verbose:
        sorted_lines = sorted(line for line in output.split('\n'))
        print('\n'.join(sorted_lines[::-1]))


parser = ArgumentParser('budget')
parser.add_argument('directory', nargs='?', help="Directory with costs")
parser.add_argument('-v', '--verbose', help="Show all costs", action='store_true')
parser.add_argument('-a', '--archive', help="Also show archive", action='store_true')
args = parser.parse_args()

root = os.environ['FINANCES']
if args.directory:
    root = args.directory
    dirs = [Path(root)]
elif root:
    dirs = [d for d in Path(root).glob('*') if d.is_dir()]
else:
    print("Must provide DIRECTORY arg, or set FINANCES env var.")
    sys.exit(1)

for direc in dirs:
    if 'archive' in str(direc) and not args.archive:
        continue
    process_dir(direc)
