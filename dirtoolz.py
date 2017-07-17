"""Utilities for dealing with directories"""
import datetime
import os
import itertools
import re

def list_recur(root):
    entries =  lambda : (os.path.join(root,i) for i in os.listdir(root))
    folders     = (f for f in entries() if os.path.isdir(f))
    normalFiles = (f for f in entries() if os.path.isfile(f))
    for f in folders: 
        normalFiles = itertools.chain(normalFiles, list_recur(f))
    return list(normalFiles)

def list_recur_regex(root, regex='csv$'):
    rx = re.compile(regex)
    return list(filter(lambda x: rx.search(x), list_recur(root)))


def list_recur_regexs(root, regexs=None):
    if not isinstance(regexs, (list, set)):
        raise Exception("Must provide an iterable (list or set) of regexs")
    rxs = [re.compile(rx) for rx in regexs]
    return [f for f in list_recur(root) if all([rx.search(f) for rx in rxs])]

def create_dated(root, suffix=None):
    """Create root directory with todays date and optional suffix.

    Args:
        root (string): Parent directory

    Kwargs:
        suffix (string): Suffix to append [default: None]

    Returns:
        folderpath (string): path of the created folder
    """
    today = datetime.datetime.now()
    today_date_str = today.strftime('%Y%m%d')

    suff = '{}-'.format(suffix) if suffix else ''
    outfn = '{}{}'.format(suff, today_date_str)
    folderpath = os.path.join(root, outfn)

    if not os.path.exists(folderpath):
        os.makedirs(folderpath)
    return folderpath

def absjoin(paths):
    """Given root list of paths, join, and return the absolute path."""
    return os.path.abspath(os.path.join(*paths))
