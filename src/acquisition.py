"""
Analog Discovery 3 Waveform Acquisition Module

Configures the AD3 oscilloscope and acquires waveform data
from one or two input channels using the WaveForms SDK.
"""

import ctypes
import time
import numpy as np

from connection import dwf


# ============================================================
# Configure Scope
# ============================================================

def configure_scope(device,
                    sample_rate=200000,
                    buffer_size=8192,
                    input_range=5.0):
    """
    Configure AD3 analog input channels.

    Parameters:
        device       : AD3 device handle
        sample_rate  : Sampling rate in samples/second
        buffer_size  : Number of samples
        input_range  : Input voltage range

    Returns:
        None
    """

    dwf.FDwfAnalogInConfigure(
        device,
        ctypes.c_int(0),
        ctypes.c_int(0)
    )

    for channel in (0, 1):

        dwf.FDwfAnalogInChannelEnableSet(
            device,
            ctypes.c_int(channel),
            ctypes.c_int(1)
        )

        dwf.FDwfAnalogInChannelRangeSet(
            device,
            ctypes.c_int(channel),
            ctypes.c_double(input_range)
        )

    dwf.FDwfAnalogInFrequencySet(
        device,
        ctypes.c_double(sample_rate)
    )

    dwf.FDwfAnalogInBufferSizeSet(
        device,
        ctypes.c_int(buffer_size)
    )


# ============================================================
# Configure Trigger
# ============================================================

def configure_trigger(device,
                      level=0.0,
                      channel=0):
    """
    Configure a simple rising-edge trigger.

    Parameters:
        device  : AD3 device handle
        level   : Trigger voltage level
        channel : Trigger channel index
    """

    dwf.FDwfAnalogInTriggerSourceSet(
        device,
        2
    )

    dwf.FDwfAnalogInTriggerChannelSet(
        device,
        ctypes.c_int(channel)
    )

    dwf.FDwfAnalogInTriggerLevelSet(
        device,
        ctypes.c_double(level)
    )


# ============================================================
# Acquire Waveform
# ============================================================

def acquire_waveform(device,
                     buffer_size=8192,
                     timeout=2.0):
    """
    Acquire waveform data from CH1 and CH2.

    Returns:
        (ch1, ch2)

    Both values are NumPy arrays.
    """

    dwf.FDwfAnalogInConfigure(
        device,
        ctypes.c_int(1),
        ctypes.c_int(1)
    )

    start_time = time.time()

    while True:

        status = ctypes.c_int()

        dwf.FDwfAnalogInStatus(
            device,
            ctypes.c_int(1),
            ctypes.byref(status)
        )

        if status.value == 2:
            break

        if time.time() - start_time > timeout:
            raise RuntimeError("Waveform acquisition timeout")

        time.sleep(0.01)

    ch1 = np.zeros(buffer_size, dtype=np.float64)
    ch2 = np.zeros(buffer_size, dtype=np.float64)

    dwf.FDwfAnalogInStatusData(
        device,
        ctypes.c_int(0),
        ch1.ctypes.data_as(ctypes.POINTER(ctypes.c_double)),
        ctypes.c_int(buffer_size)
    )

    dwf.FDwfAnalogInStatusData(
        device,
        ctypes.c_int(1),
        ch2.ctypes.data_as(ctypes.POINTER(ctypes.c_double)),
        ctypes.c_int(buffer_size)
    )

    return ch1, ch2