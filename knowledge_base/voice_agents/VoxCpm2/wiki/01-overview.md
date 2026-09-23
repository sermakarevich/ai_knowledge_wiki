[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Overview
**In one sentence:** VoxCPM2 is a 2B-parameter tokenizer-free multilingual TTS system that generates continuous speech representations end-to-end for natural synthesis, voice design, controllable/ultimate cloning, and 48kHz output.
## Key points
- VoxCPM is tokenizer-free, directly generating continuous speech representations via an end-to-end diffusion autoregressive architecture that bypasses discrete tokenization (01-overview.md:47).
- VoxCPM2 is a 2B-parameter model trained on over 2 million hours of multilingual data, supporting 30 languages plus Chinese dialects, built on a MiniCPM-4 backbone (01-overview.md:49).
- Voice Design creates a new voice from a natural-language description alone with no reference audio, while Controllable Cloning clones timbre from a short clip plus optional style guidance (01-overview.md:54-55).
- Ultimate Cloning reproduces full vocal nuance by continuing from reference audio plus its transcript, matching the VoxCPM1.5 behavior (01-overview.md:56).
- The system accepts 16kHz reference audio and outputs 48kHz studio-quality audio via AudioVAE V2 asymmetric encode/decode with built-in super-resolution (01-overview.md:57).
- Real-time streaming reaches RTF ~0.3 on RTX 4090 and ~0.13 via Nano-vLLM / vLLM-Omni with PagedAttention and OpenAI-compatible API (01-overview.md:59).
- Weights and code are released under Apache-2.0, free for commercial use (01-overview.md:60).
---
## Identity and architecture
Tokenizer-free end-to-end synthesis (01-overview.md:47):
> `VoxCPM is a **tokenizer-free** Text-to-Speech system that directly generates continuous speech representations via an end-to-end **diffusion autoregressive architecture**, bypassing discrete tokenization to achieve highly natural and expressive synthesis.`

VoxCPM2 scale and base (01-overview.md:49):
> `**VoxCPM2** is the latest major release — a **2B** parameter model trained on **over 2 million hours** of multilingual speech data ... Built on a [MiniCPM-4](https://github.com/OpenBMB/MiniCPM) backbone.`

## Highlights
Capability matrix from (01-overview.md:53-60):

| Feature | Claim |
|---|---|
| Multilingual | 30 languages, direct synthesis, no language tag needed |
| Voice Design | New voice from description alone (gender, age, tone, emotion, pace) |
| Controllable Cloning | Short reference clip + optional style guidance, timbre preserved |
| Ultimate Cloning | Reference audio + transcript continuation; timbre, rhythm, emotion, style |
| Audio quality | 48kHz output from 16kHz reference via AudioVAE V2, no external upsampler |
| Context-aware | Prosody/expressiveness inferred from text content |
| Streaming | RTF ~0.3 (PyTorch) / ~0.13 (Nano-vLLM, vLLM-Omni) on RTX 4090 |
| License | Apache-2.0 weights + code, commercial-ready |

## Languages
Supported list (01-overview.md:63): Arabic, Burmese, Chinese, Danish, Dutch, English, Finnish, French, German, Greek, Hebrew, Hindi, Indonesian, Italian, Japanese, Khmer, Korean, Lao, Malay, Norwegian, Polish, Portuguese, Russian, Spanish, Swahili, Swedish, Tagalog, Thai, Turkish, Vietnamese.

Chinese dialects (01-overview.md:65): 四川话, 粤语, 吴语, 东北话, 河南话, 陕西话, 山东话, 天津话, 闽南话.

## Releases
News timeline (01-overview.md:69-72):
- `[2026.04]` VoxCPM2 release: 2B, 30 languages, Voice Design & Controllable Cloning, 48kHz output.
- `[2025.12]` VoxCPM1.5 weights with SFT & LoRA fine-tuning (#1 GitHub Trending).
- `[2025.09]` VoxCPM Technical Report.
- `[2025.09]` VoxCPM-0.5B weights (#1 HuggingFace Trending).

## Quick Start
Install and requirements (01-overview.md:99-103):
```sh
pip install voxcpm
```
> `Requirements: Python ≥ 3.10 (<3.13), PyTorch ≥ 2.5.0, CUDA ≥ 12.0.`

### Python API
Text-to-speech defaults (01-overview.md:113-126): `VoxCPM.from_pretrained("openbmb/VoxCPM2", load_denoiser=False)` then `model.generate(text=..., cfg_value=2.0, inference_timesteps=10, seed=42)`, saved with `model.tts_model.sample_rate`. ModelScope path (01-overview.md:136-140) uses `snapshot_download("OpenBMB/VoxCPM2", local_dir='./pretrained_models/VoxCPM2')`.

Voice Design format (01-overview.md:153): description in parentheses at start of `text`, e.g. `"(your voice description)The text to synthesize."` (01-overview.md:157).

Controllable cloning args (01-overview.md:170-183): `text`, `reference_wav_path`, plus optional style prefix in `text` with `cfg_value`, `inference_timesteps`, `seed`.

Ultimate cloning args (01-overview.md:191-197): `text`, `prompt_wav_path`, `prompt_text`, optional `reference_wav_path` (same clip in both paths for maximum similarity).

Streaming API (01-overview.md:206-211): `model.generate_streaming(text=...)` yields chunks concatenated via `np.concatenate`.

### CLI
Subcommands and flags (01-overview.md:219-266):

| Command | Key flags |
|---|---|
| `voxcpm design` | `--text`, `--output`, `--control`, `--seed` |
| `voxcpm clone` | `--text`, `--reference-audio`, `--prompt-audio`, `--prompt-text`, `--output` |
| `voxcpm batch` | `--input`, `--output-dir` |
| timestamps | `--timestamps`, `--timestamp-level word\|char`, `--timestamp-language en\|zh` (needs `pip install "voxcpm[timestamps]"`) |

Character timestamps are best-effort, derived from word alignment (01-overview.md:257).

### Web Demo and deployment
Web demo (01-overview.md:272-281): `python app.py --port 8808`, `--device auto|cpu|mps|cuda|cuda:N` (`auto` uses MPS on Apple Silicon).

Production serving (01-overview.md:285-299): `pip install nano-vllm-voxcpm`, `VoxCPM.from_pretrained(model="/path/to/VoxCPM", devices=[0])`, `generate(target_text=...)`, output at 48000 Hz. Chunk notes this section is truncated at (01-overview.md:301): the RTF/batching sentence cuts off at `See the [N`.

**Covers:** 01-overview.md (repo README excerpt, lines 1-301; truncated at line 301 mid-sentence, plus a `Macro components` stub pointing at `top-level-files/`)
