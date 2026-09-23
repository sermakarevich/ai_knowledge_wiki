---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---
> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# Retrieval Practice: remsky/Kokoro-FastAPI

### Q1. What is Kokoro-FastAPI in one sentence, and what is its core endpoint?
> [!tip]- Answer
> It is a Dockerized FastAPI wrapper for the Kokoro-82M text-to-speech model that generates hours of high-quality speech in minutes. Its core surface is an OpenAI-compatible speech endpoint consumed with the standard `model`, `voice`, `input`, and `response_format` parameters. See [[wiki/01-overview|Overview]].

### Q2. Which languages does the speech endpoint support, and what voice features does the project offer?
> [!tip]- Answer
> It supports English (US/GB), Spanish, French, Hindi, Italian, Japanese, Brazilian Portuguese, and Mandarin Chinese. Voice features include custom voicepack generation via Inno Clone-Tuner plus inline multi-speaker generation with voice mixing, aliasing weighted combinations, and SSML support. See [[wiki/01-overview|Overview]].

### Q3. What are the three run paths, and where do the API, docs, and WebUI live?
> [!tip]- Answer
> The three documented paths are `docker run` with prebuilt images, `docker compose` from `docker/{cpu,gpu,rocm}`, and direct run via `uv` with the `start-cpu`/`start-gpu` scripts. All three converge on `http://localhost:8880`, with API docs at `/docs` and the Web Interface at `/web`. See [[wiki/01-overview|Overview]].

### Q4. What are the streaming latency figures and the supported output formats?
> [!tip]- Answer
> First-token latency is ~300ms on GPU at chunksize 400, ~3500ms on an older-i7 CPU at 200, and ~<1s on an M3 Pro CPU at 200, with adjustable chunking for real-time playback. Supported output formats are `mp3`, `wav`, `opus`, `flac`, `aac`, and `pcm`. See [[wiki/01-overview|Overview]].

### Q5. What does the `docker-bake.hcl` container build matrix declare?
> [!tip]- Answer
> It declares `cpu`, per-arch `gpu-amd64`/`gpu-arm64`/`gpu-cu128-amd64`, and `rocm-amd64` targets with distinct Dockerfiles, CUDA versions (12.6.3/12.9.1/12.8.1), platforms, and registry cache refs. The `cpu` and GPU targets build for linux/amd64 plus linux/arm64, while `rocm-amd64` is linux/amd64 only, and groups like `gpu`, `dev`, and `all` compose the targets. See [[wiki/02-top-level-files|top-level-files]].

### Q6. What quality scaffolding do the top-level files enforce around tests, lint, and launch?
> [!tip]- Answer
> CodeQL scans only `api` and `ui`, coverage measures the `api` package with `__repr__`/`pass`/`ImportError` exclusions, and Ruff enforces line length 88 with `F` and `I` rules on Python 3.12. Pytest runs `api/tests` excluding `integration` by default while Playwright covers `./web/tests/e2e`, and the `start-cpu`/`start-gpu` scripts pin `USE_GPU`, model/voice dirs, and the `uvicorn api.src.main:app` entrypoint on port 8880. See [[wiki/02-top-level-files|top-level-files]].

### Q7. A teammate with an Apple Silicon MacBook, one with an NVIDIA RTX 50-series desktop, and one with a CPU-only Linux server each want to run Kokoro-FastAPI: which image or run path would you recommend for each, and why?
> [!tip]- Answer
> I would recommend the MacBook user run directly via UV with `./start-gpu_mac.sh` for native MPS acceleration, since no prebuilt image supports Apple Silicon. I would recommend the RTX 50-series user run the `gpu:latest-cu128` image with `--gpus all`, since it ships CUDA 12.8.1 with Blackwell support. I would recommend the CPU-only server use the `cpu` image or `docker/cpu` compose path, accepting ~second-scale first-token latency in exchange for no GPU requirement. See [[wiki/01-overview|Overview]].
