---
type: index
title: TDD Governance for Multi-Agent Code Generation via Prompt Engineering
description: Folder index for the EASE 2026 paper turning classical TDD Red-Green-Refactor discipline into enforceable multi-agent prompt and workflow governance.
generated:
  by: claude/muse-spark-1.3-contributor
  at: 2026-09-23T20:28:44Z
sources:
  - id: original
    resource: https://arxiv.org/abs/2604.26615v1
  - id: local-copy
    resource: source/source.md
tags: [tdd, multi-agent-systems, prompt-engineering, code-generation]
---

# TDD Governance for Multi-Agent Code Generation via Prompt Engineering

This folder distils the EASE 2026 proposal for an AI-native TDD framework that enforces Red-Green-Refactor phase ordering, bounded repair, and validation gates across multi-agent code generation. Start with the two-minute summary, deepen with the ten-minute digest, then work through the wiki pages for mechanisms, limits, and critique.

## How to work through this

1. **Summary (~2 min)** — read `summary.md` for the TL;DR, problem, original ideas, findings, and outlook.
2. **Digest (~10 min)** — read `digest.md` for the five-move argument with one-sentence takeaways and key points per wiki page.
3. **Wiki pages** — go in order 01 → 05 for full detail, then `explainer.md` for plain language, `critical_thinking.md` for critique, and `questions.md` for retrieval practice.

## Read This Folder

- [Summary](summary.md)
- [Digest](digest.md)
- [Explainer](explainer.md)
- [Critical thinking](critical_thinking.md)
- [Questions](questions.md)

## Wiki

| Page | Covers |
|---|---|
| [01-tdd-governance-overview](wiki/01-tdd-governance-overview.md) | Paper identity, abstract claims, and introduction: TDD as enforceable governance with proposal/engine separation |
| [02-tdd-foundations-and-llm-instability](wiki/02-tdd-foundations-and-llm-instability.md) | Classical TDD foundations (Beck/Fowler), LLM instability evidence, and why test-guided prompting lacks phase discipline |
| [03-principle-extraction-and-manifesto](wiki/03-principle-extraction-and-manifesto.md) | Bounded Beck/Martin principle extraction, Table 1 categories, and the machine-readable TDD manifesto |
| [04-governed-workflow-and-architecture](wiki/04-governed-workflow-and-architecture.md) | Governed workflow: validation gates, role-specific prompts, atomic mutation control, and bounded (N=3) repair |
| [05-discussion-limitations-and-outlook](wiki/05-discussion-limitations-and-outlook.md) | Positioning vs auxiliary-test baselines, preliminary findings, limitations, and repository-scale future work |

## Original Source

- arXiv: [TDD Governance for Multi-Agent Code Generation via Prompt Engineering](https://arxiv.org/abs/2604.26615v1)
- Local copy: [source/source.md](source/source.md)
