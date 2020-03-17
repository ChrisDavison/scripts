#!/usr/bin/env python3
from datetime import date, timedelta

today = date.today()
year_end = date(year=today.year + 1, month=1, day=1) - timedelta(days=1)
year_start = date(year=today.year, month=1, day=1)
days_in_year = (year_end - year_start).days
days_through_year = (today - year_start).days
print("{} days ({:.1f}%)".format(days_through_year, days_through_year / days_in_year * 100))
