> PDF location (no PDF archived, under 2 MB rule N/A): https://github.com/vivekananda-2201/Swar

# vivekananda-2201/Swar
Source: https://github.com/vivekananda-2201/Swar
Kind: repo
Fetched: 2026-09-22T14:48:27.097597+00:00
Tool: git-clone

# vivekananda-2201/Swar

Commit: c0db89d7a5550794b98d4d09e641f779578cc5b8

## README

# Swar (स्वर) — Local Conversational Audio Runtime

**100% Offline, CPU-First Conversational Audio Orchestration Layer**  
*Silero VAD + NVIDIA Parakeet TDT STT + Kokoro-82M TTS*

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![License: AGPL-3.0](https://img.shields.io/badge/License-AGPL--3.0-blue.svg)](LICENSE)
[![Platform: Linux / macOS / Windows](https://img.shields.io/badge/platform-Linux%20%7C%20macOS%20%7C%20Windows-lightgrey.svg)]()
[![Hardware: CPU-First (GPU Supported)](https://img.shields.io/badge/hardware-CPU--First%20(GPU%20Supported)-orange.svg)]()

---

## 🎙️ What is Swar?

**Swar (स्वर)** is an open-source, low-latency **conversational audio runtime** designed from the ground up for **CPU-first execution**, while remaining fully compatible with GPU backends.

Rather than treating speech as a simple sequential pipeline (record → transcribe → query → synthesize → play), Swar operates as an asynchronous, full-duplex audio runtime. It solves the core concurrency and scheduling challenges of natural conversation:
- **Full-Duplex Streaming**: Real-time interim progressive transcription emitted while the user is still actively speaking.
- **Turn-Taking & Cancellation Scopes**: Bounded, near-zero interruption latency (~21.3ms audio block cutoff) that halts playback without crashing underlying ALSA/PortAudio sound card drivers.
- **Compute-Ahead Decoupled TTS**: An asynchronous producer–consumer engine where upcoming sentences are synthesized in the background while earlier sentences are actively playing through the speaker.
- **Speculative Turn Buffering**: Turn-boundary audio preservation so opening interruption words are never truncated or lost across conversational turns.
- **Stateful Wake Word Engine**: Case-insensitive, sentence-wide trigger detection that forwards the complete original user transcript to the downstream model.
- **Reasoning Model Stream Filtering**: In-flight state-machine suppression of internal reasoning monologues (`<think>...</think>`) from models like DeepSeek R1 and Qwen 2.5.
- **Speaker Echo Defense & Adaptive Barge-In Guard**: 3-mode voiceprint verification powered by CAM++ ONNX (~3ms CPU latency) that eliminates laptop speaker self-interruption on open speakers while allowing genuine human barge-in or personalized user whitelist recognition.

### Why CPU-First?
Running speech pipelines on high-TGP GPUs is relatively straightforward due to massive parallel matrix throughput. The true engineering and deployment challenge is achieving responsive, conversational turnarounds on standard multi-core laptop and server **CPUs** without exceeding thermal limits, requiring cloud APIs, or compromising synthesis fidelity.

Swar takes a **CPU-first** architectural approach: by decoupling synthesis from playback, pre-buffering upcoming sentences, utilizing sub-block audio slicing, and employing non-blocking thread scheduling, Swar masks CPU compute delays and delivers sub-second conversational turnarounds without requiring dedicated GPUs.

---

## 📐 Runtime Architecture

```
                          ┌───────────────────────────┐
                          │     Microphone Input      │
                          │     (16kHz 16-bit PCM)    │
                          └─────────────┬─────────────┘
                                        │
                                        ▼
                          ┌───────────────────────────┐
                          │   Silero VAD (v5 ONNX)    │
                          │   Speech Start / Silence  │
                          └─────────────┬─────────────┘
                                        │
                         Speech Event   │   Audio Frames
                                        ▼
                          ┌───────────────────────────┐
                          │  NVIDIA Parakeet TDT 0.6B │
                          │  Smart Progressive STT    │
                          └─────────────┬─────────────┘
                                        │
                       Final Transcript │ (e.g. "Hello Relic, can you hear me?")
                                        ▼
                          ┌───────────────────────────┐
                          │  Stateful Wake Engine     │
                          │  (STANDBY vs ACTIVE Mode) │
                          └─────────────┬─────────────┘
                                        │
                      Verified Query    │ Complete Original Transcription
                                        ▼
                          ┌───────────────────────────┐
                          │   Any LLM / Agent Brain   │
                          │   (Local Ollama/vLLM/API) │
                          └─────────────┬─────────────┘
                                        │
                       Token Stream     │ (Real-time sentence chunking)
                                        ▼
                          ┌───────────────────────────┐
                          │   Decoupled Kokoro TTS    │
                          │ ┌───────────────────────┐ │
                          │ │ Generation Worker     │ │ <── Computes ahead in queue
                          │ └───────────┬───────────┘ │
                          │             ▼             │
                          │ ┌───────────────────────┐ │
                          │ │ Playback Worker       │ │ <── Streams to speaker
                          │ └───────────────────────┘ │
                          └─────────────┬─────────────┘
                                        │
                                        ▼
                          ┌───────────────────────────┐
                          │      Speaker Audio        │
                          │        (24kHz PCM)        │
                          └───────────────────────────┘
```

---

## ⚡ Key Highlights

| Feature | Swar Implementation | Traditional Pipelines |
| :--- | :--- | :--- |
| **Runtime Architecture** | **Asynchronous Conversational Runtime** with decoupled scheduling | Sequential monolithic script |
| **Compute Profile** | **CPU-First** (AVX2/NEON vectorization); GPU optional | Requires dedicated 8GB+ VRAM GPU |
| **STT Latency** | Emits interim hypothesis deltas every **500ms** while user speaks | Waits for silence before transcribing |
| **TTS Concurrency** | **Decoupled**: Generation worker computes sentence $N+1$ while sentence $N$ plays | Blocks generation until previous audio finishes |
| **Barge-In Latency** | **Bounded ~21.3ms cutoff** (512-sample slice window) without ALSA driver faults | Audio ring buffer latency; PortAudio mmap crashes |
| **Interruption Retention** | Interrupting words are preserved in VAD memory for the next turn | Opening 1–2 words clipped or lost on barge-in |
| **Wake Detection** | Multi-phrase, case-insensitive, sentence-wide contains matching | Single fixed word, strict beginning-of-sentence prefix |
| **Reasoning Model Support**| In-flight state-machine stripping of `<think>` reasoning blocks | Model speaks aloud internal thoughts for 15+ seconds |
| **Speaker Echo Defense** | **3-Mode Adaptive Barge-In Guard** (CAM++ ~3ms CPU); eliminates self-interruption on open laptop speakers | Requires headphones; infinite self-interruption loop on speakers |

---

## 📊 Developer Benchmarks & Automated Profiling

Swar includes an automated, developer-focused benchmarking harness integrated directly into `examples/02_llm_voice_chat.py`. Rather than relying on theoretical estimates, Swar continuously measures and logs empirical turn-level metrics during live conversational sessions.

### What benchmark shows?

When building real-time conversational voice agents, what actually governs user experience:

1. **Time-to-First-Audio (TTFA)**: The end-to-end turnaround latency from the moment user speech stops (silence detected) to the moment the speaker begins playing the assistant's voice.
2. **LLM Time-to-First-Token (TTFT)**: How quickly your language model produces its initial response chunk.
3. **LLM Time-to-First-Sentence (TTFS)**: How long until Sentence 1 is fully formed and dispatched to the decoupled TTS engine.
4. **LLM Generation Speed**: Live throughput in tokens per second (calibrated with `Qwen3.5 4B` running at ~50 tokens/sec).
5. **Kokoro TTS Sentence 1 Synthesis & RTF**: Time to synthesize Chunk 1 and its Real-Time Factor speedup (e.g. $10\times - 18\times$ faster than real-time on CPU).
6. **Barge-In Interruption Cutoff**: Playback halt latency bounded within ~21.3ms (512-sample hardware slice window) without ALSA/PortAudio sound driver crashes.

### Test Machine Profile
- **Laptop**: ASUS TUF Gaming F16 (FX607VUR_FX677VU)
- **CPU**: Intel(R) Core(TM) 5 210H (4 P-Cores up to 4.8GHz + 4 E-Cores up to 3.6GHz, 12 Threads)
- **RAM**: 16 GB DDR5 (15.2 GB available)
- **GPU / Driver**: NVIDIA GeForce RTX 4050 Laptop GPU (Driver 610.57.04) — *voice runtime tested 100% on CPU*
- **OS**: Arch Linux (Kernel 7.1.9 x86_64, glibc 2.44, Python 3.11.16)
- **Audio Device**: Realtek Audio via PortAudio / ALSA (`blocksize=512`, `16kHz` input, `24kHz` output)
- **Stack**: Silero VAD v5 (ONNX) + NVIDIA Parakeet TDT 0.6B (CPU) + Kokoro-82M (CPU Native) + Qwen3.5-4B (~40–50 tok/s)

### Empirical Benchmark Results (Live Interactive Session)

Captured live during multi-turn conversational voice interaction across 8 real dialogue turns:

| Metric | Min | Median | Mean | P95 / Max | Unit |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Time-to-First-Audio (TTFA)** | **642.5 ms** | 1,664.3 ms | 1,560.9 ms | 2,425.6 ms | ms |
| **LLM Time-to-First-Token (TTFT)** | **148.7 ms** | 158.6 ms | 194.1 ms | 445.8 ms | ms |
| **LLM Time-to-First-Sentence (TTFS)** | **204.5 ms** | 470.6 ms | 449.1 ms | 671.0 ms | ms |
| **LLM Generation Throughput** | 20.8 | 39.5 | 36.8 | **40.8** | tok/s |
| **Kokoro Sentence 1 Synthesis (CPU)** | **436.1 ms** | 1,234.9 ms | 1,110.1 ms | 1,822.8 ms | ms |
| **Kokoro Real-Time Speedup (CPU)** | 2.05× | 3.34× | 3.19× | **3.85×** | Real-time |
| **Barge-In Interruption Cutoff** | — | — | **21.3 ms** | 21.3 ms | ms |

> 📖 **Deep Dive**: For detailed explanations of CPU thread optimizations, OpenMP barrier elimination, VAD silence tuning, and turn-by-turn logs, see [Architecture & Benchmark Analysis](docs/DEVELOPMENT_JOURNEY_AND_ARCHITECTURE.md#7-cpu-optimization-techniques--rigorous-benchmark-analysis).

### How to Run Automated Benchmarks
Run the voice chat tester with your local LLM:
```bash
python examples/02_llm_voice_chat.py \
  --url http://127.0.0.1:8080/v1 \
  --model Qwen3.5-4B \
  --expected-tok-s 50.0
```

- After each spoken turn, a developer metric card prints to your terminal.
- Behind the scenes, full per-turn traces are saved to `benchmarks/session_<timestamp>.jsonl`.
- Running summary statistics (median, mean, p95, min, max) are automatically updated in `benchmarks/latest_summary.json`.
- When exiting with `Ctrl+C`, a comprehensive summary table across all conversational turns is displayed.


---

## 🛡️ Speaker Echo Rejection & 3-Mode Barge-In Guard

When using laptop speakers without headphones, traditional voice pipelines suffer from a fatal flaw: **acoustic self-interruption**. The assistant's TTS audio emits from the chassis speakers, reflects off surfaces, enters the microphone, and triggers the VAD (`SpeechStartedEvent`), cutting the assistant off on its very first syllable in an endless self-interruption loop.

Swar solves this with an ultra-lightweight **3-Mode Barge-In Guard** powered by the **CAM++ (D-TDNN)** speaker embedding model (~28MB ONNX, **~3ms CPU latency** via `onnxruntime`):

```
                       ┌─────────────────────────────────────┐
                       │     Incoming Microphone Audio       │
                       └──────────────────┬──────────────────┘
                                          │
                                          ▼
                       ┌─────────────────────────────────────┐
             

... (truncated, 15173 more characters)

## pyproject.toml

```
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "swar"
version = "0.1.0"
description = "Swar: High-Performance Local Conversational Audio Runtime (CPU-First Silero VAD + Parakeet TDT STT + Kokoro TTS)"
readme = "README.md"
requires-python = ">=3.10"
dependencies = [
    "torch>=2.4.0",
    "torchaudio>=2.4.0",
    "nano-parakeet>=0.2.1",
    "kokoro>=0.9.4",
    "sounddevice>=0.5.0",
    "soundfile>=0.12.0",
    "numpy>=1.26.0",
    "rich>=13.0",
    "openai>=1.0.0",
    "requests>=2.28.0",
    "speech-to-speech>=0.2.12",
    "onnxruntime>=1.18.0",
    "pyyaml>=6.0",
    "huggingface-hub>=0.20.0",
]

[tool.setuptools.packages.find]
where = ["."]
include = ["voice_pipeline*"]

[tool.setuptools]
py-modules = ["swar"]

```

## Top-level layout

- .gitignore (~224 lines)
- benchmarks/ (dir, 1 files, ~1 lines)
- config.yaml (~1006 lines)
- docs/ (dir, 1 files, ~683 lines)
- examples/ (dir, 4 files, ~858 lines)
- LICENSE (~661 lines)
- pyproject.toml (~33 lines)
- README.md (~568 lines)
- requirements.txt (~15 lines)
- run.py (~102 lines)
- swar.py (~69 lines)
- tools/ (dir, 1 files, ~494 lines)
- voice_pipeline/ (dir, 14 files, ~3940 lines)

