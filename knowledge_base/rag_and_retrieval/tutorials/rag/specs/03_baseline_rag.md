# Task: chapter 03 — Baseline: naive RAG from scratch (no framework), first real scoreboard rows

Read `specs/COMMON.md`, `index.md`, chapters 00–02 first (cwd `/Users/sergii/.ai/knowledge/research_topics/rag_and_retrieval/tutorials/rag`).

## Problem
Before comparing frameworks, the reader should build the simplest RAG system by hand and see exactly
where it fails. This chapter is the reference implementation every later chapter is compared to.

## Fix

### `project/src/rag_tutorial/chunkers.py` (only the first strategy now; chapter 04 adds the rest)
`fixed_token_chunks(doc, size=512, overlap=64) -> list[Chunk]` using `tiktoken` boundaries, keeping
`section` from the heading path. Registry `CHUNKERS = {"fixed": …}`.

### `project/src/rag_tutorial/stores.py` (only Chroma now)
`ChromaStore(collection_name, persist_dir=data/indexes/chroma)`: `add(chunks, embeddings)`,
`query(embedding, k, where=None) -> list[(Chunk, score)]`, `count()`, `reset()`; store chunk
fields as metadata; cosine space. Add `chromadb` to pyproject (check the current version/API in
`specs/research/systems_and_infra.md`; use the embedded `PersistentClient`, no server).

### `project/src/rag_tutorial/baseline.py` (Typer CLI: `index`, `ask`, `eval`)
- `index --chunker fixed --size 512 --overlap 64`: chunk all 12 papers, embed with
  `embed_documents` (cached), write to Chroma collection `baseline_fixed_512`; print counts and
  seconds.
- `ask "question" --k 5`: embed query, top-k, build the prompt (system: "Answer only from the
  provided excerpts. Cite as [paper_short_name §section]. If the excerpts do not contain the answer,
  say: I cannot answer this from the provided documents."), print the retrieved chunk ids/scores and
  the answer.
- `eval --name 03_naive_fixed_512_k5`: `evaluate_run` with the above; also run `--k 3` and `--k 10`
  variants (`03_naive_fixed_512_k3`, `03_naive_fixed_512_k10`).
- `rag_tutorial/prompts.py`: the prompt templates as constants (later chapters reuse them so that
  generation stays constant while retrieval changes).

### Failure analysis → `runs/03_naive_fixed_512_k5/analysis.md`
From `predictions.jsonl`, list every question with correctness 0, classify the failure: (a) evidence
not retrieved (retrieval miss), (b) retrieved but answer wrong (generation/reading failure), (c)
evidence split across a chunk boundary, (d) unanswerable question answered anyway (hallucination),
(e) judge error (you disagree with the judge — note it). Counts per class + 3 worked examples.

### Tests `project/tests/test_03_baseline.py`
`fixed_token_chunks` respects size/overlap and covers the whole text; ids deterministic; `ChromaStore`
round trip in a tmp dir with `FakeEmbedder` (chromadb runs in-process); the prompt builder cites
paper short names. No network.

### `03_baseline_rag.md` (chapter)
The whole pipeline in ~150 lines shown in 4–5 excerpts; a mermaid diagram; how Chroma stores
vectors (collection, metadata, cosine); one `ask` example printed verbatim with the retrieved chunks
and the cited answer; the k sweep; "What changed on the scoreboard" with the three anchors; the failure
analysis table with examples — this table is the motivation for chapters 04–07 (say which later
chapter addresses which failure class). "Advantages and disadvantages" of a hand-rolled pipeline vs
using a framework. Troubleshooting; Exercises.

## Tests
`cd project && uv run pytest tests/ -q -m "not slow"`

## DoD
As in COMMON.md. Commit: `project/src/rag_tutorial/{chunkers,stores,baseline,prompts}.py`,
`project/pyproject.toml`, `project/uv.lock`, `project/justfile`, `project/data/cache/**`,
`project/runs/03_*/**`, `project/runs/scoreboard.md`, `project/tests/test_03_baseline.py`,
`03_baseline_rag.md`. Verify token `"What you will learn"`.

## Scope & constraints
No hybrid search, reranking or query rewriting here (chapters 05, 07). Keep `prompts.py` stable
afterwards — generation must stay constant across retrieval experiments.
