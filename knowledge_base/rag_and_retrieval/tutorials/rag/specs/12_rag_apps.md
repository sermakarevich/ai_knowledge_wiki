# Task: chapter 12 — Complete RAG applications: Open WebUI and RAGFlow scored on our corpus, survey of the rest

Read `specs/COMMON.md`, `index.md`, chapters 00–11 first (cwd `/Users/sergii/.ai/knowledge/research_topics/rag_and_retrieval/tutorials/rag`).
Research: `specs/research/systems_and_infra.md` Part 1 (deployment requirements, Ollama configuration,
API endpoints for each app).

## Problem
Many teams do not write RAG code at all — they deploy an application. The reader should see two of
them running against the same corpus and scoreboard, learn how to tune their RAG settings, and get an
honest survey of the others (with pros/cons and "pick this when…").

## Fix

### Open WebUI (`docker-compose.yml` profile `openwebui`, container `rag-openwebui`, port 3010)
Image from the research note; env `OLLAMA_BASE_URL=http://host.docker.internal:11435`,
`WEBUI_AUTH=False` (local tutorial only — say why that is acceptable here and not in production),
volume `./data/openwebui:/app/backend/data`. Steps (screenshots are not possible — describe the
clicks precisely, and do everything through the **REST API** so it is reproducible):
`project/src/rag_tutorial/app_openwebui.py` (Typer CLI: `setup`, `upload`, `ask`, `eval`): obtain an
API key / token (`/api/v1/auths/signin` or the admin settings), set RAG settings via
`/api/v1/retrieval/config/update` (embedding engine `ollama` + `nomic-embed-text`, chunk size/overlap,
top-k, hybrid search on/off, reranker model e.g. `BAAI/bge-reranker-v2-m3` — verify the current
field names against the running instance's OpenAPI at `/docs`), create a knowledge base
(`/api/v1/knowledge/create`), upload the 12 Markdown files (`/api/v1/files/`, then add to knowledge),
ask through the OpenAI-compatible `/api/chat/completions` with `files: [{type: "collection", id: …}]`,
parse the answer and (if returned) the source chunks/citations for retrieval metrics. Rows:
`12_openwebui_default`, `12_openwebui_hybrid_rerank` (hybrid + reranker + tuned top-k). Record the
settings JSON in `config.json`.

### kotaemon (`docker-compose.yml` profile `kotaemon`, container `rag-kotaemon`, port 7870 → 7860)
Image `ghcr.io/cinnamon/kotaemon:main-lite` (it has native arm64 builds — verify the tag in the research
note / GitHub packages page); volume `./data/kotaemon:/app/ktem_app_data`; env for an external
OpenAI-compatible endpoint pointing at Ollama's `http://host.docker.internal:11435/v1` (chat
`qwen3.8:27b`, embeddings `nomic-embed-text`) — kotaemon reads `flowsettings.py`/env vars such as
`OPENAI_API_BASE`, `OPENAI_API_KEY=ollama`, `OPENAI_CHAT_MODEL`, `OPENAI_EMBEDDINGS_MODEL`
(verify the current names in the repo's `flowsettings.py` and `.env.example`). kotaemon is a Gradio
app: drive it programmatically with `gradio_client` (`Client("http://localhost:7870")`, inspect
`view_api()` for the upload/index and chat endpoints) in `app_kotaemon.py` (Typer CLI: `upload`, `ask`,
`eval`). Upload the 12 Markdown files (or PDFs — its citations preview PDFs), ask the test split, parse
answer + cited chunks. Rows: `12_kotaemon_default`, `12_kotaemon_rerank` (reranking on, top-k tuned).
Record settings in `config.json`. If the Gradio API turns out unusable, fall back to `playwright`
(`uv add playwright`) driving the UI, and say so.

### RAGFlow — optional, time-boxed to 2 hours (`just ragflow-up` / `ragflow-down`)
RAGFlow publishes **x86 images only** (no ARM64) — on this Apple-silicon Mac it runs under Docker
Desktop's emulation, slowly, if at all; Docker has 41 GB of memory available so RAM is not the issue.
Follow the research note: clone the RAGFlow repo at a pinned tag into `data/ragflow/` (gitignored),
edit its `docker/.env` for the *slim* image, ports UI 8085 / API 9385 (avoid our other ports), check
`vm.max_map_count` guidance for Docker Desktop, note the RAM it needs (Docker Desktop memory limit ≥
its documented minimum — check `docker info` and print it in the chapter). If the Mac cannot run it
(RAM, arm64 image missing), **document precisely what failed** and keep the survey entry — do not
spend more than ~2 hours on RAGFlow bring-up. If it runs: configure an Ollama chat model and
embedding model (Base URL `http://host.docker.internal:11435`), create a knowledge base with the
default "General" chunking, upload the **PDFs** (RAGFlow's selling point is deep PDF parsing — compare
its chunk view of a table with our chapter 02 parsers), parse, then use its HTTP API
(`/api/v1/datasets`, `/api/v1/chats`, `/api/v1/chats/{id}/completions` — verify) from
`app_ragflow.py` to answer the test split → rows `12_ragflow_default`, `12_ragflow_tuned`
(similarity threshold, keyword weight, rerank model, top-n).

### Survey (`12_rag_apps.md` table) — from the research note, plus a 30-minute hands-on look
(pip/docker run, connect to Ollama, one question) at **two** more of: R2R, AnythingLLM, Onyx,
PrivateGPT, txtai, Quivr, Khoj — choose the two most promising and report what the first 30 minutes
were like. Mention Verba and Cognita as archived/dead (research note) in one line each. Table columns: what it is, license, deploy, RAM, Ollama support, API, distinctive
features, main drawbacks, maintenance (last release), "pick this when…".

### Tests `project/tests/test_12_apps.py`
The response parsers for Open WebUI, kotaemon and RAGFlow on saved sample JSON payloads (commit the fixtures
under `tests/fixtures/`); the settings builder produces the expected dict. No network.

### `12_rag_apps.md` (chapter)
What a "RAG app" gives you (UI, users, uploads, permissions) and takes away (control, evaluation
hooks); Open WebUI walkthrough with the real API calls and the real settings; one answer with its
citations verbatim; RAGFlow walkthrough (or the honest failure report) and its chunk view of a table;
"What changed on the scoreboard" (app rows next to our best code rows — discuss why apps usually score
lower on a fixed benchmark and why that is not the whole story); the survey table; "Advantages and
disadvantages" per app tried; Troubleshooting (`host.docker.internal` on Linux vs Mac; Open WebUI
first-user admin creation; RAGFlow Elasticsearch/Infinity memory; slow first embedding); Exercises.

## Tests
`cd project && uv run pytest tests/ -q -m "not slow"`

## DoD
As in COMMON.md. Commit: `project/src/rag_tutorial/{app_openwebui,app_kotaemon,app_ragflow}.py`,
`project/docker-compose.yml`, `project/justfile`, `project/.gitignore`, `project/.env.template`,
`project/pyproject.toml`, `project/uv.lock`, `project/data/cache/**`, `project/runs/12_*/**`,
`project/runs/scoreboard.md`, `project/tests/test_12_apps.py`, `project/tests/fixtures/*.json`,
`12_rag_apps.md`. Verify token `"What you will learn"`.

## Scope & constraints
Never commit tokens/API keys (Open WebUI key goes to `.env` as `OPENWEBUI_API_KEY`, template value
`REPLACE_ME`). Stop all app containers at the end (`just down openwebui`, `just down kotaemon`, `just ragflow-down`) so they
do not eat RAM on the machine. Do not modify earlier chapters' code.
