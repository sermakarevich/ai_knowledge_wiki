# Technical Analysis: index-tts/index-tts

**Repository:** https://github.com/index-tts/index-tts
**Version analyzed:** unknown
**Date:** 2026-09-22
**Wiki:** [[index]]

> Source scope: this summary is grounded only in two wiki pages covering `README.md` (model zoo, releases, install, usage) and root files plus the visible portion of `webui.py`. No `pyproject.toml` / `requirements` / `uv.lock` constraints, no `indextts/` internals, and no Gradio callbacks beyond the preset helpers are attested in the sources. Gaps are stated explicitly below.

## 1. Overview / What Problem It Solves

Problem space: zero-shot text-to-speech with voice cloning from a single reference clip, plus controllable prosody (emotion, speed, pronunciation) across languages without per-speaker training (01-overview.md:5).

How the repo addresses it: IndexTTS ships four model generations — IndexTTS, IndexTTS-1.5, IndexTTS-2, IndexTTS-2.5 — each distributed via ModelScope/HuggingFace with demos and papers (01-overview.md:7, 01-overview.md:14-21). The current line IndexTTS-2.5 synthesizes Chinese, English, Japanese, Spanish, and Arabic from one `spk_audio_prompt`, with a separate `emo_audio_prompt` plus `emo_alpha` intensity or an 8-float emotion vector, `duration_factor` speed control (0.5x–2.0x duration), Pinyin/CMU/Kana pronunciation control, and a vLLM production recipe (01-overview.md:6, 01-overview.md:8, 01-overview.md:10-11). Release history: 1.0 weights/inference code 2025/03/25, 1.5 stability/English 2025/05/14, 2.0 autoregressive duration/emotion control 2025/09/08, 2.5 multilingual/dis entanglement/speed/vLLM 2026/08/10 (01-overview.md:25-29).

Primary user: an application developer or operator who needs deployable multilingual voice cloning with reference-driven timbre/emotion control via WebUI, Python API, or vLLM serving (01-overview.md:10, 01-overview.md:91, 01-overview.md:104-122).

## 2. High-Level Architecture

```
                    ┌─ checkpoints/ (2.5) │ checkpoints_2/ (2) ─┐
                    │  gpt.pth, s2mel.pth, codec.pth (2.5),      │
                    │  bpe.model (2), wav2vec2bert_stats.pt,     │
                    │  config.yaml, *.tiktoken                   │
                    └───────────────────┬───────────────────────┘
                                        ▼
  examples/*.wav ─► webui.py ─► IndexTTS2 (infer_v2.py │ infer_v2_5.py)
  (spk prompt,         │  (argparse, checkpoint check,      │
   emo prompt,         │   low-VRAM adapt, build_tts)       │
   cases.jsonl)        │                                    │
                       │   ┌─ conditioning ─────────────────┘
                       │   │  spk_audio_prompt, emo_audio_prompt /
                       │   │  8-float vector / emo text, emo_alpha,
                       │   │  lang, duration_factor
                       │   ▼
                       │  GPT (autoregressive) ─► s2mel ─► codec/vocoder ─► wav
                       │                                    │
                       ▼                                    ▼
              outputs/tasks/                            gen.wav
              prompts/
```

Data-flow narrative (5 steps):

