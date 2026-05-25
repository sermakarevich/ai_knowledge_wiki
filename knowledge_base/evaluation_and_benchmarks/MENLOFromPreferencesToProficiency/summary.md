# MENLO: From Preferences to Proficiency -- Evaluating and Modeling Native-Like Quality Across 47 Languages

**Paper:** [MENLO: From Preferences to Proficiency (Whitehouse et al., 2025)](https://arxiv.org/abs/2509.26601)

## Human Readable TL;DR

Imagine hiring thousands of native speakers from 47 countries to grade AI chatbot responses -- not just for grammar, but for whether the AI sounds like a local, uses appropriate cultural references, and gets local facts right. That's what MENLO does. The researchers then trained a smaller AI to do that grading job reliably, and finally used that AI grader to coach another AI into sounding more native-like. It's like hiring a language coach who also trained a robot to be the coach, so you can scale coaching to every language on Earth.

## TL;DR

MENLO introduces a massively multilingual evaluation framework and dataset (6,423 preference pairs, 81,014 human annotations across 47 language varieties) that decomposes native-like LLM response quality into four dimensions: fluency, tone, localized tone, and localized factuality. The paper shows that pairwise LLM judging with structured rubrics outperforms pointwise evaluation, that RL fine-tuning (GRPO) of judges surpasses SFT and frontier API models, and that these trained judges can directly serve as generative reward models to improve policy LLMs' multilingual proficiency.

---

## Problem & Motivation

Current multilingual LLM benchmarks either rely on translated English prompts (introducing "translationese" artifacts) or focus narrowly on task-oriented, short-form answers. Neither approach captures whether an LLM produces responses that feel genuinely native -- culturally grounded, stylistically local, and factually accurate in context. Existing datasets covering long-form quality (OMGEval, RECON, MM-EVAL) suffer from this translation bias, while cultural benchmarks test factual knowledge rather than conversational naturalness. MENLO addresses this gap with localized, human-written prompts instantiated with region-specific entities and annotated by in-country native speakers.

---

## Main Original Ideas

1. **Audience Design-Driven Prompt Localization** -- Drawing from sociolinguistics (Bell, 1984), prompt templates embed locale-specific placeholders (`[locale_nationality]`, `[locale_country]`) that force both annotators and LLMs to reason about a defined local audience, systematically eliciting culturally appropriate register.

2. **Four-Dimension Native-Like Quality Framework** -- Native-like quality is operationalized as: (1) Fluency (grammar, coherence, clarity), (2) Tone (helpfulness, engagement, writing style), (3) Localized Tone (culturally appropriate expressions, local sensitivity), and (4) Localized Factuality (correctness and completeness grounded in local context). Detailed 5-point Likert rubrics for each dimension achieve Krippendorff's α = 0.84.

3. **Pairwise LLM Judging with Structured Rubrics** -- Systematic comparison of zero-shot pointwise, few-shot pointwise, and zero-shot pairwise evaluation setups shows that pairwise judging is the most reliable evaluation paradigm for native-like quality, with gains up to +18.0% in preference accuracy over pointwise baselines.

4. **RL-Trained LLM Judges via GRPO** -- A composite reward signal (pointwise binary reward + smoothing for partial credit + preference bonus for relative ordering + formatting penalties) trains Qwen3-4B judges that outperform frontier API models (gpt-4.1, o3) on MENLO, with RL outperforming SFT -- especially critical for reasoning-oriented models where SFT without CoT degrades performance.

5. **Judges as Generative Reward Models** -- The RL-trained pairwise judge is repurposed to post-train a Qwen3-4B policy model via GRPO, demonstrating a closed-loop pipeline from preference annotation → judge training → policy improvement, achieving win rates of 63.8--77.9% over the base policy.

---

## Key Findings

| Setup | Macro-F1 gain vs. zero-shot pointwise | Preference Acc. gain |
|-------|--------------------------------------|----------------------|
| Few-shot pointwise | +~2% | small |
| Zero-shot pairwise | up to +12.4% | up to +18.0% |
| Rubrics (pointwise) | +4.3% avg | -- |
| RL vs. SFT (Qwen3-4B) | +4.0% | significant |

- **Best language (tr-TR):** 82.1% preference accuracy; **hardest (bn-BD):** 37.9% -- performance is far from uniform.
- **Localized Factuality** is the hardest dimension; RL yields limited gains, suggesting retrieval/tool integration is needed.
- **Multi-task training** (all four dimensions jointly) matches single-task optimization, offering practical efficiency.
- **LLM judges overestimate policy improvement magnitude** by ~0.5 points compared to human raters; RL-trained judges show less of this bias than zero-shot counterparts.
- Policy model post-training yields +0.78 to +1.16 average score improvement across three automated evaluators (Llama4-Scout-RL, Qwen3-32B, gpt-4.1), with human validation confirming positive but smaller absolute gains.

---

## Suggestions & Future Directions

1. **Retrieval-augmented judges for Localized Factuality** -- Integrating external knowledge sources or tool use to improve the hardest dimension, which current RL reward shaping cannot adequately address.
2. **Closing the LLM-human overestimation gap** -- Developing reward modeling techniques that better capture human perception subtleties, potentially via calibration on held-out human judgments.
3. **Scaling to more language varieties** -- 47 languages is a strong start but many under-resourced languages remain; future work should extend coverage especially for low-resource settings where English-only training generalizes poorly.
4. **Longer-context and multi-turn evaluation** -- Current prompts are single-turn; extending to dialogue contexts would better reflect real-world conversational quality.
5. **Releasing the dataset and models** -- The authors indicate intentions to share the MENLO benchmark to enable community-level advancement in multilingual evaluation.

---

## Authors & Institutions

Chenxi Whitehouse (Meta Superintelligence Labs), Sebastian Ruder (Meta Superintelligence Labs), Tony Zhiyang Lin (Meta Superintelligence Labs), Oksana Kurylo (Meta Superintelligence Labs), Haruka Takagi (Meta Superintelligence Labs), Janice Lam (Meta Superintelligence Labs), Nicolò Busetto (Meta Superintelligence Labs), Denise Diaz (Meta Superintelligence Labs)
