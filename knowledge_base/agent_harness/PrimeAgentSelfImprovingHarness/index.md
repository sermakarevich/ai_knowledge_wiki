---
type: Paper
title: Prime Agent: A Self-Improving RLM Harness
description: An open-source harness that separates a bounded language model from a persistent, self-improving substrate of state (L0-L3 caches), recursive subagents, and a Continual Harness, raising ARC-AGI-3 Best@1 from 30% to 95.5%.
generated: { by: claude/claude-sonnet-5, at: 2026-08-26T10:42:00Z }
sources:
  - id: original
    resource: https://arxiv.org/abs/2608.23552
  - id: local-copy
    resource: source/2608.23552.pdf
tags: [agents, llm-harness, rlm, long-horizon, benchmarks]
---

# Prime Agent: A Self-Improving RLM Harness

Prime Agent is Prime Intellect's open-source harness for long-horizon LLM agent evaluation and coding workflows: a persistent IPython REPL (the Recursive Language Model, or RLM, abstraction) gives models programmatic control over their own context and test-time compute, a Continual Harness lets prompts, memories, skills, and subagent specs evolve across trajectories without touching model weights, and recursive subagents coordinate directly with each other and with a human operator through an "Agents View." The paper's central claim is that most measured agent failure is harness failure, not model failure — and that fixing the harness lets frontier models convert extra tokens and cost into real task progress, raising ARC-AGI-3 RHAE Best@1 from 30% to 95.5% (matching the 95.4% human baseline) with the same underlying model.

## How to work through this

Three depths — stop at whichever answers your question:

1. **[[summary|Summary]]** (~2 min) — the whole thing, shallow.
2. **[[digest|Digest]]** (~10 min) — the whole thing, medium: every section's headline and key points.
3. **Wiki pages below** (~5-10 min each) — one section, deep. Each opens with its headline and key points, so you can stop early.

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
| [[wiki/01-introduction-and-motivation\|Introduction and Motivation]] | The model-as-bounded-processor framing, the L0-L3 state cache, expressivity as the key harness property, and the headline results |
| [[wiki/02-prime-agent-architecture\|Prime Agent Architecture]] | Information vs. computation management, the L0-L3 hierarchy, the `rlm` primitive, session lifecycle, Continual Harness, and long-horizon controls |
| [[wiki/03-arc-agi3-and-long-context-evaluation\|ARC-AGI-3 and Long-Context Evaluation]] | The three research questions, the ARC-AGI-3 test-time-scaling result (95.5% vs. 30% baseline), and the nine-task long-context benchmark suite |
| [[wiki/04-autonomous-research-and-programmatic-systems\|Autonomous Research and Programmatic Systems]] | The nanoGPT speedrun, out-of-loop experimentation, EmulatorBench, and PMPP-Hard GPU-kernel results |
| [[wiki/05-persistent-refinement-related-work-conclusion\|Persistent Refinement, Related Work, and Conclusion]] | The seven-day Factorio run (including a refinement safety failure), MazeBench, Related Work, and the model-harness co-learning conclusion |

## Original Source

- [source/2608.23552.pdf](source/2608.23552.pdf) — PDF, retrieved 2026-08-26
