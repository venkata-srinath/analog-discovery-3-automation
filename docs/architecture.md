# System Architecture

## Overview

The Analog Discovery 3 automation system is organized into
separate hardware-interface, acquisition, signal-processing,
and measurement layers.

## Architecture

```text
+---------------------------+
|   Test / Automation App   |
+-------------+-------------+
              |
              v
+---------------------------+
|      Python Interface     |
+-------------+-------------+
              |
      +-------+-------+
      |               |
      v               v
+-----------+   +-------------+
| WaveGen   |   | Acquisition |
+-----------+   +------+------+
                      |
                      v
               +-------------+
               | AD3 Device  |
               +------+------+
                      |
          +-----------+-----------+
          |           |           |
          v           v           v
       CH1/CH2    Edge Detection  Waveform
       Samples                    Data
          |           |
          +-----+-----+
                |
                v
      +----------------------+
      | Measurement Engine   |
      +----------+-----------+
                 |
        +--------+--------+
        |        |        |
        v        v        v
    Frequency Amplitude Delay
        |        |        |
        +--------+--------+
                 |
                 v
       Measurement Results