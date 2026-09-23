> [[index|Wiki]] | [[summary|Summary]]
# ASLP-lab/FlashTTS — Digest
## 1. [[wiki/01-overview|Overview]]
**In one sentence:** FlashTTS is an open-source low-latency streaming TTS framework that combines a lagged multi-track architecture with parallel MTP and X-pred mean-flow decoding to reach 2-NFE token-to-mel at 325ms first-packet latency.
## Key points
- FlashTTS natively processes streaming text and speech inputs via a lagged multi-track architecture, eliminating sentence-level buffering (README.md:16).
- Acoustic generation integrates parallel Multi-Token Prediction (MTP) with an X-pred mean flow matching decoder for token-to-mel in exactly two function evaluations (README.md:16).
- First-packet latency is 325ms versus robust streaming baselines while preserving zero-shot voice cloning and multi-lingual intelligibility (README.md:16).
- The inference pipeline is `Text/Speech Input → [Text Tokenizer] + [Speaker Extractor] → [LLM Decoder with MTP] → [Mean Flow X-pred Module] (2-NFE) → [HiFi-GAN Vocoder] → 24kHz audio` (README.md:50).
- Streaming uses a first chunk of 24 tokens, then 18-token hop with 6-token lookahead per step (24-token context, 18 tokens output per chunk) (README.md:74).
- Entry points are `examples/inference.py` with `--mode flash_tts` (text + reference wav) or `--mode meanflow_only` (token file + reference wav), plus `--stream` for chunked mode (README.md:86).
- Core layout splits into `cosyvoice/` (LLM, tokenizer, frontend), `jit_meanflow_xpred/` (token2mel + vocoder), `third_party/` (CAMPPlus, Matcha-TTS), and `examples/` (README.md:192).
## 2. [[wiki/02-top-level-files|Top-level-files]]
**In one sentence:** The repo's top-level footprint captured here is its Python/ML hygiene (.gitignore) and its pinned CUDA-12.1 inference-and-training dependency set (requirements.txt).
## Key points
- `.gitignore` excludes Python build and cache artifacts (`__pycache__/`, `*.py[cod]`, `build/`, `dist/`, `*.egg-info/`) so generated packaging output is never committed (`.gitignore:1`, `.gitignore:9`).
- `.gitignore` excludes virtual environments (`.venv/`, `venv/`, `ENV/`, `env/`) and IDE state (`.idea/`, `.vscode/`, `*.swp`, `*.swo`), keeping local dev setup out of version control (`.gitignore:23`, `.gitignore:29`).
- `.gitignore` excludes large binary weights and checkpoint dirs (`*.pt`, `*.pth`, `*.ckpt`, `ckpts/`, `checkpoints/`, `pretrained_models/`), so model files are fetched rather than stored in git (`.gitignore:35`).
- `.gitignore` excludes runtime outputs (`*.log`, `inference_output/`, `outputs/`), OS files (`.DS_Store`, `Thumbs.db`), notebook checkpoints, and local secrets (`.env`, `*.local`) (`.gitignore:43`, `.gitignore:48`, `.gitignore:53`).
- `requirements.txt` pulls PyTorch wheels from the CUDA 12.1 index and pins `torch==2.3.1` with `torchaudio==2.3.1` as the compute base (requirements.txt:1, requirements.txt:35).
- `requirements.txt` splits platform-conditional packages: `deepspeed`, `onnxruntime-gpu`, and `tensorrt-cu12*` install only on Linux, while plain `onnxruntime` installs on macOS/Windows (requirements.txt:4, requirements.txt:22, requirements.txt:32).
- `requirements.txt` pins the serving and training stack together: `fastapi`/`uvicorn`/`gradio`/`grpcio` for APIs and demos, plus `lightning`, `hydra-core`, `omegaconf`, `diffusers`, `transformers`, and `conformer` for model code (requirements.txt:6, requirements.txt:16, requirements.txt:3).
- `requirements.txt` pins the speech/audio toolchain (`librosa`, `soundfile`, `pyworld`, `openai-whisper`, `wetext`, `inflect`, `modelscope`, `gdown`, `wget`) used for audio I/O, vocoding features, text normalization, and weight fetching (requirements.txt:15, requirements.txt:24, requirements.txt:28).
## The system in five moves
1. Text/speech enters a lagged multi-track frontend (tokenizer plus CAMPPlus speaker extractor) with no sentence-level buffering.
2. A decoder-only LLM with parallel Multi-Token Prediction emits speech tokens, streamed in 24-token first chunk then 18-token hops with 6-token lookahead.
3. The X-pred mean-flow module converts tokens to 80-dim mel in exactly 2 function evaluations with classifier-free guidance.
4. A HiFi-GAN vocoder renders 24kHz audio, reaching 325ms first-packet latency (~100ms token-to-mel plus ~50ms mel-to-wave on a 4090).
5. The whole stack ships as `cosyvoice/` plus `jit_meanflow_xpred/` plus `third_party/`, runnable via `examples/inference.py` on a pinned CUDA-12.1 torch 2.3.1 environment whose weights and outputs stay out of git by hygiene.
