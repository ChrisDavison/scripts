#!/usr/bin/env python3
"""
Filter files based on tags, contents, and filenames.

The 'content' search will be split based on whether the word begins with '@'.
If so, the '@' will be put through a tag search, rather than through a full-file text search.
A tag is defined as '@' followed by ALPHANUMERIC or '-'.
"""
from subprocess import run
from pathlib import Path
from typing import List, Set
from argparse import ArgumentParser
from dataclasses import dataclass
import re


@dataclass
class Filter:
    """
    A filter over files' name, contents, or file tags.

    A 'tag' is something that matches the regex '@[a-zA-Z0-9\-]+'.
    """
    name: Set[str]
    contents: Set[str]
    tags: Set[str]

    def matches(self, path: Path) -> bool:
        """Does a path match the filter."""
        words_in_name = set(re.split(r"\b", str(path).lower()))
        file_contents = path.read_text().lower()
        words_in_file = set(file_contents.split())
        tags = set(tags_in_file(path))
        matches_name = self.name.issubset(words_in_name)
        matches_contents = self.contents.issubset(words_in_file)
        matches_tags = self.tags.issubset(tags)
        return all([matches_name, matches_contents, matches_tags])


def tags_in_file(path: Path) -> List[str]:
    """Return all tags in a file."""
    matches = re.findall(r'@([a-zA-Z1-9\-]+)', path.read_text())
    return matches


def print_available_tags():
    """Print tags existing under the current directory."""
    print('AVAILABLE TAGS')
    print('==============')
    output = run(['tagsearch', '-l'], check=True, capture_output=True).stdout
    print(output.decode())


def print_untagged_files(only_filename):
    """Print files that aren't tagged."""
    if not only_filename:
        print('UNTAGGED FILES')
        print('==============')
    output = run(['tagsearch', '-u'], check=True, capture_output=True).stdout
    print(output.decode())


def print_matching_files(name_query, contents_query, tags_query, only_filename):
    """Print files recursively under the current dir that match queries."""
    files = list(Path('.').rglob('*.md'))
    file_filter = Filter(name=set(w.lower() for w in name_query),
                         contents=set(c.lower() for c in contents_query),
                         tags=set(t.lower() for t in tags_query))
    to_print = []
    for file in files:
        if file_filter.matches(file):
            tags = tags_in_file(file)
            if only_filename:
                to_print.append([file, ""])
            else:
                if len(tags) > 5:
                    tags = ["MANY", "TAGS"]
                to_print.append([file, " ".join(tags)])
    longest_filename = max([len(str(file)) for file, tags in to_print])
    for file, tags in to_print:
        if tags:
            tags = f"({tags})"
        print(f"{str(file).ljust(longest_filename)}  {tags}")


if __name__ == "__main__":
    parser = ArgumentParser(description="Filter files based on tags, contents, and filename")
    parser.add_argument('-n', metavar='WORD',
                        help='Words to match in FILENAME',
                        nargs='+', default=[])
    parser.add_argument('WORD',
                        help='Words and tags to match in FILE CONTENTS',
                        nargs='*', default=[])
    parser.add_argument('-l',
                        help='List all tags under current dir',
                        action='store_true')
    parser.add_argument('-f',
                        help='Only print filename after filtering',
                        action='store_true')
    parser.add_argument('-u',
                        help='Print files with no tags',
                        action='store_true')
    args = parser.parse_args()
    if args.l:
        print_available_tags()
    elif args.u:
        print_untagged_files(args.f)
    else:
        tags = [w[1:] for w in args.WORD if w.startswith('@')]
        words = [w for w in args.WORD if not w.startswith('@')]
        print_matching_files(args.n, words, tags, args.f)
