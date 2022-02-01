#!/usr/bin/env python3
import pandas as pd
from argparse import ArgumentParser
import pyperclip


def main(filename, rounding, sheetname=None):
    # not using sheetname yet
    data = pd.read_excel(filename).round(rounding)
    print(data.to_markdown(index=False))
    pyperclip.copy(data.to_markdown(index=False))


if __name__ == "__main__":
    parser = ArgumentParser("excel2markdown")
    parser.add_argument("--round", help="Number of decimal places to keep", default=2)
    parser.add_argument("--sheet", help="Sheetname to use", required=False)
    parser.add_argument("file", help="File to display as markdown", type=str)
    args = parser.parse_args()
    main(args.file, args.round, args.sheet)
