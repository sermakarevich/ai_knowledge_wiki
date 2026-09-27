---
type: index
title: Benchmarking Prompt Engineering Techniques for
description: Folder index for the Benchmarking Prompt Engineering Techniques for Secure Code Generation with GPT Models paper folder
generated:
  by: claude/muse-spark-1.3-contributor
  at: 2026-09-23T20:09:29Z
sources:
  - id: original
    resource: https://arxiv.org/abs/2502.06039v1
  - id: local-copy
    resource: source/source.md
tags: [prompt-engineering, secure-code-generation, LLM-evaluation, static-analysis]
---

# Benchmarking Prompt Engineering Techniques for

This folder summarises the paper "Benchmarking Prompt Engineering Techniques for Secure Code Generation with GPT Models" (Bruni et al.), which benchmarks prefix/suffix prompts, RCI, and chain-of-thought over 202 high-risk Python prompts on GPT-3.5-turbo, GPT-4o-mini, and GPT-4o. Start with the summary for the headline numbers (security prefix −47–56%, RCI −24–65%), then use the digest and wiki pages for per-section evidence and the explainer, critical analysis, and retrieval questions for depth.

## How to work through this

1. Read [summary](summary.md) (~2 min) for the TL;DR, key findings, and takeaways.
2. Read [digest](digest.md) (~10 min) for the chunk-by-chunk argument in nine moves plus the five-move arc.
3. Deep-dive into [wiki pages](#wiki) for verbatim evidence, then [explainer](explainer.md), [critical thinking](critical_thinking.md), and [questions](questions.md) to test understanding.

## Read This Folder

- [Summary](summary.md) — TL;DR, problem, ideas, findings, future directions.
- [Digest](digest.md) — nine chunk summaries with verbatim key points plus the five-move argument.
- [Explainer](explainer.md) — plain-language walkthrough of the benchmark, results, and trade-offs.
- [Critical thinking](critical_thinking.md) — claims vs. evidence, novelty, weaknesses, applicability, verdict.
- [Questions](questions.md) — 13 retrieval-practice Q&A covering every wiki page.

## Wiki

| Page | Covers |
|---|---|
| [01 — Benchmarking Prompt Engineering Techniques for Secure Code Generation with GPT Models](wiki/01-benchmarking-prompt-engineering-secure-code.md) | Title, authors, affiliations, and abstract gap (truncated chunk) |
| [02 — Related Work and Benchmark Design](wiki/02-related-work-and-benchmark-design.md) | Research question, prior vulnerability rates, 202-prompt dataset, generation setup |
| [03 — Models, Cost, and Code Extraction](wiki/03-models-cost-and-code-extraction.md) | GPT-3.5/4o-mini/4o range, tiktoken cost estimates, regex plus AST extraction loop |
| [04 — Experiment Setup and Metrics](wiki/04-experiment-setup-and-metrics.md) | Pinned snapshots, retry bounds, Semgrep+CodeQL scan, SAFVS/OFVP metrics |
| [05 — Results — GPT-3.5-turbo](wiki/05-results-gpt-3-5-turbo.md) | Proactive prompts backfire; only RCI helps (24.5% iter-1, 41.9% by iter-3) |
| [06 — Results — GPT-4o-mini](wiki/06-results-gpt-4o-mini.md) | Prefix −47% and RCI table topping at −61.2% stacked; pe-negative +127.7% |
| [07 — GPT-4o Results and Cross-Model Comparison](wiki/07-results-gpt-4o-and-comparison.md) | GPT-4o prefix −56%, RCI −64.7%, stacked −68.7%; sensitivity grows with capability |
| [08 — Result Figures and Distributions](wiki/08-result-figures-and-distributions.md) | Garbled Fig. 6 extraction; records the gap, no invented numbers |
| [09 — Discussion, Prompt Agent, Threats to Validity and Conclusion](wiki/09-discussion-prompt-agent-conclusion.md) | Prompt Agent (prefix + RCI), validity threats, conclusion numbers |

## Original Source

- arXiv: [Benchmarking Prompt Engineering Techniques for Secure Code Generation with GPT Models](https://arxiv.org/abs/2502.06039v1)
- Local copy: [source/source.md](source/source.md)
