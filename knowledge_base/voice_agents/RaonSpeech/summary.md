# Technical Analysis: krafton-ai/Raon-Speech

**Repository:** https://github.com/krafton-ai/Raon-Speech
**Version analyzed:** unknown
**Date:** 2026-09-22
**Wiki:** [[index]]

## 1. Overview / What Problem It Solves

Problem space: bilingual (English/Korean) speech understanding, answering, and generation is split across separate ASR, TTS, and dialogue systems, and real-time full-duplex conversation (turn-taking, backchanneling, interruption/overlap handling, pause handling, multi-turn state) is not covered by offline utterance-in/utterance-out models (README.md:47-50, README.md:63-65).

How the repo addresses it: it releases a 9B SpeechLM family with two tracks sharing one core model and processor stack under `src/raon/` (README.md:37-43): Raon-Speech (offline SpeechLM: `TTS`, `STT`, `SpeechChat`, `TextQA`) (README.md:40) and Raon-SpeechChat (offline/realtime full-duplex) (README.md:41). Raon-Speech is trained on 1M+ hours of curated speech-text data and evaluated across 42 speech and text benchmarks; Raon-SpeechChat is continually trained on 116K hours of time-aligned dialogue data (README.md:47-49). The duplex track adds causal streaming, interleaved speech-text modeling, explicit interaction-state modeling, and text lookahead (README.md:48-50). Distribution is via Hugging Face checkpoints, Transformers integration, training/inference pipeline, interactive demo, and three Korean benchmarks (`KVoiceBench`, `KOpenAudioBench`, `KMMAU`) (README.md:52-53).

Primary user: an engineer building English/Korean voice interfaces who needs one checkpoint family for offline transcription/synthesis/spoken QA plus a full-duplex conversational mode.

## 2. High-Level Architecture

```text
checkpoints (local dir / Hub repo_id)
        │
        ▼
src/raon/pipeline.py (RaonPipeline) ──► config/infer.yaml defaults
        │
        ├─► src/raon/models/ (RaonModel / RaonDuplexModel: LM backbone + audio encoder + Mimi codec path)
        │         │
        │         ▼
        │     src/raon/modules/ (audio encoder, tokenizer, speaker encoder, etc.)
        │         │
        │         ▼
        │     src/raon/utils/ (processor, datasets, losses, prompts, special tokens)
        │
        ├─► offline heads: TTS / STT / SpeechChat / TextQA
        └─► duplex runtime: streaming full-duplex dialogue
                  │
                  ▼
        scripts/*.sh + demo/ (Gradio) + data/ (JSONL) → audio/text out
```

Data-flow narrative:

1. Load: caller passes a local checkpoint directory or Hub `repo_id` (`KRAFTON/Raon-Speech-9B`, `KRAFTON/Raon-SpeechChat-9B`) into `RaonPipeline(..., device="cuda", dtype="bfloat16")` (README.md:83-105); no-install fallback uses Hub remote code with `trust_remote_code=True` (README.md:126-164).
2. Prepare: SpeechLLM samples arrive as one-JSON-per-line with `conversations`, `audios`, optional `speaker_ref_audios`, `channel`, optional `system` (README.md:235-247); duplex training samples arrive as one-JSON-per-line stereo-wav metadata with `audio_path`, `language`, `channel`, `speak_first` (README.md:322-333).
3. Encode/condition: shared backbone combines LM backbone, audio encoder, and Mimi codec path with trainable blocks `input_adaptor`, `output_adaptor`, `audio_lm_head`, `proj_code`, `code_predictor` (README.md:225-231); speaker-conditioning path is toggled by `USE_SPEAKER_EMBEDDING` (README.md:302-318).
4. Execute: offline inference runs `scripts/infer.sh` (defaults from `config/infer.yaml`, `--data_dir` scanned for JSONL, `--attn_implementation` selecting `sdpa`/`fa`) or `python -m raon.generate` or `RaonPipeline` methods (README.md:249-295); duplex inference/training runs the parallel `duplex_*` entries and demo scripts (README.md:117-124).
5. Emit: text answers, transcriptions, or `(audio, sr)` tuples persisted via `pipe.save_audio`; TTS supports speaker-reference continuation via `tts_continuation` (README.md:272-295).

