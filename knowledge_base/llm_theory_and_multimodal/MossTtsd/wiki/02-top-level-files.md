> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Top-level-files
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
---
## generation_utils.py — normalization, JSONL I/O, sampling, audio prep
Text normalization (`normalize_text(text: str) -> str`, generation_utils.py:20):
```python
text = re.sub(r"\[(\d+)\]", r"[S\1]", text)
remove_chars = "【】《》（）『』「」" '"-_“”～~‘’'
segments = re.split(r"(?=\[S\d+\])", text.replace("\n", " "))
```
verbatim behavior (generation_utils.py:21-84): strips `remove_chars`, maps `哈{2,}` to `[笑]` and `ha( ha)+` to `[laugh]`, maps `——/……/.../⸺/―/—/…` to `，`, translates `；→，`, `;→,`, `：→，`, `:→,`, `、→，`, collapses repeated `[，。？！,.?!]` to one, forces interior `。` to `，` keeping only the terminal mark, merges consecutive same-speaker segments, and replaces `‘/’` with `'`.

Sharded reader (generation_utils.py:87):
```python
def streaming_jsonl_reader(
    jsonl_path: str,
    rank: int = 0,
    world_size: int = 1,
    skip_invalid_json: bool = False,
) -> Iterator[Tuple[int, Dict[str, Any]]]:
```
Raises when `world_size < 1` or `rank` is out of range, skips blank lines, keeps only lines where `(line_no - 1) % world_size == rank`, and either warns-skips or raises `ValueError` on bad JSON depending on `skip_invalid_json` (generation_utils.py:93-116).

Path handling (generation_utils.py:119-156):
```python
path_key_pattern = re.compile(r"^(output_audio|prompt_audio(?:_speaker\d+)?|.*_path)$")
```
`_to_abs_path_str` expands/resolves; `_abspath_record_paths` absolutizes matching keys; `_resolve_path(maybe_path, base_path)` joins relative paths onto `base_path`; `_make_output_record` pops `base_path`, sets `record["id"] = sample_id`, and resolves `prompt_audio(_speakerN)` paths.

Sampling resolution (generation_utils.py:202):
```python
fallback: Dict[str, Any] = {
    "max_new_tokens": 8192,
    "temperature": 1.1,
    "top_p": 0.9,
    "top_k": 50,
    "repetition_penalty": 1.1,
}
```
`_load_generation_config(model_path)` reads `<model_path>/generation_config.json` or returns `{}` with a warning on failure (generation_utils.py:187-199); `resolve_sampling_args` keeps non-`None` CLI values, casts `top_k`/`max_new_tokens` to `int` and the rest to `float` from that file, else applies the fallback (generation_utils.py:212-225).

| Parameter | Fallback | Source |
|---|---|---|
| `max_new_tokens` | `8192` | CLI > `generation_config.json` > fallback (generation_utils.py:203) |
| `temperature` | `1.1` | CLI > `generation_config.json` > fallback (generation_utils.py:204) |
| `top_p` | `0.9` | CLI > `generation_config.json` > fallback (generation_utils.py:205) |
| `top_k` | `50` | CLI > `generation_config.json` > fallback (generation_utils.py:206) |
| `repetition_penalty` | `1.1` | CLI > `generation_config.json` > fallback (generation_utils.py:207) |

Audio prep (generation_utils.py:228-267): `_load_mono_wav` reads with `sf.read(wav_path, dtype="float32", always_2d=True)`, transposes, and means multi-channel to mono; `_maybe_resample` uses `torchaudio.functional.resample`; `_preprocess_prompt_wavs(loaded_wavs, target_sr, sample_rate_normalize_enabled)` first resamples all prompts to their minimum rate when enabled, then to `target_sr`.

Multi-speaker assembly (generation_utils.py:270-331): `_collect_speaker_fields(sample, base_path)` matches `prompt_audio_speaker(\d+)` and `prompt_text_speaker(\d+)` and returns the intersection as sorted `speaker_ids`; `_build_prefixed_text(text, text_map, speaker_ids)` prepends missing `[SN]` tags and merges consecutive duplicates; `_encode_concat_prompt_audio` concatenates per-speaker wavs with `torch.cat(wav_list, dim=-1)` then `processor.encode_audios_from_wav([wav], sampling_rate=target_sr)[0]`; `_encode_references` encodes separately and returns `[encoded_map.get(speaker_id) for speaker_id in range(1, max_speaker_id + 1)]` (generation_utils.py:357).

