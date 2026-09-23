> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Top-level-files
**In one sentence:** The repository root combines the Gradio WebUI entry point (`webui.py`) with environment, packaging, and legal guardrails (`.gitignore`, `.python-version`, `MANIFEST.in`, `.gitattributes`, `DISCLAIMER`, `LICENSE_ZH.txt`).
## Key points
- `webui.py` is the launchable WebUI entry point: it parses CLI flags, checks/downloads model checkpoints, builds an `IndexTTS2` instance, and serves the Gradio demo (webui.py:19-35, webui.py:68-92, webui.py:139-162).
- `webui.py` supports two model generations via `--version {2, 2.5}` (default `2.5`) with per-version checkpoint lists and HuggingFace repos, plus a `--model_dir` default of `./checkpoints` (webui.py:27-35, webui.py:54-67).
- `webui.py` exposes hardware/acceleration flags (`--fp16`, `--deepspeed`, `--cuda_kernel`, `--accel`, `--torch_compile`, `--qwen_emo`) and validates optional extras (`flash_attn`, `triton`) at startup (webui.py:28-35, webui.py:39-52).
- `webui.py` adapts to low-VRAM GPUs: under 10 GB it enables half precision and skips QwenEmotion unless `--qwen_emo` forces it, using BF16 on v2.5 and FP16 on v2 (webui.py:112-136, webui.py:139-159).
- `webui.py` loads demo cases from `examples/cases.jsonl`, supports four emotion-control modes (same-as-timbre, emotion reference audio, emotion vector, emotion text), and manages UI presets plus output/prompt directories (webui.py:164-216, webui.py:238-323).
- `.gitignore` excludes environments, bytecode, build artifacts, caches/checkpoints/outputs, and on-demand example audio; `.python-version` pins Python `3.11.13` (`.gitignore:1-50`, `.python-version:1`).
- `MANIFEST.in` ships CUDA/C++ sources for packaging while excluding editor and bytecode files; `.gitattributes` only notes that example audio is downloaded on demand via `indextts/utils/examples_downloader.py` (MANIFEST.in:1-3, `.gitattributes:1-2`).
- `DISCLAIMER` (Chinese TTS-voice-misuse disclaimer) and `LICENSE_ZH.txt` (bilibili model-use license for `bilibili indextts2`) set usage, commercial-licensing, and liability terms (DISCLAIMER:1-43, LICENSE_ZH.txt:1-53).
---
## Repo metadata and environment
`.gitattributes` is two comment lines pointing at the on-demand example-audio downloader (`.gitattributes:1-2`):
```
# Example audio files are now downloaded on demand from HuggingFace/ModelScope.
# See indextts/utils/examples_downloader.py
```
`.gitignore` (39 lines) covers dev tools (`.mypy_cache/`, `.ruff_cache/`, `__pycache__/`, `.idea/`, `.vscode/`), environments (`.venv*/`, `venv*/`, `conda_env*/`), bytecode (`*.py[cod]`), packaging (`/build/`, `/dist/`, `*.egg-info/`), OS junk, plus IndexTTS outputs and on-demand audio (`.gitignore:1-50`):
```
# IndexTTS.
/cache/
/checkpoints*/*
!/checkpoints*/*.yaml
/outputs/

# Example audio files (downloaded on demand, not stored in git)
/examples/*.wav
/tests/sample_prompt.wav
```
`.python-version` pins the interpreter (`.python-version:1`):
```
3.11.13
```
`MANIFEST.in` controls sdist contents (MANIFEST.in:1-3):
```
global-exclude *~ *.py[cod]
include *.cu *.cpp
include *.h *.hpp
```

## Legal files
`DISCLAIMER` (43 lines, Chinese) restricts use to research/learning/lawful creative work, bans impersonation, fraud, defamation, IP/privacy infringement, unauthorized commercial use, misuse involving minors, and deepfake-law violations, and disclaims developer liability (DISCLAIMER:1-43). Last-updated `2025.3.17`, developer `Bilibili Index Team` (DISCLAIMER:106-107).
`LICENSE_ZH.txt` (53 lines) is the bilibili model-use license for `bilibili indextts2` (weights plus released code): worldwide, non-exclusive, non-transferable, free use, with a commercial-license trigger above 100M monthly active users or 100M RMB annual revenue, as-is disclaimer, downstream-user constraints, no use of the model to improve other AI models (except non-commercial ones), PRC governing law with Shanghai Arbitration Commission arbitration (LICENSE_ZH.txt:121-128, LICENSE_ZH.txt:131-163).

