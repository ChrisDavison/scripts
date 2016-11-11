"""Utilities for getting information from pandas dataframes.

Functions:
    timekey: Get the key representing a timestamp column
    start_and_end: First and last valid timestamp of a dataframe
    first_last: First and last element of a file
    infer_fs: Infer the samplerate of a set of timestamps
    change_points: Get the index and direction when a dataset changes
    change_times: Get the timestamp and direction when a dataset changes
"""
import dateutil
import pandas as pd
import time


def epoch_to_time(epoch):
    """Convert epoch to YY-MM-DD HH:MM:SS."""
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(epoch))


def overlapping_timeperiod(dataframes):
    """Given a list of dataframes, return overlapping (start, stop)"""
    min_time = 0
    max_time = 999999999999
    for df in dataframes:
        tk = timekey(df)
        t0 = dateutil.parser.parse(df[tk][0]).timestamp()
        tN = dateutil.parser.parse(list(df[tk])[-1]).timestamp()
        if t0 > min_time:
            min_time = t0
        if tN < max_time:
            max_time = tN
    if min_time > max_time:
        raise Exception("One file ends before another begins")
    else:
        return (epoch_to_time(min_time), epoch_to_time(max_time))


def timekey(dataframe):
    """Finds the key corresponding to a dataframes timestamps.

    Args:
        dataframe (pandas dataframe): Dataframe to get info from
    """
    return [key for key in dataframe.keys() if 'time' in key][0]


def start_and_end(dataframe, **kwargs):
    """Return first and last timestamp of a dataframe.

    Args:
        dataframe (pandas dataframe)

    Kwargs:
        parsed (bool): Whether to return datetime or string, [default: False]
    """
    tk = timekey(dataframe)
    st = dataframe.ix[dataframe.first_valid_index()][tk]
    end = dataframe.ix[dataframe.last_valid_index()][tk]
    if kwargs.get('parsed', False):
        st = dateutil.parser.parse(st)
        st = dateutil.parser.parse(end)
    return st, end


def first_last(fn, **kwargs):
    """First and last element of a file.

    Args:
        fn (string): Path to file

    Kwargs:
        sep (char): Separator to split line on, [default: ',']
        headers (bool): Whether the file has headers or not, [default: True]
    """
    sep = kwargs.get('sep', ',')
    headers = kwargs.get('headers', True)
    with open(fn, "rb") as f:
        if headers:
            f.readline()     # Read and skip the first line.

        first = f.readline()     # Read the second line.
        f.seek(-2, 2)            # Jump to the second last byte.
        while f.read(1) != b"\n":   # Until EOL is found...
            f.seek(-2, 1)        # ...jump back the read byte plus one more.
        last = f.readline()
    s = first.decode('ascii').split(sep)[0]
    e = last.decode('ascii').split(sep)[0]
    return s, e


def infer_fs(timestamps, **kwargs):
    """Infer the samplerate of a set of timestamps.

    Args:
        timestamps ([timestamp strings]): List of timestamps

    Kwargs:
        N (int): Number of timestamps to use to infer the samplerate
    """
    N = kwargs.get('N', 36000)
    if N > len(timestamps):
        raise EOFError
    times = list(pd.to_datetime(timestamps[:N]))
    times2 = times[1:]
    pairs = zip(times, times2)
    diffs = list(map(lambda p: p[1]-p[0], pairs))
    tot = diffs[0]
    for dif in diffs[1:]:
        tot += dif
    return N / tot.total_seconds()


def change_points(dataseries):
    """Return a list of (index, direction) where dataseries changes value.

    Args:
        dataseries (pandas dataseries):  Dataset to look through

    Returns:
        [(index, duration)]: Duration is either -1 or +1
                             indicating fall or rise.
    """
    change_points = []
    for i, val in enumerate(dataseries[1:]):
        if dataseries[i] > dataseries[i-1]:
            change_points.append((i, 1))
        elif dataseries[i] < dataseries[i-1]:
            change_points.append((i, -1))
    return change_points


def change_times(dataseries, timestamps):
    """Get timestamps when dataset rises or falls.

    Should be used with 'digital' data, i.e. when only a few representative
    values, such as a classifier with a fixed number of states.

    Args:
        dataseries (pandas dataseries): Dataset to summarise
        timestamps ([timestamps]): Timestamps from the dataset

    Returns:
        [(timestamp, direction)]: Direction -1/+1 represents fall or rise
    """
    ch = change_points(dataseries)
    return [(timestamps[i], direction) for (i, direction) in ch]
