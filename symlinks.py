#!/usr/bin/env python3
"""
Prettyprint symlinks in the current (or specified) directory.

Basically, 'ls -lah | grep "\->"', with some formatting.
"""
from pathlib import Path
from typing import List, Tuple
from collections import namedtuple
from argparse import ArgumentParser


def get_links(root: Path) -> Tuple[List[Path], List[Path]]:
    """
    Get symlinks under root.
    """
    links_to_files = []
    links_to_dirs = []
    for p in Path(root).glob('*'):
        print(p)
        if 'refile' in str(p):
            print(p, p.is_symlink(), p.stat())
        if not p.is_symlink():
            continue
        if p.is_file():
            links_to_files.append(p)
        elif p.is_dir():
            links_to_dirs.append(p)
        else:
            print(p, 'is symlink, but not file or dir???')

    return sorted(links_to_files), sorted(links_to_dirs)


def display_links(links: List[Path], preface: str, width: int, trim_prefix: None):
    """
    Print a list of links, with a preface message/title.

    Links are resolved to ~ if they are a child of $HOME.
    """
    if not links:
        return
    to_fit = 60
    remain = to_fit - (len(preface) + 2)
    n_either_side = int(remain / 2)
    spacer = "-" * n_either_side
    print(spacer, preface.upper(), spacer)

    for link in links:
        actual = link.resolve()
        linkstr = str(link)
        actualstr = str(actual)
        if trim_prefix:
            linkstr = str(trim_prefix(link))
            try:
                actualstr = str(trim_prefix(actual))
            except:
                actualstr = str(actual)
        print(f"{linkstr:{width + 5}}{actualstr}")


def main(directory, trim_prefix):
    """
    Print symlinks and the resolved target in a prettier layout.
    """
    links_f, links_d = get_links(directory)
    longest = max(len(str(f)) for l in [links_f, links_d] for f in l)
    if trim_prefix:
        trim_prefix = lambda x: x.relative_to(directory)
    display_links(links_f, "Files", longest, trim_prefix)
    print()
    display_links(links_d, "Directories", longest, trim_prefix)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("directory", nargs='?', default=".")
    parser.add_argument("--trim-prefix", action='store_true')
    args = parser.parse_args()
    main(args.directory, args.trim_prefix)
