> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Overview

**In one sentence:** memU is a lightweight, agent-driven memory system that gives users a shared LLM wiki across sessions, agents, and devices (README:23).

## Key points

- memU stores personal memory as a wiki shared across sessions, agents, and devices (README:7, README:23).
- Its core memory logic is only 500 lines, kept compact enough to inspect, understand, and adapt (README:23).
- It automatically distills reusable Markdown skills from agent history via a scheduled bridging task (README:93, README:104).
- `MemoryService` makes no LLM or chat calls; judgment and synthesis stay inside the agent while the service stores, embeds, and retrieves skill Markdown (README:104).
- Each host runs memU as a sidecar binary binding two seams: `record` (scheduled bridging task → `commit` via `commit_results`) and `inject` (standing instruction → `<binary> retrieve` → `progressive_retrieve`) (README:130-133).
- All hosts share one memory backend configured via `~/.memu/config.env` (local or MemU Cloud), so what one host's sessions teach, another host retrieves (README:149-150).
- Configuration resolves in order process env → `~/.memu/config.env` → default, with Local and Cloud backends selected by `MEMU_MEMORY_MODE` (README:195-197).
- `<binary> doctor` verifies the whole loop (config, selected mode, live retrieval) and displays the resolved mode (README:154-155, README:209-210).

---

## Purpose and model

memU is described as "Personal memory, stored as Wiki" with the tagline "Across Sessions. Across Agents. Across Devices." (README:7, README:9). The definitional claim is verbatim (README:23):

> "memU is a lightweight, agent-driven memory system that gives users a shared LLM wiki across sessions, agents, and devices. It automatically distills your own reusable skills from your agent history. Its core memory logic is only 500 lines — compact enough to inspect, understand, and adapt."

Packaging and requirements stated in the chunk (README:11-14):

- License: Apache 2.0 (README:12)
- Python 3.11+ (README:13)
- PyPI package `memu-cli` (README:11)

## Quick start and install routes

