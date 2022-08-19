#!/usr/bin/env python3
import click
import datetime


def bpm_for_pct(age, rhr, pct):
    """Calculate heartrate for pct, assuming theoretical max based on age."""
    max_hr = (220 - age - rhr)
    return max_hr * pct / 100.0 + rhr

@click.command()
@click.argument("pct_lo", type=float, required=True)
@click.argument("pct_hi", type=float, required=True)
@click.argument("age", type=int, required=False)
@click.argument("rhr", type=int, required=False)
def main(pct_lo, pct_hi, age, rhr):
    if not age:
        age = int((datetime.date.today() - datetime.date(1989, 12, 2)).days / 365)
    if not rhr:
        rhr = 60
    bpm_lo = bpm_for_pct(age, rhr, pct_lo)
    bpm_hi = bpm_for_pct(age, rhr, pct_hi)
    print(f"{pct_lo} to {pct_hi}% => {bpm_lo} to {bpm_hi} bpm")
    bpm_lo = bpm_for_pct(age, rhr, pct_lo)

if __name__ == '__main__':
    main()
