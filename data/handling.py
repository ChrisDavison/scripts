"""Utilities for handling pandas dataframes.

Functions:
    subset: Get a subset of a pandas dataframe

    dataframe_hours: Return a list of the hours in a dataframe
    dataframe_days: Return a list of the days in a dataframe

    hours_from_dataframe: Generator over the hours in a dataframe
    days_from_dataframe: Generator over the days in a dataframe
"""
import cdutils.data.info as cddi


def subset(dataframe, **kwargs):
    """Return subset of timestamped dataframe, [start..end]

    Args:
        dataframe *(pandas dataframe): Data to get subset of

    Kwargs:
        start (datetime): Start timestamp
        end (datetime): End Timestamp

    Raises:
        KeyError (if start or end kwarg is not given)
    """
    tk = cddi.timekey(dataframe)
    try:
        s, e = str(kwargs['start']), str(kwargs['end'])
        ix_s = dataframe[dataframe[tk] > s].index[0]
        ix_e = dataframe[dataframe[tk] > e].index[0]
        return dataframe[ix_s:ix_e].reset_index()
    except KeyError as E:
        raise E


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
    days = sorted(set(map(lambda x: x.split(' ')[0], dataframe[tk])))
    prev_day = days[0]
    for day in days[1:]:
        after_start = (dataframe[tk] >= prev_day)
        before_end = (dataframe[tk] < day)
        yield prev_day, dataframe[after_start & before_end]
        prev_day = day
