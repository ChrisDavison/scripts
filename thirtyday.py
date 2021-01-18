#!/usr/bin/env python3
from datetime import date, timedelta
from argparse import ArgumentParser
import sys


def thirtyday(*, start, title, dated):
    shift = timedelta(days=1)
    end = start + timedelta(days=30)

    days = 'MTWTFSS'
    daycal = ''
    day = start
    for _ in range(30):
        daycal += days[day.weekday()]
        if day.weekday() == 6:
            daycal += ' '
        day += shift
    dateheader = ''
    if dated:
        startstr = start.strftime("%F")
        endstr = end.strftime("%F")
        n_dots = len(daycal) - 22
        dots = "." * n_dots
        dateheader = f"{startstr} {dots} {endstr}"
    out = []
    if title:
        out.append(title)
    if dated:
        out.append(dateheader)
    out.append(daycal)
    return '\n'.join(out)


if __name__ == "__main__":
    parser = ArgumentParser(description="Get a thirtyday challenge calendar")
    parser.add_argument('-s', help='Days to shift start', type=int, default=0)
    parser.add_argument('-t', '--title',
                        help='Title to show above calendar', type=str)
    parser.add_argument('-d', '--dated',
                        help='Show start and end date', action='store_true')
    args = parser.parse_args()
    start = date.today() + timedelta(days=args.s)
    print(thirtyday(start=start, title=args.title, dated=args.dated))