memU works with "Codex, Claude Code, Cursor, OpenClaw, Hermes, WorkBuddy, Cola, pi, and more" (README:29). The hosted route is "Cross-device · Free · Unlimited" via [memu.so](https://memu.so) (README:31); the user gets an API key from memu.so and sends their agent this verbatim message (README:33-35):

> "Read [https://memu.pro/SKILL.md](https://memu.pro/SKILL.md), follow its instructions to install and configure memU, API Key is memu_•••••••••(get Api Key from memu.so)."

The self-hosted route is labeled "Private · Single-device · Embedding key required" (README:110) with this verbatim agent message (README:112-114):

> "Read [https://raw.githubusercontent.com/NevaMind-AI/MemU/main/SKILL.md](https://raw.githubusercontent.com/NevaMind-AI/MemU/main/SKILL.md) and follow it to install memU."

`SKILL.md` is the routing skill handed to the agent: install the package, identify the host (falling back to `memu-agent detect`), print that host's packaged install guide (`<binary> docs install`), follow it (configure backend, register scheduled bridging task, patch instruction file, each behind a verify gate), then report which seams (memorization / retrieval) are active (README:152). Adding another host means "implementing one `TranscriptSource` … plus a `HostSpec`-sized CLI — the pipeline, verbs, and instruction text are shared" (README:157).

Uninstall uses this verbatim message (README:120-122):

> "Read [https://memu.pro/SKILL.md](https://memu.pro/SKILL.md) and follow its instructions to uninstall memU."

By default uninstalling "removes the host integration and tooling while keeping your memory store and `~/.memu/config.env`", and "Memory is erased only when you explicitly ask for it" (README:124).

## Agent support matrix

The matrix lists currently tested integrations by OS, where Memorize means capturing session knowledge through a scheduled background task and Retrieve means bringing relevant memory into a future task (README:41-44). `⚠️` means supported with an important limitation (README:45).

### macOS (README:49-60)

| Agent | Mode | Memorize | Retrieve | User note |
| --- | --- | :---: | :---: | --- |
| ChatGPT | ChatGPT(Work mode), codex and VS Code extension | ✅ | ✅ | |
| ChatGPT | Chat | ❌ | ❌ | Chat mode is not currently supported. Please use Work mode. |
| Claude Code | Desktop and CLI | ✅ | ✅ | If the selected model declines the setup steps, retry with **Opus** or another model. Sonnet 5 can occasionally do this. |
| Claude | Chat and Cowork | ❌ | ❌ | |
| Cursor | — | ✅ | ✅ | |
| OpenClaw | — | ✅ | ✅ | Retrieve support has not yet been verified. |
| Hermes Agent | — | ✅ | ✅ | |
| WorkBuddy | — | ✅ | ✅ | |

### Windows (README:64-75)

| Agent | Mode | Memorize | Retrieve | User note |
| --- | --- | :---: | :---: | --- |
| ChatGPT | ChatGPT(Work mode), codex and VS Code extension | ✅ | ✅ | |
| ChatGPT | Chat | ❌ | ❌ | Chat mode is not currently supported. Please use Work mode. |
| Claude Code | Desktop and CLI | ✅ | ✅ | If the selected model declines the setup steps, retry with **Opus** or another model. Sonnet 5 can occasionally do this. |
| Claude | Chat and Cowork | ❌ | ❌ | |
| Cursor | — | ✅ | ✅ | |
| OpenClaw | — | ✅ | ✅ | |
| Hermes Agent | — | ✅ | ⚠️ | Use a memU version with Windows `HERMES_HOME` support; older versions may retrieve from the wrong files. |
| WorkBuddy | — | ✅ | ✅ | With Hy3, retrieval may fail. Retry with another model if this happens. |

### Linux (README:79-85)

| Agent | Mode | Memorize | Retrieve | User note |
| --- | --- | :---: | :---: | --- |
| Codex | VS Code extension | ❌ | ✅ | |
| Claude Code | CLI | ✅ | ✅ | |
| OpenClaw | 4.23 / 7.1 | ✅ | ✅ | |

"Support status reflects the current release and may change as host integrations evolve." (README:87)

## Automatic skill extraction

Once the scheduled bridging task is installed, memU "can turn useful agent history into reusable Markdown skills automatically" (README:93). The six-step pipeline is (README:97-102):

1. **Capture new sessions.** The host adapter reads new session history, including messages and tool calls.
2. **Prepare self-evolve jobs.** `prepare` slices each session into a self-contained job with the paths and context the agent needs.
3. **Let the agent decide.** The agent reads related existing skills, then chooses to do nothing, patch an existing skill, or create a new one.
4. **Write readable skill Markdown.** Each skill has a name, description, and reusable workflow, including useful branches, edge cases, and pitfalls.
5. **Commit and index.** `commit` submits changed skill files through `commit_results`; memU embeds the skill name and description and stores it under the `skill` track.
6. **Retrieve it later.** On a similar future task, memU returns the relevant skill so any connected agent can use the learned workflow.

## Host adapters

"memU runs as a sidecar to a desktop agent, one binary per host. Each binds two seams" (README:130) — `record` and `inject` as defined in Key points (README:132-133). The host table is (README:136-145):

| Host | Binary | Session log it mines | Instruction file it patches |
| --- | --- | --- | --- |
| Codex | `memu-codex` | `~/.codex/sessions/**/*.jsonl` | `~/.codex/AGENTS.md` |
| Claude Code | `memu-claude-code` | `~/.claude/projects/<project>/<session>.jsonl` | `~/.claude/CLAUDE.md` |
| Cursor (Agent/CLI) | `memu-cursor` | `~/.cursor/projects/<project>/agent-transcripts/**.jsonl` | `./AGENTS.md` (per project) |
| OpenClaw | `memu-openclaw` | `~/.openclaw/agents/<agentId>/agent/openclaw-agent.sqlite` (SQLite, read-only) + legacy `<agentId>/sessions/*.jsonl` | `~/.openclaw/workspace/AGENTS.md` |
| Hermes Agent | `memu-hermes` | `~/.hermes/state.db` (SQLite, read-only) | `~/.hermes/SOUL.md` |
| WorkBuddy | `memu-workbuddy` | `~/.workbuddy/projects/<project>/<session>.jsonl` | `~/.workbuddy/SOUL.md` |
| Cola | `memu-cola` | `~/.cola/sessions/<scope>/<session>.jsonl` | `~/.cola/memory-bank/MEMORY.md` |
| pi | `memu-pi` | `~/.pi/agent/sessions/<encoded-cwd>/<session>.jsonl` | `~/.pi/agent/AGENTS.md` |
| **any other agent** | `memu-agent` | found by `memu-agent detect` (JSONL dialect sniffed) | found by `detect` (AGENTS.md / CLAUDE.md / SOUL.md / …) |

For agents without a dedicated binary, "`memu-agent detect` probes the machine and reports per agent whether **memorization** works (a recognizable session log exists) and whether **retrieval** works (an instruction file exists to patch) — then the same verbs run against what it found" (README:147).

## Developer integration

"Applications that already own their conversation history can use `memu memorize` to prepare self-evolve jobs from 1–10 completed sessions for one external agent and commit the resulting memory, skill, and resource changes" (README:163-165). The canonical input contract and complete prepare → agent → commit workflow are in `docs/developer.md` (README:165-166).

## CLI

With memU Cloud, the user signs in at memu.so to view memory files; with local installation, memory lives in the shared store configured by `MEMU_DB` in `~/.memu/config.env` — "typically `~/.memu/memu.sqlite3` for local SQLite, or a Postgres DSN" (README:172). After install the agent retrieves automatically; manual retrieval runs the host adapter (README:174-181):

```bash
memu-codex retrieve "What should I remember about this project?"


# or: memu-claude-code / memu-cursor / memu-openclaw / memu-hermes / memu-workbuddy / memu-cola / memu-pi / memu-agent
```

Install or invoke directly (README:183-189):

```bash
pip install memu-cli         # library + memu + memu-codex CLIs
npx memu-cli --help          # CLI via npm launcher (engine: PyPI package memu-cli)
uvx --from memu-cli memu     # CLI via uv, no install
```

## Configuration

"Values resolve in order: process env → `~/.memu/config.env` → default. memU supports Local and Cloud memory backends, selected by `MEMU_MEMORY_MODE`; an unset mode remains Local for backward compatibility." (README:195-197) For Local / self-hosted, every CLI flag has a matching variable (README:199-207):

| Setting | Env var | Default |
|---|---|---|
| Store | `MEMU_DB` | `./data/memu.sqlite3` (CLI); **required** for host adapters |
| Embedding provider | `MEMU_EMBED_PROVIDER` | `openai` (also: `jina`, `voyage`, `doubao`, `openrouter`); legacy `MEMU_LLM_PROVIDER` still read |
| API key | `MEMU_API_KEY` | the provider's env var, e.g. `OPENAI_API_KEY` |
| Embedding model | `MEMU_EMBED_MODEL` | the provider's default |
| Base URL | `MEMU_BASE_URL` | the provider's default |

## Storage backends

Backend table (README:216-220):

| Provider | DSN | Vector search | Use for |
|---|---|---|---|
| `inmemory` | — | brute-force cosine | tests, throwaway sessions |
| `sqlite` | `sqlite:///path.sqlite3` | brute-force cosine | local/default, single writer |
| `postgres` | `postgresql://...` | pgvector | concurrent access, large stores (`pip install "memu-cli[postgres]"`) |

Verbatim construction example (README:222-227):

```python
service = MemoryService(
    database_config={"metadata_store": {"provider": "postgres", "dsn": "postgresql://..."}},
    embedding_profiles={"default": {"provider": "jina"}},
)
```

No truncated files are noted in this chunk; all claims above are grounded in the chunk's README excerpt (README:1-227) plus its macro-component pointer to `top-level-files/` (README:229-231).

**Covers:** README (project purpose, memory-as-wiki model, install routes, agent matrix, skill-extraction pipeline, host adapters, developer integration, CLI, configuration, storage backends); macro-component pointer `top-level-files/`
