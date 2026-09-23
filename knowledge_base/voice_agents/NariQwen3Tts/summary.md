# Technical Analysis: nari-labs/nari-qwen3-tts

**Repository:** https://github.com/nari-labs/nari-qwen3-tts
**Version analyzed:** unknown
**Date:** 2026-09-22
**Wiki:** [[index]]

## 1. Overview

Problem space: serving a 1.7B text-to-speech model with low time-to-first-audio under concurrent load on a single GPU, without multi-node inference infrastructure. The target metric is first-audio latency at sustained request rate (p95 TTFA at 10–20 RPS), plus real-time playback once streaming starts.

How the repo addresses it: it ships a single-model server for `Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice` exposing HTTP (streaming and non-streaming) plus WebSocket incremental text input with an OpenAI Audio Speech request shape (README.md:11-14, README.md:115-128). Behavior is selected via `ttfa` / `balanced` / `throughput` profiles plus a strict partial YAML engine-config overlay resolved at startup (README.md:87-109). Startup gates readiness on CUDA Graph capture and a warm-up TTS request (README.md:144-145). Distribution is a Docker image for Linux x86_64 H100 hosts requiring NVIDIA Container Toolkit and a CUDA 13.0-compatible driver, with English as the tested primary language (README.md:33-33); a `uv`-based local run path is also documented (README.md:61-62).

Primary user: an operator deploying GPU-backed TTS inference behind HTTP/WebSocket clients.

## 2. High-Level Architecture

```
                  ┌─────────────────────────────┐
                  │  Profile + engine.yaml       │
                  │  overlay (startup-resolved)  │
                  └──────────────┬──────────────┘
                                 ▼
Client ──► HTTP /v1/audio/speech ──► Single-model server ──► Codec chunker ──► wav/pcm audio
   │      WS /v1/audio/speech/ws      (CustomVoice 1.7B)         │
   │         │  ▲                         │                     ▼
   │         │  │ incremental text         ▼               streaming frames
   │         └──┘                    CUDA Graph capture
   │                                  + warm-up gate
   ▼
GET /health ─ ► liveness (compose healthcheck target)
GET /ready ── ► readiness (post-capture + warm-up)
GET /v1/models ► model listing
```

Data-flow narrative:

1. Operator selects a base profile (`ttfa`, `balanced`, `throughput`) via `QWEN3_TTS_PROFILE` or `--profile`, optionally overlaid with a strict partial YAML engine config naming the base via `extends` (README.md:94-109).
2. At startup the resolved config and its SHA-256 print; unknown keys, invalid capture lists, and profile/base mismatches fail before model loading (README.md:108-109).
3. The server loads the single pinned model `Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice` (docker-compose.yaml:13), performs CUDA Graph capture, then runs a warm-up TTS request; `/ready` stays unready until both complete (README.md:144-145).
4. Inference requests arrive as `POST /v1/audio/speech` (one-shot or streamed) or as incremental text over `WS /v1/audio/speech/ws`, with the live-text protocol documented in `docs/websocket.md` (README.md:115-122).
5. The codec stage emits audio in profile-sized chunks — smaller initial chunks under `ttfa`, larger chunks/batches under `throughput`, balanced by default — in `wav` or `pcm` at `speed: 1.0` with Nari controls such as `language` (README.md:87-92, README.md:126-142).
6. Liveness is polled separately: the compose healthcheck curls `/health` every 15 s (docker-compose.yaml:29-37), while `/ready` is the deployment gate.

Persistent state lives in the model/tokenizer cache: the named volume `nari-qwen3-tts-cache` mounted at `/home/nari/.cache` (docker-compose.yaml:16-28), mirrored by the `-v nari-qwen3-tts-cache:/home/nari/.cache` Docker run flag (README.md:36-42). No database or additional persistent store is attested in the covered pages.

## 3. The Profile-Configured Serving Engine

The repo's central concept is a single-model serving engine whose latency/throughput tradeoff is parameterized by a named profile plus a validated startup overlay, rather than by per-request tuning.

