#! /usr/bin/env python
"""Utilities for dealing with pandas dataframes."""
import time
import datetime
import csv

import dateutil  # For parsing timestamps easily
import pandas


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


def start_and_end(dataframe):
    """Return first and last timestamp of a dataframe.

    Args:
        dataframe (pandas dataframe)
    """
    tk = timekey(dataframe)
    dp = dateutil.parser.parse
    st = dp(dataframe.ix[dataframe.first_valid_index()][tk])
    end = dp(dataframe.ix[dataframe.last_valid_index()][tk])
    return st, end


def first_last(fn, *, sep=',', headers=True):
    """First and last element of a file.

    Args:
        fn (string): Path to file

    Kwargs:
        sep (char): Separator to split line on.
        headers (bool): Whether the file has headers or not.
    """
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


def infer_fs(timestamps, N=36000):
    """Infer the samplerate of a set of timestamps.

    Args:
        timestamps ([timestamp strings]): List of timestamps

    Kwargs:
        N (int): Number of timestamps to use to infer the samplerate
    """
    if N > len(timestamps):
        raise EOFError
    times = list(pandas.to_datetime(timestamps[:N]))
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


def subset(dataset, *, start=None, end=None, shift=None):
    """Return subset of timestamped dataframe, [start..end]

    Args:
        dataset (pandas DataFrame): Dataset to shorten

    Kwargs:
        start (datetime): Start date for the shortened dataset
        end (datetime): End date for the shortened dataset
        shift (timedelta): Optional timedelta to move dataset.

    If start < dataset start, use dataset start.
    If end > dataset end, use dataset end.
    """
    if not shift:
        shift = datetime.timedelta(minutes=0)
    if type(start) != datetime.datetime or type(end) != datetime.datetime:
        raise Exception("Must pass datetime for start and end.")
    times = dataset[timekey(dataset)]
    ds_t_zero, ds_t_end = times.iloc[0], times.iloc[-1]
    s, e = str(start + shift), str(end + shift)
    ix_s = 0 if s < ds_t_zero else times[times > s].index[0]
    ix_e = dataset.size if e > ds_t_end else times[times > e].index[0]
    return dataset[ix_s:ix_e].reset_index()


def dataframe_hours(dataframe):
    """Return a list of all hours in the dataframe.

    Args:
        dataframe (pandas dataframe): Dataframe to summarise

    Returns:
        times ([string]): Times from the dataframe
    """
    tk = timekey(dataframe)
    return tk, sorted(set(map(lambda x: x.split(':')[0], dataframe[tk])))


def dataframe_days(dataframe):
    """Return a list of all days (dates) in the dataframe.

    Args:
        dataframe (pandas dataframe): Dataset to summarise

    Returns:
        days ([string]): List of days in the dataframe, sorted
    """
    tk = timekey(dataframe)
    return sorted(set(map(lambda x: x.split(' ')[0],
                  dataframe[tk])))


def hours_from_dataframe(dataframe):
    """Yield each hours worth of data from a dataframe.

    Generator function that will return an hours worth of data from a
    pandas dataframe.

    Args:
        dataframe (pandas dataframe): Dataframe to pull data from

    Returns:
        hours (generator): Generator over hours in the dataframe
    """
    tk, hours = dataframe_hours(dataframe)
    prev_hour = hours[0]
    for hour in hours[1:]:
        after_start = (dataframe[tk] >= prev_hour)
        before_end = (dataframe[tk] < hour)
        yield prev_hour, dataframe[after_start & before_end]
        prev_hour = hour


def days_from_dataframe(dataframe):
    """Yield each days worth of data from a dataframe.

    Generator function that will return a days worth of data from a
    pandas dataframe.

    Args:
        dataframe (pandas dataframe): Dataframe to pull data from

    Returns:
        hours (generator): Generator over days in the dataframe
    """
    tk = timekey(dataframe)
    days = dataframe_days(dataframe)
    prev_day = days[0]
    for day in days[1:]:
        after_start = (dataframe[tk] >= prev_day)
        before_end = (dataframe[tk] < day)
        yield prev_day, dataframe[after_start & before_end]
        prev_day = day
    yield day, dataframe[(dataframe[tk] >= prev_day)]


def dataframe_from_lazy_csv(filename, start, stop):
    data = []
    with open(filename) as f:
        dr = csv.DictReader(f)
        tk = [k for k in dr.fieldnames if 'time' in k][0]
        data = [row for row in dr
                if row[tk] > start and row[tk] < stop]
    return pandas.DataFrame(data).set_index(tk)
