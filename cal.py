#!/usr/bin/env python3
import datetime
import os
import sys
from argparse import ArgumentParser
from pathlib import Path


def month_cal(year, month, start_day_of_week=0, simple_display=False):
    start_day_of_week = start_day_of_week % 7
    today = datetime.date.today()
    year = int(year) if year else today.year
    month = int(month) if month else today.month
    start = datetime.date(year, month, 1)
    by_weekday, week, temp = [], [], start
    while temp.month == start.month:
        if temp.weekday() == start_day_of_week:
            if week:
                by_weekday.append(week)
            week = [temp]
        else:
            week.append(temp)
        temp += datetime.timedelta(days=1)
    by_weekday.append(week)
    by_weekday

    print(start.strftime("%B %Y").center(20))
    headers = ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su']
    headerstr = ' '.join(headers[start_day_of_week:] + headers[:start_day_of_week])
    N = len(headerstr)
    topbot_border = f'+{"-"*(N+2)}+'
    pipeize = lambda x: f"| {x} |"
    if simple_display:
        pipeize = lambda x: x
        print(headerstr)
    else:
        print(topbot_border)
        print(pipeize(headerstr))
        print(topbot_border)
    for i, week in enumerate(by_weekday):
        aligned_week = [str(w.day).rjust(2) for w in week] 
        w = ' '.join(aligned_week)
        justified = w.ljust(20) if i else w.rjust(20)
        print(pipeize(justified))
    if not simple_display:
        print(topbot_border)


if __name__ == "__main__":
    p = ArgumentParser()
    p.add_argument('-y', '--year')
    p.add_argument('-m', '--month')
    p.add_argument('-s', '--simple', help="Print without border",
            action="store_true")
    args = p.parse_args()
    start_day_of_week = 0
    sys.exit(month_cal(args.year, args.month, start_day_of_week, args.simple))
