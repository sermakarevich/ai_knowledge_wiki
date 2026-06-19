# On Training Large Language Models for Long-Horizon Tasks: An Empirical Study of Horizon Length

**Paper:** [On Training Large Language Models for Long-Horizon Tasks (Kim et al., 2026)](https://arxiv.org/abs/2605.02572)

## Human Readable TL;DR

Imagine teaching someone to solve a puzzle. If the puzzle takes 2 steps, they can learn quickly because they see what went wrong almost immediately. But if it takes 50 steps, by the time they fail, it's nearly impossible to know which of the 50 moves caused the problem. This paper shows that AI systems face exactly the same challenge: the longer the task, the more the training process breaks down -- not because the task is harder to reason about, but purely because of the distance to the goal. The fix? Let the AI take bigger "chunks" of action at once, or break the task into smaller checkpoints with rewards along the way.

## TL;DR

This paper identifies task horizon length (the minimum number of actions to reach a goal) as an independent bottleneck in training LLM agents via RL, distinct from reasoning complexity. Through controlled experiments on Sudoku and Rush Hour with fixed reasoning difficulty, increasing goal distance alone causes severe training instability. Two horizon reduction strategies -- macro actions (multi-atomic-action steps) and subgoal decomposition with dense rewards -- robustly stabilize training and improve generalization to unseen longer horizons.

---

## Problem & Motivation

LLMs deployed as interactive agents must complete tasks requiring many sequential steps. Existing work focuses on system-level optimizations (context engineering, workflow orchestration) or algorithmic improvements (SFT, RL variants like GRPO/PPO), but the intrinsic role of **horizon length** as a training bottleneck is largely ignored.

Three compounding problems arise as horizon grows:
1. Higher per-step accuracy is required (errors compound multiplicatively)
2. Exponential growth in state-action mapping complexity makes exploration intractable
3. Delayed, sparse rewards cause severe credit assignment ambiguity and high-variance gradient estimates

Prior work treats horizon as an external budget constraint rather than an intrinsic task property, leaving the question unanswered: *does horizon length itself destabilize LLM agent training?*

---

## Main Original Ideas

1. **Horizon as an independent training bottleneck** -- By constructing tasks where reasoning complexity is held constant and only goal distance varies (filtering to tasks a stronger model solves in a single step), the paper isolates horizon length as the sole variable. Training instability and collapse are shown to emerge purely from increased goal distance, not from harder reasoning.

2. **Mechanism of collapse** -- Long-horizon RL training causes a sharp rise in max-length response ratios, interpreted as policy diffusion: accumulating negative-advantage updates spread probability mass across irrelevant tokens, causing the model to generate incoherent, unbounded outputs.

3. **Macro actions as horizon reduction** -- Allowing the agent to emit multiple atomic actions per step (e.g., fill multiple Sudoku cells at once) reduces effective horizon. Flexible-length macro actions (policy-controlled granularity) outperform fixed-length variants and consistently prevent collapse on tasks where atomic actions fail.

4. **Subgoal decomposition with dense rewards** -- Decomposing the global goal into verifiable intermediate subgoals (e.g., completing a 3×3 Sudoku subgrid) provides dense reward signals, shortening effective credit assignment distance and enabling stable learning on long-horizon tasks.

5. **Horizon generalization** -- Models trained under reduced horizons (shorter goal distances) generalize effectively to longer, unseen horizon variants at inference time -- more so than models trained on long horizons directly. Curriculum learning (short → long) further amplifies this.

6. **Limits of RL generalization** -- Horizon generalization does not extend to qualitatively new reasoning primitives. RL refines and recombines existing capabilities; it does not acquire novel techniques beyond the training distribution.

---

## Key Findings

| Setting | Atomic Actions | Macro Actions | Subgoal Decomp. |
|---|---|---|---|
| Short horizon (L1-L2) Sudoku | Stable, improves | Faster convergence | -- |
| Medium horizon (L3-L4) Sudoku | **Collapse** | Stable, improves | Stable, improves |
| Long horizon (L5-L7) Sudoku | -- | Generalizes well | Generalizes well |
| WebShop (web interaction) | Unstable | Stable, higher success | -- |
| Qwen3-4B (larger model) | Still collapses | Prevents collapse | -- |
| GRPO optimizer | Still collapses | Prevents collapse | -- |

- Collapse mechanism: sharp spike in max-length response ratio, confirming policy diffusion hypothesis
- Flexible macro actions consistently outperform fixed-length macro actions
- Curriculum (short→long horizon training) yields significant gains on long-horizon test sets
- Larger model scale does NOT alleviate the horizon bottleneck
- Findings replicate across REINFORCE and GRPO optimizers

---

## Suggestions & Future Directions

1. **Automated subgoal discovery** -- The paper manually defines subgoals (Sudoku subgrids). Future work should develop methods to automatically identify verifiable intermediate goals for arbitrary tasks.
2. **Optimal action granularity search** -- Determining the right level of action abstraction (macro action length) is currently manual; principled methods for selecting granularity are needed.
3. **Beyond synthetic environments** -- Experiments are on Sudoku and Rush Hour (controlled) plus WebShop. Validation on broader real-world agentic benchmarks (coding, GUI, tool use) is a natural next step.
4. **Acquiring novel reasoning via RL** -- Since RL does not generalize to new techniques, exploring how to help LLMs acquire genuinely novel reasoning skills through training is an open question.
5. **Horizon-aware curriculum design** -- The curriculum learning results suggest a formal theory of horizon-aware training schedules could significantly improve sample efficiency.

---

## Authors & Institutions

Sunghwan Kim (Yonsei University, Microsoft Research), Junhee Cho (Yonsei University), Beong-woo Kwak (Yonsei University, Microsoft Research), Taeyoon Kwon (Yonsei University), Liang Wang (Microsoft Research), Nan Yang (Microsoft Research), Xingxing Zhang (Microsoft Research), Furu Wei (Microsoft Research), Jinyoung Yeo (Yonsei University)
