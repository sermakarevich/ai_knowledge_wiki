# Technical Analysis: vivekananda-2201/Swar

**Repository:** https://github.com/vivekananda-2201/Swar
**Version analyzed:** unknown
**Date:** 2026-09-22
**Wiki:** [[index]]

## 1. Overview / What Problem It Solves

Swar addresses the problem of running a responsive full-duplex voice assistant on commodity multi-core CPUs without cloud APIs, dedicated GPUs, or fidelity loss (`01-overview.md:33-34`). The problem space is conversational scheduling, not model quality: sequential record → transcribe → query → synthesize → play pipelines (`01-overview.md:19-21`) block on each stage, clip interruption words, self-interrupt on speaker echo, and speak reasoning-model internals aloud.

Swar answers this with an asynchronous conversational runtime that streams interim transcription while the user speaks (`01-overview.md:25`), cuts barge-in audio at ~21.3ms block boundaries without ALSA/PortAudio driver faults (`01-overview.md:26`), synthesizes sentence N+1 in the background while sentence N plays (`01-overview.md:27`), retains turn-boundary audio in a speculative buffer (`01-overview.md:28`), gates turns through a stateful case-insensitive sentence-wide wake-word engine (`01-overview.md:29`), strips `<think>...</think>` blocks from reasoning-model streams in flight (`01-overview.md:30`), and verifies barge-in speech with a 3-mode CAM++ ONNX voiceprint guard at ~3ms CPU latency (`01-overview.md:31`). The primary user is a developer deploying a local, offline voice-chat loop on a laptop or CPU server, tuning behavior through `config.yaml` rather than Python code (`02-top-level-files.md:25`).

## 2. High-Level Architecture

```
Microphone 16kHz PCM
  │ Silero VAD v5 ONNX (speech start / silence)
  ▼
Parakeet TDT 0.6B progressive STT (500ms interim deltas)
  │ final transcript
  ▼
Stateful Wake Engine (STANDBY vs ACTIVE)
  │ verified query / complete original transcript
  ▼
LLM / Agent Brain (local Ollama/vLLM/API) ─ token stream, sentence chunking
  │ sentences
  ▼
Decoupled Kokoro TTS ┌─ Generation Worker (computes ahead, queued)
                      └─ Playback Worker (streams to speaker) ► 24kHz PCM
```

Sources: pipeline stages `01-overview.md:40-50`; input/output sample rates `01-overview.md:52`; interim cadence and decoupled TTS `01-overview.md:61-62`.

Data flow in 5 steps:

1. **Capture and segment.** 16-bit 16kHz microphone PCM feeds Silero VAD v5 ONNX, which emits speech-start and silence events that delimit turns (`01-overview.md:40-42`).
2. **Transcribe progressively.** Parakeet TDT 0.6B produces interim hypothesis deltas every 500ms during speech and a final transcript at silence (`01-overview.md:42-44`, `01-overview.md:61`); barge-in slices audio at 512-sample (~21.3ms) windows (`01-overview.md:63`).
3. **Gate and route.** The wake-word engine matches multi-phrase case-insensitive triggers sentence-wide in STANDBY mode and forwards the complete original transcript once ACTIVE (`01-overview.md:44-46`, `01-overview.md:65`); `<think>` blocks are suppressed from reasoning-model token streams before they reach TTS (`01-overview.md:66`).
4. **Reason and chunk.** Any LLM/agent brain returns a token stream that is chunked into sentences in real time (`01-overview.md:46-48`); benchmarked reference is Qwen3.5-4B at ~40–50 tok/s on CPU (`01-overview.md:84`, `01-overview.md:90`).
5. **Speak decoupled.** Kokoro-82M TTS generation and playback run as separate workers: sentence N+1 synthesizes while sentence N plays, targeting 2–18× real-time CPU synthesis depending on workload (`01-overview.md:48-49`, `01-overview.md:87`).

Persistent state lives in three places: `config.yaml` as the master declarative config (`02-top-level-files.md:25`); benchmark traces at `benchmarks/session_<timestamp>.jsonl` with rolling stats in `benchmarks/latest_summary.json` (`01-overview.md:79`); and runtime VAD/turn buffers plus voiceprint embeddings held in process memory during a session (speculative turn buffer `01-overview.md:28`, VAD memory `01-overview.md:64`, CAM++ voiceprint guard `01-overview.md:67`).

