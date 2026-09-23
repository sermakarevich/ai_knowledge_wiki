> PDF location: https://github.com/remsky/Kokoro-FastAPI (no source.pdf fetched; see Source field below)
# remsky/Kokoro-FastAPI
Source: https://github.com/remsky/Kokoro-FastAPI
Kind: repo
Fetched: 2026-09-22T14:15:26.537368+00:00
Tool: git-clone

# remsky/Kokoro-FastAPI

Commit: b4ef64b1ce60682debda4fe0a066259e284eb1b4

## README

![FastKoko: Dockerized Kokoro-82M TTS, OpenAI-compatible API](assets/banner.png)
<br>

<a href="https://trendshift.io/repositories/13745?utm_source=repository-badge&amp;utm_medium=badge&amp;utm_campaign=badge-repository-13745"><img src="https://trendshift.io/api/badge/repositories/13745" alt="remsky%2FKokoro-FastAPI | Trendshift" width="164" height="36"/></a>

[![Changelog](https://img.shields.io/badge/changelog-white)](./CHANGELOG.md)
[![Coverage](https://codecov.io/gh/remsky/Kokoro-FastAPI/graph/badge.svg)](https://codecov.io/gh/remsky/Kokoro-FastAPI) [![CI](https://github.com/remsky/Kokoro-FastAPI/actions/workflows/ci.yml/badge.svg?branch=master)](https://github.com/remsky/Kokoro-FastAPI/actions/workflows/ci.yml)

[![Kokoro](https://img.shields.io/badge/kokoro-0.9.4-BB5420)](https://github.com/hexgrad/kokoro)
[![Misaki](https://img.shields.io/badge/misaki-0.9.4-B8860B)](https://github.com/hexgrad/misaki)
[![Tested at Model Commit](https://img.shields.io/badge/model-1.0::41e5892-blue)](https://huggingface.co/hexgrad/Kokoro-82M/commit/41e5892b9d8b43e56fc560f892312a328a410973) 

[![Try on Spaces](https://img.shields.io/badge/%F0%9F%A4%97%20Try%20on-Spaces-blue)](https://huggingface.co/spaces/Remsky/FastKoko) [![Downloads](https://img.shields.io/badge/downloads-2.6M%2B-2496ED?logo=docker&logoColor=white)](https://github.com/remsky?tab=packages&repo_name=Kokoro-FastAPI)


Dockerized FastAPI wrapper for [Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M) text-to-speech model. Generate hours of high quality speech in minutes.

- OpenAI-compatible Speech endpoint, multi-language support
  - English (US/GB), Spanish, French, Hindi, Italian, Japanese, Brazilian Portuguese, Mandarin Chinese
- Custom voicepack generation via [Inno Clone-Tuner](https://github.com/remsky/inno-kokoro)
- Optional integrated WebUI; read-along long-generation
- Inline multi-speaker generation & voice mixing + aliasing weighted combinations, SSML support
- Per-word, or per-chunk timestamped caption generation
- Phoneme endpoints: generate phonemes from text, or generate audio from phonemes
- Prebuilt multiplatform images
  - CPU and NVIDIA GPU (CUDA): linux/amd64 + linux/arm64
  - AMD GPU (ROCm, experimental): linux/amd64 only
- Apple Silicon (MPS) supported when running directly via UV (no image)


### Integration & Guides 
[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/remsky/Kokoro-FastAPI) [![Ask CodeWiki](https://img.shields.io/badge/Ask%20CodeWiki-4285F4?logo=googlegemini&logoColor=white)](https://codewiki.google/github.com/remsky/kokoro-fastapi)

 [![Helm Chart](https://img.shields.io/badge/Helm%20Chart-black?style=flat&logo=helm&logoColor=white)](docs/deployment/kubernetes.md) [![DigitalOcean](https://img.shields.io/badge/DigitalOcean-black?style=flat&logo=digitalocean&logoColor=white)](docs/deployment/digitalocean.md) [![SillyTavern](https://img.shields.io/badge/SillyTavern-black?style=flat&color=red)](docs/integrations/sillytavern.md)
[![OpenWebUI](https://img.shields.io/badge/OpenWebUI-black?style=flat&color=white)](docs/integrations/openwebui.md)

Community projects that use, recommend, or enable Kokoro-FastAPI as a backend:

- <sub>Home Assistant: [wyoming_openai](https://github.com/roryeckel/wyoming_openai), [openai_tts](https://github.com/sfortis/openai_tts), [Kokoro-TTS](https://github.com/beecho01/Kokoro-TTS)</sub>
- <sub>App stores and templates: [Umbrel](https://github.com/getumbrel/umbrel-apps/tree/master/kokoro), [Unraid Apps](https://github.com/nwithan8/unraid_templates), [GPUStack](https://github.com/gpustack/gpustack), [jetson-containers](https://github.com/dusty-nv/jetson-containers/tree/master/packages/speech/kokoro-tts)</sub>
- <sub>Readers and audiobooks: [openreader](https://github.com/richardr1126/openreader), [epub_to_audiobook](https://github.com/p0n1/epub_to_audiobook), [audiobook-creator](https://github.com/prakharsr/audiobook-creator), [Zotero-TTS](https://github.com/xujialiu/Zotero-TTS)</sub>
- <sub>Assistants and agents: [xiaozhi-esp32-server](https://github.com/xinnan-tech/xiaozhi-esp32-server), [call-me](https://github.com/ZeframLou/call-me), [agent-cli](https://github.com/basnijholt/agent-cli), [voice-chat-ai](https://github.com/bigsk1/voice-chat-ai)</sub>
- <sub>Browser: [kokoro-extension](https://github.com/Fooftilly/kokoro-extension), [customtts](https://github.com/BassGaming/customtts)</sub>

## Get Started

<details>
<summary>Quickest Start (docker run)</summary>

Pre-built multi-arch images with models baked in. 

`:latest` is available, but please pin to a release tag for stable usage.

<sub><ins>**No GPU**</ins> (laptop, CPU-only server)</sub>
```bash
docker run -p 8880:8880 ghcr.io/remsky/kokoro-fastapi-cpu:latest
```

<sub><ins>**NVIDIA**</ins> (GTX 900-series through RTX 40; ships cu126)</sub>
```bash
docker run --gpus all -p 8880:8880 ghcr.io/remsky/kokoro-fastapi-gpu:latest
```

<sub><ins>**NVIDIA RTX 50-series / Blackwell**</ins> (ships cu128)</sub>
```bash
docker run --gpus all -p 8880:8880 ghcr.io/remsky/kokoro-fastapi-gpu:latest-cu128
```

<sub><ins>**NVIDIA arm64**</ins> (Jetson, GH200; same tag, ships cu129)</sub>
```bash
docker run --gpus all -p 8880:8880 ghcr.io/remsky/kokoro-fastapi-gpu:latest
```

<sub><ins>**AMD GPU**</ins> (ROCm, experimental, x86_64 only)</sub>
```bash
docker run --device=/dev/kfd --device=/dev/dri -p 8880:8880 ghcr.io/remsky/kokoro-fastapi-rocm:latest
```

<sub><ins>**Apple Silicon**</ins> (native MPS clone; the CPU image also works)</sub>
```bash
./start-gpu_mac.sh
```

`gpu:latest` is the same image as `gpu:latest-cu126`. Configuration via environment variables, see [the configuration guide](docs/configuration.md).

</details>

<details>

<summary>Quick Start (docker compose) </summary>

1. Install prerequisites, and start the service using Docker Compose (Full setup including UI):
   - Install [Docker](https://www.docker.com/products/docker-desktop/)
   - Clone the repository:
        ```bash
        git clone https://github.com/remsky/Kokoro-FastAPI.git
        cd Kokoro-FastAPI

        cd docker/gpu   # For NVIDIA GPU support
        # or cd docker/cpu   # For CPU support
        # or cd docker/rocm  # For AMD GPU (ROCm, experimental, amd64 only)
        docker compose up --build

        # *Note for Apple Silicon (M1/M2/M3) users:
        # The Docker GPU image is CUDA-only and won't run on Apple Silicon. With Docker, use `docker/cpu`.
        # For native MPS (Apple GPU) acceleration, run directly via UV with `./start-gpu_mac.sh`.

        cd ../..  # back to repo root for the paths below

        # Models will auto-download, but if needed you can manually download:
        python docker/scripts/download_model.py --output api/src/models/v1_0
        ```

[Configuration guide](docs/configuration.md) covers image vs build, the volume mounts, and env vars.
</details>
<details>
<summary>Direct Run (via uv) </summary>

1. Install prerequisites:
   - Install [astral-uv](https://docs.astral.sh/uv/)
   - Install [espeak-ng](https://github.com/espeak-ng/espeak-ng) in your system if you want it available as a fallback for unknown words/sounds. The upstream libraries may attempt to handle this, but results have varied.
   - Clone the repository:
        ```bash
        git clone https://github.com/remsky/Kokoro-FastAPI.git
        cd Kokoro-FastAPI
        ```
        
        Run the [model download script](https://github.com/remsky/Kokoro-FastAPI/blob/master/docker/scripts/download_model.py) if you haven't already
     
        Start directly via UV (with hot-reload)
        
        Linux and macOS
        ```bash
        ./start-cpu.sh OR
        ./start-gpu.sh 
        ```

        Windows
        ```powershell
        .\start-cpu.ps1 OR
        .\start-gpu.ps1 
        ```

</details>

<details open>
<summary> Up and Running? </summary>


Run locally as an OpenAI-Compatible Speech Endpoint
    
```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8880/v1", api_key="not-needed"
)

with client.audio.speech.with_streaming_response.create(
    model="kokoro",
    voice="af_sky+af_bella", #single or multiple voicepack combo
    input="Hello world!"
  ) as response:
      response.stream_to_file("output.mp3")
```
  
- The API will be available at http://localhost:8880
- API Documentation: http://localhost:8880/docs

- Web Interface: http://localhost:8880/web

<div align="center">
  <img src="assets/webui-screenshot.png" width="51.4%" alt="Web UI Screenshot">
  <img src="assets/docs-screenshot.png" width="46.6%" alt="API Documentation">
</div>

</details>

## Features 

### Core

<details>
<summary>OpenAI-Compatible Speech Endpoint</summary>

```python
# Using OpenAI's Python library
from openai import OpenAI
client = OpenAI(base_url="http://localhost:8880/v1", api_key="not-needed")
response = client.audio.speech.create(
    model="kokoro",  
    voice="af_bella+af_sky", # see /api/src/core/openai_mappings.json to customize
    input="Hello world!",
    response_format="mp3"
)

response.stream_to_file("output.mp3")
```
Or Via Requests:
```python
import requests


response = requests.get("http://localhost:8880/v1/audio/voices")
voices = [v["id"] for v in response.json()["voices"]]

# Generate audio
response = requests.post(
    "http://localhost:8880/v1/audio/speech",
    json={
        "model": "kokoro",  
        "input": "Hello world!",
        "voice": "af_bella",
        "response_format": "mp3",  # Supported: mp3, wav, opus, flac, aac, pcm
        "speed": 1.0
    }
)

# Save audio
with open("output.mp3", "wb") as f:
    f.write(response.content)
```

Quick tests (run from another terminal):
```bash
python examples/assorted_checks/test_openai/test_openai_tts.py # Test OpenAI Compatibility
python examples/assorted_checks/test_voices/test_all_voices.py # Test all available voices
```
</details>

<details>
<summary>Streaming Support</summary>

```python
# OpenAI-compatible streaming
from openai import OpenAI
client = OpenAI(
    base_url="http://localhost:8880/v1", api_key="not-needed")

# Stream to file
with client.audio.speech.with_streaming_response.create(
    model="kokoro",
    voice="af_bella",
    input="Hello world!"
) as response:
    response.stream_to_file("output.mp3")

# Stream to speakers (requires PyAudio)
import pyaudio
player = pyaudio.PyAudio().open(
    format=pyaudio.paInt16, 
    channels=1, 
    rate=24000, 
    output=True
)

with client.audio.speech.with_streaming_response.create(
    model="kokoro",
    voice="af_bella",
    response_format="pcm",
    input="Hello world!"
) as response:
    for chunk in response.iter_bytes(chunk_size=1024):
        player.write(chunk)
```

Or via requests:
```python
import requests

response = requests.post(
    "http://localhost:8880/v1/audio/speech",
    json={
        "input": "Hello world!",
        "voice": "af_bella",
        "response_format": "pcm"
    },
    stream=True
)

for chunk in response.iter_content(chunk_size=1024):
    if chunk:
        # Process streaming chunks
        pass
```

<p align="center">
  <img src="assets/gpu_first_token_timeline_openai.png" width="45%" alt="GPU First Token Timeline" style="border: 2px solid #333; padding: 10px; margin-right: 1%;">
  <img src="assets/cpu_first_token_timeline_stream_openai.png" width="45%" alt="CPU First Token Timeline" style="border: 2px solid #333; padding: 10px;">
</p>

Key Streaming Metrics:
- First token latency @ chunksize
    - ~300ms  (GPU) @ 400 
    - ~3500ms (CPU) @ 200 (older i7)
    - ~<1s    (CPU) @ 200 (M3 Pro)
- Adjustable chunking settings for real-time playback 

*Note: Artifacts in intonation can increase with smaller chunks*
</details>

<details>
<summary>Multiple Output Audio Formats</summary>

- mp3
- wav
- opus 
- flac
- aac
- pcm

<p align="center">
<img src="assets/format_comparison.png" width="80%" alt="Audio Format Comparison" style="border: 2px solid #333; padding: 10px;">
</p>

</details>

### Voices

<details>


... (truncated, 25419 more characters)

## pyproject.toml

```
[project]
name = "kokoro-fastapi"
version = "0.9.1-rc1"
description = "FastAPI TTS Service"
readme = "README.md"
requires-python = ">=3.10"
dependencies = [
    # Core dependencies
    "fastapi>=0.128.8",
    "starlette>=1.3.1",
    "uvicorn==0.34.0",
    "click>=8.0.0",
    "pydantic==2.10.4",
    "pydantic-settings==2.7.0",
    "python-dotenv==1.2.2",
    "sqlalchemy==2.0.27",
    # ML/DL Base
    "numpy>=1.26.0",
    "scipy==1.14.1",
    # Audio processing
    "soundfile==0.13.0",
    "inno-kokoro==0.2.0",
    "python-multipart>=0.0.20",
    "regex>=2025.10.22",
    "unicode-segmentation-rs>=0.3.3",
    # Utilities
    "aiofiles==23.2.1",
    "tqdm==4.67.1",
    "requests==2.33.0",
    "munch==4.0.0",
    "tiktoken==0.8.0",
    "loguru==0.7.3",
    "openai>=1.59.6",
    "mutagen>=1.47.0",
    "psutil>=6.1.1",
    "espeakng-loader==0.2.4",
    "kokoro==0.9.4",
    "transformers>=5.5.0,<6",
    "misaki[en,ja,ko,zh]==0.9.4",
    "pyopenjtalk-plus>=0.4.1 ; sys_platform == 'win32'",
    "spacy==3.8.5",
    "en-core-web-sm @ https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/en_core_web_sm-3.8.0-py3-none-any.whl",
    "inflect>=7.5.0",
    "phonemizer-fork>=3.3.2",
    "av>=14.2.0",
    "text2num>=2.5.1",
]

[project.optional-dependencies]
gpu = [
    "torch==2.8.0+cu126 ; platform_machine == 'x86_64'",
    "torch==2.8.0+cu129 ; platform_machine == 'aarch64'",
]
# Blackwell / RTX 50-series variant. cu128 wheels carry sm_120 kernels but
# drop Maxwell/Pascal, so this is a separate extra rather than the default.
# See #443. aarch64 already ships cu129 (Blackwell-capable) under both extras.
gpu-cu128 = [
    "torch==2.8.0+cu128 ; platform_machine == 'x86_64'",
    "torch==2.8.0+cu129 ; platform_machine == 'aarch64'",
]
cpu = ["torch==2.8.0"]
rocm = [
    "torch==2.8.0+rocm6.4",
    "pytorch-triton-rocm>=3.2.0",
]
test = [
    "pytest==8.3.5",
    "pytest-cov==6.0.0",
    "httpx==0.26.0",
    "pytest-asyncio==0.25.3",
    "tomli>=2.0.1",
    "jinja2>=3.1.6",
    "hypothesis==6.167.1",
]
# Integration test deps (faster-whisper, jiwer, soundfile, etc.) intentionally
# live in the tts-api-test-client image, not here. Run via:
#   docker compose -f docker/docker-compose.test.yml up --build \
#       --abort-on-container-exit --exit-code-from test-client

[tool.uv]
conflicts = [
    [
        { extra = "cpu" },
        { extra = "gpu" },
        { extra = "gpu-cu128" },
        { extra = "rocm" },
    ],
]
override-dependencies = [
    "triton>=3.5.1 ; platform_machine == 'aarch64'",
    "pyopenjtalk ; sys_platform != 'win32'",
]

[tool.uv.sources]
torch = [
    { index = "pytorch-cpu", extra = "cpu" },
    { index = "pytorch-cu126", extra = "gpu", marker = "platform_machine == 'x86_64'" },
    { index = "pytorch-cu129", extra = "gpu", marker = "platform_machine == 'aarch64'" },
    { index = "pytorch-cu128", extra = "gpu-cu128", marker = "platform_machine == 'x86_64'" },
    { index = "pytorch-cu129", extra = "gpu-cu128", marker = "platform_machine == 'aarch64'" },
    { index = "pytorch-rocm", extra = "rocm" },
]
pytorch-triton-rocm = [
    { index = "pytorch-rocm", extra = "rocm" },
]

[[tool.uv.index]]
name = "pytorch-cpu"
url = "https://download.pytorch.org/whl/cpu"
explicit = true

[[tool.uv.index]]
name = "pytorch-cu126"
url = "https://download.pytorch.org/whl/cu126"
explicit = true

[[tool.uv.index]]
name = "pytorch-cu128"
url = "https://download.pytorch.org/whl/cu128"
explicit = true

[[tool.uv.index]]
name = "pytorch-cu129"
url = "https://download.pytorch.org/whl/cu129"
explicit = true

[[tool.uv.index]]
name = "pytorch-rocm"
url = "https://download.pytorch.org/whl/rocm6.4"
explicit = true

[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[tool.setuptools]
package-dir = { "" = "api/src" }
packages.find = { where = ["api/src"], namespaces = true }

```

## package.json

```
{
  "type": "module",
  "scripts": {
    "test:web": "node web/tests/unit/index.test.mjs",
    "test:e2e": "playwright test",
    "gpu:build": "docker compose -f docker/gpu/docker-compose.yml build",
    "gpu:up": "docker compose -f docker/gpu/docker-compose.yml up",
    "gpu:down": "docker compose -f docker/gpu/docker-compose.yml down",
    "cpu:build": "docker compose -f docker/cpu/docker-compose.yml build",
    "cpu:up": "docker compose -f docker/cpu/docker-compose.yml up",
    "cpu:down": "docker compose -f docker/cpu/docker-compose.yml down",
    "rocm:build": "docker compose -f docker/rocm/docker-compose.yml build",
    "rocm:up": "docker compose -f docker/rocm/docker-compose.yml up",
    "rocm:down": "docker compose -f docker/rocm/docker-compose.yml down"
  },
  "devDependencies": {
    "@playwright/test": "^1.57.0"
  }
}

```

## Top-level layout

- .claude/ (dir, 5 files, ~226 lines)
- .codeql-config.yml (~10 lines)
- .coveragerc (~19 lines)
- .dockerignore (~39 lines)
- .gitattributes (~7 lines)
- .github/ (dir, 8 files, ~641 lines)
- .gitignore (~111 lines)
- .python-version (~1 lines)
- .ruff.toml (~12 lines)
- AGENTS.md (~50 lines)
- api/ (dir, 157 files, ~14592 lines)
- assets/ (dir, 18 files, ~0 lines)
- CHANGELOG.md (~478 lines)
- charts/ (dir, 13 files, ~494 lines)
- codecov.yml (~5 lines)
- CONTRIBUTING.md (~97 lines)
- debug.http (~23 lines)
- docker/ (dir, 19 files, ~1838 lines)
- docker-bake.hcl (~242 lines)
- docs/ (dir, 21 files, ~1222 lines)
- examples/ (dir, 95 files, ~9611 lines)
- githubbanner.png (~0 lines)
- LICENSE (~201 lines)
- package-lock.json (~75 lines)
- package.json (~19 lines)
- playwright.config.mjs (~17 lines)
- pyproject.toml (~138 lines)
- pytest.ini (~8 lines)
- README.md (~917 lines)
- scripts/ (dir, 3 files, ~416 lines)
- start-cpu.ps1 (~12 lines)
- start-cpu.sh (~25 lines)
- start-gpu.ps1 (~12 lines)
- start-gpu.sh (~17 lines)
- start-gpu_mac.sh (~20 lines)
- uv.lock (~4547 lines)
- VERSION (~1 lines)
- web/ (dir, 49 files, ~10415 lines)

