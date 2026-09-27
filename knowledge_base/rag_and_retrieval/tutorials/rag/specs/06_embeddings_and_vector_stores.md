# Task: chapter 06 — Embedding models, dimensions/quantization, HNSW, and vector stores compared

Read `specs/COMMON.md`, `index.md`, chapters 00–05 first (cwd `/Users/sergii/.ai/knowledge/research_topics/rag_and_retrieval/tutorials/rag`).
Research: `specs/research/models_eval_papers.md` Part 1, `systems_and_infra.md` Part 2.

## Problem
Two infrastructure choices dominate retrieval quality and cost: the embedding model and the vector
store. This chapter measures both on our corpus (same chunks as chapter 05, dense top-5, same prompt).

## Fix

### Embedding models (`project/src/rag_tutorial/embed_eval.py`, `just embed-eval`)
- Pull on `rtx` (embedding models only, ≤ 2 GB each, see COMMON.md; exact tags from the research
  note): `bge-m3`, `mxbai-embed-large`, `snowflake-arctic-embed2`, `qwen3-embedding` (smallest tag),
  `embeddinggemma` if present, `all-minilm` (as the "tiny" reference). Record each model's dimension,
  size, prefixes/instructions required (`llm.py` prefix table must be extended), embedding
  throughput (chunks/s through Ollama) and index build time.
- **Retrieval-only** comparison for all models (hit@5, recall@5, MRR, nDCG@10 on the test split;
  cheap: no generation) → `runs/06_embedding_models.json` + bar chart `runs/06_embedding_models.png`.
- Full scoreboard rows for the best two: `06_dense_<model>_k5`.
- **Matryoshka**: for a model that supports it (nomic v1.5: truncate to 512/256/128 dims and
  re-normalise), retrieval-only metrics vs dimension → table.
- **Quantization** in Qdrant: scalar int8 and binary quantization with `oversampling` + `rescore`;
  retrieval-only recall vs the float index, RAM of the collection (`/collections/<name>` info) →
  table. Explain what each does in plain words.
- **HNSW parameters**: `m` ∈ {8,16,32}, `ef_construct`, search `hnsw_ef` ∈ {16,64,256}: recall@10
  vs exact (brute-force numpy on the cached embeddings) and query latency → small table. Note that
  at ~1–2k chunks ANN vs exact hardly differs — say so and explain when it starts to matter.

### Vector stores (`project/src/rag_tutorial/stores.py` + `store_bench.py`, `just store-bench`)
Add `FaissStore` (`faiss-cpu`, `IndexFlatIP` + `IndexHNSWFlat`), `LanceDBStore` (`lancedb`),
`PgVectorStore` (`pgvector/pgvector:pg17` via docker-compose profile `pgvector`, port 5434, `psycopg`
+ `pgvector` python package; `vector(768)`, HNSW index with `vector_cosine_ops`; metadata columns +
a `WHERE paper = …` filter). Benchmark with the *same* cached embeddings (no LLM calls): ingest
seconds for all chunks, p50/p95 query latency (100 golden+dev questions), recall@10 vs exact, index
size on disk, feature checklist (filters, hybrid native, persistence, server needed, license). Table
→ `runs/06_store_bench.json` and the chapter.

### Tests `project/tests/test_06_stores.py`
`FaissStore` and `LanceDBStore` round trip with `FakeEmbedder` in a tmp dir; Matryoshka truncation
re-normalises; the recall-vs-exact function returns 1.0 for exact. pgvector/Qdrant tests are `slow`.

### `06_embeddings_and_vector_stores.md` (chapter)
What an embedding model is trained to do and why models differ (training data, size, context
length, instructions/prefixes, multilinguality); the results table + chart with interpretation
(bigger is not always better on this corpus — report honestly); Matryoshka and quantization explained
with the numbers; HNSW in one diagram and the parameter table; the store comparison table and a
"which store when" paragraph (prototype: Chroma/LanceDB/FAISS; production: Qdrant/pgvector; already
on Postgres → pgvector; needs hybrid → Qdrant); "What changed on the scoreboard"; "Advantages and
disadvantages" table per store; Troubleshooting (model pull space; dimension mismatch when switching
models — collection per model; pgvector `maintenance_work_mem`); Exercises.

## Tests
`cd project && uv run pytest tests/ -q -m "not slow"`

## DoD
As in COMMON.md. Commit: `project/src/rag_tutorial/{llm,stores,embed_eval,store_bench}.py`,
`project/pyproject.toml`, `project/uv.lock`, `project/justfile`, `project/docker-compose.yml`,
`project/.env.template` (if new vars), `project/data/cache/**`, `project/runs/06_*/**`,
`project/runs/scoreboard.md`, `project/tests/test_06_stores.py`, `06_embeddings_and_vector_stores.md`.
Verify token `"What you will learn"`.

## Scope & constraints
Keep `nomic-embed-text` as the tutorial default unless another model is clearly better on our set
(≥ +0.05 recall@5) — if you switch, say so in the chapter and update `index.md` "default" row only.
Do not run Weaviate/Milvus/Elasticsearch — describe them in one paragraph each from the research notes.