Representation: the engine serves exactly one model id, `Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice`, with real-time playback target (README.md:11-14). Its operating point is one of three named kinds, with effects documented at README.md:87-92:

- `ttfa` — prioritizes time to first audio; latency-oriented scheduling, smaller initial Codec chunks (README.md:87-92).
- `balanced` — default container profile; balances first-audio latency and sustained throughput (README.md:87-92).
- `throughput` — larger Codec chunks and batches; prioritizes aggregate throughput under load (README.md:87-92).

Key queries against the engine are its probe and model endpoints (README.md:115-119): `GET /health`, `GET /ready`, `GET /v1/models`, `POST /v1/audio/speech`, `WS /v1/audio/speech/ws`. Verbatim performance claim (README.md:16-18):

> It achieves **10 requests per second (RPS)** and **sub-50 ms p95 time-to-first-audio (TTFA)** while maintaining real-time playback on a **single NVIDIA H100 SXM**. Even at **20 RPS**, it sustains **sub-80 ms p95 TTFA**.

Supporting methodology and comparison chart are pointed at the Nari Labs blog post and benchmark repository (README.md:20-29); the covered pages reproduce no methodology detail.

## 4. LLM / External Service Integration

The repo calls no chat-LLM or third-party inference API. The only external model dependency is the weights download for `Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice`, authenticated by `HF_TOKEN` (README.md:36-42, docker-compose.yaml:10-15). Required vs optional:

- Required at first fetch: `HF_TOKEN` (passed as `-e HF_TOKEN` in the Docker run example at README.md:36-42; compose defaults it to empty via `${HF_TOKEN:-}` at docker-compose.yaml:10-15, so the daemon starts but model fetch fails without a token on a cold cache).
- Optional / situational: `QWEN3_TTS_MODEL_CACHE_DIR` (Docker model cache dir override, README.md:94-109); `QWEN3_TTS_LOCAL_FILES_ONLY=1` / `--local-files-only` to prevent downloads at startup after the model is cached (README.md:94-109).

Env-var summary is tabulated in section 8. No provider SDK, API base URL, or per-call billing is attested.

## 5. The Profile-Resolved Serve Pipeline

Primary workflow: resolve profile plus overlay, capture graphs, warm up, then serve HTTP/WebSocket synthesis. No per-function file:line map is available — the covered component pages cite only README.md and compose/top-level lines — so each step is cited at the finest granularity the wiki provides.

1. Select profile: set `QWEN3_TTS_PROFILE` (`ttfa` | `balanced` | `throughput`) for Docker (README.md:94-109) or `--profile` for the `nari-qwen3-tts-server` binary (README.md:94-109). Compose default is `balanced` (docker-compose.yaml:10-15).
2. Optionally supply overlay: pass `--engine-config /path/to/engine.yaml` whose `extends: ttfa|balanced|throughput` names the packaged base (README.md:94-109).
3. Validate before loading: unknown keys, invalid capture lists, and profile/base mismatches fail before model loading; resolved config and SHA-256 print at startup (README.md:108-109).
4. Load model and capture: fetch (or reuse from cache) `Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice` (docker-compose.yaml:13), run CUDA Graph capture (README.md:48-49, README.md:144-145).
5. Warm up and gate: execute a warm-up TTS request; `/ready` remains unready until capture and warm-up both complete (README.md:144-145). Probe with `curl --fail http://127.0.0.1:8000/ready` (README.md:48-49).
6. Serve synthesis: accept `POST /v1/audio/speech` with OpenAI Audio Speech shape (`model`, `input`, `voice`, plus `language`, `response_format`, `stream`) (README.md:126-142) or incremental text over `WS /v1/audio/speech/ws` per `docs/websocket.md` (README.md:121-122); emit `wav`/`pcm` chunked per the active profile (README.md:87-92).
7. Operate: liveness via `GET /health` (compose curls it every 15 s with 3 s timeout, 600 s start period, 5 retries per docker-compose.yaml:29-37); reuse the cache volume across restarts (docker-compose.yaml:16-28); set `QWEN3_TTS_LOCAL_FILES_ONLY=1` to run offline once cached (README.md:94-109).

