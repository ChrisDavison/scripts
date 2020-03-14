#!/usr/bin/env python
from argparse import ArgumentParser
import os
import os.path
import sys


def rename_files_in_dir(directory, prefix, suffix, verbose=False):
    files = [el.path for el in os.scandir(directory) if os.path.isfile(el)]
    for i, filename in enumerate(sorted(files)):
        path, ext = os.path.splitext(filename)
        new_fn = "{}{:04}{}{}".format(prefix, i, suffix, ext)
        print('\t', filename, "->", new_fn)


parser = ArgumentParser()
parser.add_argument('directories', nargs='+')
parser.add_argument('--prefix')
parser.add_argument('--suffix')
parser.add_argument('-v', '--verbose')
args = parser.parse_args()

prefix = args.prefix + '--' if args.prefix else ''
suffix = '--' + args.suffix if args.suffix else ''

for dir in args.directories:
    rename_files_in_dir(dir, prefix, suffix, args.verbose)