## 3. The Full-Duplex Conversational Runtime

The central abstraction is the asynchronous conversational runtime itself, surfaced in code as `VoicePipeline` with its `PipelineConfig` family, re-exported through the `swar.py` facade (`02-top-level-files.md:92-94`). It is not a script that calls models in sequence; it is a scheduler that overlaps capture, transcription, reasoning, synthesis, and playback, with explicit cancellation scopes and a wake-state machine. Representation: configuration is declarative YAML (`general`, `vad`, `stt`, `tts`, `chunking`, `wake_word` sections at `config.yaml:9`, `config.yaml:37`, `config.yaml:61`, `config.yaml:74`, `config.yaml:101`, `config.yaml:130`); runtime composition happens in `run.py:71` where `VoicePipeline` is constructed with explicit VAD threshold, silence, STT language, live-transcription, TTS voice/speed, `device="cpu"`, wake mode, and partial/final callbacks (`02-top-level-files.md:7`).

Named kinds/types (all re-exported from `voice_pipeline` via `swar.py:9`):

- VAD: `SileroVAD`, `VADChunk` (`02-top-level-files.md:92`)
- STT: `ParakeetSTT`, `SmartProgressiveStreaming`, `PartialTranscription` (`02-top-level-files.md:92`)
- TTS/chunking: `KokoroTTS`, `TTSPipeline`, `AudioItem`, `IncrementalSpeakOutParser`, `RobustSentenceChunker`, `ChunkingConfig`, `TextSegment` (`02-top-level-files.md:92`)
- Pipeline/config: `VoicePipeline`, `PipelineConfig`, `GeneralConfig`, `VADConfig`, `STTConfig`, `TTSConfig` (`02-top-level-files.md:92`)
- Wake: `WakeWordEngine`, `WakeWordConfig`, `WakeTriggerConfig`, `WakeState` (`02-top-level-files.md:92`)
- Observability/voice: `BenchmarkLogger`, `BargeInGuardConfig`, `VoiceprintManager`, `SpeakerEmbeddingExtractor`, `PipeWireAECManager`, `PipeWireAECConfig` (`02-top-level-files.md:92`)

Key queries (verbatim):

```
Microphone Input (16kHz 16-bit PCM)
  → Silero VAD (v5 ONNX): Speech Start / Silence
  → NVIDIA Parakeet TDT 0.6B: Smart Progressive STT
  → Final Transcript (e.g. "Hello Relic, can you hear me?")
  → Stateful Wake Engine (STANDBY vs ACTIVE Mode)
  → Verified Query / Complete Original Transcription
  → Any LLM / Agent Brain (Local Ollama/vLLM/API)
  → Token Stream (real-time sentence chunking)
  → Decoupled Kokoro TTS [Generation Worker computes ahead in queue → Playback Worker streams to speaker]
  → Speaker Audio (24kHz PCM)
```

Source: `01-overview.md:40-50` (from `README.md:41-92`).

## 4. LLM / External Service Integration

Providers: any LLM or agent brain reachable over an OpenAI-compatible HTTP endpoint. The reference wiring is local Ollama/vLLM/API (`01-overview.md:46`), with the benchmark harness invoking `--url http://127.0.0.1:8080/v1 --model Qwen3.5-4B` (`01-overview.md:72-77`) against a calibrated ~50 tok/s expectation (`01-overview.md:84`). `run.py` imports `LLMClient` lazily from `examples.llm_client` only in `chat` mode (`02-top-level-files.md:72`).

Required vs optional: in `--mode chat` (the default) the LLM call is required every verified turn — `on_final` streams `llm.stream_response(transcript)` and speaks each returned sentence (`02-top-level-files.md:89`). In `--mode stt_only` no LLM call occurs. No hosted LLM or cloud speech API is required in either mode; the speech stack (Silero VAD, Parakeet STT, Kokoro TTS, CAM++ guard) runs offline on CPU (`01-overview.md:14-17`, `01-overview.md:5`).