## 6. Key Files

Coverage note: the in-scope wiki covers 2 component pages (README-level behavior plus 4 top-level files). The table below lists every file attested there; it is exhaustive relative to the allowed sources, not relative to the repository.

| File | Lines | What It Does |
|---|---|---|
| README.md | 11-14 | Declares single-model server scope and streaming/non-streaming plus WebSocket input |
| README.md | 16-18 | States 10 RPS / sub-50 ms p95 TTFA and 20 RPS / sub-80 ms p95 TTFA claims |
| README.md | 20-29 | Points performance methodology to blog post and benchmark repository |
| README.md | 33-33 | States H100 / CUDA 13.0 driver / English-primary support constraints |
| README.md | 36-42 | Documents Docker run target (ports, HF_TOKEN, profile, cache volume) |
| README.md | 48-49 | Documents readiness probe after loading and graph capture |
| README.md | 61-62 | Documents uv run prerequisites (pinned Python/uv, frozen lockfile) |
| README.md | 79-83 | Documents Python import shape (`nari_qwen3_tts`, `ModelAssetConfig`, `open_model`) |
| README.md | 87-109 | Defines profiles, selectors, cache/local-only vars, engine-config overlay and fail-fast validation |
| README.md | 115-128 | Enumerates HTTP/WebSocket endpoints and OpenAI Speech request shape |
| README.md | 126-142 | Gives curl synthesis example (model, voice, language, wav, speed) |
| README.md | 144-145 | States unready-until-capture-plus-warm-up gate |
| docs/websocket.md | (cited, unnumbered) | Documents live-text WebSocket protocol (via README.md:121-122) |
| docker-compose.yaml | 1-37 | Defines local runtime: build, ports, env defaults, cache volume, GPU reservation, healthcheck |
| .python-version | 1 | Pins interpreter to 3.12.13 |
| .dockerignore | 1-10 | Excludes VCS/venv/test/build outputs from Docker context |
| .gitignore | 1-7 | Excludes venv/build/cache artifacts from version control |

## 7. Dependencies

Only constraints stated verbatim in the covered pages are listed; the wiki reproduces no `pyproject.toml` version pins.

| Package | Version constraint | Purpose |
|---|---|---|
| python | `== 3.12.13` (`.python-version:1`) | Pinned interpreter shared by local and container builds |
| nari-qwen3-tts (uv extras: `codec`) | exact string not stated (`uv sync --frozen --extra codec`, README.md:61-62) | Codec support for audio chunking/encoding |
| nari-qwen3-tts (uv extras: `cuda`) | exact string not stated (`--extra cuda`, README.md:61-62) | CUDA execution support |
| nari-qwen3-tts (uv extras: `serving`) | exact string not stated (`--extra serving`, README.md:61-62) | HTTP/WebSocket serving stack |
| build-essential | version not pinned (`sudo apt-get install -y build-essential`, README.md:61-62) | Native build toolchain for local install |
| libsndfile1 | version not pinned (same apt line) | Audio file I/O |
| sox | version not pinned (same apt line) | Audio processing utility |
| NVIDIA Container Toolkit | version not stated (README.md:33-33) | GPU passthrough for Docker (`--gpus all`) |
| CUDA 13.0-compatible driver | `CUDA 13.0-compatible` (README.md:33-33) | Host driver requirement for H100 image |
| uv | `pinned` (versions per `pyproject.toml`, exact numbers not reproduced; README.md:61-62) | Reproducible sync with frozen `uv.lock` |

## 8. CLI / Usage Surface

Entry points:

