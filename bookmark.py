#!/usr/bin/env python3
from datetime import date
import sys

import requests
from bs4 import BeautifulSoup

r = requests.get(sys.argv[1])
title = BeautifulSoup(r.text, 'html.parser').title.string 
today = date.today().strftime("%F")
tags = ["@"+t for t in input("Tags: ")]
if not tags:
    tags = "@unread"
title_fn = "-".join(input("Title: ")) + ".txt"
template = f"""title: {title}
date: {today}
url: {sys.argv[1]}

{tags}
"""

with open(title, 'w') as f:
    f.write(template)

