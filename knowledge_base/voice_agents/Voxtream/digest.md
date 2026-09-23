> [[index|Wiki]] | [[summary|Summary]]
# herimor/voxtream — Digest

## 1. [[wiki/01-overview|Overview]]
**In one sentence:** VoXtream2 is a zero-shot full-stream text-to-speech model with dynamic speaking-rate control that can be updated mid-utterance on the fly.
## Key points
- VoXtream2 is a zero-shot full-stream TTS model with dynamic speaking-rate control updatable mid-utterance on the fly (01-overview.md:14).
- Dynamic speed control uses distribution matching and classifier-free guidance for fine-grained speaking-rate adjustment during generation (01-overview.md:24).
- Streaming performance is 4x faster than real-time with 74 ms first-packet latency in full-stream on a consumer GPU (01-overview.md:25).
- Translingual capability is enabled by prompt text masking supporting acoustic prompts in any language (01-overview.md:26).
- Inputs are a 3–10 s prompt-audio file (max 20 s, longer trimmed) plus text (max 1000 chars, longer trimmed) with optional target speaking rate in syllables per second (01-overview.md:70-72).
- The model requires 2.2 Gb VRAM (+2 Gb with speech enhancement), caps generation at 1 minute, and was tested on Ubuntu 22.04 / CUDA 12 / PyTorch 2.4 (01-overview.md:75-77).
- Interfaces cover output-streaming and full-streaming CLI (`voxtream`), Python API (`SpeechGenerator.generate_stream`), Gradio demo (`voxtream-app`), websocket server (`voxtream-server`), and benchmark (`voxtream-benchmark`) (01-overview.md:87-91,01-overview.md:143-158,01-overview.md:170-171,01-overview.md:179-180,01-overview.md:221).

## 2. [[wiki/02-top-level-files|Top-level-files]]
**In one sentence:** The repository root defines licensing, attribution, packaging, dependency, and code-quality configuration for the Voxtream project.
## Key points
- `.gitignore` excludes editor, Python cache, build, audio/benchmark artifacts, and local experiment state from version control (`.gitignore:1-11`).
- `.pre-commit-config.yaml` enforces formatting and linting with black, isort, ruff (`--fix --exit-non-zero-on-fix`), and mypy type checking (`.pre-commit-config.yaml:24-46`).
- `ATTRIBUTION.md` requires CC BY 4.0 attribution to the Emilia and HiFiTTS-2 datasets for released model weights (`ATTRIBUTION.md:51-64`).
- Dual licensing is present: full Apache License 2.0 text in `LICENSE-APACHE` and MIT License copyright 2025 Nikita Torgashov in `LICENSE-MIT` (`LICENSE-APACHE:70-71`, `LICENSE-MIT:276-278`).
- `NOTICE` attributes the Depth Transformer component to SesameAI under Apache 2.0 (`NOTICE:312-316`).
- `MANIFEST.in` packages `README.md`, `voxtream/VERSION`, `requirements.txt`, plus `assets/*.wav|*.csv` and `configs/*.json` (`MANIFEST.in:301-306`).
- `requirements.txt` pins the training/inference/demo stack including torch/torchaudio, torchtune, lightning, moshi, transformers, gradio, hydra-core, and audio/ASR deps (`requirements.txt:331-353`).

## The system in five moves
1. VoXtream2 takes a short voice prompt plus text and streams cloned speech with mid-utterance speaking-rate control.
2. Speed control, 4x real-time streaming at 74 ms first-packet latency, and translingual prompt masking define its headline capabilities.
3. Users reach it through CLI, Python streaming API, Gradio demo, websocket server, and benchmark entry points under tight input/VRAM/generation limits.
4. Training, containerized setup, dataset preparation, and evaluation/benchmark tooling support reproduction and extension.
5. The repo root wraps the system in packaging, pinned dependencies, lint/type hooks, and dual-license plus dataset/component attribution.
