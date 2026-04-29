# Think Anywhere in Code Generation

**Paper:** [Think Anywhere in Code Generation (Jiang et al., 2026)](https://arxiv.org/abs/2603.29957)

## Human Readable TL;DR

When a programmer tackles a hard problem, they don't plan everything upfront and then code on autopilot -- they stop and think at tricky spots as they go. Current AI coding assistants do the opposite: they think first, then write code without pausing. This paper teaches AI to think mid-code, inserting small reasoning checkpoints exactly where the code gets complicated. The result is more accurate code generated with fewer total words -- the AI thinks where it matters and skips thinking where it doesn't.

## TL;DR

THINK-ANYWHERE introduces on-demand reasoning blocks (`<thinkanywhere>`) that LLMs can insert at any token position during code generation, rather than reasoning exclusively upfront. Training combines SFT cold-start (using Gemini 2.5 Flash-generated trajectories) with GRPO reinforcement learning using a hierarchical reward (structural + correctness). On four benchmarks, the method achieves 70.3% average pass@1 (+9.3% over base), surpasses all reasoning-enhanced baselines, and generalizes to math reasoning despite training only on code.

---

## Problem & Motivation

Upfront thinking (the o1/DeepSeek-R1 paradigm) forces all deliberation before code generation begins. This is insufficient because:

1. **Complexity emerges during coding** -- edge cases like index-out-of-bounds errors are often invisible at planning time but obvious mid-implementation.
2. **Effort is misallocated** -- boilerplate code gets as much pre-thinking as complex algorithms. No dynamic adjustment to local difficulty.

Prior interleaved approaches (e.g., Interleaved Thinking, TwiG) require reasoning at every sub-step, creating unnecessary overhead. THINK-ANYWHERE aims for on-demand, context-sensitive reasoning -- think when needed, skip when not.

---

## Main Original Ideas

1. **On-Demand Mid-Code Reasoning** -- Introduces `<thinkanywhere>` tokens that the model autonomously inserts at any token position within generated code. The final executable code is the concatenation of code segments after stripping all thinking blocks, preserving validity.

2. **Two-Stage Training Pipeline** -- Cold-start SFT (using ~5,000 Gemini-generated examples) teaches the structural format; subsequent GRPO reinforcement learning teaches *when and where* to reason. Ablations show neither stage alone is sufficient.

3. **Dedicated Reasoning Trigger Token (THINK-ANYWHERE*)** -- A single-token variant replacing multi-token delimiters, initialized via semantic-aware embedding: `0.5 * mean(e_think, e_any, e_where) + 0.5 * e_<im_start/end>`. Trained in two stages: embedding alignment first, then joint LoRA fine-tuning.

4. **Hierarchical Reward Function** -- `R(y) = 0.1 * R_struct + 0.9 * R_correct`. The structural reward enforces that the model actually invokes on-demand blocks (not just upfront thinking); the correctness reward drives code quality via test execution.

5. **Entropy-Driven Position Selection** -- Analysis reveals the model places `<thinkanywhere>` blocks at positions with high token entropy (measured when thinking is disabled), providing empirical evidence that the model learns to identify genuinely uncertain positions rather than inserting thinking arbitrarily.

---

## Key Findings

### Main Results (Pass@1, greedy)

| Method | HumanEval | MBPP | LeetCode | LiveCodeBench | Avg |
|---|---|---|---|---|---|
| Base Model (Qwen2.5-Coder-7B) | -- | -- | -- | -- | 61.0% |
| GRPO | -- | -- | -- | -- | ~64% |
| CoT / Self-Planning | -- | -- | -- | -- | <64% |
| Interleaved Thinking | -- | -- | -- | -- | <64% |
| **THINK-ANYWHERE** | **--** | **--** | **--** | **--** | **70.3%** |

*(+9.3% absolute improvement over base model, state-of-the-art among 7B-scale methods)*

### Cross-Domain Generalization (Math, trained only on code)

| Benchmark | Base | GRPO | THINK-ANYWHERE |
|---|---|---|---|
| AIME 2024 (pass@1) | 5.3% | 6.0% | **17.3%** |
| AIME 2025 | lower | lower | significant gain |
| HMMT 2025 | lower | lower | significant gain |

### Ablation (LeetCode pass@1 drops vs. full method)

| Variant | Drop |
|---|---|
| Only Cold Start (no RL) | -21.5% |
| Only RLVR (no Cold Start) | -6.0% |
| Line-level thinking (not token-level) | -2.2% |
| No upfront thinking block | -2.8% |
| Padding thinking content | -1.8% |

- Thinking invoked most at **assignment statements** (complex computations) and **return statements** (final output correctness)
- THINK-ANYWHERE generates **fewer total tokens** than GRPO and CoT -- the shorter upfront phase more than offsets the added in-code blocks
- Performance gap over GRPO **widens with larger k** in pass@k, indicating a higher capability ceiling

---

## Suggestions & Future Directions

1. **Extend to other domains** -- Apply THINK-ANYWHERE to scientific discovery, complex decision-making, and multi-step reasoning tasks beyond code.
2. **Learn "what not to think"** -- Future work should optimize the reasoning/cost tradeoff by teaching models to skip thinking even more aggressively on trivial segments.
3. **Pre-training integration** -- Natively incorporating THINK-ANYWHERE special tokens during large-scale pre-training (rather than post-training only) could unlock stronger capabilities.
4. **Scale to larger models** -- Experiments focus on 1.5B--7B; validating gains at 70B+ scale is an open question.
5. **Richer reward signals** -- Beyond binary correctness, partial credit rewards for near-correct solutions could improve RL training stability and sample efficiency.

---

## Authors & Institutions

Xue Jiang (Peking University, Tongyi Lab/Alibaba), Tianyu Zhang (Peking University), Ge Li (Peking University, Tongyi Lab/Alibaba), Mengyang Liu (Peking University), Taozhi Chen (Peking University), Zhenhua Xu (Peking University), Binhua Li (Tongyi Lab/Alibaba), Wenpin Jiao (Peking University), Zhi Jin (Peking University), Yongbin Li (Tongyi Lab/Alibaba), Yihong Dong (Peking University, Tongyi Lab/Alibaba)
