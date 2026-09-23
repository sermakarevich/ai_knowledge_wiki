---
type: index
title: How to Build a Custom Agent Harness
description: Folder index for LangChain's guide to building a custom agent harness — agent equals model plus harness, with create_agent and composable middleware.
generated:
  by: claude/opencode
  at: 2026-09-16T15:17:30Z
sources:
  - id: original
    resource: https://www.langchain.com/blog/how-to-build-a-custom-agent-harness
  - id: local-copy
    resource: source/source.md
tags: [agents, agent-harness, langchain, middleware]
---
# How to Build a Custom Agent Harness

This folder collects notes on LangChain's guide to building a custom agent harness, which defines a useful agent as `agent = model + harness`. The core lesson is task-harness fit: start from the minimal `create_agent(model, tools, system_prompt)` loop and tailor it with composable middleware that delivers the right context at every step.

## How to work through this

1. Read the **summary** (~2 min) for the TL;DR, problem, main ideas, and findings.
2. Read the **digest** (~10 min) for the one-sentence thesis, key points, and the argument in five moves.
3. Go deeper with the **wiki pages**, then test yourself with **questions** and stress-test the claims with **critical_thinking**.

## Read This Folder

- [summary](summary.md) — TL;DR, problem and motivation, main ideas, key findings.
- [digest](digest.md) — distilled thesis, key points, and the argument in five moves.
- [explainer](explainer.md) — plain-language walkthrough of the article.
- [critical_thinking](critical_thinking.md) — claims vs. evidence and critical analysis.
- [questions](questions.md) — retrieval-practice questions with answers.

## Wiki

| Page | Covers |
| --- | --- |
| [How to Build a Custom Agent Harness](wiki/01-how-to-build-a-custom-agent-harness.md) | Agent-as-model-plus-harness definition, task-harness fit, minimal create_agent base, middleware hooks and four levers, production capability-to-middleware mapping |

## Original Source

- Original article: [How to Build a Custom Agent Harness](https://www.langchain.com/blog/how-to-build-a-custom-agent-harness)
- Local copy: [source/source.md](source/source.md)
