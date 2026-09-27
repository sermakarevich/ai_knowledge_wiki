# Task: chapter 07 — Rerankers (cross-encoder, LLM, ColBERT) and query transforms (multi-query, HyDE, step-back, decomposition)

Read `specs/COMMON.md`, `index.md`, chapters 00–06 first (cwd `/Users/sergii/.ai/knowledge/research_topics/rag_and_retrieval/tutorials/rag`).
Research: `specs/research/models_eval_papers.md` Parts 2 and 5.

## Problem
Retrieval brings candidates; reranking orders them well; query transforms fix bad questions. These
are the most-cited "tricks to improve RAG" — this chapter measures each one's gain against its cost
(extra LLM calls, seconds per question). Fixed setup: best chunking (04) + hybrid RRF (05), k_each=20,
final k=5, baseline prompt.

## Fix

### `project/src/rag_tutorial/rerankers.py`
- `CrossEncoderReranker(model="BAAI/bge-reranker-v2-m3")` via `sentence-transformers`
  (`CrossEncoder`), CPU on the Mac; also `cross-encoder/ms-marco-MiniLM-L-6-v2` as the fast one; time
  per 20 passages. Cache scores on disk keyed by (model, query, chunk id).
- `FlashRankReranker` (`flashrank`, tiny ONNX models) if it installs on macOS arm64 / Python 3.12 —
  else document why not.
- `LLMReranker`: listwise (RankGPT-style: show 20 numbered passages, ask for the ranking as JSON)
  and pointwise (relevance 0–3 per passage, batched 5 per call) — count the calls.
- `ColBERTReranker` with `pylate` or `ragatouille` using `answerdotai/answerai-colbert-small-v1`
  (research note) as a *reranker* over the 20 candidates (late interaction MaxSim explained). If the
  library does not install cleanly, fall back to describing it and skip the row — say so.

### `project/src/rag_tutorial/query_transforms.py`
`multi_query(q, n=3)` (LLM generates paraphrases; union + RRF of results), `hyde(q)` (LLM writes a
hypothetical answer; embed it instead of the question), `step_back(q)` (more general question; retrieve
for both), `decompose(q)` (sub-questions for multi_hop/comparative; retrieve each; merge), and a
`lost_in_the_middle_reorder(chunks)` (best at the ends) plus `compress(chunks, q)` (LLM extracts only
the sentences relevant to q from each chunk — "contextual compression"). Each records `n_llm_calls`.

### Experiments (`just rerank-eval`)
`07_hybrid_k20_ce_bge_k5`, `07_hybrid_k20_ce_minilm_k5`, `07_hybrid_k20_flashrank_k5`,
`07_hybrid_k20_llm_listwise_k5`, `07_hybrid_k20_colbert_k5`, `07_multi_query`, `07_hyde`,
`07_step_back`, `07_decompose`, `07_litm_reorder` (reorder only, k=10), `07_compress`,
`07_best_combo` (your best judgement: e.g. hybrid + multi-query + cross-encoder + reorder). Retrieval-only
metrics for the rerankers on k_each ∈ {20, 50} in `runs/07_rerank_sweep.json`.
Also a **per-question-type** breakdown (single_hop / multi_hop / comparative / global / unanswerable)
for the best combo vs baseline → table (decomposition should help multi-hop; measure it).

### Tests `project/tests/test_07_rerank.py`
`LLMReranker` parses a canned ranking from `FakeLLM` and handles missing/duplicate indices;
`lost_in_the_middle_reorder` puts top-ranked items at both ends; `multi_query` unions and dedups
with `FakeLLM`; cross-encoder cache hit path with a monkeypatched scorer. No model downloads.

### `07_reranking_and_query_transforms.md` (chapter)
Bi-encoder vs cross-encoder in one diagram (why cross-encoders are better and slower); late
interaction; LLM reranking; each query transform with the real rewritten queries for two golden
questions; the cost/benefit table (Δ correctness, Δ recall@5, LLM calls/q, s/q) — the key deliverable;
the per-type breakdown; "What changed on the scoreboard"; recommendations by budget; "Advantages and
disadvantages" table per technique; Troubleshooting (torch on macOS arm64; slow first model
download; JSON parse failures from the LLM); Exercises.

## Tests
`cd project && uv run pytest tests/ -q -m "not slow"`

## DoD
As in COMMON.md. Commit: `project/src/rag_tutorial/{rerankers,query_transforms,rerank_eval}.py`,
`project/pyproject.toml`, `project/uv.lock`, `project/justfile`, `project/data/cache/**`,
`project/runs/07_*/**`, `project/runs/scoreboard.md`, `project/tests/test_07_rerank.py`,
`07_reranking_and_query_transforms.md`. Verify token `"What you will learn"`.

## Scope & constraints
No frameworks yet. Keep `prompts.py` unchanged except adding the transform prompts.
