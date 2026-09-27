---
type: Paper
title: "Self-Refine: Iterative Refinement with Self-Feedback"
description: One frozen LLM loops as its own generator, feedback-giver, and refiner via few-shot prompts, lifting GPT-3.5/ChatGPT/GPT-4 by ~20% absolute on average across 7 tasks with no extra training, though self-verification fails where the model can't spot its own errors (math).
generated: { by: claude, at: 2026-09-12T06:49:00Z }
sources:
  - id: original
    resource: https://arxiv.org/abs/2303.17651
  - id: local-copy
    resource: source/full.md
tags: [llm-agents, self-critique, iterative-refinement, prompting, self-feedback]
---

# Self-Refine: Iterative Refinement with Self-Feedback

Self-Refine (Madaan et al.) uses a single frozen LLM to draft an answer, critique its own draft in plain language, and rewrite using that critique — looping for up to 4 iterations or until the feedback signals a stop. Across 7 tasks (code optimization, code readability, dialogue response, math reasoning, sentiment reversal, acronym generation, constrained generation), it lifts strong models like GPT-3.5, ChatGPT, and GPT-4 by ~20% absolute on average with no extra training, though it needs a strong instruction-following base model and fails on tasks (math) where the model cannot verify its own correctness.

## How to work through this

Three depths — stop at whichever answers your question:

1. **[[summary|Summary]]** (~2 min) — the whole thing, shallow.
2. **[[digest|Digest]]** (~10 min) — the whole thing, medium: every section's headline and key points.
3. **Wiki pages below** (~5 min each) — one section, deep. Each opens with its headline and key points, so you can stop early.

_New to the field? Start with [[explainer|the plain-language explainer]] instead. Coming back after a break? Read [[digest|the digest]], then [[questions|self-test]] — do not re-read the wiki._

## Read This Folder

- [[summary|Summary]] — rung 1: the whole source, shallow
- [[digest|Digest]] — rung 2: the whole source at medium depth; the file to re-read on review
- [[explainer|Plain-Language Explainer]] — no-jargon explanation, applications, conclusions
- [[critical_thinking|Critical Analysis]] — claims vs. evidence, applicability, what it changes, verdict
- [[questions|Retrieval Practice]] — self-test questions; **answer these from memory before re-reading anything**
- [[connections|Connections]] — related entries in this knowledge base

## Wiki

| Page | Covers |
|------|--------|
| [[wiki/01-method-evaluation\|Method and evaluation]] | The generate/feedback/refine loop, headline ~20% average gain, feedback-specificity ablations, cross-model/task results, Math Reasoning's near-null gain, failure analysis, Vicuna-13B limits |
| [[wiki/02-evaluation-appendices\|Eval appendices A-K]] | 7-task definitions and sizes, blind human A/B protocol, GPT-4-as-judge setup, SOTA comparisons, Vicuna/oracle/statistical-significance ablations, two new hard tasks |
| [[wiki/03-task-appendices\|Task appendices L-R]] | Per-task deep dives: code readability, dialogue response, code optimization, math reasoning, sentiment reversal, acronym generation, constrained generation |
| [[wiki/04-prompts\|Prompt appendix S]] | Verbatim few-shot prompts (Figures 19-38) for generation, feedback, and refine across all 7 tasks |

## Original Source

- [source/full.md](source/full.md) — full paper text, retrieved from arXiv:2303.17651
