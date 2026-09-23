# Technical Analysis: OpenMOSS/MOSS-TTSD

**Repository:** https://github.com/OpenMOSS/MOSS-TTSD
**Version analyzed:** unknown
**Date:** 2026-09-22
**Wiki:** [[index]]

## 1. Overview / What Problem It Solves

Single-speaker text-to-speech produces isolated high-fidelity utterances but does not sustain multi-party interaction: turn-taking, persona stability across interruptions, emotional continuity, and coherence over tens of minutes (01-overview.md:15-17). Target formats are conversational media (AI podcasts), dynamic commentary (sports/esports), and entertainment (audiobooks, dubbing, crosstalk), plus live-talk spontaneity and multilingual drama (01-overview.md:17, 01-overview.md:22).

MOSS-TTSD addresses this by reframing synthesis as script-to-conversation: a tagged dialogue script plus one short reference audio and prefix transcript per speaker is rendered as continuous expressive audio in a single session (01-overview.md:14-16, 01-overview.md:50). The v1.0 design supports 1–5 speakers with per-speaker identity conditioning, up to 60 minutes of coherent output per session, zero-shot cloning from short references, and 20 languages including Chinese, English, and Japanese (01-overview.md:20-23, 01-overview.md:30). It ships as open-source Python 3.10+ / PyTorch 2.0+ under Apache 2.0, installed via conda plus `requirements.txt` and `flash-attn` (01-overview.md:11, 01-overview.md:42-47). Primary user: creators and developers building long-form multi-speaker audio (podcasts, commentary, audiobooks, dubbing) from scripts (01-overview.md:17).

## 2. High-Level Architecture

```
 dialogue JSONL / script text ([S1]..[S5])
            │
            ▼
 generation_utils.py ── normalize_text / streaming_jsonl_reader /
            │           path resolution / resolve_sampling_args
            ▼
 prompt-audio prep ── _load_mono_wav / _maybe_resample /
            │         _preprocess_prompt_wavs / _encode_concat_prompt_audio
            ▼
 message assembly ── build_user_message / build_assistant_message /
            │         processor(mode="continuation")
            ▼
 TTSD model + MOSS-Audio-Tokenizer ── model.generate(...) ► decode
            │         (flash_attention_2 / sdpa; bf16 on CUDA)
            ▼
  per-segment WAV ({sample_idx}_{seg_idx}.wav) ──► merged output.jsonl
```

Data flow: (1) Input ingestion — batch driver shards an input JSONL across all visible CUDA devices and reads rank-assigned lines via `streaming_jsonl_reader` (02-top-level-files.md:80). (2) Sample preparation — each line is normalized, validated, and encoded via `prepare_sample`, which resolves speaker fields, resamples prompt wavs, and encodes reference audio codes (02-top-level-files.md:64). (3) Prompted generation — processor builds continuation messages from tagged text plus reference codes; the model generates audio-code tokens under resolved sampling arguments (01-overview.md:55, 02-top-level-files.md:50). (4) Decoding and persistence — codes are decoded to waveforms at `processor.model_config.sampling_rate` and written as per-segment WAV files plus a merged `output.jsonl` (01-overview.md:56, 02-top-level-files.md:80, 02-top-level-files.md:96). (5) Interactive path — `gradio_demo.py` reuses the same backend with cached model loading and 1–5 speaker panels (02-top-level-files.md:112-118). Persistent state lives on disk and on Hugging Face: input JSONL, `output/` WAV files, per-rank and merged `output.jsonl`, `generation_config.json` beside the model weights, and the pretrained checkpoints `OpenMOSS-Team/MOSS-TTSD-v1.0` and `OpenMOSS-Team/MOSS-Audio-Tokenizer` (01-overview.md:52, 02-top-level-files.md:50, 02-top-level-files.md:76, 02-top-level-files.md:80). No database or server-side session store is described in the wiki pages.

## 3. Script-to-Conversation Dialogue as the Core Abstraction

The central concept is a tagged dialogue script rendered by continuation: "provide reference audio for each speaker, their transcripts as a prefix, and the dialogue text to generate. The model continues in each speaker's identity" (01-overview.md:50). Representation is plain text with speaker-turn markers `[S1]`–`[S5]` embedded in `prompt_text_speakerN` prefix transcripts and in `text_to_generate` (01-overview.md:52-54). Reference identity is the pairing of each `prompt_audio_speakerN` wav with its `prompt_text_speakerN` transcript; batch rows additionally carry `base_path`, `text`, and optional `output_audio` / `*_path` keys absolutized by path helpers (02-top-level-files.md:34-38, 02-top-level-files.md:120).

