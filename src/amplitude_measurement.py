"""
Amplitude Measurement Module

Calculates peak-to-peak amplitude from sampled waveform data.
"""

import numpy as np


def measure_amplitude(signal):
    """
    Calculate peak-to-peak amplitude.

    Parameters:
        signal : Sampled waveform data

    Returns:
        Peak-to-peak amplitude.
    """

    signal = np.asarray(signal)

    if signal.size == 0:
        return 0.0

    maximum = np.max(signal)
    minimum = np.min(signal)

    return float(maximum - minimum)