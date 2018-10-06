#!/usr/bin/env python3
import sys
import re


if __name__ == '__main__':
    fn = sys.argv[1]
    date1 = sys.argv[2]
    date2 = sys.argv[3]
    printing = False
    for line in open(fn, 'r'):
        if date1 in line:
            printing = True
        if printing:
            print(line)