Named kinds/types: four inference modes — `generation`, `continuation`, `voice_clone`, `voice_clone_and_continuation` — with `generation` the default (02-top-level-files.md:82-95); speaker-count range `MIN_SPEAKERS = 1`, `MAX_SPEAKERS = 5` (02-top-level-files.md:98-111); language codes `zh en de es fr ja it he ko ru fa ar pl pt cs da sv hu el tr` covering the 20 supported languages (01-overview.md:31-40); attention implementations `flash_attention_2` / `sdpa` / `eager` / `none` / `auto` (02-top-level-files.md:114-116).

Key queries are function calls, not a query language. Verbatim assembly snippet:

```python
processor.encode_audios_from_wav(...)
processor.build_user_message(text=..., reference=...)
processor.build_assistant_message(audio_codes_list=...)
processor(batch_conversations, mode="continuation")
```

(01-overview.md:55). Speaker pairing is discovered by `_collect_speaker_fields` matching `prompt_audio_speaker(\d+)` against `prompt_text_speaker(\d+)` and returning the sorted intersection (02-top-level-files.md:62).

## 4. LLM / External Service Integration

The repository calls no LLM or third-party inference API at generation time. All synthesis is local PyTorch inference: `AutoProcessor` and `AutoModel` loaded with `trust_remote_code=True` from Hugging Face checkpoint identifiers, run on CUDA (bfloat16) or CPU (float32) (01-overview.md:52-53, 02-top-level-files.md:78, 02-top-level-files.md:116). The Hugging Face hub acts only as a weight source (`OpenMOSS-Team/MOSS-TTSD-v1.0`, `OpenMOSS-Team/MOSS-Audio-Tokenizer`); no API key or chat-completion call is involved (01-overview.md:52, 02-top-level-files.md:76). A historical SiliconFlow API example is noted in the release history (01-overview.md:28) but no current API path, key, or env var for it is specified in the wiki pages. A fused SGLang serving path (clone `OpenMOSS/sglang`, fuse via `scripts/fuse_moss_tts_delay_with_codec.py`, serve with delay-pattern flags) is documented in the Chinese readme section but no external paid provider or secret is required for the default paths (02-top-level-files.md:120). No provider-specific environment variables are documented; the only env var named is `CUDA_VISIBLE_DEVICES` for GPU visibility (01-overview.md:67). Required network access: downloading model weights and Python packages. Optional: CUDA + `flash_attn` for the fast attention path.

## 5. Voice-Clone-and-Continuation Synthesis Pipeline

Step by step, with the defining function per step:

1. Normalize dialogue text — `normalize_text(text: str) -> str` in generation_utils.py:20 strips control/bracket characters, maps laughter fillers (`哈{2,}` to `[笑]`, `ha( ha)+` to `[laugh]`), normalizes dashes/ellipses and CJK punctuation, collapses repeated sentence-final marks, and merges consecutive same-speaker segments (02-top-level-files.md:15-21). A duplicate implementation exists in gradio_demo.py:545-750 (02-top-level-files.md:118).
2. Shard and stream batch input — `streaming_jsonl_reader(jsonl_path, rank, world_size, skip_invalid_json)` in generation_utils.py:87 keeps only lines where `(line_no - 1) % world_size == rank`, skips blanks, and warns-skips or raises on malformed JSON (02-top-level-files.md:23-32).
3. Resolve relative paths — `_to_abs_path_str` / `_abspath_record_paths` / `_resolve_path(maybe_path, base_path)` / `_make_output_record` in generation_utils.py:119-156 absolutize `output_audio`, `prompt_audio(_speakerN)`, and `*_path` keys against each record's `base_path` and stamp `record["id"]` (02-top-level-files.md:34-38).
4. Resolve sampling arguments — `_load_generation_config(model_path)` in generation_utils.py:187-199 reads `<model_path>/generation_config.json` or returns `{}` with a warning; `resolve_sampling_args` in generation_utils.py:202 applies CLI value > config file > fallback (`max_new_tokens` 8192, `temperature` 1.1, `top_p` 0.9, `top_k` 50, `repetition_penalty` 1.1) (02-top-level-files.md:40-58).
5. Prepare prompt audio — `_load_mono_wav` / `_maybe_resample` / `_preprocess_prompt_wavs` in generation_utils.py:228-267 read wavs as float32, mix multi-channel to mono, and resample prompts to their minimum rate (when enabled) then to the model target rate (02-top-level-files.md:60).
6. Assemble multi-speaker conditioning — `_collect_speaker_fields` / `_build_prefixed_text` / `_encode_concat_prompt_audio` / `_encode_references` in generation_utils.py:270-357 match speaker id pairs, prepend missing `[SN]` tags, concatenate per-speaker wavs and encode them, and return per-speaker code lists (02-top-level-files.md:62).
7. Validate and package one sample — `prepare_sample(line_no, raw_sample, mode, processor, target_sr, text_normalize_enabled, sample_rate_normalize_enabled)` in generation_utils.py:361 assigns `sample_id = f"{line_no:06d}"`, requires `text`, and requires paired audio+transcript per speaker for any non-`generation` mode; behavior past generation_utils.py:389 was truncated in the wiki chunk and is not claimed (02-top-level-files.md:64).
8. Load model and processor — `_load_model_and_processor(args, device)` in inference.py:785 selects bfloat16 on CUDA else float32, moves/evals the audio tokenizer, and tries `flash_attention_2` with `sdpa` fallback on CUDA (`sdpa` on CPU); interactive equivalent is `load_backend` in gradio_demo.py:512 with `lru_cache(maxsize=1)` (02-top-level-files.md:78, 02-top-level-files.md:116).
9. Run sharded generation — `_flush_batch` / `_worker_main` in inference.py:821 and inference.py:875 pin one CUDA device per rank, call `run_infer_batch(...)` with the resolved sampling args, retry failed samples individually, and write `output.jsonl` or per-rank `output_rank_{rank:06d}.jsonl` (02-top-level-files.md:80).
10. Merge outputs — `merge_rank_jsonl_files(...)` invoked from `main()` in inference.py:985, which also seeds `torch.manual_seed(42)`, spawns workers via `mp.spawn`, merges rank files, and deletes per-rank shards (02-top-level-files.md:96). Decode uses `processor.decode(outputs)` at `processor.model_config.sampling_rate`, writing `{sample_idx}_{seg_idx}.wav` under `output/` (01-overview.md:56).

## 6. Key Files

| File | Lines | What It Does |
|---|---|---|
| `inference.py` | 273, fully shown (02-top-level-files.md:65) | Multi-GPU batch driver: arg parsing, model load, sharded workers, retry, merge |
| `generation_utils.py` | 389+ shown, truncated at `if mode =` with 6160 further chars not shown (02-top-level-files.md:12) | Shared text normalization, JSONL I/O, path/sampling resolution, audio prep |
| `gradio_demo.py` | 812, shown to line 753 with 16613 further chars not shown (02-top-level-files.md:12) | Interactive 1–5 speaker demo with cached backend and preset voices |
| `requirements.txt` | 25, fully shown (02-top-level-files.md:121-130) | Exact runtime pins for torch, transformers, audio, and UI stack |
| `README.md` | chunks 1–241 captured (01-overview.md:69) | Overview, highlights, news, languages, install, continuation and batch usage |
| `README_zh.md` | 459, shown to README_zh.md:1388 with 8089 further chars not shown (02-top-level-files.md:120) | Chinese quick-start, batch flags, JSONL schema, SGLang fused-model path |
| `asset/reference_02_s1.wav` | binary preset (02-top-level-files.md:98-111) | Default speaker-1 reference voice for the demo |
| `asset/reference_02_s2.wav` | binary preset (02-top-level-files.md:98-111) | Default speaker-2 reference voice for the demo |
| `<model_path>/generation_config.json` | config sidecar (02-top-level-files.md:40-58) | Middle-priority sampling defaults between CLI flags and hardcoded fallbacks |
| `input.jsonl` (user-supplied) | variable | Batch rows with `base_path`, tagged `text`, per-speaker prompt audio/text |
| `output.jsonl` / `output_rank_*.jsonl` | generated (02-top-level-files.md:80, 02-top-level-files.md:96) | Per-sample results; rank shards merged then deleted |
| `output/*.wav` (`{sample_idx}_{seg_idx}.wav`) | generated (01-overview.md:56) | Decoded waveform segments at the model sample rate |
| `legacy/v0.7/README.md` | referenced (01-overview.md:26) | v0.7 end-to-end SGLang instructions |
| `scripts/fuse_moss_tts_delay_with_codec.py` | referenced (02-top-level-files.md:120) | Fuses TTSD plus codec into one SGLang-servable model |

