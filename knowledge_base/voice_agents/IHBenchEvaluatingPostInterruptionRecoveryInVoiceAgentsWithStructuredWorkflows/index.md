---
type: index
title: "IHBench: Evaluating Post-Interruption Recovery in Voice Agents with Structured Workflows"
description: "Folder index for IHBench (arXiv:2606.19595) — post-interruption recovery in workflow-driven voice agents across 10 domains, 6 interruption types, and 27 model configurations."
generated:
  by: claude/muse-spark-1.3-contributor
  at: "2026-09-22T07:40:12Z"
sources:
  - id: original
    resource: https://arxiv.org/abs/2606.19595
  - id: local-copy
    resource: source/source.md
tags: [voice-agents, interruption-recovery, llm-evaluation, workflows]
---

# IHBench: Evaluating Post-Interruption Recovery in Voice Agents with Structured Workflows

IHBench measures what a voice agent says *after* a mid-utterance interruption: whether it resumes a state-machine workflow at the correct step. This folder holds a 2-minute summary, a 10-minute digest of all 20 paper chunks, 20 wiki pages, a plain-language explainer, a critical analysis, and retrieval questions.

## How to work through this

1. Read `summary.md` (~2 min) for the TL;DR, problem, ideas, findings, and limits.
2. Read `digest.md` (~10 min) for the per-chunk one-sentence takeaways and key points across all 20 sections.
3. Dive into `wiki/` pages for chunk-level detail, then use `explainer.md`, `critical_thinking.md`, and `questions.md` to check understanding.

## Read This Folder

- [Summary](summary.md) — TL;DR, problem and motivation, ideas, findings, future directions.
- [Digest](digest.md) — one-sentence plus key-points compression of all 20 wiki pages.
- [Explainer](explainer.md) — plain-language walkthrough with examples and jargon decoder.
- [Critical thinking](critical_thinking.md) — claims vs. evidence, novelty, weaknesses, applicability, verdict.
- [Questions](questions.md) — 20 retrieval questions (Q1–Q20), one per wiki page.

## Wiki

| Page | Covers |
|------|--------|
| [01-overview](wiki/01-overview.md) | Benchmark goal, two-axis scoring, 27-config headline results |
| [02-introduction](wiki/02-introduction.md) | Timing-vs-recovery gap, barge-in example, contributions |
| [03-benchmark-design-overview](wiki/03-benchmark-design-overview.md) | Data-generation pipeline (Figure 2 caption only; body garbled) |
| [04-related-work](wiki/04-related-work.md) | Prior voice/interruption/synthetic work vs. IHBench adaptation |
| [05-interruption-types](wiki/05-interruption-types.md) | Six interruption types and type-specific recovery rules |
| [06-evaluation-methodology](wiki/06-evaluation-methodology.md) | 27-config protocol, TF/RQ leaders, judge setup |
| [07-overall-results](wiki/07-overall-results.md) | Per-model points, judge agreement, depth decay, RQ distinctness |
| [08-judge-agreement](wiki/08-judge-agreement.md) | Depth-slope plot (Figure 4 caption only; body garbled) |
| [09-statistical-analysis](wiki/09-statistical-analysis.md) | TOST audio-vs-text equivalence by model family |
| [10-findings-discussion](wiki/10-findings-discussion.md) | Recovery as distinct capability, limits, extensions |
| [11-references](wiki/11-references.md) | References [17]–[50] plus start of Appendix A |
| [12-dataset-statistics](wiki/12-dataset-statistics.md) | Scale, type mix, turn skew, correction rarity (Table 2) |
| [13-audio-pipeline](wiki/13-audio-pipeline.md) | Human validation, per-type breakdown, RQ modality (Table 4, Figure 8) |
| [14-per-type-results](wiki/14-per-type-results.md) | Figure 8 modality fragment plus AMC re-run protocol |
| [15-workflow-structure](wiki/15-workflow-structure.md) | Disaster Housing Assistance state machine and success criteria |
| [16-rubric-design](wiki/16-rubric-design.md) | Per-interruption rubrics and TF/RQ judge prompts |
| [17-system-prompts](wiki/17-system-prompts.md) | Assistant system-message template and round planner |
| [18-user-simulation](wiki/18-user-simulation.md) | User-plan grounding, cut-in timing, type isolation |
| [19-simulator-branches](wiki/19-simulator-branches.md) | User simulator interrupting vs. normal branches |
| [20-verification-modifier](wiki/20-verification-modifier.md) | Verify–modify edit invariants and TTS formatting |

## Original Source

- arXiv: [IHBench: Evaluating Post-Interruption Recovery in Voice Agents with Structured Workflows](https://arxiv.org/abs/2606.19595)
- Local copy: [source/source.md](source/source.md)
