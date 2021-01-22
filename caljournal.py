#!/usr/bin/env python3
import datetime
from argparse import ArgumentParser
from cal import month_cal
from thirtyday import thirtyday


def make_journal(year: int, month: int, ticker: bool):
    """Create a calendar journal page."""
    today = datetime.date.today()
    year = int(year) if year else today.year
    month = int(month) if month else today.month
    today = today.replace(year=year, month=month, day=1)
    print(datetime.date(year, month, 1).strftime("# %Y-%m %B\n"))
    print('\n'.join(month_cal(year, month, indented=True)))

    if ticker:
        print('\n## Ticker\n')
        thirtyday_str = thirtyday(start=today, title=None, dated=True)
        for line in thirtyday_str.splitlines():
            print('    ' + line)

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
    p.add_argument("-y", "--year",
                   default=datetime.date.today().year)
    p.add_argument("-m", "--month",
                   default=datetime.date.today().month)
    p.add_argument("-t", "--ticker",
                   help="With ticker?",
                   action="store_true")
    args = p.parse_args()
    make_journal(args.year, args.month, args.ticker)
