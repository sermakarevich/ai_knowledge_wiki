---
type: index
title: Context Engineering for Multi-Agent LLM Code Assistants Using Elicit, NotebookLM, ChatGPT, and Claude Code
description: Folder index for Haseeb (2025) on a four-stage context-engineering pipeline (intent translation, retrieval, synthesis, multi-agent execution) that lifts single-shot success on a large codebase.
generated:
  by: claude/muse-spark-1.3-contributor
  at: 2026-09-23T20:10:30Z
sources:
  - id: original
    resource: https://arxiv.org/abs/2508.08322v1
  - id: local-copy
    resource: source/source.md
tags: [context-engineering, multi-agent-systems, code-assistants, retrieval-augmented-generation]
---

# Context Engineering for Multi-Agent LLM Code Assistants Using Elicit, NotebookLM, ChatGPT, and Claude Code

This folder distils Haseeb (2025), which frames repository-level coding as a context-supply problem and tests a GPT-5 → Elicit → NotebookLM → Claude Code pipeline on the ~180K-line RainMakerz Next.js app (4/5 single-shot wins vs 2/5 for a single-agent baseline, at ~3–5× token cost). Use it to learn the L1–L5 layering, the plan–delegate–test–review loop, and the honest limits (n=5, private repo, no ablations).

## How to work through this

1. Start with `summary.md` (~2 min) for the TL;DR, problem, ideas, findings, and future directions.
2. Read `digest.md` (~10 min) for the four wiki sections in condensed form plus the five-move argument.
3. Dive into `wiki/` pages for verbatim evidence, tables, and figures, then `explainer.md` for plain-language intuition, `critical_thinking.md` for claims-vs-evidence scrutiny, and `questions.md` for retrieval practice.

## Read This Folder

- [Summary](summary.md) — TL;DR, problem and motivation, main ideas, key findings, future directions.
- [Digest](digest.md) — condensed per-wiki-section brief plus the argument in five moves.
- [Explainer](explainer.md) — plain-language walkthrough with jargon decoder.
- [Critical thinking](critical_thinking.md) — claims vs evidence, novelty, weaknesses, applicability, verdict.
- [Questions](questions.md) — eight retrieval-practice Q&A covering all four wiki pages.

## Wiki

| Page | Covers |
|---|---|
| [01-context-engineering-multi-agent-code](wiki/01-context-engineering-multi-agent-code.md) | Abstract, introduction (why single agents fail), four-component workflow definition, related work opening (HyperAgent, MASAI) |
| [02-planning-iterative-refinement](wiki/02-planning-iterative-refinement.md) | CodePlan planning, DARS re-sampling, AllianceCoder retrieval, Elicit/NotebookLM pipeline, repo indexing, intent translation, agent tooling |
| [03-claude-multi-agent-architecture](wiki/03-claude-multi-agent-architecture.md) | Specialist sub-agents, isolated contexts with shared CLAUDE.md, L1–L5 layering, plan–delegate–test–review loop, RainMakerz results |
| [04-results-discussion-efficiency-cost](wiki/04-results-discussion-efficiency-cost.md) | Token/message cost, context-engineering effect, orchestration lessons, limitations, generality and future work, conclusion |

## Original Source

- arXiv: [Context Engineering for Multi-Agent LLM Code Assistants Using Elicit, NotebookLM, ChatGPT, and Claude Code](https://arxiv.org/abs/2508.08322v1)
- Local copy: [source/source.md](source/source.md)
