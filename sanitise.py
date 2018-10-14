#!/usr/bin/env python
"""Sanitise filenames."""
import argparse
import re


def sanitise(text, keepcharacters=" ._-"):
    """Sanitise some text by removing most non-alphanumeric characters."""
    fn_out = ""
    for letter in text.replace(" ", "-"):
        if letter.isalnum() or letter in keepcharacters:
            fn_out += letter
        else:
            fn_out += "-"
    return re.sub("-+", "-", fn_out)


if __name__ == "__main__":
    parser = argparse.ArgumentParser("sanitise")
    parser.add_argument("text", nargs="+")
    args = parser.parse_args()
    print(sanitise(" ".join(args.text)))
