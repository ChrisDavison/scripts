"""Critique writing"""
import sys
from pathlib import Path


def word_check(line, word_list, word_type):
    """Check a line for instances of 'bad' words"""
    non_empty_lines = [w for w in word_list if w != '']
    for word in non_empty_lines:
        if line.find(word):
            return "{}: {}".format(word_type, word)
    return ""


def main(filename):
    words_weasels = Path('../words/bw-weasel.txt').resolve().read_text()
    words_passive = Path('../words/bw-passive.txt').resolve().read_text()
    with open(filename, 'r') as f:
        for i, line in enumerate(f):
            print("{}: {}".format(i, word_check(line, words_weasels, "Weasel")))
            print("{}: {}".format(i, word_check(line, words_passive, "Passive")))


if __name__ == '__main__':
    main(sys.argv[1])