> [[index|Wiki]] | [[summary|Summary]]
# wavekat/wavekat-turn — Digest

## 1. [[wiki/01-overview|Overview]]
**In one sentence:** Unified turn detection for WaveKat voice pipelines, wrapping multiple open-source models behind common Rust traits (README.md:16-18).
## Key points
- Wraps multiple open-source turn-detection models behind common Rust traits, following the same pattern as `wavekat-vad` (README.md:16-18).
- Ships three backends: Pipecat Smart Turn v3 audio (~8 MB int8 ONNX, ~12 ms CPU, BSD 2-Clause), WaveKat Smart Turn fine-tunes (same contract, language-specialized), and LiveKit Turn Detector text backend (~400 MB ONNX, ~25 ms CPU) (README.md:29-31).
- WaveKat fine-tunes share the upstream Pipecat ONNX contract (same input shape, same tensor names) with only Mandarin (`zh`) shipped today, more languages landing in the same HF repo over time (README.md:33-37).
- Exposes two trait families by input modality — `AudioTurnDetector` on raw audio frames and `TextTurnDetector` on ASR transcript text — with `TurnController` adding soft-reset orchestration on top of any audio detector (README.md:95-99).
- Positions itself in the pipeline as answering "are they done speaking?" (vs. VAD's "is someone speaking?"), orchestrated with VAD/ASR/LLM/TTS by `wavekat-voice` (README.md:101-107).
- Requires 16 kHz PCM for audio backends — 8 kHz telephony audio must be upsampled because Smart Turn v3 silently produces incorrect results at 8 kHz — while text backends depend on streaming ASR transcript quality (README.md:153-156).
- Validates accuracy cross-checked against the original Python (Pipecat) pipeline on three fixture clips at ±0.02 probability tolerance, regenerable via `make accuracy` (README.md:163-169).

## 2. [[wiki/02-top-level-files|Top-Level Files]]
**In one sentence:** The repository root pins release automation on and excludes all build outputs, lockfiles, local tooling state, and generated training data from version control.
## Key points
- The root excludes Rust build output via `/target` (`.gitignore:1`), so compiled artifacts are never committed.
- The root ignores `Cargo.lock` (`.gitignore:2`), meaning the workspace does not pin exact dependency versions in version control.
- Editor and OS state is excluded via `*.swp`, `*.swo`, and `.DS_Store` (`.gitignore:3-5`), plus `.cargo/config.toml` (`.gitignore:6`).
- Claude Code runtime state is excluded via `.claude/scheduled_tasks.lock` (`.gitignore:9`).
- Python tooling outputs are excluded via `scripts/.venv/`, `scripts/__pycache__/`, `scripts/*.onnx`, `__pycache__/`, and `*.pyc` (`.gitignore:12-16`).
- Generated mel reference tensors are excluded via `*.mel.npy` (`.gitignore:19`), with the pointer to regenerate using `scripts/gen_reference.py` noted in the ignore comment (`.gitignore:18`).
- Training working state is broadly excluded: venvs (`training/**/.venv/`, `.gitignore:25`), wav/JSONL/VAD/ASR/grouped data (`training/smart-turn-zh/data/...`, `.gitignore:28-34`), PDF refs (`training/smart-turn-zh/refs/*.pdf`, `.gitignore:37`), and viewer build output (`training/smart-turn-zh/viewer/node_modules/`, `dist/`, `.gitignore:40-41`).
- Release automation is configured in `release-plz.toml` under `[workspace]` with `git_tag_enable = true` and `git_release_enable = true` (`release-plz.toml:1-3`), so releases create git tags and GitHub releases.

## The system in five moves
1. The crate owns one pipeline question — "are they done speaking?" — sitting above VAD's "is someone speaking?" and orchestrated with ASR/LLM/TTS by `wavekat-voice`.
2. It unifies the problem behind two trait families by modality, `AudioTurnDetector` on raw frames and `TextTurnDetector` on transcripts, so backends stay swappable.
3. Three backends fill those traits: small fast Pipecat Smart Turn v3 audio, same-contract language-specialized WaveKat fine-tunes (Mandarin first), and large LiveKit text EOU.
4. `TurnController` orchestrates any audio detector with soft reset on VAD speech start and hard reset after the assistant responds, handling pause-vs-finished state.
5. Correctness is enforced by input discipline (16 kHz PCM only, upsample telephony audio) and cross-validation against the Python reference at ±0.02 via `make accuracy`.
6. The repo root keeps all of this releasable by excluding build outputs, lockfiles, tooling state, and training data while enabling tag-plus-release automation in `release-plz.toml`.
