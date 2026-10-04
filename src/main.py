"""
AD3 Automation - Main Application

Demonstrates the high-level measurement workflow for
an Analog Discovery 3 based test and measurement system.
"""

from connection import connect_ad3, disconnect_ad3
from measurement_manager import MeasurementManager


def main():
    """
    Main application entry point.
    """

    device = None

    try:
        # ----------------------------------------------------
        # Connect to Analog Discovery 3
        # ----------------------------------------------------

        device = connect_ad3()

        # ----------------------------------------------------
        # Initialize measurement manager
        # ----------------------------------------------------

        manager = MeasurementManager()

        # ----------------------------------------------------
        # Configure acquisition
        # ----------------------------------------------------

        manager.configure(device)

        # ----------------------------------------------------
        # Example channel measurements
        # ----------------------------------------------------

        ch1_result = manager.measure_channel(
            device,
            channel=1
        )

        ch2_result = manager.measure_channel(
            device,
            channel=2
        )

        # ----------------------------------------------------
        # Display results
        # ----------------------------------------------------

        print("CH1:", ch1_result)
        print("CH2:", ch2_result)

    except Exception as error:

        print("Measurement error:", error)

    finally:

        if device is not None:
            disconnect_ad3(device)


if __name__ == "__main__":
    main()