1. Install and fetch weights. `uv sync --all-extras` builds `.venv`; `huggingface-cli`/`modelscope` download `IndexTeam/IndexTTS-2.5` into `checkpoints/` and `IndexTTS-2` into `checkpoints_2/`; example audio resolves on demand; `tools/gpu_check.py` diagnoses CUDA (01-overview.md:9, 01-overview.md:40-45, 01-overview.md:55-71).
2. Resolve and construct runtime. `webui.py` parses `--version {2, 2.5}` / `--model_dir`, checks `REQUIRED_FILES` per version against `MODEL_REPO`, calls `snapshot_download` plus `ensure_config_available` on miss, selects `indextts.infer_v2_5.IndexTTS2` vs `indextts.infer_v2.IndexTTS2`, and applies the <10 GB low-VRAM policy (half precision on, QwenEmotion skipped unless `--qwen_emo`) via `build_tts` (02-top-level-files.md:5-8, 02-top-level-files.md:99-100).
3. Condition the request. Caller supplies text plus `spk_audio_prompt` for timbre and one of four emotion modes (same-as-timbre, emotion reference audio, emotion vector, emotion text); v2.5 adds `lang`; intensity uses `emo_alpha 0.0–1.0` (01-overview.md:10-11, 01-overview.md:115-138, 02-top-level-files.md:9, 02-top-level-files.md:103).
4. Synthesize. The GPT → s2mel → codec/vocoder chain (checkpoint names `gpt.pth`, `s2mel.pth`, `codec.pth`) renders audio with optional BF16/FP16, DeepSpeed, compiled CUDA kernels, `flash_attn` accel, or `triton` torch-compile paths (01-overview.md:84-90, 02-top-level-files.md:99).
5. Emit and persist. WebUI writes to `outputs/tasks/`; Python API writes the caller-chosen `output_path` (e.g. `gen.wav`); prompts persist under `prompts/` (01-overview.md:115-122, 02-top-level-files.md:9, 02-top-level-files.md:103).

Persistent state lives in `checkpoints/` and `checkpoints_2/` (weights + `config.yaml`), `cache/`, `outputs/` (incl. `outputs/tasks/`), `prompts/`, and on-demand `examples/*.wav`; `checkpoints*/*` and `outputs/` are git-ignored while `checkpoints*/*.yaml` is kept (02-top-level-files.md:10, 02-top-level-files.md:20-31, 02-top-level-files.md:103).

## 3. Zero-Shot Timbre–Emotion Conditioning

Representation: every synthesis request is a (text, speaker-reference, emotion-spec, language) tuple. Timbre comes from a single waveform path (`spk_audio_prompt`); emotion is either entangled (same-as-timbre), a second waveform (`emo_audio_prompt` scaled by `emo_alpha`), an 8-float vector in fixed order `[happy, angry, sad, afraid, disgusted, melancholic, surprised, calm]` with optional `use_random` stochasticity, or an emotion-text description (experimental, hidden unless QwenEmotion loads) (01-overview.md:10-11, 01-overview.md:124-138, 02-top-level-files.md:9, 02-top-level-files.md:103).

Named kinds/types with file:line:

- `spk_audio_prompt` — timbre reference path, e.g. `examples/voice_01.wav` (`indextts/infer_v2.py`, `indextts/infer_v2_5.py` usage in README.md:115-122).
- `emo_audio_prompt` — disjoint emotion reference path, e.g. `examples/emo_sad.wav` (README.md:124-131).
- `emo_alpha` — float `0.0–1.0`, default `1.0`, active only with `emo_audio_prompt` (README.md:133-136).
- 8-float emotion vector — `[happy, angry, sad, afraid, disgusted, melancholic, surprised, calm]` + `use_random` (README.md:138).
- `lang` — v2.5 language selector (`ZH`, `EN`, …) (README.md:120-122, README.md:130).
- `duration_factor` — 2.5 speaking-speed control, 0.5x–2.0x duration (README.md:25).
- Four UI emotion modes — same-as-timbre / reference-audio / vector / text (`webui.py:164-173`).
- Two model generations — `"2"` vs `"2.5"` with distinct checkpoint sets and `IndexTTS2` classes (`webui.py:54-67`, `webui.py:94-104`).

Key queries: cloning is a single `infer` call parameterized by the conditioning tuple, not a training or fine-tuning query (README.md:115-122):

```python
tts.infer(spk_audio_prompt='examples/voice_01.wav', text=text, lang="EN", output_path="gen.wav", verbose=True)
```

Emotion-intensity variant (README.md:133-136):

```python
tts.infer(spk_audio_prompt='examples/voice_07.wav', text=text, output_path="gen.wav", lang="ZH", emo_audio_prompt="examples/emo_sad.wav", emo_alpha=0.9, verbose=True)
```

