# RAG tutorial — open-source Retrieval-Augmented Generation systems, compared on one corpus and one scoreboard

A from-zero, hands-on tutorial on **RAG** (Retrieval-Augmented Generation — instead of asking an LLM (Large Language Model) to answer from memory, you first *retrieve* the relevant pieces of your own documents and hand them to the model together with the question). The tutorial has two goals:

1. **An overview of the open-source / free-of-charge RAG landscape** — libraries (LangChain + LangGraph, LlamaIndex, Haystack, DSPy), complete systems (LightRAG, RAGFlow, Open WebUI, and a survey of kotaemon, R2R, AnythingLLM, Onyx, …), retrieval infrastructure (Chroma, Qdrant, pgvector, FAISS, LanceDB, BM25) and evaluation tools (RAGAS, our own judge) — with the advantages and disadvantages of each, learned by *running* them, not by reading marketing pages.
2. **A working understanding of what makes a RAG system good** — every chunking, retrieval, reranking, query-rewriting and generation trick is implemented, run on the same corpus and the same question set, and lands as one row on a shared **scoreboard** (`project/runs/scoreboard.md`). At the end you can see which tricks paid for themselves and which did not.

Everything runs locally: Python 3.12 with `uv` (fast package manager), a `justfile` (command runner like `make`), Docker for the vector databases and the RAG apps, and open-weight models served by **Ollama** (a local LLM server) on the `rtx` GPU box. No paid API is used anywhere.

Retrieve chapters with `ai show research_topics/rag_and_retrieval/tutorials/rag/<chapter>`.

## The idea that holds the tutorial together
- **One corpus**: 12 open-access arXiv papers *about* RAG — the original RAG paper (2005.11401), DPR (2004.04906), ColBERTv2 (2112.01488), HyDE (2212.10496), Lost in the Middle (2307.03172), RAGAS (2309.15217), Self-RAG (2310.11511), the RAG survey by Gao et al. (2312.10997), Seven Failure Points (2401.05856), CRAG (2401.15884), RAPTOR (2401.18059) and GraphRAG (2404.16130); ≈ 200 pages. (LightRAG and Late Chunking are CC BY-NC-SA licensed and are therefore *discussed* but not part of the corpus.) So you ask a RAG system questions about RAG, and the chapters double as a reading guide to the research.
- **One golden question set**: 36 questions in five kinds — single-hop factoid (10), multi-hop across papers (9), comparative (5), global/"what are the themes" (6), and unanswerable (6) — each with a reference answer and the evidence passages (`project/data/golden/qa.jsonl`, built and reviewed in chapter 02).
- **One evaluation** (`rag_tutorial.evaluate`): retrieval metrics (hit@k, recall@k, MRR, nDCG@k) against the evidence passages; answer metrics (correctness and faithfulness judged by the local `qwen3.8:27b`, RAGAS in chapter 12); latency and number of LLM calls per question. Every experiment writes `project/runs/<name>/metrics.json`; `just scoreboard` rebuilds `project/runs/scoreboard.md` from them.
- **Three anchors** on the scoreboard: *no retrieval* (the LLM alone — lower bound), *naive RAG* (chapter 03) and *oracle context* (the gold evidence handed to the LLM — the upper bound of generation). Everything else is judged against these.

