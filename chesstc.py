#! /usr/bin/env python3
import click


@click.command("timecontrol")
@click.argument("base", nargs=1, type=float)
@click.argument("increment", nargs=1, type=float)
def timecontrol(base, increment):
    """Calculate expected chess game time.

    Assumes 40 moves, using a given base and increment.  Each player will have
    half of this duration each."""
    totalsec = (float(base) * 60 + float(increment) * 40) * 2
    minutes = int(totalsec / 60)
    remsec = int(totalsec - minutes * 60)
    print(f"{minutes}:{remsec}")

if __name__ == "__main__":
    timecontrol()