Persistent state lives in checkpoint directories (local path or Hub-downloaded snapshot, cf. `hf download ... --local-dir /path/to/model_dir` (README.md:107-113)), JSONL datasets under `data/` (sample eval under `data/speechllm/eval`) (README.md:235-247), YAML configs under `config/` (README.md:249-258), and generated outputs under caller-specified `--output_dir` (README.md:260-270). No database or server-side store is documented in the wiki pages.

## 3. The Bilingual SpeechLM Core (RaonModel)

Representation: one shared backbone class with two model types. The wiki states the package backbone is one shared `RaonModel` (LM backbone + audio encoder + Mimi codec path) with model types `raon` (Raon-Speech) and `raon_duplex` (Raon-SpeechChat) (README.md:225-231). Code lives under `src/raon/models/` (`RaonModel` / `RaonDuplexModel`), with `src/raon/modules/` for audio encoder, tokenizer, speaker encoder and `src/raon/utils/` for processor, datasets, losses, prompts, special tokens (README.md:205-223).

Named kinds/types with citations:

- Track: `Raon-Speech (Offline SpeechLM)` with channels `TTS`, `STT`, `SpeechChat`, `TextQA` (README.md:40).
- Track: `Raon-SpeechChat (Offline/Realtime Full-Duplex)` (README.md:41).
- Model types: `raon` and `raon_duplex` (README.md:225-231).
- Trainable blocks: `input_adaptor`, `output_adaptor`, `audio_lm_head`, `proj_code`, `code_predictor` (README.md:225-231); frozen set at training time adds `audio_encoder` and `speaker_encoder` (README.md:302-318).
- SpeechLLM channel values: `tts`, `stt`, `speech-chat`, `textqa` (README.md:235-247).
- Duplex channel values: `full_duplex`, `duplex_instruct` (README.md:322-333); language codes `eng`, `kor` (README.md:322-333).
- Duplex mechanisms: causal streaming, interleaved speech-text modeling, explicit interaction-state modeling, text lookahead (README.md:48-50).

Key queries (verbatim API surface, README.md:272-295):

```python
pipe = RaonPipeline("/path/to/model", device="cuda", dtype="bfloat16", config="/path/to/config.yaml")

text = pipe.stt("/path/to/stt.wav")
audio, sr = pipe.tts("Hello!", speaker_audio="/path/to/speaker_ref.wav")
ans1 = pipe.speech_chat("/path/to/speech-chat.wav")
ans2 = pipe.textqa("What did the speaker say?", audio="/path/to/textqa.wav")

pipe.save_audio((audio, sr), "/path/to/tts.wav")

audio, sr = pipe.tts_continuation(
    target_text="Continue this sentence.",
    ref_audio="/path/to/speaker_ref.wav",
    ref_text="Optional transcription of ref audio.",
)
```

## 4. LLM / External Service Integration

The repo calls no hosted LLM or third-party inference API. All inference is local: a checkpoint directory or Hub `repo_id` loaded via `RaonPipeline` or `AutoModel.from_pretrained(..., trust_remote_code=True)` (README.md:52-53, README.md:83-105). Hugging Face appears only as artifact hosting (`https://huggingface.co/KRAFTON`, model cards `KRAFTON/Raon-Speech-9B` and `KRAFTON/Raon-SpeechChat-9B`) plus `hf download` for pre-fetching (README.md:29-35, README.md:107-113). The demo URL `https://raon.krafton.ai` is a hosted demo link, not a programmatic API dependency (README.md:29-35). No API keys, tokens (beyond standard Hub access for gated downloads), or service env vars are documented in the wiki pages. Required vs. optional: local PyTorch/CUDA execution is required (`bfloat16`/`float16`, CUDA GPU recommended) (README.md:77-81); `flash-attn` is optional/training-only; demo extras (`sglang`, `gradio`, `fastapi`, `uvicorn`) install via `pip install -e ".[demo]"` (01-overview.md:35-46).

## 5. The Offline SpeechLLM and Full-Duplex Workflow