## 4. LLM / External Service Integration

The repo calls no OpenAI-style text-LLM or paid TTS API in the attested sources. External integration is weight/example distribution plus optional local models and serving:

| Provider / component | Required vs optional | Env vars / config |
|---|---|---|
| HuggingFace Hub (`IndexTeam/IndexTTS-2.5`, `IndexTeam/IndexTTS-2`) via `huggingface-cli` / `snapshot_download` | Required (weights; small models auto-download on first run) | `HF_ENDPOINT="https://hf-mirror.com"` for slow HF access (01-overview.md:55-66, 02-top-level-files.md:99) |
| ModelScope (`IndexTeam/IndexTTS-2.5`, `IndexTeam/IndexTTS-2`) via `modelscope` CLI | Alternative to HuggingFace, required if HF unused | `--local_dir checkpoints` / `checkpoints_2` (01-overview.md:55-65) |
| Example-audio CDN (HuggingFace/ModelScope) via `indextts/utils/examples_downloader.py` | Required on first WebUI start (populates `examples/`) | Callable as `ensure_examples_available()` (01-overview.md:102, 02-top-level-files.md:11) |
| QwenEmotion (local emotion-from-text model) | Optional; auto-skipped on <10 GB VRAM unless `--qwen_emo` | `--qwen_emo` flag (`webui.py:64`, `webui.py:112-136`) |
| vLLM serving recipe | Optional production path for IndexTTS | Referenced only; no config attested (01-overview.md:91) |

No API keys are attested in the two source pages.

## 5. The Zero-Shot Inference Pipeline

Two intertwined workflows are attested: (A) WebUI startup/construction and (B) per-utterance inference. Every function below carries its attested `file:line`.

A. WebUI startup (`webui.py`):

1. Parse CLI with `argparse.ArgumentParser` — `webui.py:19-35` (`--verbose`, `--port`/`--host`, `--model_dir`, `--version {2,2.5}`, `--fp16`, `--deepspeed`, `--cuda_kernel`, `--accel`, `--torch_compile`, `--qwen_emo`, `--gui_seg_tokens`).
2. Validate optional extras with `_require_optional_extra(flag_name, module_name, install_cmd)` — `webui.py:39-52` (`--accel`→`flash_attn`, `--torch_compile`→`triton`).
3. Check `REQUIRED_FILES[version]` against `model_dir`, `snapshot_download` from `MODEL_REPO[version]`, then `ensure_config_available` — `webui.py:54-67`, `webui.py:68-92`; exit non-zero on failure.
4. Select class via `IS_V25 = cmd_args.version == "2.5"` (`indextts.infer_v2_5.IndexTTS2` vs `indextts.infer_v2.IndexTTS2`) — `webui.py:94-104`.
5. Adapt to VRAM with `detect_vram_gb()` vs `LOW_VRAM_THRESHOLD_GB = 10.0` — `webui.py:112-136` (half precision on, skip QwenEmotion unless forced).
6. Construct engine with `build_tts(use_accel, use_torch_compile)` — `webui.py:139-162` (forwards `model_dir`, `cfg_path`, `use_deepspeed`, `use_cuda_kernel`, `use_accel`, `use_torch_compile`, `use_qwen_emo`, plus `use_bf16` on 2.5 / `use_fp16` on 2).
7. Load UI data: `get_example_cases(include_experimental)` from `examples/cases.jsonl`, `format_glossary_markdown()`, `_build_preset_data` / `on_preset_save` — `webui.py:175-209`, `webui.py:211-216`, `webui.py:218-231`, `webui.py:238-323`. Gradio layout and inference callbacks past this point are not attested (cut at `has_presets =`).

B. Per-utterance inference (Python API, `README.md` usage):

