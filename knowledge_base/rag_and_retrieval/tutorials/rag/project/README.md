# rag_tutorial project

Runnable companion to the [RAG tutorial](../index.md): every chunking, retrieval, reranking, query-rewriting, framework, graph-RAG, and app trick from the chapters runs here on one corpus (12 arXiv papers about RAG) and one 36-question golden set, and lands as one row on the shared scoreboard (`runs/scoreboard.md`, 65 runs).

Stack: Python 3.12 via `uv` (fast package manager), `justfile` (command runner), Docker for vector databases and RAG apps, open-weight models served by **Ollama** (a local LLM (Large Language Model) server) at `http://127.0.0.1:11435` through an SSH tunnel to the `rtx` GPU box. No paid API is used anywhere.

## Quick start

```bash
cd project
just sync && just check && just scoreboard
```

`just sync` installs dependencies, `just check` verifies Ollama, embeddings, corpus, and cache, and `just scoreboard` rebuilds `runs/scoreboard.md` from all `runs/*/metrics.json` in ~4 s (fully cached — zero LLM calls).

## Recipes (`just --list`)

```text
anchor-no-retrieval       Run the 02_no_retrieval anchor (LLM answers from memory alone, test split).
anchor-oracle             Run the 02_oracle anchor (LLM gets the gold evidence quotes as context).
audit-all                 Chapter 13: judge-vs-RAGAS correlation table + stability + leak check.
audit-sample              Chapter 13: judge audit — sample the 25-item human spot-check.
baseline-ask              Ask the baseline pipeline one question and print the retrieved chunks + answer.
baseline-eval             Run the baseline eval at k=5 (plus the k=3/k=10 sweep) — chapter 03's scoreboard rows.
baseline-index            Chunk the corpus and build the baseline Chroma index (chapter 03).
cache-stats               Print the on-disk LLM/embedding cache size.
ch11-pertype              Chapter 11: per-type correctness table + chart for ch05/07/08/09 best + ch11 rows.
check                     Run the full setup check: Ollama, chat, embeddings, Qdrant, corpus, cache.
chunking-eval             Chapter 04 chunking bake-off; writes 04_chunk_stats.json.
corpus                    Download then parse the whole corpus.
corpus-download           Download the 12-paper corpus PDFs (skips ones already on disk).
corpus-parse              Parse the downloaded PDFs into committed Markdown under data/corpus/md/.
default                   List all available recipes.
demo-concepts             Chapter 01 demos (why-retrieval and friends).
down                      Stop one docker-compose profile's containers (keeps volumes).
dspy-baseline             Chapter 10: DSPy zero-shot baseline (-> 10_dspy_zero_shot). Needs Ollama.
dspy-eval                 Chapter 10: evaluate all three DSPy programs on test (-> 10_dspy_* rows).
dspy-optimize             Chapter 10: Bootstrap/MIPRO optimisation (light, small budgets). Needs Ollama.
embed-eval                Chapter 06 embedding/vector-store bake-off. Needs `just up qdrant` for quant/hnsw.
golden-generate           Generate golden-set candidate questions (chapter 02); then `just golden-review`.
golden-review             Print every golden-set item with its evidence for a human review pass.
golden-stats              Print golden-set counts per type/split, mean question length, paper coverage.
gpu-check                 Check the shared RTX GPU is polite to use before a big batch of LLM calls.
hs-ask                    Chapter 10: ask one question through a Haystack pipeline. Needs Ollama + `just hs-index`.
hs-eval                   Chapter 10: evaluate Haystack pipelines (-> 10_hs_* rows) + pipeline YAML dump.
hs-index                  Chapter 10: build the Haystack document store index. Needs Ollama.
injection-demo            Chapter 13: prompt-injection demo (-> runs/13_injection_demo.json).
kotaemon-ask              Chapter 12: kotaemon — ask one question through the Gradio API.
kotaemon-eval             Chapter 12: kotaemon — evaluate on the test split (mode set in UI first).
kotaemon-upload           Chapter 12: kotaemon — upload the 12 Markdown files through the Gradio API.
late-chunking-demo        Chapter 04: late-chunking demo (CPU, one paper, not scored).
li-ask                    Chapter 09: ask one question through a LlamaIndex pipeline. Needs Ollama + `just li-index`.
li-eval                   Chapter 09: evaluate LlamaIndex pipelines (-> 09_li_* rows).
li-index                  Chapter 09: build LlamaIndex indexes under data/indexes/li_09_*. Needs Ollama.
lightrag-ask              Chapter 11: ask one question through LightRAG (modes: naive/local/global/hybrid/mix).
lightrag-eval             Chapter 11: evaluate all 5 LightRAG query modes (-> 11_lightrag_* rows).
lightrag-index            Chapter 11: index the 12 papers into LightRAG (graph extraction, 1-3h, run in background).
longctx-eval              Chapter 13: long-context vs RAG mini-experiment (-> runs/13_long_context/).
openwebui-ask             Chapter 12: Open WebUI — ask one question scoped to a knowledge collection.
openwebui-eval            Chapter 12: Open WebUI — evaluate collections.
openwebui-setup           Chapter 12: Open WebUI — push one RAG config (default|hybrid_rerank), saves key to .env.
openwebui-upload          Chapter 12: Open WebUI — create the KB and upload the 12 Markdown files.
parse-compare             Compare pypdf / pymupdf4llm / docling on two table-heavy papers (chapter 02).
ragas-eval                Chapter 13: RAGAS metrics with the local judge.
ragflow-down              Chapter 12: RAGFlow — stop the RAGFlow stack.
ragflow-eval              Chapter 12: RAGFlow — evaluate chat sessions.
ragflow-up                Chapter 12: RAGFlow — start the stack (pinned tag clone under data/ragflow/).
ragflow-upload            Chapter 12: RAGFlow — upload the corpus PDFs to a dataset (needs RAGFLOW_API_KEY).
raptor-ask                Chapter 11: ask one question through collapsed-tree RAPTOR retrieval.
raptor-build              Chapter 11: build the RAPTOR tree index (~200 summary calls).
raptor-eval               Chapter 11: evaluate RAPTOR collapsed retrieval at k=5/k=10.
rerank-eval               Chapter 07: reranker + query-transform bake-off (-> 07_* rows).
rerank-pertype            Chapter 07: per-type table from runs predictions.
rerank-sweep              Chapter 07: k_each sweep; writes runs/07_rerank_sweep.json.
retrieval-eval            Chapter 05: dense/BM25/hybrid bake-off (-> 05_* rows). Needs `just up qdrant`.
retrieval-sweep           Chapter 05: cheap retrieval-only k-sweep (k=1/3/5/10/20).
scoreboard                Rebuild runs/scoreboard.md from every runs/*/metrics.json.
store-bench               Chapter 06: same chunks/queries into 5 stores. Needs `just up qdrant pgvector`.
sync                      Install/sync Python dependencies.
tunnel                    Bring up the SSH tunnel to the Ollama server on the rtx GPU box.
up                        Start one docker-compose profile (e.g. `just up qdrant`) and wait until healthy.
```

