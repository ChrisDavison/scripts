"""Various utility functions."""
import os
import re
import functools
import datetime
from collections import defaultdict

import dateutil.parser
import numpy


def choose_from_list(lst, msg="?: "):
    """Given a list, return a n entry.

    Useful to visually select from a large list of complex items."""
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
    """First filter a list, and then chose an entry from it."""
    return choose_from_list(list(filter(condition, lst)))

def insert_into_timeseries(ts_host, timeseries_to_enter, things_to_enter, default=0):
    """Insert -something- at nearest point in timeseries.

    Given [timestamps] and [(timestamp, thing)], insert
    thing into the timeseries at the closest point.

    Between timestamps, repeat current thing."""

    out = numpy.full(len(ts_host), default)

    target = 0
    _, time_next = timeseries_to_enter[target], timeseries_to_enter[target+1]
    thing_0 = things_to_enter[target]
    limit = len(timeseries_to_enter)

    for i, time in enumerate(ts_host):
        if time >= time_next:
            target += 1
            if target < (limit - 1):
                thing_0 = things_to_enter[target] # Current _thing_
                time_next = timeseries_to_enter[target+1] # Next time
        out[i] = thing_0
    return out

def timestamp_mean_duration(timeseries):
    """Estimates mean duration from a list of timestamps.

    Arguments:
    timeseries -- list of timestamps
    """
    if isinstance(timeseries[0], list):
        timeseries = list(map(dateutil.parser.parse, timeseries))
    pairs = zip(timeseries, timeseries[1:])
    diffed = map(lambda z: (z[1] - z[0]).total_seconds(), pairs)
    return numpy.mean(list(diffed))

def most_prevalent(lst):
    """Return the most prevalent element in a list."""
    seen = defaultdict(int)
    for value in lst:
        seen[value] += 1
    largest = 0
    largest_key = ''
    for key, value in seen.items():
        if value > largest:
            largest = value
            largest_key = key
    return largest_key

def listdir_matching_regex(directory, regex='.*.csv'):
    """Given a regex, return matching files.

    By default, return CSVs from a directory."""
    out = []
    reg = re.compile(regex)
    for filename in os.listdir(directory):
        match = reg.match(filename)
        has_group = '(' in regex and ')' in regex
        if match and has_group:
            out.append(match.group(1))
        elif match:
            out.append(match.group(0))
    return out

def choose_from_dir(directory, regex='.*.csv'):
    """Given a directory, enumerate values and return chosen value"""
    return choose_from_list(listdir_matching_regex(directory, regex))

def dated_directory(root, suffix=None):
    """Create a directory with todays date and optional suffix.

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

def from_adc(adc_values, precision=None, sensitivity=None):
    """Convert a data series from raw values into units
    given the precision and sensitivy of the sensor.

    adc_values :: 'list-like' object representing ADC values
    precision :: Number of 'bits'
    sensitivity :: Range of sensor for this number of 'bits'"""
    if not all([precision, sensitivity]):
        raise Exception("Must give a precision and sensitivity.")

    return adc_values * sensitivity / (float(pow(2, precision)) / 2)

def absjoin(paths):
    """Given a list of paths, join, and return the absolute path."""
    return os.path.abspath(os.path.join(*paths))

def first(iterable):
    """Return first element from a dataset.  Purely for easier reading"""
    return nth(iterable, 1)

def second(iterable):
    """Return second element from a dataset.  Purely for easier reading"""
    return nth(iterable, 2)

def nth(iterable, num=2):
    """Return Nth element from a dataset.  Purely for easier reading"""
    if len(iterable) > (num-1):
        return iterable[num-1]
    return []

def needs_refactoring(reason):
    """Decorate to not allow operation before refactoring."""
    def actual_decorator(func):
        """Closure around function needing refactoring."""
        @functools.wraps(func)
        def wrapper():
            """Wrapper to raise exception on un-refactored function."""
            # print("{} needs refactoring".format(func.__name__))
            raise Exception('REFACTOR: {}'.format(reason))
        return wrapper
    return actual_decorator

def time_gen(start, stop, step):
    """Generate timestamps in a range."""
    now, end = dateutil.parser.parse(start), dateutil.parser.parse(stop)
    backwards = True if (now > end) else False
    step = -1 * step if backwards else step
    while True:
        yield now
        now += step
        if backwards and now < end:
            break
        if not backwards and now > end:
            break
    if str(now) != start:
        yield now
