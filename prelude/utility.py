import datetime
import dateutil
import matplotlib.pyplot
import numpy
import os
import re

dt = datetime
dp = dateutil.parser
plt = matplotlib.pyplot
np = numpy

from collections import defaultdict


def choose_from_list(ls, msg="?: "):
    """Given a list, return a n entry.

    Useful to visually select from a large list of complex items."""
    if len(ls) == 0:
        return None
    if len(ls) == 1:
        print("Only 1 item.  Chose: {}".format(ls[0]))
        return ls[0]
    for i, v in enumerate(ls):
        print("{:3d}: {}".format(i, v))
    idx = input(msg)
    return ls[int(idx)]

def choose_filtered(ls, condition, msg="?: "):
    """First filter a list, and then chose an entry from it."""
    return choose_from_list(list(filter(condition, ls)))

def insert_into_timeseries(ts_host, ts_toEnter, things_toEnter, default=0):
    """Insert -something- at nearest point in timeseries.

    Given [timestamps] and [(timestamp, thing)], insert
    thing into the timeseries at the closest point.

    Between timestamps, repeat current thing."""

    out = np.full(len(ts_host), default)

    target = 0
    t0, tn = ts_toEnter[target], ts_toEnter[target+1]
    b0 = things_toEnter[target]
    limit = len(ts_toEnter)

    for i, t in enumerate(ts_host):
        if t >= tn:
            target += 1
            if target < (limit - 1):
                b0 = things_toEnter[target] # Current _thing_
                tn = ts_toEnter[target+1] # Next time
        out[i] = b0
    return out

def adc_to_value(adc_values, precision, sensitivity):
    """Convert a data series from raw values into units
    given the precision and sensitivy of the sensor.

    adc_values :: 'list-like' object representing ADC values
    precision :: Number of 'bits'
    sensitivity :: Range of sensor for this number of 'bits'"""
    adc_values = pd.Series(adc_values)
    adc_range = float(pow(2, precision - 1))
    return adc_values * sensitivity / adc_range

def timestamp_mean_duration(ts):
    """Estimates mean duration from a list of timestamps.

    Arguments:
    ts -- list of timestamps
    """
    if type(ts[0]) == type(""):
        ts = list(map(dp.parse, ts))
    pairs = zip(ts, ts[1:])
    diffed = map(lambda z: (z[1] - z[0]).total_seconds(), pairs)
    return np.mean(list(diffed))

def most_prevalent(ls):
    """Return the most prevalent element in a list."""
    seen = defaultdict(int)
    for value in ls:
        seen[value] += 1
    largest = 0
    largest_key = ''
    for k, v in seen.items():
        if v > largest:
            largest = v
            largest_key = k
    return largest_key

def listdir_matching_regex(directory, regex='.*.csv'):
    """Given a regex, return matching files.

    By default, return CSVs from a directory."""
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

def choose_from_dir(directory, regex='.*.csv', msg='?: '):
    return choose_from_list(listdir_matching_regex(directory, regex), msg)

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
    outfn = '{}{}'.format(suffix, today_date_str)
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
