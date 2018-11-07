#!/usr/bin/env python3
import os.path
from pathlib import Path
import random
import re
import sys
import textwrap


FILENAME=os.path.expanduser('~/.quotes')
p = Path(FILENAME)
if not p.exists():
    print("No file: ~/.quotes")
    sys.exit(1)
contents = p.read_text().splitlines()
quotes = [l for l in contents if not l.startswith('---')]

quote = random.choice(quotes)
author = ""
if ' -- ' in quote:
    quote, author = quote.split(' -- ')

border = '+%s+\n| %-60s |' % (('-'*62), '')

print(border)
for line in textwrap.wrap(quote, 60):
    print('| %-60s |' % line)
if author:
    print('| %-60s |' % ('-- ' + author))
print(border[::-1])