Step by step (function/entry citations from the overview page; line references are `README.md` lines via the wiki):

1. Install and select mode — `pip install -r requirements.txt` + `pip install -e .` (or `uv sync`), optional `pip install -e ".[demo]"`, optional `pip install flash-attn` (README.md:168-195). Mode 1 (installed) unlocks `scripts/infer.sh`, `scripts/duplex_infer.sh`, `scripts/train.sh`, `scripts/duplex_train.sh`, `demo/run_gradio_demo.sh`, `demo/run_gradio_duplex_demo.sh`, and `from raon import RaonPipeline` (README.md:117-124); Mode 2 (no install) supports only the Gradio fallback and pure-Transformers Hub flow (README.md:126-164).
2. Acquire weights — `RaonPipeline("KRAFTON/Raon-Speech-9B", device="cuda", dtype="bfloat16")` or the `Raon-SpeechChat-9B` id (README.md:83-105), or pre-download with `hf download KRAFTON/Raon-Speech-9B --local-dir /path/to/model_dir` (README.md:107-113).
3. Stage data — write SpeechLLM JSONL (`conversations`, `audios`, `speaker_ref_audios`, `channel`, `system`) (README.md:235-247) or duplex JSONL (`audio_path` stereo 2-channel wav, `language`, `channel`, `speak_first`) (README.md:322-333).
4. Run offline inference — `bash scripts/infer.sh` with `config/infer.yaml` defaults, `--attn_implementation` (`sdpa` default, `fa` for FlashAttention), `--data_dir` scanned for JSONL (README.md:249-258); or `python -m raon.generate --model_path ... --data_dir ... --output_dir ... --config ... --batch_size 4 --attn_implementation sdpa` (README.md:260-270).
5. Run programmatic inference — `pipe.stt(...)`, `pipe.tts(...)`, `pipe.speech_chat(...)`, `pipe.textqa(...)`, `pipe.save_audio(...)`, `pipe.tts_continuation(...)` (README.md:272-295).
6. Train — `bash scripts/train.sh` (SpeechLLM) / duplex counterpart; preset variables at top of script; `NPROC_PER_NODE` (multi-GPU torchrun), `MASTER_PORT` (rendezvous port), `USE_SPEAKER_EMBEDDING` (speaker-conditioning toggle); frozen blocks `audio_encoder`, `input_adaptor`, `output_adaptor`, `audio_lm_head`, `proj_code`, `code_predictor`, `speaker_encoder` (README.md:302-318). Worked examples: `examples/message_example.py`, `examples/message_example.ipynb` (README.md:297-300).

## 6. Key Files

| File | Lines | What It Does |
|---|---|---|
| `README.md` | n/s in wiki (cited through README.md:29-333) | Sole behavioral spec in wiki scope: tracks, links, benchmarks, setup, layout, inference/training contracts |
| `src/raon/pipeline.py` | n/s in wiki (layout README.md:205-223) | High-level API: `RaonPipeline` with `stt/tts/speech_chat/textqa/save_audio/tts_continuation` |
| `src/raon/models/` | n/s in wiki (layout README.md:205-223) | `RaonModel` / `RaonDuplexModel`: LM backbone + audio encoder + Mimi codec path |
| `src/raon/modules/` | n/s in wiki (layout README.md:205-223) | Audio encoder, tokenizer, speaker encoder, related blocks |
| `src/raon/utils/` | n/s in wiki (layout README.md:205-223) | Processor, datasets, losses, prompts, special tokens |
| `src/raon/train.py` | n/s in wiki (layout README.md:205-223; usage README.md:302-318) | SpeechLLM training entry behind `scripts/train.sh` |
| `src/raon/duplex_train.py` | n/s in wiki (layout README.md:205-223) | Full-duplex training entry behind `scripts/duplex_train.sh` |
| `src/raon/generate.py` | n/s in wiki (layout README.md:205-223; CLI README.md:260-270) | SpeechLLM JSONL inference entry (`python -m raon.generate`) |
| `src/raon/duplex_generate.py` | n/s in wiki (layout README.md:205-223) | Full-duplex inference entry |
| `scripts/infer.sh` | n/s in wiki (usage README.md:249-258) | Shell wrapper for offline inference |
| `scripts/duplex_infer.sh` | n/s in wiki (modes README.md:117-124) | Shell wrapper for duplex inference |
| `scripts/train.sh` / `scripts/duplex_train.sh` | n/s in wiki (usage README.md:302-318) | Shell wrappers presetting `NPROC_PER_NODE`/`MASTER_PORT`/`USE_SPEAKER_EMBEDDING` |
| `config/infer.yaml` | n/s in wiki (usage README.md:249-258) | Task defaults for inference |
| `data/speechllm/eval` | n/s in wiki (format README.md:235-247) | Sample eval JSONL data |
| `demo/run_gradio_demo.sh` / `demo/run_gradio_duplex_demo.sh` | n/s in wiki (modes README.md:117-124) | Interactive demo launchers |
| `examples/message_example.py` / `.ipynb`, `examples/duplex_example.ipynb` | n/s in wiki (refs README.md:126-164, README.md:297-300) | No-install Hub flow and worked message examples |
| `.gitignore` | 217 | Stock Python hygiene template; no model/data-specific patterns (02-top-level-files.md:5) |
| `NOTICE` | 40 | Legal attribution: RAON 2026 plus five third-party blocks (02-top-level-files.md:5) |
| `requirements.txt` | 18 | Runtime pins (5 pinned, 9 unpinned) installed via `pip install -r requirements.txt` (02-top-level-files.md:5) |

