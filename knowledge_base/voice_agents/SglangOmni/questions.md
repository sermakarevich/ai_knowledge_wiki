---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---
> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: sgl-project/sglang-omni

### Q1. What is SGLang-Omni and what does its design target of "multi-stage decoding" mean?
> [!tip]- Answer
> SGLang-Omni is a multi-stage serving runtime for omni, speech, and TTS models whose design target is multi-stage decoding: generation split across heterogeneous stages with different compute patterns, dependency structures, and resource needs. It owns the pipeline topology, stage lifecycle, inter-stage transport, model-family integration layer, and OpenAI-compatible serving surface, while composing with SGLang for high-performance autoregressive scheduling and execution where applicable. See [[wiki/01-overview|Overview]].

### Q2. What are the coordinated stages in the runtime and how does stage-specialized scheduling work?
> [!tip]- Answer
> The modeled stages are preprocessing, encoders, autoregressive engines, talkers, decoders, vocoders, and aggregators. Each stage runs behind a scheduler matched to its workload, ranging from SGLang-backed autoregressive scheduling to lightweight preprocessing and streaming vocoder loops. See [[wiki/01-overview|Overview]].

### Q3. How do the control plane and relay data plane divide responsibilities, and which transport backends move tensor payloads?
> [!tip]- Answer
> A control plane coordinates requests while the relay data plane moves tensor payloads between stages. The supported relay backends are shared-memory, NCCL, NIXL, and Mooncake. See [[wiki/01-overview|Overview]].

### Q4. Which models and OpenAI-compatible endpoints does SGLang-Omni serve across omni chat, speech, music, and transcription?
> [!tip]- Answer
> Omni chat and speech come from Qwen3-Omni and Ming-Omni; speech generation spans Higgs Audio v3, MOSS-TTS, Fish Speech S2-Pro, Qwen3-TTS, and others via `/v1/audio/speech` with batch, streaming, and uploaded voices. Music generation uses MiniMax Music 3 (lyrics plus caption to 32 kHz stereo song), while transcription and diarization use Qwen3-ASR, Fun-ASR, ARK-ASR, and MOSS-Transcribe-Diarize via `/v1/audio/transcriptions`, with a multi-worker Omni router as the front door. See [[wiki/01-overview|Overview]].

### Q5. What is the hardware support matrix, and what is the Apple Silicon and Intel XPU story?
> [!tip]- Answer
> NVIDIA CUDA is the supported default backend with full model coverage, while Apple Silicon (macOS arm64, Qwen3-ASR via native MLX or Torch MPS, installed with `install.sh`) and Intel GPU (XPU, with Qwen3-ASR, Qwen3-TTS, and Qwen3-Omni serving end-to-end and an auto-detected backend) are experimental. Entry points include the one-command macOS `./install.sh` setup plus cookbook guides for Qwen3-ASR, MOSS-Transcribe-Diarize, and the Omni router. See [[wiki/01-overview|Overview]].

### Q6. What do the repository top-level hygiene and gate files enforce, and what do the agent pointer files require?
> [!tip]- Answer
> `.dockerignore` and `.gitignore` keep VCS, virtualenv, bytecode, cache, packaging-output, and result/media artifacts out of builds and version control, while `.editorconfig` enforces UTF-8, LF endings, and space indentation (size 4, size 2 for JSON/YAML/Markdown). `.isort.cfg` pins `profile=black` with `sglang-omni` as first-party, `.pre-commit-config.yaml` wires autoflake, pre-commit-hooks, isort, ruff, black-jupyter, clang-format, nbstripout, and local sort-ci-permissions, rustfmt, and leading-underscore checks, and the identical 5-line `AGENTS.md`/`CLAUDE.md` require following the code-review coding-style skill before writing, modifying, or reviewing code. See [[wiki/02-top-level-files|top-level-files]].

### Q7. What does install.sh do and how does per-accelerator packaging scope the torch stack?
> [!tip]- Answer
> `install.sh` is a macOS arm64-only Apple Silicon installer that requires native `/opt/homebrew` Homebrew with `ffmpeg@7` and `uv`, creates a Python 3.12 venv, pins SGLang to `v0.5.19`, and installs `sglang-omni` plus the `sgl-omni` CLI. The `pyproject_cpu/npu/rocm/xpu.toml` variants share the `sgl-omni` console scripts and the `omni` serving entry point while pinning device-specific torch stacks, such as Intel CPU wheels for CPU, manually installed CANN-scoped packages for NPU, SGLang-base-image inheritance for ROCm, and `+xpu` torch builds for XPU. See [[wiki/02-top-level-files|top-level-files]].

### Q8. Should a team adopt SGLang-Omni as its unified serving layer for TTS, ASR, and omni chat, and what is the key risk to weigh?
> [!tip]- Answer
> Yes, recommend it when the team needs one OpenAI-compatible surface covering speech generation, transcription, and omni multimodal chat with stage-specialized scheduling and multi-backend relay transport. The key risk is hardware maturity: only NVIDIA CUDA carries full model coverage, so Apple Silicon and Intel XPU use should be scoped to the validated models (such as Qwen3-ASR, Qwen3-TTS, and Qwen3-Omni) and proven on the team's own hardware first. See [[wiki/01-overview|Overview]].
