---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: index-tts/index-tts

### Q1. What is IndexTTS, and what does zero-shot voice cloning require from the user?

> [!tip]- Answer
> IndexTTS is positioned as an industrial-level controllable and efficient text-to-speech system that clones a voice from a single reference audio clip. The user supplies that one speaker prompt (e.g. `spk_audio_prompt='examples/voice_01.wav'`) plus text, and the latest IndexTTS-2.5 release adds multilingual and fine-grained controllable synthesis on top. See [[wiki/01-overview|Overview]].

### Q2. Which languages does IndexTTS-2.5 support, and what new controls did the 2026/08/10 release add?

> [!tip]- Answer
> IndexTTS-2.5 supports Chinese, English, Japanese, Spanish, and Arabic, with cross-lingual and timbre-emotion disentanglement. The release added improved Pinyin/CMU-phoneme/Kana pronunciation controllability, speaking-speed control via `duration_factor` (0.5x–2.0x duration), faster inference than IndexTTS-2, and vLLM production deployment. See [[wiki/01-overview|Overview]].

### Q3. What are the three daily-use paths for IndexTTS, and how is emotion steered in the Python API?

> [!tip]- Answer
> The three paths are the Gradio WebUI (`uv run webui.py`, browser at `http://127.0.0.1:7860`), production serving via the vLLM recipe, and the Python API (`indextts/infer_v2.py`, `indextts/infer_v2_5.py`). Emotion is steered with a separate emotional reference audio plus `emo_alpha` intensity (range `0.0-1.0`, default `1.0`), or with an 8-float emotion vector in the order `[happy, angry, sad, afraid, disgusted, melancholic, surprised, calm]`. See [[wiki/01-overview|Overview]].

### Q4. What does `webui.py` do at startup, and how does it select between model generations?

> [!tip]- Answer
> `webui.py` parses CLI flags, checks for and downloads missing model checkpoints via `snapshot_download`, then builds an `IndexTTS2` instance and serves the Gradio demo. It supports two generations via `--version {2, 2.5}` (default `2.5`) with per-version required-file lists and HuggingFace repos (`IndexTeam/IndexTTS-2` vs `IndexTeam/IndexTTS-2.5`) plus a `--model_dir` default of `./checkpoints`. See [[wiki/02-top-level-files|Top-level-files]].

### Q5. How does `webui.py` handle hardware acceleration and low-VRAM GPUs?

> [!tip]- Answer
> It exposes `--fp16`, `--deepspeed`, `--cuda_kernel`, `--accel`, `--torch_compile`, and `--qwen_emo` flags, failing fast when the `flash_attn` or `triton` extras are missing. Below the 10 GB VRAM threshold it enables half precision and skips QwenEmotion unless `--qwen_emo` forces it, using BF16 on v2.5 and FP16 on v2. See [[wiki/02-top-level-files|Top-level-files]].

### Q6. What environment, packaging, and legal guardrails sit at the repository root?

> [!tip]- Answer
> `.gitignore` excludes environments, bytecode, caches, checkpoints, outputs, and on-demand example audio; `.python-version` pins Python `3.11.13`; `MANIFEST.in` ships CUDA/C++ sources while excluding editor and bytecode files. The `DISCLAIMER` restricts use to research/learning/lawful creative work with a TTS-voice-misuse ban, and `LICENSE_ZH.txt` is the bilibili model-use license triggering commercial licensing above 100M MAU or 100M RMB revenue. See [[wiki/02-top-level-files|Top-level-files]].

### Q7. Should a small team with a single 8 GB GPU adopt IndexTTS-2.5 via the WebUI for multilingual voice-cloning experiments?

> [!tip]- Answer
> Yes for experiments, with caveats: the WebUI auto-adapts to sub-10 GB GPUs (half precision, QwenEmotion skipped) and 2.5 covers five languages with emotion, speed, and pronunciation controls, so a pilot is low-friction. Before any production or commercial step, verify synthesis quality and speed on your own voices and hardware, and clear the research-use disclaimer plus the bilibili license's commercial terms. See [[wiki/01-overview|Overview]].
