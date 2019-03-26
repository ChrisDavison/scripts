#!/usr/bin/env python3
import os
import re
import sys
from datetime import date, timedelta
from pathlib import Path


def main(days=1):
    TODAY = date.today()
    YESTERDAY = TODAY - timedelta(days=days)
    LOGBOOK = Path(f'~/Dropbox/notes/logbook/{TODAY.strftime("%Y-%m")}.md')

    path = LOGBOOK.expanduser()
    if not path.exists():
        print("No logbook for this month yet")

    entries = []
    temp = []

    content = path.read_text().splitlines()
    for line in content:
        if line.startswith('-'):
            if temp:
                entries.append(temp)
            temp = [line.strip()]
        elif not line:
            if temp:
                entries.append(temp)
            entries.append([])
            temp = []
        else:
            temp.append(line.strip())
    if temp:
        entries.append(temp)

    for group in entries:
        reflinks = [l for l in group if ']: ' in l]
        if reflinks:
            print('\n'.join(['  '+r for r in reflinks]))
        else:
            print(' '.join(group))


if __name__ == "__main__":
    days = 1
    if len(sys.argv) > 1:
        days = int(sys.argv[1])
    main(days)