## 7. Dependencies

Required first (exact specifiers as written, requirements.txt:1-17):

| Package | Version constraint | Purpose |
|---|---|---|
| `accelerate` | `>=1.10.1` | Distributed/large-model execution support |
| `pydantic` | `>=2.11.10` | Config/schema validation |
| `soundfile` | `>=0.13.1` | Audio file I/O (wav read/write behind `save_audio`/dataset loading) |
| `transformers` | `>=4.57.1,<5.0` | Hub integration and `AutoModel` remote-code loading path |
| `datasets` | `>=3.0.0` | JSONL dataset handling |
| `torch` | (unpinned) | Tensor compute; must match CUDA (README.md:77-81) |
| `torchaudio` | (unpinned) | Audio ops; must match CUDA (README.md:77-81) |
| `speechbrain` | (unpinned) | ECAPA-TDNN speaker encoder upstream (NOTICE:9-40) |
| `einops` | (unpinned) | Tensor rearrangement ops |
| `numpy` | (unpinned) | Numeric base |
| `requests` | (unpinned) | HTTP (Hub/demo) transport |
| `tqdm` | (unpinned) | Progress reporting |
| `tensorboard` | (unpinned) | Training logging |
| `kernels` | (unpinned) | Kernel utilities |

Setup-only/optional (01-overview.md:35-46): `flash-attn` (optional, training only); demo extra `.[demo]` pulls `sglang`, `gradio`, `fastapi`, `uvicorn`. Python constraint: `>=3.11`; compute expects CUDA GPU with `bfloat16`/`float16` (README.md:77-81).

## 8. CLI / Usage Surface

Entry points:

| Entry | Command | Purpose |
|---|---|---|
| Offline inference | `bash scripts/infer.sh` | JSONL inference with `config/infer.yaml` defaults (README.md:249-258) |
| Duplex inference | `bash scripts/duplex_infer.sh` | Full-duplex inference (README.md:117-124) |
| Offline training | `bash scripts/train.sh` | SpeechLLM training (README.md:302-318) |
| Duplex training | `bash scripts/duplex_train.sh` | Full-duplex training (README.md:117-124) |
| Module inference | `python -m raon.generate --model_path ... --data_dir ... --output_dir ... --config ... --batch_size 4 --attn_implementation sdpa` | Advanced CLI (README.md:260-270) |
| Python API | `from raon import RaonPipeline` then `stt/tts/speech_chat/textqa/save_audio/tts_continuation` | Programmatic use (README.md:272-295) |
| Demos | `demo/run_gradio_demo.sh`, `demo/run_gradio_duplex_demo.sh` | Interactive Gradio (README.md:117-124) |
| Weights fetch | `hf download KRAFTON/Raon-Speech-9B --local-dir /path/to/model_dir` | Pre-download (README.md:107-113) |

