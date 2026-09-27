---
type: Paper
title: "Agent Skills Can Be Harmful: An Empirical Study of Skill-Induced Failures in LLM Agents"
description: A contrastive-testing study that attributes 307 confirmed LLM-agent task failures and cost regressions to specific loaded "agent skills," taxonomizes their root causes, and introduces SkillTriage, an automated attribution tool.
generated: { by: claude/claude-sonnet-5, at: 2026-08-14T13:30:00Z }
sources:
  - id: original
    resource: https://arxiv.org/abs/2608.11888
  - id: local-copy
    resource: source/2608.11888.pdf
tags: [agent-skills, llm-agents, failure-analysis, context-engineering, benchmarking]
---

# Agent Skills Can Be Harmful: An Empirical Study of Skill-Induced Failures in LLM Agents

This paper studies why "agent skills" — reusable SKILL.md instruction packages that guide LLM coding agents — sometimes make agents worse rather than better. Using a differential-testing-inspired contrastive design (comparing a skill-guided run against a no-skill or matched-skill reference run on the same task), the authors confirm 307 skill-induced failures across two benchmarks, build root-cause taxonomies for functional failures and efficiency regressions, and develop SkillTriage, a tool that automates attribution of new cases. It is directly relevant to anyone maintaining a library of agent instruction files (SKILL.md, CLAUDE.md-style skills, etc.).

## How to work through this

Three depths — stop at whichever answers your question:

1. **[[summary|Summary]]** (~2 min) — the whole thing, shallow.
2. **[[digest|Digest]]** (~10 min) — the whole thing, medium: every section's headline and key points.
3. **Wiki pages below** (~10 min each) — one section, deep. Each opens with its headline and key points, so you can stop early.

_New to agent skills or agent-failure analysis? Start with [[explainer|the plain-language explainer]] instead. Coming back after a break? Read [[digest|the digest]], then [[questions|self-test]] — do not re-read the wiki._

## Read This Folder

- [[summary|Summary]] — rung 1: the whole paper, shallow
- [[digest|Digest]] — rung 2: the whole paper at medium depth; the file to re-read on review
- [[explainer|Plain-Language Explainer]] — no-jargon explanation, applications, conclusions
- [[critical_thinking|Critical Analysis]] — claims vs. evidence, applicability, what it changes
- [[questions|Retrieval Practice]] — self-test questions; **answer these from memory before re-reading anything**
- [[connections|Connections]] — related entries in this knowledge base

## Wiki

| Page | Covers |
|------|--------|
| [[wiki/01-problem-and-methodology\|Problem, Background, and Methodology]] | Motivation, agent-skill/SKILL.md anatomy, the contrastive target-vs-reference design, functional-failure/efficiency-regression definitions, study subjects (SkillsBench, SWE-Skills-Bench), public-skill augmentation, and the 307-case final dataset |
| [[wiki/02-functional-failure-taxonomy\|Root Causes of Functional Failures]] | Taxonomy of the 125 functional failures: Applicability Mismatch, Environment Mismatch, Task-Implementation Fault (largest, 68.8%), Artifact Misplacement, with worked examples |
| [[wiki/03-efficiency-regression-taxonomy\|Root Causes of Efficiency Regressions]] | Taxonomy of the 182 efficiency regressions: Context Bloat, Excessive Procedure (largest, 62.6%), Dependency Resolution |
| [[wiki/04-skilltriage-tool-and-evaluation\|SkillTriage: Automated Attribution Tool]] | The DS1-DS5 differential-evidence signals, phase/action-tag cost evidence, and attribution accuracy against manual labels |
| [[wiki/05-discussion-and-related-work\|Discussion, Related Work, and Conclusion]] | Future research directions, threats to validity, positioning against SkillsBench/SWE-Skills-Bench/context-engineering/agent-failure literature, conclusion |

## Original Source

- [source/2608.11888.pdf](source/2608.11888.pdf) — Paper PDF, retrieved 2026-08-14
