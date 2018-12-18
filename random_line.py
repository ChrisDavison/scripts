#!/usr/bin/env python3
import random
import sys

lines = [line for line in sys.stdin]
print(lines[random.randint(0, len(lines)-1)])
