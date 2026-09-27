> [[index|Wiki]] | [[summary|Summary]]
# Project Aether — Digest

## 1. [[wiki/01-project-aether|Project Aether]]
**In one sentence:** Project Aether demonstrates a genuine streaming, full-duplex conversational voice system running entirely on a consumer RTX 3050 6 GB laptop GPU by co-executing Mimi, NF4-quantized Qwen2.5-1.5B, CPU Zipformer ASR, VAD barge-in, and linear AEC through eleven validated research steps (AETHER-1…AETHER-11).
## Key points
- Full-duplex voice AI runs on an NVIDIA GeForce RTX 3050 Laptop GPU (6 GB VRAM) with 1,636.1 MB peak allocated VRAM and 4,379.5 MB (71.3%) free headroom for Mimi + Qwen 1.5B NF4 coexistence.
- Mimi neural audio codec operates at 24 kHz, 12.5 frames/second (80.0 ms per frame), 8 codebooks, with real-time streaming encode and decode.
- Cooperative Yielding was frozen as the GPU scheduler after 0/2,250 deadline misses over 60-second runs (p50 latency 10.37 ms), beating uncoordinated generation whose p95 Mimi latency spiked to 99.16 ms.
- Sherpa-ONNX Streaming Zipformer (int8, CPU, 0 MB GPU VRAM) was frozen as ASR with WER 6.13%, avg RTF 0.0598, 2 threads, 80 ms cadence, and a 470 ms (7,520 samples) readiness floor.
- Acoustic VAD barge-in (20 ms frames, 2-frame confirmation, 100 ms pre-roll) detects speech onset in ~25–45 ms, cancelling interruption ~755 ms faster than the ~800.59 ms ASR-dependent path.
- Linear AEC (NLMS 512 taps + Geigel DTD) delivers ~20 dB ERLE with 100% double-talk interruption detection and <2 ms CPU overhead per 20 ms frame, reaching Class A production-ready status in AETHER-11.
- Heuristic echo gating was rejected because it suppressed 65–73% of legitimate double-talk interruptions despite rejecting 100% of single-talk echoes.

## 2. [[wiki/02-research-reports|Research Reports]]
**In one sentence:** Project Aether's research track is documented in nine reports spanning AETHER-4 through AETHER-11, covering ASR feasibility and benchmarks, Zipformer and perceived-latency optimization, VAD barge-in, full-duplex echo handling, and AEC research plus integration.
## Key points
- AETHER-4 (`AETHER4_STREAMING_ASR_FEASIBILITY_REPORT.md`) is the ASR candidate survey and feasibility analysis.
- AETHER-5 (`AETHER5_STREAMING_ASR_BENCHMARK_REPORT.md`) records the empirical ASR benchmark results.
- AETHER-6 (`AETHER6_ZIPFORMER_LATENCY_OPTIMIZATION_REPORT.md`) investigates Zipformer first-partial latency.
- AETHER-7 (`AETHER7_PERCEIVED_LATENCY_RESEARCH_REPORT.md`) covers pipeline-level perceived-latency strategies, extended by AETHER-7B (`AETHER7B_SPECULATIVE_PREPARATION_VALIDATION_REPORT.md`) with empirical validation of speculative preparation.
- AETHER-8 (`AETHER8_VAD_BARGE_IN_REPORT.md`) covers VAD barge-in implementation and validation.
- AETHER-9 (`AETHER9_FULL_DUPLEX_ECHO_AND_INTERRUPTION_REPORT.md`) analyzes full-duplex echo and false barge-in.
- AETHER-10 (`AETHER10_AEC_RESEARCH_AND_VALIDATION_REPORT.md`) covers linear AEC research and benchmark, followed by AETHER-11 (`AETHER11_AEC_INTEGRATION_REPORT.md`) with AEC integration and end-to-end validation.

## The argument in five moves
1. Coexistence is feasible but contention is the real constraint: Mimi plus NF4 Qwen fits in 6 GB VRAM with headroom, yet uncoordinated generation breaks Mimi's real-time deadline, so scheduling must be solved first.
2. Cooperative Yielding solves the GPU contention deterministically, holding zero deadline misses over sustained 60-second runs and getting frozen as the scheduler.
3. ASR must stay off the GPU entirely, so CPU int8 Zipformer is frozen on accuracy, RTF, and zero-VRAM grounds even though its readiness floor and ~0.8 s time-to-useful-partial cannot be tuned away.
4. Since ASR latency is irreducible, perceived interruption latency is attacked at the pipeline level: acoustic VAD barge-in reacts ~755 ms faster than the ASR path and is implemented as a validated controller.
5. Open-speaker full-duplex reintroduces false barge-ins from the system's own playback, heuristic gating fails by killing legitimate double-talk, and only linear NLMS AEC restores clean interruption handling.
6. Integrated end-to-end, the AEC-augmented barge-in stack validates as Class A production-ready within its envelope, closing the loop from memory baseline to full-duplex voice system.
