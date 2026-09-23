[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Table 11: Video-only model per-inference power
**In one sentence:** On the video-only model the AKD1000 reaches 14.55 it/s at 0.0165 mWh per inference, making it 4.9× more efficient than the same SNN on Pi CPU, 26× better than the Pi float-Keras baseline, and over 100× better than laptop GPU.
## Key points
- Video-only Akida backend: 14.55 it/s at 462.0 mWh per 5 min, i.e. 72.0 mWh attributable draw and 0.0165 mWh per inference.
- Same SNN on Pi CPU under the Akida backend (strongest CPU baseline): 15.55 it/s at 0.0810 mWh per inference, so the AKD1000 is 4.9× more energy-efficient per inference.
- Pi CPU Keras float baseline: 1.10 it/s at 0.4306 mWh per inference, a 26× gap versus the AKD1000.
- Laptop GPU Keras baseline: 2.54 it/s at 1.6913 mWh per inference, more than a 100× gap versus the AKD1000.
- Idle baselines adopted are 390 mWh / 5 min for the Pi and 1,280 mWh / 5 min for the GPU; Pi figures are total system draw (FNB58) while GPU figures are GPU-only draw via nvidia-smi normalised to a 5-minute window.
- The video-only pipeline uses 5 AKD1000 passes per inference: image encoder (75 NPs, 1 sequence), temporal encoder (41 NPs, 3 sequences), predictor head (2 NPs, 1 sequence).
- The audio-video extension (Table 12 preview) totals 22 passes per inference and raises Akida energy to 0.0894 mWh per inference at 2.61 it/s, still 37× less than laptop GPU but broadly comparable to the Pi-CPU Akida backend (0.0866 mWh/inf. at 13.36 it/s).
---
## Measurement setup and idle baselines
Idle baselines: Pi 390 mWh / 5 min, GPU 1,280 mWh / 5 min. Pi figures cover total system draw (FNB58). GPU figures cover GPU-only draw via nvidia-smi, normalised to a 5-minute window.

Scope caveat from the chunk:

> "scopes differ: the Pi figures cover total system draw, whereas the GPU figures cover only the GPU itself, with known precision limitations [39]. Both effects make the GPU comparison favourable to the GPU."

Idle details:
- CPU-backend idle draw on the Pi settled at approximately 390 mWh / 5 min, adopted as the baseline for inference-attributable consumption.
- Akida-backend idle draw is essentially identical (387.59 mWh), and the bare Pi with no script running drew 370.92 mWh.
- The GPU's idle draw alone was 1,280 mWh / 5 min, more than three times the Pi's total system draw.

The chunk states the most informative on-device comparison is the AKD1000 against the same SNN-converted model running on CPU under the Akida software backend (the strongest CPU baseline). The Pi-CPU Keras backend, which executes the float Keras model rather than the SNN, is reported alongside for completeness but is the weakest competitor. Comparing AKD1000 against laptop-GPU Keras measures the chip's standing against a typical accelerated-computing baseline.

## Table 11 results
TABLE 11. Video-only model: per-inference power consumption across backends.

| Backend | it/s | mWh@5 min | ∆mWh | mWh/inf. |
|---|---|---:|---:|---:|
| Pi + AKD1000 (Akida) | 14.55 | 462.0 | 72.0 | 0.0165 |
| Pi + CPU (Akida) | 15.55 | 768.0 | 378.0 | 0.0810 |
| Pi + CPU (Keras) | 1.10 | 531.9 | 141.9 | 0.4306 |
| Laptop + GPU (Keras) | 2.54 | 2,569.6 | 1,289.6 | 1.6913 |

Efficiency ratios stated in the chunk:
- Against the same model on CPU under the Akida backend (0.0810 mWh/inf., 15.55 it/s) the AKD1000 is 4.9× more energy-efficient per inference.
- Against the Pi-CPU Keras float baseline the gap widens to 26×.
- Against the laptop GPU it widens further to over 100×.

## Pipeline composition
The video-only pipeline consists of an image encoder (75 NPs, 1 sequence), a temporal encoder (41 NPs, 3 sequences) and a predictor head (2 NPs, 1 sequence), for a total of 5 AKD1000 passes per inference. The Akida backend reaches 14.55 it/s at 0.0165 mWh/inf.

## Audio-video extension (Table 12 preview in chunk)
The audio-video pipeline extends the video-only pipeline with a spectrogram encoder (348 NPs, 9 sequences) and a larger predictor head (2 NPs, 1 sequence), for a total of 22 passes per inference. Per-inference Akida energy rises to 0.0894 mWh, broadly comparable to the Pi-CPU Akida backend (0.0866 mWh/inf.) but at lower throughput (2.61 vs. 13.36 it/s). Against the laptop GPU the AKD1000 still consumes 37× less energy per inference. The chunk attributes the lost per-inference advantage on the audio-video model to a hardware-mapping behaviour of the Akida toolchain that is independent of architecture, analysed in Appendix A. Even so, 2.61 it/s is stated to be comfortably above real-time for command recognition.

**Covers:** On-board power measurements and accuracy-vs-cost Pareto analysis (Table 11 video-only per-inference power)
