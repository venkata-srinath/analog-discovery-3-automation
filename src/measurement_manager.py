"""
Measurement Manager

Coordinates waveform acquisition and signal measurements
from an Analog Discovery 3 device.
"""

import numpy as np

from acquisition import configure_scope, acquire_waveform
from edge_detection import find_rising_edges
from frequency_measurement import measure_frequency
from amplitude_measurement import measure_amplitude
from delay_measurement import measure_delay as calculate_delay


class MeasurementManager(object):
    """
    Coordinates AD3 acquisition and signal measurements.
    """

    def __init__(self,
                 sample_rate=200000,
                 buffer_size=8192,
                 input_range=5.0,
                 measurements=5):

        self.sample_rate = sample_rate
        self.buffer_size = buffer_size
        self.input_range = input_range
        self.measurements = measurements

    # ========================================================
    # Configure
    # ========================================================

    def configure(self, device):
        """
        Configure the AD3 analog input channels.
        """

        configure_scope(
            device,
            sample_rate=self.sample_rate,
            buffer_size=self.buffer_size,
            input_range=self.input_range
        )

    # ========================================================
    # Measure Channel
    # ========================================================

    def measure_channel(self, device, channel):
        """
        Measure frequency, period and amplitude
        for one channel.

        Parameters:
            device  : AD3 device handle
            channel : 1 or 2

        Returns:
            Dictionary containing measurement results.
        """

        if channel not in (1, 2):
            raise ValueError("Channel must be 1 or 2")

        frequencies = []
        periods = []
        amplitudes = []

        for _ in range(self.measurements):

            ch1, ch2 = acquire_waveform(
                device,
                buffer_size=self.buffer_size
            )

            signal = ch1 if channel == 1 else ch2

            edges = find_rising_edges(signal)

            frequency, period = measure_frequency(
                edges,
                self.sample_rate
            )

            amplitude = measure_amplitude(signal)

            if frequency is not None:
                frequencies.append(frequency)

            if period is not None:
                periods.append(period)

            amplitudes.append(amplitude)

        return {
            "frequency_hz": (
                float(np.median(frequencies))
                if frequencies else None
            ),
            "period_seconds": (
                float(np.median(periods))
                if periods else None
            ),
            "amplitude_vpp": (
                float(np.median(amplitudes))
                if amplitudes else None
            )
        }

    # ========================================================
    # Measure Delay
    # ========================================================

    def measure_delay(self, device):
        """
        Measure the time delay between CH1 and CH2.

        Returns:
            Median time delay in microseconds, or None.
        """

        delays = []

        for _ in range(self.measurements):

            ch1, ch2 = acquire_waveform(
                device,
                buffer_size=self.buffer_size
            )

            ch1_edges = find_rising_edges(ch1)
            ch2_edges = find_rising_edges(ch2)

            delay = calculate_delay(
                ch1_edges,
                ch2_edges,
                self.sample_rate
            )

            if delay is not None:
                delays.append(delay)

        if not delays:
            return None

        return float(np.median(delays))