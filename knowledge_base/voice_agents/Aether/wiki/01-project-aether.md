[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Project Aether
**In one sentence:** Project Aether demonstrates a genuine streaming, full-duplex conversational voice system running entirely on a consumer RTX 3050 6 GB laptop GPU by co-executing Mimi, NF4-quantized Qwen2.5-1.5B, CPU Zipformer ASR, VAD barge-in, and linear AEC through eleven validated research steps (AETHER-1…AETHER-11).
## Key points
- Full-duplex voice AI runs on an NVIDIA GeForce RTX 3050 Laptop GPU (6 GB VRAM) with 1,636.1 MB peak allocated VRAM and 4,379.5 MB (71.3%) free headroom for Mimi + Qwen 1.5B NF4 coexistence.
- Mimi neural audio codec operates at 24 kHz, 12.5 frames/second (80.0 ms per frame), 8 codebooks, with real-time streaming encode and decode.
- Cooperative Yielding was frozen as the GPU scheduler after 0/2,250 deadline misses over 60-second runs (p50 latency 10.37 ms), beating uncoordinated generation whose p95 Mimi latency spiked to 99.16 ms.
- Sherpa-ONNX Streaming Zipformer (int8, CPU, 0 MB GPU VRAM) was frozen as ASR with WER 6.13%, avg RTF 0.0598, 2 threads, 80 ms cadence, and a 470 ms (7,520 samples) readiness floor.
- Acoustic VAD barge-in (20 ms frames, 2-frame confirmation, 100 ms pre-roll) detects speech onset in ~25–45 ms, cancelling interruption ~755 ms faster than the ~800.59 ms ASR-dependent path.
- Linear AEC (NLMS 512 taps + Geigel DTD) delivers ~20 dB ERLE with 100% double-talk interruption detection and <2 ms CPU overhead per 20 ms frame, reaching Class A production-ready status in AETHER-11.
- Heuristic echo gating was rejected because it suppressed 65–73% of legitimate double-talk interruptions despite rejecting 100% of single-talk echoes.
---
## 1. Project Overview
**Covers:** Project Aether, sections 1–2

Project Aether is "An independent realtime full-duplex voice AI/model research project focused on low-latency conversational speech, continuous listening, interruption handling, natural backchannels, streaming speech processing, and hardware-aware model execution."

The core architecture explores the harmonized co-execution of:

- **Neural Audio Codec (Mimi)**: Operating at 24 kHz, 12.5 frames/second (80.0 ms per frame), 8 codebooks, providing real-time streaming encode and decode.
- **Semantic Reasoning Core (Qwen2.5-1.5B-Instruct)**: 4-bit NormalFloat (NF4) quantized via bitsandbytes with bfloat16 compute, providing low-latency conversational text generation.
- **Streaming ASR (Sherpa-ONNX Zipformer)**: int8 CPU inference, zero GPU VRAM usage, 80 ms ingestion cadence, WER ~6.13% on clean speech.
- **VAD Barge-In Controller**: 20 ms frame / 2-frame confirmation, ~25–45 ms speech-onset detection with 100 ms pre-roll preservation.
- **Linear AEC (NLMS + Geigel DTD)**: ~20 dB ERLE, 100% double-talk interruption detection, <2 ms CPU overhead per 20 ms frame.

## 2. Target Hardware & Runtime Environment
**Covers:** Section 2

| Component | Specification |
|-----------|--------------|
| **Host OS** | Windows 11 Home 64-bit |
| **CPU** | Intel Core i5-13450HX (10 physical / 16 logical cores) |
| **RAM** | 16.0 GB DDR5 |
| **GPU** | NVIDIA GeForce RTX 3050 6 GB Laptop GPU (6,143.5 MB physical VRAM) |
| **CUDA Runtime** | 12.4 (`torch 2.6.0+cu124`, `NO_TORCH_COMPILE=1` for Windows) |
| **Frameworks** | `moshi 0.2.13`, `transformers 5.16.1`, `bitsandbytes 0.50.2`, `accelerate 1.14.0` |

## 3. Validated Architecture (Post AETHER-11)
**Covers:** Section 3

```
Microphone (24 kHz)
        │
        ▼
  ┌─────────────────────────────────────┐
  │         AetherAEC (aether_aec.py)   │  ◄── playback reference (Mimi 24→16 kHz)
  │  NLMS (512 taps) + Geigel DTD      │
  │  ~20 dB ERLE, <2 ms/frame CPU      │
  └──────────────┬──────────────────────┘
                 │ clean mic signal (16 kHz)
        ┌────────┴──────────┐
        │                   │
        ▼                   ▼
  VAD Barge-In         Zipformer ASR
  (20 ms frames)      (sherpa-onnx int8, CPU)
  ~25–45 ms onset      80 ms cadence
  detection            WER ~6.13%
        │                   │
        └────────┬──────────┘
                 │
          AetherBargeInController
          (aether_barge_in.py)
                 │ finalized transcripts
                 ▼
        Qwen2.5-1.5B NF4 (CUDA)
        Cooperative Yielding scheduler
                 │
                 ▼
        Mimi decode → Speaker (24 kHz)
```

## 4. Research Loop Progression
**Covers:** Section 4, AETHER-1…AETHER-11

### AETHER-1 — Memory Coexistence & Contention Baseline
- **Goal**: Can Mimi + Qwen 1.5B NF4 fit in 6 GB VRAM simultaneously?
- **Result**: Peak allocated VRAM = **1,636.1 MB** (1,764 MB reserved); **4,379.5 MB (71.3%) free headroom**. Idle Qwen = 0% Mimi latency impact. Uncoordinated active generation → p95 Mimi latency spike to 99.16 ms (1 deadline miss/186 frames).
- **Decision**: Memory feasible; compute contention is the bottleneck.

### AETHER-2 — GPU Scheduling Feasibility
- **Goal**: Which scheduling regime keeps Mimi p95 < 80 ms while Qwen generates?
- **Conditions tested**: Uncoordinated baseline / CUDA Stream Priority / Cooperative Yielding / Fine-Grained Slicing.
- **Result**: Both **CUDA Stream Priority** (max 24.50 ms, 16.54 tok/s) and **Cooperative Yielding** (max 22.07 ms, 18.83 tok/s) eliminated all deadline violations.
- **Decision**: Cooperative Yielding selected as primary scheduler.

### AETHER-3 — Sustained Scheduling Robustness Validation
- **Goal**: Does Cooperative Yielding remain stable over 60-second continuous workloads (2,250 frames × 3 runs)?
- **Result**: **0/2,250 deadline misses**, p50 latency 10.37 ms, zero backlog accumulation, zero thread/VRAM leaks.
- **Decision**: Cooperative Yielding **officially frozen** as Aether's GPU scheduler.

### AETHER-4 — Streaming Speech Recognition Feasibility
- **Goal**: Which streaming ASR model fits the 6 GB VRAM envelope without GPU contention?
- **Result**: **Sherpa-ONNX Streaming Zipformer** (int8, CPU) — 0 MB GPU VRAM, 0 GPU SM contention, sub-300 ms streaming partials, RTF < 0.10. Moonshine Streaming viable but GPU-bound. Whisper/NeMo eliminated.
- **Decision**: Zipformer on CPU selected for AETHER-5 benchmarking.

### AETHER-5 — Streaming ASR Benchmark (Zipformer vs Moonshine)
- **Goal**: Empirically validate Zipformer int8 on CPU vs Moonshine Tiny on CUDA under realistic conversational workloads.
- **Result**: Zipformer int8 — WER **6.13%**, avg RTF **0.0598**, 2 threads, chunk 160 ms; Moonshine — WER 4.2% but +150–250 MB VRAM and GPU SM contention under Mimi load.
- **Decision**: **Zipformer int8 CPU frozen** as Aether's ASR engine.

### AETHER-6 — Zipformer First-Partial Latency Optimization
- **Goal**: Can the ~1.34 s time-to-first-useful-partial (TTFUP) be reduced without replacing Zipformer?
- **Findings**: 40/80/160 ms cadence produced identical TTFP/TTFUP. Blank penalty gave ~60 ms improvement with unacceptable accuracy tradeoffs. Pre-buffering worsened reset latency. **Zipformer readiness floor: 470 ms (7,520 samples)**. Actual speech-onset → useful partial on conversational audio: **~0.80–0.90 s**.
- **Decision**: 80 ms cadence selected; Zipformer configuration frozen. Latency investigation shifts to pipeline-level strategies.

### AETHER-7 — Perceived-Latency Reduction Research
- **Goal**: Which pipeline-level techniques can reduce perceived end-to-end latency without model replacement?
- **Hypotheses evaluated**: Acoustic/VAD onset detection, speculative KV-cache prefill, partial-ASR triggered generation.
- **Strongest finding**: VAD can detect speech onset **~800 ms before** ASR delivers a finalized transcript — enabling dramatically faster barge-in cancellation.
- **Rejected**: Speculative KV caching (negligible gain vs. complexity); partial-ASR triggered generation (hallucination risk).

### AETHER-7B — Speculative Preparation Empirical Validation
- **Goal**: Measure actual latency deltas for the top AETHER-7 hypotheses on the frozen stack.
- **Measured results**:
  - 10 ms VAD detection: **~25.0 ms** from speech onset
  - 20 ms VAD detection: **~45.0 ms**
  - 80 ms VAD detection: **~105.0 ms**
  - FIFO clear/mute overhead: **< 0.02 ms**
  - Zipformer reset: **~0.593 ms**
  - ASR-dependent interruption reaction: **~800.59 ms**
  - **20 ms VAD → ~755 ms faster interruption cancellation** vs ASR-dependent path
- **Decision**: Implement acoustic VAD barge-in as AETHER-8.

### AETHER-8 — VAD-Based Barge-In Implementation & Validation
- **Goal**: Implement and validate `AetherBargeInController` with acoustic VAD interruption muting.
- **Configuration**: 20 ms frames, 2 confirmation frames, 100 ms pre-roll audio preservation.
- **Result**: VAD barge-in functional; Qwen generation cancels correctly; Zipformer reset sub-millisecond; 0 VRAM/thread leaks over repeated interruption cycles.
- **Artifact**: `aether_barge_in.py`

### AETHER-9 — Full-Duplex Echo & False Barge-In Risk Investigation
- **Goal**: Characterize false barge-in risk in open-speaker (no headset) operation.
- **Finding**: In open-speaker mode, Aether's own playback couples acoustically into the microphone and reliably triggers VAD. Lightweight heuristic echo gating rejected 100% of single-talk echoes but suppressed **65–73% of legitimate double-talk interruptions** — unacceptable for full-duplex.
- **Decision**: A linear Acoustic Echo Cancellation (AEC) preprocessor is required. Identified the `playback_fifo` as the accessible reference signal.

### AETHER-10 — Linear AEC Research & Benchmark
- **Goal**: Evaluate NLMS + Geigel Double-Talk Detector as an AEC solution for the Aether pipeline.
- **Measured results**:
  - Echo Return Loss Enhancement (ERLE): **~20 dB**
  - Single-talk echo rejection: **100% at ≤ −18 dB coupling**, >95% at ≤ −12 dB
  - Double-talk interruption detection: **100%** in tested scenarios
  - Detection latency: **+90 to +100 ms** from actual user onset
  - AEC CPU cost: **1.74 ms p50 / 5.36 ms p95** per 20 ms frame
  - Mimi 80 ms deadline misses during full concurrent stress: **0/200**
- **Key limitation**: AEC requires **300–500 ms to converge** from cold start.
- **Decision**: Class A — integrate into AETHER-11.

### AETHER-11 — AEC Integration & End-to-End Validation
- **Goal**: Integrate `AetherAEC` into `AetherBargeInController`; validate full-stack coexistence.
- **Implementation**:
  - `aether_aec.py`: NLMS (512 taps) filter, Geigel DTD, 24→16 kHz polyphase resampling, bulk delay FIFO alignment.
  - `aether_barge_in.py`: Routes clean mic output to both VAD and Zipformer; AEC adaptive weights persist across turns (warm-start); transient buffers reset on barge-in.
  - Startup protection: correlation-based transient suppression for first 300 ms of un-converged speech.
- **Validation**: 5-scenario end-to-end suite (Startup, High-Volume, Matrix A–I, Stability, Realtime).
- **Final result**: **Class A — Production-Ready** within defined operating envelope.
- **Artifacts**: `aether_aec.py`, `aether_barge_in.py`, `AETHER11_AEC_INTEGRATION_REPORT.md`

## 5. Current Validated Stack Summary
**Covers:** Sections 5–6

| Layer | Component | Config | Status |
|-------|-----------|--------|--------|
| Audio codec | Mimi (moshi) | 24 kHz, 80 ms cadence, CUDA | ✅ Frozen |
| GPU scheduler | Cooperative Yielding | Qwen yields during Mimi frames | ✅ Frozen |
| ASR | Sherpa-ONNX Zipformer int8 | CPU, 2 threads, 80 ms cadence | ✅ Frozen |
| LLM | Qwen2.5-1.5B-Instruct NF4 | RTX 3050, bfloat16 compute | ✅ Frozen |
| Barge-in VAD | AetherBargeInController | 20 ms / 2-frame / 100 ms pre-roll | ✅ Frozen |
| Echo cancellation | AetherAEC (NLMS + Geigel DTD) | 512 taps, ~20 dB ERLE | ✅ Frozen |

## 6. Benchmark Scripts & Artifacts
**Covers:** Section 6

| Script | Description |
|--------|-------------|
| `benchmark_mimi.py` | Standalone Mimi streaming codec benchmark |
| `benchmark_aether2_scheduling.py` | AETHER-2 4-condition GPU scheduling evaluation |
| `benchmark_aether3_sustained.py` | AETHER-3 60-second sustained robustness validation |
| `benchmark_aether5_asr.py` | AETHER-5 Zipformer vs Moonshine ASR benchmark |
| `benchmark_aether5_final.py` | AETHER-5 final consolidated ASR validation |
| `benchmark_aether6_experiments.py` | AETHER-6 Zipformer cadence/latency experiments |
| `benchmark_aether7b_speculative.py` | AETHER-7B speculative preparation timing validation |
| `benchmark_aether8_barge_in.py` | AETHER-8 VAD barge-in controller validation |
| `benchmark_aether9_full_duplex.py` | AETHER-9 echo / false barge-in characterization |
| `benchmark_aether10_aec.py` | AETHER-10 NLMS+Geigel AEC research benchmark |
| `benchmark_aether11_aec_integration.py` | AETHER-11 end-to-end AEC integration validation |
