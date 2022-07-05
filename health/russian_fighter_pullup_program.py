#!/usr/bin/env python
from argparse import ArgumentParser
from itertools import groupby
import datetime
import sys


def rep_generator(max_pullups):
    pullups = [max_pullups, max_pullups-1, max_pullups-2, max_pullups-3, max_pullups-4]
    increments = [4, 3, 2, 1, 0]
    inc_counter = 0
    for day in range(1, 31):
        for pullup in pullups:
            yield (day, max(pullup,1))
        if day % 6 != 0:
            pullups[increments[inc_counter]] += 1
            inc_counter = (inc_counter + 1) % 5


def main(pushups, as_dates, offset=0):
    print(f"Russian Fighter Pullup Program")
    print(f"From {pushups} max reps")
    if offset:
        print(f"Starting in {offset} days")
    print()
    msg = "Date" if as_dates else "Day"
    reps = groupby(rep_generator(pushups), key=lambda x: x[0])
    total_reps = 0
    for day, data_for_day in reps:
        todays_reps = [r for _d, r in data_for_day]
        today_reps_string = ' '.join([str(r) for r in todays_reps])
        todays_total = sum(todays_reps)
        total_reps += sum(todays_reps)
        total_str = f"  ({todays_total} today)"
        if (day % 6) == 0:
            today_reps_string = "REST DAY"
            total_str = ""
        pre = f"Day {day:<2d}"
        if as_dates:
            date = datetime.date.today() + datetime.timedelta(days=day + offset)
            pre = str(date)
        print(f"{pre}  -  {today_reps_string:10}{total_str}")
    print(f"\n    TOTAL REPS {total_reps}")
    print(f"\n    MAX PUSHUPS TEST")
    
if __name__ == "__main__":
    parser = ArgumentParser("russian_fighter_pullup_program")
    parser.add_argument("max_pullups", type=int, nargs=1)
    parser.add_argument("-d", "--as-dates", help="Show specific dates", action="store_true")
    parser.add_argument("-o", "--offset", help="Number of days to offset. Assumes -d", type=int, default=0)
    args = parser.parse_args()

    main(int(sys.argv[1]), as_dates=args.as_dates, offset=args.offset)

    
