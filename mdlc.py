#!/usr/bin/env python3
"""usage: mdlc FILENAMES..."""
import os
import re
import sys
from pathlib import Path

import requests
from docopt import docopt


RE_MDLOCAL = re.compile(r"^.{1,2}/([a-zA-Z0-9-_])*[a-zA-Z0-9-_].md")
RE_MDWEB = re.compile(r"^(?:http(s)?://)?[\w.-]+(?:.[\w\.-]+)+[\w\-\._~:/?#\[\\]@!\$&'\(\)\*\+,;=.]+$")
RE_REFLINK = re.compile(r"\[.+?\]: (.*)")
RE_INLINELINK = re.compile(r"\[.+?\]\((.+?)\)|^\s*\[.+?\]: (.+)")


def check_link(url):
    pass


def is_valid_local(url):
    pass


def is_valid_web(url):
    valid_status = []
    r = requests.get(url)
    print(r.status_code in valid_status)


def main():
    args = docopt(__doc__)
    filenames = args['FILENAMES']
    for filename in filenames:
        matches = RE_LINK.findall(open(filename).read())
        if matches:
            print(matches)
        matches = RE_REFLINK.findall(open(filename).read())
        if matches:
            print(matches)
    # print(is_valid_web('https://httpstat.us/200'))


if __name__ == "__main__":
    sys.exit(main())
