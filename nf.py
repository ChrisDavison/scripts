#!/usr/bin/env python3
"""
Filter files based on tags, contents, and filenames.

...where a tag is defined as `@[a-zA-Z1-9\-]`, basically.
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
        tags = tags_in_file(path)
        matches_name = self.name.issubset(words_in_name)
        matches_contents = self.contents.issubset(words_in_file)
        matches_tags = self.tags.issubset(tags)
        return all([matches_name, matches_contents, matches_tags])


def tags_in_file(path: Path) -> List[str]:
    """Return all tags in a file."""
    return [t[1:] for t in re.findall(r'@[a-zA-Z1-9\-]+', path.read_text())]


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
    for file in files:
        if file_filter.matches(file):
            tags = tags_in_file(file)
            print(file)
            if not only_filename and tags:
                print(f"tags: {' '.join(tags)}")
                print()


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('-n', '--name', nargs='+', default=[])
    parser.add_argument('-c', '--contents', nargs='+', default=[])
    parser.add_argument('-t', '--tags', nargs='+', default=[])
    parser.add_argument('-l', '--list-tags', action='store_true')
    parser.add_argument('-o', '--only-print-filename', action='store_true')
    parser.add_argument('-u', '--untagged-files', action='store_true')
    args = parser.parse_args()
    if args.list_tags:
        print_available_tags()
    elif args.untagged_files:
        print_untagged_files(args.only_print_filename)
    else:
        print_matching_files(args.name,
                             args.contents,
                             args.tags,
                             args.only_print_filename)
