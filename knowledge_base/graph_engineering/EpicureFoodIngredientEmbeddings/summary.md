# Epicure: Navigating the Emergent Geometry of Food Ingredient Embeddings

**Paper:** [Epicure: Navigating the Emergent Geometry of Food Ingredient Embeddings (Radzikowski & Chen, 2026)](https://arxiv.org/abs/2605.22391)

## Human Readable TL;DR

Imagine a map of ingredients where similar foods cluster together -- chicken near beef, miso near soy sauce. This paper builds three versions of that map from 4 million recipes across the world, where each version tilts more toward "what do foods taste like chemically" versus "what do chefs put together in real dishes." They also build two ways to navigate the map: find the nearest neighbors, or "rotate" an ingredient toward a cuisine style (like rotating rice toward South Asian cooking, which naturally surfaces curry leaf and fenugreek). The goal is a tool that chefs can use to discover creative substitutions and pairings.

## TL;DR

Epicure is a family of three Metapath2Vec food ingredient embeddings (Cooc, Core, Chem) trained on a 4.14M-recipe multilingual corpus normalized to 1,790 canonical ingredients. The three siblings share architecture but differ only in their random-walk schema, making the chemistry-vs-recipe-context trade-off an explicit, controllable design axis. Linear probes recover 27 sensory/nutrient directions and 8 cuisine macro-regions; FastICA uncovers 150--200 stable emergent "culinary modes" per model; and SLERP direction arithmetic enables continuous navigation between cultural poles in 300-D space.

---

## Problem & Motivation

Prior work (FlavorGraph) hardcoded chemistry and co-occurrence signal into a single embedding with no knob to control the trade-off. It was also English-centric. Downstream chef-facing tools need representations where the chemistry-vs-culture axis is explicit and navigable -- not a fixed black box. This paper asks: can that trade-off become a named design variable, and what navigation operators does a well-structured ingredient embedding support?

---

## Main Original Ideas

1. **Multilingual canonical corpus** -- 4.14M recipes from 11 sources across 7+ languages (English, Chinese, Russian, Vietnamese, Spanish, Turkish, Indonesian, German, Indian-English), normalized from ~200K raw strings to 1,790 canonical ingredient entries via an LLM pipeline (Claude Opus + Gemini embeddings).

2. **Three sibling embeddings as a controlled axis** -- Epicure-Cooc (co-occurrence only), Epicure-Core (blended), and Epicure-Chem (chemistry only) share all architecture and hyperparameters; only the Metapath2Vec walk schema differs. This turns the chemistry-vs-context question into a named experimental variable.

3. **Typed FlavorDB compound graph** -- 80,019 ingredient-compound edges with 2,247 compound nodes typed across 15 flavor categories (compounds replicated per category to enable type-specific metapaths, extending FlavorGraph's single-type convention).

4. **Stratified direction quality evaluation** -- 27 supervised probe directions (14 compound-feature categories, 5 held-out basic tastes, 8 USDA macronutrients) + 8 cuisine macro-region directions under 5-fold cross-validation stratified by distance from the training signal.

5. **Multi-seed-stable emergent factor discovery** -- FastICA on food-group-residualized embeddings with Hungarian matching across 10 random seeds; GMM partitioning of high-quartile ingredients per factor yields 150--200 named culinary modes per model with quantified coherence vs. random-pair baselines.

6. **SLERP direction arithmetic operators** -- Continuous rotation of a seed ingredient toward a supervised pole vector (cuisine region, taste, nutrient) or an emergent mode pole via angle θ, enabling smooth interpolation from seed-dominated to target-dominated retrieval on the same 300-D space.

---

## Key Findings

| Metric | Cooc | Core | Chem |
|---|---|---|---|
| Participation ratio (isotropy) | 173.6 | 94.2 | 183.1 |
| Avg pairwise cosine | 0.099 | 0.349 | 0.117 |
| Food-group NMI (n=1,560) | 0.205 | 0.235 | 0.226 |
| Cuisine-region NMI (n=986) | 0.457 | 0.456 | 0.432 |
| Compound-feature probe ρ | 0.28 | 0.40 | **0.46** |
| Held-out basic taste probe ρ | 0.32 | 0.42 | **0.47** |
| USDA macronutrient probe ρ | 0.41 | 0.45 | **0.49** |
| Cuisine region Cohen's d | 2.43 | 2.70 | **3.07** |
| Emergent modes (ICA) | 150 | 193 | 200 |
| Mode coherence vs. baseline | 0.611 vs. 0.097 | **0.833** vs. 0.348 | 0.703 vs. 0.115 |

- Chem wins on 26/27 supervised probes and all 8 cuisine region directions -- chemistry signal is the stronger linear organizer.
- Core achieves tighter emergent mode coherence (0.833 vs. 0.703/0.611), despite being less isotropic.
- SLERP at θ=30° on rice + South-Asian direction surfaces curry leaf, urad dal, chana dal, fenugreek seed across all models; at θ=60° different seeds (chicken, beef) rotating toward Mexican collapse onto nearly identical Tex-Mex neighborhoods.

---

## Suggestions & Future Directions

1. **Continuous chemistry-vs-context mixing** -- Replace the three discrete siblings with a parameterizable walk-mixing family tunable at inference time.
2. **Richer operator set** -- Intra-mode interpolation, multi-direction blends, and constrained traversal (e.g., rotate toward Mediterranean while staying in the dairy mode).
3. **Cross-modal grounding** -- Extend SLERP into recipe-text, image, or sensory-descriptor spaces via the shared canonical vocabulary.
4. **Chef-facing interface** -- A concrete UI exposing model choice, mode lookup, and SLERP angle, with user evaluation.
5. Corpus imbalance should be addressed: ~50% East Asian, ~10% Mediterranean, single-digit shares for South Asian, Latin American, Eastern European recipes -- confidence intervals widen for low-n regions.
6. Code and trained artifacts are not yet released.

---

## Authors & Institutions

Jakub Radzikowski (KAIKAKU.AI), Josef Chen (KAIKAKU.AI)
