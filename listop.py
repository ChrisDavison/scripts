"""Useful utilities for working with lists."""
from itertools import chain

def flatten(list_of_lists):
    """Flatten a chan of iterables into a single list"""
    return list(chain.from_iterable(list_of_lists))

def lmap(func, seq):
    """Map a function over a sequence, returning a list."""
    return list(map(func, seq))

def flatmap(func, seq):
    """Map a function over a sequence, then flatten."""
    return flatten(lmap(func, seq))

def chunks(lst, stride):
    """Return size STRIDE chunks of a list."""
    return [lst[i:i+stride] for i in range(0, len(lst), stride)]

def ichunks(itr, stride):
    """Iterate with size STRIDE over an iterator"""
    data = []
    idx = 0
    for val in itr:
        idx += 1
        data.append(val)
        if idx == stride:
            yield data
            data = []
            idx = 0
    if data:
        yield data
