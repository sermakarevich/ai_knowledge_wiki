PDF: https://github.com/herimor/voxtream (no source.pdf fetched; see Source URL below)
# herimor/voxtream
Source: https://github.com/herimor/voxtream
Kind: repo
Fetched: 2026-09-22T14:54:28.532922+00:00
Tool: git-clone

# herimor/voxtream

Commit: 8ec2d62159dae4716ae7058827244a962d40603c

## README

# VoXtream2: Full-stream TTS with dynamic speaking rate control

[![arXiv](https://img.shields.io/badge/arXiv-Paper-<COLOR>.svg)](https://arxiv.org/pdf/2603.13518)
[![Model](https://img.shields.io/badge/%F0%9F%A4%97%20HuggingFace-Model-yellow)](https://huggingface.co/herimor/voxtream2)
<!-- [![Demo page](https://img.shields.io/badge/VoXtream2-Demo_page-red)](https://herimor.github.io/voxtream2) -->
<!-- [![Live demo](https://img.shields.io/badge/%F0%9F%A4%97%20HuggingFace-Live_demo-yellow)](https://huggingface.co/spaces/herimor/voxtream2) -->

We present VoXtream2, a zero-shot full-stream TTS model with dynamic speaking-rate control that can be updated mid-utterance on the fly.

For audio examples, see our [demo page](https://herimor.github.io/voxtream2).

Try VoXtream2 in your browser on HuggingFace 🤗 [space](https://huggingface.co/spaces/herimor/voxtream2).



## Key features

- **Dynamic speed control**: Distribution matching and Classifier-free guidance allow for a fine-grained speaking rate control, which can be adjusted as the model generates speech.
- **Streaming performance**: Works **4x** times faster than real-time and achieves **74 ms** first packet latency in a full-stream on a consumer GPU.
- **Translingual capability**: Prompt text masking enables support of acoustic prompts in any language.



## Updates

- `2026/04/30`:
    - Added a dynamic speaking rate control interactive demo. You can now adjust the speaking rate as the model produces speech in real-time. Run `voxtream-app` locally after installing the package or check our HuggingFace [space](https://huggingface.co/spaces/herimor/voxtream2).
    - Added cache reset in SynkAttention. Fixed the bug that caused the model to generate noise by relying on an invalid prompt cache.
- `2026/04/08`: Added a frame repeat counter. Reduces hallucinations caused by models getting stuck in the same frame. Controlled by the `frame_repeat_counter` parameter in `SpeechGeneratorConfig`. Recommended value (12-25), lower values for stricter control.
- `2026/03`: We released VoXtream2.
- `2026/01`: VoXtream is accepted for an oral presentation at ICASSP 2026.
- `2025/09`: We released VoXtream. Now available at [voxtream](https://github.com/herimor/voxtream/tree/voxtream) branch.



### eSpeak NG phonemizer

```bash


# For Debian-like distribution (e.g. Ubuntu, Mint, etc.)
apt-get install espeak-ng


# For RedHat-like distribution (e.g. CentOS, Fedora, etc.) 
yum install espeak-ng


# For MacOS
brew install espeak-ng
```



### Pip package
```bash
pip install "voxtream>=0.2.3"
```



## Usage

* Prompt audio: a file containing 3-10 seconds of the target voice. The maximum supported length is 20 seconds (longer audio will be trimmed).
* Text: What you want the model to say. The maximum supported length is 1000 characters (longer text will be trimmed).
* Speaking rate (optional): target speaking rate in syllables per second.

**Notes**: 
* The model was tested on Ubuntu 22.04, CUDA 12 and PyTorch 2.4.
* The model requires 2.2Gb of VRAM (enabling speech enhancement adds 2Gb).
* Maximum generation length is limited to 1 minute.
* The initial run may take a bit longer to download model weights and warmup model graph.
* If you experience problems with CUDAGraphs please check this [issue](https://github.com/herimor/voxtream/issues/8).



### Command line

#### Output streaming
```bash
voxtream \
    --prompt-audio assets/audio/english_male.wav \
    --text "In general, some method is then needed to evaluate each approximation." \
    --output "output_stream.wav"
```

#### Full streaming (slow speech, 2 syllables per second)
```bash
voxtream \
    --prompt-audio assets/audio/english_female.wav \
    --text "Staff do not always do enough to prevent violence." \
    --output "full_stream_2sps.wav" \
    --full-stream \
    --spk-rate 2.0
```

#### Acoustic prompt enhancement
```bash
voxtream \
    --prompt-audio assets/test/english_male.wav \
    --text "In general, however, some method is then needed to evaluate each approximation." \
    --output "output_enhanced.wav" \
    --prompt-enhancement
```



### Python API

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



### Gradio demo

To start a gradio web-demo run:
```bash
voxtream-app
```



### Websocket

To start a websocket server run:
```bash
voxtream-server
```

To send a request to the server run:
```bash
python voxtream/client.py
```

It sends a path to the audio prompt and a text to the server and immediately plays audio from the output stream.



### Evaluation

To reproduce evaluation metrics from the paper check [evaluation](voxtream/utils/test/README.md) section.



## Training

- Build the Docker container. If you have another version of Docker compose installed use `docker compose -f ...` instead.
```bash
docker-compose -f .devcontainer/docker-compose.yaml build voxtream
```

- Run training using the `train.py` script. You should specify GPU IDs that will be seen inside the container, ex. `GPU_IDS=0,1`. Specify the batch size according to your GPU. The default batch size is 64 (tested on H200), batch size 12 fits into RTX3090. The dataset will be downloaded automatically to the HF cache directory. Dataset size is 80Gb. The data will be loaded to RAM during training, make sure you can allocate ~80Gb of RAM per GPU. Results will be stored at the `./experiments` directory.

Example of running the training using 2 GPUs with batch size 32:
```bash
GPU_IDS=0,1 docker-compose -f .devcontainer/docker-compose.yaml run voxtream python voxtream/train.py batch_size=12
```



### Custom dataset

To prepare a custom training dataset check [dataset](voxtream/utils/dataset/README.md) section.



## Benchmark

To evaluate model's real time factor (RTF) and First packet latency (FPL) run `voxtream-benchmark`. You can compile model for faster inference using `--compile` flag (note that initial compilation take some time).

| Device  | Compiled           | FPL, ms | RTF   |
| :-:     | :-:                | :-:     | :-:   |
| RTX3090 |                    | 74      | 0.256 |
| RTX3090 | :heavy_check_mark: | 63      | 0.173 |



## TODO

- [ ] Add finetuning instructions



## Disclaimer
Any organization or individual is prohibited from using any technology mentioned in this paper to generate someone's speech without his/her consent, including but not limited to government leaders, political figures, and celebrities. If you do not comply with this item, you could be in violation of copyright laws.

## pyproject.toml

```
[build-system]
requires = ["setuptools>=70", "wheel"]
build-backend = "setuptools.build_meta"

[tool.setuptools]
license-files = ["LICENSE"]

[project]
name = "voxtream"
version = "0.2.4"
description = "Full-Stream Zero-shot TTS model with Extremely Low Latency and Speaking-rate Control"
readme = "README.md"
license = { text = "MIT" }
authors = [
  { name = "Nikita Torgashov", email = "torgaschov.nikita@gmail.com" }
]
requires-python = ">=3.9"
keywords = [
  "text-to-speech",
  "streaming",
  "tts",
  "speech-synthesis",
  "voice-cloning"
]
classifiers = [
  "Development Status :: 3 - Alpha",
  "Intended Audience :: Developers",
  "Topic :: Multimedia :: Sound/Audio",
  "License :: OSI Approved :: MIT License",
  "Programming Language :: Python :: 3",
]

# install_requires (from requirements.txt)
dependencies = [
  "torch>=2.4,<2.9",
  "torchaudio>=2.4,<2.9",
  "torchtune==0.4.0",
  "torchao==0.9.0",
  "moshi>=0.2.13",
  "transformers==4.50.0",
  "huggingface_hub==0.28.1",
  "g2p-en==2.1.0",
  "librosa==0.11.0",
  "soundfile==0.13.1",
  "inflect==7.5.0",
  "nltk==3.9.1",
  "gradio==4.44.1",
  "gradio_client==1.3.0",
  "starlette==0.52.1",
  "pydantic==2.10.6",
  "setuptools>=70,<81",
  "silero-vad==6.2.0",
  "jiwer==4.0.0",
  "openai-whisper==20250625"
]

[project.optional-dependencies]
dev = ["black", "isort", "flake8", "mypy", "pytest"]

[project.urls]
Homepage = "https://herimor.github.io/voxtream2"
"Bug Reports" = "https://github.com/herimor/voxtream/issues"
Source = "https://github.com/herimor/voxtream"

[project.scripts]
voxtream = "voxtream.run:main"
voxtream-app = "voxtream.app:main"
voxtream-benchmark = "voxtream.benchmark:main"
voxtream-server = "voxtream.server:main"

[tool.setuptools.packages.find]
where = ["."]
include = ["voxtream*"]

# Tool configs merged from your original pyproject.toml
[tool.black]
line-length = 88
target-version = ["py311"]
skip-string-normalization = false

[tool.isort]
profile = "black"

[tool.ruff]
line-length = 88
lint.select = ["E", "F", "W", "C90", "B", "I"]
lint.ignore = ["E501", "E402", "C901"]

[tool.mypy]
python_version = "3.11"
ignore_missing_imports = true
implicit_optional = true
warn_unused_ignores = false
disable_error_code = [
  "arg-type",
  "assignment",
  "attr-defined",
  "call-overload",
  "import-untyped",
  "method-assign",
  "misc",
  "name-match",
  "no-redef",
  "operator",
  "override",
  "return-value",
  "union-attr",
  "var-annotated",
]

```

## Top-level layout

- .devcontainer/ (dir, 5 files, ~80 lines)
- .gitignore (~11 lines)
- .pre-commit-config.yaml (~21 lines)
- assets/ (dir, 23 files, ~64 lines)
- ATTRIBUTION.md (~14 lines)
- configs/ (dir, 4 files, ~213 lines)
- LICENSE-APACHE (~201 lines)
- LICENSE-MIT (~21 lines)
- MANIFEST.in (~6 lines)
- NOTICE (~13 lines)
- pyproject.toml (~109 lines)
- README.md (~227 lines)
- requirements.txt (~23 lines)
- tests/ (dir, 1 files, ~71 lines)
- voxtream/ (dir, 52 files, ~10079 lines)

