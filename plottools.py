"""Utilities for dealing with formatting and saving figures"""
import datetime
import os
import os.path
import re

import matplotlib


def _time_to_str_seconds(secs):
    """Convert a passed integer to a datetime of secs seconds"""

    return str(datetime.timedelta(seconds=secs))


def format_specgram_axis(axis):
    """Add time ticks to a specgram x-axis"""

    formatter = matplotlib.ticker.FuncFormatter(_time_to_str_seconds)
    axis.xaxis.set_major_formatter(formatter)

    return axis


def dated_title(**kwargs):
    """Get time of save in YYYY-MM-DD_hh-mm format, with title and extension

    Keyword Arguments
    -----------------
    title : str [default: None]
        Title to use after timestamp to give filename extra info
    ext : str [default: 'pdf']
        Extension to use for the file
    dateonly : bool [default: False]
        Whether to use full datetime (YYYYMMDDTHHmmss) or just YYYYMMDD

    Returns
    -------
    filename : str
        String with current timestamp prepended
    """
    ext = kwargs.get('ext', 'pdf')
    timestamp = datetime.datetime.now().strftime("%Y%m%dT%H%M")

    if kwargs.get('dateonly', False):
        timestamp = datetime.datetime.now().strftime("%Y%m%d")
    title = kwargs.get('title', None)

    if not title:
        return "{}.{}".format(timestamp, ext)
    sanitised = re.sub(r'[\[\]/\;,><&*:%=+@!#^()|?^]', '', title)
    title = sanitised.replace(" ", "-").lower()

    return "{}--{}.{}".format(timestamp, title, ext)


def savefig(figure, **kwargs):
    """Save a figure into an env-variable defined directory

    Parameters
    ----------
    figure : matplotlib.pyplot.figure
        Figure to save

    Keyword Arguments
    -----------------
    project_and_trial : str [default: '']
        Root-level folder to save figure in
    task : str [default: '']
        Sub-directory to save figure in, under `project_and_trial`
    title : str [default: None]
        Title to use for the saved figure
    ext : str [default: 'png']
        Extension for the saved figure
    dated : bool [default: False]
        Whether to prepend a date to the filename

    Returns
    -------
    filename : str
        Full filepath of the saved file
    """
    project_and_trial = kwargs.get('project_and_trial', '')
    task = kwargs.get('task', '')
    title = kwargs.get('title', None)
    ext = kwargs.get('ext', 'pdf')
    dir_figures = os.environ['RESEARCHFIGURES']

    if dir_figures is None or not os.path.exists(dir_figures):
        raise Exception('Need environment RESEARCHFIGURES set to a directory')

    if figure is None:
        raise Exception("Nothing to save!  Need to pass a figure.")
    dir_saved = os.path.join(dir_figures, project_and_trial, task)

    if not os.path.exists(dir_saved):
        print('dir: ', dir_saved)
        os.makedirs(dir_saved)

    if kwargs.get('dated', False):
        title = dated_title(**kwargs)
    else:
        title = '{}.{}'.format(title, ext)
    filename_saved = os.path.join(dir_saved, title)
    figure.savefig(filename_saved, **kwargs)

    return filename_saved


def plot_projects():
    """Show the list of projects (folders) in RESEARCHFIGURES env directory"""
    dir_figures = os.environ['RESEARCHFIGURES']

    if dir_figures == '' or not os.path.exists(dir_figures):
        raise Exception("No directory at RESEARCHFIGURES environment variable")

    for filename in os.listdir(dir_figures):
        if os.path.isdir(os.path.join(dir_figures, filename)):
            print(filename)
