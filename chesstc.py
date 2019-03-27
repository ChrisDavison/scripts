#! /usr/bin/env python3
import os, sys

args = sys.argv[1:]
if len(args) < 2:
    print("usage: chesstc <BASE> <INCREMENT>")
    sys.exit(1)

base, inc, *rest = args

totalsec = float(base) * 60 + float(inc) * 40
minutes = int(totalsec / 60)
remsec = int(totalsec - minutes * 60)
print(f"{minutes}:{remsec}")
