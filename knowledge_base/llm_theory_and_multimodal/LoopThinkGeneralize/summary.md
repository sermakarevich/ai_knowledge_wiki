# Loop, Think, & Generalize: Implicit Reasoning in Recurrent-Depth Transformers

**Paper:** [Loop, Think, & Generalize: Implicit Reasoning in Recurrent-Depth Transformers (Kohli et al., 2025)](https://arxiv.org/abs/2604.07822)

## Human Readable TL;DR

Imagine a student who can recall individual facts perfectly but fails on exam questions that require combining two facts they've never seen combined before. Standard AI models have this same problem -- they can store knowledge but struggle to chain it together on the fly. This paper tests a different kind of AI architecture that loops through its "thinking" layers multiple times, like re-reading notes before answering. It turns out that by repeating its processing steps, the model can learn to connect facts it has never seen connected, and even reason through longer chains than it was ever trained on -- just by thinking more iterations at answer time.

## TL;DR

This paper systematically studies recurrent-depth (looped) transformers on two compositional reasoning challenges: *systematic generalization* (composing facts never combined during training) and *depth extrapolation* (multi-hop reasoning beyond training depth). Using controlled synthetic knowledge graph experiments, the authors show that looped transformers overcome both limitations where vanilla transformers fail. Systematic generalization emerges via a three-stage grokking process, and depth extrapolation is unlocked by scaling inference-time recurrent iterations. An adaptive halting strategy (KL divergence + entropy) mitigates the "overthinking" degradation that occurs with excessive iterations.

---

## Problem & Motivation

Transformer-based LLMs store vast parametric knowledge but fail at *implicit* multi-hop reasoning -- combining that knowledge within a single forward pass without chain-of-thought prompting. The root cause is architectural: in fixed-depth transformers, knowledge retrieval is layer-specific, so the intermediate result of one reasoning hop is not reliably accessible for the next. Two concrete failure modes are studied:

1. **Systematic generalization** -- combining atomic facts that were never composed during training (OOD composition).
2. **Depth extrapolation** -- reasoning chains longer than the maximum depth seen during training.

These are studied in a clean, controlled synthetic setting (knowledge graphs, models trained from scratch) to isolate architectural effects from confounders in web-scale pretraining.

---

## Main Original Ideas

1. **Recurrent-Depth Transformer for Implicit Reasoning** -- A decoder-only GPT-2-style block of `L` layers is applied `R` times per forward pass (effective depth `D = L × R`). Zero-initialization of output projections stabilizes training under repeated weight reuse.

2. **Dynamic Iteration Training** -- Instead of a fixed `R`, the number of recurrent iterations is sampled per batch from a clipped Poisson distribution. This trains the model to reason robustly across varying compute budgets and was shown to outperform fixed-iteration training for depth extrapolation.

3. **Three-Stage Grokking for Systematic Generalization** -- Recurrent models pass through memorization → in-distribution generalization → systematic (OOD) generalization. The logit lens technique reveals that bridge (intermediate) entities become decodable before target entities, confirming the model learns to execute multi-hop steps sequentially within its recurrent depth.

4. **Inference-Time Compute Scaling for Depth Extrapolation** -- At inference, simply increasing the number of recurrent iterations beyond training-time `R` allows models to generalize to reasoning depths never seen during training. This requires no retraining or architectural changes.

5. **Adaptive Halting (KL + Entropy)** -- To prevent "overthinking" (performance degradation at excessive iterations), an adaptive stopping criterion combines KL divergence between consecutive iteration outputs and output entropy. This outperforms KL-only halting, which tends to stop too early.

---

## Key Findings

| Setting | Vanilla (R=1) | Looped (R=2) | Looped (R=4) | Looped (R=8) |
|---|---|---|---|---|
| Systematic generalization (OOD 2-hop) | Fails (~0%) | Non-trivial | Faster convergence | Best |
| Max learnable recursion depth (ID) | ~2-hop | ~4-hop | ~8-hop | ~16-hop |
| Depth extrapolation (beyond training) | No | Moderate | Yes (w/ inference scaling) | Yes (w/ inference scaling) |

- **Grokking order matters:** Systematic generalization only emerges *after* near-perfect in-distribution accuracy -- it cannot be shortcut.
- **Vanilla transformers recover bridge entities on OOD inputs but still fail the second hop**, confirming the architectural bottleneck is in composition, not retrieval.
- **Dynamic iteration achieves larger learnable recursion depths** than fixed iteration with the same maximum `R` budget, especially when training data is sufficiently complex.
- **Overthinking is real:** Logit margin peaks then monotonically declines with excess iterations. Dynamic models decay slower. More complex tasks peak at lower confidence.
- **Adaptive KL + entropy halting** allocates compute proportional to task complexity and avoids premature stopping that plagues KL-only methods.
- **Phase transition in learning:** Models spend most training time on low-hop tasks, then rapidly generalize to much harder multi-hop chains once the compositional rule is discovered.

---

## Suggestions & Future Directions

1. **Scale to pretrained LLMs** -- All experiments are on small models trained from scratch on synthetic data; authors acknowledge the need to validate findings on large pretrained models with realistic knowledge.
2. **Better adaptive halting** -- The KL + entropy heuristic is an improvement but not fully principled; learned or meta-learned halting policies are suggested.
3. **Understand the grokking mechanism** -- The paper describes the three-stage dynamic but does not fully explain *why* systematic generalization emerges late; mechanistic interpretability work is proposed.
4. **Overthinking mitigation beyond halting** -- Regularization or training-time objectives that explicitly discourage confidence decay at high iterations may help.
5. **Broader reasoning tasks** -- Extensions to natural language reasoning, arithmetic, and real-world KG benchmarks beyond the controlled synthetic setting.
6. **Hybrid architectures** -- Combining recurrent-depth blocks with non-recurrent layers to balance efficiency and compositional reasoning.

---

## Authors & Institutions

Harsh Kohli (Ohio State University), Srinivasan Parthasarathy (Ohio State University), Huan Sun (Ohio State University), Yuekun Yao (Ohio State University)
