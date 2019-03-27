#!/usr/bin/env python3
"""usage: mdlc FILENAMES..."""
import os
import re
import sys
from pathlib import Path

import requests
from docopt import docopt


RE_REFLINK = re.compile(r"\[.+?\]: (.+)(?:\s|$)")
RE_INLINELINK = re.compile(r"\[.+?\]\((.+?)\)")
RE_MDANCHOR = re.compile("#.*")


def check_link(url):
    return is_valid_local(url) or is_valid_web(url)


def is_valid_local(url):
    p = Path(url).resolve()
    return p.exists()


def is_valid_web(url):
    valid_statuses = [200, 202, 301, 307, 308]
    r = requests.get(url)
    return r.status_code in valid_statuses

def get_links(text):
    matches = RE_INLINELINK.findall(text)
    matches2 = RE_REFLINK.findall(text)
    matches.extend(matches2)
    return [match for group in matches for match in group if match]

def main():
    args = docopt(__doc__)
    filenames = args['FILENAMES']
    for filename in filenames:
        matches = RE_REFLINK.findall(open(filename).read())
        if matches:
            print(matches)


if __name__ == "__main__":
    sys.exit(main())
