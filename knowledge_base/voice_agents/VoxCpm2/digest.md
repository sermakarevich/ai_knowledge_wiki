> [[index|Wiki]] | [[summary|Summary]]
# OpenBMB/VoxCPM — Digest

## 1. [[wiki/01-overview|Overview]]
**In one sentence:** VoxCPM2 is a 2B-parameter tokenizer-free multilingual TTS system that generates continuous speech representations end-to-end for natural synthesis, voice design, controllable/ultimate cloning, and 48kHz output.
- VoxCPM is tokenizer-free, directly generating continuous speech representations via an end-to-end diffusion autoregressive architecture that bypasses discrete tokenization (01-overview.md:47).
- VoxCPM2 is a 2B-parameter model trained on over 2 million hours of multilingual data, supporting 30 languages plus Chinese dialects, built on a MiniCPM-4 backbone (01-overview.md:49).
- Voice Design creates a new voice from a natural-language description alone with no reference audio, while Controllable Cloning clones timbre from a short clip plus optional style guidance (01-overview.md:54-55).
- Ultimate Cloning reproduces full vocal nuance by continuing from reference audio plus its transcript, matching the VoxCPM1.5 behavior (01-overview.md:56).
- The system accepts 16kHz reference audio and outputs 48kHz studio-quality audio via AudioVAE V2 asymmetric encode/decode with built-in super-resolution (01-overview.md:57).
- Real-time streaming reaches RTF ~0.3 on RTX 4090 and ~0.13 via Nano-vLLM / vLLM-Omni with PagedAttention and OpenAI-compatible API (01-overview.md:59).
- Weights and code are released under Apache-2.0, free for commercial use (01-overview.md:60).

## 2. [[wiki/02-top-level-files|Top-Level Files]]
**In one sentence:** The repo root exposes the user-facing entry points — a VoxCPM2 Gradio demo (`app.py`), a legacy VoxCPM1.5 demo (`app_old.py`), a LoRA fine-tune/inference WebUI (`lora_ft_webui.py`), the Chinese README, and ignore rules that keep weights/data out of Docker and git.
- `.dockerignore` (27 lines) excludes runtime weight/data dirs (`models/`, `data/`, `lora/`, `output/`), `.git/`, Python caches/venvs, Docker compose/nginx docs, and IDE files from the image build context (`.dockerignore:1-35`).
- `.gitignore` (14 lines) ignores `launch.json`, `.venv/`, `voxcpm.egg-info`, `./pretrained_models/`, `app_local.py`, plus the same large user-specific dirs `models/`, `data/`, `lora/`, `output/` (`.gitignore:1-14`).
- `app.py` is the current VoxCPM2 Gradio demo: `VoxCPMDemo(model_id="openbmb/VoxCPM2", device="auto")` resolves the runtime device, lazily loads `voxcpm.VoxCPM` and a `iic/SenseVoiceSmall` ASR model, and synthesizes via `generate_tts_audio` with defaults `cfg_value=2.0`, `inference_timesteps=10`, `normalize=True`, `denoise=True` (`app.py:227-312`).
- `app.py` ships inline bilingual UI strings (`en` + `zh-CN`, with `zh-Hans`/`zh` aliased to `zh-CN`) wired through `gr.I18n`, covering the three modes — Voice Design, Controllable Cloning, Ultimate Cloning — plus CFG/steps/seed/denoise/normalize labels (`app.py:26-160`).
- `app_old.py` is the legacy VoxCPM1.5 demo: it defaults `HF_REPO_ID` to `openbmb/VoxCPM1.5`, eagerly loads SenseVoiceSmall, resolves a local checkpoint dir with HF-download fallback, and returns `(sample_rate, wav)` from `generate_tts_audio` (`app_old.py:11-113`).
- `lora_ft_webui.py` is a bilingual (en/zh) LoRA training + inference WebUI that prefers `models/openbmb__VoxCPM2` (falling back to `models/openbmb__VoxCPM1.5`), reads the resampling rate from `config.json:audio_vae_config.sample_rate`, scans `lora/` for `lora_weights.safetensors`, and supports LoRA hot-swapping with rank-mismatch reload (`lora_ft_webui.py:18-60`).
- `README_zh.md` documents install (`pip install voxcpm`), Python API (`VoxCPM.from_pretrained("openbmb/VoxCPM2", load_denoiser=False)` + `generate(cfg_value=2.0, inference_timesteps=10, seed=42)`), CLI (`voxcpm design/clone/batch`), Web Demo (`python app.py --port 8808 --device auto`), and Nano-vLLM / vLLM-Omni / llama.cpp-omni deployment paths (`README_zh.md:96-260`).
- Truncation notice: the chunk cuts `app.py` just after the `generate_tts_audio` signature (~line 312 of 607), `lora_ft_webui.py` mid-`run_inference` (~line 315 of 1332), and `README_zh.md` mid version/model table — claims above cover only the visible portions.

## The system in five moves
1. VoxCPM2 synthesizes speech tokenizer-free, generating continuous representations end-to-end via a diffusion autoregressive architecture on a 2B MiniCPM-4 backbone trained on 2M+ hours.
2. One model covers 30 languages plus Chinese dialects with direct synthesis, inferring prosody from text and upsampling 16kHz references to 48kHz output via AudioVAE V2.
3. Three creation paths span the use cases: description-only Voice Design, short-clip Controllable Cloning with style guidance, and transcript-anchored Ultimate Cloning for full nuance.
4. Serving is production-ready with streaming (RTF ~0.3 PyTorch, ~0.13 via Nano-vLLM/vLLM-Omni) under Apache-2.0 weights and code.
5. The repo root exposes this through the VoxCPM2 Gradio demo (`app.py`) with lazy model/ASR loading and bilingual UI, alongside the legacy VoxCPM1.5 demo (`app_old.py`).
6. Power users get a bilingual LoRA fine-tune/inference WebUI with checkpoint hot-swapping plus the Chinese README's pip/CLI/demo/deployment paths, while ignore rules keep weights and data out of Docker and git.