1. Instantiate `IndexTTS2(cfg_path, model_dir, …)` — `indextts/infer_v2.py:108`, `indextts/infer_v2_5.py:111` (README.md:104-113).
2. Clone timbre: `tts.infer(spk_audio_prompt, text, output_path, …)` — v2 (README.md:119); v2.5 adds `lang` (README.md:121).
3. Add emotion reference: `tts.infer(…, emo_audio_prompt, …)` (README.md:128-131).
4. Scale intensity: `tts.infer(…, emo_audio_prompt, emo_alpha=0.9, …)` (README.md:135).
5. Or pass the 8-float vector with `use_random` instead of `emo_audio_prompt` (README.md:138; trailing sentence cut at `stoc`).

## 6. Key Files

Only files attested in the two wiki pages are listed; the wiki explicitly notes `webui.py` coverage ends mid-file (~line 323 of 1378) and the README chunk ends at `README.md:292`.

| File | Lines | What It Does |
|---|---|---|
| `webui.py` | 1378 (visible to ~323) | CLI, checkpoint resolution, `IndexTTS2` construction, Gradio demo, presets, `outputs/tasks` + `prompts` management (02-top-level-files.md:5-9, 02-top-level-files.md:47-103) |
| `README.md` | 292+ (cut at 292) | Model zoo, news/releases, install, WebUI/vLLM/Python API usage, emotion controls (01-overview.md:3-140) |
| `indextts/infer_v2_5.py` | unknown (usage only) | v2.5 `IndexTTS2` class; `infer(spk_audio_prompt, text, lang, emo_audio_prompt, emo_alpha, …)` (01-overview.md:93-136) |
| `indextts/infer_v2.py` | unknown (usage only) | v2 `IndexTTS2` class; benchmark loop noted against hardcoded `checkpoints/` (01-overview.md:93-119, 01-overview.md:102) |
| `indextts/utils/examples_downloader.py` | unknown | On-demand `examples/*.wav` fetch; `ensure_examples_available()` (01-overview.md:102, 02-top-level-files.md:11) |
| `tools/gpu_check.py` | unknown | GPU/CUDA diagnosis entry (`uv run tools/gpu_check.py`) (01-overview.md:68-71) |
| `examples/cases.jsonl` | unknown | Demo rows: prompt audio, emotion mode, text, emotion audio, `emo_weight`, `emo_text`, 8 vector floats, per-example `lang` (02-top-level-files.md:103) |
| `checkpoints/config.yaml` | unknown | v2.5 runtime config passed as `--cfg_path` / `cfg_path` (01-overview.md:93-113) |
| `checkpoints_2/config.yaml` | unknown | v2 runtime config (01-overview.md:104-108) |
| `.python-version` | 1 | Pins interpreter `3.11.13` (02-top-level-files.md:10, 02-top-level-files.md:32-35) |
| `.gitignore` | 39 | Excludes venvs, bytecode, `/cache/`, `/checkpoints*/*` (except `*.yaml`), `/outputs/`, on-demand wavs (02-top-level-files.md:10, 02-top-level-files.md:20-31) |
| `MANIFEST.in` | 3 | Ships `*.cu/*.cpp/*.h/*.hpp` in sdist; excludes editor/bytecode files (02-top-level-files.md:11, 02-top-level-files.md:36-41) |
| `.gitattributes` | 2 | Notes example audio is downloaded on demand (02-top-level-files.md:11, 02-top-level-files.md:15-19) |
| `DISCLAIMER` | 43 | Chinese misuse/liability disclaimer; research/lawful-creative use only (02-top-level-files.md:12, 02-top-level-files.md:44) |
| `LICENSE_ZH.txt` | 53 | Bilibili model-use license; commercial trigger >100M MAU or 100M RMB revenue; PRC/Shanghai arbitration (02-top-level-files.md:12, 02-top-level-files.md:45) |

## 7. Dependencies

No `pyproject.toml`, `requirements`, or lockfile constraint strings are attested in the two source pages. The table below records only packages/flags named in the wiki; Version constraint is `unknown` where the wiki gives none.

