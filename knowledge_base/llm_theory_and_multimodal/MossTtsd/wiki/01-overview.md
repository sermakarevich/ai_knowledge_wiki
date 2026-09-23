> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Overview
**In one sentence:** MOSS-TTSD is a long-form, multi-speaker, multilingual script-to-conversation synthesis model that turns dialogue scripts plus short reference audio into continuous expressive spoken performances.
## Key points
- Shifts the paradigm from "text-to-speech" to "script-to-conversation", prioritizing flow and emotional nuance of multi-party engagement over isolated single-speaker fidelity (01-overview.md:42-43).
- Supports 1 to 5 speakers with flexible control, handling natural turn-taking, overlapping speech patterns, and distinct persona maintenance (01-overview.md:48).
- Models extreme long context, supporting up to 60 minutes of coherent audio in a single session with consistent identity (01-overview.md:49, 01-overview.md:57).
- Performs state-of-the-art zero-shot voice cloning from only short reference audio via a continuation workflow of reference audio plus prefix transcripts (01-overview.md:51, 01-overview.md:105).
- Covers 20 languages including Chinese, English, Japanese, and European languages, with explicit per-language codes (01-overview.md:77-87).
- Targets high-variability scenarios: conversational media (AI Podcasts), dynamic commentary (Sports/Esports), and entertainment (Audiobooks, Dubbing, Crosstalk) (01-overview.md:50).
- Ships as open-source Python 3.10+ / PyTorch 2.0+ under Apache 2.0, installable via conda plus `requirements.txt` and `flash-attn` (01-overview.md:20-22, 01-overview.md:95-99).
---
## Paradigm: script-to-conversation
MOSS-TTSD is described as "the long-form dialogue specialist within our open-source MOSS‑TTS Family" (01-overview.md:42). Verbatim scope claim:
> "While foundational models typically prioritize high-fidelity single-speaker synthesis, MOSS-TTSD is architected to bridge the gap between isolated audio samples and cohesive, continuous human interaction." (01-overview.md:42)
> "The model represents a paradigm shift from "text-to-speech" to "script-to-conversation."" (01-overview.md:43)
Designed as "a robust backbone for creators and developers who require a seamless transition between distinct speaker personas without sacrificing narrative continuity" (01-overview.md:43), for "live talk show" spontaneity or "multilingual drama" complexity (01-overview.md:44).
## Highlights
Four verbatim highlight claims (01-overview.md:48-51):
- **From Monologue to Dialogue**: "supports 1 to 5 speakers with flexible control, handling natural turn-taking, overlapping speech patterns, and distinct persona maintenance."
- **Extreme Long-Context Modeling**: "supporting up to 60 minutes of coherent audio in a single session with consistent identity."
- **Diverse Scenario Adaptation**: "fine-tuned for high-variability scenarios including conversational media (AI Podcasts), dynamic commentary (Sports/Esports), and entertainment (Audiobooks, Dubbing, and Crosstalk)."
- **Multilingual & Zero-Shot Capabilities**: "requiring only short reference audio, with robust cross-lingual performance across major languages including Chinese, English, Japanese, and European languages."
## Releases / News
- `[2026-03-18]` efficient end-to-end SGLang inference for v1.0 (01-overview.md:55).
- `[2026-03-06]` end-to-end SGLang inference for v0.7; details in `./legacy/v0.7/README.md` (01-overview.md:56).
- `[2026-02-10]` v1.0 released: "redefines long-form synthesis with 60-minute single-session context and support for multi-party interactions" (01-overview.md:57).
- Earlier updates (2025-06-20 through 2025-11-01) trace v0, v0.5 (timbre switching, streaming, SiliconFlow API, fine-tuning code), v0.7 (32 kHz output, 960s→1700s single-pass length), SGLang up-to-16x speedup, 32 kHz XY-Tokenizer, and the Podever PDF/URL-to-podcast pipeline (01-overview.md:62-69).
## Supported languages
"MOSS-TTSD currently supports **20 languages**" (01-overview.md:77):
| Language | Code | Flag | Language | Code | Flag | Language | Code | Flag |
|---|---|---|---|---|---|---|---|---|
| Chinese | zh | 🇨🇳 | English | en | 🇺🇸 | German | de | 🇩🇪 |
| Spanish | es | 🇪🇸 | French | fr | 🇫🇷 | Japanese | ja | 🇯🇵 |
| Italian | it | 🇮🇹 | Hebrew | he | 🇮🇱 | Korean | ko | 🇰🇷 |
| Russian | ru | 🇷🇺 | Persian (Farsi) | fa | 🇮🇷 | Arabic | ar | 🇸🇦 |
| Polish | pl | 🇵🇱 | Portuguese | pt | 🇵🇹 | Czech | cs | 🇨🇿 |
| Danish | da | 🇩🇰 | Swedish | sv | 🇸🇪 | Hungarian | hu | 🇭🇺 |
| Greek | el | 🇬🇷 | Turkish | tr | 🇹🇷 | | | |
(01-overview.md:79-87)
## Installation
Exact commands (01-overview.md:95-99):
```bash
conda create -n moss_ttsd python=3.12 -y && conda activate moss_ttsd
pip install -r requirements.txt
pip install flash-attn
```
Badges declare `Python-3.10+`, `PyTorch-2.0+`, `License-Apache 2.0` (01-overview.md:20-22).
## Usage: continuation quick start
"MOSS-TTSD uses a **continuation** workflow: provide reference audio for each speaker, their transcripts as a prefix, and the dialogue text to generate. The model continues in each speaker's identity." (01-overview.md:105)
Exact identifiers and parameter names from the example (01-overview.md:115-136, 01-overview.md:179-215):
- `pretrained_model_name_or_path = "OpenMOSS-Team/MOSS-TTSD-v1.0"`, `audio_tokenizer_name_or_path = "OpenMOSS-Team/MOSS-Audio-Tokenizer"`
- `AutoProcessor.from_pretrained(..., trust_remote_code=True, codec_path=...)`, `AutoModel.from_pretrained(..., trust_remote_code=True, attn_implementation=..., torch_dtype=...)` with `attn_implementation = "flash_attention_2"` on CUDA else `"sdpa"`
- Speaker turn markers `[S1]` / `[S2]` in `prompt_text_speaker1`, `prompt_text_speaker2`, and `text_to_generate`
- `processor.encode_audios_from_wav(...)`, `processor.build_user_message(text=..., reference=...)`, `processor.build_assistant_message(audio_codes_list=...)`, `processor(batch_conversations, mode="continuation")`
- `model.generate(input_ids=..., attention_mask=..., max_new_tokens=2000)`, decode via `processor.decode(outputs)`, sample `sampling_rate` from `processor.model_config.sampling_rate`, outputs written as `{sample_idx}_{seg_idx}.wav` under `output/`
## Usage: batch inference
Verbatim script form (01-overview.md:229-237):
```bash
python inference.py \
  --model_path OpenMOSS-Team/MOSS-TTSD-v1.0 \
  --codec_model_path OpenMOSS-Team/MOSS-Audio-Tokenizer \
  --input_jsonl /path/to/input.jsonl \
  --save_dir outputs \
  --mode voice_clone_and_continuati
```
GPU control: "script automatically uses all visible GPUs. You can control GPU visibility via `export CUDA_VISIBLE_DEVICES=<device_ids>`." (01-overview.md:229)
Note: the chunk truncates the `--mode` value as `voice_clone_and_continuati` and cuts off after the `## Macro components` stub listing only `top-level-files/` (01-overview.md:237-241); no further batch flags or macro-component detail were present to cite, so they are not claimed here.
**Covers:** README.md (Overview, Highlights, News, Supported Languages, Installation, Usage/Quick Start, Batch Inference) as captured in chunks/01-overview.md:1-241
