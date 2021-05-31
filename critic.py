#!/usr/bin/env python3
"""Critique writing"""
import os.path as op
import sys
from pathlib import Path
from typing import List, Optional


def word_check(line, word_list, word_type) -> Optional[str]:
    """Check a line for instances of 'bad' words"""
    for word in word_list:
        if word in line:
            return "{}: {}".format(word_type, word)
    return None


def main(filename):
    script_path = Path(op.dirname(op.realpath(__file__))).resolve()
    word_path = script_path / "words"
    words_weasels = (word_path / "bw-weasel.txt").read_text().splitlines()
    words_passive = (word_path / "bw-passive.txt").read_text().splitlines()
    with open(filename, "r") as f:
        for i, line in enumerate(f):
            weasel = word_check(line, words_weasels, "Weasel")
            passive = word_check(line, words_passive, "Passive")
            if weasel:
                print(f"{i}: {weasel}".format(i, weasel))
            if passive:
                print(f"{i}: {passive}".format(i, passive))


if __name__ == "__main__":
    main(sys.argv[1])