| Package | Version constraint | Purpose |
|---|---|---|
| Python | `3.11.13` (`.python-version:1`) | Pinned interpreter |
| `uv` | unknown | Required installer; `uv sync --all-extras`, `uv run`, `uv tool install` |
| `huggingface-hub` (`huggingface-cli` / `hf`) | unknown | Weight download (`hf download IndexTeam/IndexTTS-2.5 …`) |
| `modelscope` | unknown | Alternative weight download |
| Gradio (`webui.py` server) | unknown | Web demo on `127.0.0.1:7860` |
| `torch` + NVIDIA CUDA Toolkit | `>=12.8` implied (CUDA Toolkit 12.8 or newer on CUDA error) | GPU inference |
| `deepspeed` (`--extra deepspeed`) | unknown | Optional inference acceleration; effect hardware-dependent |
| `flash_attn` (`--extra accel`) | unknown | Optional GPT2 acceleration engine (`--accel`) |
| `triton` (`--extra torch_compile`) | unknown | Optional `torch.compile` optimization of s2mel |
| QwenEmotion | unknown | Optional emotion-from-text mode; skipped on low VRAM |
| vLLM | unknown | Optional production serving recipe |
| `bilibili indextts2` weights+code | license-gated (see `LICENSE_ZH.txt`) | Model-use terms, not a PyPI package |

Install extras attested: `--all-extras`, `--extra webui` (recommended), `--extra deepspeed`, plus manual `--extra accel` / `--extra torch_compile`; China mirrors via `--default-index` Aliyun/Tuna URLs (01-overview.md:40-53, 02-top-level-files.md:79).

## 8. CLI / Usage Surface

Entry points:

| Entry point | Command | Effect |
|---|---|---|
| WebUI 2.5 (default) | `uv run webui.py` | Serve Gradio demo at `http://127.0.0.1:7860` (01-overview.md:75-82) |
| WebUI 2 | `uv run webui.py --version 2 --model_dir ./checkpoints_2` | Serve v2 model generation (01-overview.md:75-82) |
| v2.5 CLI infer | `PYTHONPATH="$PYTHONPATH:." uv run indextts/infer_v2_5.py --cfg_path checkpoints/config.yaml --model_dir checkpoints --text "Hello world" --lang EN` | Single-utterance file inference (01-overview.md:93-101) |
| GPU diagnosis | `uv run tools/gpu_check.py` | Check GPU/CUDA setup (01-overview.md:68-71) |
| Weight fetch (HF) | `hf download IndexTeam/IndexTTS-2.5 --local-dir=checkpoints` / `…/IndexTTS-2 --local-dir=checkpoints_2` | Populate checkpoint dirs (01-overview.md:55-60) |
| Weight fetch (MS) | `modelscope download --model IndexTeam/IndexTTS-2.5 --local_dir checkpoints` (and `_2` analog) | Same via ModelScope (01-overview.md:61-65) |

`webui.py` flags (`webui.py:19-35`):

| Flag | Default | Meaning |
|---|---|---|
| `--verbose` | off | Verbose mode |
| `--port` / `--host` | `7860` / `0.0.0.0` | Bind address |
| `--model_dir` | `./checkpoints` | Checkpoint directory |
| `--version` | `2.5` (`{2, 2.5}`) | Model generation |
| `--fp16` | off | FP16 inference where available |
| `--deepspeed` / `--cuda_kernel` / `--accel` / `--torch_compile` | off | Optional acceleration paths |
| `--qwen_emo` | off | Force-load QwenEmotion on low-VRAM GPUs |
| `--gui_seg_tokens` | `120` | Max tokens per generation segment in GUI |

Env vars:

| Variable | Use |
|---|---|
| `HF_ENDPOINT="https://hf-mirror.com"` | Mirror for slow HuggingFace access (01-overview.md:66) |
| `PYTHONPATH="$PYTHONPATH:."` | Required prefix in the documented CLI-infer invocation (01-overview.md:93-101) |

