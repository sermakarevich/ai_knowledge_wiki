[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Overview
**In one sentence:** MOSS-TTS Family is an open-source speech and sound generation model family for high-fidelity, high-expressiveness, complex real-world scenarios including long-form speech, multi-speaker dialogue, voice design, sound effects, and real-time streaming TTS.
## Key points
- MOSS-TTS Family is an open-source **speech and sound generation model family** from MOSI.AI and the OpenMOSS team, designed for **high-fidelity**, **high-expressiveness**, and **complex real-world scenarios** (README.md:47).
- The family covers stable long-form speech, multi-speaker dialogue, voice/character design, environmental sound effects, and real-time streaming TTS (README.md:47).
- Entry points are Quickstart, model weights on Hugging Face, samples demo, fine-tuning, and serving backends (README.md:50).
- The model chooser routes tasks to Nano (CPU/browser cloning), v1.5 / Local Transformer v1.5 (multilingual long-form), TTSD (dialogue/podcasts/dubbing), Realtime (streaming), and SoundEffect v2 / released models (voice design/SFX) (README.md:54-60).
- The repo tracks dated releases and backend support (e.g., 2026.6.18 Local-Transformer-v1.5 Day-0 SGLang-Omni support; 2026.6.2 vLLM-Omni full-series support; 2026.5.26 SoundEffect-v2.0 and TTS-v1.5 releases) (README.md:63-72).
- A demo video and a full Contents index (Introduction, Model Architecture, Released Models, Supported Languages, Quickstart, Fine-Tuning, llama.cpp backend, Accelerated Inference Backends, Evaluation, Nano, Audio-Tokenizer, License, Citation) structure the README (README.md:92-142).
- The Introduction frames the family as five production-ready models for audio that must sound like a real person, pronounce accurately, switch styles, stay stable over tens of minutes, and support dialogue/role-play/real-time use (README.md:151).
---
## Family definition
> MOSS‑TTS Family is an open‑source **speech and sound generation model family** from [MOSI.AI](https://mosi.cn/#hero) and the [OpenMOSS team](https://www.open-moss.com/). It is designed for **high‑fidelity**, **high‑expressiveness**, and **complex real‑world scenarios**, covering stable long‑form speech, multi‑speaker dialogue, voice/character design, environmental sound effects, and real‑time streaming TTS. (README.md:47)

> **Start here:** [Quickstart](#quickstart) · [Model weights](https://huggingface.co/collections/OpenMOSS-Team/moss-tts) · [Listen to samples](#demo) · [Fine-tuning](#fine-tuning) · [Serving backends](#accelerated-inference-backends) (README.md:50)

## Model chooser
Verbatim task-routing table (README.md:54-60):

| What you want to build | Start with |
| --- | --- |
| Speech and voice cloning on a CPU or in a browser | [MOSS-TTS-Nano](https://github.com/OpenMOSS/MOSS-TTS-Nano) |
| Multilingual long-form narration and voice cloning | [MOSS-TTS-v1.5](#moss-tts-v15) · [Local Transformer v1.5](#moss-tts-local-transformer-v15) |
| Multi-speaker dialogue, podcasts, and dubbing | [MOSS-TTSD](https://github.com/OpenMOSS/MOSS-TTSD) |
| Real-time streaming speech | [MOSS-TTS-Realtime](moss_tts_realtime/README.md) |
| Voice design or environmental sound effects | [Released models](#released-models) · [MOSS-SoundEffect v2](moss_soundeffect_v2/README.md) |

## News highlights
- `2026.6.18` SGLang-Omni Day-0 support for `MOSS-TTS-Local-Transformer-v1.5` (`MossTTSLocal` architecture, OpenAI-compatible `/v1/audio/speech` endpoint, streaming, voice cloning) (README.md:63).
- `2026.6.18` release of `MOSS-TTS-Local-Transformer-v1.5`: **4B** `MossTTSLocal` checkpoint, Qwen3-1.7B → Qwen3-4B backbone, **MOSS-Audio-Tokenizer-v2**, native **48 kHz stereo** output (README.md:64).
- `2026.6.7` release of `MOSS-Audio-Tokenizer-v2` with 48 kHz stereo input/output (README.md:65).
- Earlier updates (collapsed `<details>` block) record vLLM-Omni full-series support (`MossTTSDelay`, `MossTTSRealtime`, `MossTTSNano`), SoundEffect-v2.0 (DiT + Flow Matching, 48 kHz, up to 30 s), TTS-v1.5 (language tags, `[pause X.Ys]`), Nano (~100M params), GGUF/ONNX torch-free inference, and arXiv reports (README.md:67-88).

## Demo and Contents index
- Demo embeds a centered `<video>` sample (README.md:92-94).
- Contents index lists sections: Introduction, Model Architecture, Released Models, Supported Languages, MOSS-TTS-v1.5, Local-Transformer-v1.5, Quickstart (Conda / `uv` / FlashAttention 2), Fine-Tuning, llama.cpp backend, Accelerated Inference Backends (SGLang-Omni, vLLM-Omni), Evaluation, Nano, Audio-Tokenizer, Community Projects, LICENSE, Citation, Star History (README.md:96-142).

## Introduction (truncated in source)
> When a single piece of audio needs to **sound like a real person**, **pronounce every word accurately**, **switch speaking styles across content**, **remain stable over tens of minutes**, and **support dialogue, role‑play, and real‑time interaction**, a single TTS model is often not enough. The **MOSS‑TTS Family** breaks the workflow into five production‑ready models that can be used independent (README.md:151, sentence truncated in chunk — remainder not provided).

Truncated files: the chunk cuts off mid-sentence at README Introduction ("can be used independent", 01-overview.md:151); architecture, released-models, languages, quickstart, fine-tuning, backends, and evaluation sections are outside this chunk and not covered here.

**Covers:** README.md (family definition, model-chooser table, News, Demo, Contents index, Introduction opening)
