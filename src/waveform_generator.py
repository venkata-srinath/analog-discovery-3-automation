"""
Analog Discovery 3 Waveform Generator

Controls WaveGen outputs using the Digilent WaveForms SDK.
"""

import ctypes

from connection import dwf
from dwfconstants import (
    funcSine,
    funcSquare,
    funcTriangle,
    funcPulse,
    funcRampUp,
    funcRampDown,
    AnalogOutNodeCarrier,
)


# ============================================================
# Waveform selection
# ============================================================

WAVEFORMS = {
    "sine": funcSine,
    "square": funcSquare,
    "triangle": funcTriangle,
    "pulse": funcPulse,
    "ramp_up": funcRampUp,
    "ramp_down": funcRampDown,
}


# ============================================================
# Generate waveform
# ============================================================

def generate_waveform(device,
                      channel,
                      waveform,
                      frequency,
                      amplitude_vpp):
    """
    Generate a waveform on an AD3 WaveGen channel.

    Parameters:
        device        : AD3 device handle
        channel       : WaveGen channel, 1 or 2
        waveform      : Waveform name
        frequency     : Frequency in Hz
        amplitude_vpp : Peak-to-peak amplitude in volts

    Returns:
        Dictionary containing waveform settings.
    """

    if channel not in (1, 2):
        raise ValueError("Channel must be 1 or 2")

    if waveform not in WAVEFORMS:
        raise ValueError("Unsupported waveform type")

    if frequency <= 0:
        raise ValueError("Frequency must be greater than zero")

    if amplitude_vpp <= 0:
        raise ValueError("Amplitude must be greater than zero")

    channel_index = channel - 1

    # DWF amplitude represents peak amplitude.
    amplitude = amplitude_vpp / 2.0

    result = dwf.FDwfAnalogOutNodeFunctionSet(
        device,
        ctypes.c_int(channel_index),
        AnalogOutNodeCarrier,
        WAVEFORMS[waveform]
    )

    if result == 0:
        raise RuntimeError("Failed to configure waveform type")

    result = dwf.FDwfAnalogOutNodeFrequencySet(
        device,
        ctypes.c_int(channel_index),
        AnalogOutNodeCarrier,
        ctypes.c_double(frequency)
    )

    if result == 0:
        raise RuntimeError("Failed to configure frequency")

    result = dwf.FDwfAnalogOutNodeAmplitudeSet(
        device,
        ctypes.c_int(channel_index),
        AnalogOutNodeCarrier,
        ctypes.c_double(amplitude)
    )

    if result == 0:
        raise RuntimeError("Failed to configure amplitude")

    result = dwf.FDwfAnalogOutNodeEnableSet(
        device,
        ctypes.c_int(channel_index),
        AnalogOutNodeCarrier,
        1
    )

    if result == 0:
        raise RuntimeError("Failed to enable output")

    result = dwf.FDwfAnalogOutConfigure(
        device,
        ctypes.c_int(channel_index),
        1
    )

    if result == 0:
        raise RuntimeError("Failed to start waveform generation")

    return {
        "channel": channel,
        "waveform": waveform,
        "frequency_hz": frequency,
        "amplitude_vpp": amplitude_vpp,
    }