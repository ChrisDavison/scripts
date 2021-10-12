#!/usr/bin/env python3
from datetime import date, timedelta

today = date.today()
if today.weekday() > 0:
    today -= timedelta(days=today.weekday())

print(today.strftime("%Y-%m-%d"))