Config: `checkpoints/config.yaml` (2.5) and `checkpoints_2/config.yaml` (2) passed as `--cfg_path`/`cfg_path`; per-version `REQUIRED_FILES` + `MODEL_REPO` listed in §5/Appendix; `examples/cases.jsonl` drives demo rows; advanced preset parameters include `do_sample`, `top_p`, `top_k`, `temperature`, `length_penalty`, `num_beams`, `repetition_penalty`, `max_mel_tokens`, `max_text_tokens_per_segment` (01-overview.md:93-113, 02-top-level-files.md:99-103).

## 9. Extensibility Points

- New model generation or checkpoint set: extend `REQUIRED_FILES` / `MODEL_REPO` dicts and the `IS_V25` class-selection branch in `webui.py:54-104`.
- New acceleration backend: add a CLI flag alongside `--accel`/`--torch_compile`, validate with `_require_optional_extra` (`webui.py:39-52`), and forward through `build_tts` (`webui.py:139-162`).
- New emotion control mode: extend the four-mode handling and `get_example_cases` filter (`webui.py:164-173`, `webui.py:211-216`), plus preset capture in `_build_preset_data` / `on_preset_save` (`webui.py:238-323`).
- New language or pronunciation rule (Pinyin/CMU/Kana): flows through the v2.5 `lang`-conditioned `infer` path in `indextts/infer_v2_5.py` (usage in README.md:120-131); tokenizer/data files of the form `multilingual_*_char_del.tiktoken` in `checkpoints/` are the extension surface (`webui.py:86-92`).
- Custom demo/preset behavior: edit `examples/cases.jsonl` schema handling (`webui.py:175-209`) and the advanced-sampling preset fields (`do_sample` … `max_text_tokens_per_segment`) (`webui.py:238-323`).
- Custom example-audio sourcing: modify `indextts/utils/examples_downloader.py` (`ensure_examples_available`) referenced by `.gitattributes:1-2`.

## 10. Limitations and Gotchas

- **Wiki coverage is truncated.** `webui.py` analysis stops mid-preset-code at `has_presets =` (~line 323 of 1378); Gradio layout and inference callbacks are unattested, and the README chunk cuts mid-sentence on `use_random` at `README.md:292` (01-overview.md:140, 02-top-level-files.md:105).
- **`indextts/infer_v2.py` uses a hardcoded `checkpoints/` benchmark loop**, not the `checkpoints_2` layout the WebUI uses for v2 — passing `--model_dir ./checkpoints_2` to the WebUI does not carry over to that script (01-overview.md:102).
- **Low-VRAM GPUs silently change behavior.** Below 10 GB, half precision is forced and QwenEmotion (emotion-from-text mode) is skipped unless `--qwen_emo` is passed; BF16/FP16 trades a small quality loss for speed/VRAM (01-overview.md:84-90, 02-top-level-files.md:100).
- **Acceleration flags are hardware-dependent.** DeepSpeed "may speed up or slow down"; `--accel` needs `flash_attn`, `--torch_compile` needs `triton`, installed via separate `uv sync --extra` invocations, and DeepSpeed on Windows may require dropping `--all-extras` (01-overview.md:47-53, 01-overview.md:84-90, 02-top-level-files.md:79).
- **Environment prerequisites bite.** CUDA errors require NVIDIA CUDA Toolkit 12.8+; `uv` invocation auto-activates the venv (do not pre-activate); small models auto-download on first run but the default `--prompt_wav` in `examples/` only exists after a WebUI start or an explicit `ensure_examples_available()` call (01-overview.md:53, 01-overview.md:66, 01-overview.md:84-102).
- **`emo_alpha` is inert without `emo_audio_prompt`.** Intensity scaling (default `1.0`, range `0.0–1.0`) applies only alongside an emotion reference; vector mode omits the reference audio instead (01-overview.md:133-138).

## 11. How It Compares to Alternatives