| Entry point | Form | Source |
|---|---|---|
| Docker image | `ghcr.io/nari-labs/nari-qwen3-tts:latest` | README.md:36-42 |
| Compose service | `nari-qwen3-tts` (builds `nari-qwen3-tts:local`) | docker-compose.yaml:2-9 |
| Server binary | `nari-qwen3-tts-server --profile ttfa` | README.md:36-42 |
| Python API | `from nari_qwen3_tts import ModelAssetConfig, open_model` | README.md:79-83 |

Commands:

```bash
docker run --rm --gpus all -p 8000:8000 -e HF_TOKEN -e QWEN3_TTS_PROFILE=ttfa -v nari-qwen3-tts-cache:/home/nari/.cache ghcr.io/nari-labs/nari-qwen3-tts:latest
curl --fail http://127.0.0.1:8000/ready
sudo apt-get install -y build-essential libsndfile1 sox
uv sync --frozen --extra codec --extra cuda --extra serving
uv run --frozen nari-qwen3-tts-server --profile ttfa
```

Env vars:

| Variable | Default | Meaning |
|---|---|---|
| `QWEN3_TTS_PROFILE` | `balanced` (compose, docker-compose.yaml:10-15) | Base profile selector (`ttfa` \| `balanced` \| `throughput`) |
| `HF_TOKEN` | empty (`${HF_TOKEN:-}`, docker-compose.yaml:10-15) | Hugging Face token for model fetch |
| `QWEN3_TTS_MODEL` | `Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice` (docker-compose.yaml:10-15) | Model id served |
| `QWEN3_TTS_MODEL_CACHE_DIR` | not stated | Model cache dir in Docker (README.md:94-109) |
| `QWEN3_TTS_LOCAL_FILES_ONLY` | unset (`=1` enables) | Prevent downloads at startup after caching (README.md:94-109) |

Config / flags:

| Flag / key | Meaning |
|---|---|
| `--profile ttfa\|balanced\|throughput` | Server profile selector (README.md:94-109) |
| `--engine-config /path/to/engine.yaml` | Strict partial YAML overlay (README.md:94-109) |
| `--local-files-only` | Offline mode once cached (README.md:94-109) |
| `extends: ttfa\|balanced\|throughput` | Overlay header naming the packaged base (README.md:94-109) |

HTTP surface: `GET /health`, `GET /ready`, `GET /v1/models`, `POST /v1/audio/speech`, `WS /v1/audio/speech/ws` (README.md:115-119).

## 9. Extensibility Points

Attested extension seams, each tied to the file or control the covered pages name:

- Latency/throughput tradeoff: add or retune a packaged profile or its codec chunk/batch parameters; overlay via `--engine-config` with `extends` naming the base rather than forking the server (README.md:87-109). Validation rejects unknown keys, so new knobs require widening the strict schema first.
- Model/cache lifecycle: redirect the cache with `QWEN3_TTS_MODEL_CACHE_DIR` or pin offline runs with `QWEN3_TTS_LOCAL_FILES_ONLY=1` / `--local-files-only` (README.md:94-109); the compose mount `nari-qwen3-tts-cache:/home/nari/.cache` (docker-compose.yaml:16-28) is the persistence seam for pre-seeded caches.
- Client protocol: extend synthesis controls (`voice`, `language`, `response_format`, `stream`, `speed`) on `POST /v1/audio/speech` (README.md:126-142) or the incremental-text framing in `docs/websocket.md` (README.md:121-122) without changing the serve pipeline.
- Runtime topology: the compose service (`docker-compose.yaml:1-37`) is the seam for ports, `nofile` ulimits, GPU `count`, and healthcheck timing; the Python import seam is `nari_qwen3_tts.ModelAssetConfig` / `open_model` (README.md:79-83).
- Not attested in scope: internal class/function extension points (engine, scheduler, codec, graph capture) have no file:line coverage in the two wiki pages, so no finer seam can be grounded here.

## 10. Limitations and Gotchas

