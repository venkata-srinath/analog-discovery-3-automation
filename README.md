# Analog Discovery 3 Automation & Measurement System

## Project Overview

A Python-based automated signal measurement system using the
**Analog Discovery 3 (AD3)** and **Digilent WaveForms SDK**.

The system provides a modular software layer for waveform
generation, signal acquisition, signal processing, and automated
measurement of electrical signals.

The project was developed with integration into a higher-level
test application in mind, including LabVIEW-based automation.

---

## Key Features

- Analog Discovery 3 device initialization and control
- Dual-channel waveform acquisition
- Waveform generation using AD3 WaveGen
- Frequency measurement
- Period measurement
- Peak-to-peak amplitude measurement
- CH1–CH2 time-delay measurement
- Rising-edge detection
- Sub-sample edge interpolation
- Multiple measurement cycles
- Median-based result processing
- Acquisition timeout handling
- Modular Python architecture
- WaveForms SDK integration using `ctypes`

---

## System Architecture

```text
             Test / Automation Application
                         |
                         v
                Python Measurement Layer
                         |
          +--------------+--------------+
          |                             |
          v                             v
   Waveform Generation          Waveform Acquisition
          |                             |
          v                             v
      AD3 WaveGen                 AD3 Oscilloscope
                                        |
                         +--------------+--------------+
                         |              |              |
                         v              v              v
                    Edge Detection   Frequency    Amplitude
                         |
                         v
                  Time-Delay Analysis
                         |
                         v
                  Measurement Results