## `webui.py`: CLI and startup
Argument parser (webui.py:19-35):
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

| Flag | Meaning (webui.py:23-35) |
|---|---|
| `--verbose` | Enable verbose mode |
| `--port` (default `7860`) / `--host` (default `0.0.0.0`) | WebUI bind address |
| `--model_dir` (default `./checkpoints`) | Model checkpoints directory |
| `--version {2, 2.5}` (default `2.5`) | Model generation to run |
| `--fp16` | FP16 inference where available |
| `--deepspeed` / `--cuda_kernel` / `--accel` / `--torch_compile` | Optional acceleration paths |
| `--qwen_emo` | Force-load QwenEmotion on low-VRAM GPUs |
| `--gui_seg_tokens` (default `120`) | Max tokens per generation segment in the GUI |

Optional extras fail fast via `_require_optional_extra(flag_name, module_name, install_cmd)`: `--accel` requires `flash_attn` (`uv sync --extra accel`), `--torch_compile` requires `triton` (`uv sync --extra torch_compile`) (webui.py:39-52).

## `webui.py`: model resolution and TTS construction
Per-version checkpoint requirements and download repos (webui.py:54-67):
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
Missing files trigger `snapshot_download` into `model_dir`, then `ensure_config_available(model_dir, version=...)`; either failure exits non-zero (webui.py:68-92). `IS_V25 = cmd_args.version == "2.5"` selects `indextts.infer_v2_5.IndexTTS2` versus `indextts.infer_v2.IndexTTS2` (webui.py:94-104).
Low-VRAM behavior: `LOW_VRAM_THRESHOLD_GB = 10.0`; `detect_vram_gb()` reads CUDA device 0; below threshold the UI enables half precision and skips QwenEmotion unless forced (webui.py:112-136). `build_tts(use_accel, use_torch_compile)` forwards `model_dir`, `cfg_path`, `use_deepspeed`, `use_cuda_kernel`, `use_accel`, `use_torch_compile`, `use_qwen_emo`, plus `use_bf16` on v2.5 (with fallback message when BF16 is unsupported) or `use_fp16` on v2 (webui.py:139-162).

## `webui.py`: UI data (visible portion)
Supported UI languages are `{"中文": "zh_CN", "English": "en_US"}`; four emotion modes span same-as-timbre, emotion reference audio, emotion vector, and emotion text description, with the official build hiding the last experimental mode when QwenEmotion is not loaded (webui.py:164-173). The script creates `outputs/tasks` and `prompts`, then builds `example_cases` rows from `examples/cases.jsonl` (prompt audio, emotion mode, text, emotion audio, `emo_weight`, `emo_text`, eight emotion-vector floats, plus per-example `lang` on v2.5) (webui.py:175-209). `get_example_cases(include_experimental)` filters out emotion-from-text mode unless experimental features are enabled and loaded (webui.py:211-216). `format_glossary_markdown()` renders the v2 term glossary as a Markdown table, else a no-terms placeholder (webui.py:218-231). Preset helpers (`_build_preset_data`, `on_preset_save`) collect emotion settings and advanced sampling parameters (`do_sample`, `top_p`, `top_k`, `temperature`, `length_penalty`, `num_beams`, `repetition_penalty`, `max_mel_tokens`, `max_text_tokens_per_segment`) for named-preset storage (webui.py:238-323).

Truncation note: the source chunk cuts `webui.py` mid-preset-code at `has_presets =` (chunk line 500 of 502, file advertised as 1378 lines with ~40388 further characters); no claims are made about the Gradio layout, inference callbacks, or anything beyond the cut.

**Covers:** `.gitattributes`, `.gitignore`, `.python-version`, `DISCLAIMER`, `LICENSE_ZH.txt`, `MANIFEST.in`, `webui.py` (visible portion only, see truncation note)
