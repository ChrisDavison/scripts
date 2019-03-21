#!/usr/bin/env python3
"""Print out the list of dates in this month, as a markdown list"""
import datetime


today = datetime.date.today()
start_of_month = today - datetime.timedelta(days=today.day-1)
start_month_no = start_of_month.month
tmp = start_of_month
while tmp.month == start_month_no:
    print(f"- `{tmp.day:2d}`: ")
    tmp += datetime.timedelta(days=1)
