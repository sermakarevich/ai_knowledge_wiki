> [[index|Wiki]] | [[summary|Summary]]
# index-tts/index-tts — Digest

## 1. [[wiki/01-overview|Overview]]
**In one sentence:** IndexTTS is a zero-shot text-to-speech system that clones a voice from a single reference audio clip, with the latest IndexTTS-2.5 release adding multilingual and fine-grained controllable synthesis (README.md:24-28).
## Key points
- IndexTTS performs zero-shot voice cloning from a single reference audio clip, positioned as an industrial-level controllable and efficient TTS system (README.md:14-24).
- IndexTTS-2.5 supports Chinese, English, Japanese, Spanish and Arabic, with fine-grained emotion control, speaking-speed control, pronunciation control (Pinyin / CMU phonemes / Japanese Kana), and faster inference than IndexTTS-2 (README.md:25-28).
- The repo maintains four released model lines — IndexTTS, IndexTTS-1.5, IndexTTS-2, IndexTTS-2.5 — each with demos, papers, and ModelScope/HuggingFace distributions (README.md:32-39).
- IndexTTS-2.5 (2026/08/10) adds cross-lingual and timbre-emotion disentanglement, improved Pinyin/CMU/Kana controllability, `duration_factor` speed control (0.5x–2.0x duration), and vLLM production deployment (README.md:43-47).
- Installation is managed with `uv` (`uv sync --all-extras`), models are fetched via `huggingface-cli` / `modelscope` into `checkpoints` / `checkpoints_2`, and GPU setup is diagnosed with `tools/gpu_check.py` (README.md:85-95, README.md:129-151, README.md:170-172).
- Daily use has three paths: WebUI (`uv run webui.py`, browser at `http://127.0.0.1:7860`), production serving via the vLLM recipe, and Python API (`indextts/infer_v2.py`, `indextts/infer_v2_5.py`) with `spk_audio_prompt`, `emo_audio_prompt`, `emo_alpha`, and `lang` parameters (README.md:178-184, README.md:209-218, README.md:240-258).
- Emotion control supports a separate emotional reference audio plus `emo_alpha` intensity (range `0.0-1.0`, default `1.0`), or an 8-float emotion vector in the order `[happy, angry, sad, afraid, disgusted, melancholic, surprised, calm]` (README.md:272-291).

## 2. [[wiki/02-top-level-files|Top-level-files]]
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

## The system in five moves
1. IndexTTS clones a voice zero-shot from a single reference clip, evolving across four model lines into the multilingual, controllable IndexTTS-2.5.
2. Models are distributed via ModelScope/HuggingFace and installed with `uv`, with checkpoints resolved into `checkpoints` / `checkpoints_2`.
3. Users enter through three paths — Gradio WebUI, vLLM production serving, or the Python `infer_v2` / `infer_v2_5` API.
4. The WebUI entry point (`webui.py`) selects the model generation, validates acceleration extras, adapts precision for low-VRAM GPUs, and wires up emotion modes, demo cases, and presets.
5. Synthesis is steered by speaker prompt plus emotion reference (`emo_alpha`), emotion vector, pronunciation controls, and speed control, all bounded by research-use disclaimers and the bilibili model license.
