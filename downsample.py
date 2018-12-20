"""Downsample a file

usage:
    downsample file col freq [--skipfirst]

arguments:
    file    File to downsample
    col     Column with timestamps (0-indexed)
    freq    New samplerate

options:
    --skipfirst   Skip the first row (e.g. header)
"""
from pathlib import Path

from docopt import docopt
import pandas as pd

args = docopt(__doc__)

df = pd.read_csv(args['file'],
                 skiprows=1 if args['--skipfirst'] else 0,
                 parse_dates=[args['col']],
                 index_col=args['col'],
                 nrows=300)
print(df.head())

resampled = df.columns[args['col']]
    .resample(args['freq'])
    .agg(lambda x: x.iloc[0])
    .reset_index()
print(resampled.head())
