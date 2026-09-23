---
type: index
title: "MSI-Bench: Evaluating Multi-Speaker Voice Interaction for Collaborative AI Agents"
description: "Folder index for MSI-Bench: a 1,152-case bilingual multi-speaker voice benchmark testing speaker-scoped memory, instruction following, and reasoning."
generated:
  by: claude/muse-spark-1.3-contributor
  at: 2026-09-22T10:58:53Z
sources:
  - id: original
    resource: http://arxiv.org/abs/2609.24812v1
  - id: local-copy
    resource: source/source.md
tags: [voice-agents, multi-speaker, benchmarking, speaker-attribution, tool-use]
---

# MSI-Bench: Evaluating Multi-Speaker Voice Interaction for Collaborative AI Agents

This folder collects notes on MSI-Bench, a benchmark that moves voice-agent evaluation from single-user assistance to shared multi-speaker collaboration. The paper builds 1,152 bilingual audio scenes and finds even the strongest systems pass all rubrics on only 66.8% of English and 54.5% of Mandarin cases. Start with the summary, then the digest, then the wiki pages for patterns, pipeline, metrics, results, and worked example cases.

## How to work through this (summary ~2 min → digest ~10 min → wiki pages)

1. Read `summary.md` (~2 min) for the TL;DR, taxonomy, pipeline, and headline findings.
2. Read `digest.md` (~10 min) for the section-by-section key points plus the five-move argument.
3. Dive into `wiki/` pages for detail: capability patterns first, then construction and evaluation protocol, then results and example cases; use `questions.md` for retrieval practice.

## Read This Folder

- [Summary](summary.md) — TL;DR, motivation, ideas, findings, future directions.
- [Digest](digest.md) — per-section key points and the argument in five moves.
- [Explainer](explainer.md) — plain-language walkthrough of the benchmark.
- [Critical thinking](critical_thinking.md) — strengths, limits, and open questions.
- [Questions](questions.md) — 14 retrieval-practice Q&As covering every wiki page.

## Wiki

| Page | Covers |
| ---- | ------ |
| [01-overview-motivation](wiki/01-overview-motivation.md) | Title, authors, and abstract fragment (truncated) |
| [02-taxonomy-capability-families](wiki/02-taxonomy-capability-families.md) | Three capability families, six patterns, headline scores |
| [03-instruction-following-patterns](wiki/03-instruction-following-patterns.md) | Selective disclosure, speaker authority, sequential integration, prioritization |
| [04-benchmark-construction-pipeline](wiki/04-benchmark-construction-pipeline.md) | Eight domains, four-stage pipeline, gates, 1,152-case yield |
| [05-evaluation-protocol-metrics](wiki/05-evaluation-protocol-metrics.md) | Table 1 metrics, transcript-lift and speaker-count ablations |
| [06-results-failure-analysis](wiki/06-results-failure-analysis.md) | Headline results, SNR ablation, judge–human agreement, limitations |
| [07-appendix-corpus-statistics](wiki/07-appendix-corpus-statistics.md) | Corpus balance, voice pool, audio assets, compute config |
| [08-example-case-marcus-group](wiki/08-example-case-marcus-group.md) | Background-retrieval eavesdropping cases (patio cutoff, pavilion_7) |
| [09-example-case-scene-context](wiki/09-example-case-scene-context.md) | Selective-disclosure cases (kitchen gift, Mandarin trip) |
| [10-example-case-tyler-mom](wiki/10-example-case-tyler-mom.md) | Speaker-authority cases (Tyler upgrade hold, teacher-Li loan) |
| [11-example-case-maggie-group](wiki/11-example-case-maggie-group.md) | Scope-tracking dinner booking (global vs local bindings) |
| [12-example-case-mandarin-order](wiki/12-example-case-mandarin-order.md) | Mandarin takeout allergy-scope over-expansion case |
| [13-example-tool-calls](wiki/13-example-tool-calls.md) | Attribution (car charging) and prioritization (hospital ward) cases |
| [14-judge-rubrics-human-study](wiki/14-judge-rubrics-human-study.md) | Constraint-prioritization dog-walk case (leash rule vs route) |

## Original Source

- arXiv: [MSI-Bench: Evaluating Multi-Speaker Voice Interaction for Collaborative AI Agents](http://arxiv.org/abs/2609.24812v1)
- Local copy: [source/source.md](source/source.md)
