---
type: Paper
title: "Meta-Harness: End-to-End Optimization of Model Harnesses"
description: An agentic outer-loop system that searches over LLM harness code by giving a coding-agent proposer full filesystem access to every prior candidate's source, scores, and execution traces, beating hand-engineered and text-optimizer baselines on classification, math reasoning, and agentic coding.
generated: { by: claude/claude-sonnet-5, at: 2026-08-26T07:20:00Z }
sources:
  - id: original
    resource: https://arxiv.org/abs/2603.28052
  - id: local-copy
    resource: source/2603.28052.pdf
tags: [llm-agents, prompt-optimization, harness-engineering, agentic-coding]
---

# Meta-Harness: End-to-End Optimization of Model Harnesses

This paper argues that the "harness" wrapped around an LLM — the code deciding what it stores, retrieves, and sees — matters as much as the model weights, yet is still hand-engineered. It introduces Meta-Harness, a system that automates harness engineering by giving a coding-agent proposer unrestricted filesystem access to the full history of every prior harness candidate's source code, scores, and raw execution traces, then lets it repeatedly propose, evaluate, and improve harnesses. Discovered harnesses beat both hand-designed systems and prior automatic text optimizers on text classification, retrieval-augmented math reasoning, and agentic coding (TerminalBench-2).

## How to work through this

Three depths — stop at whichever answers your question:

1. **[[summary|Summary]]** (~2 min) — the whole thing, shallow.
2. **[[digest|Digest]]** (~10 min) — the whole thing, medium: every chapter's headline and key points.
3. **Wiki pages below** (~10-15 min each) — one chapter, deep. Each opens with its headline and key points, so you can stop early.

_New to the field? Start with [[explainer|the plain-language explainer]] instead. Coming back after a break? Read [[digest|the digest]], then [[questions|self-test]] — do not re-read the wiki._

## Read This Folder

- [[summary|Summary]] — rung 1: the whole source, shallow
- [[digest|Digest]] — rung 2: the whole source at medium depth; the file to re-read on review
- [[explainer|Plain-Language Explainer]] — no-jargon explanation, applications, conclusions
- [[critical_thinking|Critical Analysis]] — claims vs. evidence, applicability, what it changes, verdict
- [[questions|Retrieval Practice]] — self-test questions; **answer these from memory before re-reading anything**
- [[connections|Connections]] — related entries in this knowledge base

## Wiki

| Page | Covers |
|------|--------|
| [[wiki/01-motivation-and-related-work\|Motivation and Related Work]] | Why harnesses matter as much as models, why prior text optimizers can't automate harness engineering, headline results (Figs. 1-2), and positioning vs. external-memory, code-search, and text-optimization literatures |
| [[wiki/02-method\|The Meta-Harness Method]] | The formal harness-optimization objective, the propose-evaluate-store loop, Algorithm 1, why code-space search regularizes well, and practical implementation (Claude Code proposer, 60 harnesses/20 iterations) |
| [[wiki/03-classification-and-reasoning-experiments\|Classification and Reasoning Experiments]] | Online text classification vs. ACE/MCE and text optimizers (Figs. 3), OOD generalization to 9 datasets, and retrieval-augmented math reasoning across 5 held-out models |
| [[wiki/04-coding-experiments-and-discussion\|Agentic Coding Experiments and Discussion]] | TerminalBench-2 results on Opus 4.6 and Haiku 4.5, qualitative proposer behavior, and the Section 5 discussion (transfer, inspectability, limitations) |
| [[wiki/05-appendix-case-studies\|Appendix: Case Studies and Discovered Harnesses]] | The full search-trajectory case study (Figs. 4), the discovered draft-verification/label-primed classifiers (Figs. 5-7), the math retrieval router (Fig. 8), the TerminalBench bootstrapping harness (Fig. 9), dataset details, practical tips, and extended related work |

## Original Source

- [source/2603.28052.pdf](source/2603.28052.pdf) — PDF, retrieved 2026-08-26
