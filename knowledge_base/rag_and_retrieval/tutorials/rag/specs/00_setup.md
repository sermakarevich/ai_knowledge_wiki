# Task: chapter 00 — Setup: project skeleton, cached Ollama client, Qdrant, corpus download, `just check`

Read `specs/COMMON.md` and `index.md` first (cwd `/Users/sergii/.ai/knowledge/research_topics/rag_and_retrieval/tutorials/rag`). Also skim
`../neo4j/00_setup.md` and `../graph_rag2/00_setup.md` for the expected style, and
`../graph_rag/project/` for a working `uv` + Ollama project you can borrow from (config, httpx client).

## Problem
Nothing exists yet under `rag/project/`. Every later chapter needs: a `uv` project, settings from
`.env`, a **cached** Ollama client (chat + embeddings), Qdrant in Docker, the paper corpus downloaded
and parsed to Markdown, a GPU-politeness check, and a `just check` that proves it all works.

## Fix (create these files)

### `project/pyproject.toml`
Package `rag-tutorial`, `requires-python = ">=3.12"`, `[tool.uv] package = true`, hatchling,
`packages = ["src/rag_tutorial"]`. Dependencies: `httpx`, `pydantic>=2`, `pydantic-settings`,
`python-dotenv`, `typer`, `rich`, `pyyaml`, `tiktoken`, `pypdf`, `numpy`, `pandas`, `orjson`.
Dev group: `pytest`, `pytest-timeout`. pytest markers: `slow: needs Ollama/Docker/network`.
Later chapters add their own dependencies (chromadb, qdrant-client, langchain, …) — do not add them now.

### `project/.env.template`, `project/.gitignore`
```
OLLAMA_URL=http://127.0.0.1:11435
CHAT_MODEL=qwen3.8:27b
EMBED_MODEL=nomic-embed-text
EMBED_DIM=768
QDRANT_URL=http://localhost:6343
CACHE_DIR=data/cache
```
`.gitignore`: `.env`, `.venv/`, `data/corpus/pdf/`, `data/indexes/`, `data/qdrant/`, `data/pgvector/`,
`data/openwebui/`, `__pycache__/`, `runs/**/*.log`. Copy `.env.template` to `.env`.

### `project/docker-compose.yml`
One service now, more later, all with **profiles**: `qdrant` (image `qdrant/qdrant:latest` — pin the
concrete tag you get, see research `systems_and_infra.md`), container `rag-qdrant`, ports
`6343:6333`, `6344:6334`, volume `./data/qdrant:/qdrant/storage`, healthcheck on `/readyz` (curl may
not exist in the image — use `bash -c 'exec 3<>/dev/tcp/127.0.0.1/6333 …'` or `wget`, whatever works;
document what you chose).

### `project/justfile` (with `set dotenv-load := true`)
`default` (list), `sync`, `up profile` (`docker compose --profile {{profile}} up -d` + wait healthy),
`down profile`, `check`, `tunnel` (runs `fleet tunnel`), `gpu-check`, `corpus-download`, `corpus-parse`,
`corpus` (both), `cache-stats`. Each recipe has a one-line comment.

### `project/src/rag_tutorial/config.py`
`Settings(BaseSettings)` reading `.env` (fields above + `project_root: Path` computed from `__file__`);
`settings = Settings()` singleton; helper `path(rel)`.

### `project/src/rag_tutorial/llm.py` — the cached Ollama client (the most important file of the tutorial)
- `class Ollama` with `chat(messages, *, model=None, temperature=0.0, seed=42, num_ctx=16384,
  max_tokens=1024, json_schema: dict | None = None) -> str` (uses `/api/chat`, `stream: false`,
  `format` = schema when given, `options: {temperature, seed, num_ctx, num_predict}`), and
  `embed(texts: list[str], *, model=None, prefix: str = "") -> list[list[float]]` (uses `/api/embed`
  with a list `input`, batches of 32, `truncate: true`). Both go through a **disk cache**:
  key = sha256 of a canonical JSON of (endpoint, model, options, input); files
  `data/cache/chat/<key[:2]>/<key>.json` and `data/cache/embed/<model>/<key[:2]>/<key>.json` (embeddings
  cached per text, not per batch, so re-chunking reuses them). Record `usage` (`prompt_eval_count`,
  `eval_count`, `total_duration`) in the cached entry; expose `Ollama.stats` (hits, misses, tokens,
  seconds) and a `cache_stats()` CLI. Retries: 3 with backoff on connection errors / 5xx; a clear
  error message pointing to `just tunnel` when the port is closed.
