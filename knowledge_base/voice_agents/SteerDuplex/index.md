---
type: Index
title: "SteerDuplex: Steerable Duplex Speech Dialogue Models"
description: "Folder index for the SteerDuplex paper: steerable full-duplex speech dialogue via SFT plus two-stage RL, evaluated on the SteerBench benchmark."
generated:
  by: claude/muse-spark-1.3-contributor
  at: 2026-09-22T11:49:20Z
sources:
  - id: original
    resource: https://arxiv.org/abs/2609.12623
  - id: local-copy
    resource: source/source.md
tags: [speech-dialogue, full-duplex, steerability, reinforcement-learning, benchmarking]
---

# SteerDuplex: Steerable Duplex Speech Dialogue Models

SteerDuplex is a Moshi-based full-duplex speech dialogue model that adds steerability — reliably shifting tone, persona, speaking rate, and voice style on user instruction — on top of low-latency turn-taking and interruption handling. It pairs supervised fine-tuning on natural plus synthetic dialogues with two-stage reinforcement learning, and introduces the 390-prompt SteerBench benchmark with 1,067 human-authored rubrics. This folder holds a 2-minute summary, a 10-minute digest, nine wiki pages, and retrieval and critique companions.

## How to work through this

1. Read `summary.md` (~2 min) for the TL;DR, problem, main ideas, key findings, and future directions.
2. Read `digest.md` (~10 min) for the nine wiki-page condensations plus the argument in five moves.
3. Open the `wiki/` pages for full detail, then use `questions.md` for retrieval practice and `critical_thinking.md` / `explainer.md` for depth and critique.

## Read This Folder

- [Summary](summary.md) — TL;DR, problem and motivation, main ideas, key findings, future directions.
- [Digest](digest.md) — one-sentence plus key-points condensations of all nine wiki pages, plus the argument in five moves.
- [Explainer](explainer.md) — extended explanation companion.
- [Critical Thinking](critical_thinking.md) — critique and limits companion.
- [Questions](questions.md) — retrieval-practice questions Q1–Q14 covering every wiki page.

## Wiki

| Page | Covers |
|---|---|
| [01-steerduplex-overview](wiki/01-steerduplex-overview.md) | Paper overview: steerability gap, SFT plus two-stage RL recipe, SteerBench, headline gains |
| [02-capability-taxonomy](wiki/02-capability-taxonomy.md) | Three-family capability taxonomy and the low baseline audio-steering pass rates motivating SteerBench |
| [03-architecture-training](wiki/03-architecture-training.md) | Joint audio/text architecture, SFT setup, and two GDPO-based RL stages with continuity terms |
| [04-rl-interruption-results](wiki/04-rl-interruption-results.md) | RL gains on interruption response and pause handling, with flat or mixed secondary measures |
| [05-reward-hacking](wiki/05-reward-hacking.md) | Reward-hacking probes: silence shortcuts, empty rollouts, and the yielding-vs-continuing conflict |
| [06-references](wiki/06-references.md) | References [16]–[40], SFT/RL training settings, reward weights, compute, and checkpoint selection |
| [07-reward-components](wiki/07-reward-components.md) | Reward-component weights, capability retention, controls, judge sensitivity, and probe tables |
| [08-text-rubric-judge](wiki/08-text-rubric-judge.md) | Text rubric judge (D.4): one-criterion three-level scoring procedure |
| [09-audio-profile](wiki/09-audio-profile.md) | Artifact licenses, SteerBench construction and voicing, scoring rules, and audio prompt templates |

## Original Source

- arXiv: [SteerDuplex: Steerable Duplex Speech Dialogue Models](https://arxiv.org/abs/2609.12623)
- Local copy: [source/source.md](source/source.md)
