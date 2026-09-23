> [[index|Wiki]] | [[summary|Summary]]
# OpenMOSS/MOSS-TTS — Digest

## 1. [[wiki/01-overview|Overview]]
**In one sentence:** MOSS-TTS Family is an open-source speech and sound generation model family for high-fidelity, high-expressiveness, complex real-world scenarios including long-form speech, multi-speaker dialogue, voice design, sound effects, and real-time streaming TTS.
## Key points
- MOSS-TTS Family is an open-source **speech and sound generation model family** from MOSI.AI and the OpenMOSS team, designed for **high-fidelity**, **high-expressiveness**, and **complex real-world scenarios** (README.md:47).
- The family covers stable long-form speech, multi-speaker dialogue, voice/character design, environmental sound effects, and real-time streaming TTS (README.md:47).
- Entry points are Quickstart, model weights on Hugging Face, samples demo, fine-tuning, and serving backends (README.md:50).
- The model chooser routes tasks to Nano (CPU/browser cloning), v1.5 / Local Transformer v1.5 (multilingual long-form), TTSD (dialogue/podcasts/dubbing), Realtime (streaming), and SoundEffect v2 / released models (voice design/SFX) (README.md:54-60).
- The repo tracks dated releases and backend support (e.g., 2026.6.18 Local-Transformer-v1.5 Day-0 SGLang-Omni support; 2026.6.2 vLLM-Omni full-series support; 2026.5.26 SoundEffect-v2.0 and TTS-v1.5 releases) (README.md:63-72).
- A demo video and a full Contents index (Introduction, Model Architecture, Released Models, Supported Languages, Quickstart, Fine-Tuning, llama.cpp backend, Accelerated Inference Backends, Evaluation, Nano, Audio-Tokenizer, License, Citation) structure the README (README.md:92-142).
- The Introduction frames the family as five production-ready models for audio that must sound like a real person, pronounce accurately, switch styles, stay stable over tens of minutes, and support dialogue/role-play/real-time use (README.md:151).

## 2. [[wiki/02-top-level-files|top-level-files]]
**In one sentence:** The repo root combines a standard Python `.gitignore` plus `weights`/`outputs/*` excludes, a single `moss_audio_tokenizer` git submodule, a `MANIFEST.in` sdist allowlist, and the Chinese landing README (`README_zh.md`) that routes users to models, news, and quickstart.
## Key points
- `.gitignore` is a standard Python template (bytecode, packaging, test/coverage, envs, IDEs) with project-specific ignores for `weights` and `outputs/*` (.gitignore:1-216; project entries at .gitignore:213-216).
- `.gitmodules` declares exactly one submodule: path `moss_audio_tokenizer` pointing at `https://github.com/OpenMOSS/MOSS-Audio-Tokenizer` (.gitmodules:1-3).
- `MANIFEST.in` ships `README.md`, `README_zh.md`, `LICENSE`, `pyproject.toml` and grafts `assets`, `docs`, `moss_tts_delay`, `moss_tts_local`, `moss_tts_realtime`, `moss_audio_tokenizer`, while pruning `.git`/`.github`/`.vscode`/`moss_tts.egg-info` and globally excluding `__pycache__`, `*.py[cod]`, `.DS_Store`, `*.so` (MANIFEST.in:1-22).
- `README_zh.md` is the Chinese mirror of the landing page: it defines the MOSS-TTS family as an open-source speech/sound generation family from MOSI.AI and OpenMOSS for high-fidelity, high-expressiveness, complex real-world scenarios (README_zh.md:43).
- Its task-chooser table routes Nano → CPU/browser cloning, v1.5 / Local Transformer v1.5 → multilingual long-form, TTSD → dialogue/podcasts, Realtime → streaming, and model-overview / SoundEffect v2 → voice design and SFX (README_zh.md:50-56).
- Its News section records dated releases (2026.6.18 Local-Transformer-v1.5 Day-0 SGLang-Omni support and 4B release; 2026.6.7 Audio-Tokenizer-v2; earlier vLLM-Omni, SoundEffect-v2.0, TTS-v1.5, Nano, GGUF/ONNX entries in a collapsed block) plus a demo video and a full Contents index (README_zh.md:58-93).
- Its Introduction frames five production models (TTS flagship zero-shot cloning, TTSD v1.0 dialogue, VoiceGenerator reference-free voice design, Realtime 180 ms-TTFB agent TTS, SoundEffect content SFX) and an architecture table contrasting `MossTTSDelay` / `MossTTSLocal` baselines with the capability-type `MossTTSRealtime` design (README_zh.md:149-169).

## The system in five moves
1. Start from one demand — real-person, accurate, style-switching, long-stable, interactive audio — that no single TTS model covers, so the work splits into a family of production-ready models.
2. Route each job to its model: Nano for CPU/browser cloning, v1.5 / Local Transformer v1.5 for multilingual long-form, TTSD for multi-speaker dialogue, Realtime for streaming, SoundEffect v2 for voice design and SFX.
3. Land users through mirrored English/Chinese entry pages with Quickstart, Hugging Face weights, samples demo, fine-tuning, and serving backends plus a dated News stream of releases and backend support.
4. Ship the code as a lean root — standard Python ignores plus weights/outputs excludes, one audio-tokenizer submodule, and a MANIFEST allowlist over the model packages — with the codec (Audio-Tokenizer-v2, 48 kHz stereo) underpinning the newest checkpoints.
5. Serve it everywhere: local Conda/uv and torch-free GGUF/ONNX paths on one end, accelerated SGLang-Omni and vLLM-Omni streaming endpoints on the other, with evaluation, Nano, and community projects closing the loop.