`prepare_sample(line_no, raw_sample, mode, processor, target_sr, text_normalize_enabled, sample_rate_normalize_enabled)` (generation_utils.py:361): sets `sample_id = f"{line_no:06d}"`, raises `missing \`text\`` when absent, optionally normalizes text, and raises when `mode != "generation"` but no paired `prompt_audio_speakerN` + `prompt_text_speakerN` exists (generation_utils.py:371-387). Behavior past `if mode =` (generation_utils.py:389) was truncated in the chunk and is not claimed.
## inference.py — batch multi-GPU driver (273 lines, fully shown)
Imports from the shared module (inference.py:770):
```python
from generation_utils import (
    merge_rank_jsonl_files,
    prepare_sample,
    resolve_sampling_args,
    run_infer_batch,
    streaming_jsonl_reader,
)
```
Defaults (inference.py:781): `DEFAULT_MODEL_PATH = "OpenMOSS-Team/MOSS-TTSD-v1.0"`, `DEFAULT_CODEC_PATH = "OpenMOSS-Team/MOSS-Audio-Tokenizer"`.

Model loading (`_load_model_and_processor(args, device)`, inference.py:785): `dtype` is `bfloat16` on CUDA else `float32`; moves `processor.audio_tokenizer` to device and evals it; tries `flash_attention_2` on CUDA with `sdpa` fallback on exception, uses `sdpa` on CPU (inference.py:797-815).

Batching (inference.py:821, inference.py:875): `_flush_batch` calls `run_infer_batch(...)` with `max_new_tokens/temperature/top_p/top_k/repetition_penalty` and falls back to per-sample retries with `[WARN][rank N]` messages; `_worker_main` pins `torch.cuda.set_device(rank)`, derives `target_sr = int(processor.model_config.sampling_rate)`, writes `output.jsonl` (single GPU) or `output_rank_{rank:06d}.jsonl`, reads with `skip_invalid_json=True`, and skips bad lines with warnings.

CLI flags (`_parse_args`, inference.py:941-982):

| Flag | Default / choices |
|---|---|
| `--model_path` | `OpenMOSS-Team/MOSS-TTSD-v1.0` (inference.py:943) |
| `--save_dir` | required (inference.py:944) |
| `--input_jsonl` | required (inference.py:945) |
| `--batch_size` | `1` (inference.py:946) |
| `--mode` | `generation`, `continuation`, `voice_clone`, `voice_clone_and_continuation`; default `generation` (inference.py:947) |
| `--max_new_tokens/--temperature/--top_p/--top_k/--repetition_penalty` | `None` until `resolve_sampling_args` fills fallbacks (inference.py:958) |
| `--text_normalize` | `store_true`, default `False` (inference.py:963) |
| `--sample_rate_normalize` | `store_true`, default `False` (inference.py:969) |
| `--codec_model_path` | `OpenMOSS-Team/MOSS-Audio-Tokenizer` (inference.py:975) |

`main()` (inference.py:985): calls `resolve_sampling_args(args)`, seeds `torch.manual_seed(42)`, rejects `batch_size < 1`, resolves `save_dir`/`input_jsonl` to absolute paths, uses `torch.cuda.device_count()` as `world_size` (1 on CPU), single-worker fast path or `mp.spawn(_worker_main, ...)`, then `merge_rank_jsonl_files(...)` and deletes per-rank files (inference.py:987-1028).
## gradio_demo.py — interactive demo (812 lines, shown up to line 753)
Backend setup (gradio_demo.py:411-420):
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
Preset prompt texts are `[S1] In short, we embarked ...` and `[S2] NVIDIA reinvented computing ...`, plus a two-speaker `PRESET_DIALOGUE_TEXT` business/China/AI exchange (gradio_demo.py:425-445); one `PRESET_EXAMPLES` entry `"Quick Start | reference_02_s1/s2"` and `PRESET_DISPLAY_FIELDS` drive `_build_preset_table_rows()` (gradio_demo.py:446-482).