Env vars and credentials: none documented in the wiki pages. Endpoint, model, and key are CLI flags (`--llm_url` default `"http://127.0.0.1:8080/v1"`, `--llm_api_key` default `"empty"`, `--llm_model` default `"default"` at `run.py:30`, `run.py:31`, `run.py:32`). The Python dependency enabling the OpenAI-compatible client is `openai>=1.0.0` (plus `requests>=2.28.0`) in `requirements.txt:1` (`02-top-level-files.md:53-69`).

## 5. The Listen-Think-Speak Loop

The primary workflow is the full-duplex voice turn loop launched by `run.py`: configure → construct pipeline → stream partials/finals → speak → benchmark, with barge-in cancellation at any point.

1. **Parse CLI and load config** — `run.py:25-36` defines `--mode` (`chat`/`stt_only`), `--min_silence_ms`, `--stt_language`, `--kokoro_voice`, `--tts_speed`, `--llm_url`, `--llm_api_key`, `--llm_model`, `--enable_live_transcription`, `--enable_thinking`, `--config`, `--wake` (`02-top-level-files.md:74-88`); `PipelineConfig.load_default_or_file(args.config)` loads `config.yaml` at `run.py:41`, and `--wake` forces `config.wake_word.enabled = True` at `run.py:42` (`02-top-level-files.md:6`).
2. **Emit interim transcription** — the `on_partial` callback at `run.py:55` writes `\r\033[K[Realtime]: {delta}` to stdout as the user speaks (`02-top-level-files.md:89`).
3. **Finalize turn and query the brain** — the `on_final` callback at `run.py:59` clears the line, prints `User: {transcript}`, and calls `llm.stream_response(transcript)` (`02-top-level-files.md:89`).
4. **Check interruption and speak** — per sentence, `on_final` checks `pipeline.is_interrupted`, prints each `Assistant:` sentence, and calls `pipeline.speak_text(sentence)` at `run.py:59` (`02-top-level-files.md:89`); playback-side cutoff is bounded at ~21.3ms per 512-sample slice (`01-overview.md:63`, `01-overview.md:88`).
5. **Run until interrupted** — `pipeline.start()` at `run.py:71` begins the loop, held alive by `while True: time.sleep(0.5)` at `run.py:85`, with `SIGINT`/`KeyboardInterrupt` handlers calling `pipeline.stop()` at `run.py:95` (`02-top-level-files.md:89`).
6. **Log benchmarks** — after each turn a metric card prints (TTFA, TTFT, TTFS, tok/s, TTS synthesis/RTF); traces append to `benchmarks/session_<timestamp>.jsonl`, rolling stats update `benchmarks/latest_summary.json`, and `Ctrl+C` renders the summary table (`01-overview.md:79`, `01-overview.md:83-88`).

## 6. Key Files

| File | Lines | What It Does |
|---|---|---|
| `README.md` | cited :9–:182 | Stack label, pipeline diagram, highlights table, benchmark harness/results, echo-rejection intro (`01-overview.md:14-17`, `01-overview.md:40-50`, `01-overview.md:55-67`, `01-overview.md:70-107`) |
| `run.py` | cited :1–:95 | CLI launcher; parses flags, loads config, wires callbacks, starts/stops `VoicePipeline` (`02-top-level-files.md:71-89`) |
| `swar.py` | cited :1–:40 | Public re-export facade; 29 names from `voice_pipeline` plus `__all__` (`02-top-level-files.md:91-94`) |
| `config.yaml` | 1007 total, visible prefix ~:1–:474 | Master declarative config (`general`, `vad`, `stt`, `tts`, `chunking`, `wake_word`); truncated mid trigger list (`02-top-level-files.md:24-50`) |
| `requirements.txt` | cited :1 (14 pins) | Pinned CPU audio/LLM dependency set (`02-top-level-files.md:52-69`) |
| `.gitignore` | cited :1–:221 | Standard Python ignores plus `benchmarks/*.jsonl`, `benchmarks/*.json`, `!benchmarks/.gitkeep` (`02-top-level-files.md:14-22`) |
| `voice_pipeline` (package) | re-export source for 29 names | Houses VAD/STT/TTS/chunking/pipeline/config/wake/benchmark/voiceprint implementations (`02-top-level-files.md:92`) |
| `examples/02_llm_voice_chat.py` | benchmark flags cited | Live-session benchmark harness with `--url`, `--model`, `--expected-tok-s` (`01-overview.md:70-77`) |
| `examples/llm_client` (module) | lazy import at `run.py:48` | Provides `LLMClient` used only in `chat` mode (`02-top-level-files.md:72`) |
| `benchmarks/session_<timestamp>.jsonl` | output trace | Per-turn metric traces (`01-overview.md:79`) |
| `benchmarks/latest_summary.json` | rolling output | Running aggregate stats (`01-overview.md:79`) |
| `benchmarks/.gitkeep` | placeholder | Kept by `.gitignore` exception so the dir survives without traces (`02-top-level-files.md:17-22`) |
| `docs/DEVELOPMENT_JOURNEY_AND_ARCHITECTURE.md` | pointer §7 | CPU-optimization deep dive referenced from README (`01-overview.md:104`) |

