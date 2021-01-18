#!/usr/bin/env python3
import datetime
from argparse import ArgumentParser


def month_cal(year, month, *, indented=False, weekdays_only=False):
    start = datetime.date(year, month, 1)
    by_weekday, week, temp = [], [], start
    while temp.month == start.month:
        if temp.weekday() == 0 and week:
            by_weekday.append(week)
            week = []
        if not weekdays_only:
            week.append(temp)
        elif temp.weekday() not in [5, 6]:
            week.append(temp)
        else:
            # Weekdays only and today is sat or sun
            pass
        temp += datetime.timedelta(days=1)
    if week:
        by_weekday.append(week)

    leading = '    ' if indented else ''
    headers = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]
    if weekdays_only:
        headers = ["Mo", "Tu", "We", "Th", "Fr"]
    headerstr = " ".join(headers)
    just = 20 if not weekdays_only else 14
    out = []
    out.append(leading + start.strftime("%B %Y").center(just))
    out.append(leading + headerstr)
    for i, week in enumerate(by_weekday):
        aligned_week = [str(w.day).rjust(2) for w in week]
        w = " ".join(aligned_week)
        justified = w.ljust(just) if i else w.rjust(just)
        out.append(leading + justified)
    return out


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


def main(year, month, full_year, weekdays_only):
    if args.full_year:
        divider = "\n" + "-" * 80 + "\n\n"
        calendars = ['\n'.join(month_cal(year, month))
                     for month in range(1, 13)]
        print(divider.join(calendars))
    else:
        print('\n'.join(month_cal(year, month, weekdays_only=weekdays_only)))


if __name__ == "__main__":
    p = ArgumentParser()
    p.add_argument("-y", "--year",
                   default=datetime.date.today().year)
    p.add_argument("-m", "--month",
                   default=datetime.date.today().month)
    p.add_argument("-Y", "--full-year",
                   help="Generate calendar for every month",
                   action='store_true',)
    p.add_argument("-w", "--weekdays",
                   help="Only show weekdays", action='store_true')
    args = p.parse_args()
    main(args.year, args.month, args.full_year, args.weekdays)
