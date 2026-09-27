---
type: Paper
title: Training AI Scientists to Replicate Research
description: Post-trains a 27B model (Faraday) to direct a frontier coding agent as a tool, using RL on an auto-generated, rubric-judged figure-replication task space (Replica), beating Claude Opus 4.8 and GPT-5.5 on held-out replication tasks.
generated: { by: claude/claude-sonnet-5, at: 2026-08-17T09:42:00Z }
sources:
  - id: original
    resource: https://arxiv.org/abs/2608.13331
  - id: local-copy
    resource: source/paper.pdf
tags: [ai-for-science, rl-post-training, llm-judge, coding-agents, benchmarks]
---

# Training AI Scientists to Replicate Research

This paper (arXiv 2608.13331, the "Replica / Faraday" paper) turns scientific paper replication into a scalable RL training ground for AI agents: an auto-generated task space of redacted-figure replication tasks (Replica), scored by a human-validated rubric judge, used to post-train a small model (Faraday) that directs a much larger coding agent as a tool. Faraday beats Claude Opus 4.8 and GPT-5.5 on held-out tasks, generalizing beyond its training envelope. It was worth ingesting because it's a concrete, well-evidenced case study on non-verifiable-reward RL, LLM-as-judge design, and "small orchestrator + large tool" agent architecture — all directly relevant to agentic system design.

## How to work through this

Three depths — stop at whichever answers your question:

1. **[[summary|Summary]]** (~2 min) — the whole thing, shallow.
2. **[[digest|Digest]]** (~10 min) — the whole thing, medium: every section's headline and key points.
3. **Wiki pages below** (~10-15 min each) — one section, deep. Each opens with its headline and key points, so you can stop early.

_New to the field? Start with [[explainer|the plain-language explainer]] instead. Coming back after a break? Read [[digest|the digest]], then [[questions|self-test]] — do not re-read the wiki._

## Read This Folder

- [[summary|Summary]] — rung 1: the whole source, shallow
- [[digest|Digest]] — rung 2: the whole source at medium depth; the file to re-read on review
- [[explainer|Plain-Language Explainer]] — no-jargon explanation, applications, conclusions
- [[critical_thinking|Critical Analysis]] — claims vs. evidence, applicability, what it changes
- [[questions|Retrieval Practice]] — self-test questions; **answer these from memory before re-reading anything**
- [[connections|Connections]] — related entries in this knowledge base

## Wiki

| Page | Covers |
|------|--------|
| [[wiki/01-introduction-motivation\|Introduction & Motivation]] | Why replication needs a new reward paradigm; Replica + Faraday introduced; headline results |
| [[wiki/02-related-work\|Related Work]] | Reward-design axes, replication-benchmark spectrum, and prior AI-Scientist training approaches |
| [[wiki/03-methods-replica-and-faraday\|Methods: Replica & Faraday]] | Task generation pipeline, rubric judge design and validation, harness, GRPO training recipe |
| [[wiki/04-results\|Results]] | Faraday vs. Claude/Codex head-to-head, judge quality, per-topic difficulty, prompting-can't-close-the-gap |
| [[wiki/05-discussion\|Discussion]] | Replication as a curriculum step, CAT paradigm, safety framing, real-author validation |
| [[wiki/06-appendix-task-and-judge-design\|Appendix: Task & Judge Design]] | Full-scale/tool generalization, ablations (credit assignment, coder-tool), human studies |
| [[wiki/07-appendix-example-tasks-and-rubrics\|Appendix: Example Tasks & Rubrics]] | Verbatim system prompt, task prompt, rater guide, optimized Codex prompt, worked rubrics, infra |

## Original Source

- [source/paper.pdf](source/paper.pdf) — PDF, retrieved 2026-08-17
