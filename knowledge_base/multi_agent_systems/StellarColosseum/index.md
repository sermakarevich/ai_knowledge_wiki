---
type: index
title: "Stellar Colosseum: A Many-Agent Harness for Long-Horizon Research in Mathematics and Theoretical Computer Science"
description: "Folder index for the Stellar Colosseum paper — a model-agnostic many-agent harness for long-horizon math and TCS research."
generated:
  by: claude/muse-spark
  at: 2026-09-16T05:04:19Z
sources:
  - id: original
    resource: https://arxiv.org/pdf/2609.15983
  - id: local-copy
    resource: source/source.md
tags: [multi-agent-systems, automated-theorem-proving, inference-scaling, theoretical-computer-science]
---

# Stellar Colosseum: A Many-Agent Harness for Long-Horizon Research in Mathematics and Theoretical Computer Science

Stellar Colosseum is a model-agnostic, many-agent harness that spends inference-time compute on long-horizon mathematics and theoretical computer science (TCS — the study of computation, algorithms, and complexity) research. It explores competing proof strategies, gates when a route is ready, decomposes proofs into parallel section-level subproblems over a dependency graph, and verifies globally with targeted repair. This folder holds a 2-minute summary, a 10-minute digest, eight wiki pages, and retrieval, explainer, and critical-thinking companions.

## How to work through this (summary ~2 min → digest ~10 min → wiki pages)

1. **Summary (~2 min):** read [summary.md](summary.md) for the TL;DR (short for "too long; didn't read" — a one-paragraph gist), the problem and motivation, the main ideas, and the headline results.
2. **Digest (~10 min):** read [digest.md](digest.md) for one-sentence plus key-point condensations of all eight wiki pages and the five-move argument.
3. **Wiki pages (deep dives):** work through `wiki/01` → `wiki/08` in order via the table below; each page states its claims, quotes or paraphrases the source closely, and links back here.
4. **Check yourself:** use [questions.md](questions.md) for retrieval practice (one question per wiki page minimum), [explainer.md](explainer.md) for background, [critical_thinking.md](critical_thinking.md) for objections, and [connections.md](connections.md) for links outward.

## Read This Folder

- [summary.md](summary.md) — 2-minute TL;DR, problem and motivation, main ideas, key findings.
- [digest.md](digest.md) — 10-minute one-sentence plus key-points condensation of every wiki page.
- [explainer.md](explainer.md) — background explainer for non-expert readers.
- [critical_thinking.md](critical_thinking.md) — objections, weak points, and critical appraisal.
- [questions.md](questions.md) — retrieval-practice questions covering every wiki page.
- [connections.md](connections.md) — connections to related work and ideas.

## Wiki table

| Page | Covers |
|---|---|
| [01-overview-and-motivation](wiki/01-overview-and-motivation.md) | What Colosseum is, why long-horizon research motivates it, the two-level architecture, and Antigravity integration |
| [02-strategy-exploration-and-readiness-gate](wiki/02-strategy-exploration-and-readiness-gate.md) | Contributions, related work, strategy exploration loop, and the readiness-gate decision |
| [03-pipeline-context-and-shared-knowledge](wiki/03-pipeline-context-and-shared-knowledge.md) | Cross-stage context, adversarial generation with overlapping tree aggregation, and cross-round shared knowledge |
| [04-inference-configs-and-research-results](wiki/04-inference-configs-and-research-results.md) | Aggregation tree configurations, five new research results, and long-horizon case studies |
| [05-tcs-bench-evaluation](wiki/05-tcs-bench-evaluation.md) | TCS-Bench setup, cross-model selection rule, and 71.0% accuracy results |
| [06-codeforces-limits-and-future-work](wiki/06-codeforces-limits-and-future-work.md) | Codeforces evaluation, adaptive inference allocation, and post-training future directions |
| [07-references-and-related-work](wiki/07-references-and-related-work.md) | References [41]–[65] and Appendix A strategy-exploration prompts |
| [08-appendix-prompts-and-details](wiki/08-appendix-prompts-and-details.md) | Readiness rule for unresolved fatal bridges, decomposition/solver/verifier prompts, and conservative revision |

## Original Source

- ArXiv PDF: [https://arxiv.org/pdf/2609.15983](https://arxiv.org/pdf/2609.15983)
- Local copy: [source/source.md](source/source.md)
