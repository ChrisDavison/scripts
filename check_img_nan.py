#!/usr/bin/env python
import sys
import rasterio as rio

if len(sys.argv) == 1:
    print("usage: check_img_nan.py <filename>...")

for filename in sys.argv[1:]:
    data = rio.open(filename).read()
    print(filename)
    print(f"min: {data.min()}")
    print(f"max: {data.max()}")
    print()
