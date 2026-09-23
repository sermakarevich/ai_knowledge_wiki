> PDF location (no source.pdf under 2 MB in run dir): https://github.com/NVIDIA-NeMo/Speech
# NVIDIA-NeMo/Speech
Source: https://github.com/NVIDIA-NeMo/Speech
Kind: repo
Fetched: 2026-09-22T14:30:42.854227+00:00
Tool: git-clone

# NVIDIA-NeMo/Speech

Commit: 5dbdde68d3897c03faeda1b0d9655cd90b1c5e08

## README

[![Project Status: Active -- The project has reached a stable, usable state and is being actively developed.](http://www.repostatus.org/badges/latest/active.svg)](http://www.repostatus.org/#active)
[![CodeQL](https://github.com/NVIDIA-NeMo/Speech/actions/workflows/codeql.yml/badge.svg?branch=main&event=push)](https://github.com/NVIDIA-NeMo/Speech/actions/workflows/codeql.yml)
[![NeMo Speech license](https://img.shields.io/badge/License-Apache%202.0-brightgreen.svg)](https://github.com/NVIDIA-NeMo/Speech/blob/main/LICENSE)
[![Release version](https://badge.fury.io/py/nemo-toolkit.svg)](https://badge.fury.io/py/nemo-toolkit)
[![Python version](https://img.shields.io/pypi/pyversions/nemo-toolkit.svg)](https://badge.fury.io/py/nemo-toolkit)
[![PyPi total downloads](https://static.pepy.tech/personalized-badge/nemo-toolkit?period=total&units=international_system&left_color=grey&right_color=brightgreen&left_text=downloads)](https://pepy.tech/project/nemo-toolkit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# **NVIDIA NeMo Speech**
Checkout our [HuggingFace🤗 collection](https://huggingface.co/collections/nvidia/nemotron-speech) for the latest open
weight checkpoints and demos!

## Updates

> NeMo Speech 3.0 is now available as [release v3.0.0](https://github.com/NVIDIA-NeMo/Speech/releases/tag/v3.0.0)
> and in the [26.07.00 NeMo Speech NGC container](https://catalog.ngc.nvidia.com/orgs/nvidia/containers/nemo-speech?version=26.07.00).
> The final NeMo release before the repository split was
> [v2.7.3](https://github.com/NVIDIA-NeMo/Speech/releases/tag/v2.7.3), available in the
> [26.04 NeMo NGC container](https://catalog.ngc.nvidia.com/orgs/nvidia/containers/nemo?version=26.04).

- 2026-07: [MagpieTTS v2607](https://huggingface.co/nvidia/magpie_tts_multilingual_357m) has been released with support
    for 3 new languages (Ar, Ko, Pt) + 9 existing languages (En, Es, De, Fr, Vi, It, Zh, Hi, Ja). Try out
    [the demo](https://huggingface.co/spaces/nvidia/magpie_tts_multilingual_demo)!
- 2026-06: [Nemotron-3.5-ASR-Streaming-0.6B](https://huggingface.co/nvidia/nemotron-3.5-asr-streaming-0.6b) has been released with 40 languages supported, controllable latency 80ms-1s, and 240-2400 1xH100 concurrent streams. Built on cache-aware Fastconformer architecture.
- 2026-04: [Parakeet-unified-en-0.6b](https://huggingface.co/nvidia/parakeet-unified-en-0.6b) has been released with high-quality offline and streaming (with a minimum latency of 160ms) inference in one model for English language with punctuation and capitalization support. 
- 2026-03: [Nemotron 3 VoiceChat](https://build.nvidia.com/nvidia/nemotron-voicechat/modelcard) is now released in Early Access. Built on the Nemotron Nano v2 LLM backbone with Nemotron speech and TTS decoder, VoiceChat delivers full-duplex, natural, interruptible conversations with low latency. Try out [the demo](https://build.nvidia.com/nvidia/nemotron-voicechat) and apply for [early access](https://developer.nvidia.com/nemotron-voicechat-early-access).
- 2026-03: [Nemotron-Speech-Streaming v2603](https://huggingface.co/nvidia/nemotron-speech-streaming-en-0.6b) has been
    updated. It has been trained on a larger and more diverse corpus, resulting in lower WER across all latency modes.
    Try out [the demo](https://huggingface.co/spaces/nvidia/nemotron-speech-streaming-en-0.6b) and check out
    [the NIM](https://build.nvidia.com/nvidia/nemotron-asr-streaming).
- 2026-03: [MagpieTTS v2602](https://huggingface.co/nvidia/magpie_tts_multilingual_357m/tree/v2602) has been released with support
    for 9 languages (En, Es, De, Fr, Vi, It, Zh, Hi, Ja).
- 2026-01: Nemotron-Speech-Streaming was released: One checkpoint that enables users to pick their optimal point
    on the latency-accuracy Pareto curve!
- 2026-01: [MagpieTTS v2512](https://huggingface.co/nvidia/magpie_tts_multilingual_357m/tree/v2512) was released.
- 2026: This repo has pivoted to focus on audio, speech, and multimodal LLMs. For the final pre-split NeMo release with
    support for additional modalities, see [v2.7.3](https://github.com/NVIDIA-NeMo/Speech/releases/tag/v2.7.3).
- 2025-08: [Parakeet V3](https://huggingface.co/nvidia/parakeet-tdt-0.6b-v3) and
    [Canary V2](https://huggingface.co/nvidia/canary-1b-v2) have been released with speech recognition and translation
    support for 25 European languages.
- 2025-06: [Canary-Qwen-2.5B](https://huggingface.co/nvidia/canary-qwen-2.5b) has been released with record-setting
    5.63% WER on English Open ASR Leaderboard.

## Introduction

NVIDIA NeMo Speech is built for researchers and PyTorch developers working on Speech models including Automatic Speech
Recognition (ASR), Text to Speech (TTS), and Speech LLMs. It is designed to help you efficiently create, customize, and
deploy new AI models by leveraging existing code and pre-trained model checkpoints.

For technical documentation, please see the
[NeMo Speech Developer Documentation](https://docs.nvidia.com/nemo/speech/nightly/).

## Requirements

NeMo Speech works with the **Python, PyTorch, and CUDA versions of your choosing**:

- Python 3.12 or above
- PyTorch 2.7 or above (CPU, CUDA, etc. — your choice)
- NVIDIA GPU + CUDA (required for training; recommended for inference)

If you already have a Python/PyTorch/CUDA stack that satisfies those minimums, NeMo Speech installs on top of it **without replacing it**, so your existing PyTorch build is kept (see the install options below). The versions pinned in `uv.lock` and shipped in the official container — Python 3.13, PyTorch 2.11 with CUDA 12.9 or PyTorch 2.12 with CUDA 13.2 — are simply the combinations we actively test and support. They make setup turnkey and reproducible, but they are **not** a hard requirement.

As of [Pytorch 2.6](https://docs.pytorch.org/docs/stable/notes/serialization.html#torch-load-with-weights-only-true),
`torch.load` defaults to using `weights_only=True`. Some model checkpoints may require using `weights_only=False`.
In this case, you can set the env var `TORCH_FORCE_NO_WEIGHTS_ONLY_LOAD=1` before running code that uses `torch.load`.
However, this should only be done with trusted files. Loading files from untrusted sources with more than weights only
can have the risk of arbitrary code execution.

## Developer Documentation

| Version | Description |
| ------- | ----------- |
| 3.0.0 (latest release) | [NeMo Speech 3.0.0 documentation](https://docs.nvidia.com/nemo/speech/3.0.0/) |
| Nightly | [Documentation for the latest `main` branch](https://docs.nvidia.com/nemo/speech/nightly/) |

## Install NeMo Speech

The recommended way to install NeMo Speech is from source with [uv](https://docs.astral.sh/uv/), which reproduces our actively-tested stack from the committed `uv.lock`. If you need different Python/PyTorch/CUDA versions, NeMo Speech also installs over your existing environment via pip — see the [pip fallback](#from-pypi-with-pip-fallback--bring-your-own-versions) below.

### From source with uv (recommended)

```bash
git clone https://github.com/NVIDIA-NeMo/Speech.git
cd Speech
uv sync --extra all --extra cu13     # CUDA 13.x (recommended) — use --extra cu12 for CUDA 12.x
```

This installs our supported stack (Python 3.13, PyTorch 2.12, CUDA 13.2) into `.venv/` with NeMo Speech editable. Add `--group test` for the test suite or `--group docs` to build the docs; run tools via `uv run <cmd>` or activate with `source .venv/bin/activate`. On Linux, `cu12` and `cu13` are mutually exclusive — pass exactly one (`cu13` is the default). For the **exact** container baseline, add `--locked --python 3.13` (the path the Dockerfile and CI use).

> **SpeechLM2 / Automodel:** the Automodel backend runs **without** any compiled dependencies. It can *optionally* benefit from dedicated accelerated backends (Transformer Engine, FlashAttention, Mamba, grouped-GEMM/MoE, DeepEP) for better performance — these source-built kernels come from the `compiled` (Hopper/Blackwell) or `compiled-a100` (A100) extras, built by `docker/Dockerfile` (`GPU_TARGET=h100plus` / `a100`). See the [installation guide](https://docs.nvidia.com/nemo/speech/nightly/) for the full list and build details.

### Docker (turnkey, our supported stack)

The latest prebuilt NeMo Speech image is the
[26.07.00 NGC container](https://catalog.ngc.nvidia.com/orgs/nvidia/containers/nemo-speech?version=26.07.00):

```bash
docker pull nvcr.io/nvidia/nemo-speech:26.07.00
docker run --rm -it --gpus all -v "$PWD:/workspace" nvcr.io/nvidia/nemo-speech:26.07.00 bash
```

To build the container from source (CUDA 13 / H100+ by default):

```bash
git clone https://github.com/NVIDIA-NeMo/Speech.git
cd Speech
docker buildx build -f docker/Dockerfile -t nemo-speech .          # CUDA 13 / H100+ (default)
docker run --rm -it --gpus all -v "$PWD:/workspace" nemo-speech bash
```

For A100, set `GPU_TARGET=a100` — A100 works with **both CUDA 12 and CUDA 13** (CUDA 13, the default base image, is recommended; the CUDA 12 base is a convenience). See the header of [`docker/Dockerfile`](docker/Dockerfile) for all build arguments (`BASE_IMAGE`, `GPU_TARGET`).

### From PyPI with pip (fallback — bring your own versions)

Prefer your own Python/PyTorch/CUDA? Install your PyTorch first (any version ≥ 2.7 for your CPU/CUDA/etc. target — see the [PyTorch install matrix](https://pytorch.org/get-started/locally/)), then add NeMo Speech and it **keeps your build**. `uv pip` (uv's fast, pip-compatible installer) works like `pip`:

```bash
uv pip install 'nemo-toolkit[asr,tts]'   # or plain: pip install 'nemo-toolkit[asr,tts]'
```

> ⚠️ Do **not** use `uv sync --locked` for a bring-your-own stack — it applies `uv.lock` and replaces your Python/PyTorch/CUDA with the supported baseline. Use `uv pip`/`pip` here; reserve `uv sync --locked` for reproducing our stack.

To instead pull *our* pinned PyTorch build, add the CUDA extra and the matching wheel index (pip/uv pip do not read uv's project index config, so `--extra-index-url` is required):

```bash
pip install 'nemo-toolkit[asr,tts,cu13]' --extra-index-url https://download.pytorch.org/whl/cu132   # CUDA 13.x
pip install 'nemo-toolkit[asr,tts,cu12]' --extra-index-url https://download.pytorch.org/whl/cu129   # CUDA 12.x
```

## Contribute to NeMo Speech

We welcome community contributions! Please refer to
[CONTRIBUTING.md](https://github.com/NVIDIA-NeMo/Speech/blob/main/CONTRIBUTING.md) for the process.

## Licenses

NeMo Speech is licensed under the [Apache License 2.0](https://github.com/NVIDIA-NeMo/Speech/blob/main/LICENSE).


## pyproject.toml

```
# SPDX-FileCopyrightText: Copyright (c) 2023, NVIDIA CORPORATION & AFFILIATES.  All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

[build-system]
requires = ["setuptools >= 61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "nemo-toolkit"
dynamic = ["version"]
description = "NeMo - a toolkit for Conversational AI"
readme = "README.md"
license = {file = "LICENSE"}
requires-python = ">=3.10"
dependencies = [
    "aistore",
    "huggingface_hub>=0.24",
    "numba ; platform_system == 'Darwin'",
    "cuda-bindings ; platform_system != 'Darwin'",
    "numpy>=1.22",
    "onnx>=1.7.0",
    "scikit-learn",
    "setuptools>=70.0.0",
    "smart-open",
    "tensorboard",
    "text-unidecode",
    "torch>=2.7.0",
    "tqdm>=4.41.0",
    "wrapt",
]
authors = [{ name = "NVIDIA", email = "nemo-toolkit@nvidia.com" }]
maintainers = [{ name = "NVIDIA", email = "nemo-toolkit@nvidia.com" }]
keywords = [
    "NLP",
    "NeMo",
    "deep",
    "gpu",
    "language",
    "learning",
    "learning",
    "machine",
    "nvidia",
    "pytorch",
    "speech",
    "torch",
    "tts",
]
classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Environment :: Console",
    "Intended Audience :: Developers",
    "Intended Audience :: Information Technology",
    "Intended Audience :: Science/Research",
    "License :: OSI Approved :: Apache Software License",
    "Natural Language :: English",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.10",
    "Topic :: Scientific/Engineering :: Artificial Intelligence",
    "Topic :: Scientific/Engineering :: Image Recognition",
    "Topic :: Scientific/Engineering :: Mathematics",
    "Topic :: Scientific/Engineering",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: Software Development :: Libraries",
    "Topic :: Utilities",
]

[project.optional-dependencies]
core = [
    "hydra-core>1.3,<=1.3.2",
    "lightning>2.2.1,<=2.4.0",
    "omegaconf<=2.3",
    "torchmetrics>=0.11.0",
    "transformers",
    "wandb",
    "webdataset>=0.2.86",
    "nv_one_logger_core>=2.3.1",
    "nv_one_logger_training_telemetry>=2.3.1",
    "nv_one_logger_pytorch_lightning_integration>=2.3.1",
]

lightning = [
    "hydra-core>1.3,<=1.3.2",
    "lightning>2.2.1,<=2.4.0",
    "omegaconf<=2.3",
    "torchmetrics>=0.11.0",
    "transformers",
    "wandb",
    "webdataset>=0.2.86",
    "nv_one_logger_core>=2.3.1",
    "nv_one_logger_training_telemetry>=2.3.1",
    "nv_one_logger_pytorch_lightning_integration>=2.3.1",
]

common-only = [
    "datasets>=3.2.0",
    "einops",
    "pandas",
    "sentencepiece<1.0.0",
]

asr-only = [
    "braceexpand",
    "einops",
    "kaldialign",
    "lhotse==2.0.0a6",
    "librosa>=0.10.1",
    "packaging",
    "sacrebleu",
    "scipy>=0.14",
    "soundfile",
    "whisper_normalizer",
]

tts = [
    "einops",
    "janome",
    "jieba",
    "librosa",
    "matplotlib",
    "nemo_text_processing; 'arm' not in platform_machine and 'aarch' not in platform_machine and sys_platform != 'darwin'",
    "nltk",
    "pandas",
    "pypinyin",
    "pypinyin-dict",
    "pyopenjtalk",
    "braceexpand",
    "kaldialign",
    "lhotse==2.0.0a6",
    "librosa>=0.10.1",
    "packaging",
    "sacrebleu",
    "scipy>=0.14",
    "soundfile",
    "whisper_normalizer",
    "datasets>=3.2.0",
    "sentencepiece<1.0.0",
    "hydra-core>1.3,<=1.3.2",
    "lightning>2.2.1,<=2.4.0",
    "omegaconf<=2.3",
    "torchmetrics>=0.11.0",
    "transformers",
    "wandb",
    "webdataset>=0.2.86",
    "nv_one_logger_core>=2.3.1",
    "nv_one_logger_training_telemetry>=2.3.1",
    "nv_one_logger_pytorch_lightning_integration>=2.3.1",
]

audio = [
    "einops",
    "lhotse==2.0.0a6",
    "librosa>=0.10.0",
    "matplotlib",
    "pesq; (platform_machine != 'x86_64' or platform_system != 'Darwin')",
    "pystoi",
    "scipy>=0.14",
    "soundfile",
    "datasets>=3.2.0",
    "pandas",
    "sentencepiece<1.0.0",
    "hydra-core>1.3,<=1.3.2",
    "lightning>2.2.1,<=2.4.0",
    "omegaconf<=2.3",
    "torchmetrics>=0.11.0",
    "transformers",
    "wandb",
    "webdataset>=0.2.86",
    "nv_one_logger_core>=2.3.1",
    "nv_one_logger_training_telemetry>=2.3.1",
    "nv_one_logger_pytorch_lightning_integration>=2.3.1",
]

speechlm2-only = [
    "nemo_automodel",
    "flashoptim",
    "peft>=0.18.1",
]

# vLLM owns its exact Torch and CUDA-kernel stack.
# Install this serving extra separately from the cu*/compiled* extras below.
vllm = [
    "peft>=0.18.1",
    "vllm==0.28.0; sys_platform == 'linux'",
]

all = [
    "hydra-core>1.3,<=1.3.2",
    "lightning>2.2.1,<=2.4.0",
    "omegaconf<=2.3",
    "torchmetrics>=0.11.0",
    "transformers",
    "wandb",
    "webdataset>=0.2.86",
    "nv_one_logger_core>=2.3.1",
    "nv_one_logger_training_telemetry>=2.3.1",
    "nv_one_logger_pytorch_lightning_integration>=2.3.1",
    "datasets>=3.2.0",
    "einops",
    "pandas",
    "sentencepiece<1.0.0",
    "braceexpand",
    "kaldialign",
    "lhotse==2.0.0a6",
    "librosa>=0.10.1",
    "packaging",
    "sacrebleu",
    "scipy>=0.14",
    "soundfile",
    "whisper_normalizer",
    "janome",
    "jieba",
    "librosa",
    "matplotlib",
    "nemo_text_processing; 'arm' not in platform_machine and 'aarch' not in platform_machine and sys_platform != 'darwin'",
    "nltk",
    "pypinyin",
    "pypinyin-dict",
    "pyopenjtalk",
    "librosa>=0.10.0",
    "pesq; (platform_machine != 'x86_64' or platform_system != 'Darwin')",
    "pystoi",
    "nemo_automodel",
    "flashoptim",
    "peft>=0.18.1",
]

cu12 = [
    "torch==2.11.0+cu129 ; sys_platform == 'linux'",
    "numba-cuda[cu12] ; platform_system != 'Darwin'",
    "cuda-python>=12,<13 ; platform_system != 'Darwin'"
]

cu13 = [
    "torch==2.12.0+cu132 ; sys_platform == 'linux'",
    "numba-cuda[cu13] ; platform_system != 'Darwin'",
    "cuda-python>=13,<14 ; platform_system != 'Darwin'"
]

compiled = [
    "onnx-ir==0.2.1",
    "onnxscript==0.7.0",
    "deep_ep==1.2.1",
    "nv-grouped-gemm==1.1.4.post8",
    "causal-conv1d==1.6.2.post1",
    "mamba-ssm==2.3.2.post1",
    # v2.8.3 release assets do not include a cu13/torch2.12/cp313 wheel,
    # so uv builds this from source under the Dockerfile build environment.
    "flash-attn==2.8.3",
    "transformer-engine[pytorch,core_cu13]==2.15"
]

compiled-a100 = [
    "onnx-ir==0.2.1",
    "onnxscript==0.7.0",
    "nv-grouped-gemm==1.1.4.post8",
    "causal-conv1d==1.6.2.post1",
    "mamba-ssm==2.3.2.post1",
    # v2.8.3 release assets do not include a cu13/torch2.12/cp313 wheel,
    # so uv builds this from source under the Dockerfile build environment.
    "flash-attn==2.8.3",
    "transformer-engine[pytorch,core_cu12]==2.15"
]

common = [
    "datasets>=3.2.0",
    "einops",
    "pandas",
    "sentencepiece<1.0.0",
    "hydra-core>1.3,<=1.3.2",
    "lightning>2.2.1,<=2.4.0",
    "omegaconf<=2.3",
    "torchmetrics>=0.11.0",
    "transformers",
    "wandb",
    "webdataset>=0.2.86",
    "nv_one_logger_core>=2.3.1",
    "nv_one_logger_training_telemetry>=2.3.1",
    "nv_one_logger_pytorch_lightning_integration>=2.3.1",
]

asr = [
    "braceexpand",
    "einops",
    "kaldialign",
    "lhotse==2.0.0a6",
    "librosa>=0.10.1",
    "packaging",
    "sacrebleu",
    "scipy>=0.14",
    "soundfile",
    "whisper_normalizer",
    "datasets>=3.2.0",
    "pandas",
    "sentencepiece<1.0.0",
    "hydra-core>1.3,<=1.3.2",
  

... (truncated, 8037 more characters)
```

## setup.py

```
# ! /usr/bin/python
# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: Copyright (c) 2020, NVIDIA CORPORATION & AFFILIATES.  All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Setup for pip package."""

import importlib.util
import subprocess
from distutils import cmd as distutils_cmd
from distutils import log as distutils_log

import setuptools

spec = importlib.util.spec_from_file_location('package_info', 'nemo/package_info.py')
package_info = importlib.util.module_from_spec(spec)
spec.loader.exec_module(package_info)


__contact_emails__ = package_info.__contact_emails__
__contact_names__ = package_info.__contact_names__
__description__ = package_info.__description__
__download_url__ = package_info.__download_url__
__homepage__ = package_info.__homepage__
__keywords__ = package_info.__keywords__
__license__ = package_info.__license__
__package_name__ = package_info.__package_name__
__repository_url__ = package_info.__repository_url__
__version__ = package_info.__version__


with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()
    long_description_content_type = "text/markdown"


###############################################################################
#                            Code style checkers                              #
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% #


class StyleCommand(distutils_cmd.Command):
    __ISORT_BASE = 'isort'
    __BLACK_BASE = 'black'
    description = 'Checks overall project code style.'
    user_options = [
        ('scope=', None, 'Folder of file to operate within.'),
        ('fix', None, 'True if tries to fix issues in-place.'),
    ]

    def __call_checker(self, base_command, scope, check):
        command = list(base_command)

        command.append(scope)

        if check:
            command.extend(['--check', '--diff'])

        self.announce(
            msg='Running command: %s' % str(' '.join(command)),
            level=distutils_log.INFO,
        )

        return_code = subprocess.call(command)

        return return_code

    def _isort(self, scope, check):
        return self.__call_checker(
            base_command=self.__ISORT_BASE.split(),
            scope=scope,
            check=check,
        )

    def _black(self, scope, check):
        return self.__call_checker(
            base_command=self.__BLACK_BASE.split(),
            scope=scope,
            check=check,
        )

    def _pass(self):
        self.announce(msg='\033[32mPASS\x1b[0m', level=distutils_log.INFO)

    def _fail(self):
        self.announce(msg='\033[31mFAIL\x1b[0m', level=distutils_log.INFO)

    # noinspection PyAttributeOutsideInit
    def initialize_options(self):
        self.scope = '.'
        self.fix = ''

    def run(self):
        scope, check = self.scope, not self.fix
        isort_return = self._isort(scope=scope, check=check)
        black_return = self._black(scope=scope, check=check)

        if isort_return == 0 and black_return == 0:
            self._pass()
        else:
            self._fail()
            exit(isort_return if isort_return != 0 else black_return)

    def finalize_options(self):
        pass


###############################################################################

setuptools.setup(
    name=__package_name__,
    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version=__version__,
    description=__description__,
    long_description=long_description,
    long_description_content_type=long_description_content_type,
    # The project's main homepage.
    url=__repository_url__,
    download_url=__download_url__,
    # Author details
    author=__contact_names__,
    author_email=__contact_emails__,
    # maintainer Details
    maintainer=__contact_names__,
    maintainer_email=__contact_emails__,
    # The licence under which the project is released
    license=__license__,
    classifiers=[
        # How mature is this project? Common values are
        #  1 - Planning
        #  2 - Pre-Alpha
        #  3 - Alpha
        #  4 - Beta
        #  5 - Production/Stable
        #  6 - Mature
        #  7 - Inactive
        'Development Status :: 5 - Production/Stable',
        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Information Technology',
        # Indicate what your project relates to
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Scientific/Engineering :: Image Recognition',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: Apache Software License',
        # Supported python versions
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        # Additional Setting
        'Environment :: Console',
        'Natural Language :: English',
        'Operating System :: OS Independent',
    ],
    packages=setuptools.find_packages(),
    python_requires='>=3.10',
    # Add in any packaged data.
    include_package_data=True,
    exclude=['tools', 'tests'],
    package_data={'': ['*.tsv', '*.txt', '*.far', '*.fst', '*.cpp', 'Makefile']},
    zip_safe=False,
    # PyPI package information.
    keywords=__keywords__,
    # Custom commands.
    cmdclass={'style': StyleCommand},
)

```

## Top-level layout

- .claude/ (dir, 20 files, ~2537 lines)
- .codex/ (dir, 0 files, ~0 lines)
- .coveragerc (~40 lines)
- .cursor/ (dir, 0 files, ~0 lines)
- .dockerignore (~19 lines)
- .flake8 (~9 lines)
- .flake8.other (~12 lines)
- .flake8.speech (~12 lines)
- .github/ (dir, 41 files, ~3721 lines)
- .gitignore (~197 lines)
- .pre-commit-config.yaml (~46 lines)
- .pylintrc (~5 lines)
- .pylintrc.other (~13 lines)
- .pylintrc.speech (~9 lines)
- .readthedocs.yml (~36 lines)
- .secrets.baseline (~2082 lines)
- AGENTS.md (~146 lines)
- CITATION.cff (~41 lines)
- CLAUDE.md (~146 lines)
- codecov.yml (~23 lines)
- CONTRIBUTING.md (~146 lines)
- docker/ (dir, 1 files, ~318 lines)
- docs/ (dir, 282 files, ~23154 lines)
- examples/ (dir, 303 files, ~53417 lines)
- external/ (dir, 7 files, ~383 lines)
- LICENSE (~201 lines)
- MANIFEST.in (~1 lines)
- nemo/ (dir, 772 files, ~300135 lines)
- nemo_dependencies.py (~205 lines)
- pyproject.toml (~587 lines)
- README.md (~137 lines)
- scripts/ (dir, 198 files, ~2153375 lines)
- SECURITY.md (~25 lines)
- setup.py (~186 lines)
- tests/ (dir, 702 files, ~145077 lines)
- THIRD-PARTY-NOTICES (~320 lines)
- tools/ (dir, 83 files, ~21009 lines)
- tutorials/ (dir, 87 files, ~53899 lines)
- uv.lock (~17299 lines)