## Chapters (read in order)
- [00_setup.md](00_setup.md) — tools (`uv`, `just`, Docker, Ollama over an SSH tunnel), project layout, `.env`, the cached Ollama client (chat + embeddings, on-disk cache so re-runs are free), Qdrant in Docker, downloading and parsing the paper corpus, `just check`.
- [01_concepts.md](01_concepts.md) — what RAG is and why it exists; the anatomy of a RAG system (ingest → chunk → embed → index → retrieve → rerank → generate → evaluate); the landscape map of open-source options (libraries vs engines vs apps vs infrastructure) with a first pros/cons table; RAG vs long context vs fine-tuning; how this tutorial measures things.
- [02_corpus_and_golden_set.md](02_corpus_and_golden_set.md) — PDF → Markdown with `pypdf`, `pymupdf4llm` and Docling compared (tables, headings, speed); building and reviewing the golden question set with the LLM; the metrics module; the scoreboard.
- [03_baseline_rag.md](03_baseline_rag.md) — naive RAG in ~150 lines with no framework (fixed chunks, `nomic-embed-text`, Chroma, top-k, one prompt, citations); the three anchor rows; reading a failure case by case.
- [04_chunking.md](04_chunking.md) — fixed / recursive / token / sentence / Markdown-structure / semantic chunking, chunk size and overlap ablation, small-to-big (parent–child), sentence-window, contextual chunk headers and Anthropic-style *contextual retrieval*, late chunking; what changed on the scoreboard.
- [05_retrieval_hybrid_search.md](05_retrieval_hybrid_search.md) — dense vs BM25 vs hybrid (Reciprocal Rank Fusion), MMR (Maximal Marginal Relevance), metadata filtering, query prefixes, top-k sweeps; hybrid search natively in Qdrant.
- [06_embeddings_and_vector_stores.md](06_embeddings_and_vector_stores.md) — embedding models compared on our 23-question set (`snowflake-arctic-embed2`, `bge-m3`, `embeddinggemma`, `nomic-embed-text`, `mxbai-embed-large`, `qwen3-embedding`, `all-minilm` — recall@5 / hit@5 / MRR / nDCG@5), dimension truncation with **Matryoshka embeddings** (768→512 free, measured recall drop at 256/128), scalar / product / binary **quantization** (recall vs RAM — 5.7 MB → 0.02 MB with `product_x64`), **HNSW** parameters (`m`, `ef_construct`, `ef_search`) and the latency-vs-recall trade-off; **Chroma vs Qdrant vs pgvector vs FAISS vs LanceDB** (build time, p50/p95 latency, QPS, on-disk size, per-store advantages & disadvantages); when to pick which.
- [07_reranking_and_query_transforms.md](07_reranking_and_query_transforms.md) — bi-encoder vs cross-encoder vs late interaction (ColBERT); cross-encoder rerankers on CPU (`bge-reranker-v2-m3`, FlashRank, MiniLM) with a k_each=20/50 sweep, LLM listwise / pointwise reranking, `best_combo`; multi-query, HyDE, step-back, decomposition with real rewrites for two golden questions; lost-in-the-middle (LITM) context reordering, context compression; per-question-type breakdown (where listwise reranking helps single/multi-hop and hurts comparative); recommendations by budget; troubleshooting for macOS arm64 torch, model pulls and listwise-order parsing; the cost of each in LLM calls and seconds.
- [08_langchain_langgraph.md](08_langchain_langgraph.md) — the same pipeline in LangChain (Runnables, LCEL `|`; naive, parent-document, multi-query, ensemble, ensemble+rerank retrievers) and agentic RAG with LangGraph (2-hop Corrective-RAG: retrieve → grade → rewrite → retrieve); all six rows vs the ch07 best and anchors (framework ensemble+rerank loses on pool size — a config trap, not a framework verdict); pros/cons.
- [09_llamaindex.md](09_llamaindex.md) — the same in LlamaIndex (node parsers: sentence-window, hierarchical + auto-merging; query fusion + rerank ties the ch07 best on hit@5; sub-question engine best correctness despite worst chunk-id retrieval; router; response-mode cost table; built-in evaluators vs our judge; RAPTOR pack skipped as deprecated); pros/cons.
- [10_haystack_and_dspy.md](10_haystack_and_dspy.md) — Haystack 2 pipelines (hybrid retrieval, ranker, prompt builder, YAML serialisation, evaluators vs our judge) and DSPy (zero-shot SOTA 0.739 correctness; Bootstrap/MIPRO optimisation trades correctness for faithfulness); pros/cons.
- [11_graph_rag_systems.md](11_graph_rag_systems.md) — LightRAG (naive / local / global / hybrid / mix modes: correctness 0.065–0.130, below no-retrieval) and RAPTOR (summary tree 1942→194→19→2, k10 correctness 0.522, ties the best global score); per-type table, indexing-cost table, when graph RAG is worth it; pointers to the `graph_rag` tutorial for the Neo4j-based version.
- [12_rag_apps.md](12_rag_apps.md) — complete applications: Open WebUI scored on our corpus via its API (default correctness 0.500, hybrid + rerank 0.587 — ties the tutorial best); kotaemon probed but unscorable (no stateless API) and RAGFlow not run (x86-only ~9 GB image, ≥ 16 GB RAM) with both failure reports; txtai hands-on; survey table of R2R, AnythingLLM, Onyx, PrivateGPT, txtai, Quivr, Khoj with pros/cons and when to pick which.
- [13_evaluation_and_production.md](13_evaluation_and_production.md) — RAGAS metric by metric with a local judge, judge reliability (human spot-check agreement, seed stability), synthetic question-leak bias, long context vs RAG and Lost in the Middle, a prompt-injection demo with verbatim transcripts, the final 65-run scoreboard analysis (what helped most per unit of cost, Pareto frontier, per-type breakdown), production checklist (ingestion updates, caching, monitoring, guardrails, access control, PII, cost model) and a framework decision table.
- [Q&A.md](Q&A.md) — questions asked while reading, with answers (appended over time).