Attention selection (`resolve_attn_implementation(requested, device, dtype)`, gradio_demo.py:485): `"none"` returns `None`; non-empty/non-`"auto"` passes through; `auto` returns `"flash_attention_2"` when CUDA + `flash_attn` installed + `float16/bfloat16` + capability major ≥ 8, else `"sdpa"` on CUDA, else `"eager"` on CPU (gradio_demo.py:488-509).

`load_backend(model_path, codec_path, device_str, attn_implementation)` with `@functools.lru_cache(maxsize=1)` (gradio_demo.py:512): falls back to CPU when CUDA is unavailable, picks `bfloat16` on CUDA else `float32`, loads `AutoProcessor` with `trust_remote_code=True, codec_path=...`, moves/evals `audio_tokenizer`, loads `AutoModel` with the resolved `attn_implementation`, and returns `(model, processor, device, sample_rate)` where `sample_rate = int(getattr(processor.model_config, "sampling_rate", 24000))` (gradio_demo.py:513-542).

Audio/text helpers (gradio_demo.py:545-750): `_resample_wav` via `interpolate(..., mode="linear")`; `_load_audio` via `soundfile` mono with `FileNotFoundError`/empty errors; a `normalize_text` duplicate of the generation-utils logic; `_validate_dialogue_text` requiring `[S1]`-style tags and `max_tag <= speaker_count`; `update_speaker_panels` clamping to 1–5 and toggling `MAX_SPEAKERS` panels; `apply_preset_selection(evt: gr.SelectData)` filling speaker count, S1/S2 audio+prompt, and dialogue from the preset table; `_normalize_prompt_text` prepending `[SN]` and `_build_prefixed_text(dialogue_text, prompt_text_map, cloned_speakers)` merging consecutive speaker tags. Code from `_encode_reference_audio_codes(processo` (gradio_demo.py:753) onward was truncated and is not claimed.
## README_zh.md + requirements.txt — docs and pins
`README_zh.md` (459 lines, shown up to `http://loc`, README_zh.md:1388): frames MOSS-TTSD as script-to-conversation for 1–5 speakers and ~60-minute sessions with AI-podcast/commentary/audiobook/dubbing use cases (README_zh.md:1070-1081); installs via `conda create -n moss_ttsd python=3.12` plus `pip install -r requirements.txt` and `pip install flash-attn` (README_zh.md:1125); quick-start builds a `continuation` message with `encode_audios_from_wav`, concatenated prompt wav, `build_user_message`/`build_assistant_message`, and `model.generate(..., max_new_tokens=2000)` decoding to `output/*.wav` (README_zh.md:1135-1255); batch usage is `python inference.py --model_path ... --codec_model_path ... --input_jsonl ... --save_dir outputs --mode voice_clone_and_continuation --batch_size 1 --text_normalize` with a flag table recommending `voice_clone_and_continuation`, always-on `text_normalize`, and `sample_rate_normalize` for ≥2 speakers (README_zh.md:1262-1287); JSONL rows carry `base_path`, `text` with `[S1]`–`[S5]`, and `prompt_audio_speakerN/prompt_text_speakerN` (README_zh.md:1289-1305); SGLang path clones `OpenMOSS/sglang -b moss-ttsd-v1.0-with-cat`, fuses via `scripts/fuse_moss_tts_delay_with_codec.py`, and serves with `--delay-pattern --trust-remote-code` (README_zh.md:1307-1370). Remainder beyond README_zh.md:1388 was truncated.
`requirements.txt` (25 lines, fully shown, requirements.txt:1-25):
```python
torch==2.9.1+cu128
torchaudio==2.9.1+cu128
transformers==5.0.0
# ...
gradio==6.5.1
#flash_attn
```
Full verbatim pin list: `torch==2.9.1+cu128`, `torchaudio==2.9.1+cu128`, `transformers==5.0.0`, `safetensors==0.6.2`, `numpy==2.1.0`, `orjson==3.11.4`, `tqdm==4.67.1`, `PyYAML==6.0.3`, `einops==0.8.1`, `scipy==1.16.2`, `librosa==0.11.0`, `tiktoken==0.12.0`, `soundfile==0.13.1`, `gradio==6.5.1`, `pybase64`, `requests`, plus build deps `psutil`, `packaging`, `ninja`, `setuptools`, `wheel` (requirements.txt:1-25).
**Covers:** `generation_utils.py`, `gradio_demo.py`, `inference.py`, `README_zh.md`, `requirements.txt`
