"""
Example Measurement Workflow

Demonstrates the public measurement workflow without
including application-specific protocol information.
"""

from connection import connect_ad3, disconnect_ad3
from measurement_manager import MeasurementManager


def run_example():
    device = None

    try:
        device = connect_ad3()

        manager = MeasurementManager()
        manager.configure(device)

        ch1 = manager.measure_channel(device, 1)
        ch2 = manager.measure_channel(device, 2)

        print("Channel 1:", ch1)
        print("Channel 2:", ch2)

        delay = manager.measure_delay(device)

        print("Time delay (us):", delay)

    finally:
        if device is not None:
           disconnect_ad3(device)


if __name__ == "__main__":
    run_example()