import datetime
import matplotlib
import re
import os
import os.path

dt = datetime

def format_specgram_axis(ax):
    def timeTicks(x, pos):
        d = dt.timedelta(seconds=x)
        return str(d)
    formatter = matplotlib.ticker.FuncFormatter(timeTicks)
    ax.xaxis.set_major_formatter(formatter)

def __fn_sanitise(s):
    for c in r'[]/\;,><&*:%=+@!#^()|?^':
        s = s.replace(c,'')
    return s

def formatted_date():
    return dt.datetime.now().strftime("%Y-%m-%d_%H-%M")

def dated_title(title=None, ext='png'):
    fmtdate = formatted_date()
    title = __fn_sanitise(title).replace(" ", "-").lower()
    return "{}--{}.{}".format(fmtdate, title, ext)

def dated_fig_dir_and_filename(notebook_name=None, title=None, ext='png'):
    curdir = os.getcwd()
    plotdir = os.path.join(curdir, '..', '__PLOTS', __fn_sanitise(notebook_name))
    plotdir_abs = os.path.abspath(plotdir)
    out = os.path.join(plotdir_abs, dated_title(title, ext))
    return plotdir_abs, out


def savefig(figure, *, project=None, trial=None, task=None, title=None, ext='png', **kwargs):
    def get_title(title, ext):
        d = formatted_date()
        if title is None:
            return "{}.{}".format(d, ext)
        return "{}_{}.{}".format(d, title, ext)
    dir_figures = os.environ['RESEARCHFIGURES']
    dir_saved = ""
    if dir_figures == '' or not os.path.exists(dir_figures):
        raise Exception('Need environment RESEARCHFIGURES set to a directory')
    if figure is None:
        raise Exception("Nothing to save!  Need to pass a figure.")
    if project is None:
        dir_saved = os.path.join(dir_figures)
    elif trial is None:
        dir_saved = os.path.join(dir_figures, project)
    elif task is None:
        dir_saved = os.path.join(dir_figures, project, trial)
    else:
        dir_saved = os.path.join(dir_figures, project, trial, task)
    if not os.path.exists(dir_saved):
        print('dir: ', dir_saved)
        os.makedirs(dir_saved)
    filename_saved = os.path.join(dir_saved, get_title(title, ext))
    figure.savefig(filename_saved, **kwargs)
    return filename_saved

def save_dated_fig(fig, *, notebook_name=None, title=None, ext='png'):
    """Save in ./../__PLOTS a file with date as prefix."""
    if not notebook_name:
        raise Exception("Must give a notebook name.")
    plotdir, fn_out = dated_fig_dir_and_filename(notebook_name, title, ext)
    if not os.path.exists(plotdir):
        os.mkdir(plotdir)
    fig.savefig(fn_out)
