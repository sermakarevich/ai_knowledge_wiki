---
type: index
title: "JEV-as-a-Judge: Accept When Confident, Escalate When Unsure | alphaXiv"
description: "Folder index for the JEV-as-a-Judge paper: cheap decision-only judge with confidence-gated escalation to a strong LLM judge."
generated:
  by: claude/muse-spark-1.3-contributor
  at: 2026-09-25T09:24:34Z
sources:
  - id: original
    resource: https://www.alphaxiv.org/abs/2609.26550
  - id: local-copy
    resource: source/source.md
tags: [llm-as-judge, confidence-cascade, evaluation-cost, selective-prediction]
---

# JEV-as-a-Judge: Accept When Confident, Escalate When Unsure | alphaXiv

This folder distils the alphaXiv paper on TypeSafe JEV, a cheap decision-only judge that handles routine preference comparisons and escalates uncertain cases to a stronger model. The headline result is a frozen cascade keeping ~99% of GPT-6 Astra's accuracy at roughly half its fee. Start with the summary, then the digest, then the wiki pages for the full evidence.

## How to work through this

1. **Summary (~2 min)** — the TL;DR, problem, main ideas, and key findings.
2. **Digest (~10 min)** — the argument in five moves plus verbatim key points per wiki page.
3. **Wiki pages** — deep dives with measurements, tables, and caveats; use the explainer for plain-language background, critical_thinking for claims-vs-evidence scrutiny, and questions for retrieval practice.

## Read This Folder

- [Summary](summary.md) — TL;DR, problem and motivation, main ideas, key findings.
- [Digest](digest.md) — condensed key points and the argument in five moves.
- [Explainer](explainer.md) — plain-language walkthrough: what, why, how, where to use.
- [Critical thinking](critical_thinking.md) — claims vs evidence, novelty, weaknesses, applicability.
- [Questions](questions.md) — retrieval-practice questions with answers.

## Wiki table

| Page | Covers |
|------|--------|
| [01](wiki/01-abstract.md) | Paper abstract; cheap first-pass results on RewardBench/JudgeBench/RM-Bench; confidence routing signal; frozen cascade test |

## Original Source

- Online: [JEV-as-a-Judge: Accept When Confident, Escalate When Unsure](https://www.alphaxiv.org/abs/2609.26550)
- Local copy: [source/source.md](source/source.md)
