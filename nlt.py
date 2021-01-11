#!/usr/bin/env python3
"""
NLT - natural language times

Given a string, return the best-guess datetime that represents this.

Supports:
    today
    tomorrow
    [next] monday|tuesday|wednesday|thursday|friday|saturday|sunday
    [next] weekday|weekend
    [next] day|month|year
"""
import datetime
import sys
from argparse import ArgumentParser
from parsedatetime import Calendar


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('-f', '--format', type=str, default='%Y-%m-%d')
    parser.add_argument('when', nargs='+')
    args = parser.parse_args()
    t = datetime.datetime(*Calendar().parse(' '.join(args.when))[0][:6])
    print(t.strftime(args.format))
