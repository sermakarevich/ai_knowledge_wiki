---
type: index
title: "AURA: Uncertainty-Routed Activation Editing for Acoustic Grounding in Speech Foundation Models"
description: "Folder index for the AURA paper — ultra-efficient uncertainty-routed activation editing that cuts speech-model hallucination while preserving clean-speech accuracy."
generated:
  by: claude/muse-spark-1.3-contributor
  at: 2026-09-22T10:36:59Z
sources:
  - id: original
    resource: http://arxiv.org/abs/2609.23979v1
  - id: local-copy
    resource: source/source.md
tags: [speech-recognition, acoustic-grounding, parameter-efficient-fine-tuning, hallucination-mitigation]
---

# AURA: Uncertainty-Routed Activation Editing for Acoustic Grounding in Speech Foundation Models

AURA freezes a pretrained attention encoder-decoder speech model and learns sparse scale-and-shift edits to decoder cross-attention heads, routed per decoding step by cross-attention uncertainty. It cuts non-speech hallucination dramatically (UrbanSound8K HRnorm 89.18% to 0.93%) with ~500x fewer parameters than LoRA, while an encoder-unfreezing diagnostic marks where decoder-only editing reaches its capacity boundary.

## How to work through this

Start with the summary (~2 min) for the TL;DR, problem, ideas, and findings. Then read the digest (~10 min) for the section-by-section argument in five moves. Then go deep in the wiki pages in order (overview → methodology → setup → results), use the explainer for plain-language intuition, the critical_thinking page for claims-vs-evidence scrutiny, and the questions page for retrieval practice.

## Read This Folder

- [Summary](summary.md) — TL;DR, problem and motivation, main ideas, key findings, future directions.
- [Digest](digest.md) — section-by-section distillation plus the argument in five moves.
- [Explainer](explainer.md) — plain-language walkthrough with jargon decoder.
- [Critical thinking](critical_thinking.md) — claims vs. evidence, novelty, weaknesses, applicability, verdict.
- [Questions](questions.md) — 8 retrieval-practice questions covering every wiki page.

## Wiki

| Page | Covers |
|------|--------|
| [01-aura-overview](wiki/01-aura-overview.md) | Paper framing: acoustic grounding failures and hallucination in AED speech foundation models, AURA proposal |
| [02-methodology-uncertainty-routed-editing](wiki/02-methodology-uncertainty-routed-editing.md) | Uncertainty-routed editing: cross-attention scale-and-shift backbone, Hard-Concrete static gates, Max-Prob/Entropy/Shift dynamic gate, training objective |
| [03-experimental-setup-and-baselines](wiki/03-experimental-setup-and-baselines.md) | Experimental setup training protocol through Sec. IV-C / Tables II–VII: AdamW protocol, baselines, non-speech and stressor protocols, capacity diagnostic |
| [04-results-and-analysis](wiki/04-results-and-analysis.md) | Results and analysis: hallucination reduction, grounding-stressor adaptation, ablations, and operating point |

## Original Source

- arXiv: [AURA: Uncertainty-Routed Activation Editing for Acoustic Grounding in Speech Foundation Models](http://arxiv.org/abs/2609.23979v1)
- Local copy: [source/source.md](source/source.md)
