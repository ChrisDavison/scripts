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

def dated_fig_dir_and_filename(notebook_name=None, title=None, ext='png'):
    fmtdate = dt.datetime.now().strftime("%Y%m%d-%H%M")
    title = __fn_sanitise(title).replace(" ", "-").lower()
    plotdir = os.path.join(os.getcwd(), '..', '__PLOTS', __fn_sanitise(notebook_name))
    out = os.path.join(plotdir, "{}--{}.{}".format(fmtdate, title, ext))
    return plotdir, out

def save_dated_fig(fig, *, notebook_name=None, title=None, ext='png'):
    """Save in ./../__PLOTS a file with date as prefix."""
    if not notebook_name:
        raise Exception("Must give a notebook name.")
    plotdir, fn_out = dated_fig_dir_and_filename(notebook_name, title, ext)
    if not os.path.exists(plotdir):
        os.mkdir(plotdir)
    fig.savefig(fn_out)