- **Single-model, single-GPU envelope:** only `Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice` on Linux x86_64 H100 hosts with NVIDIA Container Toolkit and a CUDA 13.0-compatible driver is documented (README.md:11-14, README.md:33-33, docker-compose.yaml:16-28); other GPUs, model ids, and output settings beyond the `wav`/`pcm`, `speed: 1.0` example are unattested.
- **Slow, gated startup:** `/ready` stays unready until CUDA Graph capture and a warm-up TTS request complete (README.md:144-145), and the compose healthcheck allows a 600 s start period (docker-compose.yaml:29-37) — readiness probes with short timeouts will flap during model load.
- **Strict startup validation fails fast:** unknown overlay keys, invalid capture lists, and profile/base mismatches abort before model loading, with only the resolved config and SHA-256 printed (README.md:108-109) — a typo in `engine.yaml` costs a full restart cycle.
- **Cold cache requires network plus token:** first start downloads weights with `HF_TOKEN` (README.md:36-42); compose defaults the token to empty (docker-compose.yaml:10-15), so a fresh volume without the variable set fails. Set `QWEN3_TTS_LOCAL_FILES_ONLY=1` only after the cache is warm (README.md:94-109).
- **English-primary testing:** the image is tested only with English as primary language (README.md:33-33); non-English `language` values are a documented control (README.md:126-142) but their quality is not evidenced in scope.
- **Thin wiki coverage:** only README-level behavior and 4 top-level files are covered by the in-scope pages; internals (scheduler, CUDA-graph code, codec, WebSocket framing) and exact Python dependency pins are not grounded here and must be read from the repo before modifying them.

## 11. How It Compares to Alternatives

The covered component pages name no competing TTS servers, so a grounded feature comparison cannot be written from the allowed sources. Related references cited in the wiki, not alternatives:

- Nari Labs blog post — pointed to as the performance methodology source (README.md:20-29).
- Nari benchmark repository — pointed to alongside the performance comparison chart (README.md:20-29).
- Upstream weights `Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice` — the single served model id (README.md:11-14, docker-compose.yaml:10-15); the repo is a serving implementation around it, not a model release.
- Generic `uv`-plus-Docker Python serving pattern (pinned interpreter, frozen lockfile, extras-gated install per README.md:61-62) — shared packaging practice, not a named rival.

Positioning sentence: within the evidence available, this repo is a single-model, profile-tuned H100 serving wrapper for Qwen3-TTS CustomVoice, differentiated by its TTFA-oriented profiles, graph-capture plus warm-up readiness gate, and OpenAI-shaped HTTP/WebSocket surface — not by model novelty.

## Appendix: Selected Code Snippets

Docker run (README.md:36-42):

```bash
docker run --rm --gpus all \
  -p 8000:8000 \
  -e HF_TOKEN \
  -e QWEN3_TTS_PROFILE=ttfa \
  -v nari-qwen3-tts-cache:/home/nari/.cache \
  ghcr.io/nari-labs/nari-qwen3-tts:latest
```

Local run (README.md:61-62):

```bash
sudo apt-get install -y build-essential libsndfile1 sox
uv sync --frozen --extra codec --extra cuda --extra serving
uv run --frozen nari-qwen3-tts-server --profile ttfa
```

Synthesis request (README.md:126-142):

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

Compose service (docker-compose.yaml:1-37):

```yaml
services:
  nari-qwen3-tts:
    init: true
    ipc: host
    build:
      context: .
      args:
        VCS_REF: ${VCS_REF:-unknown}
    image: nari-qwen3-tts:local
    ports:
      - "8000:8000"
    environment:
      QWEN3_TTS_MODEL: Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice
      QWEN3_TTS_PROFILE: balanced
      HF_TOKEN: ${HF_TOKEN:-}
    volumes:
      - nari-qwen3-tts-cache:/home/nari/.cache
    ulimits:
      nofile:
        soft: 65536
        hard: 65536
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    healthcheck:
      test: ["CMD", "curl", "--fail", "--silent", "http://127.0.0.1:8000/health"]
      interval: 15s
      timeout: 3s
      start_period: 600s
      retries: 5

volumes:
  nari-qwen3-tts-cache:
```
