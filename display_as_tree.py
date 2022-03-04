#!/usr/bin/env python
import sys
from pathlib import Path
from argparse import ArgumentParser


child_char = "├"
last_child_char = "└"

def parse_heirarchy(line, *, delim):
    return line.split(delim)

def display_as_tree(heirarchies, assume_sorted=False):
    if not assume_sorted:
        heirarchies.sort()
    path = []
    output = []
    for heirarchy in heirarchies:
        for (i, word) in enumerate(heirarchy):
            part_at_same_depth = path[i] if len(path) > i else None
            if part_at_same_depth:
                if part_at_same_depth == word:
                    continue
                while len(path) > i:
                    path.pop()
                path.append(word)
            else:
                path.append(word)

            indent = "    " * (len(path) - 1)
            stem = path[-1]
            line = f"{indent}{stem}"
            print(line)
            output.append((len(path), stem))
    return output

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('FILE', type=Path, nargs='?')
    parser.add_argument('-a', '--assume-sorted', required=False, action='store_true')
    parser.add_argument('-d', '--delimiter', required=False, type=str, default='/')
    args = parser.parse_args()

    if args.FILE:
        lines = FILE.read_text().splitlines()
    else:
        lines = []
        for line in sys.stdin:
            lines.append(line.strip())
    heirarchy=[parse_heirarchy(line, delim=args.delimiter) for line in lines]
    output = display_as_tree(heirarchy, args.assume_sorted)

    # for (pathlen, name), (pathlen2, _) in zip(output, output[1:]):
    #     if pathlen == 1:
    #         print(child_char, name)
    #     elif pathlen2 > pathlen:
    #         print("| ", "  " * (pathlen-2), last_child_char, name)
    #     elif pathlen2 == pathlen:
    #         print("| ", "  " * (pathlen-2), child_char, name)
    #     else:
    #         print("| ", "  " * (pathlen-2), last_child_char, name)

