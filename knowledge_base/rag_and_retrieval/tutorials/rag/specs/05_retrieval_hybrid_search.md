# Task: chapter 05 — Retrieval: dense vs BM25 vs hybrid (RRF), MMR, metadata filters, Qdrant native hybrid

Read `specs/COMMON.md`, `index.md`, chapters 00–04 first (cwd `/Users/sergii/.ai/knowledge/research_topics/rag_and_retrieval/tutorials/rag`).
Research: `specs/research/systems_and_infra.md` Part 2 (Qdrant, bm25s), `models_eval_papers.md` Part 5.

## Problem
Dense retrieval misses exact terms (method names, numbers, acronyms — common in our questions);
keyword search misses paraphrases. This chapter adds BM25, fuses both, adds MMR diversity and metadata
filtering, and shows how Qdrant does hybrid search natively. Fix the chunking to the best cheap
strategy from chapter 04 (state which and why) so only retrieval changes.

## Fix

### `project/src/rag_tutorial/retrievers.py` — extend
- `BM25Retriever` with `bm25s` (tokenise: lowercase, simple stemmer via `PyStemmer` if available,
  stopwords), persisted under `data/indexes/bm25/<name>`.
- `HybridRetriever(dense, sparse, fusion="rrf"|"weighted", k_each=20, rrf_k=60, alpha=0.5)`; RRF
  formula in a docstring; min-max normalisation for the weighted variant.
- `MMR` re-selection (`lambda_mult=0.7`) over the top-20 dense candidates using cached embeddings.
- Metadata filtering: `where={"paper": …}` and a tiny **query router** that asks the LLM (JSON) which
  paper(s) a question is about when the question names one (else no filter); measure how often it
  fires and whether it helps.
- `retrievers.py` gains `k` sweeps via CLI.

### `project/src/rag_tutorial/stores.py` — add `QdrantStore`
`qdrant-client`; collection with a dense vector (`nomic`, 768, cosine) **and** a sparse vector
(`bm25`, using qdrant-client's built-in `Qdrant/bm25` sparse encoder through `fastembed`, or our own
bm25s term weights — pick whatever the installed version supports; document it); `query_hybrid` with
Qdrant's prefetch + RRF fusion (`models.FusionQuery`); payload filters. `just up qdrant` first. Also
`query_points` timing.

### Experiments (`just retrieval-eval`)
`05_dense_k5` (= best 04 chunking, dense), `05_bm25_k5`, `05_hybrid_rrf_k5`, `05_hybrid_weighted_k5`,
`05_hybrid_rrf_k10`, `05_dense_mmr_k5`, `05_hybrid_rrf_filtered_k5` (router + filter),
`05_qdrant_native_hybrid_k5`. Also a **retrieval-only** table for k ∈ {1,3,5,10,20} (hit/recall/MRR/nDCG
only — no generation, cheap) for dense, bm25, hybrid → `runs/05_retrieval_sweep.json` + a matplotlib
plot `runs/05_retrieval_sweep.png` (recall@k curves).

### Tests `project/tests/test_05_retrieval.py`
RRF on two hand-made rankings gives the expected order; weighted fusion normalises; MMR prefers the
diverse candidate in a constructed case; BM25 retrieves the chunk containing a rare term; router
parsing with `FakeLLM`. No network, no Qdrant (Qdrant tests are `@pytest.mark.slow`).

### `05_retrieval_hybrid_search.md` (chapter)
BM25 in plain words (with the formula and a two-document example); why dense and sparse fail
differently — show two real questions: one only BM25 gets, one only dense gets; RRF with a worked
example; MMR; filtering and routing; the recall@k plot and what it says about choosing k; Qdrant
native hybrid (code + response time) vs doing it in Python; "What changed on the scoreboard";
"Advantages and disadvantages" table for dense / BM25 / hybrid / Qdrant-native; Troubleshooting
(Qdrant not running; sparse encoder download; BM25 tokeniser mismatch); Exercises.

## Tests
`cd project && uv run pytest tests/ -q -m "not slow"`

## DoD
As in COMMON.md. Commit: `project/src/rag_tutorial/{retrievers,stores,retrieval_eval}.py`,
`project/pyproject.toml`, `project/uv.lock`, `project/justfile`, `project/docker-compose.yml` (only if
changed), `project/data/cache/**`, `project/runs/05_*/**`, `project/runs/scoreboard.md`,
`project/tests/test_05_retrieval.py`, `05_retrieval_hybrid_search.md`. Verify token `"What you will learn"`.

## Scope & constraints
No rerankers or query rewriting (chapter 07). One embedding model only (chapter 06 compares them).
