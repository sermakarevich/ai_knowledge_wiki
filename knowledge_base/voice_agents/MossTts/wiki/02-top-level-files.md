[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# top-level-files
**In one sentence:** The repo root combines a standard Python `.gitignore` plus `weights`/`outputs/*` excludes, a single `moss_audio_tokenizer` git submodule, a `MANIFEST.in` sdist allowlist, and the Chinese landing README (`README_zh.md`) that routes users to models, news, and quickstart.
## Key points
- `.gitignore` is a standard Python template (bytecode, packaging, test/coverage, envs, IDEs) with project-specific ignores for `weights` and `outputs/*` (.gitignore:1-216; project entries at .gitignore:213-216).
- `.gitmodules` declares exactly one submodule: path `moss_audio_tokenizer` pointing at `https://github.com/OpenMOSS/MOSS-Audio-Tokenizer` (.gitmodules:1-3).
- `MANIFEST.in` ships `README.md`, `README_zh.md`, `LICENSE`, `pyproject.toml` and grafts `assets`, `docs`, `moss_tts_delay`, `moss_tts_local`, `moss_tts_realtime`, `moss_audio_tokenizer`, while pruning `.git`/`.github`/`.vscode`/`moss_tts.egg-info` and globally excluding `__pycache__`, `*.py[cod]`, `.DS_Store`, `*.so` (MANIFEST.in:1-22).
- `README_zh.md` is the Chinese mirror of the landing page: it defines the MOSS-TTS family as an open-source speech/sound generation family from MOSI.AI and OpenMOSS for high-fidelity, high-expressiveness, complex real-world scenarios (README_zh.md:43).
- Its task-chooser table routes Nano → CPU/browser cloning, v1.5 / Local Transformer v1.5 → multilingual long-form, TTSD → dialogue/podcasts, Realtime → streaming, and model-overview / SoundEffect v2 → voice design and SFX (README_zh.md:50-56).
- Its News section records dated releases (2026.6.18 Local-Transformer-v1.5 Day-0 SGLang-Omni support and 4B release; 2026.6.7 Audio-Tokenizer-v2; earlier vLLM-Omni, SoundEffect-v2.0, TTS-v1.5, Nano, GGUF/ONNX entries in a collapsed block) plus a demo video and a full Contents index (README_zh.md:58-93).
- Its Introduction frames five production models (TTS flagship zero-shot cloning, TTSD v1.0 dialogue, VoiceGenerator reference-free voice design, Realtime 180 ms-TTFB agent TTS, SoundEffect content SFX) and an architecture table contrasting `MossTTSDelay` / `MossTTSLocal` baselines with the capability-type `MossTTSRealtime` design (README_zh.md:149-169).
---
## .gitignore
Standard Python ignore template plus two project-specific entries at the tail (`.gitignore:213-216`):
```
# Weights
weights

outputs/*
```
Broader coverage includes `__pycache__/`, `*.py[codz]` (`.gitignore:1-3`), packaging dirs (`build/`, `dist/`, `*.egg-info/`, `.gitignore:9-28`), test/coverage (`.gitignore:39-52`), envs (`.env`, `.venv`, `env/`, `venv/`, `.gitignore:137-148`), and tool caches (`.mypy_cache/`, `.ruff_cache/`, `.cursorignore`, `marimo/_static/`, `.gitignore:160-210`).

## .gitmodules
Verbatim whole file (`.gitmodules:1-3`):
```
[submodule "moss_audio_tokenizer"]
	path = moss_audio_tokenizer
	url = https://github.com/OpenMOSS/MOSS-Audio-Tokenizer
```

## MANIFEST.in
Verbatim include/graft/prune/exclude rules (`MANIFEST.in:1-22`):
```
include README.md
include README_zh.md
include LICENSE
include pyproject.toml

graft assets
graft docs
graft moss_tts_delay
graft moss_tts_local
graft moss_tts_realtime
graft moss_audio_tokenizer

prune .git
prune .github
prune .vscode
prune moss_tts.egg-info

global-exclude __pycache__
global-exclude __pycache__/*
global-exclude *.py[cod]
global-exclude .DS_Store
global-exclude *.so
```

## README_zh.md
Chinese landing page; language toggle at the top (README_zh.md:40):
```
[English](README.md) | [简体中文](README_zh.md)
```
Family definition (README_zh.md:43):
> MOSS‑TTS 家族是由 [MOSI.AI](https://mosi.cn/#hero) 与 [OpenMOSS 团队](https://www.open-moss.com/) 推出的开源 **语音与声音生成模型家族**。该系列面向 **高保真**、**高表现力** 与 **复杂真实场景** 设计，覆盖稳定长文本语音、多说话人对话、音色/角色设计、环境音效以及实时流式 TTS 等能力。

Entry links (README_zh.md:46):
> **从这里开始：** [快速开始](#快速开始) · [模型下载](https://huggingface.co/collections/OpenMOSS-Team/moss-tts) · [试听](#演示) · [微调](#微调) · [推理部署](#加速推理后端)

Task-chooser table, verbatim (README_zh.md:50-56):

| 你想完成的任务 | 建议入口 |
| --- | --- |
| 在 CPU 或浏览器中合成语音、克隆音色 | MOSS-TTS-Nano |
| 多语言长文本朗读、音色克隆 | MOSS-TTS-v1.5 · Local Transformer v1.5 |
| 多角色对话、播客与配音 | MOSS-TTSD |
| 实时流式语音生成 | MOSS-TTS-Realtime (`moss_tts_realtime/README.md`) |
| 设计音色或生成环境音效 | 模型概览 · MOSS-SoundEffect v2 (`moss_soundeffect_v2/README.md`) |

News (README_zh.md:58-82): three visible entries (2026.6.18 SGLang-Omni Day-0 `MossTTSLocal` support with OpenAI-compatible `/v1/audio/speech`; 2026.6.18 4B Local-Transformer-v1.5 with Qwen3-4B backbone and 48 kHz stereo via Audio-Tokenizer-v2; 2026.6.7 Audio-Tokenizer-v2) plus a collapsed `<details>` block of earlier updates (vLLM-Omni full-series support, SoundEffect-v2.0 DiT + Flow Matching up to 30 s at 48 kHz, TTS-v1.5 language tags and `[pause X.Ys]`, Nano, GGUF/ONNX torch-free inference, arXiv reports).
Contents index (README_zh.md:93-139) lists 介绍, 模型架构, 模型概览, 支持的语言, v1.5, Local-Transformer-v1.5, 快速开始 (Conda / `uv` / FlashAttention 2), 微调, llama.cpp 后端, 加速推理后端 (SGLang-Omni, vLLM-Omni), 评测, Nano, 语音编解码器, 更多信息/社区项目, 证书, 引用, 星标历史数据.
Five-model introduction (README_zh.md:149-155): MOSS‑TTS (flagship zero-shot cloning, long-form, pinyin/phoneme/duration control, multilingual + Chinese-English mix); MOSS‑TTSD v1.0 (dialogue, best objective scores, beats closed models in arena); MOSS‑VoiceGenerator (reference-free voice design from style prompts); MOSS‑TTS‑Realtime (multi-turn context-aware streaming, 180 ms TTFB, 377 ms with LLM first sentence); MOSS‑SoundEffect (controllable-duration SFX for film/game/interaction/data).
Architecture framing (README_zh.md:158-169): `MossTTSDelay` (long-context stability, speed, engineering) and `MossTTSLocal` (lightweight, streaming metrics) as complementary baselines; `MossTTSRealtime` as a capability design on history text plus user voice acoustics — with a three-row table mapping each architecture to its core mechanism (`多头并行 RVQ 预测，结合延迟模式调度` / `基于深度 Transformer 的时间同步 RVQ 模块` / `用于实时合成的分层文本-音频输入`) and a per-architecture README link.

Truncated files: `README_zh.md` (795 lines) is cut mid-table at line 179 — the chunk ends at `| **MOSS-TTS-Local-Transformer-v1.5** | \`MossTTSLocal\` | 4B | [[` with the note `... (truncated, 32118 more characters)`; all content after 模型概览 row 3 (quickstart, fine-tuning, backends, evaluation, Nano, codec, license, citation) is not in this chunk and not covered here.

**Covers:** .gitignore (ignore template + weights/outputs tail), .gitmodules (moss_audio_tokenizer submodule), MANIFEST.in (sdist include/graft/prune/exclude list), README_zh.md:1-179 (landing, task chooser, news, demo, contents, five-model intro, architecture table, model-overview head)
