---
type: index
title: Rethinking Code Review Workflows with LLM
description: Folder index for the WirelessCar field study comparing AI-led co-reviewer summaries with on-demand LLM assistance during code review.
generated:
  by: claude/muse-spark-1.3-contributor
  at: 2026-09-23T20:43:49Z
sources:
  - id: original
    resource: https://arxiv.org/abs/2505.16339v1
  - id: local-copy
    resource: source/source.md
tags: [code-review, llm-assistants, human-ai-interaction, rag]
---

# Rethinking Code Review Workflows with LLM

This folder distils a WirelessCar field study and field experiment on LLM-assisted code review. It contrasts a proactive Co-Reviewer (Mode A) with a passive on-demand assistant (Mode B) across familiar and unfamiliar reviewers. Developers valued AI orientation on large or unfamiliar pull requests but preferred the mode situationally, with trust, verbosity, latency, and tool integration as the gating concerns.

## How to work through this

- Start with `summary.md` (~2 min) for the TL;DR, problem, ideas, findings, and future directions.
- Read `digest.md` (~10 min) for the full argument in eight verbatim lead blocks plus the five-move arc.
- Go deep in `wiki/` page by page for quotes, tables, RAG/`start_review` details, and Phase 1/Phase 2 themes; use `explainer.md` for plain language, `critical_thinking.md` for claims-vs-evidence, and `questions.md` for retrieval practice.

## Read This Folder

- [Summary](summary.md) — TL;DR, problem and motivation, ideas, findings, directions.
- [Digest](digest.md) — eight verbatim page leads plus the argument in five moves.
- [Explainer](explainer.md) — plain-language walkthrough with jargon decoder.
- [Critical Thinking](critical_thinking.md) — claims vs evidence, novelty, weaknesses, verdict.
- [Questions](questions.md) — ten retrieval prompts covering every wiki page.

## Wiki

| Page | Covers |
|---|---|
| [01 Rethinking Code Review Workflows with LLM](wiki/01-rethinking-code-review-workflows-with-llm.md) | Paper title, authors, affiliations, and abstract framing (source chunk truncated) |
| [02 Background, Related Work, and Research Questions](wiki/02-background-and-research-questions.md) | Review pain points, prior LLM-for-review work, RQ1/RQ2, two-phase design |
| [03 Phase 1 Participants and Setup](wiki/03-phase1-participants-and-setup.md) | Phase 1 interview roster: roles and team assignments |
| [04 Phase 2 Experiment Design](wiki/04-phase2-experiment-design.md) | Mode A vs Mode B field experiment, PRs, rotation, think-aloud procedure |
| [05 Tool Implementation: RAG Pipeline and Agentic Structure](wiki/05-tool-implementation-rag-pipeline.md) | GPLv3 artifact, `search_requirements`, Mode A `start_review` full-context sub-agent |
| [06 Phase 1 Findings: Challenges and AI Use Cases](wiki/06-phase1-findings-challenges-and-ai-use-cases.md) | Expected defect-catching, false positives, accuracy/trust, efficiency, integration wishes |
| [07 Phase 2 Findings — Trust and Integration](wiki/07-phase2-findings-trust-and-integration.md) | Quality gains, prompting skill, missing context, long output, latency, newcomer use |
| [08 Interaction Modes and Design Implications](wiki/08-interaction-modes-and-design-implications.md) | Situational Mode A/Mode B preference, pre-review patterns, implications, conclusion |

## Original Source

- ArXiv: [Rethinking Code Review Workflows with LLM Assistance: An Empirical Study](https://arxiv.org/abs/2505.16339v1)
- Local copy: [source/source.md](source/source.md)
