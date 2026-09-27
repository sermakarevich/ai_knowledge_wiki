---
type: Codebase
source: https://github.com/gitpcl/openorchestrator
commit: 1b485ae105596de19d8012ace921701c7b84b99c
date: 2026-09-09
---

> [[summary|Summary]] | [[digest|Digest]] | [[explainer|Plain-language explainer]]

# OpenOrchestrator (`owt`) — Wiki Hub

OpenOrchestrator is a multi-provider cockpit for parallel AI coding: it supervises Claude Code, Pi, Droid, OpenCode (and custom tools) across isolated git worktrees from one keyboard-driven control plane, with Conflict Guard overlap warnings, two-phase merge + queue, and PR-based shipping. Version analyzed: 0.5.0 @ `1b485ae` (2026-07-04). ~16k lines of Python, 7 runtime dependencies, no daemon — one shared SQLite file is the whole memory.

## How to work through this

1. **2 minutes** — read [[summary]] (what it is, architecture, 11-section reference).
2. **10 minutes** — read [[digest]] (every component's headline + key points).
3. **Deep dive** — open one wiki page below for the component you care about; start with [[wiki/targeted]] if you came for the fleet comparison.
4. **No background?** — read [[explainer]] first (analogies, no jargon).
5. **Test yourself** — [[questions]] (answers hidden); **judgment** — [[critical_thinking]] (verdict + what to borrow); **related work** — [[connections]].

## Read This Folder

- [[summary]] — the 11-section technical analysis (rung 1)
- [[digest]] — every component at medium depth (rung 2)
- [[explainer]] — plain-language version with applications
- [[questions]] — retrieval practice (8 questions, answers collapsed)
- [[critical_thinking]] — engineering appraisal and adoption verdict
- [[connections]] — links to related KB entries
- [[source/source]] — provenance pin (repo + exact commit)

## Wiki

| Page | What it covers |
|---|---|
| [[wiki/01-control-plane-cockpit\|01 — Control-Plane Cockpit]] | Textual TUI: lanes, verb dispatch, footer, poll loop |
| [[wiki/02-multiplexer-backends\|02 — Multiplexer Backends]] | `MultiplexerBackend` protocol, tmux vs herdr, selection, attach |
| [[wiki/03-harness-plugin-layer\|03 — Harness Plugin Layer]] | Tool protocol + registry, built-ins, custom tools, auto-detect, `--workflow` |
| [[wiki/04-merge-queue-conflict-guard\|04 — Merge, Queue, Conflict Guard]] | Two-phase merge, overlap detection, queue order, PR shipping, lifecycle |
| [[wiki/05-cli-config-models\|05 — CLI, Config, Models]] | Command inventory, TOML schema, env vars, Pydantic models |
| [[wiki/06-status-mcp-observability\|06 — Status, MCP, Observability]] | SQLite store, lifecycle policy, peer messaging, env setup, logging |
| [[wiki/targeted\|targeted — Fleet Comparison]] | 6 fleet questions answered + 7 borrowable ideas with file:line sources |

## Original Source

- Repository: https://github.com/gitpcl/openorchestrator (commit `1b485ae`, branch `main`, retrieved 2026-09-09; see [[source/source]])
- Reproduce: `git clone https://github.com/gitpcl/openorchestrator && git checkout 1b485ae105596de19d8012ace921701c7b84b99c`
