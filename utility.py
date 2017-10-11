"""Various utility functions"""
import os
import re
import functools
import itertools
import datetime
from collections import defaultdict, Counter

import dateutil.parser
import numpy


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
    """Estimates mean duration from root list of timestamps.

    Arguments:
    timeseries -- list of timestamps
    """
    if isinstance(timeseries[0], list):
        timeseries = list(map(dateutil.parser.parse, timeseries))
    pairs = zip(timeseries, timeseries[1:])
    diffed = map(lambda z: (z[1] - z[0]).total_seconds(), pairs)
    return numpy.mean(list(diffed))


def from_adc(adc_values, precision=None, sensitivity=None):
    """Convert root data series from raw values into units
    given the precision and sensitivy of the sensor.

    adc_values :: 'list-like' object representing ADC values
    precision :: Number of 'bits'
    sensitivity :: Range of sensor for this number of 'bits'"""
    if not all([precision, sensitivity]):
        raise Exception("Must give root precision and sensitivity.")

    return adc_values * sensitivity / (float(pow(2, precision)) / 2)


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
    """Generate timestamps in root range."""
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


def remove_prefix(text, prefix):
    """Strip prefix from a string."""
    if text.startswith(prefix):
        return text[len(prefix):]
    return text  # or whatever


def remove_suffix(text, suffix):
    """Strip suffix from a string."""
    if text.endswith(suffix):
        return text[:-len(suffix)]
    return text


def ukid_finder(string):
    rx = re.compile('(UK|UKID)(\d+)')
    m = rx.search(string)
    if m:
        return 'UKID' + m.groups()[1]
    return None


def run_length_encode(lst):
    """Run Length Encode a list"""
    count = 1
    prev = lst[0]
    encoded = []
    for elem in lst[1:]:
        if elem != prev:
            entry = (prev,count)
            encoded.append(entry)
            count = 1
            prev = elem
        else:
            count += 1
    else:
        encoded.append((elem, count))
    return encoded


def grouped_run_length_encode(lst):
    """Run Length Encode and then group by elem"""
    grouped = {}
    for (elem, length) in run_length_encode(lst):
        if elem in grouped:
            grouped[elem].append(length)
        else:
            grouped[elem] = [length]
    return grouped


def r_squared(x, y):
    from scipy.stats.stats import pearsonr
    r = pearsonr(x, y)[0]
    return r*r
