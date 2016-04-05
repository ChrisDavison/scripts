import numpy as np


def integral(signal, dt, window):
    """
    Get the integral of the signal.
    """
    integratedSignal = []
    a = 0
    b = a + window
    while b < len(signal):
        value = 0
        for i in range(a, b):
            value += float(signal[i]) * dt
        integratedSignal.append(value)
        a += 1
        b += 1
    return integratedSignal


def derivate(signal, dt, absolute=False):
    """
    Get the derivate of the signal.
    """
    d = []
    for i in range(1, len(signal)):
        val = (float(signal[i]) - float(signal[i-1])) / dt
        if absolute:
            val = np.abs(val)
        d.append(val)
    return d
