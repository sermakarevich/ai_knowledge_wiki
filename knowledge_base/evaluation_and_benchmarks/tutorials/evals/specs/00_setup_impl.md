# Task: chapter 00 impl — project skeleton, cached Ollama client, GPU check, `just check` (code only, NO chapter writing)

Read ONLY `specs/COMMON.md` and `index.md` (cwd `/Users/sergii/.ai/knowledge/research_topics/evaluation_and_benchmarks/tutorials/evals`).
You may COPY files from the finished RAG tutorial at `../rag/project/` — they solve the same problems
(cached Ollama client, settings, fake LLM, GPU check). Do not read RAG chapter markdown.

## Problem
Nothing exists yet under `project/` except `data/public/` (committed datasets — do not touch). Every
later chapter needs a `uv` project, settings from `.env`, a **cached** Ollama client (chat with optional
JSON-schema output + embeddings), a fake LLM for offline tests, a GPU-politeness check and `just check`.

## Fix (create these files)

### `project/pyproject.toml`
Package `evals-tutorial`, `requires-python = ">=3.12"`, `[tool.uv] package = true`, hatchling,
`packages = ["src/evals_tutorial"]`. Dependencies: `httpx`, `pydantic>=2`, `pydantic-settings`,
`python-dotenv`, `typer`, `rich`, `pyyaml`, `tiktoken`, `numpy`, `pandas`, `orjson`, `scikit-learn`,
`matplotlib`. Dev group: `pytest`, `pytest-timeout`. pytest marker `slow: needs Ollama/Docker/network`.
Later chapters add their own dependencies — do not add them now.

### `project/.env.template`, `project/.gitignore`
```
OLLAMA_URL=http://127.0.0.1:11435
CHAT_MODEL=qwen3.8:27b
JUDGE_MODEL=qwen3.8:27b
EMBED_MODEL=nomic-embed-text
CACHE_DIR=data/cache
```
`.gitignore`: `.env`, `.venv/`, `__pycache__/`, `runs/**/*.log`, `data/langfuse/`. Copy `.env.template`
to `.env`.

### `project/justfile` (`set dotenv-load := true`)
Recipes with a one-line comment each: `default` (list), `sync`, `check`, `tunnel` (runs `fleet tunnel`),
`gpu-check`, `cache-stats`, `test` (`uv run pytest tests/ -q -m "not slow"`).

### `project/src/evals_tutorial/config.py`
Copy `../rag/project/src/rag_tutorial/config.py`, rename, fields = the `.env` variables above plus
`project_root: Path` computed from `__file__`; `settings = Settings()` singleton; helper `path(rel)`.

### `project/src/evals_tutorial/llm.py` — the cached Ollama client
Copy `../rag/project/src/rag_tutorial/llm.py` and adapt (keep its disk-cache design: key = sha256 of a
canonical JSON of (endpoint, model, options, input); files `data/cache/chat/<key[:2]>/<key>.json`,
`data/cache/embed/<model>/<key[:2]>/<key>.json`; per-text embedding cache; `usage` recorded; `stats`
with hits/misses/tokens/seconds; 3 retries with backoff; clear error pointing to `just tunnel`).
Required API:
- `chat(messages, *, model=None, temperature=0.0, seed=42, num_ctx=16384, max_tokens=1024,
  json_schema: dict | None = None, think: bool = False) -> str`
- `chat_json(messages, schema: type[BaseModel], **kw) -> BaseModel` — passes the Pydantic JSON schema as
  Ollama `format`, parses and validates the reply, one retry with the validation error appended.
- `embed(texts, *, model=None, prefix="")`, `embed_documents(texts)`, `embed_query(text)` (nomic prefixes
  `search_document: ` / `search_query: `).
- `count_tokens(text)` via `tiktoken` `cl100k_base` (approximation — say so in a docstring).
- Add `usage_log`: a module-level counter of calls made *this process* (cache hits vs live calls) that
  experiments read to fill `llm_calls` in `metrics.json`.

### `project/src/evals_tutorial/testing.py`
Copy/adapt `../rag/project/src/rag_tutorial/testing.py`: `FakeLLM` (canned answers by substring match,
else echoes; supports `chat_json` by returning a given dict) and `FakeEmbedder(dim=32)`.

### `project/src/evals_tutorial/gpu.py` → `just gpu-check`
Copy `../rag/project/src/rag_tutorial/gpu.py` (ssh to rtx, `nvidia-smi --query-compute-apps`, exit 1 if a
non-ollama process holds > 6 GB; `wait_for_gpu(max_hours=6)`).

### `project/src/evals_tutorial/check.py` → `just check`
Table: Ollama reachable + version (`/api/version`), the chat model answers "Reply with the single word
OK", `chat_json` returns a valid object for a 2-field schema, embedding dimension = 768, the three files
in `data/public/` exist with their row counts, cache size. Exit non-zero if Ollama/chat fail.

### `project/tests/test_00_setup.py`
Cache round-trip with a monkeypatched `httpx` transport (second call hits the cache); embedding cache
is per text; `chat_json` validation retry path with `FakeLLM`; `FakeEmbedder` deterministic and
unit-norm; `count_tokens > 0`; `data/public/*.jsonl` parse and have the row counts from
`data/public/README.md`. No network.

### Findings note `project/runs/00_findings.md` (REQUIRED handoff to the writeup task)
Terse bullets: the real `just check` output, `uv pip list` versions of every dependency, Ollama version
and model digests (`/api/tags`), the project tree (`find project -type f -not -path '*/.venv/*' -not
-path '*/cache/*'`), anything that differed from this spec and why.

## Tests
`cd project && uv run pytest tests/ -q -m "not slow"`

## DoD
As in COMMON.md. Commit: `project/{pyproject.toml,uv.lock,.env.template,.gitignore,justfile}`,
`project/src/evals_tutorial/{__init__,config,llm,testing,gpu,check}.py`, `project/data/cache/**`,
`project/tests/test_00_setup.py`, `project/runs/00_findings.md`.
Verify: `git show HEAD:knowledge/research_topics/evaluation_and_benchmarks/tutorials/evals/project/src/evals_tutorial/llm.py | grep -c "def chat"` ≥ 1.

## Scope & constraints
No chapter markdown (separate task). No handbook, tickets or evaluation code yet. Do not edit
`index.md`. Do not touch `data/public/`. Context budget ≈ 45k tokens. Do not run `fleet serve restart`
or `fleet run`.
