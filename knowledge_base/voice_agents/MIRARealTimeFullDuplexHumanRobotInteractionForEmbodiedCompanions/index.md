---
type: index
title: "MIRA: Real-Time Full-Duplex Human-Robot Interaction for Embodied Companions"
description: "Folder index for the MIRA paper — orientation, reading order, and links to summary, digest, explainer, critical thinking, questions, wiki pages, and the original source."
generated:
  by: claude/opencode-go/muse-spark-1.3-contributor
  at: 2026-09-22T09:19:58Z
sources:
  - id: original
    resource: http://arxiv.org/abs/2609.24547v1
  - id: local-copy
    resource: source/source.md
tags: [human-robot-interaction, full-duplex-dialogue, co-speech-gesture, diffusion-motion, turn-taking]
---

# MIRA: Real-Time Full-Duplex Human-Robot Interaction for Embodied Companions

MIRA is a unified real-time full-duplex framework that lets an Astribot S1 humanoid speak, gesture, and yield gracefully under streaming, interruptible interaction. Its CORTEX policy pairs a fast 450 ms interruption gate with deliberative turn arbitration and explicit embodiment-cue routing, while the ROSCO diffusion generator streams co-speech motion under Receding-Horizon Prefix Commitment (predict 50 frames, commit 15). Start with the summary for the big picture, then use the digest and wiki pages below for the mechanisms, numbers, and limits.

## How to work through this

1. **Summary (~2 min)** — the TL;DR, problem, original ideas, key findings, and future directions.
2. **Digest (~10 min)** — one-sentence take plus key points per wiki page, then the argument in five moves.
3. **Wiki pages** — deep dives in order: overview → related work → CORTEX → embodiment routing → ROSCO → RHPC → evaluation → discussion → references.
4. **Explainer, critical thinking, questions** — build intuition, stress-test the claims, then self-quiz with retrieval prompts.

## Read This Folder

- [Summary](summary.md) — TL;DR, problem and motivation, original ideas, findings, future directions.
- [Digest](digest.md) — per-page one-sentence summaries with verbatim key points plus the argument in five moves.
- [Explainer](explainer.md) — intuitive walkthrough of the system.
- [Critical Thinking](critical_thinking.md) — strengths, weaknesses, and open questions.
- [Questions](questions.md) — retrieval-practice prompts with answers covering every wiki page.

## Wiki

| Page | Covers |
|------|--------|
| [MIRA Overview and Contributions](wiki/01-mira-overview-and-contributions.md) | Unified full-duplex framework, embodiment-cue routing, RHPC idea, CORTEX + execution overview, Astribot S1 deployment |
| [Related Work — Streaming Dialogue and Embodied Companions](wiki/02-related-work-streaming-dialogue-and-companions.md) | Audio Interaction Model, endpointing/overlap timing, ProAct contrast, physical-commitment problem, conservative affect fusion |
| [CORTEX Interaction Policy and Architecture](wiki/03-cortex-interaction-policy-and-architecture.md) | Three-stage architecture, 450 ms VAD interruption gate, deliberative arbiter (IGNORE/REPLY/INTERRUPT_AND_REPLY), reactive generator, shared response-identity state |
| [Embodiment Cue, Routing, and Execution](wiki/04-embodiment-cue-routing-and-execution.md) | `<motion: m>` cue protocol, parsing/defaults, validated-library vs ROSCO routing, MuJoCo collision-aware projection, 250 Hz control loop |
| [ROSCO Model and Training](wiki/05-rosco-model-and-training.md) | Prefix-conditioned diffusion transformer, causal audio discipline, architecture dimensions, four training objectives |
| [Receding-Horizon Prefix Commitment Inference](wiki/06-receding-horizon-prefix-commitment.md) | 50-frame predict / 15-frame commit / 10-frame prefix loop, overlap smoothing, train-test mismatch, barge-in bounding |
| [Evaluation: Motion Quality, Streaming Latency, and Turn Arbitration](wiki/07-evaluation-motion-quality-and-streaming.md) | FID-G/beat-consistency/collision results, 195 ms chunk inference (RTF 0.390), 466 ms preemption, 199-session turn-arbitration traces |
| [Discussion and Limitations: System Insights](wiki/08-discussion-limitations-and-deployment.md) | Hybrid-routing insight, end-to-end streaming quality, constrained vocabulary, per-platform safety tuning, startup latency, missing long-term user studies |
| [References and Further Reading](wiki/09-references-and-further-reading.md) | Reference-list tail [24]–[44]: body models, gesture synthesis, datasets, diffusion backbones, turn-taking and affect surveys |

## Original Source

- arXiv: [MIRA: Real-Time Full-Duplex Human-Robot Interaction for Embodied Companions](http://arxiv.org/abs/2609.24547v1)
- Local copy: [source/source.md](source/source.md)