Env-var table:

| Variable | Default / context | Effect |
|---|---|---|
| `NPROC_PER_NODE` | preset at top of `scripts/train.sh` | Multi-GPU torchrun width (README.md:302-318) |
| `MASTER_PORT` | preset at top of `scripts/train.sh` | Rendezvous port (README.md:302-318) |
| `USE_SPEAKER_EMBEDDING` | preset at top of `scripts/train.sh` | Toggles speaker-conditioning inputs (README.md:302-318) |

Config table:

| Config | Used by | Notes |
|---|---|---|
| `config/infer.yaml` | `scripts/infer.sh` | Task defaults (README.md:249-258) |
| `--config /path/to/config.yaml` | `python -m raon.generate`, `RaonPipeline(..., config=...)` | Override path (README.md:260-295) |
| `--attn_implementation` | inference entries | `sdpa` default, `fa` for FlashAttention (README.md:249-270, README.md:302-318) |
| `--data_dir` / `--output_dir` / `--batch_size` | `python -m raon.generate` | JSONL scan dir, output dir, batch width (README.md:260-270) |

## 9. Extensibility Points

- New offline capability/channel: extend the `channel` contract (`tts`, `stt`, `speech-chat`, `textqa`) and the JSONL loader in `src/raon/utils/` (datasets), wiring the head through `src/raon/models/` and exposing it in `src/raon/pipeline.py` (layout and contracts README.md:205-247, API README.md:272-295).
- New backbone behavior (adaptors, codec path, LM head): modify trainable blocks `input_adaptor`, `output_adaptor`, `audio_lm_head`, `proj_code`, `code_predictor` in `src/raon/models/`, with encoder/tokenizer pieces in `src/raon/modules/` (README.md:225-231).
- New prompt/special-token convention: edit prompts and special tokens in `src/raon/utils/` (README.md:205-223).
- New loss or data collation: extend losses/datasets in `src/raon/utils/` (README.md:205-223).
- Duplex interaction policy (language prompts, channel types, speaking-mode defaults): extend `src/raon/duplex_train.py` / `src/raon/duplex_generate.py` and the stereo-JSONL fields (`language`, `channel`, `speak_first`) (README.md:322-333).
- Inference serving/demo: wrap `RaonPipeline` methods or add scripts under `scripts/` and launchers under `demo/` (entries README.md:117-124, API README.md:272-295).
- Dependency hygiene: pinning currently unpinned runtime (`torch`, `torchaudio`, `speechbrain`, others) belongs in `requirements.txt` (requirements.txt:1-17).

## 10. Limitations and Gotchas

- **Duplex contract is truncated in the available source.** The wiki's duplex table ends mid-description in the `speak_first` row and states no further full-duplex inference/training details are present in that chunk (01-overview.md:114-123). Do not infer stereo alignment, turn-taking labels, or sidecar fields beyond `audio_path`/`language`/`channel`/`speak_first` (README.md:322-333).
- **Half the entry points vanish without install.** `python -m raon.*` and the `demo/gradio_duplex_demo.py` realtime runtime require `raon` installed; without install only the Gradio fallback and pure-Transformers Hub flow work (README.md:126-164).
- **Training freezes most of the speech stack by default.** Current code freezes `audio_encoder`, `input_adaptor`, `output_adaptor`, `audio_lm_head`, `proj_code`, `code_predictor`, `speaker_encoder` (README.md:302-318); fine-tuning beyond defaults requires editing the freeze set and the `USE_SPEAKER_EMBEDDING` toggle.
- **CUDA + matched torch stack is effectively mandatory.** Requirements call for Python `>=3.11`, CUDA GPU, `bfloat16`/`float16`, and PyTorch/Torchaudio matching CUDA (README.md:77-81), while `requirements.txt` leaves `torch`, `torchaudio`, `speechbrain`, and six others unpinned (requirements.txt:1-17) — environment drift is the likely first failure.
- **Latency numbers are narrow.** The published RTF/TTFT/TBT table covers single-GPU streaming TTS on LibriSpeech `test-clean` for two GPUs (RTX 6000 Pro Blackwell, L40S) (README.md:65-71); it does not generalize to duplex, STT, or multi-GPU serving.
- **Repo root carries no model/data ignore rules.** `.gitignore` is the stock Python template with no checkpoint, dataset, or audio patterns (02-top-level-files.md:13-28); large-asset hygiene depends on Hub/outside paths, not the ignore file.

