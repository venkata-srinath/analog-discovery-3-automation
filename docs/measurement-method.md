# Measurement Methods

## 1. Waveform Acquisition

The Analog Discovery 3 is used to acquire sampled waveform data
from multiple input channels.

The acquisition layer configures:

- Sampling rate
- Input channels
- Input voltage range
- Buffer size
- Trigger conditions

The acquired samples are passed to the signal-processing layer.

---

## 2. Rising-Edge Detection

Rising edges are detected by identifying transitions where the
sampled waveform crosses a selected threshold from below to above.

For improved timing resolution, linear interpolation is applied
between the two samples surrounding the threshold crossing.

```text
Sample i              Sample i+1
   ●----------------------●
    \                    /
     \                  /
      \------●---------/
             ↑
         Threshold