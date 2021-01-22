#!/usr/bin/env python3
"""Capture a literature entry"""
import pyperclip
from doi2bib import crossref
from typing import Iterator


FORMAT = """## {title}

Authors: {authors}

```bibtex
{bibtex}
```
"""


def get_authors() -> str:
    """Ask for an author until nothing is entered."""
    authors = []
    while True:
        author = input("Author: ")
        if not author:
            break
        authors.append(author.title())
    return ' and '.join(authors)


def make_literature_entry():
    """Read a literature entry, with bibtex."""
    title = input("Title: ")
    authors = get_authors()
    found, bibtex = crossref.get_bib(input("DOI: "))
    print('-'*40)
    msg = FORMAT.format(title=title, authors=authors, bibtex=bibtex)
    print(msg)
    pyperclip.copy(msg)
    print('-'*40)
    print('...copied entry to clipboard.')
    print('-'*40)
    print('Hit <Enter> to copy filename to clipboard')
    filename = title.lower().replace(' ', '-') + ".pdf"
    print('Filename:', filename)
    input()
    pyperclip.copy(filename)
    print('...copied filename to clipboard')


if __name__ == "__main__":
    make_literature_entry()