## 7. Dependencies

Required first, with exact constraint strings from requirements.txt:1-25 (02-top-level-files.md:121-130):

| Package | Version constraint | Purpose |
|---|---|---|
| `torch` | `==2.9.1+cu128` | Model inference, CUDA device handling, wav tensor ops |
| `torchaudio` | `==2.9.1+cu128` | Audio resampling (`torchaudio.functional.resample`) |
| `transformers` | `==5.0.0` | `AutoProcessor` / `AutoModel` loading and `generate` |
| `safetensors` | `==0.6.2` | Checkpoint weight loading |
| `numpy` | `==2.1.0` | Array handling around audio processing |
| `orjson` | `==3.11.4` | Fast JSONL parse/serialize in batch path |
| `tqdm` | `==4.67.1` | Progress reporting during batch inference |
| `PyYAML` | `==6.0.3` | Config file parsing |
| `einops` | `==0.8.1` | Tensor rearrangement in model/audio code |
| `scipy` | `==1.16.2` | Signal-processing utilities |
| `librosa` | `==0.11.0` | Audio feature/loading utilities |
| `tiktoken` | `==0.12.0` | Text tokenization support |
| `soundfile` | `==0.13.1` | WAV read/write (`sf.read`, demo `_load_audio`) |
| `gradio` | `==6.5.1` | Interactive demo UI |
| `pybase64` | unpinned | Base64 payloads (SGLang WAV responses) |
| `requests` | unpinned | HTTP fetch (weights, API examples) |
| `psutil` | unpinned (build dep) | Process/system utilities |
| `packaging` | unpinned (build dep) | Version handling at install |
| `ninja` | unpinned (build dep) | Native-extension builds |
| `setuptools` | unpinned (build dep) | Packaging builds |
| `wheel` | unpinned (build dep) | Packaging builds |
| `flash_attn` | commented out in requirements.txt; installed separately via `pip install flash-attn` (01-overview.md:42-47, 02-top-level-files.md:121-130) | `flash_attention_2` kernel for CUDA inference |
| `conda` Python | `python=3.12` in install command; badges declare `Python-3.10+`, `PyTorch-2.0+` (01-overview.md:42-48) | Runtime environment |

## 8. CLI / Usage Surface

Entry points: `python inference.py` (batch multi-GPU driver), `gradio_demo.py` (interactive demo), and inline Python quick-start using `AutoProcessor` / `AutoModel` (01-overview.md:51-56, 02-top-level-files.md:5-7).

Batch command form (verbatim, truncated in source chunk after `--mode` value):

```bash
python inference.py \
  --model_path OpenMOSS-Team/MOSS-TTSD-v1.0 \
  --codec_model_path OpenMOSS-Team/MOSS-Audio-Tokenizer \
  --input_jsonl /path/to/input.jsonl \
  --save_dir outputs \
  --mode voice_clone_and_continuati
```

(01-overview.md:58-66). GPU control is automatic over all visible devices; limit with `export CUDA_VISIBLE_DEVICES=<device_ids>` (01-overview.md:67).

| Flag | Default | Meaning |
|---|---|---|
| `--model_path` | `OpenMOSS-Team/MOSS-TTSD-v1.0` (02-top-level-files.md:82-95) | TTSD checkpoint id or local path |
| `--codec_model_path` | `OpenMOSS-Team/MOSS-Audio-Tokenizer` (02-top-level-files.md:82-95) | Audio tokenizer checkpoint |
| `--input_jsonl` | required (02-top-level-files.md:82-95) | Tagged-dialogue batch input |
| `--save_dir` | required (02-top-level-files.md:82-95) | WAV + JSONL output directory |
| `--batch_size` | `1` (02-top-level-files.md:82-95) | Samples per generation batch |
| `--mode` | `generation` (choices `generation`, `continuation`, `voice_clone`, `voice_clone_and_continuation`) (02-top-level-files.md:82-95) | Conditioning regime; Chinese docs recommend `voice_clone_and_continuation` (02-top-level-files.md:120) |
| `--max_new_tokens` / `--temperature` / `--top_p` / `--top_k` / `--repetition_penalty` | `None` until `resolve_sampling_args` fills fallbacks 8192 / 1.1 / 0.9 / 50 / 1.1 (02-top-level-files.md:40-58) | Sampling controls; CLI beats config file beats fallback |
| `--text_normalize` | `False` (`store_true`) (02-top-level-files.md:82-95) | Enable `normalize_text` preprocessing |
| `--sample_rate_normalize` | `False` (`store_true`) (02-top-level-files.md:82-95) | Resample multi-speaker prompts to a common rate first |