The two source pages name no competing TTS systems and provide no benchmark table, so no grounded comparison can be drawn from the wiki alone. This section is therefore intentionally non-comparative: within the attested facts, IndexTTS is positioned as a locally deployed, reference-driven zero-shot cloner (single `spk_audio_prompt`, optional `emo_audio_prompt`/vector, `lang`-conditioned v2.5, WebUI + Python + vLLM surfaces) distributed as versioned weights on HuggingFace/ModelScope rather than as a hosted API (01-overview.md:5-11, 01-overview.md:14-21). A comparison against named alternatives (e.g. other open voice-cloning toolkits) requires sources beyond the two wiki pages and is omitted rather than invented.

## Appendix: Selected Code Snippets

1. WebUI CLI surface (`webui.py:19-35`):

```python
parser = argparse.ArgumentParser(
    description="IndexTTS WebUI",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)
parser.add_argument("--verbose", action="store_true", default=False, help="Enable verbose mode")
parser.add_argument("--port", type=int, default=7860, help="Port to run the web UI on")
parser.add_argument("--host", type=str, default="0.0.0.0", help="Host to run the web UI on")
parser.add_argument("--model_dir", type=str, default="./checkpoints", help="Model checkpoints directory")
parser.add_argument("--version", type=str, default="2.5", choices=["2", "2.5"], help="Model version to use")
parser.add_argument("--fp16", action="store_true", default=False, help="Use FP16 for inference if available")
parser.add_argument("--deepspeed", action="store_true", default=False, help="Use DeepSpeed to accelerate if available")
parser.add_argument("--cuda_kernel", action="store_true", default=False, help="Use CUDA kernel for inference if available")
parser.add_argument("--accel", action="store_true", default=False, help="Use GPT2 acceleration engine if available")
parser.add_argument("--torch_compile", action="store_true", default=False, help="Use torch.compile to optimize s2mel if available")
parser.add_argument("--qwen_emo", action="store_true", default=False, help="Load QwenEmotion even on a low-VRAM GPU, where it is skipped by default")
parser.add_argument("--gui_seg_tokens", type=int, default=120, help="GUI: Max tokens per generation segment")
```

2. Per-version checkpoint requirements and repos (`webui.py:54-67`):

```python
REQUIRED_FILES = {
    "2": ["bpe.model", "gpt.pth", "s2mel.pth", "wav2vec2bert_stats.pt"],
    "2.5": [
        "gpt.pth",
        "s2mel.pth",
        "codec.pth",
        "multilingual_zh_ja_yue_char_del.tiktoken",
        "wav2vec2bert_stats.pt",
    ],
}
MODEL_REPO = {
    "2": "IndexTeam/IndexTTS-2",
    "2.5": "IndexTeam/IndexTTS-2.5",
}
```

3. Engine construction (`README.md:104-113`, init calls):

```python
# IndexTTS2
from indextts.infer_v2 import IndexTTS2
tts = IndexTTS2(cfg_path="checkpoints_2/config.yaml", model_dir="checkpoints_2", use_fp16=False, use_cuda_kernel=False, use_deepspeed=False)

# IndexTTS2.5
from indextts.infer_v2_5 import IndexTTS2
tts = IndexTTS2(cfg_path="checkpoints/config.yaml", model_dir="checkpoints", use_bf16=True)
```

4. Cloning + emotion-reference inference (`README.md:124-136`):

```python
text = "酒楼丧尽天良，开始借机竞拍房间，哎，一群蠢货。"
# IndexTTS2
tts.infer(spk_audio_prompt='examples/voice_07.wav', text=text, output_path="gen.wav", emo_audio_prompt="examples/emo_sad.wav", verbose=True)
# IndexTTS2.5
tts.infer(spk_audio_prompt='examples/voice_07.wav', text=text, lang="ZH", output_path="gen.wav", emo_audio_prompt="examples/emo_sad.wav", verbose=True)
```

```python
tts.infer(spk_audio_prompt='examples/voice_07.wav', text=text, output_path="gen.wav", lang="ZH", emo_audio_prompt="examples/emo_sad.wav", emo_alpha=0.9, verbose=True)
```
