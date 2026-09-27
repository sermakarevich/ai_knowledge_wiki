---
type: Paper
title: "FormBharo: Designing and Evaluating a Voice Agent for Conversational Form Filling in Rural India"
description: Hybrid Hindi voice agent pairing LLM extraction and reply with rule-based validation to fill a 12-field maternal-health enrollment form by phone, plus the 3,760-test FormVoiceAgentBench showing end-to-end testing is required because real-speech errors cut completion by up to ~41 points.
generated: { by: claude/opencode-go/muse-spark-1.3-contributor, at: 2026-09-22T09:39:14Z }
sources:
  - id: original
    resource: https://arxiv.org/abs/2608.06027
  - id: local-copy
    resource: source/source.md
tags: [voice-agents, speech-recognition, low-resource-hci, llm-evaluation, form-filling]
---

# FormBharo: Designing and Evaluating a Voice Agent for Conversational Form Filling in Rural India

FormBharo ("fill the form" in Hindi) is a hybrid voice agent piloted with ARMMAN to enroll low-income Hindi-speaking mothers in maternal care over a phone call, pairing LLM extraction and reply with deterministic validation, retries, and branching. Its headline lesson is that component accuracy does not predict form completion: real-speech transcripts cut completion by up to ~41 points and reorder model rankings, so the deployable configuration (Scribe v2, Gemini 3.5 Flash, GPT-5.4-mini) emerges only from end-to-end Pareto-filtered evaluation on the released FormVoiceAgentBench.

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
| [[wiki/01-introduction-and-motivation\|Introduction and Motivation]] | Literacy barrier, worker burden, voice precedent, hybrid overview, benchmark and end-to-end claim |
| [[wiki/02-system-architecture\|System Architecture: Hybrid LLM plus Rule-Based Pipeline]] | VAD/STT/EXTRACT/rule-layer/REPLY/TTS flow, retries, branching, interruption handling, Pareto selection |
| [[wiki/03-benchmark-form-and-users\|Benchmark Form and Simulated Users]] | 12-field form, skip/end semantics, 5 users, 4 acoustic conditions, 960 calls, 1,880 unit tests per LLM |
| [[wiki/04-evaluation-and-results\|Evaluation and model selection: STT, extraction, form completion, and reply]] | LLM-WER STT ranking, extraction saturation and reordering, completion gaps, EXTRACT/REPLY selection |
| [[wiki/05-reply-generation-and-examples\|Reply generation and examples: enrollment flow and EXTRACT judges]] | Full call flow, Hindi scripts, EXTRACT field and acknowledgement/name judge criteria |
| [[wiki/06-appendix-call-flow-and-setup\|Appendix: Call Flow and Setup]] | Agent-first flow, retry/skip rules, Aadhaar last-4, five REPLY judges, calibration, STT cost table |
| [[wiki/07-appendix-detailed-tables\|Appendix: Detailed Tables — Per-Turn Extraction Accuracy and Model Selection]] | Tables 10–13, per-turn vs completion accuracy, latency/cost, weighting sweep, determinism notes |

## Original Source

- [arXiv:2608.06027](https://arxiv.org/abs/2608.06027) — original paper page
- [source/source.md](source/source.md) — local copy of the source text
