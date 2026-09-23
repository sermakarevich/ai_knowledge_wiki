> [[index|Wiki]] | [[summary|Summary]]
# krafton-ai/Raon-Speech — Digest
## 1. [[wiki/01-overview|Overview]]
**In one sentence:** Raon-Speech is a 9B bilingual (English/Korean) SpeechLM family with an offline track (`TTS`, `STT`, `SpeechChat`, `TextQA`) and a real-time full-duplex track (Raon-SpeechChat) sharing one core model and processor stack under `src/raon/`.
## Key points
- The repo contains two tracks sharing the same core family and processor stack under `src/raon/`: Raon-Speech (Offline SpeechLM: `TTS`, `STT`, `SpeechChat`, `TextQA`) and Raon-SpeechChat (Offline/Realtime Full-Duplex) (README.md:37-43).
- Raon-Speech is a 9B bilingual English/Korean SpeechLM for speech understanding, answering, and generation, trained on 1M+ hours of curated speech-text data and evaluated across 42 speech and text benchmarks; Raon-SpeechChat is continually trained on 116K hours of time-aligned dialogue data (README.md:47-49).
- Raon-SpeechChat extends Raon-Speech to real-time full-duplex conversation via causal streaming, interleaved speech-text modeling, explicit interaction-state modeling, and text lookahead, with strength in turn-taking, backchanneling, and interruption handling (README.md:48-50).
- The system is distributed with Hugging Face Transformers integration via `AutoModel.from_pretrained(..., trust_remote_code=True)` plus an open release of checkpoints, training/inference pipeline, interactive demo, and three Korean benchmarks (KVoiceBench, KOpenAudioBench, KMMAU) (README.md:52-53).
- All model entry points accept either a local checkpoint directory or a Hugging Face `repo_id` (e.g. `KRAFTON/Raon-Speech-9B`, `KRAFTON/Raon-SpeechChat-9B`), loaded via `RaonPipeline(..., device="cuda", dtype="bfloat16")` or `bash scripts/infer.sh` / `bash scripts/duplex_infer.sh` (README.md:83-105).
- Two execution modes exist: with `raon` installed (all entry points: `scripts/*.sh`, demos, `from raon import RaonPipeline`) versus without install (only Hub-remote-code Gradio demo and pure-Transformers flow; `python -m raon.*` and the full-duplex realtime runtime are not supported as-is) (README.md:115-164).
- The package backbone is one shared `RaonModel` (LM backbone + audio encoder + Mimi codec path) with two model types, `raon` (Raon-Speech) and `raon_duplex` (Raon-SpeechChat), and trainable blocks `input_adaptor`, `output_adaptor`, `audio_lm_head`, `proj_code`, `code_predictor` (README.md:225-231).
## 2. [[wiki/02-top-level-files|Top-level-files]]
**In one sentence:** The repository root defines only project hygiene, legal attribution, and the Python runtime — a standard Python `.gitignore`, a `NOTICE` file crediting five third-party projects, and a 14-package `requirements.txt`.
## Key points
- The chunk grounds this page in exactly 3 source files: `.gitignore` (217 lines), `NOTICE` (40 lines), and `requirements.txt` (18 lines) (`02-top-level-files.md:5`).
- `.gitignore` is the stock Python template excluding bytecode (`__pycache__/`, `*.py[codz]`), C extensions (`*.so`), and packaging outputs (`build/`, `dist/`, `*.egg-info/`, `wheels/`) (`.gitignore:1-35`).
- `.gitignore` excludes environments and secrets including `.env`, `.envrc`, `.venv`, `venv/`, plus `.streamlit/secrets.toml` and `.abstra/` credentials (`.gitignore:158-166`, `.gitignore:199-201`, `.gitignore:223-224`).
- `.gitignore` excludes test/coverage, lint/typecheck, and IDE artefacts such as `.coverage`, `htmlcov/`, `.pytest_cache/`, `.ruff_cache/`, `.mypy_cache/`, and `.pytype/` (`.gitignore:47-60`, `.gitignore:178-187`, `.gitignore:212-213`).
- `NOTICE` copyrights the project as "RAON / Copyright 2026 The RAON Authors" and attributes five third-party codebases, all but PyTorch under Apache-2.0 (`NOTICE:1-8`).
- `NOTICE` explicitly names HuggingFace Transformers (2018–), Qwen3/Qwen3OmniMoe (Alibaba Cloud 2026), Mimi Audio Codec (Kyutai 2024), SpeechBrain ECAPA-TDNN speaker encoder (2021), and PyTorch (BSD 3-Clause, Facebook 2016–) (`NOTICE:9-40`).
- `requirements.txt` installs with `pip install -r requirements.txt` and pins only five packages (`accelerate>=1.10.1`, `pydantic>=2.11.10`, `soundfile>=0.13.1`, `transformers>=4.57.1,<5.0`, `datasets>=3.0.0`), leaving `torch`, `torchaudio`, `speechbrain`, and six others unpinned (`requirements.txt:1-17`).
## The system in five moves
1. One 9B bilingual SpeechLM family splits into an offline track (TTS, STT, SpeechChat, TextQA) and a real-time full-duplex track sharing the same core and processor stack under `src/raon/`.
2. The full-duplex extension adds causal streaming, interleaved speech-text modeling, interaction-state modeling, and text lookahead for turn-taking, backchanneling, and interruption handling.
3. A single shared `RaonModel` backbone (LM + audio encoder + Mimi codec path, types `raon` / `raon_duplex`) exposes both tracks through `RaonPipeline` via local checkpoint or Hub `repo_id`.
4. Distribution is Hub-native with Transformers remote-code loading, open checkpoints, training/inference scripts, demos, and Korean benchmarks, in installed versus no-install execution modes.
5. The repository root itself carries no model logic — only Python hygiene (`.gitignore`), third-party attribution (`NOTICE`), and the 14-package runtime (`requirements.txt`).
