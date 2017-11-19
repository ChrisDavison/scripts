import scipy.fftpack as sfft


def easy_fft(data, fs):
    X = abs(sfft.fft(data)) / len(X)
    f = sfft.fftfreq(len(X), 1/fs)
    N = int(len(X) / 2)
    return X[:N], f[:N]
