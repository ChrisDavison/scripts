#!/usr/bin/env python
import datetime
import os
import sys
from argparse import ArgumentParser
from pathlib import Path


def month_cal(year, month, start_day_of_week=0):
    start_day_of_week = int(start_day_of_week) % 7
    today = datetime.date.today()
    year = int(year) if year else today.year
    month = int(month) if month else today.month
    start = datetime.date(year, month, 1)
    by_weekday, week, temp = [], [], start
    while temp.month == start.month:
        if temp.weekday() == start_day_of_week and week:
            by_weekday.append(week)
            week = []
        week.append(temp)
        temp += datetime.timedelta(days=1)
    if week:
        by_weekday.append(week)

    print(start.strftime("%B %Y").center(20))
    headers = ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su']
    headerstr = ' '.join(headers[start_day_of_week:] + headers[:start_day_of_week])
    N = len(headerstr)
    topbot_border = f'+{"-"*(N+2)}+'
    outstr = headerstr + "\n"
    for i, week in enumerate(by_weekday):
        aligned_week = [str(w.day).rjust(2) for w in week] 
        w = ' '.join(aligned_week)
        justified = w.ljust(20) if i else w.rjust(20)
        outstr += justified + "\n"
    return outstr


if __name__ == "__main__":
    p = ArgumentParser()
    p.add_argument('-y', '--year')
    p.add_argument('-m', '--month')
    p.add_argument('-s', '--startofweek', default=0,
            help='Day of week to start (0=Monday)')
    args = p.parse_args()
    print(month_cal(args.year, args.month, args.startofweek))

