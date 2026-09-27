---
type: Paper
title: "Reflexion: Language Agents with Verbal Reinforcement Learning"
description: Reflexion reinforces language agents via verbal self-reflection stored in a bounded episodic memory instead of weight updates, lifting AlfWorld decision-making, HotPotQA reasoning, and HumanEval coding pass@1 without fine-tuning.
generated: { by: claude/sonnet-5, at: 2026-09-12T06:44:00Z }
sources:
  - id: original
    resource: https://arxiv.org/abs/2303.11366
  - id: local-copy
    resource: source/full.html
tags: [language-agents, self-reflection, episodic-memory, reinforcement-learning, llm-agents]
---

# Reflexion: Language Agents with Verbal Reinforcement Learning

Reflexion (Shinn, Cassano, Berman, Gopinath, Narasimhan, Yao — arXiv:2303.11366) reinforces language agents through linguistic feedback rather than gradient updates: an Actor, Evaluator, and Self-Reflection LLM loop stores verbal self-critiques of failed trials in a small episodic memory and replays them as context on the next attempt, lifting AlfWorld decision-making to 130/134 tasks, HotPotQA reasoning by +20%, and HumanEval Python coding to 91% pass@1 — all without fine-tuning.

## How to work through this

Three depths — stop at whichever answers your question:

1. **[[summary|Summary]]** (~2 min) — the whole thing, shallow.
2. **[[digest|Digest]]** (~10 min) — the whole thing, medium: every section's headline and key points.
3. **Wiki pages below** (~10 min each) — one section, deep. Each opens with its headline and key points, so you can stop early.

_New to language agents or self-reflection loops? Start with [[explainer|the plain-language explainer]] instead. Coming back after a break? Read [[digest|the digest]], then [[questions|self-test]] — do not re-read the wiki._

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
| [[wiki/01-introduction-method\|Intro, Related Work, Reflexion Method]] | Actor/Evaluator/Self-Reflection loop, policy pi_theta, short-term vs long-term memory bounded to Omega=1-3, comparison tables vs Self-Refine/AlphaCode/CodeT/Self-Debugging/CodeRL |
| [[wiki/02-experiments\|Experiments Across Decision/Reasoning/Programming]] | AlfWorld 130/134 over 12 trials, HotPotQA +20%, HumanEval/MBPP/LeetCode pass@1 scores, MBPP false-positive test analysis, HumanEval Rust ablation, StarChat-Beta capability gating |
| [[wiki/03-appendices\|Appendices C-D and Extra Evals]] | AlfWorld mug/desklamp trial trace, WebShop failure (no improvement, unhelpful reflections), strict function-body-only coding prompts, HotPotQA cast-intersection example |

## Original Source

- [source/full.html](source/full.html) — Paper source, arXiv:2303.11366
