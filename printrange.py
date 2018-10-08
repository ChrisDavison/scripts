#!/usr/bin/env python3
import sys
import re
import argparse


class LinePrinter:
    """LinePrinter will print a limited range of CSV lines.

    Options are --after and --before, and can be paired to get 'between'
    LinePrinter uses a builder pattern, to incrementally build the instance
    and avoid confusion of function parameter order.
    """
    def __init__(self):
        self.start, self.end = None, None

    def start_date(self, date):
        self.start = date
        return self
    
    def end_date(self, date):
        self.end = date
        return self

    def filename(self, filename):
        self.fname = filename
        return self

    def run(self):
        printing = not self.start
        for line in open(self.fname, 'r'):
            if self.start and self.start in line:
                printing = True
            if printing:
                print(line.strip())
            if self.end and self.end in line:
                break


if __name__ == '__main__':
    parser = argparse.ArgumentParser('printrange')
    parser.add_argument('filename')
    parser.add_argument('--after', type=str)
    parser.add_argument('--before', type=str)
    args = parser.parse_args()
    lp = LinePrinter().start_date(args.after)\
                      .end_date(args.before)\
                      .filename(args.filename)
    lp.run()
