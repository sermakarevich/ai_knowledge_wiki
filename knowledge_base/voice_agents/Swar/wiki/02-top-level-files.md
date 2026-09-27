> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# top-level-files
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
---
## .gitignore
Standard Python-template ignore rules covering bytecode (`__pycache__/`, `*.py[codz]`), packaging (`build/`, `dist/`, `*.egg-info/`), test/coverage (`.coverage`, `htmlcov/`, `.pytest_cache/`), environments (`.env`, `.venv`, `venv/`), caches (`.mypy_cache/`, `.ruff_cache/`), and IDE files (`.spyderproject`, `.ropeproject`) (`.gitignore:1`, `.gitignore:17`, `.gitignore:47`, `.gitignore:158`, `.gitignore:178`, `.gitignore:214`).

Swar-specific tail, verbatim (`.gitignore:221`):
```
benchmarks/*.jsonl
benchmarks/*.json
!benchmarks/.gitkeep
```

## config.yaml
Master voice-pipeline configuration; header states "Edit this file to safely adjust any setting without modifying Python code" (`config.yaml:1`).

| Section | Selected keys (exact names) | Values shown |
|---|---|---|
| `general` (`config.yaml:9`) | `device`, `cpu_threads`, `verbose`, `allow_barge_in`, `input_device`, `output_device` | `"cpu"`, `4`, `false`, `true`, `null`, `null` (`config.yaml:11`, `config.yaml:16`, `config.yaml:21`, `config.yaml:28`, `config.yaml:31`) |
| `vad` (`config.yaml:37`) | `threshold`, `min_silence_ms`, `min_speech_ms`, `min_speech_continuation_ms`, `speech_pad_ms`, `progressive_interval` | `0.6`, `256`, `384`, `192`, `500`, `0.5` (`config.yaml:39`, `config.yaml:43`, `config.yaml:46`, `config.yaml:49`, `config.yaml:53`, `config.yaml:56`) |
| `stt` (`config.yaml:61`) | `model_name`, `language`, `enable_live_transcription` | `"nvidia/parakeet-tdt-0.6b-v3"`, `"en"`, `true` (`config.yaml:63`, `config.yaml:66`, `config.yaml:69`) |
| `tts` (`config.yaml:74`) | `voice`, `speed`, `lang_code`, `sample_rate`, `max_text_queue_size`, `max_audio_queue_size` | `"af_bella"`, `1.18`, `"a"`, `24000`, `100`, `50` (`config.yaml:80`, `config.yaml:83`, `config.yaml:86`, `config.yaml:89`, `config.yaml:93`, `config.yaml:96`) |
| `chunking` (`config.yaml:101`) | `strategy`, `progressive_stages`, `target_buffer_seconds`, `low_buffer_seconds`, `medium_buffer_seconds`, `low/medium/high_buffer_sentences`, `min_words_for_boundary` | `"progressive"`, `[2, 1]` then `[-1, 3]`, `5.0`/`1.5`/`3.5`, `1`/`2`/`3`, `2` (`config.yaml:106`, `config.yaml:112`, `config.yaml:117`, `config.yaml:125`) |
| `wake_word` (`config.yaml:130`) | `enabled`, `default_timeout`, `strip_wake_phrase`, `prefix_only`, `triggers[].phrase`, `triggers[].timeout` | `false`, `15.0`, `false`, `false`, e.g. `"hey assistant"`/`20.0`, `"relic"`/`25.0`, `"take a note"`/`30.0` (`config.yaml:135`, `config.yaml:138`, `config.yaml:142`, `config.yaml:146`, `config.yaml:152`, `config.yaml:155`) |

Verbatim excerpts (`config.yaml:112`, `config.yaml:152`):
```
progressive_stages:
  - [2, 1]
  - [-1, 3]
```
```
triggers:
  - phrase: "hey assistant"
    timeout: 20.0
  - phrase: "relic"
    timeout: 25.0
```

Truncation note: the chunk contains only the first ~474 lines of the 1007-line `config.yaml`; the visible `wake_word.triggers` list runs through explanation, search, analysis, and coding phrases and is cut mid-list at `- phrase: "migrate"` with `timeout: 40.` plus 10357 unshown characters, so remaining triggers and any later sections are not covered (`config.yaml:474`).