## 11. How It Compares to Alternatives

- Qwen3 / Qwen3OmniMoe (Alibaba Cloud): upstream omni-model family explicitly attributed in `NOTICE` (NOTICE:9-40); the general-purpose alternative for joint text-speech modeling, against which Raon positions as a bilingual EN/KO speech-specialized family with a dedicated duplex track (README.md:47-50).
- Kyutai Mimi audio codec: attributed codec upstream (NOTICE:9-40) and named as part of the RaonModel codec path (README.md:225-231); using Mimi standalone (or a Mimi-based generator) is the lower-level alternative to adopting the full Raon pipeline.
- SpeechBrain (ECAPA-TDNN speaker encoder): attributed speaker-encoder upstream (NOTICE:9-40) with a freeze/toggle role in training (`speaker_encoder`, `USE_SPEAKER_EMBEDDING`) (README.md:302-318); the modular alternative for speaker conditioning without the SpeechLM.
- HuggingFace Transformers ecosystem: attributed platform (NOTICE:9-40) and the no-install consumption path (`trust_remote_code=True`, Hub `repo_id`s) (README.md:52-53, README.md:126-164); the generic alternative is assembling ASR/TTS/dialogue from Hub components rather than taking Raon's single-family offline+duplex stack.

Positioning: Raon-Speech competes not as a codec, speaker encoder, or generic Hub toolkit but as a single bilingual checkpoint family that bundles offline speech tasks and realtime full-duplex dialogue behind one backbone and one pipeline API.

## Appendix: Selected Code Snippets

1. Model loading, local-or-Hub (`README.md:83-88` via 01-overview.md:49-55):

```python
pipe = RaonPipeline("KRAFTON/Raon-Speech-9B", device="cuda", dtype="bfloat16")
# or
pipe = RaonPipeline("KRAFTON/Raon-SpeechChat-9B", device="cuda", dtype="bfloat16")
```

2. Full programmatic pipeline surface (`README.md:272-295` via 01-overview.md:96-112):

```python
pipe = RaonPipeline("/path/to/model", device="cuda", dtype="bfloat16", config="/path/to/config.yaml")

text = pipe.stt("/path/to/stt.wav")
audio, sr = pipe.tts("Hello!", speaker_audio="/path/to/speaker_ref.wav")
ans1 = pipe.speech_chat("/path/to/speech-chat.wav")
ans2 = pipe.textqa("What did the speaker say?", audio="/path/to/textqa.wav")

pipe.save_audio((audio, sr), "/path/to/tts.wav")

audio, sr = pipe.tts_continuation(
    target_text="Continue this sentence.",
    ref_audio="/path/to/speaker_ref.wav",
    ref_text="Optional transcription of ref audio.",
)
```

3. Advanced generation CLI (`README.md:260-270` via 01-overview.md:87-95):

```bash
python -m raon.generate \
  --model_path /path/to/model \
  --data_dir /path/to/data_dir \
  --output_dir /path/to/output_dir \
  --config /path/to/config.yaml \
  --batch_size 4 \
  --attn_implementation sdpa
```

4. Environment requirements header (`requirements.txt:1-17` via 02-top-level-files.md:46-68):

```text
# RAON - Environment Requirements
# Install with: pip install -r requirements.txt
```

Pinned subset: `accelerate>=1.10.1`, `pydantic>=2.11.10`, `soundfile>=0.13.1`, `transformers>=4.57.1,<5.0`, `datasets>=3.0.0`; remainder (`einops`, `kernels`, `numpy`, `requests`, `speechbrain`, `tensorboard`, `torch`, `torchaudio`, `tqdm`) unpinned.
