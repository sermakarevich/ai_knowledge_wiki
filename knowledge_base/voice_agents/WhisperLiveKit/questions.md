---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---
> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# Retrieval Practice: QuentinFuxa/WhisperLiveKit

### Q1. What simultaneous-speech research backends does WhisperLiveKit build on, and why not just run Whisper on every audio batch?
> [!tip]- Answer
> WhisperLiveKit combines Simul-Whisper/Streaming with AlignAtt, NLLB-based NLLW translation, WhisperStreaming with LocalAgreement, Streaming Sortformer diarization, Qwen3-ASR-causal, and AlignAtt4LLM for decoder-only LLM translation. Naively running Whisper on every audio batch loses context and cuts words mid-syllable, so these policies enable low-latency incremental transcription and translation instead. See [[wiki/01-overview|Overview]].

### Q2. What does the `wlk` CLI cover for serving, transcribing, models, and benchmarking?
> [!tip]- Answer
> The CLI starts the server with commands like `wlk --model base --language en` or `wlk run whisper:tiny`, transcribes files offline via `wlk transcribe meeting.wav`, and generates subtitles with `wlk transcribe --format srt podcast.mp3 -o podcast.srt`. It also manages models (`wlk models`, `wlk pull large-v3`, `wlk rm large-v3`) and benchmarks speed and accuracy with `wlk bench`. See [[wiki/01-overview|Overview]].

### Q3. How do clients reach the server over REST and WebSocket, and what per-session parameters does the native stream accept?
> [!tip]- Answer
> Clients use an OpenAI-compatible REST endpoint (`POST http://localhost:8000/v1/audio/transcriptions`, usable with the OpenAI Python SDK against `http://localhost:8000/v1`) and a native real-time WebSocket at `ws://localhost:8000/asr`. The WebSocket accepts per-session query parameters `language`, `target_language`, `context`, `mode`, and `token`, with the bundled web UI using `full` state rather than the experimental `diff` protocol. See [[wiki/01-overview|Overview]].

### Q4. How are optional backends installed, what environment conflicts exist, and how are accuracy/speed claims made reproducible?
> [!tip]- Answer
> Optional backends install as extras via `uv sync --extra <name>` or `pip install -e ".[<name>]"`, covering MLX, FunASR, Voxtral, CPU/CUDA stacks, translation, Qwen3 variants, Sortformer/Diart diarization, and Canary. Heavy extras declare conflicts in `[tool.uv].conflicts`, e.g. `qwen3-vllm` needs a separate environment from `cu129` and Canary conflicts with `voxtral-hf` and `qwen3-vllm-metal`. Claims rest on H100 scatter benchmarks over 6 minutes of LibriVox audio per language with Project Gutenberg ground truth, raw results in `benchmarks/h100_scatter/` and reproduction via `python scripts/run_scatter_benchmark.py`. See [[wiki/01-overview|Overview]].

### Q5. What do the ignore files, submodule, and packaging manifest declare?
> [!tip]- Answer
> `.dockerignore` trims the Docker build context (`.git`, `.venv`, caches, `dist`, `build`), while `.gitignore` adds project-specific entries for audio/models (`*.wav`, `*.mp3`, `*.pt`), run scripts, generated chrome-extension bundles, `/benchmarks/runs/`, and test scaffolding with `!tests/` kept. `.gitmodules` registers a single submodule at `third_party/qwen3-asr-causal`, and `MANIFEST.in` includes Sortformer two-speaker fixture files. See [[wiki/02-top-level-files|Top-Level Files]].

### Q6. What deployment profiles and contributor contracts do the top-level files define?
> [!tip]- Answer
> `compose.yml` defines GPU Sortformer, GPU Voxtral, and CPU services sharing an `hf-cache` volume with `HF_TOKEN` passthrough, while `Dockerfile.cpu` is a two-stage bookworm-slim build on Python 3.12 with `ARG EXTRAS=cpu`, runtime `ffmpeg`, port 8000, `ENTRYPOINT ["wlk", "--host", "0.0.0.0"]`, and an HTTP healthcheck. `CLAUDE.md` sets runtime boundaries (shared `TranscriptionEngine` per process vs. per-session `AudioProcessor`, `parse_args()` returning `WhisperLiveKitConfig`, `online_factory()` selection, `FrontData.to_dict()` WebSocket JSON), and `CITATION.cff`/`SECURITY.md`/`CHANGES.md` govern citation, private vulnerability reporting, and release notes. See [[wiki/02-top-level-files|Top-Level Files]].

### Q7. For a small team deploying CPU-only live transcription with occasional GPU experiments, which WhisperLiveKit setup would you recommend and why?
> [!tip]- Answer
> I would recommend starting from the `Dockerfile.cpu` image and `wlk-cpu` compose profile for the default service, keeping the H100 scatter benchmarks as the accuracy/speed reference when choosing models. I would isolate GPU experiments (Sortformer diarization or Voxtral/Qwen3 stacks) in separate environments per the `[tool.uv].conflicts` rules so the CPU baseline stays reproducible. See [[wiki/02-top-level-files|Top-Level Files]].
