# Composer 2 Technical Report

**Paper:** [Composer 2 Technical Report (Cursor Research Team, 2026)](https://cursor.com/resources/Composer2.pdf)

## Human Readable TL;DR

Imagine you're training a new employee to be a specialist programmer. First, you give them a massive library of code to study (like an apprenticeship), and then you let them practice on real projects with feedback on what they got right and wrong (like on-the-job training). That's essentially what Cursor did with Composer 2 -- they took an existing AI model, gave it intensive coding education, then had it practice solving real engineering problems thousands of times with a scoring system. The result is an AI coding assistant that's as good as the most expensive models from OpenAI and Anthropic, but significantly cheaper to run, because it's laser-focused on just one thing: writing and fixing code.

## TL;DR

Composer 2 is a domain-specialized coding agent built on Kimi K2.5 (1.04T parameters, 32B active MoE) through two training phases: continued pretraining on code-dominated data and large-scale asynchronous reinforcement learning in realistic Cursor harness environments. It achieves 61.3% on CursorBench (a new real-world benchmark from actual engineering sessions), 73.7% on SWE-bench Multilingual, and 61.7% on Terminal-Bench -- competitive with frontier models like GPT-5.4 and Opus 4.6 while being significantly cheaper at inference. The paper also introduces CursorBench, a continuously-evolving benchmark addressing key limitations of existing coding evaluations.

---

## Problem & Motivation

Existing coding agent benchmarks suffer from four critical limitations:
1. **Domain mismatch** -- benchmarks like SWE-bench focus narrowly on bug-fixing, missing the full spectrum of developer workflows
2. **Prompt over-specification** -- real developer requests are ambiguous, but benchmarks provide unnaturally explicit instructions
3. **Data contamination** -- public benchmarks leak into training data, artificially inflating scores (OpenAI suspended SWE-bench Verified reporting for this reason)
4. **Narrow evaluation scope** -- existing benchmarks only measure functional correctness, ignoring code quality, latency, cost, and interactive behavior

Additionally, general-purpose frontier models are expensive to serve for coding tasks. The paper investigates whether domain specialization through continued pretraining and RL can produce a model that matches frontier accuracy at lower cost.

---

## Main Original Ideas

1. **Two-Phase Domain Specialization Pipeline** -- Starting from Kimi K2.5, the model undergoes continued pretraining (32k then 256k context, plus SFT) followed by large-scale RL. Cross-entropy loss after pretraining is shown to be predictive of downstream RL performance.

2. **Asynchronous RL at Scale** -- A fully decoupled RL infrastructure spanning 3 GPU regions and 4 CPU regions, with in-flight weight updates (PipelineRL-style), MoE router replay to align inference and training, and delta-compressed weight synchronization over S3.

3. **CursorBench** -- A continuously-evolving benchmark derived from actual Cursor engineering team sessions. Tasks require a median of 181 lines changed (vs. 7-10 for SWE-bench) with under-specified prompts (median 390 chars vs. 1,185-3,055 for public benchmarks).

4. **Nonlinear Length Penalty** -- A concave-increasing reward penalty `C(x) = ((1 + kx)^(1-q) - 1) / (k(1-q))` that encourages the model to be fast on easy tasks while allowing extended reasoning on hard problems.

5. **Self-Summarization for Long Horizons** -- Extending Composer 1.5's technique, training rollouts chain multiple generations via learned summaries. RL naturally upweights good summaries and downweights ones that lose critical information.

6. **Novel NVFP4 Variant for MoE Training** -- Per-token FP4 scaling (instead of per-tensor) to prevent batch-variant numerical collapse and future-token information leakage during RL training on Blackwell GPUs.

7. **Anyrun Compute Platform** -- A Firecracker VM-based environment system supporting 500+ pod scheduling per second, filesystem/memory-level forking and snapshotting, and transparent egress control -- the same platform used in production.

---

## Key Findings

| Model | CursorBench | SWE-bench Multi. | Terminal-Bench |
|---|---|---|---|
| **Composer 2** | **61.3** | **73.7** | **61.7** |
| Composer 1.5 | 44.2 | 65.9 | 47.9 |
| Composer 1 | 38.0 | 56.9 | 40.0 |
| GPT-5.4 | 63.9 | 76.8 | 66.5 |
| GPT-5.3 Codex | 59.1 | 74.8 | 64.8 |
| Opus 4.6 High | 58.2 | 75.8 | 58.0 |
| Opus 4.5 High | 48.4 | 73.8 | 52.1 |
| Kimi K2.5 (base) | 36.0 | 65.1 | 47.3 |
| GLM-5 | 42.7 | 66.9 | 59.6 |

- Composer 2 achieves a **37% relative improvement** over Composer 1.5 and **61% over Composer 1** on CursorBench
- Both average and best-of-K performance improve during RL training -- contradicting the common view that RL merely concentrates probability mass on already-known trajectories
- Composer 2 achieves a **Pareto-optimal cost-accuracy frontier** -- similar inference cost to smaller/low-effort model variants while matching frontier accuracy
- Continued pretraining reliably predicts downstream RL performance (validated on Qwen3-Coder at three compute levels)
- Per-token NVFP4 scaling is critical -- per-tensor scaling causes RL training divergence; IEEE-compliant arithmetic (not fast-approximation) is required for FP4

| Base Model | FreshBench | State Tracking | Neg. Log-Likelihood |
|---|---|---|---|
| DeepSeek V3.2 | 68.9% | 66 | 11.75M |
| **Kimi K2.5** | **83.2%** | 86 | 13.81M |
| GLM-5 | 79.2% | 92 | 14.11M |
| GPT-5.4 | 92.5% | 103 | -- |
| Claude 4.6 Opus | 88.9% | 65 | -- |

---

## Suggestions & Future Directions

1. **Scaling further** -- Results are "optimistic on the future improvement available through further scaling." The model (1.04T params, 32B active) is likely smaller than other proprietary models of similar ability, suggesting room for architectural and algorithmic development.

2. **Longer-horizon tasks** -- The scope of coding agents is expanding from interactive problems to tasks requiring hours of human time. Future Composer iterations will focus on algorithms that effectively utilize longer-term training signal and infrastructure to support faithful long-horizon problems.

3. **Improving intelligence and coherence** -- Despite strong results, there are "many cases where the model shows intelligence or coherence behaviors that can be clearly improved."

4. **Continued pretraining-RL connection** -- The relationship between pretraining loss and downstream RL performance is described as "an area of active research."

5. **Evolving CursorBench** -- The benchmark is continuously updated as developer workflows evolve and agent capabilities improve, ensuring evaluations remain aligned with real-world difficulty.

---

## Authors & Institutions

Cursor Research Team: Aaron Chan, Ahmed Shalaby, Alexander Wettig, Aman Sanger, Andrew Zhai, Anurag Ajay, Ashvin Nair, Charlie Snell, Chen Lu, Chen Shen, Emily Jia, Federico Cassano, Hanpeng Liu, Haoyu Chen, Henry Wildermuth, Jacob Jackson, Janet Li, Jediah Katz, Jiajun Yao, Joey Hejna, Josh Warner, Julius Vering, Kevin Frans, Lee Danilek, Less Wright, Lujing Cen, Luke Melas-Kyriazi, Michael Truell, Michiel de Jong, Naman Jain, Nate Schmidt, Nathan Wang, Niklas Muennighoff, Oleg Rybkin, Paul Loh, Phillip Kravtsov, Rishabh Yadav, Sahil Shah, Sam Kottler, Alexander M Rush, Shengtong Zhang, Shomil Jain, Sriram Sankar, Stefan Heule, Stuart H. Sul, Sualeh Asif, Victor Rong, Wanqi Zhu, William Lin, Yuchen Wu, Yuri Volkov, Yury Zemlyanskiy, Zack Holbrook, Zhiyuan Zhang -- all at Cursor.
