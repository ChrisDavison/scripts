#!/usr/bin/env python3
"""
Prettyprint symlinks in the current directory.

Basically, 'ls -lah | grep "\->"', with some formatting.
"""
from pathlib import Path
from typing import List, Tuple
from collections import namedtuple


def get_links(root: Path) -> Tuple[List[Path], List[Path]]:
    """
    Get symlinks under root.
    """
    links_to_files = [p for p in Path(root).glob('*') if p.is_symlink() and p.is_file()]
    links_to_dirs = [p for p in Path(root).glob('*') if p.is_symlink() and p.is_dir()]

    return sorted(links_to_files), sorted(links_to_dirs)


def display_links(links: List[Path], preface: str):
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
    width = max([len(str(l.name)) for l in links])
    home = Path('~').expanduser()

    for link in links:
        actual = link.resolve()
        home_flag = ''
        if str(home) in str(actual):
            home_flag = '~/'
            actual = actual.relative_to(home)
        print(f"{str(link):{width}}  >  {home_flag}{actual}")


def main():
    """
    Print symlinks and the resolved target in a prettier layout.
    """
    links_f, links_d = get_links('.')
    display_links(links_f, "Files")
    print()
    display_links(links_d, "Directories")


if __name__ == "__main__":
    main()
