# Meta-Harness: End-to-End Optimization of Model Harnesses

**Paper:** [Meta-Harness: End-to-End Optimization of Model Harnesses (Lee et al., 2025)](https://arxiv.org/abs/2603.28052)

## Human Readable TL;DR

When you use an AI chatbot, its performance depends not just on the AI brain itself but also on all the surrounding instructions, memory systems, and workflows that tell the brain what to look at and how to respond -- like a jockey riding a racehorse. Right now, humans manually tweak these "jockey" programs through trial and error. This paper builds a system that automatically designs better jockeys by letting an AI coding assistant review all past attempts (including detailed logs of what went wrong), figure out the root cause of failures, and write improved code. The result: automatically discovered strategies that beat hand-crafted ones across classification, math reasoning, and coding tasks.

## TL;DR

Meta-Harness automates LLM harness engineering -- the design of context management, retrieval, and prompting logic surrounding a frozen model -- via an outer-loop search where an agentic proposer (Claude Code with Opus) iteratively inspects full, uncompressed execution traces stored on a filesystem and rewrites harness code. Across text classification, retrieval-augmented math reasoning, and agentic coding benchmarks, discovered harnesses outperform hand-engineered and prior text-optimization baselines while using fewer context tokens.

---

## Problem & Motivation

LLM performance is heavily influenced by the "harness" -- the external code governing prompt construction, memory management, retrieval, and tool use. A single model's output can vary by up to 6x depending on its harness. Yet harness design remains a manual, iterative process relying on human intuition.

Existing text optimization methods fail at this task because they provide compressed feedback (scalar scores, short summaries, or limited context windows). Harnesses are stateful programs where early decisions cascade into long-horizon failures, requiring rich diagnostic information -- full source code, execution traces, and per-instance scores -- to diagnose root causes. Prior optimizers cap feedback at thousands or tens of thousands of tokens per iteration; a single harness evaluation can produce up to 10 million tokens of diagnostic data.

---

## Main Original Ideas

1. **Filesystem-as-feedback-channel.** Instead of summarizing prior attempts into compressed signals, Meta-Harness stores complete source code, evaluation scores, and raw execution traces for every candidate on a filesystem. The proposer selectively inspects this data using standard CLI tools (`grep`, `cat`), enabling causal reasoning over arbitrarily long histories.

2. **Agentic proposer with unrestricted code-space search.** The proposer is a full coding agent (Claude Code) that autonomously decides what to inspect, which failure modes to address, and how to modify harness code -- including algorithmic rewrites of retrieval, memory, and prompt-construction logic. No hard-coded search heuristics constrain the modification space.

3. **End-to-end harness optimization loop.** A single outer loop initializes a population of harnesses, evaluates them, logs everything to the filesystem, queries the proposer for new candidates, and repeats. After N iterations the Pareto frontier (trading off accuracy vs. context cost) is returned.

4. **Multi-objective Pareto selection.** When multiple objectives matter (e.g., accuracy and context token cost), candidates are ranked by Pareto dominance, surfacing a frontier of trade-off options rather than a single solution.

---

## Key Findings

### Text Classification (LawBench, S2D, USPTO-50k)

| Method | Accuracy | Context Tokens |
|---|---|---|
| Zero-shot | 26.3% | 0.5K |
| Few-shot (8) | 33.0% | 4.2K |
| ACE (hand-designed) | 40.9% | 50.8K |
| MCE (hand-designed) | 40.0% | -- |
| OpenEvolve | 43.3% | -- |
| TTT-Discover | 45.6% | -- |
| **Meta-Harness** | **48.6%** | **11.4K** |

- Outperforms ACE by +7.7 points with **4x fewer tokens**.
- Matches OpenEvolve/TTT-Discover accuracy in ~4 evaluations (10x fewer).
- Best search-set accuracy reaches 56.7%, +10 points over prior optimizers.
- Generalizes to 9 unseen OOD datasets (73.1% avg vs. 70.2% for ACE).

### Retrieval-Augmented Math (IMO-level, 200 problems)

- Discovered retrieval harness improves accuracy by +4.7 points averaged across 5 held-out models vs. no-retrieval baseline.
- Outperforms BM25 by +1.3 points on average, avoids regressions seen with dense retrieval.
- The discovered harness is a compact four-route BM25 program with subject-specific retrieval, deduplication, and difficulty reranking.

### Agentic Coding (TerminalBench-2, 89 tasks)

| Agent | Model | Pass Rate |
|---|---|---|
| Terminus-KIRA (hand-engineered) | Opus 4.6 | 74.7% |
| **Meta-Harness** | **Opus 4.6** | **76.4%** |
| Goose (best prior) | Haiku 4.5 | 35.5% |
| **Meta-Harness** | **Haiku 4.5** | **37.6%** |

- Ranks #2 on the Opus 4.6 leaderboard and #1 on the Haiku 4.5 leaderboard.

### Ablation: Feedback Richness

| Feedback Level | Median Acc. | Best Acc. |
|---|---|---|
| Scores only | 34.6% | 41.3% |
| Scores + summary | 34.9% | 38.7% |
| **Full Meta-Harness** | **50.0%** | **56.7%** |

Full trace access is critical -- compressed feedback severely limits optimization quality.

---

## Suggestions & Future Directions

1. **Co-evolution of harnesses and model weights.** Current work optimizes harnesses around a frozen model; jointly evolving strategy (harness) and learning (weights) could yield further gains.
2. **Broader proposer diversity.** Exploring different proposer agents beyond Claude Code may reveal complementary search strategies and reduce proposer-specific biases.
3. **Scaling to larger harness populations.** More parallel evaluations and longer search horizons could discover even stronger harnesses, especially for complex agentic tasks.
4. **Inspectability as a feature.** Since optimization occurs in code space, any discovered overfitting or brittle logic is human-readable and auditable -- a transparency advantage over weight-space optimization that could be further leveraged for safety and trust.
5. **Generalization to other software engineering tasks.** The paradigm of providing coding agents with structured historical data for iterative optimization may transfer beyond harness engineering to broader automated software development.

---

## Authors & Institutions

Yoonho Lee (Stanford), Roshen Nair (Stanford), Qizheng Zhang (Stanford), Kangwook Lee (KRAFTON), Omar Khattab (MIT), Chelsea Finn (Stanford)
