---
type: Paper
title: "AVTR-1: Open Stack for Real-Time Interactive Avatars"
description: Open stack for live interactive avatars — a 153M-parameter dyadic flow-matching motion model, a real-time TensorRT renderer, and a worklet-based streamer with derived latency bounds — plus the R-DGG metric proving listening depends on speaker speech.
generated: { by: claude/muse-spark-1.3-contributor, at: 2026-09-22T16:00:00Z }
sources:
  - id: original
    resource: http://arxiv.org/abs/2609.22913v1
  - id: local-copy
    resource: source/source.md
tags: [talking-heads, dyadic-motion, real-time-serving, latency-model, r-dgg]
---

# AVTR-1: Open Stack for Real-Time Interactive Avatars

Kravtsov, Ziganshin, Poletaev et al. (Avaturn Live) build the full live-avatar loop: a compact dyadic motion model that watches both speakers, a renderer that paints motion onto a portrait in real time, and a streamer that serves the call with derived, measured delay bounds — plus a new test proving the avatar's listening actually tracks your speech.

## How to work through this

Three depths — stop at whichever answers your question:

1. **[[summary|Summary]]** (~2 min) — the whole thing, shallow.
2. **[[digest|Digest]]** (~10 min) — the whole thing, medium: every section's headline and key points.
3. **Wiki pages below** (~5 min each) — one section, deep. Each opens with its headline and key points, so you can stop early.

_New to the field? Start with [[explainer|the plain-language explainer]] instead. Coming back after a break? Read [[digest|the digest]], then [[questions|self-test]] — do not re-read the wiki._

## Read This Folder

- [[summary|Summary]] — rung 1: the whole source, shallow
- [[digest|Digest]] — rung 2: the whole source at medium depth; the file to re-read on review
- [[explainer|Plain-Language Explainer]] — no-jargon explanation, applications, conclusions
- [[critical_thinking|Critical Analysis]] — claims vs. evidence, applicability, what it changes, verdict
- [[questions|Retrieval Practice]] — self-test questions; **answer these from memory before re-reading anything**

## Wiki

| Page | Covers |
|------|--------|
| [[wiki/01-avtr-1-overview-and-introduction\|AVTR-1 overview and introduction]] | Paper framing, contributions, and the interactive-avatar problem statement |
| [[wiki/02-motion-representation-and-model-architecture\|Motion representation and model architecture]] | LivePortrait motion representation and the flow-matching Transformer architecture |
| [[wiki/03-data-pipeline-and-training-procedure\|Data pipeline and training procedure]] | Dyadic data pipeline, speaker separation, and the training procedure |
| [[wiki/04-chunk-based-audio-encoder-and-distillation\|Chunk-based audio encoder and distillation]] | Streaming chunk-based HuBERT audio encoder via self-distillation |
| [[wiki/05-streamer-architecture-and-stream-clock\|Streamer architecture and stream clock]] | Streamer serving architecture, worklets, and the shared stream clock |
| [[wiki/06-renderer-and-rendering-worklet\|Renderer and rendering worklet]] | Renderer inference component and the rendering worklet loop |
| [[wiki/07-speech-schedulers-and-latency-model\|Speech schedulers and latency model]] | Speech schedulers and the response/interruption latency analysis |
| [[wiki/08-evaluation-protocol-and-r-dgg-metric\|Evaluation protocol and R-DGG metric]] | Evaluation protocol and the Reference-Based Directed Granger Gain metric |
| [[wiki/09-quantitative-results\|Quantitative results]] | Quantitative comparisons on visual quality, lip sync, and listening motion |
| [[wiki/10-references-and-further-reading\|References and further reading]] | Cited references and pointers for further reading |
| [[wiki/11-appendix-additional-evaluation\|Appendix additional evaluation]] | Appendix tables and additional evaluation details |

## Original Source

- [http://arxiv.org/abs/2609.22913v1](http://arxiv.org/abs/2609.22913v1) — original paper (Kravtsov et al., Avaturn Live)
- [source/source.md](source/source.md) — local copy of the paper text
