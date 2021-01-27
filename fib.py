#!/usr/bin/env python3
import sys
from typing import Iterator
from itertools import islice


def fib_gen() -> Iterator[int]:
    prev = 1
    cur = 2
    yield prev
    yield cur
    while True:
        prev, cur = cur, prev + cur
        yield cur


n = int(sys.argv[1])
n_fibs = list(islice(fib_gen(), n))
print(' '.join(str(f) for f in n_fibs))

