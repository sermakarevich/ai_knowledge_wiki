> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# top-level-files
**In one sentence:** Top-level files define the repo's build, test, lint, container-matrix, and launch scaffolding around the `api/`, `ui`/`web/`, and `docker/` components.
## Key points
- CodeQL scans only `api` and `ui` and ignores `.venv`, `node_modules`, `__pycache__`, `examples`, `docs`, and `tests` (`.codeql-config.yml:1-10`).
- Coverage measures the `api` package, omits tests/examples/builds, and excludes `__repr__`, `NotImplementedError`, `__main__`, `pass`, and `ImportError` lines (`.coveragerc:1-20`).
- Python pins to `3.12` (`.python-version:1`) and Ruff enforces line length 88 with `F` and `I` rules, isort combine/wrap settings, and an `examples` exclusion (`.ruff.toml:1-13`).
- `AGENTS.md` maps the macro layout (`api/src/routers/`, `services/`, `inference/`, `core/`, `web/`, `docker/`, `examples/`) and mandates conventional-commit scopes, tests per change, `CHANGELOG.md` entries without `VERSION` bumps, and opt-in flags for debug/voice-tag endpoints (`AGENTS.md:20-32`).
- `docker-bake.hcl` declares `cpu`, per-arch `gpu-amd64`/`gpu-arm64`/`gpu-cu128-amd64`, and `rocm-amd64` targets with distinct Dockerfiles, CUDA versions (12.6.3/12.9.1/12.8.1), platforms, registry cache refs, and OCI labels/annotations (`docker-bake.hcl:37-66`, `docker-bake.hcl:425-529`).
- Pytest runs `api/tests` with verbose, short-traceback, coverage, and `-m "not integration"` defaults, while Playwright serves `./web/tests/e2e` from a static fixture server on port 4173 (`pytest.ini:1-9`, `playwright.config.mjs:1-18`).
- `start-cpu.sh/ps1` and `start-gpu.sh/ps1`/`start-gpu_mac.sh` set `USE_GPU`, `PYTHONPATH`, `MODEL_DIR`, `VOICES_DIR`, `WEB_PLAYER_PATH`, install extras, download the model, and launch `uvicorn api.src.main:app` on port 8880; the Mac variant adds `DEVICE_TYPE=mps` and `PYTORCH_ENABLE_MPS_FALLBACK=1` (`start-cpu.sh:5-24`, `start-gpu_mac.sh:9-20`).
---
## Scan, coverage, and code style
CodeQL scope (`.codeql-config.yml:1-10`):
```
paths:
  - api
  - ui
paths-ignore:
  - .venv
  - "**/node_modules"
  - "**/__pycache__"
  - examples
  - docs
  - "**/tests/**"
```
Coverage (`.coveragerc:1-20`): `source = api`; `omit = api/tests/*, Kokoro-82M/*, MagicMock/*, test_*.py, examples/*, src/builds/*`; excluded report lines are `pragma: no cover`, `def __repr__`, `raise NotImplementedError`, `if __name__ == .__main__.`, `pass`, `raise ImportError`. Codecov disables both comment and project/patch status (`codecov.yml:1-6`).
Lint/format (`.ruff.toml:1-13`):
```
line-length = 88
exclude = ["examples"]
[lint] select = ["F", "I"]
```
with isort `combine-as-imports`, `force-wrap-aliases`, `split-on-trailing-comma`, and section order `future, standard-library, third-party, first-party, local-folder`. Runtime pins Python `3.12` (`.python-version:1-2`).
## VCS, ignore, and line endings
`.gitattributes:1-7` forces `text=auto eol=lf`, `*.py`/`*.sh`/`*.yml` to LF, and marks `uv.lock` as binary linguist-generated. `.gitignore:1-25` drops `.git`, bytecode, packaging artifacts, `.venv/`/`node_modules/`/`env/`, and IDE dirs; `.gitignore:26-73` additionally ignores model blobs (`*.pth`, `*.tar*`, `api/src/models/**/*.download`), `.env`, `.claude/*` and `.agents/*` except listed skills, `Kokoro-82M/`, `api/temp_files/`, audio outputs, and scratch dirs. `.dockerignore:1-40` mirrors this for builds, excluding git metadata, bytecode, venvs, `examples/`, `Kokoro-82M/`, `tests/`, `*.md`/`*.txt` (except `requirements.txt`), and `Dockerfile*`/`docker-compose*`.
## Contributor and agent guide
`AGENTS.md:1-18` assigns accountability to the human reviewer, bans em-dash overuse and expositional commenting, and points to `CONTRIBUTING.md` plus task guides in `.claude/skills/`. Layout map (`AGENTS.md:20-28`):
| Path | Role |
|---|---|
| `api/src/routers/` | HTTP endpoints; `openai_compatible.py` is the main surface |
| `api/src/services/` | TTS orchestration, audio encoding/streaming, `text_processing/` |
| `api/src/inference/` | Model backends, model and voice managers |
| `api/src/core/` | `config.py`, `paths.py`, `openai_mappings.json` |
| `web/` | Vanilla JS player, no framework/build step |
| `docker/{cpu,gpu,rocm}/` | Per-accelerator images; `docker-bake.hcl` CI targets |
| `examples/` | Standalone samples with their own uv venv |
Commands (`AGENTS.md:30-35`): `uv run pytest`, `ruff format .` then `ruff check . --fix`, `npm run test:web` / `test:e2e`, `npm run cpu:up` (`gpu:up`, `rocm:up`). Conventions (`AGENTS.md:37-42`): `fix(audio): ...` style scopes, a test per behavior change, user-notice `CHANGELOG.md` entries, no `VERSION` bumps, and opt-in settings (`enable_debug_endpoints`, `allow_dev_unload`, default-on `enable_voice_tags`). Gotchas (`AGENTS.md:45-52`): multi-arch Dockerfiles, espeak-ng on PATH, full UniDic (~526MB) for Japanese, SHA-pinned actions, never manually triggering the `release`-branch publish workflow. Current version is `0.9.1-rc1` (`VERSION:1`).
## Container build matrix
`docker-bake.hcl:37-66` defines variables `VERSION` (`latest`), `REGISTRY` (`ghcr.io`), `OWNER` (`remsky`), `REPO` (`kokoro-fastapi`), `DOWNLOAD_MODEL` (`true`), plus empty `REVISION`/`CREATED` for local builds. Target `_common` (`docker-bake.hcl:73-95`) sets context `.`, `DEBIAN_FRONTEND=noninteractive`, and shared OCI labels/annotations (source, url, licenses `Apache-2.0`, revision, version, created).
| Target | Base/Dockerfile | Platform / CUDA | Tag pattern |
|---|---|---|---|
| `cpu` | `_cpu_base`, `docker/cpu/Dockerfile.optimized` | `linux/amd64`, `linux/arm64` | `...-cpu:${VERSION}` |
| `gpu-amd64` | `_gpu_base`, `docker/gpu/Dockerfile.optimized` | `linux/amd64`, `CUDA_VERSION=12.6.3` | `...-gpu:${VERSION}-cu126-amd64` |
| `gpu-arm64` | `_gpu_base` | `linux/arm64`, `CUDA_VERSION=12.9.1` | `...-gpu:${VERSION}-cu129-arm64` |
| `gpu-cu128-amd64` | `_gpu_base`, `GPU_EXTRA=gpu-cu128` | `linux/amd64`, `CUDA_VERSION=12.8.1`, Blackwell sm_120 | `...-gpu:${VERSION}-cu128-amd64` |
| `rocm-amd64` | `_rocm_base`, `docker/rocm/Dockerfile` | `linux/amd64` only | `...-rocm:${VERSION}-amd64` |
(`docker-bake.hcl:97-129`, `docker-bake.hcl:425-529`). Groups (`docker-bake.hcl:438-577`): `gpu` → `gpu-amd64, gpu-arm64`; `dev` → `cpu-dev, gpu-dev`; `cpu-all`, `gpu-all`, `rocm-all`, `all`, `individual-platforms`. Dev targets reuse registry cache refs and tag `:dev` variants (`docker-bake.hcl:531-556`).
## Tests and debug probes
`pytest.ini:1-9`:
```
testpaths = api/tests
python_files = test_*.py
addopts = -v --tb=short --cov=api --cov-report=term-missing --cov-config=.coveragerc -m "not integration"
pythonpath = .
asyncio_mode = auto
```
`integration` marker requires a running server plus a Whisper download and is opted in via `pytest -m integration`. `playwright.config.mjs:1-18` sets `testDir: './web/tests/e2e'`, 30s timeout, `baseURL http://127.0.0.1:${port}` (default 4173), and a `webServer` running `node web/tests/e2e/fixtures/static-server.mjs`. `package-lock.json:1-12` records package `Kokoro-FastAPI`, lockfile v3, with `@playwright/test ^1.57.0` resolved to 1.60.0 (node `>=18`). `debug.http:1-23` probes `GET /debug/threads`, `/debug/storage`, `/debug/system`, and `GET /v1/models` plus `/v1/models/tts-1` on `http://localhost:8880`.
## Launch scripts
All five scripts install extras, fetch the model to `api/src/models/v1_0`, and start `uvicorn api.src.main:app --host 0.0.0.0 --port 8880` (`start-cpu.sh:15-24`, `start-cpu.ps1:9-12`, `start-gpu.sh:14-18`, `start-gpu.ps1:10-12`, `start-gpu_mac.sh:17-20`).
| Script | Key env / install |
|---|---|
| `start-cpu.sh` | `USE_GPU=false`, `ESPEAK_DATA_PATH=/usr/lib/x86_64-linux-gnu/espeak-ng-data`, `.[cpu]` |
| `start-cpu.ps1` | `USE_GPU=false`, `PHONEMIZER_ESPEAK_LIBRARY`, `PYTHONUTF8=1`, `.[cpu]` |
| `start-gpu.sh` | `USE_GPU=true`, `.[gpu]` |
| `start-gpu.ps1` | `USE_GPU=true`, `PHONEMIZER_ESPEAK_LIBRARY`, `.[gpu]` |
| `start-gpu_mac.sh` | `USE_GPU=true`, `DEVICE_TYPE=mps`, `PYTORCH_ENABLE_MPS_FALLBACK=1`, plain `.` install |
Common exports: `PYTHONPATH=$PROJECT_ROOT:$PROJECT_ROOT/api`, `MODEL_DIR=src/models`, `VOICES_DIR=src/voices/v1_0`, `WEB_PLAYER_PATH=$PROJECT_ROOT/web` (`start-cpu.sh:5-12`, `start-gpu_mac.sh:9-14`). No chunk-truncated files: all 20 top-level files were fully present in the chunk.
**Covers:** `.codeql-config.yml`, `.coveragerc`, `.dockerignore`, `.gitattributes`, `.gitignore`, `.python-version`, `.ruff.toml`, `AGENTS.md`, `codecov.yml`, `debug.http`, `docker-bake.hcl`, `package-lock.json`, `playwright.config.mjs`, `pytest.ini`, `start-cpu.ps1`, `start-cpu.sh`, `start-gpu.ps1`, `start-gpu.sh`, `start-gpu_mac.sh`, `VERSION`
