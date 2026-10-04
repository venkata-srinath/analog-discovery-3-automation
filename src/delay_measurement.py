"""
Time Delay Measurement Module

Measures the time difference between corresponding rising
edges of two sampled waveforms.
"""

import numpy as np


def measure_delay(ch1_edges,
                  ch2_edges,
                  sample_rate,
                  min_delay_us=0.0,
                  max_delay_us=None):
    """
    Measure time delay between two channels.

    Parameters:
        ch1_edges    : Rising-edge positions for channel 1
        ch2_edges    : Rising-edge positions for channel 2
        sample_rate  : Sampling rate in samples/second
        min_delay_us : Minimum accepted delay in microseconds
        max_delay_us : Maximum accepted delay in microseconds.
                       None disables the upper limit.

    Returns:
        Median delay in microseconds, or None if no valid
        corresponding edges are found.
    """

    if sample_rate <= 0:
        return None

    if ch1_edges is None or ch2_edges is None:
        return None

    if len(ch1_edges) == 0 or len(ch2_edges) == 0:
        return None

    min_delay_samples = (
        float(min_delay_us) *
        sample_rate /
        1000000.0
    )

    if max_delay_us is not None:
        max_delay_samples = (
            float(max_delay_us) *
            sample_rate /
            1000000.0
        )
    else:
        max_delay_samples = None

    delays = []

    for edge1 in ch1_edges:

        differences = np.asarray(ch2_edges) - edge1

        valid = differences[
            differences >= min_delay_samples
        ]

        if max_delay_samples is not None:
            valid = valid[
                valid <= max_delay_samples
            ]

        if len(valid) > 0:
            delays.append(valid[0])

    if len(delays) == 0:
        return None

    delay_samples = np.median(delays)

    delay_us = (
        float(delay_samples) /
        float(sample_rate) *
        1000000.0
    )

    return float(delay_us)