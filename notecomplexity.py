#!/usr/bin/env python
from argparse import ArgumentParser
from pathlib import Path


def note_complexity(notepath, symbol):
    contents = notepath.read_bytes().split(b'\n')
    complexity = 0
    for line in contents:
        first_word = line.split(b' ')[0]
        chars_in_first_word = list(set(first_word))
        if list(chars_in_first_word) == [ord(symbol)]:
            complexity += len(first_word)
    return complexity


def main():
    parser = ArgumentParser()
    parser.add_argument('path')
    parser.add_argument('-f', '--format', default='md')
    args = parser.parse_args()

    notes = Path(args.path).rglob(f'*.{args.format}')
    symbol = {'md': '#', 'org': '*'}[args.format]
    notes_and_complexity = sorted([(note_complexity(n, symbol), n) for n in notes], reverse=True)
    for note in notes_and_complexity:
        if note[0]:
            print(f"{note[0]:4d}\t{(Path(args.path) / note[1]).resolve()}")


if __name__ == "__main__":
    main()
