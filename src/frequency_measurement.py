"""
Frequency Measurement Module

Calculates waveform frequency and period from detected
rising-edge positions.
"""


def measure_frequency(edges, sample_rate):
    """
    Calculate frequency and period from rising edges.

    Parameters:
        edges       : Rising-edge sample positions
        sample_rate : Sampling rate in samples/second

    Returns:
        (frequency_hz, period_seconds)

        Returns (None, None) if fewer than two edges
        are available.
    """

    if edges is None or len(edges) < 2:
        return None, None

    period_samples = edges[1] - edges[0]

    if period_samples <= 0 or sample_rate <= 0:
        return None, None

    period_seconds = (
        float(period_samples) / float(sample_rate)
    )

    frequency_hz = 1.0 / period_seconds

    return frequency_hz, period_seconds