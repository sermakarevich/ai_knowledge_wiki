# RAG Systems & Infra Research — for local Mac tutorial (Docker Desktop, external Ollama)

Research date: 2026-08-30. All facts sourced live via WebFetch/WebSearch on 2026-08-30; source URL given inline. Anything not found in a fetched page is marked **UNVERIFIED** or "not documented".

Target environment reminder: MacBook (Apple Silicon), Docker Desktop, Python 3.12 / `uv`, LLM served by **Ollama** on a remote GPU box (`qwen3.8:27b` note: likely means a Qwen3 ~27B-class model, `nomic-embed-text`), reachable locally at `http://127.0.0.1:11435` via ssh tunnel.

---

## PART 1 — RAG systems / apps

### 1. RAGFlow (infiniflow)
- License: Apache 2.0. Stars: 89.6k. [github.com/infiniflow/ragflow](https://github.com/infiniflow/ragflow)
- Version: v0.27.1, released **2026-08-28**; v0.27.0 released 2026-08-19 (adds "document/dataset-level knowledge compilation" with Wiki/Graph/Tree views). [releases](https://github.com/infiniflow/ragflow/releases)
- What it is: full-stack RAG **engine + web UI + API**, "deep document understanding" focused.
- Deploy: Docker Compose (primary). Requires Docker ≥24.0.0, Docker Compose ≥v2.26.1, Python ≥3.13 for source builds.
  - Min RAM: **≥16 GB**; CPU ≥4 cores; Disk ≥50 GB. `vm.max_map_count` must be **≥262144** (Elasticsearch requirement — RAGFlow's default document engine is Elasticsearch; **Infinity** is the alternative doc engine).
  - Image variants: full image ~9 GB (bundles embedding models) vs. **slim** image ~2 GB (v0.22.0+, no embedded models).
  - **ARM64/Apple Silicon: NOT officially supported** — "All Docker images are built for x86 platforms. We don't currently offer Docker images for ARM64" (would need manual Docker build on Apple Silicon under Docker Desktop's x86 emulation, likely slow). [github.com/infiniflow/ragflow](https://github.com/infiniflow/ragflow)
- Connect to external Ollama: Settings → Model Providers → Ollama → set **Base URL** to `http://host.docker.internal:11434` (Docker-to-host) or a remote URL directly (e.g. your SSH-tunnel address), enter model name, Save. For a genuinely remote Ollama host, Ollama itself must be started with `OLLAMA_HOST=0.0.0.0` so it accepts non-localhost connections. [ragflow.io/docs/faq](https://ragflow.io/docs/faq), corroborated by GitHub issue #333.
- HTTP API: yes (implied by SDK/agent/MCP integration docs; exact endpoint list not captured in this pass — UNVERIFIED specifics).
- Distinctive features: deep document layout parsing ("knowledge extraction from unstructured data"), template-based chunking with visualization, hybrid multi-recall + fused re-ranking, multimodal parsing of images inside PDFs/DOCX, agent workflows + MCP integration, knowledge graph views.
- Default chunking: template-based, per-document-type (no single numeric default captured).

### 2. LightRAG (HKUDS)
- License: MIT. Stars: 39.3k. [github.com/HKUDS/LightRAG](https://github.com/HKUDS/LightRAG)
- Version/release date: not shown on repo page (PyPI package `lightrag-hku`) — UNVERIFIED exact number.
- What it is: **hybrid library + REST API server + WebUI** (`lightrag-hku[api]`).
- Deploy: `pip`/`uv` install, or Docker Compose (standard/lite/postgres variants), or Kubernetes.
- Min RAM: not documented; tunables exist for concurrency (`MAX_ASYNC_LLM`, `MAX_PARALLEL_INSERT`, `EMBEDDING_FUNC_MAX_ASYNC`).
- Connect to external Ollama: `.env` file, `OLLAMA_LLM_*` provider variables plus matching embedding-model env vars.
- HTTP API: documented in `LightRAG-API-Server.md`; server binds `0.0.0.0` by default; covers document management, query, multimodal endpoints, optional auth.
- Distinctive features: dual-layer **knowledge graph + vector** retrieval; 4 query modes — `local`, `global`, `hybrid`, `naive`, and default **`mix`** (combines local+global+naive); optional reranker (disabled by default, adds ~1–2s latency when on); pluggable storage backends (in-memory/file for dev; Postgres/MongoDB/Neo4j/Milvus/Qdrant for prod); ingestion via MinerU/Docling for tables/formulas/images.
- Default chunking: Fixed / Recursive / Vector / Paragraph-semantic strategies available, default not pinned in README excerpt.

### 3. Open WebUI
- License: "Open WebUI License" (source-available with branding-preservation clause, not OSI-approved MIT/Apache). Stars: 150.4k. [github.com/open-webui/open-webui](https://github.com/open-webui/open-webui)
- What it is: **self-hosted AI chat platform** with built-in RAG, not a dedicated RAG engine — RAG is one feature among many (multi-LLM chat UI, tools, pipelines).
- Deploy: single Docker container. `docker run -d -p 3000:8080 --add-host=host.docker.internal:host-gateway -v open-webui:/app/backend/data --name open-webui --restart always ghcr.io/open-webui/open-webui:main`. GPU variant `:cuda`; bundled-Ollama variant `:ollama`. pip install needs Python ≥3.11.
- Connect to external Ollama: env var `OLLAMA_BASE_URL` (e.g. `-e OLLAMA_BASE_URL=http://127.0.0.1:11435` for an SSH-tunnel-forwarded remote Ollama, or `http://host.docker.internal:11434` for host-local Ollama).
- HTTP API: OpenAI-compatible API surface.
- RAG features: "backed by 9 vector databases", **hybrid search (BM25 + vector) with reranking**, 30+ web-search-provider integrations (Google PSE, Brave, Kagi, SearXNG, etc.), full-context mode.
- Min RAM / ARM64: not documented in fetched page — UNVERIFIED (widely reported to run fine on Apple Silicon in community usage, but not confirmed from an official source here).

### 4. kotaemon (Cinnamon)
- License: Apache-2.0. Stars: 25.7k. [github.com/Cinnamon/kotaemon](https://github.com/Cinnamon/kotaemon)
- What it is: **open-source RAG QA web UI** aimed at both end users and RAG-pipeline developers.
- Deploy: Docker, with **lite**, **full** (bundles Unstructured for more file types), and **Ollama-bundled** image variants. Explicitly built for **both `linux/amd64` and `linux/arm64`** — i.e. native Apple Silicon Docker support (rare among this list).
- Connect to external Ollama: pull models via Ollama, then set them as default LLM/embedding models in the web UI, using Ollama's OpenAI-compatible server endpoint.
- RAG features: hybrid full-text + vector retriever with re-ranking; advanced citations with in-browser PDF preview; GraphRAG support via pluggable backends (NanoGraphRAG, LightRAG, MS GraphRAG).
- Min RAM: not documented. HTTP API: not mentioned in fetched README excerpt — UNVERIFIED.
- Maintenance: appears active (recent Docker tags, ongoing GitHub discussions).

### 5. R2R (SciPhi)
- License: MIT. Stars: 8.0k. [github.com/SciPhi-AI/R2R](https://github.com/SciPhi-AI/R2R)
- What it is: "agentic RAG" **API engine** ("most advanced AI retrieval system"), Python SDK (`pip install r2r`) + RESTful server.
- Deploy: Docker Compose, incl. a `compose.full.yaml` for the fuller feature set.
- Connect to external Ollama: not documented in the fetched page — UNVERIFIED (R2R's config historically defaults to `OPENAI_API_KEY`/OpenAI-compatible endpoints, so an Ollama connection likely goes through its OpenAI-compatible provider config, but this specific detail was not verified from a fetched source).
- HTTP API (via SDK, effectively REST under the hood): `client.retrieval.search()`, `client.retrieval.rag()` (RAG with citations), `client.retrieval.agent()` (deep-research agent), `client.documents.create()`, `client.documents.list()`.
- RAG features: hybrid search (semantic + keyword, reciprocal rank fusion), automatic knowledge-graph entity/relationship extraction, agentic reasoning integrated with retrieval, citations, "Deep Research" multi-step API.
- Maintenance: active (2,096 commits, open issues/PRs present). Min RAM / ARM64: not documented — UNVERIFIED.

### 6. AnythingLLM (Mintplex-Labs)
- License: MIT. Stars: 65.4k. [github.com/Mintplex-Labs/anything-llm](https://github.com/Mintplex-Labs/anything-llm)
- What it is: all-in-one **desktop/self-hosted chat app** with RAG, agents, multi-user support, vector-DB integration ("private ChatGPT" style).
- Deploy: Docker (see `docker/HOW_TO_USE_DOCKER.md` in repo).
- Connect to external Ollama: supported as a chat-model provider; exact env var/UI steps not captured in this pass — UNVERIFIED specifics (community docs describe an in-UI LLM-provider picker where you choose "Ollama" and give it a base URL).
- HTTP API: "Full Developer API for custom integrations" (endpoint list not captured — UNVERIFIED).
- RAG features: multi-format ingestion (PDF/TXT/DOCX/etc.), built-in optimizations for large document sets, agents, source citations in chat UI. No confirmation of hybrid search/reranking/chunking defaults from fetched content.
- Min RAM / ARM64: not documented — UNVERIFIED.

### 7. Onyx (ex-Danswer)
- License: MIT (Community Edition). Stars: 31.8k. [github.com/onyx-dot-app/onyx](https://github.com/onyx-dot-app/onyx)
- Version: 3.0.0 shown on repo (exact release date not captured).
- What it is: "application layer for LLMs" — full chat/search UI with RAG, web search, code execution, agents; positions itself as an enterprise search + AI assistant platform, not a bare RAG engine.
- Deploy: `curl -fsSL https://onyx.app/install_onyx.sh | bash`, Docker Compose, or Kubernetes. Two modes: **Onyx Lite** (<1 GB memory, minimal stack) vs. **Standard** (full vector+keyword indexing, background workers, caching — heavier, exact RAM number not documented even in the dedicated deployment docs page fetched: [docs.onyx.app/deployment/overview](https://docs.onyx.app/deployment/overview)).
- Connect to external Ollama: not documented in fetched pages — UNVERIFIED.
- RAG features: hybrid search (vector + keyword index), agentic RAG, web search (Serper/Google PSE/Brave/SearXNG), sandboxed code execution, document-artifact generation.
- Maintenance: active (~9,939 commits). ARM64/HTTP API specifics: UNVERIFIED from fetched content.

### 8. PrivateGPT (zylon-ai)
- License: Apache-2.0. Stars: 57.5k. [github.com/zylon-ai/private-gpt](https://github.com/zylon-ai/private-gpt)
- What it is: local, privacy-first RAG chat app/API.
- Deploy: macOS (Homebrew), Linux (`uv` tool), Windows (PowerShell), Docker.
- Connect to external Ollama: set `OPENAI_API_BASE=http://<host>:<llm-port>/v1` and `OPENAI_EMBEDDING_API_BASE=http://<host>:<embedding-port>/v1` (Ollama's OpenAI-compatible surface), then `private-gpt serve`. For this tutorial's tunnel setup that would be `http://127.0.0.1:11435/v1`.
- RAG features: retrieval with citations and "agentic RAG".
- Maintenance: appears active (426 commits shown, ongoing discussion) — no archival notice found.
- Min RAM / chunking defaults / ARM64: not documented in fetched content — UNVERIFIED.

### 9. Verba (Weaviate) — **DEAD, drop from tutorial**
- Status: **archived 2026-06-08**, explicitly discontinued, no more updates/patches. [github.com/weaviate/Verba](https://github.com/weaviate/Verba)
- License: BSD-3-Clause. Stars: 7.7k.
- For completeness: hybrid (semantic+keyword) search implemented; reranking was only "planned", never shipped; **no useful HTTP API** ("Verba does not offer any useful API endpoints" — disqualifying for programmatic evaluation even if it weren't archived); Ollama connection was `OLLAMA_URL=http://host.docker.internal:11434` (Mac/Windows) or the LAN IP (Linux).
- **Recommendation: exclude from the tutorial** — archived and lacks an API.

### 10. txtai (NeuML)
- License: Apache 2.0. Stars: 12.9k. [github.com/neuml/txtai](https://github.com/neuml/txtai)
- What it is: **Python library/framework** (not a turnkey app) for embeddings, semantic search, RAG, agents, workflows — closer to a toolkit than kotaemon/RAGFlow-style products.
- Deploy: pip/PyPI, Docker, and a FastAPI-based **REST API** you stand up yourself (`CONFIG=app.yml uvicorn "txtai.api:app"`), plus MCP API support.
- RAG features: hybrid (sparse+dense) indexes, graph/semantic-graph analysis, GraphRAG (with a Wikipedia example), context retrieval from web/SQL/other sources.
- Connect to external Ollama: not documented in fetched content — UNVERIFIED (txtai is LLM-provider-agnostic via its pipeline abstraction, so an Ollama connection is plausible but not confirmed here).
- Chunking defaults: not documented — UNVERIFIED.
- Given it's a library requiring you to author the app yourself, it's a poor fit for a "run a pre-built system" tutorial step, but good if the tutorial wants a coded/library-based RAG example.

### 11. Cognita (TrueFoundry) — **DEAD, drop from tutorial**
- Status: **archived 2026-03-13**, explicitly no longer maintained ("read-only"). [github.com/truefoundry/cognita](https://github.com/truefoundry/cognita)
- License: Apache-2.0. Stars: 4.4k.
- For completeness: modular, API-driven RAG framework; Docker Compose stack = Postgres + Qdrant + FastAPI backend + frontend; optional `--profile` flags for Ollama/Infinity server; FastAPI backend on port 8000.
- **Recommendation: exclude — archived.**

### 12. Quivr
- License: Apache 2.0. Stars: 39.4k. [github.com/QuivrHQ/quivr](https://github.com/QuivrHQ/quivr)
- What it is: "Opinionated RAG for integrating GenAI in your apps" — developer-facing RAG app/toolkit; multi-LLM (OpenAI/Anthropic/Mistral/Groq/Llama) and multi-vectorstore (PGVector, FAISS) support.
- Connect to external Ollama: stated as supported ("also supports local models using Ollama") but exact config steps not captured — UNVERIFIED specifics.
- RAG features: customizable retrieval workflows, Cohere reranker support, multi-format ingestion via "Megaparse", internet search hinted at.
- Deploy method (Docker Compose specifics), HTTP API, min RAM, chunking defaults: not documented in fetched content — UNVERIFIED. Repo shows active commit history (2,295 commits), no archival notice found, so presumed maintained but with materially thinner docs footprint than RAGFlow/kotaemon/Open WebUI for this use case.

### 13. Microsoft GraphRAG
- License: MIT. Stars: 35.7k. [github.com/microsoft/graphrag](https://github.com/microsoft/graphrag)
- What it is: **not an app** — a pip-installable **library/data pipeline** that builds a knowledge graph from text and answers via global/local community-based search. Explicitly described by Microsoft as "in maintenance mode, not accepting new feature PRs" and "a demonstration methodology rather than an officially supported Microsoft product."
- Deploy: `pip install graphrag`.
- Connect to Ollama / local LLM: not documented in the fetched README excerpt — UNVERIFIED (community guides exist for pointing GraphRAG's OpenAI-compatible config at Ollama, but not confirmed from an official source here).
- Features: community summaries, global search (broad thematic Qs) vs. local search (entity-centric Qs).
- Given its "library, maintenance mode" status, GraphRAG is better suited as an optional advanced/graph-RAG add-on than as a primary tutorial app — pairs naturally with LightRAG/kotaemon's GraphRAG backends instead of standing alone.

### 14. Khoj
- License: AGPL-3.0. Stars: 36.8k. [github.com/khoj-ai/khoj](https://github.com/khoj-ai/khoj)
- What it is: "AI second brain" — personal assistant app with web+document RAG, custom agents, scheduled automations, deep research.
- Deploy: Docker (Dockerfile + docker-compose.yml in repo).
- Connect to external Ollama, HTTP API, min RAM, chunking defaults: **not documented** in the fetched page — UNVERIFIED across the board; would need deeper docs dive to use in a tutorial.
- Maintenance: active (5,180 commits, 102 open issues), no clear maintenance-commitment statement found.
- Because core Ollama/API connection details couldn't be verified from official sources in this pass, treat Khoj as **lower priority / needs more research** before including.

### Ranking: which 3–4 to install for the tutorial

Constraints: Docker ≤16 GB RAM budget, must work with an external/remote Ollama, must expose an HTTP API for programmatic evaluation.

1. **Open WebUI** — lightest footprint (single container), officially documented `OLLAMA_BASE_URL` env var for external Ollama, OpenAI-compatible API for programmatic eval, native hybrid search + reranking + web search. Best "quick win" / baseline chat-RAG app. Caveat: source-available license, not OSI Apache/MIT.
2. **kotaemon** — only app in this list with **explicit official arm64 Docker images** (a real win on Apple Silicon/Docker Desktop), clean UI-based Ollama hookup, hybrid retrieval + reranking + citations + pluggable GraphRAG backends (can demo graph RAG through it without standing up GraphRAG separately). Best "feature-complete demo" app.
3. **LightRAG** — true dual-mode (library + server) with a documented REST API (best fit for programmatic evaluation harnesses), lightweight enough to run via pip/uv instead of a heavy Docker stack, and a genuinely distinctive knowledge-graph+vector "mix" retrieval mode worth teaching. Ollama connection is env-var based and simple.
4. **RAGFlow** (optional/advanced, resource permitting) — most feature-rich "flagship" open-source RAG engine and the most talked-about in 2025–2026 reviews, has a real HTTP API and slim (~2 GB) image option, but the documented **≥16 GB RAM** minimum eats the entire Docker budget by itself and it has **no official ARM64 image** — so only include it as a "if you have RAM/patience to spare, here's the heavyweight option" bonus section, not the primary walkthrough on a 16 GB-Docker Apple Silicon laptop.

Explicitly excluded: **Verba** and **Cognita** (both archived/dead in 2026). **GraphRAG** treated as an add-on library, not a standalone app. **Onyx, AnythingLLM, R2R, PrivateGPT, Quivr, txtai, Khoj** are all viable/active but had thinner officially-documented Ollama/API/resource specifics in this research pass, or (Onyx) skew toward heavier enterprise-search use cases than a laptop tutorial.

---

## PART 2 — vector stores & retrieval infra (local, from Python)

| Store | PyPI pkg + version | Docker image + tag | License | Default port | Native hybrid search? | Notes |
|---|---|---|---|---|---|---|
| **Chroma** | `chromadb` **1.5.9** (2026-05-05) [pypi.org/project/chromadb](https://pypi.org/project/chromadb/) | can run as server via `chroma run --path <dir>` (no docker tag confirmed here) | Apache 2.0 | not documented in fetched page — UNVERIFIED | **Yes** — official docs state "Dense, sparse, and hybrid search" | Simplest embedded mode (`import chromadb; chromadb.Client()`), zero external service needed — good for a first tutorial step. Python ≥3.9. |
| **Qdrant** | `qdrant-client` **1.19.0** (2026-08-04), Python 3.10–3.14 | `qdrant/qdrant:v1.19.0` / `:v1.19` / `:v1` / `:latest` (pushed ~26 days before 2026-08-30); also `gpu-nvidia-latest`, `gpu-amd-latest`, `*-unprivileged` variants; most tags multi-arch (`linux/amd64`+`linux/arm64`) [hub.docker.com/r/qdrant/qdrant/tags](https://hub.docker.com/r/qdrant/qdrant/tags) | Apache 2.0 | REST 6333, gRPC 6334 (standard Qdrant defaults; port list not fully re-confirmed in this pass for the fetched page but is Qdrant's long-standing default) | **Yes** — dense + sparse vectors + multivector, with RRF and DBSF fusion strategies | Payload filtering (keyword/full-text/numeric/geo) confirmed; quantization confirmed ("cuts RAM up to 97%") but scalar-vs-binary split and default HNSW `m`/`ef_construct` values not captured from fetched page — UNVERIFIED specifics, check `qdrant.tech/documentation` for exact defaults before the tutorial. Multi-arch image = clean on Apple Silicon. |
| **Weaviate** | `weaviate-client` (unpinned "latest" in docs) | `cr.weaviate.io/semitechnologies/weaviate:1.36.0` | BSD-3-Clause | HTTP 8080, gRPC 50051 | **Yes** — official "combine semantic search with BM25 keyword search" | Built-in vector quantization / multi-vector encoding for RAM reduction. |
| **Milvus Lite** | via `pymilvus[milvus-lite]` | N/A — file-based, no server container needed | Apache 2.0 | N/A (embedded) | Sparse vectors + hybrid search exist in full Milvus; **not explicitly confirmed for Lite** — UNVERIFIED | Documented Python support is **">3.8 and <=3.11" for full Milvus** — **Python 3.12 compatibility for Milvus Lite is unclear/UNVERIFIED**, worth a version-pin check before using in this tutorial's `uv`/3.12 environment. macOS ARM64: full Milvus supports Apple Silicon (Go ≥1.21, llvm ≥15) but Lite-specific ARM64 confirmation not found. |
| **pgvector** | (Postgres extension, no separate PyPI pkg — used via `psycopg`/`asyncpg`+SQL) | `pgvector/pgvector:pg18-trixie` / `pg18-bookworm` / `pg17-*` / `pg16-*` / `pg15-*` / `pg14-*` / `pg13-*` | **PostgreSQL License** (BSD-style) [github.com/pgvector/pgvector/LICENSE](https://github.com/pgvector/pgvector/blob/master/LICENSE) | 5432 (Postgres default) | No — needs pairing with Postgres full-text search (`tsvector`) for hybrid | `vector` type: 4×dim+8 bytes, up to 16,000 dims, L2/inner-product/cosine/L1. `halfvec` type: half-precision, 2×dim+8 bytes, same 16,000-dim cap. HNSW defaults: `m=16`, `ef_construction=64`, query-time `hnsw.ef_search=40`. IVFFlat: default `probes=1`; recommended list count `rows/1000` (small) or `sqrt(rows)` (large). |
| **LanceDB** | `lancedb` **0.37.1** (2026-08-10), Python ≥3.10 (3.10–3.13), Alpha status, macOS ARM64 wheel confirmed on PyPI | embedded (Lance columnar format on disk, no server needed) | Apache 2.0 | N/A (embedded) | Multimodal "keyword, vector, or SQL" search mentioned; explicit BM25+vector **hybrid confirmed by product docs generally, not re-verified word-for-word in this pass** — treat as UNVERIFIED-detail, likely-true | Serverless/embedded like Chroma — good zero-infra option. |
| **FAISS (faiss-cpu)** | `faiss-cpu` **1.15.0** (2026-08-03), Python 3.10–3.14 | N/A (library, no server) | MIT | N/A | No (pure ANN library, no keyword/BM25 side) | Confirmed **macOS 14.0+ ARM64 (Apple Silicon)** wheel and macOS 15.0+ x86-64 wheel — good native compatibility on the target Mac. No metadata filtering/payload store built in (roll your own). |
| **sqlite-vec** | `sqlite-vec` (pip-installable, version not captured — UNVERIFIED) | N/A (SQLite extension, no server) | Dual Apache-2.0/MIT | N/A | Not documented — likely no native hybrid | Pure C, no dependencies, "fast enough" vector search inside SQLite; supports float/int8/binary vectors; **pre-v1.0, breaking changes possible** — pin version carefully. Successor to the deprecated `sqlite-vss`. |
| **DuckDB VSS** | N/A (DuckDB extension, `INSTALL vss; LOAD vss;`) | N/A (embedded in DuckDB) | not stated on fetched page — UNVERIFIED | N/A | No | **Explicitly experimental.** HNSW index (`CREATE INDEX ... USING HNSW`, metrics: L2/cosine/negative-inner-product) only persists to disk if you set `hnsw_enable_experimental_persistence=true`, and even then the docs warn of **possible data loss/index corruption on crash** — official docs recommend against production persistence. Fine for a disposable tutorial demo, not for anything you want to survive a laptop restart untested. [duckdb.org/docs/current/core_extensions/vss.html](https://duckdb.org/docs/current/core_extensions/vss.html) |
| **BM25 (bm25s)** | `bm25s` **0.3.11** (2026-08-25) | N/A (library) | MIT | N/A | N/A (this *is* the keyword/BM25 half) | NumPy + sparse-matrix based, positions itself as faster than `rank_bm25`/Elasticsearch for query throughput with a small disk footprint; optional PyStemmer/numba/huggingface_hub extras. Python ≥3.8. Good pairing with any of the embedded vector stores above for a manual hybrid pipeline. |
| **BM25 (rank_bm25)** | `rank-bm25` **0.2.2** (2022-02-16) | N/A (library) | Apache 2.0 | N/A | N/A | Older/simpler, includes Okapi BM25, BM25L, BM25+, BM25-Adpt, BM25T variants; not updated since 2022 — `bm25s` is the more actively maintained, faster choice for a 2026 tutorial. |
| **Elasticsearch / OpenSearch** | — | — | Elastic License / SSPL (ES) vs Apache-2.0 (OpenSearch) | 9200 | Yes (native BM25 + dense vector via kNN plugin) | Noted only, per instructions — heavy (JVM, multi-GB RAM) relative to the ≤16 GB Docker budget; RAGFlow's default dependency, which is part of why RAGFlow's own footprint is large. Not recommended as a *standalone* pick for this laptop tutorial. |

Python 3.12 / macOS arm64 compatibility flags to double check before the tutorial:
- **Milvus Lite**: documented Python ceiling for full Milvus is 3.11 — verify actual Lite wheel support for 3.12 before committing to it in the `uv` environment (UNVERIFIED here).
- **FAISS, LanceDB, qdrant-client**: all confirmed 3.10–3.13/3.14 range covering 3.12, with native arm64 wheels/images — safe defaults.
- **pgvector, Weaviate, DuckDB, sqlite-vec**: language/runtime is not Python-version-gated (extension or server processes accessed via drivers), so no 3.12 conflict expected.

---

## PART 3 — document parsing & chunking libraries

| Library | Version (date) | License | Strengths | CPU cost on Mac / model downloads |
|---|---|---|---|---|
| **Docling (IBM)** | **2.123.1** (2026-08-28) [pypi.org/project/docling](https://pypi.org/project/docling/) | MIT | Advanced PDF understanding: page layout, reading order, table structure, code/formula/image classification; extensive OCR for scanned docs; wide format coverage (PDF, DOCX, PPTX, XLSX, HTML, EPUB, even video/audio/email) | Python ≥3.10, runs on macOS x86_64 **and arm64** natively. Optional VLM (e.g. GraniteDocling) not required for basic operation — can run fully local/CPU for sensitive data. Best all-rounder for table/layout-heavy PDFs in this tutorial. |
| **Unstructured (OSS)** | **0.27.5** (2026-08-28) | Apache-2.0 | 60+ file-format partitioning, chunking, enrichment; strong general-purpose ingestion library | Python 3.11–3.13 (note: **excludes 3.10 and 3.14**, and by extension isn't validated for a bare 3.12-only pin outside that range — but 3.12 itself is fine). Needs system deps: `libmagic`, `poppler-utils`, `tesseract-ocr` (OCR), `libreoffice` (Office docs), `pandoc`. "hi_res" strategy pulls extra ML-based layout/OCR models — heavier CPU cost than the fast/default strategy. |
| **pypdf** | **6.16.2** (2026-08-23) | BSD-3-Clause | Pure-Python PDF split/merge/crop/transform, text+metadata extraction, encryption | Lightweight, no model downloads, minimal CPU — good for simple text-only PDFs, not layout-aware. |
| **PyMuPDF / pymupdf4llm** | **1.28.2** (2026-08-06) | **Dual AGPLv3 / commercial (Artifex)** — free for OSS projects, needs a paid license for proprietary/closed use | Converts PDFs (and other formats via optional PyMuPDF Pro) to Markdown/JSON/text; handles multi-column layouts, tables, images, headers, and scanned pages with **automatic, region-selective OCR** (~50% faster than whole-page OCR) | No GPU/cloud required, runs locally. **Flag the AGPL license explicitly in the tutorial** since it's a copyleft license, unlike the other MIT/Apache tools here. |
| **marker** | version not pinned on repo page (1,395 commits) | Apache-2.0 for code; **model weights under a modified "OpenRAIL-M"-style license** (free for research/personal/startups under $5M funding-or-revenue) | Strong table reconstruction (text-layer based, VLM fallback for low-confidence), layout detection (fast rf-detr vs. balanced Surya VLM mode), multilingual OCR via Surya for garbled/scanned pages | **Needs model downloads** (Surya VLM + small CPU models for layout/OCR-error detection); an inference server auto-spawns on first use. GPU path uses vLLM+NVIDIA; **Apple Silicon/CPU path needs a llama.cpp binary**. Fast/CPU mode: 23.7 pages/s without OCR; balanced GPU mode: 2.9 pages/s at 76% olmOCR-bench accuracy. Heavier setup than Docling for this tutorial's Mac-only, no-NVIDIA-GPU context. |
| **MarkItDown (Microsoft)** | version not captured on repo page — UNVERIFIED | MIT | Converts PDF/Word/Excel/PowerPoint/EPub/images(EXIF+OCR)/audio(transcription)/HTML/YouTube/CSV/JSON/XML/ZIP to Markdown, preserving headings/lists/tables/links | Python ≥3.10. **No built-in model downloads** — image-description via LLM is opt-in and bring-your-own-client (e.g. point it at your Ollama vision model if desired). Lightest-weight "good enough" converter of the parsing tools here. |
| **MinerU** | **3.4** (2026-06-18) | "MinerU Open Source License" (Apache-2.0-based, custom) | Converts PDF/image/DOCX/PPTX/XLSX to LLM-ready output; handles scanned docs, multi-column layout, cross-page tables; strips headers/footers; formulas → LaTeX, tables → HTML | **Pipeline backend runs pure CPU**, min 4 GB VRAM if GPU used; **hybrid/VLM backends need GPU** — explicitly including **Apple Silicon** as a supported accelerator path (min 8 GB VRAM-equivalent) alongside Volta+ NVIDIA GPUs. Needs model downloads before first use (v3.4 added automatic model-source selection + cache reuse to cut redundant downloads). macOS 14.0+ required. |
| **Chonkie** | version not pinned on repo page — UNVERIFIED (PyPI: `chonkie`) | MIT | Lightweight chunking library, 11+ strategies: token, SIMD-accelerated "FastChunker", sentence, recursive, semantic-similarity, "LateChunker" (embed-then-split), code-aware, neural-model-based, LLM-powered semantic, markdown-table-aware, domain-specific | Base chunkers need no model download; **semantic chunking modes need an embedding model** (16+ providers pluggable: sentence-transformers, OpenAI, Cohere, etc. — could point at the tutorial's `nomic-embed-text` via Ollama), installed via optional extra `chonkie[semantic]`. |
| **semantic-chunkers** (Aurelio Labs) | version not captured — UNVERIFIED | MIT | Multi-modal chunking (text, video, audio) using semantic-similarity boundaries | Needs an embedding model to compute semantic boundaries (specifics of which providers not confirmed in this pass). 998 commits, 10 open issues — activity level suggests maintained but exact 2025–2026 release cadence not verified here. |
| **LangChain / LlamaIndex splitters** | not separately researched this pass — out of scope of the fetched pages | — | Widely-used `RecursiveCharacterTextSplitter`, `TokenTextSplitter`, `SemanticSplitterNodeParser`, etc. — the "default choice" many tutorials reach for | No model download for character/token/recursive splitters; semantic splitters need an embedding model, same pattern as Chonkie/semantic-chunkers. Treat as the "boring, well-known baseline" to compare Docling/Chonkie against in the tutorial. |

General notes for the tutorial's Mac/CPU-only, no local-GPU environment:
- **Docling** and **MarkItDown** are the two parsing tools here that run comfortably CPU-only with no extra model downloads for basic use — best default picks for a laptop-only walkthrough.
- **marker** and **MinerU** both want either a GPU or (on Apple Silicon) a llama.cpp/MPS-style acceleration path plus multi-hundred-MB-to-GB model downloads — fine as an "advanced/optional" section, not the default path.
- **pymupdf4llm**'s AGPL licensing is the one item in this list that needs a callout box in the tutorial (it's fine for an OSS tutorial repo, but readers repurposing the code into closed-source products need to know).

---

## Gaps / follow-up research suggested
- RAGFlow's full HTTP API endpoint list (chat/dataset/agent endpoints) — not enumerated from the pages fetched this pass.
- R2R's, AnythingLLM's, Onyx's, and Khoj's exact Ollama-connection config keys — found only generic "supported" statements, not the precise env var / UI field names; worth a dedicated docs-site fetch per project before writing tutorial steps.
- Qdrant's exact default HNSW `m` / `ef_construct` values and confirmation of binary-vs-scalar quantization naming — only the RAM-savings headline ("up to 97%") was captured.
- Milvus Lite's actual Python 3.12 wheel support — full Milvus docs cap at 3.11, Lite-specific ceiling unconfirmed.
- Chroma's default server port for `chroma run` — not stated on the fetched docs page.
