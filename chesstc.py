#! /usr/bin/env python3
import os, sys

def timecontrol(b, i):
    totalsec = b*60 + i*40
    minutes = int(totalsec/60)
    remsec = int(totalsec - minutes*60)
    print(f"{minutes}:{remsec}")


if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) < 2:
        print("usage: chesstc <BASE> <INCREMENT>")
        sys.exit(1)
    b, i, *rest = args
    timecontrol(float(b), float(i))
