# Technical Analysis: itechmeat/open-second-brain

**Repository:** https://github.com/itechmeat/open-second-brain
**Version analyzed:** 1.58.2 (from `plugin.yaml` and `openclaw.plugin.json`; README narrative latest noted is 1.57.0)
**Date:** 2026-09-26
**Wiki:** [[index]]

## 1. Overview / What Problem It Solves

Agent frameworks lose working context between turns: preferences, extracted signals, supporting evidence, and audit trails either live in opaque vector stores or disappear with the session. The primary user is a Hermes Agent operator who already keeps notes in Obsidian and needs agent memory that remains inspectable and reversible.

The repo addresses this by making the Obsidian vault itself the memory store. Identity is stated as `An Obsidian-native memory layer for your AI agent. Plain Markdown you own, in the same vault you already use.` (README.md:11). Storage is `Brain/` real `.md` files: `Preferences, signals, evidence, and audit trails are real `.md` files under `Brain/` (README.md:13). The supported operations are `grep them, version them with git, search them in Obsidian, edit them by hand` (README.md:13), with the explicit negation `No daemon, no vector black box, no hidden state outside the vault.` (README.md:13). Integration is `plugs into Hermes Agent` with reads and writes `through deterministic CLI / MCP tools` (README.md:13).

Recent releases harden that model along three axes: portability (1.57.0 runs natively on Windows 10 and 11, files under `%LOCALAPPDATA%\open-second-brain`, `.cmd` launchers, `o2b install-cli` and MCP host configs — README.md:19); self-description (1.56.0 adds `o2b version`, `second_brain_wiring` views for linked projects and host health, and an instruction block rendered from the granted capability window — README.md:21); and write accountability plus read boundaries (1.55.0/1.54.0 add write record, before-image store, digest-sealed planned revert, fleet-freeze guard, per-shard hash chain, and turn `visibility:` from a label into a boundary enforced `at the three roots every read surface reaches page content through` — README.md:23).

## 2. High-Level Architecture

```text
Obsidian vault (+ Brain/*.md)
        │
        ▼
Hermes plugin root (__init__.py / cli.py) ──► Hermes gateway
        │                                          │
        ▼                                          ▼
o2b CLI (install/init/doctor/search/ ──► MCP stdio servers (full + writer,
  mcp/version/uninstall/hook)               alwaysLoad) ──► agent runtimes
        │                                     (Hermes, Claude Code, Codex,
        ▼                                      OpenClaw, Cursor, opencode, …)
install router + verification
(install.md / after-install.md / install.lock.json)
```

Data-flow narrative:

1. The Hermes gateway clones the repo and loads the repository root first; `__init__.py` re-exports the memory provider and registration functions from `.plugins.hermes` (`__init__.py:1-5`, `__init__.py:12-16`). CLI discovery imports `<plugin_root>/cli.py` without executing root `__init__.py` and delegates to `plugins/hermes/cli.py` (`cli.py:1-10`, `cli.py:14-16`).
2. The agent reaches vault content only through two deterministic surfaces: the `o2b` CLI and the two MCP stdio servers declared in `.mcp.json` (`open-second-brain` via `o2b mcp`, `open-second-brain-writer` via `o2b mcp --scope writer` — `.mcp.json:5-12`). `plugin.yaml` declares `memory_provider: true` and seven lifecycle hooks (`system_prompt_block`, `prefetch`, `sync_turn`, `on_pre_compress`, `on_session_end`, `on_memory_write`, `shutdown` — `plugin.yaml:5-13`).
3. Writes land as Markdown under `Brain/` plus accountability sidecars: write record, before-image, digest-sealed planned revert, per-shard hash chain, kernel on-disk evidence beside agent outcome claims (README.md:23, README.md:47). Reads pass `visibility:` enforcement at the three content roots (README.md:23).
4. Retrieval mixes file search with an optional vector lane: `o2b search check` audits pending-vector count and embedder dimension drift, `o2b search restamp` repairs provider-free drift, and 1.52.0 documents `visibility: private` as a view filter (README.md:29). Opt-in scope is `vault.include_paths` (absent by default, changes nothing — README.md:41).
5. Installation and verification are per-runtime adapters driven by one CLI: `o2b install --target <name> --apply` per host, `o2b init`, `o2b doctor`, MCP registration, `@agent` identity check (`install.md:22-28`, `install.md:41-57`, `after-install.md:7-10`, `after-install.md:33-53`). Uninstall removes exactly what install wrote per `<vault>/.open-second-brain/install.lock.json`; vault Markdown is never deleted (`install.md:59-67`).

Persistent state lives in two places: the vault itself (`Brain/*.md` notes, `_brain.yaml` scoping, `.open-second-brain/install.lock.json` ) and the platform user-data directory (`%LOCALAPPDATA%\open-second-brain` on Windows per README.md:19; `~/.local/bin` symlinks and `~/.hermes/plugins/` on Unix-style installs per `after-install.md:7-10`). There is no daemon and no external database in the default path (README.md:13).

## 3. The Vault-Native Memory Record

The central concept is a plain-Markdown memory record stored under `Brain/` and versioned with the vault. Representation is files, not rows: preferences, signals, evidence, and audit trails as `.md` (README.md:13). Records carry frontmatter controls attested in the wiki: `visibility:` (boundary, not label — README.md:23; `visibility: private` as view filter — README.md:29), `vault.include_paths` index scope (README.md:41), `origin_channel` as a server-derived Brain record field no caller can supply (README.md:29), and body-declared dates used for ranking (README.md:47). Caller-named writes are gated by `_brain.yaml` path prefixes (README.md:47).

Named kinds/types attested with file:line:

- `OpenSecondBrainMemoryProvider` re-exported from `.plugins.hermes` (`__init__.py:12-16`) — the Hermes memory-provider object.
- `check_health` / `health` (`__init__.py:12-16`) — provider health probes surfaced also as the `vault_health` contracted tool (`openclaw.plugin.json:7-13`).
- `register` / `register_cli` (`__init__.py:12-16`) and `run` (`cli.py:14-16`) — plugin and CLI registration.
- `second_brain_status`, `second_brain_query`, `second_brain_capture`, `event_log_append`, `vault_health` (`openclaw.plugin.json:7-13`) — the five contracted OpenClaw tools.
- `second_brain_wiring` views for linked projects and host health (`README.md:21` via 1.56.0).
- `visibility: private`, `origin_channel`, `target_unreadable`, `allow_empty`, `vault.include_paths` (README.md:29, README.md:41) — record and query controls.

Key queries are file-search plus the `o2b search` lane (`o2b search check`, `o2b search restamp` — README.md:29) and the `second_brain_query` tool (`openclaw.plugin.json:7-13`). Verbatim storage contract:

```markdown
Preferences, signals, evidence, and audit trails are real `.md` files under `Brain/`
```

(README.md:13). Verbatim access contract: `grep them, version them with git, search them in Obsidian, edit them by hand` with `No daemon, no vector black box, no hidden state outside the vault.` (README.md:13).

## 4. LLM / External Service Integration

No LLM provider, model name, or API key is named in the two available wiki pages. External coupling is to agent runtimes and hosts, not to a foundation-model endpoint: Hermes Agent as the native host (README.md:13), plus install adapters for Cursor, Aider, opencode, Grok Build, Kiro, GitHub Copilot CLI, Google Gemini CLI, Pi, generic, Hermes, OpenClaw, Codex, and Claude Code (`install.md:22-38`).

The only model-adjacent calls attested are optional local maintenance operations: `o2b search check` (pending-vector count, embedder dimension drift audit) and `o2b search restamp` (provider-free drift repair) (README.md:29). `SECURITY.md` scopes network use to `only configured embedding/rerank/research calls` (`SECURITY.md:24-28`), but the wiki pages do not name which embedding, rerank, or research providers are configured, nor the environment variables that hold their credentials. No required-versus-optional call matrix can be grounded beyond this: the Markdown read/write path requires no external service; the vector lane is provider-free for repair and presumably requires a configured embedder only for indexing, which the available pages do not specify.

## 5. The Capture–Recall–Install Pipeline

Primary workflow is write accountable Markdown, read it back through enforced boundaries, and keep every host wired to the same vault.

1. `o2b init [--interactive] [--vault … --name … --agent-name …]` — guided setup; reads stdin, prints the plan, requires explicit `yes` (`install.md:42-46`); full form in `after-install.md:33-41`.
2. `o2b install --target <name> --apply` — per-runtime adapter; nine CLI rows (cursor, aider, opencode, grok, kiro, copilot-cli, gemini-cli, pi, generic) plus four pipeline runtimes (hermes, openclaw, codex, claudecode) (`install.md:22-38`). Publishes `o2b`/`vault-log` symlinks via `o2b install-cli` (`after-install.md:7-10`).
3. `second_brain_capture` / `event_log_append` (`openclaw.plugin.json:7-13`) — agent write path; every note write produces an attributable, revertible event with write record, before-image store, digest-sealed planned revert, fleet-freeze guard at the single guard every content writer passes, and per-shard hash chain (README.md:23). Untrusted-source entities go to a quarantine lane; caller-named writes are gated by `_brain.yaml` prefixes; creation is idempotent/validated/templated (README.md:47).
4. `second_brain_query` / `o2b search check` / `o2b search restamp` (`openclaw.plugin.json:7-13`; README.md:29) — recall path with `visibility:` enforced at the three roots (README.md:23), `visibility: private` view filtering, `origin_channel` attribution, `target_unreadable` raising instead of empty-parsing, `allow_empty` gating blank-over-non-empty overwrite, body-declared-date ranking, `--dry-run` schema previews, and kernel on-disk evidence beside outcome claims (README.md:29, README.md:47).
5. `o2b doctor --vault /path/to/vault --repo .` and `o2b install --check` (`install.md:49-57`) — verification; exit `0` = ok/not-installed, `3` = drift, `5` = configured-but-unreachable (new in v1.46.0). `second_brain_wiring` plus `o2b version` provide self-description and host-health views (README.md:21). `event_log_append` without `agent` must stamp `@<chosen-agent-name>` not `@agent` (`after-install.md:73-82`).
6. `o2b uninstall --target <name> --apply` keyed by `install.lock.json` (`install.md:59-67`); Hermes update is `hermes plugins update open-second-brain` plus gateway restart; full removal order ends with `hermes plugins remove` and restart, with `--remove-cli` run before plugin removal so symlink targets still exist (`after-install.md:88-117`).

Every function above is a CLI/tool entry point; the wiki pages do not expose the implementing `file.py:line` for the `plugins/hermes` internals, only the root shims (`__init__.py:12-16`, `cli.py:14-16`).

## 6. Key Files

| File | Lines | What It Does |
|---|---|---|
| `__init__.py` | root | Hermes gateway entry; re-exports provider, health, register functions (`__init__.py:1-16`) |
| `cli.py` | root | CLI-discovery shim delegating to `plugins/hermes/cli.py` without executing root `__init__` (`cli.py:1-16`) |
| `.mcp.json` | root | Declares full and always-loaded writer MCP stdio servers (`.mcp.json:5-12`) |
| `plugin.yaml` | root | Hermes manifest: `memory_provider: true`, seven hooks (`plugin.yaml:5-13`) |
| `openclaw.plugin.json` | root | OpenClaw manifest: id, v1.58.2, five tools, vault/agent/timezone config schema |
| `package.json` | root | Single source of truth for `version`; mirrors propagated by `sync-version.ts` (`CLAUDE.md:5-9`) |
| `install.md` | root/docs | Install router: per-target table, guided init, doctor/check exit codes, uninstall rule |
| `after-install.md` | root/docs | Post-install sequence: symlinks, init, doctor, MCP registration, identity check, update/remove order |
| `install/windows.md` | docs | Native Windows 10/11 install detail pointer (README.md:19) |
| `install/prerequisites.md` | docs | Prerequisite pointer for all runtimes (`install.md:4-8`) |
| `README.md` | root | Product identity, storage model, release markers 1.43.0–1.57.0 (README.md:9-49) |
| `CHANGELOG.md` | root | Per-release detail behind every README release pointer (README.md:21-49) |
| `CLAUDE.md` | root | Versioning and Codex-mirror regeneration policy (`CLAUDE.md:5-23`) |
| `SECURITY.md` | root | Support, disclosure, and local-scope policy (`SECURITY.md:5-28`) |
| `tsconfig.json` | root | Strict TS config: ES2022/ES2023, bundler resolution, include set (`tsconfig.json:3-26`) |
| `oxlint.json` | root | Lint gate: correctness:error, selected plugins and ignores (`oxlint.json:3-25`) |
| `bunfig.toml` | root | Test preload `./tests/setup.ts` as hermetic default (`bunfig.toml:1-3`) |
| `link-ratchet.json` | root | Link-integrity ladder state for `templates/brain-starter` (`link-ratchet.json:2-9`) |
| `docs/images/readme-poster.jpg` | docs | README poster image asset (README.md:9) |

Structural-importance ordering is by load path (entrypoints, manifests), then install/verify, then policy/toolchain. Inner implementation directories beyond `top-level-files/` were truncated in the source list (README.md:55) and are not enumerated here.

## 7. Dependencies

The two wiki pages name hosts, toolchains, and config files but publish no package-manager manifest lines with exact semver ranges. Constraints below are the exact strings stated in the wiki; where the wiki states no constraint, that is marked.

| Package | Version constraint | Purpose |
|---|---|---|
| Hermes Agent (NousResearch/hermes-agent) | *no constraint stated in wiki* | Native host gateway loading repo root as plugin (README.md:13) |
| Obsidian | *no constraint stated in wiki* | Vault UI: search, edit, browse `Brain/*.md` (README.md:13) |
| git | *no constraint stated in wiki* | Versioning of `Brain/*.md` (README.md:13) |
| Bun | *no constraint stated; invoked as `bun run …`* | Version propagation, mirror sync, test preload (`CLAUDE.md:5-23`, `bunfig.toml:1-3`) |
| TypeScript toolchain | `target ES2022`, `lib ES2023`, `module ESNext`, `moduleResolution bundler` | Strict build config with `noUncheckedIndexedAccess` et al. (`tsconfig.json:3-19`) |
| oxlint | `correctness:error` gate; plugins `typescript` + `unicorn` | Lint gate with named rule overrides and ignores (`oxlint.json:3-25`) |
| oxfmt | `printWidth: 100` | Formatter default (`.oxfmtrc.json:2`) |
| Node/cmd launchers | `*.cmd`/`*.bat` kept `text eol=crlf`; all else `text=auto eol=lf` | Windows-native execution parity (`.gitattributes:5-10`) |
| MCP host apps (Cursor, opencode, Grok, Kiro, Copilot CLI, Gemini CLI, Aider, Pi, Codex, Claude Code, OpenClaw) | *no constraints stated in wiki* | Install targets consuming MCP servers or skill symlinks (`install.md:22-38`) |
| Optional embedder / reranker / research service | *provider and version not named in wiki* | Only configured external calls; locally scoped otherwise (`SECURITY.md:24-28`) |

Plugin self-version pins attested verbatim: `plugin.yaml` `version: "1.58.2"`, `openclaw.plugin.json` `version: "1.58.2"`; `package.json` `version` is the source all eight mirrors follow (`CLAUDE.md:5-9`).

## 8. CLI / Usage Surface

Entry points: repository root as Hermes plugin directory (`__init__.py:1-5`); `<plugin_root>/cli.py` for Hermes CLI discovery (`cli.py:1-10`); `scripts/o2b` as the MCP server command (`${CLAUDE_PLUGIN_ROOT}/scripts/o2b` — `.mcp.json:5-12`); `openclaw/index.js` via `package.json` `openclaw.extensions` for the native OpenClaw path (`after-install.md:132-148`).

| Command | Effect |
|---|---|
| `o2b install --target <cursor\|aider\|opencode\|grok\|kiro\|copilot-cli\|gemini-cli\|pi\|generic> --apply` | Per-runtime install; generic prints payload only (`install.md:22-28`) |
| `o2b install` for hermes / openclaw / codex / claudecode | Pipeline-runtime install via dedicated pages (`install.md:32-38`) |
| `o2b install --check` | Exit `0` ok/not-installed, `3` drift, `5` configured-but-unreachable (`install.md:49-57`) |
| `o2b install-cli` | Publishes `o2b`/`vault-log` symlinks into `~/.local/bin` (`after-install.md:7-10`); Windows-capable (README.md:19) |
| `o2b init [--interactive] [--vault … --name … --agent-name …]` | Guided setup requiring explicit `yes` (`install.md:42-46`, `after-install.md:33-41`) |
| `o2b doctor --vault /path/to/vault --repo .` | Verification expecting `[OK]` lines (`after-install.md:33-53`, `after-install.md:156-158`) |
| `o2b mcp` / `o2b mcp --scope writer` | Full vs always-loaded writer MCP stdio servers (`.mcp.json:5-12`) |
| `o2b version` | Self-description (new in 1.56.0 — README.md:21) |
| `o2b search check` / `o2b search restamp` | Vector-lane audit and provider-free repair (README.md:29) |
| `o2b uninstall --target <name> --apply` | Removes exactly what install wrote per `install.lock.json` (`install.md:59-67`) |
| `o2b-hook <name>` | Required trailing fallback for every hook command (`CLAUDE.md:20-23`) |
| `vault-log` | Published alongside `o2b` (`after-install.md:7-10`) |
| `hermes mcp add/remove`, `hermes gateway restart`, `hermes plugins update/remove` | Host-side wiring lifecycle (`after-install.md:48-117`) |
| `bun run scripts/sync-version.ts [--check]` | Propagate/check version mirrors; CI-gated (`CLAUDE.md:5-16`) |
| `bun run sync-plugin-mirrors` | Regenerate Codex mirrors after skill/hook changes (`CLAUDE.md:20-23`) |

| Env var | Used for |
|---|---|
| `VAULT_AGENT_NAME` | Fallback for `agentName` identity in `Brain/log/*.md` (`openclaw.plugin.json:18-21`) |
| `VAULT_TIMEZONE` | Fallback for `timezone` `HH:MM` stamps (`openclaw.plugin.json:22-25`) |
| `CLAUDE_PLUGIN_ROOT` | Base for MCP server command path (`${CLAUDE_PLUGIN_ROOT}/scripts/o2b` — `.mcp.json:5-12`) |
| `%LOCALAPPDATA%` | Windows user-data root (`%LOCALAPPDATA%\open-second-brain` — README.md:19) |

| Config key | Default | Meaning |
|---|---|---|
| `vault` | — (required) | Absolute Obsidian vault path (`openclaw.plugin.json:10-13`) |
| `instanceName` | — | Human-readable instance name (`openclaw.plugin.json:14-17`) |
| `agentName` | `VAULT_AGENT_NAME` → `@agent` | Log identity; verify `@<chosen>` not `@agent` (`openclaw.plugin.json:18-21`, `after-install.md:73-82`) |
| `timezone` | `VAULT_TIMEZONE` → host clock | IANA timezone for stamps (`openclaw.plugin.json:22-25`) |
| `mcpEnabled` | `false` | Also expose MCP stdio server (`openclaw.plugin.json:26-29`) |
| `vault.include_paths` | absent (no-op) | Opt-in index scope; absent changes nothing (README.md:41) |
| `visibility:` | — | Read boundary enforced at three roots; `private` acts as view filter (README.md:23, README.md:29) |
| `_brain.yaml` path prefixes | — | Gate caller-named writes (README.md:47) |
| `<vault>/.open-second-brain/install.lock.json` | — | Uninstall source of truth; vault Markdown never deleted (`install.md:59-67`) |

## 9. Extensibility Points

- New Hermes lifecycle behavior: extend the seven hooks in `plugin.yaml` (`system_prompt_block`, `prefetch`, `sync_turn`, `on_pre_compress`, `on_session_end`, `on_memory_write`, `shutdown` — `plugin.yaml:5-13`) with implementation behind `.plugins.hermes` re-exported through `__init__.py` (`__init__.py:12-16`).
- New CLI surface: add to `plugins/hermes/cli.py` behind the `cli.py` shim's `register_cli`/`run` re-export (`cli.py:14-16`); every hook command must end in the `o2b-hook <name>` fallback (`CLAUDE.md:20-23`).
- New agent tool: extend the five contracted tools (`second_brain_status`, `second_brain_query`, `second_brain_capture`, `event_log_append`, `vault_health`) and `configSchema` in `openclaw.plugin.json` (`openclaw.plugin.json:7-31`).
- New host target: add a row to the `o2b install --target` table pattern plus a pipeline page under `install/` following `install/hermes.md`, `install/openclaw.md`, `install/codex.md`, `install/claudecode.md` (`install.md:22-38`).
- New index scope or record control: extend `vault.include_paths`, `visibility:` handling, or `_brain.yaml` prefix gating (README.md:23, README.md:41, README.md:47) at all three read roots, not just one surface.
- New MCP scope: add a server beside the two in `.mcp.json` following the `o2b mcp --scope writer` + `alwaysLoad` pattern (`.mcp.json:5-12`).
- Versioned release: bump `package.json` `version`, propagate with `bun run scripts/sync-version.ts`, add the `CHANGELOG.md` heading plus bottom link-reference in the same PR (`CLAUDE.md:5-24`); regenerate Codex payload with `bun run sync-plugin-mirrors` after skill/hook edits (`CLAUDE.md:20-23`).

## 10. Limitations and Gotchas

- **Wiki coverage is truncated; inner implementation is unmapped.** The chunk cuts off mid-sentence (`01-overview.md:51`) and the macro-component list ends after `top-level-files/` (README.md:55), so only root entrypoints, manifests, install docs, and hygiene are grounded here; `plugins/hermes` internals, `Brain/` templates, and retrieval code have no attested file:line in the available pages.
- **Version mirrors are fragile by design.** `package.json` feeds eight mirrors (`plugin.yaml`, both Hermes/Codex plugin manifests, `openclaw.plugin.json`, `pyproject.toml`, `uv.lock` — `CLAUDE.md:5-9`); hand-editing a mirror instead of running `bun run scripts/sync-version.ts` fails the `--check` CI gate, and the bump plus `CHANGELOG.md` entry must ride the feature PR because `main` is protected (`CLAUDE.md:14-24`).
- **Codex installs silently drop symlinks.** Codex reads only `./plugins/codex` and its cache drops symlinks, so `plugins/codex/skills/` must remain a byte-identical copy with generated `hooks.json` (3 s SessionEnd cap, `commandWindows` cmd.exe form); forgetting `bun run sync-plugin-mirrors` after a skill or hook edit ships stale behavior (`CLAUDE.md:20-23`).
- **Uninstall order matters.** Full Hermes removal must run `o2b uninstall --apply-local --remove-cli` before `hermes plugins remove` so symlink targets still exist, followed by gateway restart; reversing the order orphans symlinks (`after-install.md:104-117`). Vault Markdown is never deleted by uninstall, so host-config drift (exit `3`) and unreachable-config (exit `5`) must be distinguished with `o2b install --check` (`install.md:49-67`).
- **`visibility:` and quarantine rules are easy to misread.** `visibility:` is enforced at the three content roots, not a display label (README.md:23); `origin_channel` cannot be caller-supplied (README.md:29); unreadable notes raise (`target_unreadable`) and blank-over-non-empty writes require `allow_empty` (README.md:29); untrusted entities sit in a quarantine lane and caller-named writes outside `_brain.yaml` prefixes are refused (README.md:47).
- **Platform paths diverge.** Windows state lives under `%LOCALAPPDATA%\open-second-brain` with `.cmd` launchers (README.md:19) while Unix-style docs publish into `~/.local/bin` and `~/.hermes/plugins/` (`after-install.md:7-10`); scripts assuming one layout break on the other.

## 11. How It Compares to Alternatives

- **Mem0 (mem0ai/mem0):** managed/ self-hosted memory API with vector + graph extraction behind an SDK. Open Second Brain inverts this: storage is human-readable vault Markdown with git history instead of an opaque store, at the cost of leaving semantic ranking to a thinner optional vector lane (`o2b search check/restamp` — README.md:29).
- **Zep / Graphiti:** temporal knowledge-graph memory aimed at multi-session agents. Open Second Brain offers auditability (write record, before-image, digest-sealed revert, per-shard hash chain — README.md:23) but attests no entity/edge graph model in the available pages; provenance is file-level (`origin_channel`, kernel on-disk evidence — README.md:29, README.md:47).
- **Obsidian Smart Connections / similar vault RAG plugins:** embedding search inside Obsidian for human recall. Open Second Brain targets the agent instead: deterministic CLI/MCP tools plus Hermes lifecycle hooks (`memory_provider: true`, seven hooks — `plugin.yaml:5-13`) so the same files serve both human browsing and machine read/write (README.md:13).
- **Basic Memory (basicmachines-co/basic-memory):** Markdown-on-disk agent memory with CLI/MCP, closest in spirit. Differentiators attested here are the Hermes-native provider entrypoints (`__init__.py:12-16`, `cli.py:14-16`), the nine-plus-four runtime install router (`install.md:22-38`), and the Windows-native path with `.cmd` launchers and `%LOCALAPPDATA%` state (README.md:19).

Positioning: choose Open Second Brain when the Obsidian vault must remain the source of truth for both human and agent, with every write attributable and revertible on disk; choose a vector/graph memory service when ranking quality or entity-temporal reasoning matters more than file-level inspectability.

## Appendix: Selected Code Snippets

1. Hermes gateway entry — `__init__.py:12-16` (docstring context `__init__.py:1-5`):

```python
from .plugins.hermes import (
    OpenSecondBrainMemoryProvider,
    check_health,
    health,
    register,
    register_cli,
)

__all__ = [
    "OpenSecondBrainMemoryProvider",
    "check_health",
    "health",
    "register",
    "register_cli",
]
```

2. CLI-discovery shim — `cli.py:14-16` (docstring context `cli.py:1-10`):

```python
from .plugins.hermes.cli import register_cli, run

__all__ = ["register_cli", "run"]
```

3. MCP server declarations — `.mcp.json:5-12`:

```json
{
  "mcpServers": {
    "open-second-brain": {
      "command": "${CLAUDE_PLUGIN_ROOT}/scripts/o2b",
      "args": ["mcp"]
    },
    "open-second-brain-writer": {
      "command": "${CLAUDE_PLUGIN_ROOT}/scripts/o2b",
      "args": ["mcp", "--scope", "writer"],
      "alwaysLoad": true
    }
  }
}
```

4. Hermes manifest — `plugin.yaml:5-13`:

```yaml
name: open-second-brain
version: "1.58.2"
description: "Open Second Brain - native Hermes memory provider backed by an Obsidian-compatible Markdown vault."
author: "Open Second Brain contributors"
memory_provider: true
hooks:
  - system_prompt_block
  - prefetch
  - sync_turn
  - on_pre_compress
  - on_session_end
  - on_memory_write
  - shutdown
```
