---
type: Paper
title: ReAct: Synergizing Reasoning and Acting in Language Models
description: Interleaves free-form language thoughts with task actions so LLM agents plan, track, and adjust while grounding reasoning in retrieved facts, beating CoT hallucination and Act-only myopia on QA, fact-checking, and embodied/web decision-making.
generated: { by: claude, at: 2026-09-12T06:44:00Z }
sources:
  - id: original
    resource: https://arxiv.org/abs/2210.03629
  - id: local-copy
    resource: source/full.md
tags: [llm-agents, reasoning, tool-use, prompting, decision-making]
---

# ReAct: Synergizing Reasoning and Acting in Language Models

ReAct (Yao et al., Princeton + Google Research) augments an LLM agent's action space with free-form "thoughts" interleaved with task actions, so reasoning guides acting (plan, track progress, handle exceptions) and acting grounds reasoning (retrieve external facts). With just 1–6 in-context examples on frozen PaLM-540B and GPT-3, it stays competitive with chain-of-thought on HotpotQA/FEVER while far more grounded, and beats imitation/RL baselines trained on 10^3–10^5 instances by +34% absolute on ALFWorld and +10% on WebShop.

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
- [[connections|Connections]] — related entries in this knowledge base

## Wiki

| Page | Covers |
|------|--------|
| [[wiki/01-react-method\|ReAct method: reason+act interleaving]] | Action-space formalism, thought repertoire, motivation, headline results, design claims |
| [[wiki/02-experiments-results\|Knowledge-intensive and decision-making experiments]] | GPT-3 vs PaLM-540B, up-to-date knowledge retrieval, human thought-editing, finetuning, verbatim prompts |
| [[wiki/03-appendices-trajectories\|Appendices: prompts, trajectories, analysis]] | Full FEVER/ALFWorld/WebShop trajectories, ReAct-IM ablation, success/failure-mode taxonomy |

## Original Source

- [source/full.md](source/full.md) — full paper text, retrieved from arXiv:2210.03629v3 [cs.CL]
