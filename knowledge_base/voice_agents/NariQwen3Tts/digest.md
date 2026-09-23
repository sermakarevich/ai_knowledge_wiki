> [[index|Wiki]] | [[summary|Summary]]
# nari-labs/nari-qwen3-tts — Digest

## 1. [[wiki/01-overview|Overview]]
**In one sentence:** Nari Qwen3-TTS is a single-H100 serving implementation of Qwen3-TTS 1.7B CustomVoice exposing streaming/non-streaming speech generation over HTTP plus WebSocket input streaming.
## Key points
- Serves `Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice` over HTTP (streaming and non-streaming) plus WebSocket-based incremental text input (README.md:11-14).
- Claims 10 RPS with sub-50 ms p95 time-to-first-audio on one NVIDIA H100 SXM, and sub-80 ms p95 TTFA even at 20 RPS (README.md:16-18).
- Publishes performance comparison chart and points methodology to the Nari Labs blog post and benchmark repository (README.md:20-29).
- Ships as a Docker image for Linux x86_64 H100 hosts requiring NVIDIA Container Toolkit and a CUDA 13.0-compatible driver, tested only with English as primary language (README.md:33-33).
- Selects behavior via `ttfa` / `balanced` / `throughput` profiles plus a strict partial YAML engine-config overlay resolved at startup (README.md:87-109).
- Exposes `GET /health`, `GET /ready`, `GET /v1/models`, `POST /v1/audio/speech`, and `WS /v1/audio/speech/ws` with an OpenAI Audio Speech request shape (README.md:115-128).
- Stays unready until CUDA Graph capture and a warm-up TTS request have both completed (README.md:144-145).

## 2. [[wiki/02-top-level-files|Top-Level Files]]
**In one sentence:** The top-level files pin the Python version and define the local Docker Compose runtime — build context, port mapping, model/profile defaults, GPU reservation, cache volume, and healthcheck — while excluding build and cache artifacts from git and Docker builds.
## Key points
- The repo pins Python to `3.12.13` via `.python-version:1`, so local and container builds share one interpreter version.
- `.dockerignore:1-10` excludes VCS, virtualenv, test, and build outputs (`.git/`, `.venv/`, `tests/`, `artifacts/`, `build/`, `dist/`, `*.egg-info/`, `__pycache__/`, `.pytest_cache/`, `.ruff_cache/`) from the Docker build context to keep images small.
- `.gitignore:1-7` excludes the same class of generated artifacts (`.venv/`, `build/`, `dist/`, `*.egg-info/`, `__pycache__/`, `.pytest_cache/`, `.ruff_cache/`) from version control.
- `docker-compose.yaml:2-9` defines a single service `nari-qwen3-tts` that builds from `context: .` with build arg `VCS_REF` defaulting to `unknown` and tags the image `nari-qwen3-tts:local`.
- `docker-compose.yaml:10-15` publishes container port `8000` as host port `8000` and sets runtime defaults `QWEN3_TTS_MODEL: Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice`, `QWEN3_TTS_PROFILE: balanced`, and `HF_TOKEN` defaulting to empty.
- `docker-compose.yaml:16-28` mounts the named volume `nari-qwen3-tts-cache` at `/home/nari/.cache`, raises the `nofile` ulimit to `65536/65536`, and reserves one NVIDIA GPU (`driver: nvidia`, `count: 1`, `capabilities: [gpu]`).
- `docker-compose.yaml:29-37` adds a healthcheck polling `http://127.0.0.1:8000/health` by `curl` every `15s` with `3s` timeout, `600s` start period, and `5` retries, and declares the `nari-qwen3-tts-cache` volume.

## The system in five moves
1. A single Qwen3-TTS CustomVoice model is served as low-TTFA speech generation over HTTP and WebSocket from one H100 host.
2. Latency/throughput behavior is selected up front via `ttfa` / `balanced` / `throughput` profiles with a strict engine-config overlay.
3. The runtime pins Python 3.12.13 and keeps git and Docker contexts clean of venv, build, and cache artifacts.
4. Local Docker Compose builds the image, maps port 8000, injects the model/profile/HF_TOKEN defaults, and reserves one NVIDIA GPU with a raised nofile limit and persistent cache volume.
5. The container gates traffic on `/health` and `/ready`, staying unready until CUDA Graph capture and a warm-up TTS request complete, then serves the OpenAI-shaped speech endpoints.
