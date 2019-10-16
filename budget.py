#!/usr/bin/env python3
import os
import re
import sys
from argparse import ArgumentParser
from collections import defaultdict, namedtuple
from pathlib import Path


RE_KEYWORD = re.compile(r"([a-zA-Z]+): (.*)")


BudgetItem = namedtuple('BudgetItem', 'name cost date notes')
BudgetDir = namedtuple('BudgetDir', 'directory budget_items')

class BudgetItem:
    def __init__(self, name, cost, date, notes, extra):
        self.name = name
        self.cost = cost
        self.date = date
        self.notes = notes
        self.extra = extra

    def __str__(self):
        return f"{int(self.cost):>8d} -- {self.name} {self.date}"

    def __repr__(self):
        output = f"{int(self.cost):>8d} -- {self.name} {self.date}"
        for note in self.notes:
            output += "\t" + note
        for kw, val in self.extra:
            output += "\t" + kw + ": " + val
        return output

    @staticmethod
    def from_filepath(filepath):
        if not filepath.is_file():
            return None
        keywords = defaultdict(list)
        name, cost, date, notes = None, 0.0, "", []
        for line in filepath.read_text().splitlines():
            m = RE_KEYWORD.match(line)
            if m and m.group(1) == 'name':
                name = m.group(2)
            elif m and m.group(1) == 'cost':
                cost = float(m.group(2))
            elif m and m.group(1) == 'date':
                date = m.group(2)
            elif m:
                keywords[m.group(1)].append(m.group(2))
            elif line:
                notes.append(line)
        return BudgetItem(name, cost, date, notes, extra)


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


def process_dir(path):
    output = []
    for file in path.glob('*'):
        current = []
        keywords = parse_file(file)
        name = keywords['name'][0]
        cost = float(keywords.get('cost', [0])[0])
        date = keywords.get('date', [''])[0]
        date = f"({date})" if date else ""
        current.append(f"{int(cost):>8d} -- {name} {date}")
        if args.verbose:
            for line in keywords.get('notes', []):
                current.append(f"\t\t\t{line}")
        output.append((cost, '\n'.join(current)))
    summed = sum([cost for cost, _ in output])
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
