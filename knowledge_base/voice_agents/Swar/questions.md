---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---
> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# Retrieval Practice: vivekananda-2201/Swar
### Q1. What is Swar and what three-model stack does it orchestrate?
> [!tip]- Answer
> Swar is a 100% offline, CPU-first, full-duplex conversational audio runtime, not a sequential record-transcribe-query-synthesize-play pipeline. It orchestrates Silero VAD (v5 ONNX) for speech detection, NVIDIA Parakeet TDT 0.6B for progressive STT, and Kokoro-82M for TTS. It accepts 16kHz 16-bit PCM mic input and outputs 24kHz PCM speaker audio. See [[wiki/01-overview|Overview]].
### Q2. How does Swar achieve natural turn-taking and barge-in without driver crashes?
> [!tip]- Answer
> Swar enforces turn-taking with a bounded ~21.3ms audio block cutoff (512-sample slices) that cancels TTS playback without crashing ALSA/PortAudio drivers. A speculative turn buffer preserves turn-boundary audio so the opening words of an interruption are never lost. A 3-mode CAM++ ONNX barge-in guard (~3ms CPU) rejects speaker echo so TTS audio re-entering the mic does not self-interrupt. See [[wiki/01-overview|Overview]].
### Q3. What do Swar's benchmark harness and empirical results report?
> [!tip]- Answer
> The harness lives in `examples/02_llm_voice_chat.py`, takes `--url`, `--model`, and `--expected-tok-s` flags, and logs per-turn metrics to `benchmarks/session_<timestamp>.jsonl` plus `benchmarks/latest_summary.json`. Key UX metrics are TTFA, LLM TTFT/TTFS, generation tok/s, Kokoro sentence-1 synthesis and RTF, and barge-in cutoff. Over 8 live CPU turns median TTFA was ~1,664ms, TTFT ~159ms, and Kokoro RTF ~3.34x. See [[wiki/01-overview|Overview]].
### Q4. What do `run.py` and `swar.py` each do at the repository root?
> [!tip]- Answer
> `run.py` is the CLI launcher running Silero VAD + Parakeet TDT STT + Kokoro TTS on CPU, with `--mode` limited to `chat` or `stt_only` and flags for silence, STT language, voice, speed, LLM endpoint, and `--wake`. It builds `VoicePipeline` with explicit overrides and keeps it alive via `pipeline.start()` plus a sleep loop with SIGINT handling. `swar.py` is a re-export facade exposing 29 names such as `VoicePipeline`, `PipelineConfig`, and `VoiceprintManager` with an explicit `__all__`. See [[wiki/02-top-level-files|top-level-files]].
### Q5. What sections and key values does the master `config.yaml` define?
> [!tip]- Answer
> `config.yaml` is the documented master config edited instead of Python code, with sections `general`, `vad`, `stt`, `tts`, `chunking`, and `wake_word`. Notable values include `device: "cpu"`, VAD threshold 0.6 with 256ms silence, STT model `nvidia/parakeet-tdt-0.6b-v3`, TTS voice `af_bella` at 24kHz, and progressive chunking stages `[2, 1]` then `[-1, 3]`. Wake-word defaults are disabled with per-trigger phrases such as "hey assistant" and "relic". See [[wiki/02-top-level-files|top-level-files]].
### Q6. What does `requirements.txt` pin and what does the `.gitignore` tail do?
> [!tip]- Answer
> `requirements.txt` pins the CPU audio/LLM stack including `torch`, `torchaudio`, `nano-parakeet`, `kokoro`, `sounddevice`, `soundfile`, `speech-to-speech`, `onnxruntime`, plus `openai`, `pyyaml`, and `huggingface-hub`. The `.gitignore` is a standard Python template plus a Swar-specific tail that ignores `benchmarks/*.jsonl` and `benchmarks/*.json` while keeping the `!benchmarks/.gitkeep` placeholder. This keeps generated session traces out of version control without losing the directory. See [[wiki/02-top-level-files|top-level-files]].
### Q7. Would you recommend Swar for an offline CPU-only voice assistant, and why?
> [!tip]- Answer
> Yes, when the priority is fully offline sub-second conversation on commodity CPUs: its full-duplex runtime with progressive STT, decoupled compute-ahead TTS, ~21.3ms barge-in cutoff, speculative turn buffering, and CAM++ echo guard directly target that gap, and the `run.py`/`config.yaml` wiring plus benchmark harness aid tuning. The main caveats are validating the reported TTFA/RTF medians on your own CPU and mic/speaker setup, and noting the config's visible truncation past the `wake_word.triggers` section. See [[wiki/01-overview|Overview]].
