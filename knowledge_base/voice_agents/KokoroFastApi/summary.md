# Technical Analysis: remsky/Kokoro-FastAPI

**Repository:** https://github.com/remsky/Kokoro-FastAPI
**Version analyzed:** 0.9.1-rc1 (`VERSION:1`)
**Date:** 2026-09-22
**Wiki:** [[index]]

## 1. Overview / What Problem It Solves

Self-hosting the Kokoro-82M text-to-speech model requires wiring model weights, phonemization, audio encoding, streaming, and a client-compatible API. This repo packages that stack as a Dockerized FastAPI service exposing an OpenAI-compatible speech endpoint (`README.md:22`, `README.md:158-171`). It adds multi-language synthesis (English US/GB, Spanish, French, Hindi, Italian, Japanese, Brazilian Portuguese, Mandarin Chinese), voice mixing and aliasing, SSML input, per-word/per-chunk timestamped captions, phoneme endpoints, and an optional integrated WebUI with read-along long-form generation (`README.md:24-30`). The primary user is a developer or small team that wants a drop-in local replacement for the OpenAI `audio.speech` API with GPU or CPU execution and no per-token billing.

## 2. High-Level Architecture

```
              ┌─────────────────────────────┐
              │  Clients: OpenAI SDK /       │
              │  requests / WebUI (/web)     │
              └──────────────┬──────────────┘
                             │ HTTP :8880
                             ▼
              ┌─────────────────────────────┐
              │  FastAPI: api/src/routers/   │
              │  openai_compatible.py (main  │
              │  surface) (AGENTS.md:20-28)  │
              └──────────────┬──────────────┘
                             ▼
              ┌─────────────────────────────┐
              │  api/src/services/: TTS      │
              │  orchestration, audio        │
              │  encoding/streaming,         │
              │  text_processing/            │
              └──────────────┬──────────────┘
                             ▼
              ┌─────────────────────────────┐
              │  api/src/inference/: model   │
              │  backends, model + voice     │
              │  managers (AGENTS.md:20-28)  │
              └──────────────┬──────────────┘
                             ▼
              ┌─────────────────────────────┐
              │  Kokoro-82M weights +        │
              │  voices (api/src/models/v1_0,│
              │  VOICES_DIR=src/voices/v1_0) │
              └─────────────────────────────┘
   Config side-channel: api/src/core/ (config.py, paths.py,
   openai_mappings.json) ──► routers + services
```

Data flow: (1) client POSTs `{model, voice, input, response_format, speed}` to `/v1/audio/speech` (`README.md:205-228`); (2) the router resolves the voice expression against `api/src/core/openai_mappings.json` (`README.md:112`); (3) services chunk text (tunable chunk size; first-token latency ~300ms on GPU at chunksize 400, ~3500ms on older-i7 CPU at 200, <1s on M3 Pro at 200) and run inference (`README.md:298-305`); (4) audio is encoded to `mp3`, `wav`, `opus`, `flac`, `aac`, or `pcm` (`README.md:309-316`); (5) bytes return either buffered or as an OpenAI-style streaming response consumed via `with_streaming_response.create(...)` or chunked `requests` iteration (`README.md:241-291`); (6) the WebUI at `/web` serves read-along generation and caption display against the same endpoints (`README.md:173-177`, `README.md:27`). Persistent state lives in model weight files under `api/src/models/v1_0` and voice data under `VOICES_DIR=src/voices/v1_0` (`start-cpu.sh:5-12`); ephemeral audio lands in `api/temp_files/` (git-ignored, `.gitignore:26-73`). No database is evidenced in the available pages.

## 3. The Voicepack

The central concept is the voicepack: a named voice identity referenced by id (e.g. `af_bella`) that can be combined inline with `+`-weighted mixing (`af_bella+af_sky`, `af_sky+af_bella`) and aliased to custom names (`README.md:158-171`, `README.md:106-119`). Representation: voice data files under `VOICES_DIR=src/voices/v1_0` (`start-cpu.sh:5-12`), with id-to-definition mapping in `api/src/core/openai_mappings.json` (customizable per `README.md:112`). Named kinds evidenced: single voicepack (`af_bella`); multi-speaker / mixed combination (`af_bella+af_sky`); aliased weighted combination (`README.md:28`); custom voicepacks generated externally via Inno Clone-Tuner (`README.md:26`). Key query: listing available voices is a GET with exact shape:

```python
response = requests.get("http://localhost:8880/v1/audio/voices")
voices = [v["id"] for v in response.json()["voices"]]
```

(`README.md:205-228`). Voice tags are gated behind an opt-in setting, default-on `enable_voice_tags` (`AGENTS.md:37-42`).

