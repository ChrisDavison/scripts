#!/usr/bin/env python3
import datetime
from typing import List, Iterator
from argparse import ArgumentParser
import textwrap


WEEK = List[datetime.date]


def justified_week_line(week: WEEK, weekdays_only: bool, justification: int) -> str:
    """Justify the days in the current week, calendar style."""
    days = [w.strftime("%2d") for w in week
            if not weekdays_only
            or (weekdays_only and w.weekday() < 5)]
    return " ".join(days).rjust(justification)


def day_iter(start, end=None) -> Iterator[datetime.date]:
    """Iterate a day at a time.

    If end is provided, stop without yielding end."""
    while True:
        yield start
        start += datetime.timedelta(days=1)
        if end and start >= end:
            break


def next_month(now: datetime.date) -> datetime.date:
    """Get the month after this one."""
    if now.month == 12:
        return now.replace(year=now.year+1, month=1)
    return now.replace(month=now.month+1)


def cal(year: int, month: int, *,
        indented: bool = False,
        weekdays_only: bool = False) -> List[str]:
    """Generate a calendar."""
    start = datetime.date(year, month, 1)
    weeks: List[WEEK] = [[]]
    week: WEEK = []
    for day in day_iter(start, next_month(start)):
        weeks[len(weeks)-1].append(day)
        if day.weekday() == 6:
            weeks.append([])

    headers = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]
    if weekdays_only:
        headers = headers[:-2]

    justification = len(headers) * 2 + len(headers) - 1
    out = [
        start.strftime("%B %Y").center(justification),
        " ".join(headers)
    ]
    for week in weeks:
        out.append(justified_week_line(week, weekdays_only, justification))
    if indented:
        return textwrap.indent('\n'.join(out), prefix='    ').splitlines()
    return out


if __name__ == "__main__":
    p = ArgumentParser()
    p.add_argument("-y", "--year",
                   default=datetime.date.today().year, type=int)
    p.add_argument("-m", "--month",
                   default=datetime.date.today().month, type=int)
    p.add_argument("-Y", "--full-year",
                   help="Generate calendar for every month",
                   action='store_true')
    p.add_argument("-w", "--weekdays-only",
                   help="Only show weekdays",
                   action='store_true')

    args = p.parse_args()
    months = list(range(1, 13)) if args.full_year else [args.month]
    calendars = [
        '\n'.join(cal(args.year, month, weekdays_only=args.weekdays_only))
        for month in months
    ]
    print('\n\n'.join(calendars))
