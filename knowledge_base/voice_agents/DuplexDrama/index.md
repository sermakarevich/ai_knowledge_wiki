---
type: index
title: "DuplexDrama: A Synthesized Dialogue Dataset with Scenarios, Full-Duplex Behaviors, Expressive Speech, and Sound Events"
description: "Index for a synthesized full-duplex spoken dialogue dataset covering persona/scenario settings, interruption/backchannel/incomplete behaviors, expressive speech, and script-aware sound events."
generated:
  by: claude/muse-spark-1.3-contributor
  at: 2026-09-22T11:41:22Z
sources:
  - id: original
    resource: https://arxiv.org/abs/2609.12872
  - id: local-copy
    resource: source/source.md
tags: [full-duplex-dialogue, synthetic-speech-dataset, expressive-tts, sound-events]
---

# DuplexDrama: A Synthesized Dialogue Dataset with Scenarios, Full-Duplex Behaviors, Expressive Speech, and Sound Events

DuplexDrama is a synthesized spoken dialogue corpus that jointly scripts personas/scenarios, full-duplex overlap behaviors, expressive emotion labels, and sound events into multi-track audio. This folder holds a 2-minute summary, a 10-minute digest, five wiki pages covering the pipeline and validation, plus explainer, critical analysis, and retrieval questions. Start with the summary, then use the digest and wiki pages for section-level detail.

## How to work through this

1. Read `summary.md` (~2 min) for the TL;DR, problem, ideas, findings, and future directions.
2. Read `digest.md` (~10 min) for the five-section argument with verbatim key points per wiki page.
3. Deep-dive the `wiki/` pages in order for per-section evidence, verbatim claims, and tables/figures.
4. Use `explainer.md` for plain-language intuition, `critical_thinking.md` for claims-vs-evidence scrutiny, and `questions.md` for retrieval practice.

## Read This Folder

- [Summary](summary.md) — TL;DR, problem and motivation, main ideas, key findings, future directions.
- [Digest](digest.md) — five-section condensed argument with verbatim key points.
- [Explainer](explainer.md) — plain-language walkthrough: what it is, why it matters, how it works, where it applies.
- [Critical thinking](critical_thinking.md) — claims vs. evidence, novelty, weaknesses, applicability, verdict.
- [Questions](questions.md) — ten retrieval prompts with answers covering every wiki page.

## Wiki

| Page | Covers |
|---|---|
| [01-overview-and-contributions](wiki/01-overview-and-contributions.md) | Title/abstract "first" claim, Lisa-and-Tom persona/scenario example, 4-file multi-track audio figure |
| [02-pipeline-persona-script-synthesis](wiki/02-pipeline-persona-script-synthesis.md) | Four-stage pipeline overview; persona/scenario generation (§2.1), tagged script generation (§2.2), IndexTTS2 synthesis and full-duplex assembly (§2.3), background channels (§2.4) |
| [03-audio-assembly-background-validation](wiki/03-audio-assembly-background-validation.md) | Pipeline/sound-event figures (Fig. 2–3), event mixing at FA onsets, dual-LLM plus 4-metric validator (§2.5), Tables 1–2 fragments |
| [04-dataset-statistics-audio-quality](wiki/04-dataset-statistics-audio-quality.md) | Corpus overview and tag distributions (Tables 1–2, Fig. 4–5), clean-vs-mixed audio metrics (Table 3), prior-corpora comparison (Table 5) |
| [05-script-validation-comparison-conclusion](wiki/05-script-validation-comparison-conclusion.md) | Dual-LLM script rationality validation (§3.2.2, Table 4), dataset comparison (§3.3, Table 5), conclusion, future work, ethics disclosures |

## Original Source

- arXiv: [DuplexDrama: A Synthesized Dialogue Dataset with Scenarios, Full-Duplex Behaviors, Expressive Speech, and Sound Events](https://arxiv.org/abs/2609.12872)
- Local copy: [source/source.md](source/source.md)
