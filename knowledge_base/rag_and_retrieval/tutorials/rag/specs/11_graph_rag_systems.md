# Task: chapter 11 — Graph and hierarchical RAG: LightRAG and RAPTOR on our corpus

Read `specs/COMMON.md`, `index.md`, chapters 00–10 first (cwd `/Users/sergii/.ai/knowledge/research_topics/rag_and_retrieval/tutorials/rag`).
Research: `specs/research/systems_and_infra.md` (LightRAG), `models_eval_papers.md` Part 5 (RAPTOR,
GraphRAG, LightRAG, HippoRAG notes). Also skim `../graph_rag/index.md` — that tutorial builds a
Neo4j-based Graph RAG by hand; here we use the ready-made open-source systems and *measure* them.

## Problem
Chunk-level retrieval struggles with multi-hop and "global" questions (chapter 07 per-type table).
Graph-based (LightRAG, GraphRAG) and hierarchical (RAPTOR) systems build extra structure at
indexing time to fix this — at a large indexing cost. This chapter runs them on our 12 papers and puts
them on the scoreboard, with per-type breakdown and indexing cost.

## Fix

### `project/src/rag_tutorial/sys_lightrag.py` (Typer CLI: `index`, `ask`, `eval`) — dependency group `lightrag`
`lightrag-hku` (check the PyPI name in the research note). Configure `LightRAG(working_dir=
data/indexes/lightrag, llm_model_func=ollama_model_complete, llm_model_name="qwen3.8:27b",
llm_model_kwargs={"host": settings.ollama_url, "options": {"num_ctx": 32768, "temperature": 0}},
embedding_func=EmbeddingFunc(embedding_dim=768, max_token_size=8192, func=ollama_embed …))` — use the
exact current API from the installed version. Indexing makes ≈ 2–4 LLM calls per chunk (entity/
relation extraction + gleaning) → expect 1,000–2,000 calls and 1–3 hours: run `just gpu-check` first,
run it in the background (`nohup … > runs/11_lightrag/index.log`), and record wall time, call count
(count via a wrapper around the llm func) and the size of the resulting graph (entities, relations,
communities if any) in `runs/11_lightrag/index_stats.json`. **Do not restart from scratch if it
fails halfway** — LightRAG resumes from its working dir.
Query modes: `naive`, `local`, `global`, `hybrid`, `mix` → rows `11_lightrag_<mode>` (test split,
`only_need_context=False`). For retrieval metrics also request `only_need_context=True` and map the
returned chunks back to our chunk ids by text matching (LightRAG returns source chunk text) — say how
well that mapping works.

### `project/src/rag_tutorial/raptor.py` (Typer CLI: `build`, `ask`, `eval`)
Build RAPTOR by hand (if chapter 09 already ran the llama pack, still implement the ~120-line
version so the reader sees the algorithm): leaf chunks (chapter 05 setup) → embed → cluster (UMAP +
GMM as in the paper, or plain k-means/agglomerative — say which and why; `scikit-learn`) → LLM
summary per cluster → embed summaries → repeat until one root or ≤ 5 nodes. Store all nodes (leaves +
summaries) in one Chroma collection with `level` metadata. Retrieval "collapsed tree": top-k over
all levels. Row `11_raptor_collapsed_k5` (+ `k10`). Count summary calls and record the tree shape.
Summary nodes count as relevant for metrics only if they *contain* the evidence (they usually won't),
so also report correctness — explain the metric caveat in the chapter.

### Per-type analysis
Table: correctness per question type for `05/07 best`, `08_lg_crag`, `09_li_router`, `11_lightrag_*`,
`11_raptor_*` → `runs/11_per_type.json` and chart `runs/11_per_type.png`. Plus the indexing cost table
(LLM calls, minutes, disk) for baseline / contextual (04) / RAPTOR / LightRAG.

### Tests `project/tests/test_11_graph.py`
RAPTOR tree building on 30 fake chunks with `FakeEmbedder` + `FakeLLM` terminates and produces levels;
the collapsed retrieval returns leaves and summaries; the LightRAG chunk→id mapping helper on a small
example. No network; no LightRAG import in tests if it is heavy (guard with `importorskip`).

### `11_graph_rag_systems.md` (chapter)
Why chunk retrieval fails for multi-hop/global (one real example from our set); the GraphRAG idea in
one diagram (entities, relations, communities, summaries) and how LightRAG simplifies it (dual-level
keywords, no community summaries — from the paper in our corpus); the RAPTOR idea (tree of summaries);
running LightRAG (config, the real index stats and time, one `local` vs `global` answer verbatim);
RAPTOR's real tree shape; the per-type table + chart; the indexing cost table; "What changed on the
scoreboard"; "Advantages and disadvantages" tables (LightRAG, RAPTOR, and hand-built Graph RAG from
`../graph_rag` by reference); when graph RAG is worth its cost; Troubleshooting (LightRAG API changes,
JSON parsing errors from extraction, long indexing, Ollama `num_ctx` too small); Exercises.

## Tests
`cd project && uv run pytest tests/ -q -m "not slow"`

## DoD
As in COMMON.md. Commit: `project/src/rag_tutorial/{sys_lightrag,raptor}.py`, `project/pyproject.toml`,
`project/uv.lock`, `project/justfile`, `project/data/cache/**`, `project/runs/11_*/**` (stats, metrics,
predictions, plots — NOT the LightRAG working dir), `project/runs/scoreboard.md`,
`project/tests/test_11_graph.py`, `11_graph_rag_systems.md`. Verify token `"What you will learn"`.

## Scope & constraints
Do not run Microsoft GraphRAG (covered by `../graph_rag`; describe it and cross-link). Do not run
HippoRAG (describe from the research note). Budget: LightRAG indexing may exceed the usual per-chapter
LLM budget — that is expected; report the real cost.
