---
type: Paper
title: "PathRouter: Aligning Rewards with Retrieval Quality in Agentic Graph Retrieval-Augmented Generation"
description: A GRPO-based training framework for agentic GraphRAG that routes advantage scaling by a four-way answer-correctness × evidence-overlap taxonomy and adds selective teacher-KL distillation, fixing answer-path reward aliasing and search-update ambiguity.
generated: { by: claude/claude-sonnet-5, at: 2026-08-21T08:45:00Z }
sources:
  - id: original
    resource: https://arxiv.org/abs/2606.16409
  - id: local-copy
    resource: source/source.md
tags: [graphrag, agentic-rag, reinforcement-learning, retrieval]
---

# PathRouter: Aligning Rewards with Retrieval Quality in Agentic Graph Retrieval-Augmented Generation

PathRouter is a training framework for agentic Graph RAG — LLM agents that iteratively query a knowledge graph and reason over the results — that fixes a specific credit-assignment bug in outcome-only reinforcement learning: a correct final answer can hide a completely ungrounded retrieval trajectory, and a wrong answer can follow a well-grounded one. It classifies every training trajectory into one of four answer-correctness × evidence-overlap routes, scales the GRPO advantage differently per route, and adds a selective, token-level teacher-KL signal for the worst trajectories. It's worth ingesting because it directly targets a failure mode (reward aliasing that lets models "cheat" via parametric memory) that plagues most RL-trained retrieval agents, and it backs the claim with six benchmarks, an unusually thorough ablation, and a strong cross-dataset transfer result (95.7% average OOD ratio vs. 70.6–85.8% for prior baselines).

## How to work through this

Three depths — stop at whichever answers your question:

1. **[[summary|Summary]]** (~2 min) — the whole thing, shallow.
2. **[[digest|Digest]]** (~10 min) — the whole thing, medium: every chapter's headline and key points.
3. **Wiki pages below** (~10-15 min each) — one section, deep. Each opens with its headline and key points, so you can stop early.

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
| [[wiki/01-introduction-and-related-work\|Introduction and Related Work]] | The two failure modes (answer-path reward aliasing, search-update ambiguity) and how PathRouter differs from prior GraphRAG, RL retrieval agents, and distillation/routing work |
| [[wiki/02-pathrouter-method\|PathRouter Method]] | Task formulation, the two diagnostic scores (correctness C_i, evidence overlap P_i), four-way route classification, route-conditioned advantage scaling, selective teacher-KL distillation, and the combined training objective |
| [[wiki/03-experimental-setup-and-main-results\|Experimental Setup and Main Results]] | Six-benchmark evaluation protocol, baselines, metrics, and Table 1 main results across three model scales |
| [[wiki/04-experiments-and-main-results\|Ablation, Trajectory Quality, Teacher Scale, and Cross-Dataset Transfer]] | Ablation study (Table 2), routing/trajectory-quality shift (Figure 3), teacher-scale analysis, and the 95.7% cross-dataset OOD transfer result (Figure 4) |
| [[wiki/05-limitations-and-appendix\|Limitations and Appendix]] | Conclusion, acknowledged limitations, metric definitions, hyperparameters, dataset details, KL-selection/threshold-sensitivity analysis, training dynamics, baseline cross-dataset transfer, and three case studies |

## Original Source

- [source/source.md](source/source.md) — provenance pin (PDF binary not copied, 3.4 MB ≥ 2 MB size guard; see file for re-fetch command), retrieved 2026-08-21
