#!/usr/bin/env python3
from argparse import ArgumentParser
import sys
import parsedatetime
import time

cal = parsedatetime.Calendar()

def maybe_one_string(args):
    dt, parsed = cal.parse(' '.join(args))
    if parsed:
        return dt
    return None

def main(fmt, datestrs):
    dt = maybe_one_string(datestrs)
    if dt:
        print(time.strftime(fmt, dt))
    else:
        for arg in datestrs:
            dt, parsed = cal.parse(arg)
            if parsed:
                print(time.strftime(fmt, dt))
            else:
                print(f"Couldn't parse {arg}")


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('-f', '--format', default='%Y-%m-%d')
    parser.add_argument('datestrs', nargs='+')
    args = parser.parse_args()
    main(args.format, args.datestrs)

