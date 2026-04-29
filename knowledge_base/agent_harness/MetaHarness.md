# Meta-Harness: End-to-End Optimization of Model Harnesses

**Paper:** [Meta-Harness: End-to-End Optimization of Model Harnesses (Lee et al., 2025)](https://arxiv.org/abs/2603.28052)

## Human Readable TL;DR

Imagine you hire an expert chef (the AI model), but their performance depends heavily on the kitchen setup -- the recipe cards, ingredient layout, and cooking tools they are given. Traditionally, a human manager arranges this kitchen by hand, watching the chef fail and tweaking things one dish at a time. Meta-Harness is like hiring a second expert who watches recordings of every past cooking attempt, reads every recipe card that was used, and then redesigns the entire kitchen layout to help the chef perform better. The key insight is that this second expert needs to see the full footage, not just a final score -- because knowing *why* a dish failed matters far more than just knowing *that* it failed.

## TL;DR

Meta-Harness is an outer-loop optimization system that automatically searches over LLM harness code -- the external programs controlling what information is stored, retrieved, and presented to a model. Unlike prior text optimizers that compress feedback into scalar scores or short summaries, Meta-Harness gives an agentic proposer (a coding agent) filesystem access to the full source code, execution traces, and evaluation scores of all prior candidates. Across text classification, retrieval-augmented math reasoning, and agentic coding benchmarks, discovered harnesses outperform hand-engineered and automatically-optimized baselines, achieving +7.7 points over state-of-the-art context engineering, +4.7 average accuracy on IMO-level math across five models, and top-tier rankings on TerminalBench-2.

---

## Problem & Motivation

LLM performance depends not only on model weights but critically on the **harness** -- the surrounding code that manages context, retrieval, memory, and prompt construction. Harness design can cause up to a **6x difference** in model performance on the same benchmark, yet it remains a largely manual process where practitioners inspect failures and iterate on heuristics.

Existing automated text optimizers are poorly suited for harness engineering because they **compress feedback too aggressively**: they are memoryless, condition only on scalar scores, or restrict feedback to short templates or summaries. Harnesses are stateful programs with long-horizon effects -- a design choice made early in an interaction can cascade into failures many steps later. Diagnosing such failures requires access to raw execution traces (potentially 10M+ tokens per evaluation), far exceeding what prior methods handle (hundreds to tens of thousands of tokens per iteration).

---

## Main Original Ideas

1. **Filesystem-Based Full History Access** -- Instead of compressing feedback into scores or summaries, Meta-Harness stores every prior candidate's complete source code, execution traces, and evaluation scores on a filesystem. The proposer agent selectively inspects this data using standard terminal tools (grep, cat), enabling causal reasoning about failures that lossy feedback would obscure.

2. **Agentic Proposer for Code-Space Search** -- The optimization occurs directly in code space via an autonomous coding agent (Claude Code with Opus-4.6) that decides what to inspect, which failure modes to prioritize, and how to modify the harness. This avoids hard-coded search heuristics and enables algorithmic modifications to retrieval, memory, and prompt-construction logic -- including full program rewrites.

3. **Minimal Outer-Loop Structure** -- Meta-Harness imposes minimum necessary structure on the search loop: initialize, evaluate, log to filesystem, let the proposer read and propose, repeat. This contrasts with prior methods that impose structured feedback templates, mutation operators, or workflow graphs, and yields 10x faster convergence than structured alternatives.

4. **Pareto-Frontier Discovery** -- When multiple objectives matter (e.g., accuracy vs. context cost), Meta-Harness evaluates candidates based on Pareto dominance, discovering a frontier of harnesses that trade off performance dimensions rather than collapsing to a single solution.

---

## Key Findings

### Online Text Classification (GPT-OSS-120B on LawBench, S2D, USPTO-50k)

| Method | Accuracy (%) | Context Tokens (K) | Notes |
|---|---|---|---|
| Zero-shot | 29.5 | 0.0 | Baseline |
| Few-shot (32) | 37.3 | 12.3 | Fixed examples |
| ACE (hand-designed) | 40.9 | 50.8 | State-of-the-art manual |
| MCE (hand-designed) | 40.0 | -- | Manual context engineering |
| OpenEvolve | 43.3 | -- | Automated text optimizer |
| TTT-Discover | 45.6 | -- | Automated text optimizer |
| **Meta-Harness** | **48.6** | **11.4** | **+7.7 over ACE, 4x fewer tokens** |

### Ablation: Feedback Richness Matters

| Proposer Interface | Median Acc (%) | Best Acc (%) |
|---|---|---|
| Scores Only | 34.6 | 41.3 |
| Scores + Summary | 34.9 | 38.7 |
| **Meta-Harness (full traces)** | **50.0** | **56.7** |

### Retrieval-Augmented Math (200 IMO-Level Problems, 5 Held-Out Models)

| Method | Avg Accuracy (%) | Improvement |
|---|---|---|
| No Retriever | 34.1 | -- |
| Dense Retrieval | 32.2 | -1.9 (regresses on some models) |
| BM25 Retrieval | 37.5 | +3.4 |
| **Meta-Harness** | **38.8** | **+4.7 avg across all 5 models** |

### Agentic Coding (TerminalBench-2)

| Agent | Base Model | Pass Rate (%) |
|---|---|---|
| Terminus-KIRA | Opus 4.6 | 74.7 |
| **Meta-Harness** | **Opus 4.6** | **76.4 (#2 on leaderboard)** |
| ForgeCode | Opus 4.6 | 81.8 (#1) |
| Goose | Haiku 4.5 | 35.5 |
| **Meta-Harness** | **Haiku 4.5** | **37.6 (#1 on leaderboard)** |

- Meta-Harness matches the best prior text optimizers within ~4 evaluations (10x fewer than competitors)
- Discovered harnesses generalize to 9 unseen classification datasets (73.1% avg vs. 70.2% for ACE)
- The proposer exhibits causal reasoning: isolating structural bugfixes from prompt rewrites, pivoting toward additive modifications after identifying confounded regressions
- Discovered strategies are readable Python programs (e.g., "Draft Verification," "Label-Primed Query," four-route BM25 with difficulty reranking)

---

## Suggestions & Future Directions

1. **Co-Evolution of Harness and Model Weights** -- The natural next step is to jointly optimize the harness code and the underlying model parameters, letting strategy shape what the model learns and vice versa.

2. **Broader Proposer Agent Study** -- All experiments used a single strong proposer (Claude Code with Opus-4.6). Investigating how performance varies across different proposer agents and capability levels remains open.

3. **Inspectability Advantage of Code-Space Search** -- Unlike weight-space optimization, overfitting in code space is directly inspectable (brittle if-chains, hard-coded mappings are visible). The authors suggest this transparency is a practical advantage worth leveraging further.

4. **Transferability of Discovered Strategies** -- Discovered harnesses generalize across unseen datasets and base models, suggesting they capture broadly effective strategies. Future work could explore systematic transfer and reuse across domains.

5. **Scaling to Larger Search Budgets** -- The current setup uses ~60 harness evaluations over ~20 iterations. The relationship between search budget and discovery quality, and whether diminishing returns occur, is not yet characterized.

---

## Authors & Institutions

Yoonho Lee (Stanford), Roshen Nair (Stanford), Qizheng Zhang (Stanford), Kangwook Lee (KRAFTON), Omar Khattab (MIT), Chelsea Finn (Stanford)
