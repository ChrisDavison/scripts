#!/usr/bin/env python3
"""Print out the list of dates in this month, as a markdown list"""
import datetime
import sys


offset = 0
if len(sys.argv) > 1:
    offset = int(sys.argv[1])
today = datetime.date.today()
tmp = datetime.date(today.year, today.month + offset, 1)
end = datetime.date(today.year, today.month+1 + offset, 1)
print(f"# {tmp.strftime('%B')}\n")
while tmp < end:
    print(f"- `{tmp.day:2d}`: ")
    tmp += datetime.timedelta(days=1)