## 4. LLM / External Service Integration

The repo calls no LLM and no paid external API at inference time. Synthesis runs locally against baked-in or auto-downloaded Kokoro-82M weights (`README.md:56-58`, `README.md:62-66`). The only external network interactions evidenced are build/download-time: pulling prebuilt images from `ghcr.io/remsky/kokoro-fastapi-*` (`README.md:60-88`), running `python docker/scripts/download_model.py --output api/src/models/v1_0` (`README.md:62-66`), and registry cache refs in the bake file (`docker-bake.hcl:531-556`). No API keys are required: the OpenAI client is pointed at the local server with `api_key="not-needed"` (`README.md:158-171`). No provider-specific env vars are evidenced in the available pages.

## 5. The Speech Synthesis Pipeline

Reconstructed from the documented usage path and the `AGENTS.md:20-28` layout map (`routers/` → `services/` → `inference/`, config in `core/`): (1) ingress — OpenAI-compatible request arrives at `api/src/routers/openai_compatible.py`, the documented main surface, with parameters `model`, `voice`, `input`, `response_format` (`README.md:192-204`); (2) voice resolution — the `voice` expression is resolved via `api/src/core/openai_mappings.json`, including mixed (`af_bella+af_sky`) and aliased forms (`README.md:106-119`); (3) text processing — `api/src/services/text_processing/` prepares text, phonemes, or SSML (phoneme endpoints generate phonemes from text or audio from phonemes, `README.md:29-30`); (4) chunked inference — `api/src/inference/` model backends synthesize per chunk with adjustable chunking; smaller chunks lower latency but increase intonation artifacts (`README.md:298-305`); (5) encoding and delivery — `api/src/services/` audio encoding/streaming emits `mp3`, `wav`, `opus`, `flac`, `aac`, or `pcm`, buffered via `client.audio.speech.create(...)` or streamed via `with_streaming_response.create(...)` / `stream=True` chunk iteration (`README.md:241-291`); (6) optional caption path — per-word or per-chunk timestamped captions are generated alongside audio (`README.md:29-30`). Per-function `file.py:line` citations below router level are not present in the available component pages, which cover only the macro layout, not the service/inference internals.

## 6. Key Files

| File | Lines | What It Does |
|---|---|---|
| `README.md` | whole (usage excerpts :22-:316) | Feature list, three run paths, OpenAI-compatible usage, streaming, formats |
| `api/src/routers/openai_compatible.py` | layout ref (`AGENTS.md:20-28`) | Main HTTP surface (OpenAI-compatible endpoints) |
| `api/src/services/` | layout ref (`AGENTS.md:20-28`) | TTS orchestration, audio encoding/streaming, `text_processing/` |
| `api/src/inference/` | layout ref (`AGENTS.md:20-28`) | Model backends, model and voice managers |
| `api/src/core/` | layout ref (`AGENTS.md:20-28`) | `config.py`, `paths.py`, `openai_mappings.json` (voice mapping) |
| `web/` | layout ref (`AGENTS.md:20-28`) | Vanilla JS player and WebUI, no framework/build step |
| `docker-bake.hcl` | `:37-66`, `:73-95`, `:97-129`, `:425-577` | cpu/gpu/rocm target matrix, CUDA versions, platforms, cache refs, OCI labels |
| `start-cpu.sh` / `start-cpu.ps1` | `:5-24` / `:9-12` | CPU launch: `USE_GPU=false`, env exports, model fetch, uvicorn on 8880 |
| `start-gpu.sh` / `start-gpu.ps1` / `start-gpu_mac.sh` | `:14-18` / `:10-12` / `:9-20` | GPU launch; Mac variant adds `DEVICE_TYPE=mps`, `PYTORCH_ENABLE_MPS_FALLBACK=1` |
| `AGENTS.md` | `:1-52` | Layout map, commands, commit/CHANGELOG conventions, opt-in flags, gotchas |
| `pytest.ini` | `:1-9` | `api/tests` path, coverage flags, `not integration` default marker |
| `playwright.config.mjs` | `:1-18` | E2E dir, 30s timeout, fixture static server on port 4173 |
| `.coveragerc` | `:1-20` | `source = api`, omits, excluded report lines |
| `.ruff.toml` | `:1-13` | Line length 88, `F`+`I` rules, isort settings, `examples` exclusion |
| `VERSION` | `:1` | Current version `0.9.1-rc1` |
| `debug.http` | `:1-23` | Probes for `/debug/*`, `/v1/models` on localhost:8880 |
| `docker/scripts/download_model.py` | invoked (`README.md:62-66`) | Model download into `api/src/models/v1_0` |

## 7. Dependencies