## Runnable project
`project/` — `pyproject.toml` (uv, Python 3.12, package `rag_tutorial` under `src/`), `justfile`, `docker-compose.yml` (Qdrant, pgvector, Open WebUI, kotaemon, RAGFlow — each behind a `just` recipe, none required for the early chapters), `.env.template`, `data/corpus/` (parsed papers, committed; PDFs downloaded on demand), `data/golden/qa.jsonl`, `data/cache/` (Ollama response and embedding cache, committed so re-runs and tests are free), `src/rag_tutorial/` (one module per chapter), `tests/` (CPU-only, no network), `runs/<experiment>/metrics.json` + `runs/scoreboard.md`. Start with `cd project && just sync && just check`.

## Local settings (shared by all chapters — never change these)
| setting | value |
|---|---|
| Ollama | `http://127.0.0.1:11435` — an SSH tunnel to the `rtx` GPU box (RTX 4090 24 GB); `fleet tunnel` (or `ssh -N -L 11435:127.0.0.1:11434 rtx`) brings it up |
| chat / judge model | `qwen3.8:27b` (17 GB in VRAM while loaded; shared with other work — see 00) |
| embedding model (default) | `nomic-embed-text` (768 dimensions); other embedding models are pulled in chapter 06 |
| Qdrant | Docker `qdrant/qdrant`, container `rag-qdrant`, REST http://localhost:6343 (→ 6333), gRPC 6344 (→ 6334) |
| pgvector (chapter 06) | Docker `pgvector/pgvector:pg17`, container `rag-pgvector`, port 5434, db/user/password `rag`/`rag`/`rag123` |
| Open WebUI (chapter 12) | Docker `ghcr.io/open-webui/open-webui:main`, container `rag-openwebui`, http://localhost:3010 |
| kotaemon (chapter 12) | Docker `ghcr.io/cinnamon/kotaemon:main-lite` (arm64), container `rag-kotaemon`, http://localhost:7870 (→ 7860) |
| RAGFlow (chapter 12, optional) | Docker compose from the RAGFlow repo (x86 images under emulation), UI http://localhost:8085, API 9385 |
| Chroma, FAISS, LanceDB, BM25 | in-process (no server), data under `project/data/indexes/` (gitignored) |
| Python | 3.12 via `uv`; exact library versions are recorded in `00_setup.md` once installed |

Ports are shifted from the defaults because other tutorials on this machine already use the default ones (Neo4j 7474/7687, Grafana 3000/3001, Prometheus 9091, …). Container names are prefixed `rag-`.

## Corpus and golden set (fixed in chapter 02, then never changed)
| item | value |
|---|---|
| papers | the 12 arXiv papers listed above, ≈ 200 pages, `project/data/corpus/papers.yaml` |
| parsed text | `project/data/corpus/md/<arxiv_id>.md` (Markdown with headings, one file per paper) |
| golden set | `project/data/golden/qa.jsonl` — 36 questions (9 `dev` / 27 `test`), fields `id, type, question, answer, evidence[{paper, quote}]`, types `single_hop` (10: 2 dev + 8 test), `multi_hop` (9: 2+7), `comparative` (5: 2+3), `global` (6: 1+5), `unanswerable` (6: 2+4) |
| split | `dev` (used to tune, e.g. DSPy) / `test` (reported on the scoreboard) — `split` field, roughly 1:3 |

## Scoreboard columns (shared by all chapters)
`experiment | chapter | hit@5 | recall@5 | MRR | nDCG@10 | correctness | faithfulness | unanswerable-abstain | LLM calls/q | s/q`. Numbers on the scoreboard are always on the `test` split.

