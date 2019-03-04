#!/usr/bin/env python3
from collections import defaultdict
import datetime
import os
import sys

usage = """usage: total_by_category.py [date]

Date can be anything `YYYY-MM-DD`-like (will just search for this
prefix on the line, rather than anything fancy)
"""

if '-h' in sys.argv[1:]:
    print(usage)
    sys.exit(0)

fn = os.environ['FINANCEFILE']
query = sys.argv[1] if len(sys.argv) > 1 else ''
data = [line.strip().split(',') for line in open(fn)][1:]
data = [line for line in data if line[0].startswith(query)]

grouped_by_category = defaultdict(list)
for row in data:
    grouped_by_category[row[3]].append(row)

widest_str = max(len(s[0]) for s in grouped_by_category.keys())

print("{}".format(query))
grand_tot, num_items = 0, 0
for category, items in grouped_by_category.items():
    tot = sum(float(item[1]) for item in items)
    grand_tot += tot
    num_items += len(items)
    print("\t{:20s}{:.2f} ({})".format(category, tot, len(items)))
print("\t{}".format("-"*40))
print("\t{:20s}{:.2f} ({})".format("TOTAL", grand_tot, num_items))

