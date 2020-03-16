#!/usr/bin/env python3
from datetime import date, timedelta
from argparse import ArgumentParser
import sys

parser = ArgumentParser(description="Get a thirtyday challenge calendar")
parser.add_argument('-s', help='Days to shift start', type=int, default=0)
parser.add_argument('-t', '--title', help='Title to show above calendar', type=str)
parser.add_argument('-d', '--dated', help='Show start and end date', action='store_true')
args = parser.parse_args()

day = date.today() + timedelta(days=args.s)
shift = timedelta(days=1)

if args.title:
    print(args.title)
if args.dated:
    print(day.strftime("%F"), "--", (day + timedelta(days=30)).strftime("%F"))
days = 'MTWTFSS'
daycal = '['
for _ in range(30):
    daycal += days[day.weekday()]
    if day.weekday() == 6:
        daycal += ' '
    day += shift
daycal += ']'
print(daycal)
