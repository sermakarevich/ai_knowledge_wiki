> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Overview
**In one sentence:** Nari Qwen3-TTS is a single-H100 serving implementation of Qwen3-TTS 1.7B CustomVoice exposing streaming/non-streaming speech generation over HTTP plus WebSocket input streaming.
## Key points
- Serves `Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice` over HTTP (streaming and non-streaming) plus WebSocket-based incremental text input (README.md:11-14).
- Claims 10 RPS with sub-50 ms p95 time-to-first-audio on one NVIDIA H100 SXM, and sub-80 ms p95 TTFA even at 20 RPS (README.md:16-18).
- Publishes performance comparison chart and points methodology to the Nari Labs blog post and benchmark repository (README.md:20-29).
- Ships as a Docker image for Linux x86_64 H100 hosts requiring NVIDIA Container Toolkit and a CUDA 13.0-compatible driver, tested only with English as primary language (README.md:33-33).
- Selects behavior via `ttfa` / `balanced` / `throughput` profiles plus a strict partial YAML engine-config overlay resolved at startup (README.md:87-109).
- Exposes `GET /health`, `GET /ready`, `GET /v1/models`, `POST /v1/audio/speech`, and `WS /v1/audio/speech/ws` with an OpenAI Audio Speech request shape (README.md:115-128).
- Stays unready until CUDA Graph capture and a warm-up TTS request have both completed (README.md:144-145).
---
## Serving engine
Single-model server (`Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice`) with real-time playback target (README.md:11-14). Performance claim (README.md:16-18):

> It achieves **10 requests per second (RPS)** and **sub-50 ms p95 time-to-first-audio (TTFA)** while maintaining real-time playback on a **single NVIDIA H100 SXM**. Even at **20 RPS**, it sustains **sub-80 ms p95 TTFA**.

## Run targets
Docker run (README.md:36-42):

```bash
docker run --rm --gpus all \
  -p 8000:8000 \
  -e HF_TOKEN \
  -e QWEN3_TTS_PROFILE=ttfa \
  -v nari-qwen3-tts-cache:/home/nari/.cache \
  ghcr.io/nari-labs/nari-qwen3-tts:latest
```

Readiness probe after model loading and CUDA Graph capture (README.md:48-49):

```bash
curl --fail http://127.0.0.1:8000/ready
```

uv run requires pinned Python/uv versions (` .python-version`, `pyproject.toml`) with frozen lockfile `uv.lock` (README.md:61-62):

```bash
sudo apt-get install -y build-essential libsndfile1 sox
uv sync --frozen --extra codec --extra cuda --extra serving
uv run --frozen nari-qwen3-tts-server --profile ttfa
```

Python import uses underscores while the distribution name uses hyphens (README.md:79-83):

```python
from nari_qwen3_tts import ModelAssetConfig, open_model
```

## Profiles and configuration
| Profile | Effect (README.md:87-92) |
|---|---|
| `ttfa` | Prioritizes time to first audio; latency-oriented scheduling, smaller initial Codec chunks |
| `balanced` | Default container profile; balances first-audio latency and sustained throughput |
| `throughput` | Larger Codec chunks and batches; prioritizes aggregate throughput under load |

Selection and overlay (README.md:94-109):

| Flag / variable | Meaning |
|---|---|
| `QWEN3_TTS_PROFILE` | Docker profile selector (`ttfa`, `balanced`, `throughput`) |
| `--profile` | `nari-qwen3-tts-server` profile selector |
| `QWEN3_TTS_MODEL_CACHE_DIR` | Model cache dir in Docker |
| `QWEN3_TTS_LOCAL_FILES_ONLY=1` / `--local-files-only` | Prevent downloads at startup after model is cached |
| `--engine-config /path/to/engine.yaml` | Strict partial YAML overlay; `extends: ttfa\|balanced\|throughput` names the packaged base |

Unknown keys, invalid capture lists, and profile/base mismatches fail before model loading; resolved config and SHA-256 print at startup (README.md:108-109).

## API surface
Endpoints (README.md:115-119):

- `GET /health`
- `GET /ready`
- `GET /v1/models`
- `POST /v1/audio/speech`
- `WS /v1/audio/speech/ws`

HTTP example supports only the listed model, `wav`/`pcm` output, `speed: 1.0`, plus Nari controls such as `language` (README.md:126-142):

```bash
curl http://127.0.0.1:8000/v1/audio/speech \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice",
    "input": "Hello from Nari Labs.",
    "voice": "ryan",
    "language": "english",
    "response_format": "wav",
    "stream": false
  }' \
  --output speech.wav
```

Live-text protocol documented in `docs/websocket.md` (README.md:121-122). No files were noted as truncated in the chunk.
**Covers:** README.md (project TL;DR, Docker/uv run targets, profiles, API surface)
