#!/usr/bin/env python3
"""
Prettyprint symlinks in the current directory.

Basically, 'ls -lah | grep "\->"', with some formatting.
"""
from pathlib import Path
from typing import List


def print_links_relative_to_home(links: List[Path]):
    """
    Prettyprint symlinks, and replace home dir with '~'.
    """
    home = Path('~').expanduser()
    width = max([len(str(l)) for l in links])
    for link in links:
        actual = link.resolve()
        home_flag = ''
        if str(home) in str(actual):
            home_flag = '~/'
            actual = actual.relative_to(home)
        print(f"{str(link):{width}}  |  {home_flag}{actual}")


def main():
    """
    Print symlinks and the resolved target in a prettier layout.
    """
    # Sort symlinks by dir-first, then alphabetically
    # NOTE: dotfiles come first alphabetically
    links = sorted([p for p in Path('.').glob('*') if p.is_symlink()], key=lambda p: (p.is_file(), p))

    if not links:
        print("No symlinks.")
        return
    width = max([len(str(l)) for l in links])
    home = Path('~').expanduser()

    for link in links:
        actual = link.resolve()
        home_flag = ''
        if str(home) in str(actual):
            home_flag = '~/'
            actual = actual.relative_to(home)
        type = 'F' if link.is_file() else 'D'
        print(f"{type} | {str(link):{width}} | {home_flag}{actual}")


if __name__ == "__main__":
    main()
