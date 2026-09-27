---
type: index
title: Towards Practical and Useful Automated Program Repair for Debugging — Index
description: Folder index for the PracAPR vision paper (SE 2030): test-free interactive repair from debugger state, ROSE results, LLM local repair, and multi-location global repair.
generated:
  by: claude/muse-spark-1.3-contributor
  at: 2026-09-23T21:34:23Z
sources:
  - id: original
    resource: https://arxiv.org/abs/2407.08958v1
  - id: local-copy
    resource: source/source.md
tags: [automated-program-repair, debugging, fault-localization, llm-repair]
---

# Towards Practical and Useful Automated Program Repair for Debugging

This folder summarises the SE 2030 vision paper proposing PracAPR, an interactive IDE repair system that starts from a debugger-suspended program instead of a test suite. Start with the two-minute summary, deepen with the ten-minute digest, then use the wiki pages for section-level detail and the explainer, critical analysis, and retrieval questions for learning and review.

## How to work through this

1. Read [summary.md](summary.md) (~2 min) for the TL;DR, problem, ideas, findings, and future directions.
2. Read [digest.md](digest.md) (~10 min) for the section-by-section argument in six verbatim blocks plus the five-move arc.
3. Deep-dive the wiki pages in order ([01](wiki/01-motivation-and-pracapr-vision.md) → [06](wiki/06-references-tail.md)) for evidence, numbers, and the Chart_3 and taxonomy details.
4. Use [explainer.md](explainer.md) for plain language, [critical_thinking.md](critical_thinking.md) for claims-vs-evidence scrutiny, and [questions.md](questions.md) for retrieval practice.

## Read This Folder

- [Summary](summary.md) — two-minute TL;DR and full-paper overview.
- [Digest](digest.md) — ten-minute section-by-section digest with the argument in five moves.
- [Explainer](explainer.md) — plain-language walkthrough with jargon decoder.
- [Critical thinking](critical_thinking.md) — claims vs. evidence, novelty, weaknesses, verdict.
- [Questions](questions.md) — ten retrieval-practice questions covering every wiki page.

## Wiki table

| Page | Covers |
|---|---|
| [01](wiki/01-motivation-and-pracapr-vision.md) | Motivation: debugging cost, APR families, test-suite and re-execution assumptions, and the PracAPR vision statement |
| [02](wiki/02-pracapr-architecture-and-pipeline.md) | PracAPR pipeline (Figure 1): problem specification, test-free flow-analysis fault localization, local plus global generation, simulated-trace validation, preview |
| [03](wiki/03-rose-interactive-test-free-framework.md) | ROSE framework: preview interaction, 89% localization / top-5 validation, 36/40 QuixBugs and 37/60 Defects4J in seconds, user study, two PracAPR upgrades |
| [04](wiki/04-llm-based-local-repair.md) | LLM local repair: Chart_3 minY/maxY misdiagnosis vs. augmented prompt, ambiguity mitigations, single-fault multi-location framing with 118 bugs and 8 relationships |
| [05](wiki/05-global-repair-strategies.md) | Bibliography entries [1]–[47] on APR, fault localization, LLMs, and empirical studies (file body is references; filename slug implies global-repair strategies) |
| [06](wiki/06-references-tail.md) | Bibliography entries [48]–[55]: Nopol, patch-correctness data, ITER, evolutionary repair, surveys, ensemble and syntax-guided repair |

## Original Source

- arXiv: [Towards Practical and Useful Automated Program Repair for Debugging](https://arxiv.org/abs/2407.08958v1)
- Local copy: [source/source.md](source/source.md)
