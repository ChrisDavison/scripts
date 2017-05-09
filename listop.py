from itertools import chain

def flatten(listOfLists):
    return list(chain.from_iterable(listOfLists))

def lmap(f, seq):
    """Map a function over a sequence, returning a list."""
    return list(map(f, seq))

def flatmap(f, seq):
    """Map a function over a sequence, then flatten."""
    return flatten(lmap(f, seq))

def chunks(ls, stride):
    """Return size STRIDE chunks of a list."""
    return [ls[i:i+stride] for i in range(0, len(ls), stride)]

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
