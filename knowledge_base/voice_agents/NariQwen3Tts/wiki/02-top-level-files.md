> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Top-Level Files
**In one sentence:** The top-level files pin the Python version and define the local Docker Compose runtime — build context, port mapping, model/profile defaults, GPU reservation, cache volume, and healthcheck — while excluding build and cache artifacts from git and Docker builds.
## Key points
- The repo pins Python to `3.12.13` via `.python-version:1`, so local and container builds share one interpreter version.
- `.dockerignore:1-10` excludes VCS, virtualenv, test, and build outputs (`.git/`, `.venv/`, `tests/`, `artifacts/`, `build/`, `dist/`, `*.egg-info/`, `__pycache__/`, `.pytest_cache/`, `.ruff_cache/`) from the Docker build context to keep images small.
- `.gitignore:1-7` excludes the same class of generated artifacts (`.venv/`, `build/`, `dist/`, `*.egg-info/`, `__pycache__/`, `.pytest_cache/`, `.ruff_cache/`) from version control.
- `docker-compose.yaml:2-9` defines a single service `nari-qwen3-tts` that builds from `context: .` with build arg `VCS_REF` defaulting to `unknown` and tags the image `nari-qwen3-tts:local`.
- `docker-compose.yaml:10-15` publishes container port `8000` as host port `8000` and sets runtime defaults `QWEN3_TTS_MODEL: Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice`, `QWEN3_TTS_PROFILE: balanced`, and `HF_TOKEN` defaulting to empty.
- `docker-compose.yaml:16-28` mounts the named volume `nari-qwen3-tts-cache` at `/home/nari/.cache`, raises the `nofile` ulimit to `65536/65536`, and reserves one NVIDIA GPU (`driver: nvidia`, `count: 1`, `capabilities: [gpu]`).
- `docker-compose.yaml:29-37` adds a healthcheck polling `http://127.0.0.1:8000/health` by `curl` every `15s` with `3s` timeout, `600s` start period, and `5` retries, and declares the `nari-qwen3-tts-cache` volume.
---
## .dockerignore
Build-context exclusions (` .dockerignore:1-10`):

```
.git/
.venv/
.pytest_cache/
.ruff_cache/
__pycache__/
artifacts/
build/
dist/
*.egg-info/
tests/
```

Notably `artifacts/` and `tests/` are Docker-ignored (` .dockerignore:6,10`) but have no counterpart in `.gitignore:1-7`, so they are version-controlled yet kept out of the image.

## .gitignore
Version-control exclusions (`.gitignore:1-7`):

```
.pytest_cache/
.ruff_cache/
.venv/
build/
dist/
*.egg-info/
__pycache__/
```

Unlike `.dockerignore`, it does not list `.git/`, `artifacts/`, or `tests/`.

## .python-version
Single pinned version (`.python-version:1`):

```
3.12.13
```

## docker-compose.yaml service `nari-qwen3-tts`
Full service definition (`docker-compose.yaml:1-37`):

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

Runtime settings (`docker-compose.yaml:3-4` set `init: true` and `ipc: host`):

| Setting | Value | Location |
|---|---|---|
| Build context | `.` | `docker-compose.yaml:6` |
| Build arg `VCS_REF` | `${VCS_REF:-unknown}` | `docker-compose.yaml:8` |
| Image | `nari-qwen3-tts:local` | `docker-compose.yaml:9` |
| Port mapping | `"8000:8000"` | `docker-compose.yaml:11` |
| `QWEN3_TTS_MODEL` | `Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice` | `docker-compose.yaml:13` |
| `QWEN3_TTS_PROFILE` | `balanced` | `docker-compose.yaml:14` |
| `HF_TOKEN` | `${HF_TOKEN:-}` (empty default) | `docker-compose.yaml:15` |
| Cache mount | `nari-qwen3-tts-cache:/home/nari/.cache` | `docker-compose.yaml:17` |
| `nofile` soft/hard | `65536` / `65536` | `docker-compose.yaml:20-21` |
| GPU | `driver: nvidia`, `count: 1`, `capabilities: [gpu]` | `docker-compose.yaml:26-28` |
| Healthcheck target | `http://127.0.0.1:8000/health` | `docker-compose.yaml:30` |
| Healthcheck timing | `interval: 15s`, `timeout: 3s`, `start_period: 600s`, `retries: 5` | `docker-compose.yaml:31-34` |

No truncated files were noted in the chunk; all four files above are fully covered.

**Covers:** `.dockerignore`, `.gitignore`, `.python-version`, `docker-compose.yaml`
