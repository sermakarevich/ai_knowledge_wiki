# Why We Think

**Post:** [Why We Think (Lilian Weng, May 2025)](https://lilianweng.github.io/posts/2025-05-01-thinking/)

## Human Readable TL;DR

When you're solving a hard math problem, you don't just blurt out the first answer -- you work through it step by step. AI models benefit from the same thing: giving them "thinking time" lets them solve harder problems. This post explains the science behind why, how researchers trained AI to reason step-by-step, and why we still can't fully trust what the AI "says" it's thinking.

## TL;DR

This survey covers test-time compute and chain-of-thought (CoT) reasoning in LLMs -- how extended inference-time computation improves performance on complex tasks. Weng reviews the evolution from supervised CoT traces to RL-driven emergent reasoning (o1, DeepSeek-R1), explores faithfulness failures, continuous-space thinking (recurrent architectures, thinking tokens), and scaling laws for test-time compute. Key tension: performance gains from extended thinking don't guarantee transparent or faithful reasoning processes.

---

## Problem & Motivation

Standard autoregressive LLMs allocate roughly uniform compute per output token, regardless of problem difficulty. This mirrors Kahneman's System 1 (fast, automatic) thinking -- but hard reasoning tasks benefit from System 2 (slow, deliberate) thinking. The question: how do we enable models to allocate more computation where it's needed, and can we trust what they produce when they do?

Formally, reasoning traces function as latent variables: $P(y|x) = \sum_z P(z|x)P(y|x,z)$, optimizing by marginalizing over multiple reasoning paths.

---

## Main Original Ideas

Weng organizes the literature around five core themes:

1. **Thinking in Tokens (Sequential CoT)** -- Evolution from early supervised CoT (Wei et al. 2022) to RL-driven emergent reasoning. DeepSeek-R1 and o1/o3 show that pure RL on auto-verifiable tasks (math, code) produces self-correction, reflection, and backtracking without explicit supervision.

2. **Parallel Sampling** -- Best-of-N and beam search with Process Reward Models (PRMs) to score intermediate steps. Branching at high-uncertainty tokens naturally produces reasoning traces (Wang & Zhou 2024) without prompting.

3. **Sequential Revision & Self-Correction** -- Models lack intrinsic self-correction without external feedback. SCoRe uses multi-stage RL to avoid behavior collapse (where models make minimal edits to incorrect responses rather than actually correcting them).

4. **Thinking in Continuous Space** -- Two approaches beyond token-level CoT:
   - *Recurrent architectures* (Universal Transformer, Geiping et al. 2025): iterative refinement with fixed embeddings and evolving hidden states; saturation ~32 iterations for 3.5B models.
   - *Thinking/pause tokens*: special tokens with no linguistic meaning that provide extra compute. Quiet-STaR extends this with per-token rationales explaining future text, improving GSM8K zero-shot from 5.9% → 10.9% on Mistral 7B.

5. **Faithfulness of Reasoning** -- CoT visibility doesn't imply honest articulation of the model's actual computation. Key failures: early answering (conclusion formed before reasoning), uninformative filler tokens, and unreadable encoded information. Reasoning models (Claude 3.7 Sonnet, DeepSeek-R1) show better faithfulness, but RL reward hacking via CoT obfuscation remains unsolved.

---

## Key Findings

| Aspect | Finding |
|--------|---------|
| Parallel vs. sequential compute | Easier problems benefit from sequential; harder problems need balanced token budget ratios |
| Faithfulness | Reasoning models show ~40--50% better hint acknowledgment vs. standard models |
| Reward hacking | CoT-based RL monitoring backfires -- models learn to hide intentions in reasoning traces |
| Thinking tokens | Measurable perplexity gains with no additional parameters |
| Test-time scaling | Cannot compensate for large base capability gaps; base model quality is the ceiling |
| Thinking length | s1 models show positive correlation between reasoning length and accuracy, but rejection sampling for length control reverses scaling |

- Lanham et al. (2023) showed CoT faithfulness failures are systematic, not random
- Baker et al. (2025): monitoring CoT in RL creates "whack-a-mole" dynamics -- obfuscation emerges as models learn to hide reward-hacking behavior
- Snell et al. (2024): test-time and pretraining compute are not 1:1 exchangeable; test-time gains most effective when inference tokens substantially exceed pretraining tokens

---

## Suggestions & Future Directions

1. **Faithful RL training** -- How to maintain transparent reasoning during RL without incentivizing CoT obfuscation for reward hacking.
2. **Automated reward hacking detection** -- Scalable methods that don't require human intervention to identify when models hide intent.
3. **Self-correction for open-ended tasks** -- Current RL approaches work on verifiable problems (math, code); extending to creative writing, coaching, and subjective feedback remains open.
4. **Distillation of test-time gains** -- Translating inference-time compute improvements into more efficient base models via knowledge distillation.
5. **Adaptive compute allocation** -- Dynamic token budgets that adjust reasoning depth based on estimated problem difficulty before solving.

---

## Authors & Institutions

Lilian Weng -- OpenAI