Verified on: 2026-09-09 (see `project/runs/14_quickstart_report.md`) — from `project/`: `just sync` ~2 s, `just check` ~3 s (Ollama 0.32.12, chat `qwen3.8:27b`, embedding dim 768, corpus 12/12 parsed), `just scoreboard` ~4 s (65 rows + analysis + ch13 plots), `uv run pytest tests/ -q -m "not slow"` ~5 s — **146 passed, 4 skipped, 3 deselected**. Library versions live in the "Verified on" table in `00_setup.md`.

## Results at a glance

Final scoreboard (`project/runs/scoreboard.md`, 65 runs, `test` split): top 8 rows by correctness, plus the three anchors. Columns: `experiment | chapter | hit@5 | recall@5 | MRR | nDCG@10 | correctness | faithfulness | unanswerable-abstain | LLM calls/q | s/q`.

| experiment | chapter | hit@5 | recall@5 | MRR | nDCG@10 | correctness | faithfulness | unanswerable-abstain | LLM calls/q | s/q |
|---|---|---|---|---|---|---|---|---|---|---|
| 10_dspy_zero_shot | 10 | 0.739 | 0.558 | 0.667 | 0.680 | 0.739 | 0.865 | 1.000 | 1.000 | 10.459 |
| 09_li_subquestion | 09 | 0.304 | 0.239 | 0.097 | 0.148 | 0.739 | 0.919 | 1.000 | 5.185 | 450.074 |
| 07_litm_reorder | 07 | 0.609 | 0.414 | 0.481 | 0.552 | 0.717 | 0.917 | 1.000 | 1.000 | 41.907 |
| 10_dspy_bootstrap | 10 | 0.739 | 0.558 | 0.667 | 0.680 | 0.717 | 0.896 | 1.000 | 1.000 | 13.274 |
| 05_hybrid_rrf_k10 | 05 | 0.609 | 0.414 | 0.481 | 0.552 | 0.696 | 0.934 | 1.000 | 1.000 | 8.530 |
| 10_dspy_mipro | 10 | 0.739 | 0.558 | 0.667 | 0.680 | 0.696 | 0.945 | 1.000 | 1.000 | 11.828 |
| 10_hs_hybrid | 10 | 0.609 | 0.471 | 0.373 | 0.431 | 0.696 | 0.702 | 1.000 | 1.000 | 11.478 |
| 07_hybrid_k20_ce_bge_k5 | 07 | 0.739 | 0.558 | 0.667 | 0.680 | 0.674 | 0.957 | 1.000 | 1.000 | 0.155 |
| **02_no_retrieval** (anchor, lower bound) | **02** | **0.000** | **0.000** | **0.000** | **0.000** | **0.174** | **1.000** | **1.000** | **1.000** | **0.000** |
| **03_naive_fixed_512_k5** (anchor, naive RAG) | **03** | **0.478** | **0.370** | **0.307** | **0.349** | **0.435** | **0.937** | **1.000** | **1.000** | **0.006** |
| **02_oracle** (anchor, upper bound) | **02** | **1.000** | **0.988** | **1.000** | **1.000** | **0.543** | **0.865** | **1.000** | **1.000** | **0.000** |

Five takeaways (from `project/runs/scoreboard_analysis.md`):

1. **Prompt program beats frameworks on cost-adjusted quality** — DSPy zero-shot reaches 0.739 correctness (+0.304 over naive) at 1 LLM call per question and ~10.5 s/q, while the LlamaIndex sub-question engine ties it at 5.2 calls and ~450 s/q.
2. **Hybrid + cross-encoder rerank is the best cheap win** — `bge-reranker-v2-m3` over a hybrid k=20 pool hits 0.674 correctness in 0.155 s/q at 1 call/q, sitting on the Pareto frontier next to hybrid-RRF k10 (0.696 at 8.5 s/q).
3. **Retrieval quality drives answer quality** — the strongest retrieval runs (hit@5 0.739) are also the strongest answer runs, and per-type scores show reranking lifts single-hop to 1.000 and multi-hop to 0.857 while comparative questions stay the hardest (≤ 0.333 for every run).
4. **Graph RAG did not pay off on this corpus** — all five LightRAG modes score 0.065–0.130 correctness, below no-retrieval (0.174); collapsed-tree RAPTOR at k=10 (0.522) only ties the best global-question score rather than beating the dense baselines.
5. **Compression and agentic loops cost more than they return here** — context compression drops correctness to 0.304 at 6 calls/q and the Corrective-RAG loop matches naive (0.435) at ~17 s/q, so spend the budget on hybrid retrieval plus reranking first.
