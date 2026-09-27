---
type: index
title: Introduction - TypeSafe AI
description: Folder index for TypeSafe's Jev introduction — System One models, Choice/Score/Noul primitives, and atomic-question composition.
generated:
  by: claude/muse-spark
  at: 2026-09-16T19:46:20Z
sources:
  - id: original
    resource: https://docs.typesafe.ai/introduction
  - id: local-copy
    resource: source/source.md
tags: [typesafe, structured-decisions, system-one-models, ai-primitives]
---

# Introduction - TypeSafe AI

TypeSafe's Jev is a System One model that returns fast, structured decisions — Choice, Score, and Noul answers — directly to code instead of text to parse. This folder distills the introduction page into a quick summary, a verbatim digest, a plain-language explainer, and one wiki page. Start here to decide what to read next.

## How to work through this

1. Read `summary.md` (~2 min) for the TL;DR, core ideas, and findings.
2. Read `digest.md` (~10 min) for the verbatim key points and the argument in five moves.
3. Go deeper with the wiki page for full detail, then `explainer.md`, `critical_thinking.md`, and `questions.md` to test yourself.

## Read This Folder

- [Summary](summary.md) — TL;DR, problem and motivation, ideas, findings, next steps.
- [Digest](digest.md) — verbatim key points plus the argument in five moves.
- [Explainer](explainer.md) — plain-language walkthrough with examples and jargon decoder.
- [Critical thinking](critical_thinking.md) — claims vs. evidence, weaknesses, applicability, verdict.
- [Questions](questions.md) — retrieval practice (Q1–Q7) with answers.

## Wiki

| Page | Covers |
|---|---|
| [Documentation Index](wiki/01-documentation-index.md) | Documentation Index through Next steps (Introduction - TypeSafe AI chunk 01-documentation-index) |
| [[wiki/02-quick-start|Quick Start]] | Playground, HTTP API, Python SDK, and agent-skill paths to a first request. |
| [[wiki/03-system-one|System One]] | Calibrated System One decisions from Jev instead of generated text. |
| [[wiki/04-state|State]] | One state per request: facts in the state, judgments in the questions. |
| [[wiki/05-primitives-overview|Primitives Overview]] | Choice, Score, and Noul pairs evaluated independently in parallel. |
| [[wiki/06-choice|Choice]] | Fixed-set routing with full probabilities and confidence. |
| [[wiki/07-score|Score]] | Spectrum ratings with fractional probability-weighted values. |
| [[wiki/08-noul|Noul]] | Yes-or-no probability with no separate confidence value. |
| [[wiki/09-advanced-structure|Advanced structure]] | JSON structure in instructions, options, levels, and criteria. |
| [[wiki/10-ai-primer|AI primer]] | RLCD decision models for ~99% machine-to-machine automation. |
| [[wiki/11-confidence|Confidence]] | Distribution-derived confidence with risk-scaled thresholds. |
| [[wiki/12-how-to-build-with-system-one|How to build with TypeSafe]] | Code-owned workflows with atomic parallel questions. |
| [[wiki/13-use-case-map|Example use cases]] | Five capability categories and ten decision shapes. |
| [[wiki/14-patterns|Patterns]] | Four composable patterns trading cost, speed, reliability, safety. |
| [[wiki/15-speculative-fan-out|Speculative Fan-Out]] | Ask everything upfront in one parallel call. |
| [[wiki/16-confidence-gated-routing|Confidence-Gated Routing]] | The answer says what, confidence says whether to act. |
| [[wiki/17-composite-scoring|Composite Scoring]] | Weighted blends of normalized Score dimensions. |
| [[wiki/18-intent-routing|Intent Routing]] | Cheap classification fronting expensive handlers. |
| [[wiki/19-demos|Demos]] | Thin index of interactive examples (Smart Home demo). |
| [[wiki/20-smart-home-demo|Smart Home Assistant Demo]] | Speculative fan-out plus LLM splitting and fallback in action. |
| [[wiki/21-client-sdks|Client SDKs]] | Typed Python/JS clients with automatic retries. |
| [[wiki/22-api-reference|API Reference]] | jev-latest endpoint, request/response shapes, errors, retries. |
| [[wiki/23-agent-skill|Agent Skill]] | Drop-in TypeSafe context for coding agents. |

## Original Source

- Original: [Introduction - TypeSafe AI](https://docs.typesafe.ai/introduction)
- Local copy: [source/source.md](source/source.md)
