#!/usr/bin/env python3
"""Markdown link checker"""
import re
import sys
from argparse import ArgumentParser
from pathlib import Path

import requests


VERBOSE = False
RE_REFLINK = re.compile(r"\[.+?\]: (.+)(?:\s|$)")
RE_INLINELINK = re.compile(r"\[.+?\]\((.+?)\)")
RE_MDANCHOR = re.compile("#.*")


def is_valid(url, relative_to):
    """Check if a url is valid (either local or web)."""
    return is_valid_local(url, relative_to) or is_valid_web(url)


def trim_md_anchor(url):
    """Remove any #text from a url."""
    return RE_MDANCHOR.sub("", url)


def is_valid_local(url, relative_to):
    """Check if a url references a local file."""
    no_anchor = trim_md_anchor(url)
    p = (Path(relative_to).parent / no_anchor).resolve()
    return p.exists()


def is_valid_web(url):
    """Check if a url returns a valid status code."""
    valid_statuses = [200, 202, 301, 307, 308]
    if not (url.startswith("http://") or url.startswith("https://")):
        url = f"https://{url}"
    try:
        r = requests.get(url)
        return r.status_code in valid_statuses
    except:
        return False


def get_links(text):
    """Get all links from with in a text as a list of URLs."""
    matches = RE_INLINELINK.findall(text)
    matches2 = RE_REFLINK.findall(text)
    matches.extend(matches2)
    return matches


def get_links_from_file(filename):
    """Get all links from markdown file."""
    if VERBOSE:
        print(filename)
    try:
        text = Path(filename).read_text()
        return get_links(text)
    except Exception as E:
        print(E, filename)
        return []


def mdlc(filename):
    """Get all invalid links from markdown file."""
    links = get_links_from_file(filename)
    return [l for l in links if not is_valid(l, relative_to=filename)]


def main():
    """Run markdown link checking on all files passed from the commandline."""
    p = ArgumentParser(prog="mdlc")
    p.add_argument("-v", "--verbose", action="store_true")
    p.add_argument("FILENAMES", nargs="+")
    args = p.parse_args()
    VERBOSE = args.verbose
    bad_links = {filename: mdlc(filename) for filename in args.FILENAMES}
    for filename, badlinks in bad_links.items():
        if badlinks:
            print(filename)
            for link in badlinks:
                print("\t", link)


if __name__ == "__main__":
    sys.exit(main())