Exact version-constraint strings from a manifest are not present in the available component pages (they cover badges, launch scripts, and configs, not `pyproject`/lock contents). Evidenced dependencies:

| Package | Version constraint | Purpose |
|---|---|---|
| kokoro | `0.9.4` (badge, `README.md:15-17`) | TTS model package |
| misaki | `0.9.4` (badge, `README.md:15-17`) | G2P/phonemization |
| Kokoro-82M weights | model `1.0::41e5892` (badge, `README.md:15-17`) | Synthesis weights |
| Python | `3.12` (`.python-version:1`) | Runtime pin |
| uv extras `.[cpu]` / `.[gpu]` / plain `.` (Mac) | no constraint string evidenced (`start-cpu.sh:5-24`, `start-gpu_mac.sh:9-20`) | Accelerator-specific installs |
| espeak-ng | system package, `ESPEAK_DATA_PATH` / `PHONEMIZER_ESPEAK_LIBRARY` (`start-cpu.sh:5-24`, `start-cpu.ps1:9-12`) | Fallback phonemizer for unknown words |
| UniDic | full dictionary ~526MB (`AGENTS.md:45-52`) | Japanese synthesis support |
| openai (client lib) | no constraint evidenced (`README.md:158-171`) | Client-side usage only, not server-required |
| pyaudio | optional, speaker playback (`README.md:241-291`) | Stream-to-speakers example |
| @playwright/test | `^1.57.0`, resolved 1.60.0, node `>=18` (`package-lock.json:1-12`) | Web E2E tests |

## 8. CLI / Usage Surface

Entry points: API at `http://localhost:8880`, docs at `/docs`, WebUI at `/web` (`README.md:173-177`); voices at `GET /v1/audio/voices`, synthesis at `POST /v1/audio/speech`, debug probes at `GET /debug/threads`, `/debug/storage`, `/debug/system`, `GET /v1/models` (`README.md:205-228`, `debug.http:1-23`). No repo CLI binary is evidenced; operation is via Docker/uv scripts plus HTTP.

| Command | Purpose |
|---|---|
| `docker run -p 8880:8880 ghcr.io/remsky/kokoro-fastapi-cpu:latest` | CPU server (`README.md:60-88`) |
| `docker run --gpus all -p 8880:8880 ghcr.io/remsky/kokoro-fastapi-gpu:latest[-cu128]` | NVIDIA server, cu126 default / cu128 Blackwell (`README.md:60-88`) |
| `docker run --device=/dev/kfd --device=/dev/dri -p 8880:8880 ghcr.io/remsky/kokoro-fastapi-rocm:latest` | AMD ROCm experimental (`README.md:60-88`) |
| `./start-gpu_mac.sh` | Apple Silicon native MPS (`README.md:60-88`) |
| `docker compose up --build` (from `docker/gpu`, `docker/cpu`, or `docker/rocm`) | Full compose setup incl. UI (`README.md:94-121`) |
| `./start-cpu.sh` / `./start-gpu.sh` (`.\start-cpu.ps1` / `.\start-gpu.ps1` on Windows) | Direct uv run with hot-reload (`README.md:138-148`) |
| `python docker/scripts/download_model.py --output api/src/models/v1_0` | Manual model fetch (`README.md:62-66`) |
| `python examples/assorted_checks/test_openai/test_openai_tts.py`, `.../test_all_voices.py` | Smoke tests (`README.md:230-234`) |
| `uv run pytest`, `ruff format .` + `ruff check . --fix`, `npm run test:web` / `test:e2e`, `npm run cpu:up` (`gpu:up`, `rocm:up`) | Dev/test/compose shortcuts (`AGENTS.md:30-35`) |

| Env var | Effect |
|---|---|
| `USE_GPU` | `false` (cpu) / `true` (gpu) (`start-cpu.sh:5-24`, `start-gpu.sh:14-18`) |
| `MODEL_DIR=src/models` | Model location (`start-cpu.sh:5-12`) |
| `VOICES_DIR=src/voices/v1_0` | Voice data location (`start-cpu.sh:5-12`) |
| `WEB_PLAYER_PATH=$PROJECT_ROOT/web` | WebUI path (`start-cpu.sh:5-12`) |
| `PYTHONPATH=$PROJECT_ROOT:$PROJECT_ROOT/api` | Import root (`start-cpu.sh:5-12`) |
| `DEVICE_TYPE=mps`, `PYTORCH_ENABLE_MPS_FALLBACK=1` | Apple GPU path (`start-gpu_mac.sh:9-20`) |
| `ESPEAK_DATA_PATH`, `PHONEMIZER_ESPEAK_LIBRARY`, `PYTHONUTF8=1` | Phonemizer/data-path fixes (`start-cpu.sh:5-24`, `start-cpu.ps1:9-12`) |

