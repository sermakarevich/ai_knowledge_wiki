[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Overview
**In one sentence:** Swar is a 100% offline, CPU-first, full-duplex conversational audio runtime orchestrating Silero VAD + Parakeet TDT STT + Kokoro TTS (README.md:9, README.md:21).
## Key points
- Swar is an open-source, low-latency conversational audio runtime designed for CPU-first execution while remaining GPU-compatible (README.md:21).
- It operates as an asynchronous full-duplex runtime, not a sequential record-transcribe-query-synthesize-play pipeline (README.md:23).
- It emits real-time interim progressive transcription while the user is still speaking (README.md:24).
- It provides bounded ~21.3ms audio block cutoff for turn-taking/cancellation without crashing ALSA/PortAudio drivers (README.md:25, README.md:104).
- It uses an asynchronous producer–consumer TTS engine where upcoming sentences synthesize in the background while earlier sentences play (README.md:26).
- It preserves turn-boundary audio via a speculative turn buffer so opening interruption words are never lost (README.md:27).
- It includes a stateful case-insensitive sentence-wide wake-word engine forwarding the complete original transcript (README.md:28), plus in-flight `<think>...</think>` suppression for reasoning models (README.md:29) and a 3-mode CAM++ ONNX (~3ms CPU) speaker echo defense / barge-in guard (README.md:30).
---
## What is Swar
Swar (स्वर) is an open-source, low-latency **conversational audio runtime** designed for **CPU-first execution**, fully compatible with GPU backends (README.md:21). Verbatim stack label (README.md:9-10):

> **100% Offline, CPU-First Conversational Audio Orchestration Layer**
> *Silero VAD + NVIDIA Parakeet TDT STT + Kokoro-82M TTS*

Rather than a simple sequential pipeline (README.md:23):

> record → transcribe → query → synthesize → play

it solves concurrency/scheduling for natural conversation via (README.md:24-30):

- **Full-Duplex Streaming**: interim progressive transcription while the user speaks.
- **Turn-Taking & Cancellation Scopes**: ~21.3ms audio block cutoff, no ALSA/PortAudio driver crash.
- **Compute-Ahead Decoupled TTS**: upcoming sentences synthesized in background while earlier ones play.
- **Speculative Turn Buffering**: turn-boundary audio preservation across turns.
- **Stateful Wake Word Engine**: case-insensitive sentence-wide trigger detection, forwards complete original transcript.
- **Reasoning Model Stream Filtering**: state-machine suppression of `<think>...</think>` monologues (DeepSeek R1, Qwen 2.5).
- **Speaker Echo Defense & Adaptive Barge-In Guard**: 3-mode CAM++ ONNX voiceprint verification (~3ms CPU latency).

### Why CPU-first
Per README.md:33-35, GPUs make speech pipelines easy via matrix throughput; the deployment challenge is responsive turnarounds on multi-core laptop/server **CPUs** without thermal excess, cloud APIs, or fidelity loss. Swar masks CPU delays via decoupled synthesis-from-playback, pre-buffered sentences, sub-block audio slicing, and non-blocking thread scheduling for sub-second turnarounds without dedicated GPUs.

## Runtime architecture
Verbatim pipeline (README.md:41-92):

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

Input is 16kHz 16-bit PCM (README.md:44); output is 24kHz PCM (README.md:90).

## Key highlights
Verbatim comparison table (README.md:98-108):

| Feature | Swar Implementation | Traditional Pipelines |
| :--- | :--- | :--- |
| **Runtime Architecture** | **Asynchronous Conversational Runtime** with decoupled scheduling | Sequential monolithic script |
| **Compute Profile** | **CPU-First** (AVX2/NEON vectorization); GPU optional | Requires dedicated 8GB+ VRAM GPU |
| **STT Latency** | Interim hypothesis deltas every **500ms** while user speaks | Waits for silence before transcribing |
| **TTS Concurrency** | **Decoupled**: Generation worker computes sentence N+1 while sentence N plays | Blocks generation until previous audio finishes |
| **Barge-In Latency** | **Bounded ~21.3ms cutoff** (512-sample slice window) without ALSA driver faults | Audio ring buffer latency; PortAudio mmap crashes |
| **Interruption Retention** | Interrupting words preserved in VAD memory for next turn | Opening 1–2 words clipped/lost on barge-in |
| **Wake Detection** | Multi-phrase, case-insensitive, sentence-wide contains matching | Single fixed word, strict prefix |
| **Reasoning Model Support** | In-flight state-machine stripping of `<think>` blocks | Speaks internal thoughts for 15+ seconds |
| **Speaker Echo Defense** | **3-Mode Adaptive Barge-In Guard** (CAM++ ~3ms CPU) | Requires headphones; self-interruption loop on speakers |

## Developer benchmarks and profiling
Benchmark harness is integrated into `examples/02_llm_voice_chat.py` and logs empirical turn-level metrics during live sessions (README.md:114). Benchmark command verbatim (README.md:155-159):

```bash
python examples/02_llm_voice_chat.py \
  --url http://127.0.0.1:8080/v1 \
  --model Qwen3.5-4B \
  --expected-tok-s 50.0
```

Exact parameter names: `--url`, `--model`, `--expected-tok-s` (README.md:156-158). After each turn a metric card prints; traces go to `benchmarks/session_<timestamp>.jsonl`; running stats update `benchmarks/latest_summary.json`; `Ctrl+C` shows the summary table (README.md:161-164).

Governing UX metrics (README.md:120-126):

1. **Time-to-First-Audio (TTFA)**: silence-detected → speaker starts.
2. **LLM Time-to-First-Token (TTFT)**: first response chunk latency.
3. **LLM Time-to-First-Sentence (TTFS)**: Sentence 1 formed and dispatched to TTS.
4. **LLM Generation Speed**: tokens/sec (calibrated `Qwen3.5 4B` ~50 tok/s).
5. **Kokoro TTS Sentence 1 Synthesis & RTF**: Chunk 1 time and Real-Time Factor (e.g. 10×–18× faster than real-time on CPU).
6. **Barge-In Interruption Cutoff**: ~21.3ms (512-sample slice), no driver crash.

Test machine profile (README.md:128-134): ASUS TUF Gaming F16, Intel Core 5 210H (4P+4E, 12 threads), 16GB DDR5, RTX 4050 Laptop (voice runtime 100% CPU), Arch Linux Kernel 7.1.9, Python 3.11.16, Realtek via PortAudio/ALSA (`blocksize=512`, 16kHz in, 24kHz out), Silero VAD v5 ONNX + Parakeet TDT 0.6B CPU + Kokoro-82M CPU Native + Qwen3.5-4B (~40–50 tok/s).

Empirical results over 8 live turns (README.md:140-148):

| Metric | Min | Median | Mean | P95 / Max | Unit |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Time-to-First-Audio (TTFA)** | **642.5 ms** | 1,664.3 ms | 1,560.9 ms | 2,425.6 ms | ms |
| **LLM Time-to-First-Token (TTFT)** | **148.7 ms** | 158.6 ms | 194.1 ms | 445.8 ms | ms |
| **LLM Time-to-First-Sentence (TTFS)** | **204.5 ms** | 470.6 ms | 449.1 ms | 671.0 ms | ms |
| **LLM Generation Throughput** | 20.8 | 39.5 | 36.8 | **40.8** | tok/s |
| **Kokoro Sentence 1 Synthesis (CPU)** | **436.1 ms** | 1,234.9 ms | 1,110.1 ms | 1,822.8 ms | ms |
| **Kokoro Real-Time Speedup (CPU)** | 2.05× | 3.34× | 3.19× | **3.85×** | Real-time |
| **Barge-In Interruption Cutoff** | — | — | **21.3 ms** | 21.3 ms | ms |

Deep dive pointer in chunk: `docs/DEVELOPMENT_JOURNEY_AND_ARCHITECTURE.md#7-cpu-optimization-techniques--rigorous-benchmark-analysis` (README.md:150).

## Speaker echo rejection and barge-in guard
Without headphones, TTS audio re-enters the mic and triggers VAD `SpeechStartedEvent`, cutting the assistant off in a self-interruption loop (README.md:171). Fix: ultra-lightweight **3-Mode Barge-In Guard** with **CAM++ (D-TDNN)** speaker embedding (~28MB ONNX, **~3ms CPU latency** via `onnxruntime`) (README.md:173). Truncated in chunk: the incoming-microphone-audio ASCII diagram beginning at README.md:175-182 is cut off, so guard-mode details downstream of that diagram are not covered here.

**Covers:** README.md (repo overview, architecture diagram, highlights table, benchmark harness and results, echo-rejection intro); truncated: speaker-guard diagram at chunk lines 175–182 cut off, contents not guessed.
