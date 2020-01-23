#!/usr/bin/env python3
from datetime import date
from os.path import expanduser
import sys

import requests
from bs4 import BeautifulSoup

r = requests.get(sys.argv[1])
title = BeautifulSoup(r.text, 'html.parser').title.string 
today = date.today().strftime("%F")
tags = ' '.join(["@"+t for t in input("Tags: ").split(' ')])
if not tags:
    tags = "@unread"
template = f"""title: {title}
date: {today}
url: {sys.argv[1]}

{tags}
"""
title_fn = "-".join(input("Title (filename): ").split(" ")) + ".txt"
title_fn_full = expanduser(f"~/Dropbox/bookmarks/{title_fn.lower()}")

print(title_fn_full)

with open(title_fn_full, 'w') as f:
    f.write(template)