## 7. Dependencies

Required first (all verbatim constraint strings from `requirements.txt:1`, per `02-top-level-files.md:53-69`):

| Package | Version constraint | Purpose |
|---|---|---|
| `torch` | `>=2.4.0` | Tensor runtime for VAD/STT/TTS models on CPU |
| `torchaudio` | `>=2.4.0` | Audio I/O and resampling alongside torch |
| `nano-parakeet` | `>=0.2.1` | Parakeet TDT 0.6B STT inference |
| `kokoro` | `>=0.9.4` | Kokoro-82M TTS synthesis |
| `sounddevice` | `>=0.5.0` | PortAudio microphone/speaker streaming |
| `soundfile` | `>=0.12.0` | Audio file read/write |
| `numpy` | `>=1.26.0` | Numeric audio-buffer processing |
| `rich` | `>=13.0` | CLI console/metric-card rendering |
| `openai` | `>=1.0.0` | OpenAI-compatible LLM client |
| `requests` | `>=2.28.0` | HTTP calls |
| `speech-to-speech` | `>=0.2.12` | Speech pipeline utilities (VAD streaming events) |
| `onnxruntime` | `>=1.18.0` | Silero VAD v5 and CAM++ ONNX inference on CPU |
| `pyyaml` | `>=6.0` | `config.yaml` parsing |
| `huggingface-hub` | `>=0.20.0` | Model fetching (e.g. `nvidia/parakeet-tdt-0.6b-v3`) |

Model/runtime assets resolved at runtime rather than pip: Silero VAD v5 ONNX, `nvidia/parakeet-tdt-0.6b-v3` (`config.yaml:63`), Kokoro voice `af_bella` (`config.yaml:80`), CAM++ (~28MB ONNX, `01-overview.md:107`). No optional/dev dependency group is documented in the wiki pages.

## 8. CLI / Usage Surface

Entry points: `python run.py` (CLI launcher, `02-top-level-files.md:71-89`); `python examples/02_llm_voice_chat.py` (benchmarked voice-chat session, `01-overview.md:70-77`); library import `from swar import VoicePipeline, PipelineConfig, VoiceprintManager` (`02-top-level-files.md:91-94`).

Commands (all `run.py` flags, `02-top-level-files.md:74-88`):

| Flag | Type / action | Default |
|---|---|---|
| `--mode` | `choices=["chat", "stt_only"]` | `"chat"` |
| `--min_silence_ms` | `int` | `800` |
| `--stt_language` | `str` | `"en"` |
| `--kokoro_voice` | `str` | `"af_bella"` |
| `--tts_speed` | `float` | `1.0` |
| `--llm_url` | `str` | `"http://127.0.0.1:8080/v1"` |
| `--llm_api_key` | `str` | `"empty"` |
| `--llm_model` | `str` | `"default"` |
| `--enable_live_transcription` | `store_true`, default on | `True` |
| `--enable_thinking` | `store_true` | off |
| `--config` | `str` | `"config.yaml"` |
| `--wake` | `store_true` | off |

Benchmark command:

```bash
python examples/02_llm_voice_chat.py \
  --url http://127.0.0.1:8080/v1 \
  --model Qwen3.5-4B \
  --expected-tok-s 50.0
```

Source: `01-overview.md:70-77`. Exact parameter names are `--url`, `--model`, `--expected-tok-s`.

Env-var table: none documented in the wiki pages — endpoint, key, model, devices, and voices are flags or `config.yaml` keys, not environment variables.

