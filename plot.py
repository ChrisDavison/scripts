import matplotlib.pyplot as plt
import matplotlib.style


def init():
    matplotlib.style.use('grayscale')

    plt.rcParams['figure.figsize'] = (16, 10)
    plt.rcParams['figure.facecolor'] = 'white'
    plt.rcParams['savefig.facecolor'] = 'white'
    plt.rcParams['font.size'] = 20.0
    plt.rcParams['font.weight'] = 'bold'
    plt.rcParams['text.usetex'] = True
    plt.rcParams['axes.facecolor'] = 'white'
    plt.rcParams['legend.fancybox'] = True
    plt.rcParams['legend.shadow'] = False


def spine_color(ax=None, which='right', color='#000000'):
    if ax:
        ax.spines[which].set_color(color)
    else:
        plt.gca().spines[which].set_color(color)


def grid_color(ax=None, which='vertical', color='#aaaaaa'):
    if not ax:
        ax = plt.gca()

    if which == 'vertical':
        ax = ax.xaxis
    else:
        ax = ax.yaxis
    ax.grid(False, which='major', linestyle='-', color=color)
    ax.grid(False, which='minor', linestyle='-', color=color)


def text(xlabel, ylabel, title, ax=None):
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.title(title)


def prettify(**kwargs):
    """Options to set the gridcolor as well as hide spines.

    This is an alternative to hard-coding the values in the matplotlibrc file
    or having to remember the right syntax to do this repeatedly and verbosely.

    Args:
        gridcolor (string): Hex code to color grid
        trbl_axis ((Bool,Bool,Bool,Bool)): Which axes to color
        grid ((Bool, Bool)): Whether to display vertical or horizontal grid
    """
    ax = kwargs.get('ax', None)
    gridcolor = kwargs.get('gridcolor', '#dddddd')
    trbl_axis = kwargs.get('trbl_axis', (False, False, False, False))
    grid = kwargs.get('grid', (False, True))

    top, right, bottom, left = trbl_axis
    if not right:
        spine_color(ax, 'right', 'none')
    if not top:
        spine_color(ax, 'top', 'none')
    if not bottom:
        spine_color(ax, 'bottom', 'none')
    if not left:
        spine_color(ax, 'left', 'none')

    vert, hor = grid
    if not vert:
        grid_color(ax, 'vertical', 'none')
    else:
        grid_color(ax, 'vertical', gridcolor)

    if not hor:
        grid_color(ax, 'horizontal', 'none')
    else:
        grid_color(ax, 'horizontal', gridcolor)
