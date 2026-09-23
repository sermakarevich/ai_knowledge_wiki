> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Overview
**In one sentence:** Kokoro-FastAPI is a Dockerized FastAPI wrapper for the Kokoro-82M text-to-speech model that exposes an OpenAI-compatible speech endpoint for fast multi-language speech generation (README.md:22).
## Key points
- The project is a Dockerized FastAPI wrapper for [Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M) that generates "hours of high quality speech in minutes" (README.md:22).
- It exposes an OpenAI-compatible Speech endpoint with English (US/GB), Spanish, French, Hindi, Italian, Japanese, Brazilian Portuguese, and Mandarin Chinese support (README.md:24-25).
- Voice features include custom voicepack generation via Inno Clone-Tuner, inline multi-speaker generation with voice mixing plus aliasing weighted combinations, and SSML support (README.md:26, README.md:28).
- It provides an optional integrated WebUI with read-along long-generation, per-word or per-chunk timestamped captions, and phoneme endpoints for text-to-phonemes and phonemes-to-audio (README.md:27, README.md:29-30).
- Prebuilt multiplatform images cover CPU and NVIDIA GPU CUDA on linux/amd64 plus linux/arm64, AMD GPU ROCm experimental on linux/amd64 only, with Apple Silicon MPS supported when running directly via UV with no image (README.md:31-34).
- Three run paths are documented — `docker run`, `docker compose`, and direct run via `uv` — all serving the API at `http://localhost:8880` with docs at `/docs` and the Web Interface at `/web` (README.md:56-88, README.md:99-118, README.md:136-149, README.md:173-177).
- Streaming is OpenAI-compatible with first-token latency of ~300ms on GPU at chunksize 400, ~3500ms on older-i7 CPU at 200, and ~<1s on M3 Pro CPU at 200, and output formats are `mp3`, `wav`, `opus`, `flac`, `aac`, `pcm` (README.md:298-305, README.md:309-316).
---
## Purpose
Dockerized FastAPI wrapper for [Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M) text-to-speech model; generate hours of high quality speech in minutes (README.md:22).

Badges pin `kokoro-0.9.4`, `misaki-0.9.4`, and model `1.0::41e5892` (README.md:15-17).

## Capabilities
Feature list verbatim from the chunk (README.md:24-34):

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

## Run modes
### Quickest Start — `docker run` (README.md:54-90)
Pre-built multi-arch images with models baked in; `:latest` is available but pinning to a release tag is recommended for stable usage (README.md:56-58).

| Target | Command (README.md:60-88) |
|---|---|
| No GPU (laptop, CPU-only server) | `docker run -p 8880:8880 ghcr.io/remsky/kokoro-fastapi-cpu:latest` |
| NVIDIA GTX 900 through RTX 40 (ships cu126) | `docker run --gpus all -p 8880:8880 ghcr.io/remsky/kokoro-fastapi-gpu:latest` |
| NVIDIA RTX 50-series / Blackwell (ships cu128) | `docker run --gpus all -p 8880:8880 ghcr.io/remsky/kokoro-fastapi-gpu:latest-cu128` |
| NVIDIA arm64 (Jetson, GH200; same tag, ships cu129) | `docker run --gpus all -p 8880:8880 ghcr.io/remsky/kokoro-fastapi-gpu:latest` |
| AMD GPU (ROCm, experimental, x86_64 only) | `docker run --device=/dev/kfd --device=/dev/dri -p 8880:8880 ghcr.io/remsky/kokoro-fastapi-rocm:latest` |
| Apple Silicon (native MPS clone; CPU image also works) | `./start-gpu_mac.sh` |

`gpu:latest` is the same image as `gpu:latest-cu126`; configuration is via environment variables, see `docs/configuration.md` (README.md:90).

### Quick Start — `docker compose` (README.md:94-121)
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
Requires Docker; the compose setup is the full setup including UI (README.md:98-99). The configuration guide at `docs/configuration.md` covers image vs build, volume mounts, and env vars (README.md:120).

### Direct Run — via `uv` (README.md:122-150)
Prerequisites: `astral-uv`, `espeak-ng` as fallback for unknown words/sounds, then clone (README.md:125-132):
```bash
git clone https://github.com/remsky/Kokoro-FastAPI.git
cd Kokoro-FastAPI
```
Run the model download script at `docker/scripts/download_model.py` if models are not already downloaded, then start directly via UV with hot-reload (README.md:134-136):

| OS | Command (README.md:138-148) |
|---|---|
| Linux and macOS | `./start-cpu.sh` OR `./start-gpu.sh` |
| Windows | `.\start-cpu.ps1` OR `.\start-gpu.ps1` |

### Up and Running (README.md:152-183)
OpenAI-compatible usage (README.md:158-171):
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

| Endpoint | Value (README.md:173-177) |
|---|---|
| API | `http://localhost:8880` |
| API Documentation | `http://localhost:8880/docs` |
| Web Interface | `http://localhost:8880/web` |

## Core endpoint
OpenAI-library usage with exact parameter names `model`, `voice`, `input`, `response_format` (README.md:192-204):
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
Requests usage (README.md:205-228):
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
Quick tests run from another terminal (README.md:230-234):
```bash
python examples/assorted_checks/test_openai/test_openai_tts.py # Test OpenAI Compatibility
python examples/assorted_checks/test_voices/test_all_voices.py # Test all available voices
```

## Streaming
OpenAI-compatible streaming to file and to speakers with exact parameters `model`, `voice`, `response_format`, `input`, `chunk_size` (README.md:241-291):
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
Requests streaming variant (README.md:273-291):
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

Key Streaming Metrics (README.md:298-305):

| Metric | Value |
|---|---|
| First token latency, GPU @ 400 | ~300ms |
| First token latency, CPU older i7 @ 200 | ~3500ms |
| First token latency, CPU M3 Pro @ 200 | ~<1s |
| Chunking | Adjustable chunking settings for real-time playback |

Note: artifacts in intonation can increase with smaller chunks (README.md:305).

## Output formats
Supported values (README.md:309-316):

- mp3
- wav
- opus
- flac
- aac
- pcm

## Truncation note
The source chunk is cut mid-section at `### Voices` / `<details>` (chunk 01-overview.md:324-327) and the trailing `Macro components` list is cut after `top-level-files/` (chunk 01-overview.md:328-331); no claims are made about voice details or any module beyond the cut.

**Covers:** README.md (project purpose, feature list, docker run / compose / uv run paths, OpenAI-compatible usage, streaming, output formats) as given in `chunks/01-overview.md`
