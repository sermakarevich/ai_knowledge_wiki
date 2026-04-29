# Power and Limitations of Aggregation in Compound AI Systems

**Paper:** [Power and Limitations of Aggregation in Compound AI Systems (Nivasini Ananthakrishnan, Meena Jagadeesan, 2025)](https://arxiv.org/abs/2602.21556)

## Human Readable TL;DR

Imagine you need to bake a complex cake but each of your bakers can only follow simple recipes. One baker is great at chocolate layers, another at vanilla frosting -- but no single baker can do both well at once. This paper asks: when does combining outputs from multiple identical bakers (who each follow different simple instructions) give you a result that no single baker could produce alone? The authors found three specific situations where this "combining trick" works -- like filtering out unwanted ingredients both bakers add, merging complementary specialties, or freeing the result from trade-offs each baker is individually stuck with. They also proved that if none of these three situations applies, combining identical bakers never helps, no matter how clever your instructions are.

## TL;DR

This paper develops a principal-agent framework to theoretically characterize when aggregating outputs from multiple copies of the same LLM expands the set of achievable outputs beyond what a single model can produce. The authors identify three necessary mechanisms -- feasibility expansion, support expansion, and binding set contraction -- and prove that a strengthened version of these conditions is both necessary and sufficient for aggregation to be "elicitability-expanding." They validate these mechanisms empirically using GPT-4o-mini on a reference-generation task.

---

## Problem & Motivation

Modern compound AI systems frequently deploy multiple copies of the same LLM, each prompted differently, and then aggregate their outputs -- for example in multi-agent debate, prompt ensembling, or multi-agent research pipelines. Despite using identical underlying models, these systems empirically outperform single-model queries. This raises a fundamental theoretical question: **when and why does aggregating responses from identical models yield outputs that no single model could produce?**

Two specific limitations drive the need for aggregation:

- **Prompt engineering limitations:** Complex desired behaviors are hard to encode in a single prompt. Prompts operate on coarser features than the fine-grained output space, making precise steering difficult.
- **Model capability limitations:** Individual models face inherent trade-offs (e.g., creativity vs. hallucination, safety vs. over-refusal) that prevent them from producing certain "pure" outputs.

The paper aims to formalize these intuitions and provide system designers with principled guidance on when aggregation genuinely adds power versus when it is ineffective.

---

## Main Original Ideas

1. **Principal-agent framework for compound AI systems:** The authors extend the classical Kleinberg-Raghavan principal-agent model to handle multiple agents and aggregation, modeling LLM outputs as non-negative vectors, model limitations as conic constraints, and prompt engineering limitations as coarser feature mappings.

2. **Three mechanisms for elicitability-expansion:** The paper formalizes three distinct mechanisms by which aggregation can produce outputs unreachable by any single agent:
   - **Feasibility expansion** -- aggregation (via intersection/min) produces outputs that violate model capability constraints, effectively "breaking" inherent trade-offs.
   - **Support expansion** -- aggregation (via addition/union) combines outputs with different non-zero dimensions into richer outputs that no single prompt can elicit.
   - **Binding set contraction** -- aggregation frees the output from binding constraints that individually limit each agent, allowing access to "interior" outputs.

3. **Necessity and sufficiency characterization:** The authors prove that these three mechanisms are necessary (Theorem 3.7) -- if none is active, aggregation never helps. They then introduce strengthened versions of support expansion and binding set contraction to form a "power-characterizing condition" that is both necessary and sufficient for elicitability-expansion (Theorems 4.3 and 4.4).

4. **Complementary roles of aggregation rules:** The analysis shows that intersection and addition aggregation have complementary strengths -- intersection enables feasibility expansion and binding set contraction, while addition enables support expansion (Table 1).

---

## Key Findings

- **Necessity result (Theorem 3.7):** If an aggregation operation is elicitability-expanding, it must implement at least one of the three mechanisms. This establishes a strong limitation -- without these mechanisms, aggregation adds zero power regardless of prompt sophistication.

- **Insufficiency of individual mechanisms:** Implementing a single mechanism is generally not sufficient for elicitability-expansion (Propositions A.4, A.5), with the exception of feasibility expansion, which is always sufficient on its own (Proposition A.6).

- **Complete characterization (Theorems 4.3 & 4.4):** A strengthened "power-characterizing condition" -- requiring either feasibility expansion or sufficient geometric distance between aggregate and individual outputs along specific constraint-violating directions -- is both necessary and sufficient.

- **Intersection vs. addition trade-offs (Table 1):**
  - Intersection aggregation can implement feasibility expansion and binding set contraction but cannot implement support expansion.
  - Addition aggregation can implement support expansion and binding set contraction but cannot implement feasibility expansion.

- **Empirical validation with GPT-4o-mini (Section 5):** On a reference-generation task, all three mechanisms were successfully demonstrated:
  - Support expansion: prompting separately for "CS theory" and "economics" then merging produced topic coverage unachievable by a single prompt.
  - Binding set contraction: prompting for "NLP excluding CV" and "CV excluding NLP" then intersecting isolated pure "deep learning" papers.
  - Feasibility expansion: prompting with complementary exclusion constraints then intersecting produced near-pure "blockchain" output that broke individual model trade-offs.

---

## Suggestions & Future Directions

- **Stochastic outputs:** The current model assumes deterministic agent behavior. Extending to stochastic outputs (e.g., incorporating LLM temperature) would increase realism.

- **Non-linear limitations:** Both conic constraints and feature maps are linear. Exploring non-linear model limitations and non-linear feature spaces would add modeling fidelity.

- **Reward interdependencies:** The framework assumes agents optimize independently. Future work could model reward interdependencies arising from multi-turn interactions or explicit agent collaboration.

- **Beyond reward design:** The paper focuses on prompt-based steering. Incorporating other compound AI mechanisms -- tool use, fine-tuning, retrieval augmentation, architectural choices -- would broaden the framework's applicability.

- **Practical design guidance:** The three mechanisms can serve as diagnostic tools for system designers to predict when aggregation will be beneficial and to choose between intersection and addition aggregation strategies.

---

## Authors & Institutions

- **Nivasini Ananthakrishnan** -- UC Berkeley
- **Meena Jagadeesan** -- Stanford University

The work builds on the principal-agent framework of Kleinberg and Raghavan (2020) and acknowledges feedback from Kate Donahue, Nika Haghtalab, Tatsu Hashimoto, Michael I. Jordan, and Manish Raghavan.
