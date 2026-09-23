> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Realtime-Venus: A Full-Duplex Interaction System with Asynchronous Delegation — Overview
**In one sentence:** Realtime-Venus is a proactive full-duplex interaction system with two separately trained 9B models (Omni for audio–visual, Audio for spoken interaction) coordinated by a dual-loop runtime that keeps foreground interaction live while Realtime-Venus-Harness executes tasks asynchronously.
## Key points
- Realtime-Venus provides two separately trained 9B models: Realtime-Venus-Omni for audio–visual interaction and Realtime-Venus-Audio for spoken interaction.
- Each model serves as a complete conversational frontend integrating continuous perception, conversational control, and native speech generation through a shared causal timeline for user inputs, model outputs, and delegation events.
- A dual-loop runtime coordinates live interaction with background reasoning and tool execution: foreground interaction continues while Realtime-Venus-Harness executes tasks asynchronously and returns results into the ongoing dialogue.
- Both models follow a common post-training recipe combining offline understanding, proactive full-duplex trajectories, and delegation workflows.
- Realtime-Venus-Omni achieves the highest scores among evaluated online models on six of eight video benchmarks, including StreamingBench (70.2%), OVO-Bench (64.7%), and Daily-Omni (81.3%).
- Realtime-Venus-Audio leads compared models on MMAU (78.0%), MMAU-Pro (63.2%), Llama Questions (83.8%), and Speech CMMLU (67.8%), while matching the best VoiceBench AlpacaEval score of 4.81.
- On Full-Duplex-Bench v1.5, Realtime-Venus-Audio responds to 75% of user interruptions and achieves continuation rates of 97%, 88%, and 86% under backchannels, other-directed speech, and background speech, exceeding Gemini 3.1 Live and GPT-4o on all three continuation metrics.
---
## Title and framing
**Covers:** title block, authors, and opening motivation (chunk lines 1–10)

> "Realtime-Venus: A full-duplex interaction system with asynchronous delegation"
> "Venus Team, Ant Group"
> "Tsinghua University"

> "Natural interaction in digital and physical environments requires continuous perception and timely responses. Spoken dialogue relies on acoustic and linguistic cues, while video interaction also requires grounding the conversation in evolving visual context."

Source identifier in chunk: "arXiv:2609.13814v2 [cs.CV] 18 Sep 2026".

## Models and runtime
**Covers:** system definition: two 9B frontends, shared causal timeline, dual-loop runtime (chunk lines 13–21)

> "We present Realtime-Venus, a proactive full-duplex interaction system with two separately trained 9B models: Realtime-Venus-Omni for audio–visual interaction and Realtime-Venus-Audio for spoken interaction."

| Element | Chunk statement |
|---|---|
| Realtime-Venus-Omni | 9B model for audio–visual interaction; complete conversational frontend |
| Realtime-Venus-Audio | 9B model for spoken interaction; complete conversational frontend |
| Shared causal timeline | Covers user inputs, model outputs, and delegation events; integrates continuous perception, conversational control, and native speech generation |
| Dual-loop runtime | Coordinates live interaction with background reasoning and tool execution |
| Realtime-Venus-Harness | Executes tasks asynchronously while foreground interaction continues; returns results for integration into the ongoing dialogue |

> "Each model serves as a complete conversational frontend, integrating continuous perception, conversational control, and native speech generation through a shared causal timeline for user inputs, model outputs, and delegation events."
> "A dual-loop runtime coordinates live interaction with background reasoning and tool execution. Foreground interaction continues while Realtime-Venus-Harness executes tasks asynchronously and returns results for integration into the ongoing dialogue."

Post-training (chunk line 20–21):

> "Both models follow a common post-training recipe combining offline understanding, proactive full-duplex trajectories, and delegation workflows."

## Benchmark highlights
**Covers:** reported results: video, audio, and full-duplex benchmarks (chunk lines 22–31)

Video (Realtime-Venus-Omni, among evaluated online models):

| Benchmark | Score |
|---|---|
| StreamingBench | 70.2% |
| OVO-Bench | 64.7% |
| Daily-Omni | 81.3% |

Scope claim: "highest scores on six of eight video benchmarks".

Audio (Realtime-Venus-Audio, across eight audio understanding and spoken question answering benchmarks):

| Benchmark | Score |
|---|---|
| MMAU | 78.0% |
| MMAU-Pro | 63.2% |
| Llama Questions | 83.8% |
| Speech CMMLU | 67.8% |
| VoiceBench AlpacaEval | 4.81 (matching the best) |

Full-duplex (Realtime-Venus-Audio on Full-Duplex-Bench v1.5):

| Condition | Rate |
|---|---|
| Responds to user interruptions | 75% |
| Continuation under backchannels | 97% |
| Continuation under other-directed speech | 88% |
| Continuation under background speech | 86% |

Comparison claim: "exceeding Gemini 3.1 Live and GPT-4o on all three continuation metrics."

## Links and figure fragment
**Covers:** project/code links and garbled benchmark-figure text (chunk lines 33–70)

- Project: https://realtime-venus.github.io/
- Code: https://github.com/inclusionAI/Realtime-Venus
- Figure file named in chunk: "combined-benchmark-radars.svg", dated "2026/9/11 17:55", with panel titles "Streaming & Offline Benchmark Comparison" and "Audio Benchmark Comparison".
- Remaining figure text in the chunk (lines 38–70) is garbled SVG fragments (e.g., "StreamingBench", "OVO-Bench", "MMAU", "MMAU-Pro", "Speech CMMLU") without complete sentences; no additional factual claims are extracted from it.

**Covers:** chunk 01-realtime-venus-a-full-duplex-interaction-system (title page, abstract-level system description, and benchmark headline numbers)
