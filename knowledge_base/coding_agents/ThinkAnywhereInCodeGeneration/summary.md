# Think Anywhere in Code Generation

**Paper:** [Think Anywhere in Code Generation (Jiang et al., 2026)](https://arxiv.org/abs/2603.29957)

## Human Readable TL;DR

Imagine a student solving a hard coding problem. A typical "reasoning" model is like a student who thinks hard at the beginning, then writes the whole program straight through without stopping -- no matter what surprises come up. This paper teaches the model to behave like a better student: it plans up front, but it also pauses to think again at tricky spots mid-code (just before a return statement or a complicated assignment, for example). The model learns, on its own, where those "pause and think" moments should happen, and this leads to noticeably better code.

## TL;DR

Think-Anywhere lets an LLM invoke inline reasoning blocks (`<thinkanywhere>...</thinkanywhere>`) at arbitrary token positions during code generation, not just as an upfront `<think>` prefix. Training is a two-stage pipeline: cold-start SFT on ~5K samples distilled from Gemini 2.5 Flash, then outcome-based RL (GRPO) with a hierarchical reward combining a structural check for reasoning tags and a pass@1 correctness signal. On Qwen2.5-Coder-7B-Instruct it reaches 70.3% average pass@1 across LeetCode / LiveCodeBench / HumanEval / MBPP, beating GRPO (68.4%) and the base model (61.0%), and the learned reasoning triggers cluster at high-entropy tokens such as return/assignment statements.

---

## Problem & Motivation

Reasoning LLMs today do all their thinking up front -- a single `<think>` block before the answer. For code generation this is a poor fit: the full complexity of a problem often only reveals itself mid-implementation (edge cases, loop invariants, tricky return values). A one-shot upfront plan either over-thinks simple spots or under-thinks hard ones. The paper asks: can we let the model decide, per token, whether this is a moment that deserves more deliberation, and learn those decisions from reward?

---

## Main Original Ideas

1. **Think-Anywhere mechanism.** A generation format that interleaves code segments `c^(i)` with inline reasoning blocks `h^(i)` wrapped in `<thinkanywhere>...</thinkanywhere>`, alongside an optional upfront `<think>...</think>`. Final executable code is recovered by stripping all thinking blocks. This gives the model a discrete action -- "start thinking here" -- that it can place anywhere in the token stream.

2. **Two-stage cold-start + RLVR training.** Stage 1 is LoRA SFT on ~5K Gemini-2.5-Flash-distilled trajectories that demonstrate the interleaved format. Stage 2 is Group Relative Policy Optimization (GRPO) with outcome-based reward over 14K Skywork programming problems, letting the model autonomously explore *where* to think.

3. **Hierarchical structural + correctness reward.** Reward combines a binary structural check (are `<think>` and `<thinkanywhere>` blocks present?) weighted by α=0.1 with the primary signal `1[PassAllTests(c)]`. The structural term prevents format collapse during RL; the correctness term drives useful reasoning placement.

4. **Special-token variant with semantic-aware init.** Instead of text tags, the authors test a dedicated special token initialized from the averaged embeddings of "think", "any", "where", and delimiter tokens, trained in two sub-stages (embedding alignment, then joint fine-tune). It underperforms the text variant due to limited post-training data but points to a cleaner native-pretraining path.

5. **Emergent high-entropy reasoning placement.** Post-hoc analysis shows the trained model triggers `<thinkanywhere>` disproportionately at high-entropy positions -- most often right before assignment and return statements -- giving a human-interpretable view of where the model is uncertain.

---

## Key Findings

**Main results, Pass@1 (Qwen2.5-Coder-7B-Instruct backbone):**

| Method | LeetCode | LiveCodeBench | HumanEval | MBPP | Average |
|---|---|---|---|---|---|
| Base model | 50.6 | 34.3 | 88.4 | 70.7 | 61.0 |
| CodeRL+ | 63.3 | 36.9 | 90.9 | 76.2 | 66.8 |
| GRPO | 67.3 | 36.0 | 88.6 | 81.7 | 68.4 |
| **Think-Anywhere** | **69.4** | **37.2** | **91.5** | **82.9** | **70.3** |

**Cross-model generalization (absolute gain over the same-base baseline):**

- Qwen2.5-Coder-7B: 70.3% average, +9.3 over base
- Qwen2.5-Coder-1.5B: 54.5%, +13.9 over base
- LLaMA-3.1-8B: 43.8%, +5.4 over base

**Ablations on LeetCode Pass@1 (full = 69.4):**

- Only Cold-Start SFT: 47.9 (-21.5) -- RL is doing the heavy lifting
- Only RLVR: 63.4 (-6.0) -- cold-start still matters as a prior
- Line-level thinking: 67.2 (-2.2) -- token-level granularity wins
- No upfront `<think>`: 66.6 (-2.8) -- inline alone is not enough
- Padding thinking (fixed positions): 67.6 (-1.8) -- learned placement > fixed

**Cross-domain transfer (math reasoning, after code training):** modest AIME 2024 Pass@1 of 17.3% (Pass@5 32.9, Pass@10 40.2), AIME 2025 17.7/28.0/33.2, HMMT 2025 14.4/18.5/19.6 -- shows the mechanism carries some signal beyond code but is weaker outside the training domain.

**Qualitative:** trained models place `<thinkanywhere>` triggers at tokens with high next-token entropy, predominantly immediately before assignment statements and return statements.

---

## Suggestions & Future Directions

1. **Extend Think-Anywhere beyond code** to math, agentic, and general reasoning tasks, where mid-generation uncertainty is also non-uniform.
2. **Learn what *not* to think about** -- explicitly optimize the trade-off between reasoning depth and compute, so the model suppresses unhelpful reasoning rather than only adding helpful reasoning.
3. **Native pretraining integration** for the special-token variant, to close the gap with the text-tag version that benefits from the base model's existing token distribution.
4. **Acknowledged limitation**: the special-token variant underperforms due to insufficient post-training data; the text-tag form is the recommended default for now.

---

## Authors & Institutions

Xue Jiang, Tianyu Zhang, Ge Li, Mengyang Liu, Taozhi Chen, Zhenhua Xu, Wenpin Jiao, Zhi Jin, Yihong Dong (School of Computer Science, Peking University); Binhua Li, Yongbin Li (Tongyi Lab, Alibaba Group).
