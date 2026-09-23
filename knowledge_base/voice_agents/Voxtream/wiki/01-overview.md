> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Overview
**In one sentence:** VoXtream2 is a zero-shot full-stream text-to-speech model with dynamic speaking-rate control that can be updated mid-utterance on the fly.
## Key points
- VoXtream2 is a zero-shot full-stream TTS model with dynamic speaking-rate control updatable mid-utterance on the fly (01-overview.md:14).
- Dynamic speed control uses distribution matching and classifier-free guidance for fine-grained speaking-rate adjustment during generation (01-overview.md:24).
- Streaming performance is 4x faster than real-time with 74 ms first-packet latency in full-stream on a consumer GPU (01-overview.md:25).
- Translingual capability is enabled by prompt text masking supporting acoustic prompts in any language (01-overview.md:26).
- Inputs are a 3–10 s prompt-audio file (max 20 s, longer trimmed) plus text (max 1000 chars, longer trimmed) with optional target speaking rate in syllables per second (01-overview.md:70-72).
- The model requires 2.2 Gb VRAM (+2 Gb with speech enhancement), caps generation at 1 minute, and was tested on Ubuntu 22.04 / CUDA 12 / PyTorch 2.4 (01-overview.md:75-77).
- Interfaces cover output-streaming and full-streaming CLI (`voxtream`), Python API (`SpeechGenerator.generate_stream`), Gradio demo (`voxtream-app`), websocket server (`voxtream-server`), and benchmark (`voxtream-benchmark`) (01-overview.md:87-91,01-overview.md:143-158,01-overview.md:170-171,01-overview.md:179-180,01-overview.md:221).
---
## Key features
Verbatim feature list (01-overview.md:24-26):
- **Dynamic speed control**: Distribution matching and Classifier-free guidance allow for a fine-grained speaking rate control, which can be adjusted as the model generates speech.
- **Streaming performance**: Works **4x** times faster than real-time and achieves **74 ms** first packet latency in a full-stream on a consumer GPU.
- **Translingual capability**: Prompt text masking enables support of acoustic prompts in any language.

Recent updates (01-overview.md:32-38):
- `2026/04/30`: dynamic speaking-rate interactive demo (`voxtream-app`); cache reset in SynkAttention fixing noise from invalid prompt cache.
- `2026/04/08`: frame repeat counter (`frame_repeat_counter` in `SpeechGeneratorConfig`, recommended 12–25) reducing stuck-frame hallucinations.
- `2026/03`: VoXtream2 released; `2026/01`: VoXtream oral at ICASSP 2026; `2025/09`: VoXtream released on `voxtream` branch.

## Installation
eSpeak NG phonemizer prerequisite (01-overview.md:45-56):
```bash
# For Debian-like distribution (e.g. Ubuntu, Mint, etc.)
apt-get install espeak-ng

# For RedHat-like distribution (e.g. CentOS, Fedora, etc.)
yum install espeak-ng

# For MacOS
brew install espeak-ng
```
Pip package (01-overview.md:63-64):
```bash
pip install "voxtream>=0.2.3"
```

## Usage inputs and constraints
Input contract and runtime notes (01-overview.md:70-79):

| Parameter | Constraint |
|---|---|
| `prompt-audio` / `prompt_audio_path` | 3–10 s target voice; max 20 s, longer trimmed |
| `text` | max 1000 chars, longer trimmed |
| `speaking rate` (`--spk-rate` / `speaking_rate`) | optional, syllables per second, e.g. `2.0` |
| VRAM | 2.2 Gb (+2 Gb with speech enhancement) |
| Max generation length | 1 minute |
| Tested stack | Ubuntu 22.04, CUDA 12, PyTorch 2.4 |
| First run | downloads weights, warms up model graph |
| CUDAGraphs issues | see `https://github.com/herimor/voxtream/issues/8` |

## Command-line interface
Output streaming (01-overview.md:87-91):
```bash
voxtream \
    --prompt-audio assets/audio/english_male.wav \
    --text "In general, some method is then needed to evaluate each approximation." \
    --output "output_stream.wav"
```
Full streaming, slow speech at 2 syllables/second (01-overview.md:95-101):
```bash
voxtream \
    --prompt-audio assets/audio/english_female.wav \
    --text "Staff do not always do enough to prevent violence." \
    --output "full_stream_2sps.wav" \
    --full-stream \
    --spk-rate 2.0
```
Acoustic prompt enhancement (01-overview.md:105-110):
```bash
voxtream \
    --prompt-audio assets/test/english_male.wav \
    --text "In general, however, some method is then needed to evaluate each approximation." \
    --output "output_enhanced.wav" \
    --prompt-enhancement
```

