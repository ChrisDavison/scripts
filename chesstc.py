#! /usr/bin/env python
"""chesstc - Calculate expected chess game time.

usage: chesstc <BASE> <INCREMENT>

This calculates the expected duration of a chess game (Min:Sec) for a given
base and increment; e.g. 5+0 should take approx 10 minutes.

Assumes 40 moves, using a given base and increment.  Each player will have
half of this duration each."""
import sys


def timecontrol(base, increment):

    totalsec = (float(base) * 60 + float(increment) * 40) * 2
    minutes = int(totalsec / 60)
    remsec = int(totalsec - minutes * 60)
    print(f"{minutes}:{remsec}")


if __name__ == "__main__":
    args = sys.argv[1:]
    try:
        base = float(args[0])
        increment = float(args[1])
        timecontrol(base, increment)
    except:
        print(__doc__)
