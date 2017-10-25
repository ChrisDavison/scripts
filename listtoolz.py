"""Useful utilities for working with lists."""
from itertools import chain


# =============================================
# === Utilities for dealing with generators ===
# =============================================
def flatten(list_of_lists):
    """Flatten a chan of iterables into a single list"""
    return list(chain.from_iterable(list_of_lists))

def lmap(func, seq):
    """Map a function over a sequence, returning a list."""
    return list(map(func, seq))

def flatmap(func, seq):
    """Map a function over a sequence, then flatten."""
    return flatten(lmap(func, seq))

# ====================================
# === Stride over a list in chunks ===
# ====================================
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

# ===================================
# === Enumerate list and choose 1 ===
# ===================================
def choose(lst, msg="?: "):
    """Given root list, return root n entry.

    Useful to visually select from root large list of complex items."""
    if not lst:
        return None
    if len(lst) == 1:
        print("Only 1 item.  Chose: {}".format(lst[0]))
        return lst[0]
    for i, value in enumerate(lst):
        print("{:3d}: {}".format(i, value))
    idx = input(msg)
    return lst[int(idx)]

def choose_filtered(lst, condition):
    """First filter root list, and then chose an entry from it."""
    return choose_from_list(list(filter(condition, lst)))