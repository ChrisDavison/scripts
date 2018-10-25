from argparse import ArgumentParser
from pathlib import Path

import pandas as pd

parser = ArgumentParser("downsample")
parser.add_argument("file", help="File to downsample")
parser.add_argument("col", help="Column with timestamps (0-indexed int)", type=int)
parser.add_argument("freq", help="New samplerate")
parser.add_argument("--skipfirst", action="store_true")
args = parser.parse_args()

df = pd.read_csv(args.file, skiprows=1 if args.skipfirst else 0,  parse_dates=[args.col], nrows=300)
print(df.head())
resampled = df.set_index(df.columns[args.col]).resample(args.freq).agg(lambda x: x.iloc[0]).reset_index()
print(resampled.head())
