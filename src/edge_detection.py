"""
Edge Detection Module

Detects rising edges in sampled waveform data using
threshold crossing and linear interpolation.
"""

import numpy as np


def find_rising_edges(signal,
                      threshold=None,
                      min_distance=20):
    """
    Detect rising edges in a waveform.

    Parameters:
        signal       : 1-D waveform array
        threshold    : Detection threshold. If None, the
                       midpoint of the signal range is used.
        min_distance : Minimum sample distance between edges

    Returns:
        NumPy array containing interpolated edge positions.
    """

    signal = np.asarray(signal)

    if signal.size < 2:
        return np.array([], dtype=np.float64)

    if threshold is None:
        threshold = (
            np.min(signal) + np.max(signal)
        ) / 2.0

    edges = []

    last_edge = -min_distance

    for i in range(len(signal) - 1):

        if signal[i] < threshold <= signal[i + 1]:

            if i - last_edge < min_distance:
                continue

            y1 = signal[i]
            y2 = signal[i + 1]

            if y2 != y1:
                fraction = (
                    threshold - y1
                ) / (y2 - y1)

                edge_position = i + fraction
            else:
                edge_position = float(i)

            edges.append(edge_position)
            last_edge = i

    return np.asarray(edges, dtype=np.float64)