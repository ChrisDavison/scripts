#!/usr/bin/env python3
import os
import json
import sys
from argparse import ArgumentParser

glossary_path = os.path.expanduser("~/.glossary.json")
glossary = json.load(open(glossary_path))


parser = ArgumentParser()
parser.add_argument("alias", type=str)
parser.add_argument("target", type=str)
args = parser.parse_args()

word = args.target
alias = args.alias

if word in glossary:
    glossary[alias] = {
        'alias': word
    }
else:
    print(word, "NOT IN GLOSSARY")

with open(glossary_path, 'w') as f:
    print(json.dumps(glossary, indent=2), file=f)