- `nomic-embed-text` needs task prefixes: `search_document: ` for passages, `search_query: ` for
  queries (verify on the Ollama/HF page in the research note); implement `embed_documents()` /
  `embed_query()` that add the right prefix per model (a small table: nomic → prefixes, others → none).
- A `count_tokens(text)` helper with `tiktoken` (`cl100k_base` — an approximation; say so).

### `project/src/rag_tutorial/testing.py`
`FakeLLM` (returns canned answers by substring match or echoes the last user message) and
`FakeEmbedder(dim=32)` (deterministic hashed bag-of-words vectors, unit-normalised) with the same
method names as `Ollama` so every later module can be tested offline.

### `project/src/rag_tutorial/corpus.py` (Typer CLI: `download`, `parse`, `stats`)
- `data/corpus/papers.yaml`: exactly the 12 papers named in `index.md` (ids 2005.11401, 2004.04906,
  2112.01488, 2212.10496, 2307.03172, 2309.15217, 2310.11511, 2312.10997, 2401.05856, 2401.15884,
  2401.18059, 2404.16130) with `id, title, year, short_name, license, url` — titles/authors/licences
  are in `specs/research/models_eval_papers.md` Part 4. Record the real page count of each PDF after
  download (`pypdf`) in the yaml and in the chapter (the research note only has estimates).
- `download`: fetch `https://arxiv.org/pdf/<id>` to `data/corpus/pdf/<id>.pdf` (skip if present;
  polite 3-second sleep between downloads; set a User-Agent).
- `parse`: PDF → `data/corpus/md/<id>.md` with `pypdf` for now (chapter 02 compares parsers): one
  `# <title>` heading, then page text with `<!-- page N -->` markers, hyphenation at line ends joined,
  references section kept. Print a table: paper, pages, characters, tokens.
- `stats`: same table from the Markdown files. Commit the Markdown (≈ 250 pages ≈ 1–2 MB is fine).

### `project/src/rag_tutorial/check.py`
Prints a table: Ollama reachable + version, chat model answers "Reply with the single word OK",
embedding dimension for one sentence, Qdrant `/readyz` (or "not started — `just up qdrant`"),
corpus present (n papers), cache size. Exit non-zero on the first two failing.

### `project/src/rag_tutorial/gpu.py` → `just gpu-check`
`ssh -o ClearAllForwardings=yes rtx nvidia-smi --query-compute-apps=pid,process_name,used_memory --format=csv,noheader`
→ prints the processes; exit 1 if any non-`ollama` process uses > 6 GB (see COMMON.md), else 0.
`wait_for_gpu(max_hours=6)` loop used by later batch jobs.

### `project/tests/test_00_setup.py`
Cache round-trip with a monkeypatched `httpx` transport (second call hits the cache, no HTTP);
embedding cache is per text; `FakeEmbedder` is deterministic and unit-norm; `count_tokens` > 0;
`corpus.parse` on a tiny generated PDF (make one with `pypdf`'s writer or skip if not possible —
say which). No network.

### `00_setup.md` (chapter)
Explain every tool (uv, just, Docker, Ollama, SSH tunnel, why the LLM is on another machine); the
`project/` tree with one line per file; the cache design (why caching makes the whole tutorial
reproducible and free to re-run; what the key contains; how to invalidate); nomic prefixes; the GPU
sharing rule; the corpus download + the real `stats` table; the real `just check` output; a
**"Verified on"** table (Ollama version from `/api/version`, model digests, Qdrant image tag, Python
and package versions from `uv pip list`). Troubleshooting (tunnel down; port 6343 busy; Ollama slow
because the model is being loaded / GPU busy; PDF download 403). Exercises.

## Tests
`cd project && uv run pytest tests/ -q -m "not slow"`

## DoD
As in COMMON.md. Commit: `project/{pyproject.toml,uv.lock,.env.template,.gitignore,docker-compose.yml,justfile}`,
`project/src/rag_tutorial/{__init__,config,llm,testing,corpus,check,gpu}.py`, `project/data/corpus/papers.yaml`,
`project/data/corpus/md/*.md`, `project/data/cache/**` (the few entries created by `just check`),
`project/tests/test_00_setup.py`, `00_setup.md`. Verify token `"What you will learn"`.

## Scope & constraints
No chunking, no retrieval, no evaluation yet. Do not add LangChain/LlamaIndex/etc. Do not edit
`index.md` except to fix a port that turns out to be busy (then say so in the chapter and keep
`index.md` and `.env.template` consistent).
