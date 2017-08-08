import datetime
import matplotlib
import re
import os
import os.path


def format_specgram_axis(ax):
    """Add time ticks to a specgram x-axis"""
    def timeTicks(x, pos):
        d = datetime.timedelta(seconds=x)
        return str(d)
    formatter = matplotlib.ticker.FuncFormatter(timeTicks)
    ax.xaxis.set_major_formatter(formatter)


def dated_title(title=None, ext='png'):
    """Get time of save in YYYY-MM-DD_hh-mm format, with title and extension."""
    d = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
    if not title:
        return "{}.{}".format(d, ext)
    sanitised = re.sub(r'[\[\]/\;,><&*:%=+@!#^()|?^]', '', title)
    title = sanitised.replace(" ", "-").lower()
    return "{}_{}.{}".format(d, title, ext)


def savefig(figure, *, project_and_trial='', task='', title=None, ext='png', **kwargs):
    """Save a figure into an env-variable defined directory

    Using the env variable RESEARCHFIGURES, save the passed figure into directory
    `project_and_trial`, with subdirectory `task` and a timestamped title"""
    dir_figures = os.environ['RESEARCHFIGURES']
    if dir_figures == '' or not os.path.exists(dir_figures):
        raise Exception('Need environment RESEARCHFIGURES set to a directory')
    if figure is None:
        raise Exception("Nothing to save!  Need to pass a figure.")
    dir_saved = os.path.join(dir_figures, project_and_trial, task)
    if not os.path.exists(dir_saved):
        print('dir: ', dir_saved)
        os.makedirs(dir_saved)
    filename_saved = os.path.join(dir_saved, dated_title(title, ext))
    figure.savefig(filename_saved, **kwargs)
    return filename_saved
