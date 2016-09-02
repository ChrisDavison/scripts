"""Utilities for handling pandas dataframes.

Functions:
    subset: Get a subset of a pandas dataframe

    dataframe_hours: Return a list of the hours in a dataframe
    dataframe_days: Return a list of the days in a dataframe

    hours_from_dataframe: Generator over the hours in a dataframe
    days_from_dataframe: Generator over the days in a dataframe
"""
from . import info as cddi
import datetime as dt
import dateutil.parser as dp

def subset(dataset, **kwargs):
    """Return subset of timestamped dataframe, [start..end]

    Args:
        dataset (pandas DataFrame): Dataset to shorten

    Kwargs:
        start (timestamp): Start date for the shortened dataset
        end (timestamp): End date for the shortened dataset

    If start < dataset start, use dataset start.
    If end > dataset end, use dataset end.
    """
    start = kwargs.get('start', None)
    end = kwargs.get('end', None)
    shift = kwargs.get('shift', dt.timedelta(minutes=0))

    if start == None or end == None:
        return None

    tk = cddi.timekey(dataset)
    N = len(dataset)
    ds_t_zero = dataset.iloc[0][tk]
    ds_t_end = dataset.iloc[-1][tk]
    s, e = str(dp.parse(start )+ shift), str(dp.parse(end )+ shift)
    ix_s = 0 if (s < ds_t_zero) else  dataset[dataset[tk] > s].index[0]
    ix_e = (N-1) if (e > ds_t_end) else dataset[dataset[tk] > e].index[0]
    return dataset[ix_s:ix_e].reset_index(drop=True)


def dataframe_hours(dataframe):
    """Return a list of all hours in the dataframe.

    Args:
        dataframe (pandas dataframe): Dataframe to summarise

    Returns:
        times ([string]): Times from the dataframe
    """
    tk = cddi.timekey(dataframe)
    return tk, sorted(set(map(lambda x: x.split(':')[0], dataframe[tk])))


def dataframe_days(dataframe):
    """Return a list of all days (dates) in the dataframe.

    Args:
        dataframe (pandas dataframe): Dataset to summarise

    Returns:
        days ([string]): List of days in the dataframe, sorted
    """
    tk = cddi.timekey(dataframe)
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
    tk = cddi.timekey(dataframe)
    days = dataframe_days(dataframe)
    prev_day = days[0]
    for day in days[1:]:
        after_start = (dataframe[tk] >= prev_day)
        before_end = (dataframe[tk] < day)
        yield prev_day, dataframe[after_start & before_end]
        prev_day = day
    yield day, dataframe[(dataframe[tk] >= prev_day)]
