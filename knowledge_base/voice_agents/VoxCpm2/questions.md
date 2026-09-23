---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: OpenBMB/VoxCPM

### Q1. What is VoxCPM2, and what does "tokenizer-free" mean here?

> [!tip]- Answer
> VoxCPM2 is a 2B-parameter multilingual TTS model built on a MiniCPM-4 backbone and trained on over 2 million hours of speech data. Tokenizer-free means it directly generates continuous speech representations via an end-to-end diffusion autoregressive architecture, bypassing discrete tokenization for more natural and expressive synthesis. See [[wiki/01-overview|Overview]].

### Q2. What are the three voice-creation modes, and how is each invoked?

> [!tip]- Answer
> Voice Design creates a new voice from a natural-language description alone, written as a parenthesized prefix such as `(your voice description)The text to synthesize.` Controllable Cloning clones timbre from a short reference clip plus optional style guidance in the text, while Ultimate Cloning takes reference audio plus its transcript (`prompt_wav_path` + `prompt_text`) and continues seamlessly to preserve timbre, rhythm, emotion, and style. See [[wiki/01-overview|Overview]].

### Q3. Which languages, dialects, and audio quality does VoxCPM2 claim?

> [!tip]- Answer
> VoxCPM2 synthesizes directly in 30 languages with no language tag needed, plus 9 Chinese dialects (四川话, 粤语, 吴语, 东北话, 河南话, 陕西话, 山东话, 天津话, 闽南话). It accepts 16kHz reference audio and outputs 48kHz studio-quality audio via AudioVAE V2 asymmetric encode/decode with built-in super-resolution and no external upsampler. See [[wiki/01-overview|Overview]].

### Q4. How do you install VoxCPM2, synthesize via the Python API and CLI, and serve it fast?

> [!tip]- Answer
> Install with `pip install voxcpm` (Python ≥ 3.10 and <3.13, PyTorch ≥ 2.5.0, CUDA ≥ 12.0), then call `VoxCPM.from_pretrained("openbmb/VoxCPM2", load_denoiser=False)` with `generate(cfg_value=2.0, inference_timesteps=10, seed=42)`. The CLI offers `voxcpm design/clone/batch` with word/char timestamps, the web demo runs via `python app.py --port 8808`, and streaming reaches RTF ~0.3 in PyTorch or ~0.13 via Nano-vLLM/vLLM-Omni with PagedAttention. See [[wiki/01-overview|Overview]].

### Q5. How does the current VoxCPM2 demo (app.py) differ from the legacy VoxCPM1.5 demo (app_old.py)?

> [!tip]- Answer
> `app.py` targets `openbmb/VoxCPM2` with lazy loading of `voxcpm.VoxCPM` plus the `iic/SenseVoiceSmall` ASR model, device auto-resolution, and `generate_tts_audio` defaults of `cfg_value=2.0`, `inference_timesteps=10`, `normalize=True`, `denoise=True` behind a bilingual en/zh-CN Gradio UI. `app_old.py` defaults `HF_REPO_ID` to `openbmb/VoxCPM1.5`, loads ASR eagerly in `__init__`, resolves a local checkpoint dir with HF-download fallback, and returns a plain `(sample_rate, wav)` pair with no seed passthrough. See [[wiki/02-top-level-files|Top-Level Files]].

### Q6. What do the LoRA WebUI, the ignore rules, and the Chinese README provide?

> [!tip]- Answer
> `lora_ft_webui.py` is a bilingual LoRA training and inference WebUI that prefers `models/openbmb__VoxCPM2`, reads the resampling rate from `config.json:audio_vae_config.sample_rate`, scans `lora/` for `lora_weights.safetensors`, and supports LoRA hot-swapping with rank-mismatch reload. Both `.dockerignore` and `.gitignore` keep the heavy `models/`, `data/`, `lora/`, and `output/` dirs out of builds and version control, while `README_zh.md` documents the pip install, Python API, `voxcpm design/clone/batch` CLI, web demo device flags, and Nano-vLLM/vLLM-Omni/llama.cpp-omni deployment paths. See [[wiki/02-top-level-files|Top-Level Files]].

### Q7. Should a small team adopt VoxCPM2 for multilingual voice cloning and voice design?

> [!tip]- Answer
> Yes as a guarded pilot: VoxCPM2 offers a strong open package with Apache-2.0 weights and code, 30 languages plus dialects, description-only Voice Design, two cloning modes, 48kHz output, and quantified streaming paths. Before production use, verify cloning similarity and style control on your own voices and hardware, confirm the LoRA fine-tuning WebUI covers your customization needs, and budget for retries since generative voice design varies run to run. See [[wiki/01-overview|Overview]].
