# Technical Analysis: NevaMind-AI/memU

**Repository:** https://github.com/NevaMind-AI/memU
**Version analyzed:** unknown
**Date:** 2026-09-26
**Wiki:** [[index]]

## 1. Overview / What Problem It Solves

Coding and desktop agents lose working knowledge between sessions: project conventions, user preferences, and learned workflows are re-derived or lost when the context window closes. The primary user is an individual running one or more LLM agents (Codex, Claude Code, Cursor, OpenClaw, Hermes, WorkBuddy, Cola, pi) across machines.

memU addresses this with a shared, agent-maintained wiki. Each host runs memU as a sidecar binary bound to two seams: `record` (a scheduled bridging task mines session logs and commits reusable Markdown skills) and `inject` (a standing instruction in the host's instruction file makes the agent retrieve relevant skills before answering) (README:130-133). All hosts on a machine share one backend configured via `~/.memu/config.env` (local SQLite/Postgres or MemU Cloud), so a workflow learned in one agent's session is retrievable from another host (README:149-150). The design constraint is that judgment stays in the agent: `MemoryService` performs storage, embedding, and retrieval of skill Markdown and makes no LLM or chat calls (README:104; AGENTS.md:8-14). Core memory logic is stated at ~500 lines (README:23). License Apache 2.0, Python 3.11+ required, distributed as PyPI package `memu-cli` (README:11-14).

## 2. High-Level Architecture

```text
Agent session logs                       Agent prompt context
(JSONL / SQLite per host)                (instruction files)
        │                                          ▲
        ▼                                          │
┌───────────────┐   prepare/commit    ┌────────────────────┐
│ Host adapters │ ──────────────────► │   MemoryService    │
│ memu-codex …  │                     │ service.py +       │
│ memu-agent    │ ◄────────────────── │ agentic.py         │
└───────────────┘   progressive_      └────────────────────┘
        │           retrieve                   │  │  │
        ▼                                      ▼  ▼  ▼
scheduled bridging task               embedding clients  storage backends
(record seam)                         (openai/jina/…)    (inmemory/sqlite/postgres)
        │                                      │              │
        └──────── shared ~/.memu/config.env ───┴──────────────┘
```

Data-flow narrative:

1. **Capture.** The host adapter reads new session history (messages plus tool calls) from the host-specific log, e.g. `~/.codex/sessions/**/*.jsonl` or `~/.hermes/state.db` (README:97-102, README:136-145).
2. **Prepare.** `prepare` slices each session into a self-contained self-evolve job with the paths and context the agent needs (README:97-102).
3. **Decide and write.** The agent (not the service) reads related existing skills and chooses to do nothing, patch a skill, or create a new Markdown skill with name, description, workflow, branches, and pitfalls (README:97-102).
4. **Commit and index.** `commit` submits changed skill files through `commit_results`; the service embeds skill name plus description and stores the record under the `skill` track (README:97-102).
5. **Inject.** On a later task the standing instruction invokes `<binary> retrieve`, which runs `progressive_retrieve` against the shared store and returns relevant skills into context (README:130-133, README:174-181).
6. **Verify.** `<binary> doctor` checks config, resolved mode, and live retrieval end to end (README:154-155, README:209-210).

Persistent state lives in the configured shared store: local SQLite (typically `~/.memu/memu.sqlite3`), Postgres via DSN, or MemU Cloud; selection and credentials resolve from process env → `~/.memu/config.env` → default (README:172, README:195-207). Session logs and instruction files on each host are read/patched but are not the memory store itself.

## 3. The Skill Wiki — The Core Abstraction

The central concept is a shared wiki of Markdown skills distilled from agent history (README:23-24). Representation: each skill is a readable Markdown file carrying a name, description, and reusable workflow including branches, edge cases, and pitfalls (README:97-102). On commit the service embeds the skill name and description and stores it under the `skill` track (README:97-102). Developer-facing commits distinguish three change kinds — `memory`, `skill`, and `resource` — prepared from 1–10 completed sessions via `memu memorize` (README:163-165).

Named kinds and types cited in the wiki:

- `MemoryService`, composition root: config, storage, embedding client pool; public surface exactly `list_all_recall_files`, `progressive_retrieve`, `commit_results` via `AgenticMixin` (`src/memu/app/service.py`, `src/memu/app/agentic.py`, AGENTS.md:8-14, AGENTS.md:18-28).
- Storage providers `inmemory`, `sqlite`, `postgres` with a shared repository contract requiring backend parity (`src/memu/database/interfaces.py`, `src/memu/database/factory.py`, `src/memu/database/{inmemory,sqlite,postgres}/*`, AGENTS.md:12, AGENTS.md:18-28, AGENTS.md:42-46).
- `TranscriptSource` plus `HostSpec`-sized CLI as the per-host extension unit: adding a host is "implementing one `TranscriptSource` … plus a `HostSpec`-sized CLI" (README:157).
- Skill tracks: `skill` track for indexed skills; `memory` / `resource` change kinds in the developer flow (README:97-102, README:163-165).
- Embedding profiles keyed by name (e.g. `"default"`) with provider selection per profile (README:222-227).

Key queries. Manual retrieval runs the host adapter binary (README:174-181):

```bash
memu-codex retrieve "What should I remember about this project?"


# or: memu-claude-code / memu-cursor / memu-openclaw / memu-hermes / memu-workbuddy / memu-cola / memu-pi / memu-agent
```

The install verification query is the fixed check `<binary> retrieve "When did the user register for memU?"` with a word-for-word ready-report template (SKILL.md:81-148).

## 4. LLM / External Service Integration

The service calls no LLM or chat API. `AGENTS.md` states this as an invariant: "memU is embedding-only. No LLM/chat call happens anywhere in the service; do not add one." (AGENTS.md:8-14). Synthesis and judgment happen inside the host agent during the bridging task; the service only stores, embeds, and retrieves (README:104).

Embedding calls are required for indexing and retrieval. Providers named in the wiki (README:199-207):

| Provider | Env var for key | Role |
|---|---|---|
| `openai` (default) | `OPENAI_API_KEY` (via `MEMU_API_KEY` fallback) | default embedding provider |
| `jina` | provider key via `MEMU_API_KEY` | alternative embedding backend |
| `voyage` | provider key via `MEMU_API_KEY` | alternative embedding backend |
| `doubao` | provider key via `MEMU_API_KEY` | alternative embedding backend |
| `openrouter` | provider key via `MEMU_API_KEY` | alternative embedding backend |

Relevant env vars (all `MEMU_*`, every CLI flag has a matching variable; resolution process env → `~/.memu/config.env` → default) (README:195-207): `MEMU_MEMORY_MODE` (selects Local vs Cloud; unset stays Local), `MEMU_DB` (store DSN; `./data/memu.sqlite3` default for CLI, required for host adapters), `MEMU_EMBED_PROVIDER`, `MEMU_API_KEY`, `MEMU_EMBED_MODEL`, `MEMU_BASE_URL`; legacy `MEMU_LLM_PROVIDER` still read. MemU Cloud route uses an API key of form `memu_…` obtained from memu.so (README:31-35). Optional external calls: Postgres with pgvector for concurrent/large stores (requires `pip install "memu-cli[postgres]"`) (README:216-220); GitHub commits API read during `INSTALL-LATEST.md` SHA confirmation (INSTALL-LATEST.md:55-72).

## 5. The Record-to-Inject Skill Loop — The Main Pipeline

Primary workflow is the six-step automatic skill-extraction loop plus the two host seams (README:93-102, README:130-133). Wiki excerpts give file-level placement (AGENTS.md:18-28) rather than per-function line numbers; citations below pair each step with its documented stage and owning file.

1. **Capture new sessions** (`src/memu/hosts/*`). Host adapter reads new session history including messages and tool calls (README:97-102). Per-host logs and instruction files enumerated in README:136-145 (e.g. Codex `~/.codex/sessions/**/*.jsonl` → `~/.codex/AGENTS.md`; OpenClaw SQLite `~/.openclaw/agents/<agentId>/agent/openclaw-agent.sqlite`; Hermes `~/.hermes/state.db`).
2. **Prepare self-evolve jobs** (`src/memu/app/agentic.py`, `src/memu/app/service.py`). `prepare` slices each session into a self-contained job with paths and context (README:97-102). Developer variant `memu memorize` prepares jobs from 1–10 completed external sessions; full contract in `docs/developer.md` (README:163-166).
3. **Agent decides** (host agent, no service code). Agent reads related existing skills, then does nothing, patches a skill, or creates a new one (README:97-102). Service contributes `list_all_recall_files` and `progressive_retrieve` for the lookup (`src/memu/app/agentic.py`, AGENTS.md:8-14).
4. **Write skill Markdown** (agent-authored files). Name, description, reusable workflow with branches, edge cases, pitfalls (README:97-102).
5. **Commit and index** (`commit_results` in `src/memu/app/agentic.py` via `MemoryService` in `src/memu/app/service.py`, AGENTS.md:8-14). `commit` submits changed files through `commit_results`; service embeds name plus description, stores under `skill` track using `src/memu/embedding/*` client pool and `src/memu/vector.py` ranking (README:97-102, AGENTS.md:18-28).
6. **Retrieve later** (`progressive_retrieve` in `src/memu/app/agentic.py`, invoked as `<binary> retrieve`; `src/memu/cli.py`, `src/memu/env.py` for config). Returns relevant skill on similar future tasks across any connected agent (README:97-102, README:174-181).
7. **Seam binding** (`src/memu/hosts/*` + `<binary> docs install`). `record` = scheduled bridging task → `commit`; `inject` = standing instruction → `<binary> retrieve` (README:130-133). Install path: `<binary> init`, `<binary> config`, register bridging task, patch instruction file, verify with fixed retrieve check (SKILL.md:71-148).

## 6. Key Files

| File | Lines | What It Does |
|---|---|---|
| `src/memu/app/service.py` | n/a in wiki excerpts | `MemoryService` composition root: config, storage, embedding client pool (AGENTS.md:8-14) |
| `src/memu/app/agentic.py` | n/a in wiki excerpts | `AgenticMixin` with the three public entry points `list_all_recall_files`, `progressive_retrieve`, `commit_results` (AGENTS.md:8-14) |
| `src/memu/app/settings.py` | n/a in wiki excerpts | Config models and defaults (AGENTS.md:18-28) |
| `src/memu/database/interfaces.py` | n/a in wiki excerpts | Storage protocols (repository contract) (AGENTS.md:18-28) |
| `src/memu/database/factory.py` | n/a in wiki excerpts | Storage backend factory (AGENTS.md:18-28) |
| `src/memu/database/{inmemory,sqlite,postgres}/*` | n/a in wiki excerpts | Pluggable backends; parity required on protocol change (AGENTS.md:12, AGENTS.md:42-46) |
| `src/memu/vector.py` | n/a in wiki excerpts | Vector math and ranking (AGENTS.md:18-28) |
| `src/memu/embedding/*` | n/a in wiki excerpts | Embedding clients and `ClientPool` reuse pattern (AGENTS.md:18-28, AGENTS.md:32-38) |
| `src/memu/cli.py` | n/a in wiki excerpts | `memu` CLI entry point (AGENTS.md:18-28) |
| `src/memu/env.py` | n/a in wiki excerpts | Shared `MEMU_*` config resolution (AGENTS.md:18-28) |
| `src/memu/hosts/*` | n/a in wiki excerpts | Per-host adapters, binaries, session-log mining, instruction patching (AGENTS.md:18-28, README:136-145) |
| `SKILL.md` | 168 lines cited | `install-memu` router skill: install, host-binary pick, `docs install`, verify gates, uninstall (SKILL.md:1-168) |
| `INSTALL-LATEST.md` | 107 lines cited | `install-memu-latest` dev-build installer from git `main` HEAD (INSTALL-LATEST.md:1-107) |
| `AGENTS.md` | 70 lines cited | Contributor contract: invariants, layer map, backend-parity procedure, validation (AGENTS.md:1-70) |
| `README.md` | 231 lines excerpted | Purpose, install routes, agent matrix, pipeline, CLI, config, backends (README:1-227) |
| `tests/test_agentic.py` | n/a in wiki excerpts | Protocol-change coverage target for all backends (AGENTS.md:42-46) |
| `.pre-commit-config.yaml` | 21 lines | Lint hooks: pre-commit-hooks plus ruff/ruff-format (.pre-commit-config.yaml:1-21) |
| `MANIFEST.in` | 22 lines | sdist include/prune list (MANIFEST.in:1-22) |
| `.gitignore` | 216 lines | Ignores runtime DBs, secrets, models, envs, IDE/OS artefacts (.gitignore:1-223) |
| `.python-version` | 1 line | Pins interpreter to `3.13` (.python-version:1) |

Line counts marked n/a are not stated in the two wiki pages; only the seven root files above carry explicit counts.

## 7. Dependencies

Wiki excerpts name runtime distribution channels and hook revisions but no full dependency manifest; constraint strings below are exactly as stated, with gaps marked.

| Package | Version constraint | Purpose |
|---|---|---|
| `memu-cli` (PyPI) | stated as `pip install memu-cli`; `pip install --upgrade memu-cli`; `uv tool install --upgrade memu-cli` (no pinned version in excerpts) | library plus `memu` and `memu-<host>` CLIs (README:11, README:183-189, SKILL.md:21-40) |
| `memu-cli[postgres]` | stated as `pip install "memu-cli[postgres]"` (no version in excerpts) | Postgres/pgvector backend extra (README:216-220) |
| `memu-cli` (npm launcher) | stated as `npx memu-cli --help` (no version in excerpts) | npm-launched CLI, engine is PyPI package (README:183-189) |
| Python | `3.11+` required (README:13); `.python-version` pins `3.13` (.python-version:1) | interpreter floor and repo pin |
| pre-commit-hooks | `rev: "v6.0.0"` (.pre-commit-config.yaml:1-21) | lint hook set (case-conflict, merge-conflict, toml/yaml/json, pretty-format-json, eof, whitespace) |
| ruff-pre-commit (ruff, ruff-format) | `rev: "v0.14.3"` (.pre-commit-config.yaml:1-21) | lint and format hooks |
| pgvector (via Postgres extra) | no constraint string in excerpts | vector search for Postgres backend (README:216-220) |

Embedding SDKs (openai/jina/voyage/doubao/openrouter clients) and database drivers are implied by the provider/backend tables but their package names and pins do not appear in the two wiki pages.

## 8. CLI / Usage Surface

Entry points: `memu` (core CLI) plus one binary per host — `memu-codex`, `memu-claude-code`, `memu-cursor`, `memu-openclaw`, `memu-hermes`, `memu-workbuddy`, `memu-cola`, `memu-pi`, and generic `memu-agent` (README:136-145, SKILL.md:44-58). Install launchers: `pip install memu-cli`, `npx memu-cli --help`, `uvx --from memu-cli memu` (README:183-189); dev builds install durably via `uv tool install "git+https://github.com/NevaMind-AI/memU"` pinned at `@<sha>`, never ephemeral `uvx`/`npx` (INSTALL-LATEST.md:30-46).

| Command | Effect |
|---|---|
| `<binary> init [--cloud-api-key <key>]` | initialize host integration; cloud key vs local memory (SKILL.md:71-78) |
| `<binary> docs install` | print and follow packaged host install guide: backend, bridging task, instruction patch (SKILL.md:81-90, README:152) |
| `<binary> docs uninstall` / `<binary> remove-instruction` | remove host integration without hand-editing (SKILL.md:154-168) |
| `<binary> retrieve "<query>"` | manual retrieval, e.g. `memu-codex retrieve "What should I remember about this project?"` (README:174-181) |
| `<binary> doctor` | verify config, resolved mode, live retrieval (README:154-155, README:209-210) |
| `<binary> config` | settle backend selection (SKILL.md:81-90) |
| `memu memorize` | prepare self-evolve jobs from 1–10 external sessions for developer-owned history (README:163-165) |
| `memu-agent detect` | probe machine for recognizable session logs and patchable instruction files (README:147, SKILL.md:60-68) |
| `memu --help`, `memu-<host> --help` | fresh-shell verification after install (INSTALL-LATEST.md:55-72) |

Env-var and config tables:

| Setting | Env var | Default |
|---|---|---|
| Store | `MEMU_DB` | `./data/memu.sqlite3` (CLI); required for host adapters (README:199-207) |
| Embedding provider | `MEMU_EMBED_PROVIDER` | `openai` (also `jina`, `voyage`, `doubao`, `openrouter`); legacy `MEMU_LLM_PROVIDER` still read (README:199-207) |
| API key | `MEMU_API_KEY` | provider env var, e.g. `OPENAI_API_KEY` (README:199-207) |
| Embedding model | `MEMU_EMBED_MODEL` | provider default (README:199-207) |
| Base URL | `MEMU_BASE_URL` | provider default (README:199-207) |
| Memory mode | `MEMU_MEMORY_MODE` | Local when unset (backward compatible); selects Local vs Cloud (README:195-197) |

Config file `~/.memu/config.env` holds the shared machine-wide backend; resolution order process env → `config.env` → default; one backend per machine (README:149-150, README:195-197, SKILL.md:81-148).

## 9. Extensibility Points

- **New host agent:** implement one `TranscriptSource` plus a `HostSpec`-sized CLI reusing the shared pipeline, verbs, and instruction text; generic fallback is `memu-agent detect` plus per-agent memorization/retrieval probing (README:147, README:157, SKILL.md:60-68). Code location `src/memu/hosts/*` (AGENTS.md:18-28).
- **New storage backend:** extend the repository protocol in `src/memu/database/repositories/`, add parity implementations under `src/memu/database/{inmemory,sqlite,postgres}/*` via `src/memu/database/interfaces.py` and `src/memu/database/factory.py`, extend `tests/test_agentic.py`, check `src/memu/database/postgres/migrations/` (AGENTS.md:42-46).
- **New embedding provider:** keep logic inside `memu.embedding.backends` under `src/memu/embedding/*` and reuse the `ClientPool` pattern instead of duplicating client caching (AGENTS.md:32-38).
- **New service capability:** add it through `MemoryService` in `src/memu/app/service.py` and expose only via the three `AgenticMixin` entry points in `src/memu/app/agentic.py`; do not add LLM/chat calls (AGENTS.md:8-14).
- **Developer-owned history:** use `memu memorize` plus the `docs/developer.md` prepare → agent → commit contract rather than writing a new adapter (README:163-166).
- **Docs and decisions:** update `README.md`/`npm/README.md` on user-visible change; record decisions as ADRs under `docs/adr/` without rewriting history (AGENTS.md:68-70).

## 10. Limitations and Gotchas

- **SQLite is single-writer; concurrent or large stores need Postgres.** `sqlite` uses brute-force cosine and is labeled "local/default, single writer"; concurrent access requires the `postgres` + pgvector extra (README:216-220).
- **Host coverage has hard gaps and unverified paths.** ChatGPT Chat mode and Claude Chat/Cowork are unsupported; Linux Codex VS Code extension retrieves but does not memorize; OpenClaw retrieval is "not yet verified" (README:49-85, README:136-145).
- **Setup is model- and version-sensitive.** Claude Code setup may be declined by Sonnet 5 (retry with Opus); Hermes on Windows needs a build with `HERMES_HOME` support or retrieval reads wrong files; WorkBuddy with Hy3 may fail retrieval (README:49-85).
- **Self-hosted mode still needs an embedding key.** The self-host route is "Private · Single-device · Embedding key required" — local store does not remove the third-party embedding dependency (README:110-114, README:199-207).
- **One shared backend per machine by design.** All host binaries share the `~/.memu/config.env` backend; per-project or per-agent stores are not the documented topology (README:149-150, SKILL.md:81-148).
- **Stale installs and wrong installers break setup.** `SKILL.md` requires `pip install --upgrade memu-cli` (stale builds fail with `invalid choice`) and forbids `uv pip install` into one venv; `INSTALL-LATEST.md` forbids ephemeral `uvx`/`npx` and requires unshadowing `uv tool`/`pipx`/`pip` copies first (SKILL.md:21-40, INSTALL-LATEST.md:11-46).

## 11. How It Compares to Alternatives

The two wiki pages name no competing memory systems and contain no comparison matrix; positioning below is inferred from the documented architecture, not from a wiki comparison.

- **mem0:** hosted plus self-hosted agent-memory API with automatic extraction backed by its own service. memU keeps extraction inside the user's own agent (bridging task) and restricts its service to embedding plus retrieval, with a ~500-line auditable core (README:23, README:104).
- **Zep / Graphiti-style stores:** temporal and graph memory services consumed via SDK. memU stores plain Markdown skill files under a `skill` track and patches host instruction files, trading graph queries for file-level readability and per-host sidecars (README:97-102, README:136-145).
- **Letta (ex-MemGPT):** stateful agents with archival-recall memory management inside the agent runtime. memU is runtime-agnostic: one shared store fronted by per-host binaries and a scheduled log-mining task across Codex, Claude Code, Cursor, and others (README:136-150).
- **LangChain / framework-native memory modules:** in-codebase conversation buffers and vector retrievers the developer wires per app. memU's developer path (`memu memorize` plus `docs/developer.md`) targets apps that already own history, while the default path requires no app changes — only a host adapter and instruction patch (README:163-166, SKILL.md:81-148).

Positioning: memU is a sidecar skill-wiki for individual multi-agent users rather than a developer memory API or an agent runtime — smallest where others are platforms, at the cost of host-by-host adapter maintenance and an external embedding dependency even in self-host mode.

## Appendix: Selected Code Snippets

1. Definition of the system (README:23, via wiki 01-overview.md):

```text
"memU is a lightweight, agent-driven memory system that gives users a shared LLM wiki across sessions, agents, and devices. It automatically distills your own reusable skills from your agent history. Its core memory logic is only 500 lines — compact enough to inspect, understand, and adapt."
```

2. Backend construction example (README:222-227, via wiki 01-overview.md):

```python
service = MemoryService(
    database_config={"metadata_store": {"provider": "postgres", "dsn": "postgresql://..."}},
    embedding_profiles={"default": {"provider": "jina"}},
)
```

3. Contributor invariants (AGENTS.md:8-14, via wiki 02-top-level-files.md):

```text
- `MemoryService` (`src/memu/app/service.py`) is the composition root: config, storage, and the embedding client pool. Its public surface is exactly the three `AgenticMixin` entry points — `list_all_recall_files`, `progressive_retrieve`, `commit_results`.
- memU is embedding-only. No LLM/chat call happens anywhere in the service; do not add one.
- Storage is pluggable across `inmemory`, `sqlite`, and `postgres`; repository contract changes require backend parity.
```

4. Router skill front matter (SKILL.md:1-3, via wiki 02-top-level-files.md):

```text
name: install-memu
description: Install or uninstall memU for whatever agent you are — identify your host, print its packaged guide, and follow it to wire (or unwire) both seams (record and inject).
```
