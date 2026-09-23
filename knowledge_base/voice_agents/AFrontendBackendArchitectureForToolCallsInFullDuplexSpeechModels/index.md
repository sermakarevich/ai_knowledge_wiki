---
type: Paper
title: "A frontend-backend architecture for tool calls in full-duplex speech models"
description: Modular split giving duplex speech-to-speech interaction strong agentic tool use without internalizing it — a duplex speech-to-text frontend emits a delegation token pair (<tc bos>/<tc eos>) plus filler, routes the endpointed ASR transcript to a LangGraph ReAct text backend, and repeats the prefilled natural-language answer aloud, reaching 92–97% delegation recall, 81.2% irrelevance rejection, and ~74.6% spoken BFCL average.
generated: { by: claude/muse-spark-1.3-contributor, at: 2026-09-20T10:46:13Z }
sources:
  - id: original
    resource: https://arxiv.org/pdf/2609.19334
  - id: local-copy
    resource: source/source.md
tags: [speech-agents, tool-use, full-duplex, backend-delegation]
---

# A frontend-backend architecture for tool calls in full-duplex speech models

Ke Hu et al. (NVIDIA) split the voice-agent job in two: a fast duplex speech-to-text frontend owns natural turn-taking and learns a minimal delegation-token protocol, while a mature LangGraph ReAct text backend owns multi-round tool execution and multi-turn state. The frontend signals tool need with `<tc bos>`/`<tc eos>`, stays silent during the call, then repeats the backend's prefilled answer as if it knew it all along — staying warm and responsive while borrowing a much stronger model's brains.

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
| [[wiki/01-frontend-backend-architecture\|A Frontend-Backend Architecture for Tool Calls]] | Paper title/abstract framing: duplex speech frontend delegating tool calls to a text backend (source chunk garbled; substantive detail lives in later pages) |
| [[wiki/02-background-related-work\|Background and Related Work: Why Delegate Tool Calls to a Backend]] | Sect. 1 motivation and τ-Voice capability gap, internalize-vs-delegate design choice, concurrent hybrids (KAME, MoshiRAG, Thinking Machines, Qwen-audio-agent, GPT-Live), cascaded systems, architecture sketch, headline evaluation claims |
| [[wiki/03-architecture-training-results\|Architecture, Training and Results: STT Frontend, LangGraph Backend, Tool-Call Delegation]] | Sec. 3 frontend delegation tokens and LangGraph backend, Sec. 4 training/inference data pipeline, Sec. 5 BFCL / Full-Duplex-Bench-V3 / EVA-Bench / turn-taking results, Sec. 6 conclusion |

## Original Source

- [https://arxiv.org/pdf/2609.19334](https://arxiv.org/pdf/2609.19334) — original paper PDF (Ke Hu et al., NVIDIA)
- [source/source.md](source/source.md) — local copy of the paper text
