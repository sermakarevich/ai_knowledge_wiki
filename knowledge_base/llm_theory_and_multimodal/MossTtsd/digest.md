> [[index|Wiki]] | [[summary|Summary]]
# OpenMOSS/MOSS-TTSD — Digest

## 1. [[wiki/01-overview|Overview]]
**In one sentence:** MOSS-TTSD is a long-form, multi-speaker, multilingual script-to-conversation synthesis model that turns dialogue scripts plus short reference audio into continuous expressive spoken performances.
## Key points
- Shifts the paradigm from "text-to-speech" to "script-to-conversation", prioritizing flow and emotional nuance of multi-party engagement over isolated single-speaker fidelity (01-overview.md:42-43).
- Supports 1 to 5 speakers with flexible control, handling natural turn-taking, overlapping speech patterns, and distinct persona maintenance (01-overview.md:48).
- Models extreme long context, supporting up to 60 minutes of coherent audio in a single session with consistent identity (01-overview.md:49, 01-overview.md:57).
- Performs state-of-the-art zero-shot voice cloning from only short reference audio via a continuation workflow of reference audio plus prefix transcripts (01-overview.md:51, 01-overview.md:105).
- Covers 20 languages including Chinese, English, Japanese, and European languages, with explicit per-language codes (01-overview.md:77-87).
- Targets high-variability scenarios: conversational media (AI Podcasts), dynamic commentary (Sports/Esports), and entertainment (Audiobooks, Dubbing, Crosstalk) (01-overview.md:50).
- Ships as open-source Python 3.10+ / PyTorch 2.0+ under Apache 2.0, installable via conda plus `requirements.txt` and `flash-attn` (01-overview.md:20-22, 01-overview.md:95-99).

## 2. [[wiki/02-top-level-files|Top-level-files]]
**In one sentence:** The repository root exposes the runnable surface of MOSS-TTSD — batch inference, shared generation utilities, an interactive demo, install pins, and the Chinese project readme.
## Key points
- `inference.py` is the multi-GPU batch entry point that shards a JSONL over all visible CUDA devices, prepares each line via `generation_utils.prepare_sample`, and merges per-rank outputs into `output.jsonl` (inference.py:875, inference.py:901, inference.py:1016).
- `generation_utils.py` centralizes text normalization, sharded JSONL reading, path resolution, sampling-arg resolution, and multi-speaker prompt-audio encoding consumed by `inference.py` (generation_utils.py:20, generation_utils.py:87, generation_utils.py:202, generation_utils.py:270).
- `gradio_demo.py` is the interactive 1–5 speaker demo with hard-coded `OpenMOSS-Team/MOSS-TTSD-v1.0` and `OpenMOSS-Team/MOSS-Audio-Tokenizer` defaults, preset reference audios, and CUDA attention auto-selection (gradio_demo.py:417, gradio_demo.py:423, gradio_demo.py:485).
- `inference.py` supports four modes — `generation`, `continuation`, `voice_clone`, `voice_clone_and_continuation` — defaulting to `generation`, with `--text_normalize` and `--sample_rate_normalize` off by default (inference.py:947, inference.py:963).
- Sampling defaults resolve as CLI value > `generation_config.json` > fallback (`max_new_tokens` 8192, `temperature` 1.1, `top_p` 0.9, `top_k` 50, `repetition_penalty` 1.1) via `resolve_sampling_args` (generation_utils.py:202).
- `README_zh.md` documents the Chinese quick-start `continuation` workflow, the batch `inference.py` invocation, the 20-language table, and the SGLang fused-model path (README_zh.md:1135, README_zh.md:1262, README_zh.md:1109).
- `requirements.txt` pins the runtime (`torch==2.9.1+cu128`, `transformers==5.0.0`, `gradio==6.5.1`, `soundfile==0.13.1`) with `flash_attn` left commented out (requirements.txt:1).
- Truncated in this chunk: `generation_utils.py` cuts off at `if mode =` (generation_utils.py:389, 6160 further characters not shown); `gradio_demo.py` cuts off at `_encode_reference_audio_codes(processo` (gradio_demo.py:753, 16613 further characters not shown); `README_zh.md` cuts off at `http://loc` (README_zh.md:1388, 8089 further characters not shown) — contents beyond those points are not claimed here.

## The system in five moves
1. Start from a dialogue script tagged `[S1]`–`[S5]` plus short reference audio and prefix transcripts per speaker, framing synthesis as script-to-conversation rather than isolated utterances.
2. Clone voices zero-shot via the continuation workflow, continuing each speaker's identity with consistent persona and turn-taking across up to 60 minutes and 20 languages.
3. Normalize dialogue text and resample/mono/encode prompt audios through shared utilities, assembling multi-speaker prefixed prompts and resolved sampling args.
4. Generate continuations in batch over sharded JSONL on all visible GPUs or interactively in the 1–5 speaker Gradio demo, decoding audio codes to per-segment wav outputs.
5. Ship and scale the runnable surface as open-source pinned Python/PyTorch with batch, demo, Chinese readme, and SGLang fused-model serving paths.
