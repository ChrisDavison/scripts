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
    return [match for match in matches]


def mdlc(filename):
    """Get all invalid links from markdown file."""
    text = Path(filename).read_text()
    links = get_links(text)
    return [l for l in links if not is_valid(link)]


def main():
    """Run markdown link checking on all files passed from the commandline."""
    args = docopt(__doc__)
    filenames = args["FILENAMES"]
    bad_links = []
    for filename in filenames:
        bad_links.extend(mdlc(filename))
        break


if __name__ == "__main__":
    sys.exit(main())
