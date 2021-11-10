#!/usr/bin/env python3
import os
import json
import sys
from argparse import ArgumentParser

glossary_path = os.path.expanduser("~/.glossary.json")
glossary = json.load(open(glossary_path))


parser = ArgumentParser()
parser.add_argument("word", type=str)
parser.add_argument("definition", type=str)
parser.add_argument("tags", nargs='+', type=str)
args = parser.parse_args()

word = args.word
definition = args.definition.replace('\n', ' ')
tags = args.tags

if word in glossary:
    print("{} ALREADY IN GLOSSARY".format(word), file=sys.stderr)
    print(word)
    print(glossary[word]['definition'])
    print(' '.join("@" + tag for tag in glossary[word]['tags']))
else:
    glossary[word] = {
        'definition': definition,
        'tags': tags
    }

with open(glossary_path, 'w') as f:
    print(json.dumps(glossary, indent=2), file=f)
