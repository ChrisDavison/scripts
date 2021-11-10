#!/usr/bin/env python3
import os
import json
import sys
from argparse import ArgumentParser


parser = ArgumentParser()
parser.add_argument("word", type=str, nargs='*')
parser.add_argument("--words", action='store_true')
parser.add_argument("--all", action='store_true')
parser.add_argument("--full", action='store_true')
args = parser.parse_args()


glossary_path = os.path.expanduser("~/.glossary.json")
glossary = json.load(open(glossary_path))
word = ' '.join(args.word)

def print_entry(word, glossary, full=False):
    entry = glossary[word]
    if 'alias' in entry:
        if full:
            print(word, ">>>", end=' ')
            print_entry(entry['alias'], glossary)
        else:
            print(word, 'is alias of', entry['alias'])
        return
    tags = ' '.join(entry['tags'])
    print('{} [{}]'.format(word, tags))
    print("-", entry['definition'])


def case_insensitive_matching_key(word, glossary):
    if word in glossary:
        return word
    if word.upper() in glossary:
        return word.upper()
    if word.lower() in glossary:
        return word.lower()
    return None


if args.all:
    for word in glossary.keys():
        entry = glossary[word]
        print_entry(word, glossary, args.full)
        print()
elif args.words:
    print('\n'.join(sorted(glossary.keys())))
elif case_insensitive_matching_key(word, glossary):
    matching = case_insensitive_matching_key(word, glossary)
    print_entry(matching, glossary, True)
else:
    print(word, "NOT IN GLOSSARY")

