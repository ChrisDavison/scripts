#!/usr/bin/env python3
import fileinput
import math
import re


READ_SPEED = (150.0, 200.0)


def reading_time(words):
    hi = math.ceil(float(words) / READ_SPEED[0])
    lo = math.ceil(float(words) / READ_SPEED[1])
    plural = "s" if hi > 1 else ""
    if lo == hi:
        return f"{lo} minute{plural}"
    return f"{lo}-{hi} minute{plural}"


count = 0
current_filename = None
for line in fileinput.input():
    if not current_filename: 
        current_filename = fileinput.filename()
    else:
        if fileinput.filename() != current_filename: 
            print(f"{current_filename} - {reading_time(count)}")
            count = 0
    words = [w for w in re.split("\W+", line) if w]
    count += len(words)
    current_filename = fileinput.filename()

if count:
    print(f"{current_filename} - {reading_time(count)}")
