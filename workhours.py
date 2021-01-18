#!/usr/bin/env python3
import datetime
import os
import sys
import string
from argparse import ArgumentParser


def workable_hours(year, month):
    today = datetime.date.today()
    year = int(year) if year else today.year
    month = int(month) if month else today.month
    start = datetime.date(year, month, 1)
    temp = start
    workable = 0
    while temp.month == start.month:
        if temp.weekday() < 5:
            workable += 1
        temp += datetime.timedelta(days=1)
    when = start.strftime("%Y-%m")
    print(f"{when}: {workable} weekdays ({workable * 8} hr)")


if __name__ == "__main__":
    p = ArgumentParser()
    p.add_argument("-y", "--year")
    p.add_argument("-m", "--month")
    args = p.parse_args()
    workable_hours(args.year, args.month)
