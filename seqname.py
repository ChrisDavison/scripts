#!/usr/bin/env python
"""Rename a sequence of files"""
from argparse import ArgumentParser
from pathlib import Path
from shutil import move


p = ArgumentParser(prog="seqname")
p.add_argument("--version", action='version', version='%(prog)s 0.1.0')
p.add_argument("DIR", help="Directory containing files")
p.add_argument("-p", "--prefix", default='', help="Prefix to insert before number")
p.add_argument("-s", "--suffix", default='', help="Suffix to insert after number")
args = p.parse_args()

pref = '' if not args.prefix else f'{args.prefix}--'
suff = '' if not args.suffix else f'--{args.suffix}'

for i, p in enumerate(Path(args.DIR).glob('*')):
    new = p.parent / f"{pref}{i:02d}{suff}{p.suffix}"
    move(p, new)
