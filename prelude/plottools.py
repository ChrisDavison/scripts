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

def dated_title(title=None, ext='png'):
    fmtdate = dt.datetime.now().strftime("%Y%m%d-%H%M")
    title = __fn_sanitise(title).replace(" ", "-").lower()
    return "{}--{}.{}".format(fmtdate, title, ext)

def dated_fig_dir_and_filename(notebook_name=None, title=None, ext='png'):
    curdir = os.getcwd()
    plotdir = os.path.join(curdir, '..', '__PLOTS', __fn_sanitise(notebook_name))
    plotdir_abs = os.path.abspath(plotdir)
    out = os.path.join(plotdir_abs, dated_title(title, ext))
    return plotdir_abs, out

def save_dated_fig(fig, *, notebook_name=None, title=None, ext='png'):
    """Save in ./../__PLOTS a file with date as prefix."""
    if not notebook_name:
        raise Exception("Must give a notebook name.")
    plotdir, fn_out = dated_fig_dir_and_filename(notebook_name, title, ext)
    if not os.path.exists(plotdir):
        os.mkdir(plotdir)
    fig.savefig(fn_out)