Config surface: `docs/configuration.md` (image vs build, volume mounts, env vars, `README.md:90`, `README.md:120`); opt-in flags `enable_debug_endpoints`, `allow_dev_unload`, default-on `enable_voice_tags` (`AGENTS.md:37-42`); voice customization via `api/src/core/openai_mappings.json` (`README.md:112`).

## 9. Extensibility Points

- New or remapped voices: edit `api/src/core/openai_mappings.json` (aliasing, weighted combos); generate custom packs externally with Inno Clone-Tuner (`README.md:112`, `README.md:26`).
- New HTTP behavior: add routers under `api/src/routers/` following `openai_compatible.py` as the reference surface (`AGENTS.md:20-28`).
- Synthesis/encoding behavior: extend `api/src/services/` (orchestration, audio encoding/streaming) and `api/src/services/text_processing/` for text normalization or SSML handling (`AGENTS.md:20-28`).
- Model execution: add or swap backends in `api/src/inference/` (model backends, model/voice managers) (`AGENTS.md:20-28`).
- Configuration: extend `api/src/core/config.py` and `paths.py`; expose toggles in the `enable_debug_endpoints` / `allow_dev_unload` / `enable_voice_tags` style (`AGENTS.md:37-42`).
- WebUI: modify `web/` directly (vanilla JS, no build step) (`AGENTS.md:20-28`).
- New accelerator targets: add `docker/{name}/` image plus a `docker-bake.hcl` target following the `cpu` / `gpu-*` / `rocm-amd64` pattern (`docker-bake.hcl:97-129`).
- Samples: add standalone scripts under `examples/` (own uv venv, excluded from lint) (`.ruff.toml:1-13`, `AGENTS.md:20-28`).

## 10. Limitations and Gotchas

- **Chunk-size/latency tradeoff is load-bearing:** smaller chunks cut first-token latency but increase intonation artifacts; quoted figures are hardware-specific (GPU ~300ms@400 vs older-i7 CPU ~3500ms@200) (`README.md:298-305`).
- **Apple Silicon has no container GPU path:** the Docker GPU image is CUDA-only, so Mac users must use `docker/cpu` or run natively via `./start-gpu_mac.sh` for MPS (`README.md:56-61`).
- **Heavyweight phonemizer prerequisites:** `espeak-ng` must be on PATH and full UniDic (~526MB) is required for Japanese (`AGENTS.md:45-52`, `README.md:125-132`).
- **ROCm and multi-arch fragility:** ROCm is experimental and `linux/amd64`-only; Dockerfiles are multi-arch with distinct CUDA versions (12.6.3/12.9.1/12.8.1), and `:latest` floats — pin a release tag for stability (`README.md:31-34`, `README.md:56-58`, `docker-bake.hcl:97-129`).
- **Voice detail gap in available evidence:** the source overview chunk is cut mid-section at `### Voices`, so voice-catalog specifics beyond the mixing/aliasing behavior above are not covered by the component pages (`01-overview.md:225-226`).

## 11. How It Compares to Alternatives

The available component pages name no direct competing TTS servers, so a sourced feature matrix is not possible from wiki evidence alone. Positioning, grounded in what is evidenced: the repo's stated design goal is OpenAI API compatibility (`client.audio.speech.create` against `http://localhost:8880/v1` with `api_key="not-needed"`, `README.md:158-171`), i.e. it competes with hosted TTS APIs on interface while executing fully locally via Dockerized Kokoro-82M weights (`README.md:56-58`). The one related project named is Inno Clone-Tuner (`github.com/remsky/inno-kokoro`), positioned as a complement (custom voicepack generation) rather than an alternative (`README.md:26`). Coverage of third-party alternatives (other local TTS servers, Piper/Coqui-style engines, or hosted providers) would require sources beyond the two available component pages.

## Appendix: Selected Code Snippets

OpenAI-compatible synthesis, exact parameter names `model`, `voice`, `input`, `response_format` (`README.md:106-119`):

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

Streaming to file and to speakers with `response_format="pcm"` (`README.md:151-183`):

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

Launch-contract env exports shared by all start scripts (`start-cpu.sh:5-12`):

```bash
PYTHONPATH=$PROJECT_ROOT:$PROJECT_ROOT/api
MODEL_DIR=src/models
VOICES_DIR=src/voices/v1_0
WEB_PLAYER_PATH=$PROJECT_ROOT/web
# plus USE_GPU=false, ESPEAK_DATA_PATH=..., .[cpu]
# uvicorn api.src.main:app --host 0.0.0.0 --port 8880
```
