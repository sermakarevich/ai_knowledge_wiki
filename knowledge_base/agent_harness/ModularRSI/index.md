---
type: Paper
title: 'ModularRSI: Modular and Generalizable Recursive Harness Self-Improvement'
description: Benchmark-disjoint, contrastive, modular framework that evolves five agent-harness modules independently for generalizable self-improvement on terminal and software-engineering tasks.
generated: { by: claude/muse-spark-1.3-contributor, at: 2026-09-21T05:49:00Z }
sources:
  - id: original
    resource: https://arxiv.org/pdf/2609.14857
  - id: local-copy
    resource: source/source.md
tags: [recursive-self-improvement, agent-harness, software-engineering-agents, terminal-bench]
---

# ModularRSI: Modular and Generalizable Recursive Harness Self-Improvement

ModularRSI (Wu et al., arXiv 2609.14857, 14 Sep 2026) improves coding-agent harnesses — the loop, tool, observation, context, and completion machinery around the language model — by evolving them on 2,000 benchmark-disjoint tasks. It contrasts same-task success and failure trajectories to localize reusable fixes, evolves each of five modules independently with validation gates, then integrates them. The frozen harness gains on TerminalBench 2.0 and SWE-Bench Verified, transfers across domains and models, and beats joint and non-modular evolution.

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
| [[wiki/01-introduction-abstract\|Abstract and Introduction]] | Three RSI blockers, ModularRSI proposal, five modules, 2,000-task protocol, headline gains |
| [[wiki/02-related-work-comparison\|Related Work and Comparison]] | Prior self-evolving frameworks, Table 1 comparison, monolithic vs modular gap |
| [[wiki/03-contrastive-trajectory-analysis\|Contrastive Trajectory Analysis and Trajectory Memory]] | Trajectory Memory, Contrastive/Negative/Positive groups, voting, validation gates |
| [[wiki/04-evolution-dataset-protocol\|Experiment Setting and Generalization Results]] | Benchmarks, metrics, setup, in-domain, cross-domain, cross-model, modularity wins |
| [[wiki/05-experimental-results\|Contrastive Analysis, Data Quality, and Conclusion]] | Contrastive-pair ratio trend, medium-difficulty curation, limitations, conclusion |
| [[wiki/06-module-wise-evolution\|Agent Loop Five-Module Harness Architecture]] | Five-module architecture, Agent Loop coordination, normal iteration, completion logic |
| [[wiki/07-appendix-function-interfaces\|Function Interfaces and Analysis Schema]] | Per-module function signatures, Table 8 routing, Listing 2 findings, prompts C.1–C.4 |
| [[wiki/08-appendix-prompts-integration\|Trajectory Case Studies, Difficulty Curation, Evolution Curve]] | NULL-filter, FFmpeg, Zip Slip cases, difficulty curation, TerminalBench evolution curve |

## Original Source

- [https://arxiv.org/pdf/2609.14857](https://arxiv.org/pdf/2609.14857) — original paper PDF
- [source/source.md](source/source.md) — local copy of the source text
