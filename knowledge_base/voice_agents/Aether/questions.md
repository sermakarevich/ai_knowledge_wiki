---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---
> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: Project Aether

### Q1. What is the frozen Aether stack and what target hardware does it run on?

> [!tip]- Answer
> > The frozen stack combines Mimi at 24 kHz / 12.5 frames/s / 8 codebooks, Qwen2.5-1.5B-Instruct in NF4 with bfloat16 compute, Sherpa-ONNX Zipformer int8 on CPU, a VAD barge-in controller, and NLMS + Geigel linear AEC. It runs entirely on a 6 GB RTX 3050 laptop GPU with a 16 GB DDR5 host, validating full-duplex conversational voice on consumer hardware. See [[wiki/01-project-aether|Project Aether]].

### Q2. What did AETHER-1 (memory coexistence) prove, and why was Cooperative Yielding frozen in AETHER-2/3?

> [!tip]- Answer
> > AETHER-1 showed Mimi + Qwen NF4 fit in 6 GB VRAM at 1,636.1 MB allocated / 1,764 MB reserved peak with 71.3% free, but uncoordinated generation spiked Mimi p95 to 99.16 ms with a deadline miss. AETHER-2 found both CUDA Stream Priority and Cooperative Yielding eliminated misses, and Cooperative Yielding was selected for higher throughput (18.83 tok/s). AETHER-3 froze it after 0/2,250 misses over sustained 60-second runs. See [[wiki/01-project-aether|Project Aether]].

### Q3. Why was CPU Zipformer int8 frozen over Moonshine, and what first-partial latency floor did AETHER-6 find?

> [!tip]- Answer
> > Zipformer int8 was frozen with WER 6.13%, avg RTF 0.0598, 2 threads and zero GPU VRAM, while Moonshine had better WER (4.2%) but added 150–250 MB VRAM plus GPU SM contention. AETHER-6 showed 40/80/160 ms cadence gave identical time-to-first-partial, with a 470 ms readiness floor and ~0.80–0.90 s onset-to-useful-partial on conversational audio. The 80 ms cadence was frozen and latency work shifted to pipeline-level strategies. See [[wiki/01-project-aether|Project Aether]].

### Q4. How much faster is VAD barge-in than the ASR-dependent path, and why was heuristic echo gating rejected in AETHER-9?

> [!tip]- Answer
> > A 20 ms VAD detects onset in ~45 ms versus ~800.59 ms for the ASR-dependent reaction, enabling ~755 ms faster interruption cancellation. In open-speaker mode the system's own playback couples into the mic and reliably triggers VAD, but heuristic echo gating suppressed 65–73% of legitimate double-talk. It was therefore rejected in favor of a linear AEC preprocessor using playback_fifo as reference. See [[wiki/01-project-aether|Project Aether]].

### Q5. Which reports document the ASR feasibility-to-latency arc (AETHER-4 through AETHER-7B), and what does each contribute?

> [!tip]- Answer
> > AETHER-4 surveys streaming ASR candidates for the 6 GB VRAM envelope, AETHER-5 records the empirical Zipformer-vs-Moonshine benchmark, and AETHER-6 investigates Zipformer first-partial latency. AETHER-7 then researches pipeline-level perceived-latency strategies, extended by AETHER-7B with empirical validation of speculative preparation. Together they form the evidence chain from ASR selection to the VAD barge-in decision. See [[wiki/02-research-reports|Research Reports]].

### Q6. Which reports cover barge-in, echo analysis, AEC research, and integration (AETHER-8 through AETHER-11)?

> [!tip]- Answer
> > AETHER-8 covers VAD barge-in implementation and validation, and AETHER-9 analyzes full-duplex echo and false barge-in risk. AETHER-10 then reports the linear NLMS + Geigel AEC research and benchmark (~20 dB ERLE, 100% double-talk detection), followed by AETHER-11 with AEC integration and end-to-end validation. The arc closes with a Class A production-ready verdict within the defined operating envelope. See [[wiki/02-research-reports|Research Reports]].

### Q7. Would you recommend this stack as a starting point for a new low-latency full-duplex voice prototype on consumer hardware?

> [!tip]- Answer
> > Yes, with qualifications: adopt the proven combination of Cooperative Yielding, CPU Zipformer int8, VAD barge-in with 100 ms pre-roll, and warm-started NLMS AEC, since each resolves a measured bottleneck. Budget for the irreducible ~0.8–1.3 s ASR first-partial floor and the 300–500 ms AEC cold-start convergence in the interaction design. See [[wiki/01-project-aether|Project Aether]].
