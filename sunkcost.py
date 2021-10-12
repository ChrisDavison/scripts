#!/usr/bin/env python3
import datetime
import sys

args = sys.argv[1:]
if len(args) < 2:
    print("usage: sunkcost <cost> <start_date>")
    sys.exit()

cost = float(args[0])

yyyy, mm, dd = args[1].split("-")
startdate = datetime.date(int(yyyy), int(mm), int(dd))
enddate = startdate + datetime.timedelta(days=365)
now = datetime.date.today()

elapsed = (now - startdate).days
proportion = elapsed / 365
proportion_cost = proportion * cost
proportion_left = (1 - proportion) * cost
print(
    f"Subscription: £{proportion_cost:.2f} of £{cost:.2f} -- £{proportion_left:.2f} ({(1 - proportion) * 100:.0f}%) remaining")