Config table (selection; `02-top-level-files.md:27-34`):

| Section | Selected keys | Documented values |
|---|---|---|
| `general` | `device`, `cpu_threads`, `verbose`, `allow_barge_in`, `input_device`, `output_device` | `"cpu"`, `4`, `false`, `true`, `null`, `null` |
| `vad` | `threshold`, `min_silence_ms`, `min_speech_ms`, `min_speech_continuation_ms`, `speech_pad_ms`, `progressive_interval` | `0.6`, `256`, `384`, `192`, `500`, `0.5` |
| `stt` | `model_name`, `language`, `enable_live_transcription` | `"nvidia/parakeet-tdt-0.6b-v3"`, `"en"`, `true` |
| `tts` | `voice`, `speed`, `lang_code`, `sample_rate`, `max_text_queue_size`, `max_audio_queue_size` | `"af_bella"`, `1.18`, `"a"`, `24000`, `100`, `50` |
| `chunking` | `strategy`, `progressive_stages`, buffer seconds/sentences, `min_words_for_boundary` | `"progressive"`, `[2, 1]` then `[-1, 3]`, `5.0`/`1.5`/`3.5`, `1`/`2`/`3`, `2` |
| `wake_word` | `enabled`, `default_timeout`, `strip_wake_phrase`, `prefix_only`, `triggers[].phrase/timeout` | `false`, `15.0`, `false`, `false`, e.g. `"hey assistant"`/`20.0`, `"relic"`/`25.0` |

## 9. Extensibility Points

- **New pipeline behavior / orchestration** — extend `VoicePipeline` in the `voice_pipeline` package (re-exported at `swar.py:9`); `run.py:71` is the composition site where overrides and callbacks are injected (`02-top-level-files.md:7`, `02-top-level-files.md:89`).
- **Configuration surface** — add keys under the matching `config.yaml` section (`general`, `vad`, `stt`, `tts`, `chunking`, `wake_word`) and the corresponding `*Config` dataclass (`GeneralConfig`, `VADConfig`, `STTConfig`, `TTSConfig`, `WakeWordConfig` at `swar.py:9`); header rule is config-first, no Python edits for tuning (`02-top-level-files.md:25`).
- **STT / transcription policy** — extend `SmartProgressiveStreaming`, `ParakeetSTT`, or `PartialTranscription` (`swar.py:9`); live-transcription toggle is `stt.enable_live_transcription` (`config.yaml:69`) and `run.py:33`.
- **TTS / sentence streaming** — extend `TTSPipeline`, `KokoroTTS`, `IncrementalSpeakOutParser`, `RobustSentenceChunker`, `ChunkingConfig`, or `TextSegment` (`swar.py:9`); queue depths and `progressive_stages` live under `tts`/`chunking` (`config.yaml:93`, `config.yaml:96`, `config.yaml:112`).
- **Wake phrases and gating** — append to `wake_word.triggers` (`config.yaml:152`) and extend `WakeWordEngine` / `WakeTriggerConfig` / `WakeState` (`swar.py:9`); `--wake` at `run.py:36` forces enablement.
- **Speaker guard / echo defense** — extend `VoiceprintManager`, `SpeakerEmbeddingExtractor`, `BargeInGuardConfig`, or `PipeWireAECManager` / `PipeWireAECConfig` (`swar.py:9`); guard exists to stop TTS-from-speaker self-interruption loops (`01-overview.md:107`).
- **LLM backends** — replace or extend `LLMClient` in `examples.llm_client` (lazy import at `run.py:48`); endpoint/model/key arrive via `--llm_url`, `--llm_model`, `--llm_api_key` (`run.py:30-32`).
- **Metrics** — extend `BenchmarkLogger` (`swar.py:9`); per-turn cards, JSONL traces, and `latest_summary.json` are the documented sinks (`01-overview.md:79`).

## 10. Limitations and Gotchas

