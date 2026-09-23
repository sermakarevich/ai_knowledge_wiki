> [[index|Wiki]] | [[summary|Summary]]
# remsky/Kokoro-FastAPI — Digest

## 1. [[wiki/01-overview|Overview]]
**In one sentence:** Kokoro-FastAPI is a Dockerized FastAPI wrapper for the Kokoro-82M text-to-speech model that exposes an OpenAI-compatible speech endpoint for fast multi-language speech generation (README.md:22).
## Key points
- The project is a Dockerized FastAPI wrapper for [Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M) that generates "hours of high quality speech in minutes" (README.md:22).
- It exposes an OpenAI-compatible Speech endpoint with English (US/GB), Spanish, French, Hindi, Italian, Japanese, Brazilian Portuguese, and Mandarin Chinese support (README.md:24-25).
- Voice features include custom voicepack generation via Inno Clone-Tuner, inline multi-speaker generation with voice mixing plus aliasing weighted combinations, and SSML support (README.md:26, README.md:28).
- It provides an optional integrated WebUI with read-along long-generation, per-word or per-chunk timestamped captions, and phoneme endpoints for text-to-phonemes and phonemes-to-audio (README.md:27, README.md:29-30).
- Prebuilt multiplatform images cover CPU and NVIDIA GPU CUDA on linux/amd64 plus linux/arm64, AMD GPU ROCm experimental on linux/amd64 only, with Apple Silicon MPS supported when running directly via UV with no image (README.md:31-34).
- Three run paths are documented — `docker run`, `docker compose`, and direct run via `uv` — all serving the API at `http://localhost:8880` with docs at `/docs` and the Web Interface at `/web` (README.md:56-88, README.md:99-118, README.md:136-149, README.md:173-177).
- Streaming is OpenAI-compatible with first-token latency of ~300ms on GPU at chunksize 400, ~3500ms on older-i7 CPU at 200, and ~<1s on M3 Pro CPU at 200, and output formats are `mp3`, `wav`, `opus`, `flac`, `aac`, `pcm` (README.md:298-305, README.md:309-316).

## 2. [[wiki/02-top-level-files|top-level-files]]
**In one sentence:** Top-level files define the repo's build, test, lint, container-matrix, and launch scaffolding around the `api/`, `ui`/`web/`, and `docker/` components.
## Key points
- CodeQL scans only `api` and `ui` and ignores `.venv`, `node_modules`, `__pycache__`, `examples`, `docs`, and `tests` (`.codeql-config.yml:1-10`).
- Coverage measures the `api` package, omits tests/examples/builds, and excludes `__repr__`, `NotImplementedError`, `__main__`, `pass`, and `ImportError` lines (`.coveragerc:1-20`).
- Python pins to `3.12` (`.python-version:1`) and Ruff enforces line length 88 with `F` and `I` rules, isort combine/wrap settings, and an `examples` exclusion (`.ruff.toml:1-13`).
- `AGENTS.md` maps the macro layout (`api/src/routers/`, `services/`, `inference/`, `core/`, `web/`, `docker/`, `examples/`) and mandates conventional-commit scopes, tests per change, `CHANGELOG.md` entries without `VERSION` bumps, and opt-in flags for debug/voice-tag endpoints (`AGENTS.md:20-32`).
- `docker-bake.hcl` declares `cpu`, per-arch `gpu-amd64`/`gpu-arm64`/`gpu-cu128-amd64`, and `rocm-amd64` targets with distinct Dockerfiles, CUDA versions (12.6.3/12.9.1/12.8.1), platforms, registry cache refs, and OCI labels/annotations (`docker-bake.hcl:37-66`, `docker-bake.hcl:425-529`).
- Pytest runs `api/tests` with verbose, short-traceback, coverage, and `-m "not integration"` defaults, while Playwright serves `./web/tests/e2e` from a static fixture server on port 4173 (`pytest.ini:1-9`, `playwright.config.mjs:1-18`).
- `start-cpu.sh/ps1` and `start-gpu.sh/ps1`/`start-gpu_mac.sh` set `USE_GPU`, `PYTHONPATH`, `MODEL_DIR`, `VOICES_DIR`, `WEB_PLAYER_PATH`, install extras, download the model, and launch `uvicorn api.src.main:app` on port 8880; the Mac variant adds `DEVICE_TYPE=mps` and `PYTORCH_ENABLE_MPS_FALLBACK=1` (`start-cpu.sh:5-24`, `start-gpu_mac.sh:9-20`).

## The system in five moves
1. Kokoro-82M is wrapped as a Dockerized FastAPI service exposing an OpenAI-compatible speech endpoint for multi-language synthesis.
2. Requests flow through voice mixing, SSML, phoneme, and caption handling into streaming audio encoded as mp3/wav/opus/flac/aac/pcm.
3. Three launch paths — docker run, docker compose, direct uv run — all converge on port 8880 with API docs and WebUI.
4. A container build matrix (cpu, per-arch gpu, rocm) plus launch scripts pin accelerators, env vars, model/voice dirs, and the uvicorn entrypoint.
5. Repo scaffolding enforces quality around the service: CodeQL/coverage scope, Ruff/Python 3.12, pytest plus Playwright e2e, and AGENTS.md conventions.
