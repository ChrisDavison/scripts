#!/usr/bin/env python3
import datetime
import os
import sys
import string
from argparse import ArgumentParser


def month_cal(year, month, start_day_of_week=0, indented=False):
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

    leading = '    ' if indented else ''
    outstr = leading + start.strftime("%B %Y").center(20) + "\n"
    headers = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]
    headerstr = " ".join(headers[start_day_of_week:] + headers[:start_day_of_week])
    N = len(headerstr)
    topbot_border = '+' + '-'*(N+2) + '+'
    outstr += leading + headerstr + "\n"
    for i, week in enumerate(by_weekday):
        aligned_week = [str(w.day).rjust(2) for w in week]
        w = " ".join(aligned_week)
        justified = w.ljust(20) if i else w.rjust(20)
        outstr += leading + justified + "\n"
    return outstr.splitlines()


def make_journal(year, month):
    today = datetime.date.today()
    year = int(year) if year else today.year
    month = int(month) if month else today.month
    today = today.replace(year=year, month=month, day=1)
    print(datetime.date(year, month, 1).strftime("# %Y-%m %B\n"))
    print(month_cal(year, month, 0, indented=True))

    print("\n## Recurring\n")
    print("| Day | What |")
    print("|-----|------|")
    print("\n## Entries\n")
    print("| Day  | What |")
    print("|------|------|")
    while today.month == month:
        dow = 'MTWTFSS'[today.weekday()]
        print(f"| {today.day:2d}.{dow} |      |")
        today += datetime.timedelta(days=1)
    print()


if __name__ == "__main__":
    p = ArgumentParser()
    p.add_argument("-y", "--year")
    p.add_argument("-m", "--month")
    p.add_argument("-Y", "--full-year", help="Generate calendar for every month", action='store_true')
    p.add_argument(
        "-s", "--startofweek", default=0, help="Day of week to start (0=Monday)"
    )
    p.add_argument('-j', '--journal', help="Print in calendar journal-file format", default=False, action='store_true')
    args = p.parse_args()
    months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 
              'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
    month = args.month
    if args.month and args.month[0] in string.ascii_letters:
        month = months.index(args.month[:3]) + 1

    if args.full_year:
        divider = "\n" + "-" * 80 + "\n\n"
        calendars = ['\n'.join(month_cal(args.year, month, args.startofweek)) for month in range(1, 13)]
        print(divider.join(calendars))
    else:
        if args.journal:
            make_journal(args.year, args.month)
        else:
            print('\n'.join(month_cal(args.year, args.month, args.startofweek)))
