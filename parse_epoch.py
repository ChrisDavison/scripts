#!/usr/bin/env python3
import sys
import datetime

from argparse import ArgumentParser

parser = ArgumentParser("parse_epoch")
parser.add_argument("epoch", type=int)
epoch = parser.parse_args().epoch

parser.

print(datetime.datetime.fromtimestamp(int(epoch)).strftime("%Y-%m-%d %H:%M:%S"))
