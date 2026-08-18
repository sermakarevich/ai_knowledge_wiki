---
type: Paper
title: "GoAgent: Group-of-Agents Communication Topology Generation for LLM-based Multi-Agent Systems"
description: Generates multi-agent communication topologies by treating groups of agents — not individual agents — as the atomic unit, and filters inter-group noise with a task-conditioned information bottleneck.
generated: { by: claude/claude-sonnet-5, at: 2026-08-18T09:05:00Z }
sources:
  - id: original
    resource: https://arxiv.org/abs/2603.19677
  - id: local-copy
    resource: source/2603.19677.pdf
tags: [multi-agent-systems, communication-topology, information-bottleneck, graph-generation, autoregressive-generation]
---

# GoAgent: Group-of-Agents Communication Topology Generation for LLM-based Multi-Agent Systems

Existing methods for designing how LLM agents talk to each other build the communication graph one agent at a time (node-centric), which misses natural "divide-and-conquer" team structures and lets task-irrelevant noise pile up in the graph. GoAgent instead treats whole collaborative *groups* of agents as the atomic building block: an LLM first proposes a pool of candidate groups, then a learned autoregressive model selects and wires up groups (not individual agents), with a Conditional Information Bottleneck compressing inter-group signals down to only what the current task needs. It reaches state-of-the-art accuracy (93.84% average across six benchmarks) while cutting token usage by about 17% versus the strongest prior baseline, and it is markedly more robust to a simulated prompt-injection attack.

## How to work through this

Three depths — stop at whichever answers your question:

1. **[[summary|Summary]]** (~2 min) — the whole thing, shallow.
2. **[[digest|Digest]]** (~10 min) — the whole thing, medium: every wiki page's headline and key points.
3. **Wiki pages below** (~5-10 min each) — one section, deep. Each opens with its headline and key points, so you can stop early.

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
|---|---|
| [[wiki/01-problem-and-motivation\|1. Problem and Motivation]] | Node-centric vs. group-centric paradigms; problem formulation; the information bottleneck background |
| [[wiki/02-method\|2. Method]] | Task encoding, group discovery, autoregressive group/edge generation, Conditional Information Bottleneck, training strategy |
| [[wiki/03-experiments-and-related-work\|3. Experiments and Related Work]] | Accuracy across 6 benchmarks, ablations, token efficiency, robustness to attack, case study, related work, conclusion |
| [[wiki/04-appendix-and-implementation\|4. Appendix and Implementation]] | Algorithms, complexity, datasets/baselines, parameter sensitivity, training config, LLM prompt templates |

## Original Source

- [arXiv abstract page](https://arxiv.org/abs/2603.19677)
- Local copy: `source/2603.19677.pdf` (retrieved 2026-08-18)
