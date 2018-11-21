#!/usr/bin/env python
"""Sanitise filenames."""
import argparse
import re
import shutil
from pathlib import Path


def sanitise(text):
    """Sanitise some text by removing most non-alphanumeric characters."""
    lowercase = lambda x: x.lower()
    replace_non_alnum_dotdash_with_dash = lambda x: re.sub(r"[^a-z0-9.-]", "-", x)
    reduce_consecutive_dashes = lambda x: re.sub("-+", "-", x)
    return reduce_consecutive_dashes(replace_non_alnum_dotdash_with_dash(lowercase(text)))


if __name__ == "__main__":
    parser = argparse.ArgumentParser("sanitise")
    parser.add_argument("text", nargs="+")
    parser.add_argument('--move', required=False, action='store_true')
    args = parser.parse_args()
    filepath = Path(" ".join(args.text))
    sanitised_filepath = filepath.parent / sanitise(filepath.name)
    if args.move:
        shutil.move(filepath, sanitised_filepath)
    print(sanitised_filepath)
