#!/usr/bin/env python
"""Utilities relating to the operating system.

Functions:
    dated_directory: Create a directory with todays date as name
    choose_from_dir: Choose from filtered files in a directory
    listdir_matching_regex: Return filepath from directory matching regex
"""
import os
import datetime
import re


def dated_directory(root, **kwargs):
    """Create a directory with todays date and optional suffix.

    Parameters
    ----------
    Args:
        root (string): Parent directory

    Kwargs:
        project (string): Prefix to append [default: None]
        source (string): Origin of the data (script) [default: None]

    Return
    ------
        folderpath (string): path of the created folder
    """
    project = kwargs.get('project', None)
    source = kwargs.get('source', None)
    today = datetime.datetime.now()
    today_date_str = today.strftime('%Y%m%d')

    outfn = '{}'.format(today_date_str)
    outfn = '{}-{}'.format(source, outfn) if source else outfn
    outfn = '{}-{}'.format(project, outfn) if project else outfn
    folderpath = os.path.join(root, outfn)

    if not os.path.exists(folderpath):
        os.makedirs(folderpath)
    return folderpath


def choose_from_dir(directory, **kwargs):
    """Given a directory, choose and return a single filepath.

    Parameters
    ----------
    Args:
        directory (string): The directory to list

    Kwargs:
        regex (string): Regular expression to filter files
        searchstr (string): Filter additionally with direct string match
        msg (string): Prompt to display while choosing file
    """
    regex = kwargs.get('regex', '.*{}.*.csv$')
    searchstr = kwargs.get('searchstr', '')
    msg = kwargs.get('msg', 'Which file: ')

    if '{}' in regex:
        regex = regex.format(searchstr)
    rx = re.compile(regex)
    files = sorted(filter(rx.match, os.listdir(directory)))

    for i, f in enumerate(files):
        print("{:3d}:\t{}".format(i, f))

    while(1):
        choice = int(input(msg))
        if choice in range(0, len(files)):
            break
    print()
    return os.path.join(directory, files[choice])


def listdir_matching_regex(directory, regex):
    "Given a regex, return matching files."
    out = []
    reg = re.compile(regex)
    for f in os.listdir(directory):
        m = reg.match(f)
        has_group = '(' in regex and ')' in regex
        if m and has_group:
            out.append(m.group(1))
        elif m:
            out.append(m.group(0))
    return out