- **Benchmarks are single-machine and CPU-contingent.** Reported TTFA median 1,664ms, Kokoro sentence-1 median 1,235ms at 3.34× RTF, and 36.8 tok/s mean come from one ASUS TUF F16 (Intel Core 5 210H, 16GB DDR5, Arch Kernel 7.1.9, Python 3.11.16, `blocksize=512`) with the voice runtime on CPU (`01-overview.md:90`, `01-overview.md:94-102`). Other CPUs, block sizes, or devices will diverge; the deep-dive pointer is `docs/DEVELOPMENT_JOURNEY_AND_ARCHITECTURE.md#7` (`01-overview.md:104`).
- **Speaker-guard documentation is truncated in the wiki.** The incoming-microphone-audio ASCII diagram is cut off at `README.md:175-182`, so guard-mode behavior downstream of that diagram is not covered and should not be assumed (`01-overview.md:107`).
- **`config.yaml` coverage is partial.** The wiki chunk exposes only ~474 of 1007 lines and cuts the `wake_word.triggers` list mid-entry at `- phrase: "migrate"`; remaining triggers and any later sections are unknown from these pages (`02-top-level-files.md:36-50`).
- **`run.py` defaults disagree with `config.yaml` on two keys.** `run.py` defaults to `--min_silence_ms 800` (`run.py:26`) and `--tts_speed 1.0` (`run.py:29`) while `config.yaml` shows `vad.min_silence_ms 256` (`config.yaml:43`) and `tts.speed 1.18` (`config.yaml:83`); the effective value depends on override precedence at `run.py:71`, so verify which wins before tuning latency or voice rate (`02-top-level-files.md:27-34`, `02-top-level-files.md:74-88`).
- **No-headphone operation depends on the voiceprint guard.** Without it, speaker output re-enters the mic, fires VAD `SpeechStartedEvent`, and traps the runtime in a self-interruption loop (`01-overview.md:107`); speaker deployments should confirm CAM++ enrollment/mode before relying on barge-in.

## 11. How It Compares to Alternatives

The wiki names no competing end-to-end voice runtimes; its comparison table positions Swar only against unnamed "Traditional Pipelines" / "Sequential monolithic script[s]" (`01-overview.md:55-67`). The closest real named systems in the pages are the components Swar orchestrates plus the swappable brain backends:

- **Silero VAD (standalone scripts)** — using Silero directly gives speech/silence events but no progressive STT, turn buffering, wake gating, or 512-sample barge-in cutoff; Swar wraps it in the full-duplex scheduler (`01-overview.md:40-42`, `01-overview.md:63`).
- **NVIDIA Parakeet TDT (standalone transcription)** — running Parakeet alone waits for silence before transcribing; Swar adds 500ms interim deltas, speculative turn buffering, and sentence-wide wake forwarding (`01-overview.md:61`, `01-overview.md:64-65`).
- **Kokoro TTS (standalone synthesis)** — plain Kokoro calls block generation behind playback; Swar decouples generation and playback workers so sentence N+1 synthesizes during sentence N (`01-overview.md:62`).
- **Ollama / vLLM / OpenAI-compatible APIs (brain backends)** — these supply tokens only; Swar contributes the audio-side scheduling around them: `<think>` suppression for reasoning models (DeepSeek R1, Qwen 2.5), sentence chunking, TTFA/TTFT/TTFS instrumentation, and echo-guarded barge-in (`01-overview.md:46-48`, `01-overview.md:66-67`, `01-overview.md:83-88`).

Positioning sentence: Swar is the CPU-first offline orchestration layer between microphone/speaker drivers and swappable STT/TTS/LLM models, competing on turn-taking latency and concurrency rather than on model quality.

## Appendix: Selected Code Snippets

1. Stack label (`README.md:9-10`, via `01-overview.md:14-17`):

```
**100% Offline, CPU-First Conversational Audio Orchestration Layer**
*Silero VAD + NVIDIA Parakeet TDT STT + Kokoro-82M TTS*
```

2. Pinned dependencies (`requirements.txt:1`, via `02-top-level-files.md:53-69`):

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

3. Benchmark invocation (`README.md:155-159`, via `01-overview.md:70-77`):

```bash
python examples/02_llm_voice_chat.py \
  --url http://127.0.0.1:8080/v1 \
  --model Qwen3.5-4B \
  --expected-tok-s 50.0
```

4. Benchmark-output ignore rules (`.gitignore:221`, via `02-top-level-files.md:17-22`):

```
benchmarks/*.jsonl
benchmarks/*.json
!benchmarks/.gitkeep
```
