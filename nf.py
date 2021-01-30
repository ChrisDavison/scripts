#!/usr/bin/env python3
from subprocess import run
from pathlib import Path
from typing import List, Set
from argparse import ArgumentParser
import re

re_tag = re.compile(r'@[a-zA-Z1-9\-]+')


def matches_all_words(*, ls: List[str], query: List[str]) -> bool:
    if not query:
        return True
    query = [q.lower() for q in query]
    words = set(w.lower() for w in ls)
    return set(query).issubset(words)


def print_if_matches(*, filename, name_query, contents_query, tags_query):
    file_str = f"file: {filename}"
    tags_query = [t if not t.startswith('@') else t[1:] for t in tags_query]
    words_in_name = re.split(r"\b", str(filename).lower())
    file_contents = filename.read_text()
    words_in_file = file_contents.split()
    tags_in_file = [t[1:] for t in re_tag.findall(file_contents)]
    tag_str = f"tags_query: {' '.join(tags_in_file)}"
    if matches_all_words(ls=words_in_name, query=name_query) and \
       matches_all_words(ls=words_in_file, query=contents_query) and \
       matches_all_words(ls=tags_in_file, query=tags_query):
        print(file_str)
        if tags_in_file:
            print(tag_str)
        print()


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('-n', '--name', nargs='+', default=[])
    parser.add_argument('-c', '--contents', nargs='+', default=[])
    parser.add_argument('-t', '--tags', nargs='+', default=[])
    args = parser.parse_args()
    files = list(Path('.').rglob('*.md'))
    for file in files:
        print_if_matches(filename=file,
                         name_query=args.name,
                         contents_query=args.contents,
                         tags_query=args.tags)


