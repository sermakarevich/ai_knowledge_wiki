# BERAG: Bayesian Ensemble Retrieval-Augmented Generation for Knowledge-based Visual Question Answering

**Paper:** [BERAG: Bayesian Ensemble Retrieval-Augmented Generation for Knowledge-based Visual Question Answering (Chen et al., 2026)](https://arxiv.org/abs/2604.22678)

## Human Readable TL;DR

Imagine you're a detective trying to answer a question by consulting 50 witnesses. The standard approach shoves all 50 testimonies into one long document and hopes the detective (the AI) finds the right clue. The problem is the detective keeps ignoring witnesses buried in the middle. BERAG instead lets the AI listen to each witness separately, keeps track of which witnesses are proving most helpful after every word spoken, and automatically focuses on just the key witnesses as the answer unfolds -- running faster than the original approach and never losing track of who said what.

## TL;DR

BERAG replaces the standard concatenate-all-documents RAG paradigm with a Bayesian ensemble approach: the model conditions on each retrieved document independently, then marginalizes over documents token-by-token using dynamically updated posterior weights (Bayes' rule). The companion BEFT fine-tuning loss trains this formulation end-to-end without requiring document relevance labels. On KB-VQA benchmarks BEFT sets new state-of-the-art results, eliminates the "lost-in-the-middle" positional bias, enables principled deflection when retrieval fails, and with Top-P pruning achieves 4.6× faster decoding than standard RAG at K=50.

---

## Problem & Motivation

Standard Concatenative RAG (ConcatRAG) suffers from three compounding problems as retrieval depth grows:

1. **Quadratic scaling** -- attention cost grows as O(K²D²) where K is the number of documents and D is document length, making Top-50 inference prohibitively expensive or impossible within model context limits.
2. **Lost-in-the-middle effect** -- LLMs systematically ignore documents placed in the middle of a long context, so simply retrieving more documents does not translate to better answers.
3. **Opaque document contribution** -- fusing all documents into one context makes it impossible to know which document drove the answer, forcing attribution to be handled via separate, post-hoc heuristics.

These issues compound in multimodal tasks (KB-VQA) where visual tokens further inflate context costs and retrieval recall strongly determines final answer quality.

---

## Main Original Ideas

1. **BERAG -- Bayesian Ensemble Inference.** Instead of concatenating K documents, BERAG maintains K independent generation branches (one per document). At each decoding step, next-token probabilities are mixed using document posterior weights. The posterior is updated token-by-token via Bayes' rule: `P(z_k | y_{<j}, x, Z) ∝ P(y_{<j} | z_k, x) · P(z_k | x, Z)`. This makes the ensemble order-agnostic and naturally immune to the lost-in-the-middle effect.

2. **Learned Document Prior via MLP Head.** The document prior `P(z_k | x, Z)` is computed from the model's own last-layer [EOS] embedding for each (query, document) pair, passed through a trainable two-layer MLP. This gives the model an implicit reranker with no separate retrieval component required.

3. **BEFT -- End-to-end Bayesian Ensemble Fine-Tuning.** BEFT minimizes a weighted maximum-likelihood loss derived from the BERAG marginalization equation, with the document posterior acting as token-level soft supervision. No ground-truth document relevance labels are needed; the model learns to upweight the document that best explains the target answer.

4. **Deflection via Empty Passage.** By inserting an empty document z₀ into training on 50% of examples (where the gold document is absent), the model learns to assign high posterior to z₀ when retrieval fails -- providing a principled, prompt-free signal to refuse to answer.

5. **Top-P Posterior Pruning for Fast Decoding.** At each decoding step, branches whose cumulative posterior mass falls below `1 - 1/(2K)` are pruned. Because the posterior concentrates on a few relevant documents very early in generation, later tokens are decoded from a tiny context -- achieving O(KD²) prefill cost and constant-in-K decoding time.

---

## Key Findings

| Benchmark | BEFT Score | Prior SoTA | Gain |
|-----------|-----------|------------|------|
| E-VQA (BEM) | **70.3** | MuKA 63.1 | +7.2 |
| Infoseek (EM) | **42.8** | EchoSight 41.8 | +1.0 |
| SlideVQA QA EM | **69.6** | AVIR 60.3 | +9.3 |
| SlideVQA ES EM | **90.4** | M3D 75.0 | +15.4 |
| MMNeedle 4×4 (Acc) | **41.4** | GPT-4o 26.9 | +14.5 |

**Scaling behavior:** BEFT is the only system that consistently improves as K grows from 1 to 50. Baseline SFT/DPO and GPT-4o-mini peak at moderate K (≈5--15) then degrade; BEFT reaches its best score at K=50 on both E-VQA (70.3) and Infoseek (42.8), exceeding the respective DPO baselines by >5%.

- **Lost-in-the-middle immunity:** Base, SFT, and DPO all show position-dependent VQA scores; BEFT produces identical scores regardless of where the ground-truth document is ranked in the list.
- **Deflection:** BEFT[w/z₀] achieves 93.2% deflection accuracy and 0.96 F1 at K=1 on Infoseek, vs. 89.4% / 0.93 for standard BEFT.
- **Decoding speed:** With Top-P pruning, BERAG runs at ~44 ms/token regardless of K, vs. 203 ms/token for standard RAG at K=50 -- a 4.6× speedup.
- **BEFT as reranker:** Using the trained prior head's logits for reranking boosts PreFLMR-L Recall@1 from 39.5% to 59.7% on E-VQA and from 13.1% to 51.2% on Infoseek -- essentially matching a much heavier dedicated reranker.

---

## Suggestions & Future Directions

1. **Powerset marginalization.** The current method marginalizes over document singletons. Marginalizing over all document subsets (the powerset of Z) could better model questions requiring synthesis across multiple documents, though at exponential computational cost.
2. **Training-free BERAG.** BEFT training is currently required because LLMs are pretrained under ConcatRAG. Continued pretraining under the BERAG objective could produce models that apply ensemble inference zero-shot.
3. **Inference infrastructure optimization.** Current implementations (HuggingFace Transformers) are optimized for standard RAG. Production deployment of BERAG would benefit from batched prefill that avoids re-encoding the shared multimodal query context K times, and dedicated KV-cache management for parallel document branches.
4. **Higher K training.** Authors experimented with K>2 in BEFT training but found diminishing returns; the sweet spot and theoretical bound remain open.

---

## Authors & Institutions

Jinghong Chen (University of Cambridge), Jingbiao Mei (University of Cambridge), Guangyu Yang (University of Cambridge), Bill Byrne (University of Cambridge)
