# HiGram: Hierarchical Graph Memory for LLM Agents with Path-level Localization and Rewrite

**Paper:** [HiGram: Hierarchical Graph Memory for LLM Agents with Path-level Localization and Rewrite (Yue et al., 2026-08)](https://arxiv.org/abs/2608.05095)
**Wiki:** [[index]] | **Digest:** [[digest]]

## Human Readable TL;DR

Imagine an assistant's memory as a messy pile of sticky notes: to answer one question, or to correct one fact, it has to re-read the whole pile every time. HiGram instead files notes into folders by topic (a two-tier graph), quickly narrows to the one small cluster of notes relevant to the current question or correction (a "MicroGraph"), picks the single chain of notes that actually supports the answer, and only edits that chain — checking whether notes that depended on the edited note still make sense, and marking the ones that don't as outdated. The result: cheaper answers (far fewer tokens read) and fewer stale or contradictory facts surviving updates.

## TL;DR

HiGram organizes agent memory as a hierarchical graph — coarse subject/category/context nodes over fine-grained MemoryUnits with explicit inter-unit dependency edges — and introduces MicroGraphs, localized views keyed by (subject, object-category), to cheaply retrieve a query- and update-relevant region. Within that region it selects a single evidence path by scoring candidate paths on attribute matching, dependency consistency, temporal validity, and contextual compatibility, then performs coordinated rewriting: intra-unit updates to the matched MemoryUnits, followed by inter-unit re-validation of their dependents (accept if still supported, else mark outdated). On LoCoMo and MemConflict, HiGram gets the best average F1/BLEU/LLM-Judge at ~7.2% of full-context token usage, and leads on MemConflict's Macro-AA, SEH@3, and SRS.

---

## Problem & Motivation

Graph-based agent memories help long-horizon reasoning agents structure entities, relations, and history, but two failure modes persist: (1) retrieval runs over one flat, ever-growing graph, pulling in irrelevant context as memory accumulates; (2) updates are applied to memory units independently, even though answers depend on interconnected evidence *paths* — so an update's downstream effects are missed unless the whole graph is repeatedly re-searched, which is expensive and can leave outdated dependencies still in play. HiGram's diagnosis: a granularity mismatch between how memory is organized/updated (whole graph, per unit) and how evidence is actually used (small, localized, interconnected paths).

---

## Main Original Ideas

1. **Two-tier hierarchical graph memory.** Upper-level nodes (subject, object-category, context) give coarse organizational access; MemoryUnits hold fine-grained facts with explicit dependency edges and lifecycle statuses (active/superseded/pending/outdated).
2. **MicroGraph-based path-level localization.** MicroGraphs are localized views keyed by a (subject, object-category) pair — stable across temporal updates — used to cheaply retrieve a relevant region (top-K_g) before scoring up to K_p candidate evidence paths and selecting one as the rewrite region.
3. **Coordinated rewriting.** Rewriting is confined to the selected evidence path: intra-unit rewriting updates matched MemoryUnits (commit new facts as active, revise existing ones), then inter-unit rewriting re-validates dependents — dependencies are never blindly inherited, so unsupported downstream conclusions are marked outdated rather than silently persisting.

---

## Key Findings

| Benchmark | Headline result |
|---|---|
| LoCoMo | Best average F1/BLEU/LLM-J under both GPT-5.4 and GPT-4o backbones; token length ~2,912, only 7.2% of full-context's 4,909 tokens |
| MemConflict | Best Macro-AA (67.84), SEH@3 (81.06), SRS (77.31); best Static AA (68.75) and Cond AA (90.00) |

- Ablation: removing MicroGraph organization raises token use by 68.6% and hurts LLM-J everywhere; removing the support subgraph causes the largest quality drop overall (Multi-Hop F1 ~33 → ~19).
- Update-strategy comparison: HiGram's coordinated rewrite (avg 56.77) beats Append-Only (42.89) and Relation-level updates (40.76) on MemConflict.
- HiGram is robust to its two main hyperparameters (K_g, K_p) — performance saturates rather than requiring careful tuning.
- Weaker/less dominant on Open Domain LoCoMo questions, where the answer needs external knowledge the stored history doesn't contain.

---

## Suggestions & Future Directions

1. The authors note future work on integrating external knowledge sources beyond the agent's own interaction history.
2. Extending to multimodal memories.

---

## Authors & Institutions

Yue et al. (full author list and affiliations not extracted from the available chunk text — see original paper for details).