| CLI flag | Meaning |
|---|---|
| `--prompt-audio` | path to prompt wav |
| `--text` | text to synthesize |
| `--output` | output wav path |
| `--full-stream` | enable full streaming mode |
| `--spk-rate` | target speaking rate, e.g. `2.0` |
| `--prompt-enhancement` | enable acoustic prompt enhancement |

## Python API
Verbatim usage pattern (01-overview.md:117-162):
```python
import json
from itertools import repeat
from pathlib import Path

import numpy as np
import soundfile as sf

from voxtream.utils.generator import (
    set_seed,
    text_generator,
)
from voxtream.generator import SpeechGenerator, SpeechGeneratorConfig


set_seed()
with open('configs/generator.json') as f:
    config = SpeechGeneratorConfig(**json.load(f))

with open('configs/speaking_rate.json') as f:
    spk_rate_config = json.load(f)

speech_generator = SpeechGenerator(config, spk_rate_config)



# Output streaming, no speaking rate control
speech_stream = speech_generator.generate_stream(
    prompt_audio_path=Path('assets/audio/english_male.wav'),
    text="In general, however, some method is then needed to evaluate each approximation.",
)

audio_frames = [audio_frame for audio_frame, _ in speech_stream]
sf.write('output_stream.wav', np.concatenate(audio_frames), config.mimi_sr)



# Full streaming & fixed speaking rate control (2 syllables per second)
speech_stream = speech_generator.generate_stream(
    prompt_audio_path=Path('assets/audio/english_female.wav'),
    text=text_generator("Staff do not always do enough to prevent violence."),
    speaking_rate=repeat(2.0),
)

audio_frames = [audio_frame for audio_frame, _ in speech_stream]
sf.write('full_stream_2sps.wav', np.concatenate(audio_frames), config.mimi_sr)
```

Exact parameter names: `SpeechGenerator(config, spk_rate_config)`, `generate_stream(prompt_audio_path=..., text=..., speaking_rate=...)`, `text_generator(...)`, `set_seed()`, `config.mimi_sr` (01-overview.md:124-161).

## Demo, server, and evaluation
Gradio demo (01-overview.md:170-171):
```bash
voxtream-app
```
Websocket server and client (01-overview.md:179-187):
```bash
voxtream-server
```
```bash
python voxtream/client.py
```
It sends a path to the audio prompt and a text to the server and immediately plays audio from the output stream (01-overview.md:187). Evaluation metrics reproduction is documented at `voxtream/utils/test/README.md` (01-overview.md:193).

## Training
Build container (01-overview.md:200-202):
```bash
docker-compose -f .devcontainer/docker-compose.yaml build voxtream
```
Run training with `train.py`; specify container-visible `GPU_IDS` and `batch_size` (default 64, tested on H200; 12 fits RTX3090); dataset auto-downloads to HF cache (80 Gb, loaded to RAM, ~80 Gb RAM per GPU); results in `./experiments` (01-overview.md:204).
```bash
GPU_IDS=0,1 docker-compose -f .devcontainer/docker-compose.yaml run voxtream python voxtream/train.py batch_size=12
```
Custom dataset preparation: `voxtream/utils/dataset/README.md` (01-overview.md:215).

## Benchmark
Run `voxtream-benchmark` for real-time factor (RTF) and first-packet latency (FPL); `--compile` flag compiles the model for faster inference at the cost of initial compilation time (01-overview.md:221). Results table (01-overview.md:223-226):

| Device  | Compiled           | FPL, ms | RTF   |
| :-:     | :-:                | :-:     | :-:   |
| RTX3090 |                    | 74      | 0.256 |
| RTX3090 | :heavy_check_mark: | 63      | 0.173 |

Open item: add finetuning instructions (01-overview.md:232). Misuse disclaimer prohibits generating someone's speech without consent (01-overview.md:237). No truncated files were noted in the chunk.

**Covers:** README.md (VoXtream2 model statement, key features, updates, install, usage, training, benchmark, TODO, disclaimer); referenced entry points `voxtream`, `voxtream-app`, `voxtream-server`, `voxtream-benchmark`, `voxtream/client.py`, `voxtream/train.py`, `voxtream/generator.py`, `voxtream/utils/generator.py`, `configs/generator.json`, `configs/speaking_rate.json`, `assets/audio/`, `voxtream/utils/test/README.md`, `voxtream/utils/dataset/README.md`, `.devcontainer/docker-compose.yaml`
