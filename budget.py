#!/usr/bin/env python3
from collections import defaultdict, namedtuple
import re
import sys
import os

def boxed_text(text, width):
    space_width = (width - len(text)) / 2
    space_left = "=" * int(space_width)
    space_right = space_left
    if space_width != int(space_width):
        space_right += "="
    print("=" * width)
    print("{} {} {}".format(space_left[:-1], text, space_right[:-1]))
    print("=" * width)

def parse_cost(line):
    re_cost = re.compile(r"(.*) -- £(.*)")
    m = re_cost.search(line)
    if m:
        number = m.groups()[1]
        text = m.groups()[0]
        return Cost(int(number), text)
    return None

def summarise(savings, income, costs, verbose=False):
    boxed_text("BASELINE", 20)
    print("{:10s} £{}".format("Savings", savings))
    print("{:10s} £{}".format("Income", income))
    print()
    boxed_text("COSTS", 20)
    for category, items in costs.items():
        total = sum([item.value for item in items])
        print("{:10s} £{}".format(category, int(total)))

    projected_spend = sum([item.value for item in costs['To Buy']]) + sum([item.value for item in costs['Spent']])
    print("{:10s} £{}".format("Projected", projected_spend))

def parse_costs(file):
    category_and_costs = defaultdict(list)
    current_category = None
    savings, income = 0, 0
    for line in file:
        line = line.strip()
        is_dash_line = all([c == "-" for c in line])
        if not line or is_dash_line:
            continue
        elif line.startswith('Income'):
            income = int(line.split(' ')[1])
            continue
        elif line.startswith('Savings'):
            savings = int(line.split(' ')[1])
            continue
        elif '-- £' in line:
            category_and_costs[current_category].append(parse_cost(line))
        else:
            current_category = line
    return savings, income, category_and_costs

if __name__ == "__main__":
    Cost = namedtuple('Cost', 'value description')
    file = sys.stdin
    fn_budget = os.environ.get("BUDGET", None)
    if fn_budget:
        file = open(fn_budget)
    summarise(*parse_costs(file))