| Env var | Required | Effect |
|---|---|---|
| `CUDA_VISIBLE_DEVICES` | No | Restricts which GPUs the auto-sharded batch run uses (01-overview.md:67) |

| Config | Location | Effect |
|---|---|---|
| `generation_config.json` | `<model_path>/generation_config.json` (02-top-level-files.md:40-58) | Middle-priority sampling defaults |
| JSONL record | per-line `base_path`, `text` with `[S1]`–`[S5]`, `prompt_audio_speakerN`, `prompt_text_speakerN` (02-top-level-files.md:120) | Per-sample script plus per-speaker references |
| Quick-start knobs | `attn_implementation = "flash_attention_2"` on CUDA else `"sdpa"`; `max_new_tokens=2000` in example; `torch_dtype` bf16/float32 by device (01-overview.md:52-56, 02-top-level-files.md:78) | Device/attention/dtype and generation length |

## 9. Extensibility Points

- New normalization rules: edit `normalize_text` in generation_utils.py:20 (and its duplicate in gradio_demo.py:545-750); rules are sequential regex/substitution passes, so append or reorder passes there (02-top-level-files.md:15-21, 02-top-level-files.md:118).
- New input schemas or sharding policy: extend `streaming_jsonl_reader` in generation_utils.py:87 and `_make_output_record` / `_resolve_path` in generation_utils.py:119-156 (02-top-level-files.md:23-38).
- New sampling controls or defaults: extend `resolve_sampling_args` fallback dict and `_load_generation_config` in generation_utils.py:187-225, and add the matching `--flag` in `_parse_args` in inference.py:941-982 (02-top-level-files.md:40-58, 02-top-level-files.md:82-95).
- New conditioning regimes: extend `prepare_sample` in generation_utils.py:361 and the mode branch past generation_utils.py:389, plus the `--mode` choices in inference.py:947 (02-top-level-files.md:64, 02-top-level-files.md:82-95).
- New speaker counts or demo behavior: change `MIN_SPEAKERS` / `MAX_SPEAKERS`, `update_speaker_panels`, `_validate_dialogue_text`, and preset table builders in gradio_demo.py:411-482 and gradio_demo.py:545-750 (02-top-level-files.md:98-118).
- New attention backends or device policy: extend `resolve_attn_implementation` in gradio_demo.py:485 and `_load_model_and_processor` in inference.py:785 / `load_backend` in gradio_demo.py:512 (02-top-level-files.md:78, 02-top-level-files.md:114-116).
- New serving path: follow the SGLang fuse-and-serve sequence via `scripts/fuse_moss_tts_delay_with_codec.py` referenced in README_zh.md:1307-1370 (02-top-level-files.md:120).

## 10. Limitations and Gotchas

- **Truncated sources bound what can be trusted.** `generation_utils.py` cuts off at `if mode =` (generation_utils.py:389), `gradio_demo.py` cuts off mid-function (gradio_demo.py:753), the batch `--mode` value is truncated as `voice_clone_and_continuati`, and `README_zh.md` cuts off at `http://loc` — behavior beyond those points is not claimed (01-overview.md:68, 02-top-level-files.md:12).
- **Normalization is off by default and lossy by design.** Both `--text_normalize` and `--sample_rate_normalize` default to `False`, so multi-speaker runs without them skip punctuation/laughter-tag canonicalization and common-rate resampling; when enabled, the normalizer rewrites punctuation and fillers irreversibly (e.g. interior `。` forced to `，`, `哈{2,}` to `[笑]`) (02-top-level-files.md:15-21, 02-top-level-files.md:82-95).
- **Strict speaker-tag and pairing contract.** Non-`generation` modes raise unless every speaker has both `prompt_audio_speakerN` and `prompt_text_speakerN`; demo validation additionally requires `[S1]`-style tags with `max_tag <= speaker_count`, and `_build_prefixed_text` silently prepends/merges tags, so malformed scripts either fail or get rewritten (02-top-level-files.md:62-64, 02-top-level-files.md:118).
- **Attention and dtype are device-fragile.** CUDA attempts `flash_attention_2` with `sdpa` fallback, CPU forces `sdpa`/`eager` with float32; the demo further requires `flash_attn` installed plus float16/bfloat16 plus compute capability ≥ 8 for the fast path, so missing kernels or wrong dtype silently downgrade performance characteristics (02-top-level-files.md:78, 02-top-level-files.md:114-116).
- **Batch sharding assumes homogeneous GPUs and discards shards.** World size equals `torch.cuda.device_count()`, rank files are merged then deleted, and bad JSONL lines are skipped with warnings under `skip_invalid_json=True` — interrupted runs lose per-rank evidence and heterogeneous devices get equal shares (02-top-level-files.md:80, 02-top-level-files.md:96).

