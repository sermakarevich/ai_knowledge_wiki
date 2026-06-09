# Latent Agents: A Post-Training Procedure for Internalized Multi-Agent Debate

**Paper:** [Latent Agents: A Post-Training Procedure for Internalized Multi-Agent Debate (Yi, Mueller, Lee, 2026)](https://arxiv.org/abs/2604.24881)

## Human Readable TL;DR

Imagine you have a committee of three experts who debate a problem before giving an answer -- it works well but takes forever and costs a lot. This paper teaches a single person to internally simulate that same debate in their head, arriving at the same quality answer much faster. Even more surprisingly, you can look inside the person's brain and find distinct "mental voices" corresponding to each original expert -- and you can turn those voices up or down. That means you can actually suppress a bad voice (say, one that tends to lie) without hurting the person's overall thinking ability.

## TL;DR

IMAD (Internalized Multi-Agent Debate) distills multi-agent debate into a single LLM via a two-stage pipeline: supervised fine-tuning on debate traces (structure learning), followed by GRPO reinforcement learning with decaying format rewards and progressive length clipping (internalization). The resulting model matches explicit multi-agent debate performance while using 79--94% fewer tokens. Activation analysis reveals that distinct agent reasoning styles are encoded as separable subspaces, enabling targeted behavioral steering with smaller performance tradeoffs than steering base models.

---

## Problem & Motivation

Multi-agent debate substantially reduces hallucinations and improves reasoning quality in LLMs, but requires running multiple models over many conversational turns -- generating verbose, expensive transcripts before a final answer emerges. This computational overhead makes debate impractical at scale. The paper asks: can the reasoning benefits of debate be internalized into a single model, and if so, what does that internalization look like mechanistically?

---

## Main Original Ideas

1. **Two-Stage Fine-Tuning Pipeline (IMAD)** -- Stage 1 uses SFT on full debate transcripts so the model learns the structural format of multi-agent debate. Stage 2 applies GRPO with two carefully designed dynamic rewards that progressively pressure the model to produce correct answers with less and less explicit debate scaffolding.

2. **Dynamic Reward Scheduling** -- A formatting reward (positive score for structural tags) decays over training, reducing incentive for verbose structure. A length-clipping reward R(y; l) = 1 if the correct answer appears within the first l tokens, with l shrinking from 2000 to 500. Together these rewards force internalization rather than mere transcription of debate.

3. **Agent-Specific Subspaces** -- Using Contrastive Activation Addition (CAA / difference-in-means), the authors extract steering vectors per agent type and show that IMAD models have interpretable, separable directions in activation space corresponding to Chain-of-Thought, Self-Critique, and Program-of-Thought reasoning styles. These directions don't meaningfully exist in base or SFT-only models.

4. **Behavioral Control via Steering** -- By inserting malicious agents (evil intent, hallucination tendency) into the debate training data, then negatively steering the corresponding subspace, the authors demonstrate cleaner suppression of harmful behaviors in IMAD models versus base models -- with smaller degradation of general task performance.

---

## Key Findings

| Model | Dataset | IMAD Acc. | Debate Acc. | Single Agent | IMAD Token % of Debate |
|---|---|---|---|---|---|
| LLaMA-3.1 8B | GSM8K | **85.20%** | 83.03% | 78.49% | 6.3% |
| LLaMA-3.1 8B | BBH | **58.53%** | 51.06% | 46.53% | ~10% |
| Qwen 2.5 7B | GSM8K | competitive | baseline | baseline | ~21% |
| Mistral Nemo 12B | MMLU-Pro | competitive | baseline | baseline | ~15% |

- IMAD uses **6.3--21.1% of Debate's tokens** (5--16x inference efficiency improvement)
- Agent subspace AUC improvements over base models: **+6.10% to +24.97%** (Agent 3 / Program-of-Thought showed the largest gain)
- Evil agent steering: IMAD achieves **complete suppression** at coefficients -3.0 to -5.0; base models retain residual harmful behavior
- Hallucination agent steering: IMAD suppresses the trait while maintaining better task performance across the steering range
- IMAD perplexity **decreases** under negative steering (on-distribution behavior), while base model perplexity increases (off-distribution)

---

## Suggestions & Future Directions

1. **Circuit-level mechanistic analysis** -- move from steering vectors to identifying specific attention heads and MLP circuits responsible for agent subspaces
2. **Naturally occurring traits** -- extend behavioral control beyond deliberately injected personas to traits that emerge organically in pretraining data
3. **More complex debate configurations** -- test hierarchical debate structures, more agents, additional rounds, and adversarial agent setups
4. **Longer-context reasoning** -- investigate whether internalization holds on tasks requiring extended reasoning chains beyond arithmetic
5. **Smaller models** -- the current results are strongest for 7B+ models; applicability to sub-7B models remains an open question

---

## Authors & Institutions

John Seon Keun Yi (Boston University), Aaron Mueller (Boston University), Dokyun Lee (Boston University)
