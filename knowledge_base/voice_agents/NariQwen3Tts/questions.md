---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: nari-labs/nari-qwen3-tts

### Q1. What does Nari Qwen3-TTS serve, and what is its headline performance claim?

> [!tip]- Answer
> It serves `Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice` as streaming and non-streaming speech generation over HTTP plus WebSocket incremental text input. The headline claim is 10 RPS with sub-50 ms p95 time-to-first-audio on a single NVIDIA H100 SXM while maintaining real-time playback. Even at 20 RPS it sustains sub-80 ms p95 TTFA on the same GPU. See [[wiki/01-overview|Overview]].

### Q2. What are the three serving profiles, and how do they trade latency against throughput?

> [!tip]- Answer
> The `ttfa` profile prioritizes time-to-first-audio with latency-oriented scheduling and smaller initial Codec chunks. The `balanced` profile is the default container profile, balancing first-audio latency against sustained throughput. The `throughput` profile uses larger Codec chunks and batches to prioritize aggregate throughput under load. See [[wiki/01-overview|Overview]].

### Q3. How is a serving profile selected and fine-tuned, and what happens on invalid configuration?

> [!tip]- Answer
> In Docker the profile is selected via `QWEN3_TTS_PROFILE`, while the `nari-qwen3-tts-server` binary takes `--profile`. Advanced tuning uses a strict partial YAML overlay via `--engine-config` whose `extends` names the packaged base (`ttfa`/`balanced`/`throughput`). Unknown keys, invalid capture lists, and profile/base mismatches fail before model loading, and the resolved config plus SHA-256 print at startup. See [[wiki/01-overview|Overview]].

### Q4. Which endpoints does the server expose, and what gates readiness?

> [!tip]- Answer
> It exposes `GET /health`, `GET /ready`, `GET /v1/models`, `POST /v1/audio/speech`, and `WS /v1/audio/speech/ws`, with the POST body following the OpenAI Audio Speech shape plus Nari controls such as `language`. The service stays unready until CUDA Graph capture and a warm-up TTS request have both completed. The container therefore requires Linux x86_64 with an H100, the NVIDIA Container Toolkit, and a CUDA 13.0-compatible driver, with English as the only tested primary language. See [[wiki/01-overview|Overview]].

### Q5. What do the top-level ignore files exclude, and how do they differ?

> [!tip]- Answer
> Both `.dockerignore` and `.gitignore` exclude virtualenv, test-cache, and build outputs such as `.venv/`, `build/`, `dist/`, `*.egg-info/`, `__pycache__/`, `.pytest_cache/`, and `.ruff_cache/`. The `.dockerignore` additionally excludes `.git/`, `artifacts/`, and `tests/`, so those stay version-controlled but out of the image. The repo also pins Python to `3.12.13` via `.python-version` so local and container builds share one interpreter. See [[wiki/02-top-level-files|Top-Level Files]].

### Q6. What runtime does docker-compose.yaml define for local serving?

> [!tip]- Answer
> It defines a single `nari-qwen3-tts` service built from `context: .` (build arg `VCS_REF`, default `unknown`) and tagged `nari-qwen3-tts:local`. It publishes port `8000`, defaults to model `Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice` with profile `balanced` and empty `HF_TOKEN`, and mounts `nari-qwen3-tts-cache` at `/home/nari/.cache`. It raises the `nofile` ulimit to 65536, reserves one NVIDIA GPU, and healthchecks `http://127.0.0.1:8000/health` every 15 s with a 600 s start period. See [[wiki/02-top-level-files|Top-Level Files]].

### Q7. For an interactive voice agent needing the fastest first audio versus an offline batch job needing maximum completions per hour on one H100, which profile and deployment default would you recommend for each and why?

> [!tip]- Answer
> Recommend the `ttfa` profile for the interactive agent because its latency-oriented scheduling and smaller initial Codec chunks minimize time-to-first-audio, which dominates perceived responsiveness. Recommend the `throughput` profile for the batch job because its larger Codec chunks and batches maximize aggregate completions, where per-request first-byte latency matters less than total output. Keep the compose default of `balanced` only when neither objective clearly dominates. See [[wiki/01-overview|Overview]].
