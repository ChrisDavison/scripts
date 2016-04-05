import pandas as pd
import numpy as np
import scipy.fftpack as sfft


def high_pass(signal, fs, fc):
    """1st order high pass filter.

    Args:
        signal ([float]): signal to filter
        fs (float): sampling frequency
        fc (float): cutoff frequency
    """
    RC = 1.0 / (2 * np.pi * fc)
    alpha = (RC * fs) / (RC * fs + 1)

    filtered = np.zeros(len(signal))
    yk = float(signal[0])
    for k in range(1, len(signal)):  # We need a previous point
        yk = alpha * (float(signal[k]) + float(yk) - float(signal[k-1]))
        filtered[k] = yk
    # First element is empty since we start at index 1
    return pd.Series(filtered[1:])


def low_pass(signal, fs, fc):
    """1st order low pass filter.

    Args:
        signal ([float]): signal to filter
        fs (float): sampling frequency
        fc (float): cutoff frequency
    """
    alpha = 1 - np.exp(-fc / fs)

    filtered = np.zeros_like(signal)
    yk = float(signal[0])
    for k in range(len(signal)):
        yk += alpha * (float(signal[k]) - float(yk))
        filtered[k] = yk
    return pd.Series(filtered)


def band_pass(signal, fs, fcl, fch, **kwargs):
    """1st order band pass filter.

    Args:
        signal ([float]): signal to filter
        fs (float): sampling frequency
        fcl (float): lower cutoff frequency
        fch (float): higher cutoff frequency

    Kwargs:
        hard (bool): hard-bandpass, [default: False]
    """
    hard = kwargs.get('hard', False)
    out = []
    if not hard:  # Soft bandpass
        hp = high_pass(signal, fs, fch)
        out = low_pass(hp, fs, fcl)
    else:
        X = abs(sfft.fft(signal))
        freqs = sfft.fftfreq(len(signal), 1 / fs)
        N = int(len(freqs)/2)

        X = X[:N]
        freqs = freqs[:N]

        for i, freq in enumerate(freqs):
            if freq < fcl or freq > fch:
                X[i] = 0

        filtered = sfft.ifft(X)
        filtered[:3] = 0
        filtered[-2:] = 0
        out = filtered
    return pd.Series(out)
