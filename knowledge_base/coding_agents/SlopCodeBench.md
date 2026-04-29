# SlopCodeBench: Benchmarking How Coding Agents Degrade Over Long-Horizon Iterative Tasks

**Paper:** [SlopCodeBench: Benchmarking How Coding Agents Degrade Over Long-Horizon Iterative Tasks (Orlanski et al., 2026)](https://arxiv.org/abs/2603.24755v1)

## Human Readable TL;DR

Imagine hiring a contractor to renovate your house one room at a time. Each room they finish looks fine on its own, but because they never plan ahead, the plumbing gets more tangled and the wiring more chaotic with every room -- until eventually the house becomes a nightmare to maintain. This paper builds a test that works the same way for AI coding assistants: it gives them a project and keeps adding requirements step by step. The AI's code passes each test, but it steadily becomes messier, more repetitive, and harder to extend -- 2x worse than code written by human developers. Even telling the AI "please write clean code" only helps at the start; the mess accumulates at the same rate regardless.

## TL;DR

SlopCodeBench is a language-agnostic benchmark of 20 iterative coding problems (93 checkpoints) where agents must repeatedly extend their own prior solutions under evolving specifications. No agent among 11 evaluated models solves any problem end-to-end (best strict solve rate: 17.2%). Two trajectory-level metrics -- structural erosion and verbosity -- reveal that agent code degrades monotonically: erosion rises in 80% of trajectories, verbosity in 89.8%, and agent code is 2.2x more verbose than maintained human repositories. Prompt-based interventions improve initial quality but do not reduce the degradation rate.

---

## Problem & Motivation

Existing coding-agent benchmarks overwhelmingly evaluate single-shot solutions against complete specifications. Code can pass a test suite but become progressively harder to extend -- a failure mode that pass-rate benchmarks cannot detect. Recent iterative benchmarks either supply gold-standard code between turns (breaking the causal chain of compounding design decisions), derive tasks from public repositories (introducing contamination risk), or measure only pass/fail without tracking quality over time. There is no benchmark that forces agents to live with the consequences of their own early architectural choices while quantifying how code quality evolves across multiple iterations.

---

## Main Original Ideas

1. **SlopCodeBench (SCBench)** -- A language-agnostic benchmark comprising 20 problems and 93 checkpoints where agents repeatedly extend their own prior code under evolving specifications. Problems specify only external behavior (CLI/API contracts), never internal structure, and test suites remain hidden. This forces agents to make architectural decisions whose consequences compound across checkpoints.

2. **Structural Erosion Metric** -- A novel trajectory-level quality signal measuring the fraction of total complexity mass concentrated in high-complexity functions. Defined as the share of cyclomatic-complexity-weighted mass (CC x sqrt(SLOC)) held by functions exceeding CC > 10. This captures the pathological pattern where agents patch new logic into existing functions rather than distributing it across focused callables.

3. **Verbosity Metric** -- A complementary quality signal combining 137 targeted AST-Grep rules (detecting wasteful code patterns) with structural duplication detection (clone lines normalized by LOC). Together these measure redundant code growth that adds no functionality.

4. **Prompt Intervention Study** -- A controlled experiment showing that "anti-slop" and "plan-first" prompts improve initial code quality (up to 34.5% reduction in verbosity) but do not change the degradation slope -- compounding resumes at the same rate once iteration begins.

---

## Key Findings

| Model | Strict (%) | Iso. (%) | Core (%) | Erosion | Verbosity | $/Checkpoint |
|---|---|---|---|---|---|---|
| **Opus 4.6** | **17.2** | **21.5** | **53.8** | 0.774 | 0.346 | $3.47 |
| GPT 5.4 | 11.8 | 20.4 | 48.4 | **0.515** | **0.286** | $3.27 |
| Opus 4.5 | 10.9 | 17.4 | 44.6 | 0.710 | 0.287 | $2.64 |
| GPT 5.2 | 10.8 | 19.4 | 43.0 | 0.711 | 0.358 | $4.55 |
| GPT 5.3 Codex | 9.7 | **23.7** | 51.6 | 0.676 | 0.356 | $3.14 |
| Sonnet 4.6 | 8.5 | 18.3 | 45.1 | 0.703 | 0.313 | $1.92 |
| GLM 4.7 | 4.3 | 9.7 | 32.3 | 0.664 | 0.305 | $1.61 |

- **No agent solves any problem end-to-end** across all 20 problems and 11 models evaluated.
- **Quality degrades monotonically**: erosion rises in 80% of trajectories, verbosity in 89.8%.
- **Agent code is 2.2x more verbose** than 48 maintained open-source Python repositories and has significantly higher erosion (0.68 vs. 0.31).
- **Human code stays flat over time** while agent code deteriorates with each iteration -- only 55% of human repos show rising erosion vs. 79% of agent trajectories.
- **Cost grows 2.9x** from first to last checkpoint without improving correctness.
- **Strict solve rates collapse** from ~10% at Start to 0.5% at Final progress phase; the gap between core and full test pass rates widens from 1.4x to 13.3x.
- **Early design decisions compound**: on code_search, all 7 configurations score 100% at C1-C2, but diverge dramatically by C3-C5 based on initial architectural choices.
- **Prompt interventions shift the intercept but not the slope**: anti-slop prompts cut initial verbosity by ~34% but degradation rate is unchanged, pass rates do not improve, and costs increase by up to 47.9%.

---

## Suggestions & Future Directions

1. **Stopping degradation, not just delaying it** -- The paper's central open question: prompt pressure shifts the starting point but not the rate. Interventions that enforce structural discipline across checkpoints (at training time or through tooling) remain untested and are the most critical next step.

2. **Training-time interventions** -- Current models lack the design discipline iterative development demands. Training approaches that reward long-horizon code quality, not just pass rates, could address the root cause.

3. **Tooling-based structural enforcement** -- External tools that detect and prevent erosion/verbosity accumulation during agent coding sessions could complement model-level improvements.

4. **Multi-language evaluation** -- The benchmark is language-agnostic by design, but current experiments cover only Python. Extending to other languages would test generalizability.

5. **Limitations acknowledged** -- Single run per configuration (no variance estimates), Python-only evaluation despite language-agnostic design, and the quality metrics (erosion and verbosity) do not cover all dimensions of code quality (e.g., security, performance).

---

## Authors & Institutions

Gabriel Orlanski (University of Wisconsin--Madison), Devjeet Roy (Washington State University), Alexander Yun (University of Wisconsin--Madison), Changho Shin (University of Wisconsin--Madison), Alex Gu (MIT), Albert Ge (University of Wisconsin--Madison), Dyah Adila (University of Wisconsin--Madison), Frederic Sala (University of Wisconsin--Madison), Aws Albarghouthi (University of Wisconsin--Madison)
