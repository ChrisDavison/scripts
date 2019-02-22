#!/usr/bin/env python3
from collections import defaultdict
import datetime
import os
import sys

fn = os.environ['FINANCEFILE']
data = [line.strip().split(',') for line in open(fn) if line.startswith(sys.argv[1])]

grouped_by_category = defaultdict(list)
for row in data:
    grouped_by_category[row[3]].append(row)

widest_str = max(len(s[0]) for s in grouped_by_category.keys())

print("{}".format(sys.argv[1]))
grand_tot, num_items = 0, 0
for category, items in grouped_by_category.items():
    tot = sum(float(item[1]) for item in items)
    grand_tot += tot
    num_items += len(items)
    print("\t{:20s}{:.2f} ({})".format(category, tot, len(items)))
print("\t{}".format("-"*40))
print("\t{:20s}{:.2f} ({})".format("TOTAL", grand_tot, num_items))

