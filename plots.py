import pandas
import scipy.fftpack
import matplotlib.pyplot as plt

sfft = scipy.fftpack

pd = pandas

def plot_fft(window, fs, axis, FFTLEN=512, label=None):
    spec = pd.Series(sfft.fft(window, FFTLEN)).abs()
    freqs = sfft.fftfreq(len(spec), 1.0/fs)
    N = int(len(spec) / 2)
    axis.plot(freqs[:N], spec[:N], label=label)
    return axis, spec


def rotate_xaxis_labels(ax, rotation):
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=rotation)