## Layout

```text
project/
  pyproject.toml            uv deps (Python 3.12); chapters 08/09/10/11 frameworks live in opt-in groups
  justfile                  all recipes above (one-line comment each)
  docker-compose.yml        Qdrant / pgvector / Open WebUI / kotaemon (+ RAGFlow via its own repo)
  .env.template             every setting (Ollama URL, models, ports, keys)
  src/rag_tutorial/         one module per chapter (Typer CLI + importable functions)
  data/corpus/md/           parsed papers, committed (PDFs under data/corpus/pdf/, gitignored)
  data/golden/qa.jsonl      36 questions (9 dev / 27 test)
  data/cache/               Ollama chat + embedding cache, committed — re-runs are free
  data/indexes/             vector indexes, gitignored (rebuilt per chapter)
  runs/<experiment>/        metrics.json + predictions.jsonl + config.json per experiment
  runs/scoreboard.md        rebuilt by `just scoreboard`
  tests/                    CPU-only, no network (FakeLLM/FakeEmbedder); live calls are @pytest.mark.slow
```

## How to add a new experiment

Implement two plain functions — `retrieve_fn(item) -> list[Chunk]` and `answer_fn(item, retrieved) -> (answer, contexts, n_llm_calls)` — then call the shared contract in `src/rag_tutorial/evaluate.py`:

```python
evaluate_run(name, chapter, answer_fn, retrieve_fn, split="test", limit=None, judge_client=None) -> dict
```

It runs every `split` golden question through your functions, judges correctness/faithfulness with the local `qwen3.8:27b` (temperature 0, fixed seed), times each question, and writes `runs/<name>/{metrics.json,predictions.jsonl,config.json}`. Name the run `<chapter>_<short-name>` (e.g. `04_semantic_512`), re-run `just scoreboard`, and quote the real numbers in your chapter. Chunk ids must be deterministic (hash of paper + start + end) so retrieval metrics compare across strategies.

## How the cache works

`src/rag_tutorial/llm.py` wraps every Ollama chat and embedding call with an on-disk cache under `data/cache/`, keyed by a hash of (model, options, input). The cache is committed to git, so `just scoreboard`, the tests, and chapter re-runs cost zero LLM calls. Always call the LLM through this module (or wrap framework clients around it) and keep temperature 0 with a fixed seed for anything evaluated. Before any uncached batch of 100+ calls, run `just gpu-check` — the RTX 4090 box is shared with other work.

## Docker profiles and ports

One `docker-compose.yml`, everything behind opt-in profiles — `just up <profile>` starts only what a chapter needs, `just down <profile>` stops it (volumes kept). Ports are shifted from defaults because other tutorials on this machine already use them; container names are prefixed `rag-`.

| service | profile | container | ports (host → container) |
|---|---|---|---|
| Qdrant (`qdrant/qdrant:v1.19.0`) | `qdrant` | `rag-qdrant` | REST 6343 → 6333, gRPC 6344 → 6334 |
| pgvector (`pgvector/pgvector:pg17`, db/user/password `rag`/`rag`/`rag123`) | `pgvector` | `rag-pgvector` | 5434 → 5432 |
| Open WebUI (`ghcr.io/open-webui/open-webui:main`) | `openwebui` | `rag-openwebui` | 3010 → 8080 |
| kotaemon (`ghcr.io/cinnamon/kotaemon:main-lite`, arm64) | `kotaemon` | `rag-kotaemon` | 7870 → 7860 |
| RAGFlow (own repo clone under `data/ragflow/`, x86 slim image) | via `just ragflow-up` | — | UI 8085, API 9385 |

Chroma, FAISS, LanceDB, and BM25 run in-process (no server); their data lives under `data/indexes/` (gitignored).
