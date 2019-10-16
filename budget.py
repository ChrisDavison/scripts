#!/usr/bin/env python3
import os
import re
import sys
from argparse import ArgumentParser
from collections import defaultdict
from pathlib import Path


RE_KEYWORD = re.compile(r"([a-zA-Z]+): (.*)")


def parse_file(filename):
    name, cost = None, 0.0
    if not filename.is_file():
        return name, cost
    keywords = defaultdict(list)
    extra = []
    for line in filename.read_text().splitlines():
        m = RE_KEYWORD.match(line)
        if m:
            keywords[m.group(1)].append(m.group(2))
        elif line:
            extra.append(line)
    keywords['notes'] = extra
    return keywords


# def budget_string_repr(file_keywords, verbose):
#     name = keywords['name'][0]
#     cost = float(keywords.get('cost', [0])[0])
#     date = keywords.get('date', [''])[0]
#     date = f"({date})" if date else ""



def process_dir(path):
    summed = 0
    output = []
    for file in path.glob('*'):
        current = []
        keywords = parse_file(file)
        name = keywords['name'][0]
        cost = float(keywords.get('cost', [0])[0])
        date = keywords.get('date', [''])[0]
        date = f"({date})" if date else ""
        summed += cost
        current.append(f"{int(cost):>8d} -- {name} {date}")
        if args.verbose:
            for line in keywords.get('notes', []):
                current.append(f"\t\t\t{line}")
        output.append((cost, '\n'.join(current)))
    print(f"{path.stem:8s} ~ {int(summed)}")
    if args.verbose:
        sorted_outputs = sorted(output, key=lambda x: x[0], reverse=True)
        for _, output in sorted_outputs:
            print(output)


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
    if 'archive' in str(direc) and not args.archive and not args.directory:
        continue
    process_dir(direc)
