"""
Analog Discovery 3 Connection Module

Handles loading the Digilent WaveForms SDK and
opening/closing an Analog Discovery 3 device.
"""

import ctypes
import platform


# ============================================================
# Load WaveForms SDK
# ============================================================

if platform.system() == "Windows":
    dwf = ctypes.cdll.LoadLibrary("dwf.dll")
else:
    dwf = ctypes.cdll.LoadLibrary("libdwf.so")


# ============================================================
# Connect to AD3
# ============================================================

def connect_ad3():
    """
    Open the first available Analog Discovery device.

    Returns:
        Device handle.
    """

    device = ctypes.c_int()

    result = dwf.FDwfDeviceOpen(
        ctypes.c_int(-1),
        ctypes.byref(device)
    )

    if result == 0:
        raise RuntimeError("Unable to open Analog Discovery device")

    return device


# ============================================================
# Disconnect AD3
# ============================================================

def disconnect_ad3(device):
    """
    Close the Analog Discovery device.
    """

    dwf.FDwfDeviceClose(device)