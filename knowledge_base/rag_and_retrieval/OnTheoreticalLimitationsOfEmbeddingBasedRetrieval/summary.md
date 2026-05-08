# On the Theoretical Limitations of Embedding-Based Retrieval

**Paper:** [On the Theoretical Limitations of Embedding-Based Retrieval (Weller, Boratko, Naim, Lee, 2025)](https://arxiv.org/abs/2508.21038)

## Human Readable TL;DR

Imagine you're trying to organize a library by assigning each book and each reader a single barcode number, then finding relevant books by comparing numbers. That works fine for simple cases, but if you have millions of books and every reader wants a different unique combination of books, you'd need barcodes so long they'd be impractical. This paper proves mathematically that AI search engines face exactly this problem: the single "summary number" (vector) they compute for each document fundamentally cannot capture every possible combination of results a query might need. The authors also build a deceptively simple test set that exposes this failure in today's best search models -- while a simple keyword search passes easily.

## TL;DR

This paper proves that single-vector embedding models have fundamental theoretical limits tied to the mathematical concept of sign-rank: for any fixed embedding dimension `d`, there exist retrieval tasks whose relevance structure cannot be represented, regardless of training data or model size. The authors empirically validate this via direct vector optimization (best-case scenario), fit a polynomial showing critical document count grows as `~0.0037d³`, and introduce LIMIT -- a dataset of 50k documents with a dense query-relevance pattern that collapses state-of-the-art dense retrievers to <20% recall@100 while BM25 scores 93.6%.

---

## Problem & Motivation

Dense retrieval has become the dominant paradigm in neural IR, yet increasingly complex tasks (logical query operators, instruction-following, reasoning-intensive retrieval) implicitly demand that a single embedding vector represent arbitrary relevance combinations. Prior work acknowledged vague theoretical limits but assumed they were surmountable with larger models and better training data. This paper asks: are these limits *fundamental*, and do they arise even with simple natural-language queries?

---

## Main Original Ideas

1. **Representational Capacity via Sign-Rank** -- The minimum embedding dimension needed to correctly rank all relevant documents for a binary relevance matrix `A` equals the sign-rank of `(2A - 1)`, up to ±1. This connects a well-studied algebraic concept to neural IR for the first time.

2. **Rank Equivalence (Proposition 1 & 2)** -- Row-wise order-preserving rank equals row-wise thresholdable rank for binary matrices. Both are bounded tightly by the sign-rank of the signed version, providing a clean characterization of what dimension is required.

3. **Free Embedding Experiments** -- Instead of training a model, the authors directly optimize query/document vectors with gradient descent on the test data (unconstrained best-case). They find a *critical-n* point per dimension `d` where optimization fails to achieve 100% accuracy. Fitted polynomial: `n_crit = -10.53 + 4.03d + 0.052d² + 0.0037d³` (r² = 0.999). At d=1024, critical-n ≈ 4M -- already insufficient for web-scale corpora.

4. **LIMIT Dataset** -- A deliberately simple corpus (50k documents, 1000 queries, k=2 relevant docs per query) designed to maximize `qrel` interconnectedness using a *dense* pattern where all C(46,2)=1035 document-pair combinations appear. Language is trivial (person names + attributes); difficulty is purely structural.

5. **Qrel Pattern as Difficulty Driver** -- Ablation over four patterns (random, cycle, disjoint, dense) shows that dense qrel patterns cause the largest performance drops, confirming the theoretical mechanism rather than query linguistic complexity.

---

## Key Findings

| Model | LIMIT Full recall@100 | LIMIT Small recall@20 |
|---|---|---|
| GritLM-7B (d=4096) | ~18% | ~40% |
| Qwen3 Embeddings (d=2048) | ~15% | ~35% |
| Gemini Embeddings (d=3072) | ~17% | ~38% |
| E5-Mistral-7B (d=4096) | ~5% (dense qrel) | -- |
| **BM25** | **93.6%** | **100%** |
| GTE-ModernColBERT (multi-vec) | significantly > single-vec | -- |
| Gemini-2.5-Pro (reranker) | -- | **100%** |

- No correlation was found between BEIR/MTEB performance and LIMIT performance -- existing benchmarks do not expose these limits.
- Fine-tuning on a synthetic LIMIT training set moved recall@10 from ~0 to only 2.8, ruling out domain shift as the cause.
- Fine-tuning *on the test set* recovers high recall, confirming the task is solvable but requires per-pattern overfitting -- consistent with theory.
- Sparse (BM25) and multi-vector (ColBERT) models sidestep the single-vector bottleneck and perform substantially better.

---

## Suggestions & Future Directions

1. **Improve evaluation benchmarks** -- Current benchmarks (BEIR, MTEB) sample an infinitesimally small fraction of possible qrel combinations; new benchmarks should deliberately probe representational capacity.
2. **Develop alternatives to single-vector retrieval** -- Multi-vector models, cross-encoders, and sparse models demonstrate the path forward for complex retrieval tasks; theoretical bounds for multi-vector models remain an open question.
3. **Error-tolerant theoretical extensions** -- The current framework proves exact representation limits; bounding approximate (top-k with tolerance ε) representational capacity is left for future work.
4. **Instruction-following retrieval** -- As the IR community pushes toward arbitrary relevance definitions, the sign-rank framework should guide what is provably representable vs. what requires architectural changes.
5. **Scaling laws for retrieval** -- The polynomial fit between dimension and critical-n invites investigation of whether scaling embedding dimension follows predictable returns for coverage of real-world qrel distributions.

---

## Authors & Institutions

Orion Weller (Google DeepMind, Johns Hopkins University), Michael Boratko (Google DeepMind), Iftekhar Naim (Google DeepMind), Jinhyuk Lee (Google DeepMind)
