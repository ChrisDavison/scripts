#!/usr/bin/env python3
from collections import defaultdict
import datetime
import os
import sys

fn = os.environ['FINANCEFILE']
data = [line.strip().split(',') for line in open(fn)][1:]
spacer = ""
if len(sys.argv) > 1:
    data = [row for row in data if row[0].startswith(sys.argv[1])]
    spacer = "\t"

grouped_by_category = defaultdict(list)
for row in data:
    grouped_by_category[row[3]].append(row)

cat_items_tot = [(category, items, sum(float(item[1]) for item in items))
                 for category, items in grouped_by_category.items()]
cat_items_tot_sorted = sorted(cat_items_tot, key=lambda x: x[2])[::-1]

if len(sys.argv) > 1:
    print("{} - {:4.0f} GBP".format(sys.argv[1], sum(s[2] for s in cat_items_tot_sorted)))
print("{}CATEGORY : GBP : # : MEAN".format(spacer))
print("{}-------- : ----- : ----- : -----".format(spacer))
len_longest_line = 0
for category, items, tot in cat_items_tot_sorted:
    N = len(items)
    line = "{}{} : {:4.0f} : {:2d} : {:4.0f}".format(spacer, category, tot, N, tot / N)
    print(line)
    if len(line) > len_longest_line:
        len_longest_line = len(line)
