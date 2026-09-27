> PDF location: https://github.com/NevaMind-AI/memU (no source.pdf fetched; see Source field below)
# NevaMind-AI/memU
Source: https://github.com/NevaMind-AI/memU
Kind: repo
Fetched: 2026-09-26T13:45:52.968270+00:00
Tool: git-clone
Research-Target: /Users/sergii/.ai/knowledge/research_topics/agent_memory/research/AgentBrain
Topic: agent_memory

# NevaMind-AI/memU

Commit: 2c050bc9681a4c0aff1af211a000e73d14f33356

## README

### Personal memory, stored as Wiki

**Across Sessions. Across Agents. Across Devices.**

[![PyPI version](https://badge.fury.io/py/memu-cli.svg)](https://badge.fury.io/py/memu-cli)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Discord](https://img.shields.io/badge/Discord-Join%20Chat-5865F2?logo=discord&logoColor=white)](https://discord.com/invite/hQZntfGsbJ)
[![Twitter](https://img.shields.io/badge/Twitter-Follow-1DA1F2?logo=x&logoColor=white)](https://x.com/memU_ai)

<a href="https://trendshift.io/repositories/17374" target="_blank"><img src="https://trendshift.io/api/badge/repositories/17374" alt="NevaMind-AI%2FmemU | Trendshift" style="width: 250px; height: 55px;" width="250" height="55"/></a>

</div>

---

memU is a lightweight, agent-driven memory system that gives users a shared LLM wiki across sessions, agents, and devices. It automatically distills your own reusable skills from your agent history. Its core memory logic is only 500 lines — compact enough to inspect, understand, and adapt.



## Quick start

memU works with Codex, Claude Code, Cursor, OpenClaw, Hermes, WorkBuddy, Cola, pi, and more. See [Host adapters](#host-adapters-memory-for-desktop-coding-agents).

**Cross-device · Free · Unlimited · [View online](https://memu.so)**

Get your API key from [memu.so](https://memu.so), then send this message to your agent:

> Read [https://memu.pro/SKILL.md](https://memu.pro/SKILL.md), follow its instructions to install and configure memU, API Key is memu_•••••••••(get Api Key from memu.so).



## Agent support

This matrix lists the currently tested memU integrations by operating system.

- **Memorize** — capture useful session knowledge through a scheduled background task and turn it into reusable memory.
- **Retrieve** — bring relevant memory into a future task.
- **⚠️** — supported with an important limitation; see the user note.



### macOS

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



### Windows

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



### Linux

| Agent | Mode | Memorize | Retrieve | User note |
| --- | --- | :---: | :---: | --- |
| Codex | VS Code extension | ❌ | ✅ | |
| Claude Code | CLI | ✅ | ✅ | |
| OpenClaw | 4.23 / 7.1 | ✅ | ✅ | |

Support status reflects the current release and may change as host integrations evolve.



## Automatic skill extraction

Once the scheduled bridging task is installed, memU can turn useful agent history into reusable Markdown skills automatically.

![How memU turns agent history into reusable skills](assets/skill-extraction.png)

1. **Capture new sessions.** The host adapter reads new session history, including messages and tool calls.
2. **Prepare self-evolve jobs.** `prepare` slices each session into a self-contained job with the paths and context the agent needs.
3. **Let the agent decide.** The agent reads related existing skills, then chooses to do nothing, patch an existing skill, or create a new one.
4. **Write readable skill Markdown.** Each skill has a name, description, and reusable workflow, including useful branches, edge cases, and pitfalls.
5. **Commit and index.** `commit` submits changed skill files through `commit_results`; memU embeds the skill name and description and stores it under the `skill` track.
6. **Retrieve it later.** On a similar future task, memU returns the relevant skill so any connected agent can use the learned workflow.

The judgment and synthesis stay inside the agent. `MemoryService` makes no LLM or chat calls; it stores, embeds, and retrieves the skill Markdown the agent prepared.



## Self-hosted

**Private · Single-device · Embedding key required**

To run memU locally with your own storage and embedding provider, send this message to your agent:

> Read [https://raw.githubusercontent.com/NevaMind-AI/MemU/main/SKILL.md](https://raw.githubusercontent.com/NevaMind-AI/MemU/main/SKILL.md) and follow it to install memU.



## Uninstall

To uninstall memU, send this message to your agent:

> Read [https://memu.pro/SKILL.md](https://memu.pro/SKILL.md) and follow its instructions to uninstall memU.

By default, uninstalling removes the host integration and tooling while keeping your memory store and `~/.memu/config.env`, so a later reinstall can resume where you left off. Memory is erased only when you explicitly ask for it.



## Host adapters: memory for desktop coding agents

memU runs as a sidecar to a desktop agent, one binary per host. Each binds two seams:

- **record** — a scheduled bridging task slices new session logs into self-contained job files; the agent itself distills them into memory/skill Markdown; `commit` submits whatever the agent left on disk back through `commit_results`.
- **inject** — a standing instruction in the host's instruction file tells the agent to run `<binary> retrieve` (→ `progressive_retrieve`) before answering.

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

For agents without a dedicated binary, `memu-agent detect` probes the machine and reports per agent whether **memorization** works (a recognizable session log exists) and whether **retrieval** works (an instruction file exists to patch) — then the same verbs run against what it found.

All hosts share one configured memory backend via `~/.memu/config.env` — local
or MemU Cloud. What one host's sessions taught memU, another host retrieves.

Installation is the one-message setup in [Quick start](#quick-start) or [Self-hosted](#self-hosted). [SKILL.md](SKILL.md) is the routing skill it hands your agent: install the package, identify which host you are (falling back to `memu-agent detect` for anything without a dedicated adapter), print that host's packaged install guide (`<binary> docs install`), and follow it — configure the memory backend, register the scheduled bridging task, patch the instruction file, each step behind a verify gate — then report which seams (memorization / retrieval) are now active.

Afterwards `<binary> doctor` proves the whole loop resolves: config, selected
mode, and a live retrieval.

Adding another host means implementing one `TranscriptSource` (where its session logs live, how its records are shaped) plus a `HostSpec`-sized CLI — the pipeline, verbs, and instruction text are shared.



## Developer integration

Applications that already own their conversation history can use `memu memorize`
to prepare self-evolve jobs from 1–10 completed sessions for one external agent and
commit the resulting memory, skill, and resource changes. See [Developer integration](docs/developer.md) for the
canonical input contract and the complete prepare → agent → commit workflow.



## CLI

With memU Cloud, sign in at [memu.so](https://memu.so) to view your memory files. With a local installation, memory lives in the shared store configured by `MEMU_DB` in `~/.memu/config.env` — typically `~/.memu/memu.sqlite3` for local SQLite, or a Postgres DSN.

Once installed, your agent retrieves relevant memory automatically before answering. To retrieve manually, run the adapter for your host:

```bash
memu-codex retrieve "What should I remember about this project?"


# or: memu-claude-code / memu-cursor / memu-openclaw / memu-hermes / memu-workbuddy / memu-cola / memu-pi / memu-agent
```

Install or invoke the CLI directly:

```bash
pip install memu-cli         # library + memu + memu-codex CLIs
npx memu-cli --help          # CLI via npm launcher (engine: PyPI package memu-cli)
uvx --from memu-cli memu     # CLI via uv, no install
```



## Configuration

Values resolve in order: process env → `~/.memu/config.env` → default. memU
supports Local and Cloud memory backends, selected by `MEMU_MEMORY_MODE`; an
unset mode remains Local for backward compatibility.

For Local / self-hosted installations, every CLI flag has a matching variable:

| Setting | Env var | Default |
|---|---|---|
| Store | `MEMU_DB` | `./data/memu.sqlite3` (CLI); **required** for host adapters |
| Embedding provider | `MEMU_EMBED_PROVIDER` | `openai` (also: `jina`, `voyage`, `doubao`, `openrouter`); legacy `MEMU_LLM_PROVIDER` still read |
| API key | `MEMU_API_KEY` | the provider's env var, e.g. `OPENAI_API_KEY` |
| Embedding model | `MEMU_EMBED_MODEL` | the provider's default |
| Base URL | `MEMU_BASE_URL` | the provider's default |

Run `<binary> doctor` to display the resolved mode and verify the same retrieval
path the host uses.



### Storage backends

| Provider | DSN | Vector search | Use for |
|---|---|---|---|
| `inmemory` | — | brute-force cosine | tests, throwaway sessions |
| `sqlite` | `sqlite:///path.sqlite3` | brute-force cosine | local/default, single writer |
| `postgres` | `postgresql://...` | pgvector | concurrent access, large stores (`pip install "memu-cli[postgres]"`) |

```python
service = MemoryService(
    database_config={"metadata_store": {"provider": "postgres", "dsn": "postgresql://..."}},
    embedding_profiles={"default": {"provider": "jina"}},
)
```

## pyproject.toml

```
[project]
name = "memu-cli"
version = "0.11.0-beta.3"
authors = [
    {name = "MemU Team", email = "contact@nevamind.ai"},
]
description = "Personal memory as files — fast retrieval, higher accuracy, lower cost."
readme = "README.md"
# license = {file = "LICENSE"}
requires-python = ">=3.11"
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",

    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3.13",
]
keywords = ["agent", "agentic", "agent-harness", "harness", "loop-engineering", "context-engineering", "context-window", "memory", "personal-information", "workspace", "retrieval", "llm"]
dependencies = [
    "httpx>=0.28.1",
    "numpy>=2.3.4",
    "openai>=2.8.0",
    "pydantic>=2.12.4",
    "sqlmodel>=0.0.27",
    "alembic>=1.14.0",
    "pendulum>=3.1.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/memu"]

[dependency-groups]
dev = [
    {include-group = "lint"},
    {include-group = "test"},
]
lint = [
    "deptry>=0.23.1",
    "mypy>=1.18.2",
    "pre-commit>=4.3.0",
    "ruff>=0.14.3",
    "types-defusedxml>=0.7.0",
]
test = [
    "pytest>=8.4.2",
    "pytest-asyncio>=0.24.0",
    "pytest-cov>=7.0.0",
]

[project.optional-dependencies]
postgres = ["pgvector>=0.3.4", "sqlalchemy[postgresql-psycopgbinary]>=2.0.36"]

[project.scripts]
memu = "memu.cli:main"
# Host adapters get their own binary rather than a subcommand: `memu` is the
# algorithm surface, these are sidecars to a desktop agent (ADR 0008/0009/0010).
memu-codex = "memu.hosts.codex.cli:main"
memu-claude-code = "memu.hosts.claude_code.cli:main"
memu-cursor = "memu.hosts.cursor.cli:main"
memu-openclaw = "memu.hosts.openclaw.cli:main"
memu-hermes = "memu.hosts.hermes.cli:main"
memu-workbuddy = "memu.hosts.workbuddy.cli:main"
memu-cola = "memu.hosts.cola.cli:main"
memu-pi = "memu.hosts.pi.cli:main"
# The generic adapter: any agent without a dedicated binary. `memu-agent
# detect` finds the session log and instruction file, then reports which of
# the two seams (memorization / retrieval) work for that agent.
memu-agent = "memu.hosts.generic.cli:main"

[project.urls]
"Homepage" = "https://github.com/NevaMind-AI/MemU"
"Bug Tracker" = "https://github.com/NevaMind-AI/MemU/issues"
"Documentation" = "https://github.com/NevaMind-AI/MemU#readme"

[tool.mypy]
files = ["src", "tests"]
python_version = "3.11"
disallow_untyped_defs = true
disallow_any_unimported = true
no_implicit_optional = true
check_untyped_defs = true
warn_return_any = true
warn_unused_ignores = true
show_error_codes = true

[[tool.mypy.overrides]]
module = ["tests.*"]
disallow_untyped_defs = false
disallow_incomplete_defs = false
warn_unused_ignores = false
disable_error_code = ["attr-defined", "call-arg"]

[[tool.mypy.overrides]]
module = ["pgvector.*"]
ignore_missing_imports = true

[tool.deptry.per_rule_ignores]
# memu.trust imports certifi only as a fallback, inside a try/except that
# degrades when it is absent — so it is deliberately a transitive dependency
# (via httpx) rather than one this package declares and would then require.
DEP003 = ["certifi"]

[tool.ruff]
target-version = "py311"
line-length = 120
fix = true

[tool.ruff.lint]
select = [
    # flake8-2020
    "YTT",
    # flake8-bandit
    "S",
    # flake8-bugbear
    "B",
    # flake8-builtins
    "A",
    # flake8-comprehensions
    "C4",
    # flake8-debugger
    "T10",
    # flake8-simplify
    "SIM",
    # isort
    "I",
    # mccabe
    "C90",
    # pycodestyle
    "E", "W",
    # pyflakes
    "F",
    # pygrep-hooks
    "PGH",
    # pyupgrade
    "UP",
    # ruff
    "RUF",
    # tryceratops
    "TRY",
]
ignore = [
    # LineTooLong
    "E501",
    # DoNotAssignLambda
    "E731",
]

[tool.ruff.lint.per-file-ignores]
"tests/*" = ["S101"]

[tool.ruff.format]
preview = true

[tool.coverage.report]
skip_empty = true

[tool.coverage.run]
branch = true
source = ["memu"]

[tool.pytest.ini_options]
testpaths = ["tests"]
log_cli = true
log_cli_level = "INFO"
asyncio_mode = "auto"

```

## setup.cfg

```
[flake8]
max-line-length = 120
extend-ignore = E203,W503,E501
exclude =
    .git,
    __pycache__,
    .venv,
    venv,
    build,
    dist,
    *.egg-info,
    .pytest_cache,
    .mypy_cache
per-file-ignores =
    */test*.py:E402
    **/test_*.py:E402
    **/tests.py:E402
    **/quick_memory_test.py:E402

```

## Top-level layout

- .github/ (dir, 10 files, ~549 lines)
- .gitignore (~215 lines)
- .pre-commit-config.yaml (~20 lines)
- .python-version (~1 lines)
- AGENTS.md (~77 lines)
- assets/ (dir, 24 files, ~0 lines)
- CHANGELOG.md (~390 lines)
- CONTRIBUTING.md (~238 lines)
- docs/ (dir, 21 files, ~3917 lines)
- INSTALL-LATEST.md (~136 lines)
- LICENSE.txt (~194 lines)
- Makefile (~22 lines)
- MANIFEST.in (~21 lines)
- npm/ (dir, 3 files, ~152 lines)
- pyproject.toml (~172 lines)
- README.md (~209 lines)
- scripts/ (dir, 1 files, ~89 lines)
- setup.cfg (~18 lines)
- SKILL.md (~170 lines)
- src/ (dir, 157 files, ~21008 lines)
- tests/ (dir, 36 files, ~9877 lines)
- uv.lock (~1389 lines)

