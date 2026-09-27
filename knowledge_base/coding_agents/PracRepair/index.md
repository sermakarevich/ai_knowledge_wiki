---
type: index
title: 'PracRepair: LLM-Empowered Automated Program Repair Inspired by Human-Like Debugging Practices'
description: Folder index for the PracRepair paper — orientation, reading order, and links to summary, digest, wiki pages, and original source.
generated:
  by: claude/muse-spark-1.3-contributor
  at: '2026-09-23T20:38:40Z'
sources:
  - id: original
    resource: https://arxiv.org/abs/2606.17612v1
  - id: local-copy
    resource: source/source.md
tags: [automated-program-repair, llm, debugging, defects4j]
---

# PracRepair: LLM-Empowered Automated Program Repair Inspired by Human-Like Debugging Practices

PracRepair is an LLM-based automated program repair framework that mirrors human debugging: on-demand static-dynamic context, question-driven diagnosis, and feedback-guided patch refinement. It fixes substantially more Defects4J bugs than prior methods while costing less per fixed bug. Use this folder to go from a 2-minute overview to detailed per-section evidence.

## How to work through this

1. Start with `summary.md` (~2 min) for the TL;DR, problem, ideas, findings, and future directions.
2. Read `digest.md` (~10 min) for 13 verbatim section digests plus the five-move argument.
3. Dive into `wiki/` pages for full per-section evidence, then `explainer.md` for plain language, `critical_thinking.md` for claims-vs-evidence scrutiny, and `questions.md` for retrieval practice.

## Read This Folder

- [Summary](summary.md) — TL;DR, problem, ideas, findings, future directions.
- [Digest](digest.md) — 13 verbatim section digests and the argument in five moves.
- [Explainer](explainer.md) — plain-language walkthrough.
- [Critical thinking](critical_thinking.md) — claims vs. evidence and validity analysis.
- [Questions](questions.md) — retrieval-practice questions covering every wiki page.

## Wiki

| Page | Covers |
| ---- | ------ |
| [01 Introduction and Context](wiki/01-introduction-and-context.md) | Proposal, motivation cost figures, and headline Defects4J/RWB results |
| [02 Limitations of Prior APR](wiki/02-limitations-of-prior-apr.md) | Missing failure-execution/patch-validation dynamics and challenges C1–C3 |
| [03 Motivating Example: Static Repair](wiki/03-motivating-example-static-repair.md) | Compress-21 `writeBits` bug info and the static-only repair attempt |
| [04 Dynamic Traces and Diagnosis](wiki/04-dynamic-traces-and-diagnosis.md) | Why static-only fails; trace, diagnosis, and trace-diff path to passing fix |
| [05 Framework Overview: Three Stages](wiki/05-framework-overview-three-stages.md) | Diagnosis/refinement loops, Joern CPG, JavaAgent/ASM traces, on-demand interface |
| [06 Static-Dynamic Context Construction](wiki/06-static-dynamic-context-construction.md) | What/why/how questions, QA history, and four-field repair hypothesis |
| [07 Question-Driven Diagnosis and Refinement](wiki/07-question-driven-diagnosis-and-refinement.md) | Zero-shot generation, 10-minute validation, four failure types, diff feedback |
| [08 Evaluation Design and RQ1](wiki/08-evaluation-design-and-rq1.md) | Models, budgets, hardware, baselines, plausible-vs-correct metrics |
| [09 Main Repair Results](wiki/09-main-repair-results.md) | Defects4J correct counts, unique fixes, cross-project and no-PFL results |
| [10 Generalization, RWB, Ablation, Costs](wiki/10-generalization-rwb-results.md) | SL/SH/SF/MF scenarios, ablations, refinement rounds, RWB, per-bug cost |
| [11 Ablation and RQ3](wiki/11-ablation-and-rq3.md) | RQ3/RQ4 answers, RWB generalization, internal and external threats |
| [12 Related Work](wiki/12-related-work.md) | Retrieval pipelines, learning-based, one-shot/iterative/agent LLM repair |
| [13 Conclusion and References](wiki/13-conclusion-and-references.md) | Bibliography tail [24]–[61] and cited LLM/classic repair works |

## Original Source

- arXiv: [PracRepair: LLM-Empowered Automated Program Repair Inspired by Human-Like Debugging Practices](https://arxiv.org/abs/2606.17612v1)
- Local copy: [source/source.md](source/source.md)
