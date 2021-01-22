#!/usr/bin/env python3
"""chesstc - Calculate expected chess game time.

usage: chesstc <base> <increment>

This calculates the expected duration of a chess game (minutes:seconds) for a
given base and increment; e.g. 5+0 should take approx 10 minutes.

Assumes 40 moves, using a given base and increment.  Each player will have
half of this duration each.
"""
from argparse import ArgumentParser

PARSER = ArgumentParser(description="Get expected time of a chess match")
PARSER.add_argument("base", help="Number of minutes to start", type=int)
PARSER.add_argument("increment", help="Seconds per move", type=int)

ARGS = PARSER.parse_args()

total_sec = ARGS.base * 60 + ARGS.increment * 40 * 2
minute = int(total_sec / 60)
remsec = int(int(total_sec) - minute*60)
print("{}:{}".format(minute, remsec))