## requirements.txt
Pinned runtime dependencies, verbatim (`requirements.txt:1`):
```
torch>=2.4.0
torchaudio>=2.4.0
nano-parakeet>=0.2.1
kokoro>=0.9.4
sounddevice>=0.5.0
soundfile>=0.12.0
numpy>=1.26.0
rich>=13.0
openai>=1.0.0
requests>=2.28.0
speech-to-speech>=0.2.12
onnxruntime>=1.18.0
pyyaml>=6.0
huggingface-hub>=0.20.0
```

## run.py
Docstring declares "Main CLI Launcher for Voice Pipeline. Runs Silero VAD + Parakeet TDT STT + Kokoro TTS natively on CPU" (`run.py:2`). Imports are `argparse`, `signal`, `sys`, `time`, `rich.console.Console`, `PipelineConfig`, and `VoicePipeline`, with `LLMClient` imported lazily from `examples.llm_client` only in `chat` mode (`run.py:11`, `run.py:17`, `run.py:48`).

| Flag | Type / action | Default |
|---|---|---|
| `--mode` (`run.py:25`) | `choices=["chat", "stt_only"]` | `"chat"` |
| `--min_silence_ms` (`run.py:26`) | `int` | `800` |
| `--stt_language` (`run.py:27`) | `str` | `"en"` |
| `--kokoro_voice` (`run.py:28`) | `str` | `"af_bella"` |
| `--tts_speed` (`run.py:29`) | `float` | `1.0` |
| `--llm_url` (`run.py:30`) | `str` | `"http://127.0.0.1:8080/v1"` |
| `--llm_api_key` (`run.py:31`) | `str` | `"empty"` |
| `--llm_model` (`run.py:32`) | `str` | `"default"` |
| `--enable_live_transcription` (`run.py:33`) | `store_true`, default `True` | `True` |
| `--enable_thinking` (`run.py:34`) | `store_true` | disabled |
| `--config` (`run.py:35`) | `str` | `"config.yaml"` |
| `--wake` (`run.py:36`) | `store_true` | off |

Runtime flow: `on_partial` writes `\r\033[K[Realtime]: {delta}` to stdout; `on_final` clears the line, prints `User: {transcript}`, streams `llm.stream_response(transcript)`, checks `pipeline.is_interrupted`, prints each `Assistant:` sentence, and calls `pipeline.speak_text(sentence)` (`run.py:55`, `run.py:59`). `VoicePipeline` is then started with `pipeline.start()` and kept alive by `while True: time.sleep(0.5)` with `SIGINT`/`KeyboardInterrupt` handlers calling `pipeline.stop()` (`run.py:71`, `run.py:85`, `run.py:95`).

## swar.py
Module docstring: "Swar (स्वर) — Local Conversational Audio Runtime. 100% Offline, CPU-First Conversational Audio Orchestration Layer" with usage `from swar import VoicePipeline, PipelineConfig, VoiceprintManager` (`swar.py:1`). Single re-export statement `from voice_pipeline import (...)` covering `SileroVAD`, `VADChunk`, `ParakeetSTT`, `SmartProgressiveStreaming`, `PartialTranscription`, `KokoroTTS`, `TTSPipeline`, `AudioItem`, `IncrementalSpeakOutParser`, `RobustSentenceChunker`, `ChunkingConfig`, `TextSegment`, `VoicePipeline`, `PipelineConfig`, `GeneralConfig`, `VADConfig`, `STTConfig`, `TTSConfig`, `WakeWordConfig`, `WakeTriggerConfig`, `WakeWordEngine`, `WakeState`, `BenchmarkLogger`, `BargeInGuardConfig`, `PipeWireAECConfig`, `VoiceprintManager`, `SpeakerEmbeddingExtractor`, `PipeWireAECManager` (`swar.py:9`).

`__all__` lists the same 28 re-exported names (pipeline/config classes, VAD/STT/TTS/chunking types, wake-word engine, `BenchmarkLogger`, voiceprint/AEC helpers) (`swar.py:40`).

**Covers:** `.gitignore`, `config.yaml` (visible prefix only; file truncated in chunk), `requirements.txt`, `run.py`, `swar.py`
