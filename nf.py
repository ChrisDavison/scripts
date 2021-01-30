#!/usr/bin/env python3
from subprocess import run
from pathlib import Path
from typing import List, Set
from argparse import ArgumentParser
import re

re_tag = re.compile(r'@[a-zA-Z1-9\-]+')


def print_if_matches(*, filename, name_query=[], contents_query=[], tags_query=[]):
    # Tidy up the queries (make them lowercase sets)
    tags_query = [t if not t.startswith('@') else t[1:] for t in tags_query]
    tags_query = set(t.lower() for t in tags_query)
    contents_query = set(c.lower() for c in contents_query)
    name_query = set(n.lower() for n in name_query)
    # ===================
    file_str = f"file: {filename}"
    words_in_name = set(re.split(r"\b", str(filename).lower()))
    file_contents = filename.read_text().lower()
    words_in_file = set(file_contents.split())
    tags_in_file = set(t[1:] for t in re_tag.findall(file_contents))
    tag_str = f"tags_query: {' '.join(tags_in_file)}"
    if name_query.issubset(words_in_name) and \
       contents_query.issubset(words_in_file) and \
       tags_query.issubset(tags_in_file):
        print(file_str)
        if tags_in_file:
            print(tag_str)
        print()


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('-n', '--name', nargs='+', default=[])
    parser.add_argument('-c', '--contents', nargs='+', default=[])
    parser.add_argument('-t', '--tags', nargs='+', default=[])
    parser.add_argument('-l', '--list-tags', action='store_true')
    parser.add_argument('-u', '--untagged-files', action='store_true')
    args = parser.parse_args()
    if args.list_tags:
        # print('AVAILABLE TAGS')
        # print('==============')
        print(run(['tagsearch', '-l'], capture_output=True).stdout.decode())
    elif args.untagged_files:
        # print('UNTAGGED FILES')
        # print('==============')
        print(run(['tagsearch', '-u'], capture_output=True).stdout.decode())
    else:
        files = list(Path('.').rglob('*.md'))
        for file in files:
            print_if_matches(filename=file,
                             name_query=args.name,
                             contents_query=args.contents,
                             tags_query=args.tags)


