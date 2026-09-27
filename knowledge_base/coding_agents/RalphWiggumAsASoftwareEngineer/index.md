---
type: index
title: Ralph Wiggum as a "software engineer"
description: Folder index for the Ralph loop technique — monolithic one-item-per-loop agent with spec-driven work selection and fast verification back-pressure, from the CURSED compiler build.
generated:
  by: claude/muse-spark-1.3-contributor
  at: 2026-09-25T05:50:25Z
sources:
  - id: original
    resource: https://ghuntley.com/ralph
  - id: local-copy
    resource: source/source.md
tags: [ai-agents, agentic-coding, llm-loops, verification]
---

# Ralph Wiggum as a "software engineer"

Ralph is a monolithic, single-process agentic loop that implements one priority-sorted item per iteration against written specifications, keeping the primary context thin while fanning work out to subagents. This folder distils the technique from the CURSED compiler build: deterministic context allocation, steering via stdlib and specs, fast back-pressure verification, and senior-operated reset-or-rescue discipline. Scope is Greenfield-only bootstrapping (~90% done), not brownfield work.

## How to work through this

1. Start with [summary.md](summary.md) (~2 min) for the TL;DR, core ideas, and findings.
2. Continue to [digest.md](digest.md) (~10 min) for the verbatim per-page key points plus the five-move argument.
3. Go deep in the [wiki pages](wiki/01-prompt-md-contents.md) one by one (01 → 02 → 03), then use [explainer.md](explainer.md) for plain-language onboarding, [critical_thinking.md](critical_thinking.md) for claims-vs-evidence scrutiny, and [questions.md](questions.md) for retrieval practice.

## Read This Folder

- [Summary](summary.md) — TL;DR, motivation, main ideas, findings, and future directions.
- [Digest](digest.md) — verbatim key points per wiki page plus the argument in five moves.
- [Explainer](explainer.md) — plain-language walkthrough: what Ralph is, why it matters, how it works, where to use it.
- [Critical thinking](critical_thinking.md) — claims vs. evidence, new vs. repackaged, blind spots, applicability, verdict.
- [Questions](questions.md) — retrieval practice Q1–Q7 with answers linked back to wiki pages.

## Wiki

| Page | Covers |
|---|---|
| [01](wiki/01-prompt-md-contents.md) | prompt.md contents: no copy-pasteable prompt, monolithic one-item-per-loop, deterministic plan-plus-specs allocation, scheduler-style subagent fan-out, don't-assume search discipline |
| [02](wiki/02-phase-one-generate.md) | phase one generate and phase two back-pressure: stdlib/spec steering, fast verification wheel, why-capture in tests/docs, anti-placeholder discipline, TODO-list lifecycle, loop-back self-improvement |
| [03](wiki/03-broken-codebase-overnight.md) | broken mornings and operating envelope: reset-vs-rescue judgment, commit/tag discipline, cross-model rescue, Greenfield-only ~90% scope, senior-guidance requirement, current build and plan prompts |

## Original Source

- Original article: [Ralph Wiggum as a "software engineer"](https://ghuntley.com/ralph)
- Local copy: [source/source.md](source/source.md)
