> [[index|Wiki]] | [[summary|Summary]]
# vivekananda-2201/Swar — Digest
## 1. [[wiki/01-overview|Overview]]
**In one sentence:** Swar is a 100% offline, CPU-first, full-duplex conversational audio runtime orchestrating Silero VAD + Parakeet TDT STT + Kokoro TTS (README.md:9, README.md:21).
## Key points
- Swar is an open-source, low-latency conversational audio runtime designed for CPU-first execution while remaining GPU-compatible (README.md:21).
- It operates as an asynchronous full-duplex runtime, not a sequential record-transcribe-query-synthesize-play pipeline (README.md:23).
- It emits real-time interim progressive transcription while the user is still speaking (README.md:24).
- It provides bounded ~21.3ms audio block cutoff for turn-taking/cancellation without crashing ALSA/PortAudio drivers (README.md:25, README.md:104).
- It uses an asynchronous producer–consumer TTS engine where upcoming sentences synthesize in the background while earlier sentences play (README.md:26).
- It preserves turn-boundary audio via a speculative turn buffer so opening interruption words are never lost (README.md:27).
- It includes a stateful case-insensitive sentence-wide wake-word engine forwarding the complete original transcript (README.md:28), plus in-flight `<think>...</think>` suppression for reasoning models (README.md:29) and a 3-mode CAM++ ONNX (~3ms CPU) speaker echo defense / barge-in guard (README.md:30).
## 2. [[wiki/02-top-level-files|top-level-files]]
**In one sentence:** The repository root wires the voice pipeline together via a runnable CLI (`run.py`), a public re-export facade (`swar.py`), a master YAML config (`config.yaml`), pinned Python dependencies (`requirements.txt`), and ignore rules (`.gitignore`).
## Key points
- `run.py` is the CLI launcher for Silero VAD + Parakeet TDT STT + Kokoro TTS on CPU, with `--mode` limited to `chat` or `stt_only` (`run.py:1`, `run.py:25`).
- `run.py` loads `PipelineConfig.load_default_or_file(args.config)` (default `config.yaml`) and forces `config.wake_word.enabled = True` when `--wake` is passed (`run.py:41`, `run.py:42`).
- `run.py` constructs `VoicePipeline` with explicit overrides for VAD threshold (`0.5`), silence, STT language, live transcription, TTS voice/speed, `device="cpu"`, wake mode, and partial/final callbacks (`run.py:71`).
- `swar.py` provides top-level imports (`from swar import VoicePipeline, PipelineConfig, VoiceprintManager`) by re-exporting 29 names from `voice_pipeline` with an explicit `__all__` list (`swar.py:1`, `swar.py:9`, `swar.py:40`).
- `config.yaml` is the documented master config with sections `general`, `vad`, `stt`, `tts`, `chunking`, and `wake_word`, edited instead of Python code (`config.yaml:1`, `config.yaml:9`, `config.yaml:37`, `config.yaml:61`, `config.yaml:74`, `config.yaml:101`, `config.yaml:130`).
- `requirements.txt` pins the CPU audio/LLM stack including `torch`, `torchaudio`, `nano-parakeet`, `kokoro`, `sounddevice`, `soundfile`, `speech-to-speech`, and `onnxruntime` (`requirements.txt:1`, `requirements.txt:3`, `requirements.txt:4`, `requirements.txt:11`).
- `.gitignore` is a standard Python ignore file plus a Swar-specific exception that ignores benchmark outputs but keeps the placeholder (`benchmarks/*.jsonl`, `benchmarks/*.json`, `!benchmarks/.gitkeep`) (`.gitignore:221`).
- `config.yaml` was truncated in the source chunk (1007 lines total, cut after the `wake_word.triggers` coding section around `migrate`), so trigger entries and any sections after that point are not covered here (`config.yaml:474`).
## The system in five moves
1. Swar frames voice interaction as an asynchronous full-duplex runtime rather than a sequential record-transcribe-query-synthesize-play pipeline.
2. Microphone input flows through Silero VAD speech/silence detection into Parakeet TDT progressive STT with interim hypotheses while the user speaks.
3. Final transcripts pass through a stateful wake-word engine and optional think-block filtering before reaching any local or API LLM brain.
4. LLM token streams are chunked into sentences and fed to a decoupled Kokoro TTS engine that synthesizes ahead while earlier sentences play.
5. Turn-taking is enforced by ~21.3ms barge-in cutoff, speculative turn buffering, and a CAM++ speaker echo guard, all wired via the `run.py` CLI, `swar.py` facade, and master `config.yaml`.