## 11. How It Compares to Alternatives

The wiki pages name no competing system, so this section uses external project knowledge against the wiki-grounded feature set (multi-speaker script continuation, 60-minute sessions, zero-shot cloning, 20 languages).

- **Coqui XTTS v2** — open multilingual zero-shot cloning with strong single/clone fidelity, but no native 1–5-speaker script-to-conversation continuation or 60-minute single-session design; MOSS-TTSD targets the multi-party long-form session where XTTS targets utterance cloning.
- **Suno Bark / Bark-style semantic-codec TTS** — expressive multilingual generation with laughter/filler tokens comparable to MOSS-TTSD's `[笑]`/`[laugh]` normalization, but single-prompt utterance synthesis rather than reference-conditioned multi-persona dialogue with turn-taking.
- **Microsoft VALL-E / VALL-E X** — zero-shot continuation from 3-second prompts, the closest architectural cousin to MOSS-TTSD's continuation workflow, but monolingual-leaning short-utterance cloning rather than 5-speaker 60-minute conversation management.
- **Alibaba CosyVoice 2 / F5-TTS** — current open strong multilingual zero-shot baselines with natural prosody and cross-lingual cloning, but single- or dual-speaker oriented; MOSS-TTSD differentiates on explicit `[S1]`–`[S5]` script conditioning plus batch multi-GPU and SGLang fused serving for hour-scale output.

Positioning: MOSS-TTSD is the long-form dialogue specialist — it trades single-utterance leaderboard fidelity for script-level conversation coherence (persona-stable, turn-aware, hour-scale) with an open batch-plus-demo production surface.

## Appendix: Selected Code Snippets

1. Text normalization head (`generation_utils.py:20`, range 20–21):

```python
text = re.sub(r"\[(\d+)\]", r"[S\1]", text)
remove_chars = "【】《》（）『』「」" '"-_“”～~‘’'
segments = re.split(r"(?=\[S\d+\])", text.replace("\n", " "))
```

(02-top-level-files.md:15-21)

2. Sampling fallback defaults (`generation_utils.py:202`, range 202–208):

```python
fallback: Dict[str, Any] = {
    "max_new_tokens": 8192,
    "temperature": 1.1,
    "top_p": 0.9,
    "top_k": 50,
    "repetition_penalty": 1.1,
}
```

(02-top-level-files.md:40-48)

3. Shared-module imports for the batch driver (`inference.py:770`, range 770–775):

```python
from generation_utils import (
    merge_rank_jsonl_files,
    prepare_sample,
    resolve_sampling_args,
    run_infer_batch,
    streaming_jsonl_reader,
)
```

(02-top-level-files.md:65-75)

4. Demo backend constants (`gradio_demo.py:411-420`, range 411–420):

```python
torch.backends.cuda.enable_cudnn_sdp(False)
torch.backends.cuda.enable_flash_sdp(True)
torch.backends.cuda.enable_mem_efficient_sdp(True)
torch.backends.cuda.enable_math_sdp(True)
MODEL_PATH = "OpenMOSS-Team/MOSS-TTSD-v1.0"
CODEC_MODEL_PATH = "OpenMOSS-Team/MOSS-Audio-Tokenizer"
DEFAULT_MAX_NEW_TOKENS = 2000
MIN_SPEAKERS = 1
MAX_SPEAKERS = 5
PRESET_REF_AUDIO_S1 = "asset/reference_02_s1.wav"
PRESET_REF_AUDIO_S2 = "asset/reference_02_s2.wav"
```

(02-top-level-files.md:98-111)
