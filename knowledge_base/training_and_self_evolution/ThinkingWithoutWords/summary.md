# Thinking Without Words: Efficient Latent Reasoning with Abstract Chain-of-Thought

**Paper:** [Thinking Without Words: Efficient Latent Reasoning with Abstract Chain-of-Thought (Ramji, Naseem, Astudillo, 2025)](https://arxiv.org/abs/2604.22709)

## Human Readable TL;DR

When you ask a smart person a hard question, they might scribble a bunch of notes before answering. AI models do something similar -- they "write out" their thinking in plain English before giving a response, which takes a lot of time and energy. This paper asks: what if the AI could jot down its thoughts in a secret shorthand nobody can read, but that's much faster? The answer is yes -- the AI invents its own compact symbol language during training, uses it to think with 10x fewer symbols, and still gets the right answers.

## TL;DR

This paper introduces **Abstract Chain-of-Thought (Abstract-CoT)**, a post-training method that replaces verbose natural-language reasoning traces with a short sequence of discrete, abstract tokens drawn from a reserved vocabulary. A two-stage recipe (bottlenecked SFT warm-up + GRPO reinforcement learning) teaches an LLM to develop and use this non-verbal scratchpad. On Qwen3 and Granite models, Abstract-CoT matches or beats verbal CoT performance while using **4x--12x fewer reasoning tokens**.

---

## Problem & Motivation

Standard Chain-of-Thought (CoT) prompting makes LLMs generate long natural-language rationales before answering. This is expensive at inference time, inflates RL trace lengths during training, and may not faithfully reflect actual internal reasoning. The paper asks whether short sequences of new, abstract discrete tokens can substitute for verbose verbal rationales -- achieving the same reasoning benefit at a fraction of the token cost, purely through post-training without re-pre-training.

---

## Main Original Ideas

1. **Abstract Token Vocabulary** -- The tokenizer is extended with `M` new reserved tokens (e.g., `<TOKEN_A>`) plus `<beginabstract>`/`<endabstract>` delimiters. The model generates a bounded sequence `z` from this codebook as a latent scratchpad before producing its answer.

2. **Information Bottleneck via Block Attention Masking** -- During SFT warm-up, a custom attention mask forces the answer to attend *only* to the prompt and the abstract tokens -- not to the verbal CoT. This compels abstract tokens to compress and transmit all reasoning-relevant information, creating a true discrete latent bottleneck.

3. **Two-Phase Policy Iteration Warm-Up** -- Stage 1 alternates between (a) bottlenecked SFT using the verbal CoT as a teacher signal, and (b) self-distillation where the model learns to produce abstract traces from the prompt alone, iteratively for T rounds. This solves the cold-start problem of randomly initialized abstract embeddings.

4. **RL Fine-Tuning Over Discrete Codebook (GRPO)** -- Stage 2 applies GRPO with a generative reward model to further refine the abstract-token policy. Constrained decoding keeps outputs within the abstract vocabulary; KL regularization anchors to the warm-started reference policy.

5. **Emergent "Reasoning Language"** -- The distribution over abstract token usage evolves during RL from uniform into a power-law (Zipf-like) pattern, suggesting the model spontaneously develops structured, reusable reasoning vocabulary analogous to natural language.

---

## Key Findings

| Model | Benchmark | Verbal CoT tokens | Abstract-CoT tokens | Efficiency gain | Performance delta |
|---|---|---|---|---|---|
| Qwen3-8B | MATH-500 | ~high | ~low | **10.4x** | comparable |
| Qwen3-4B | MATH-500 | ~high | ~low | **11.6x** | comparable |
| Qwen3-8B | AlpacaEval-LC | baseline | fewer | **2.2x** | **+2.4 pp win-rate** |
| Qwen3-4B | AlpacaEval-LC | baseline | fewer | **1.9x** | **+1.6 pp win-rate** |
| Granite 4.0 Micro | AlpacaEval-LC | baseline | fewer | **2.0x** | **+1.6 pp win-rate** |
| Qwen3-8B | HotpotQA | baseline | fewer | **4.0x** | comparable |
| Qwen3-8B | AIME'25 | baseline | fewer | **2.7x** | comparable |
| Qwen3-8B | GPQA-Diamond | baseline | fewer | **7.9x** | comparable |

- **Cold-start RL fails**: applying RL directly to untrained abstract tokens consistently underperforms the base instruction-tuned model -- warm-up is mandatory.
- **Pause tokens underperform**: filler token baselines degraded performance, confirming that pre-training is typically required for them to work.
- **Permutation sensitivity**: shuffling abstract token order degrades performance (~7.8 pts on MATH-500), confirming learned compositional structure.
- **Truncation robustness**: truncating abstract traces to 32 tokens causes less performance drop than truncating verbal CoT, demonstrating compact efficiency.
- **Optimal vocabulary size**: M=64 abstract tokens performs best; beyond this, gains plateau or regress slightly.

---

## Suggestions & Future Directions

1. **Budget-adaptive reasoning** -- Develop mechanisms to dynamically adjust abstract sequence length based on task difficulty or a user-specified compute budget.
2. **Hierarchical codebooks** -- Explore organizing abstract tokens hierarchically to encode reusable reasoning subroutines, potentially improving efficiency further.
3. **Cold-start scaling** -- Investigate whether drastically increased RL compute can bootstrap useful abstract embeddings without the warm-up stage.
4. **Interpretability of the abstract language** -- Study how individual tokens acquire meaning, which concepts they encode, and whether the Zipf-like distribution reveals structure analogous to morphology or syntax.
5. **Long-horizon tasks** -- Extend Abstract-CoT to agentic or multi-turn settings where reasoning must span many steps.

---

## Authors & Institutions

Keshav Ramji (IBM Research AI), Tahira Naseem (IBM Research AI), Ramón Fernandez Astudillo (IBM Research AI)
