#!/usr/bin/env python3
import os
import re
import sys
from argparse import ArgumentParser
from collections import defaultdict, namedtuple
from pathlib import Path


RE_KEYWORD = re.compile(r"([a-zA-Z]+): (.*)")


BudgetItem = namedtuple('BudgetItem', 'name cost date')


def parse_budget_item(filepath):
    """Generate a BudgetItem from a file with key: value pairs"""
    if not filepath.is_file():
        return None
    keywords = defaultdict(list)
    for line in filepath.read_text().splitlines():
        m = RE_KEYWORD.match(line)
        if m:
            keywords[m.group(1)].append(m.group(2))
        elif line:
            keywords['notes'].append(line.strip())
    name = keywords.get('name', [None])[0]
    cost = keywords.get('cost', [None])[0]
    date = keywords.get('date', '')
    return BudgetItem(name, float(cost), date)


def budget_item_repr(budget_item):
    date = f" ({budget_item.date})" if budget_item.date else ''
    return f"{int(budget_item.cost):>8d} -- {budget_item.name}{date}"


def process_dir(path, verbose):
    if not isinstance(path, Path):
        path = Path(path)
    budgets = [parse_budget_item(f) for f in path.glob('*')]
    summed = sum([budget.cost for budget in budgets])
    print(f"{path.stem:8s} ~ £{int(summed)}")
    if verbose:
        for budget in sorted(budgets, key=lambda x: x.cost)[::-1]:
            print(budget_item_repr(budget))


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
    process_dir(direc, args.verbose)
