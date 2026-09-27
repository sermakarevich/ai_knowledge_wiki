> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Top-level-files
**In one sentence:** The repository-root layer that exposes the Hermes plugin entrypoints, runtime manifests, install router/verification docs, and shared versioning, hygiene, and toolchain defaults around the Obsidian-vault core.
## Key points
- Root `__init__.py` re-exports `OpenSecondBrainMemoryProvider`, `check_health`, `health`, `register`, `register_cli` from `.plugins.hermes` so the Hermes gateway loads the repo root first (`__init__.py:12-16`).
- Root `cli.py` re-exports `register_cli, run` from `.plugins.hermes.cli` as a lightweight Hermes CLI-discovery shim that avoids executing root `__init__.py` (`cli.py:14-16`).
- `.mcp.json` declares two stdio servers, `open-second-brain` (`o2b mcp`) and always-loaded `open-second-brain-writer` (`o2b mcp --scope writer`) (`.mcp.json:5-12`).
- `plugin.yaml` declares `memory_provider: true` plus seven hooks (`system_prompt_block`, `prefetch`, `sync_turn`, `on_pre_compress`, `on_session_end`, `on_memory_write`, `shutdown`) (`plugin.yaml:5-13`).
- `openclaw.plugin.json` declares plugin id `open-second-brain` v`1.58.2` with five contracted tools and a `configSchema` of `vault`, `instanceName`, `agentName`, `timezone`, `mcpEnabled` (`openclaw.plugin.json:2-5`, `openclaw.plugin.json:7-13`, `openclaw.plugin.json:14-31`).
- `CLAUDE.md` makes `package.json` `version` the single source of truth propagated by `bun run scripts/sync-version.ts`, and requires Codex-mirror regeneration via `bun run sync-plugin-mirrors` (`CLAUDE.md:5-12`, `CLAUDE.md:20-23`).
- `install.md` routes per-runtime installs (nine `o2b install --target <name> --apply` rows plus four pipeline runtimes) and defines `o2b install --check` exit codes `0`/`3`/`5`; `after-install.md` sequences symlink publish, `o2b init`, `o2b doctor`, MCP registration, and `@agent` identity verification (`install.md:22-28`, `install.md:41-46`, `after-install.md:7-10`).
- Hygiene/toolchain roots pin LF checkouts with CRLF batch launchers, shared ignore lists, `printWidth: 100`, oxlint `correctness:error` gate, strict `ES2022`/bundler TS config, and a hermetic Bun test preload (` .gitattributes:5`, `.gitignore:20-22`, `.oxfmtrc.json:2`, `oxlint.json:5-7`, `tsconfig.json:3-5`, `bunfig.toml:3`).
---
## Plugin entrypoints
`__init__.py` docstring states Hermes installs Git plugins by cloning the repo and treating the root as the plugin directory, so this file is the entry the gateway loads first (`__init__.py:1-5`):

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

`cli.py` docstring states Hermes `discover_plugin_cli_commands()` imports `<plugin_root>/cli.py` with synthetic parent packages pre-registered and without executing root `__init__.py`; implementation lives in `plugins/hermes/cli.py` (`cli.py:1-10`):

```python
from .plugins.hermes.cli import register_cli, run

__all__ = ["register_cli", "run"]
```

## Runtime manifests
`.mcp.json` (verbatim):

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

`plugin.yaml` (verbatim):

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

`openclaw.plugin.json`: `id: "open-second-brain"`, `activation: { "onStartup": true }`, `skills: ["./skills"]`, `version: "1.58.2"` (`openclaw.plugin.json:2-6`, `openclaw.plugin.json:6`). Contracted tools (`openclaw.plugin.json:7-13`): `second_brain_status`, `second_brain_query`, `second_brain_capture`, `event_log_append`, `vault_health`.

| Config key | Type | Default | Meaning |
|---|---|---|---|
| `vault` | `string` | — | Absolute path to the Obsidian-compatible vault directory (`openclaw.plugin.json:10-13`) |
| `instanceName` | `string` | — | Human-readable second-brain instance name (`openclaw.plugin.json:14-17`) |
| `agentName` | `string` | — | Identity in `Brain/log/*.md` entries; falls back to `VAULT_AGENT_NAME`, then `@agent` (`openclaw.plugin.json:18-21`) |
| `timezone` | `string` | — | IANA timezone for `HH:MM` stamps; falls back to `VAULT_TIMEZONE`, then host clock (`openclaw.plugin.json:22-25`) |
| `mcpEnabled` | `boolean` | `false` | Also expose an MCP stdio server (optional) (`openclaw.plugin.json:26-29`) |

## Versioning and Codex mirrors
`package.json` `version` is the single source of truth, mirrored into `plugin.yaml`, `plugins/hermes/plugin.yaml`, `.claude-plugin/plugin.json`, `.codex-plugin/plugin.json`, `plugins/codex/.codex-plugin/plugin.json`, `openclaw.plugin.json`, `pyproject.toml`, `uv.lock`; never hand-edit mirrors (`CLAUDE.md:5-9`). Propagate with:

```
bun run scripts/sync-version.ts
```

CI gates on `bun run scripts/sync-version.ts --check` (`CLAUDE.md:14-16`). The bump rides in the feature PR with the `CHANGELOG.md` entry (heading plus bottom link-reference), not as a post-merge step, because `main` is protected (`CLAUDE.md:17-24`).

Codex installs from `./plugins/codex` only and its cache drops symlinks, so `plugins/codex/skills/` is a byte-identical copy of `skills/` and `LICENSE`, `README.md`, `SECURITY.md`, `.codexignore`, plus generated `plugins/codex/hooks/hooks.json` (SessionEnd timeouts capped at 3 s, `commandWindows` cmd.exe form added); every hook command must end in the `o2b-hook <name>` fallback (`CLAUDE.md:20-23`). After changing a skill or `hooks/hooks.json`, run:

```
bun run sync-plugin-mirrors
```

## Install router and post-install verification
`install.md` is a router: one CLI (`o2b`), one always-loaded MCP writer server, one full MCP server, one install adapter per runtime; prerequisites live in `install/prerequisites.md` (plus `install/windows.md` on native Windows) (`install.md:4-8`, `install.md:13-16`). Quick-install table (`install.md:22-28`):

| Runtime | Command | Notes |
|---|---|---|
| Cursor | `o2b install --target cursor --apply` | JSON-merge; restart Cursor after apply |
| Aider | `o2b install --target aider --apply` | managed block + sidecar context; no native MCP |
| opencode | `o2b install --target opencode --apply` | MCP servers + native plugin |
| Grok Build | `o2b install --target grok --apply` | MCP in `~/.grok/config.toml` + native hooks (absolute command) |
| kiro | `o2b install --target kiro --apply` | JSON-merge |
| GitHub Copilot CLI | `o2b install --target copilot-cli --apply` | `copilot mcp add` with JSON fallback |
| Google Gemini CLI | `o2b install --target gemini-cli --apply` | JSON-merge in `~/.gemini/settings.json` |
| Pi (pi.dev) | `o2b install --target pi --apply` | skill symlink, not MCP |
| Generic / other | `o2b install --target generic --apply --out -` | prints payload; never edits external config |

Pipeline runtimes hook into their own installer: Hermes (`install/hermes.md`), OpenClaw (`install/openclaw.md`), Codex (`install/codex.md`), Claude Code (`install/claudecode.md`) (`install.md:32-38`). Guided setup: `o2b init --interactive` reads stdin, prints the plan, requires explicit `yes` (`install.md:42-46`). Verify with `o2b doctor --vault /path/to/vault --repo .` and `o2b install --check`; exit `0` = ok/not-installed, `3` = drift, `5` = configured-but-unreachable (new in v1.46.0) (`install.md:49-57`). Uninstall removes exactly what install wrote per `<vault>/.open-second-brain/install.lock.json` via `o2b uninstall --target <name> --apply`; vault Markdown is never deleted (`install.md:59-67`).

`after-install.md` sequence: `~/.hermes/plugins/open-second-brain/scripts/o2b install-cli` publishes `o2b`/`vault-log` symlinks into `~/.local/bin`; choose `--agent-name`; `o2b init --vault … --name … --agent-name …` plus `o2b doctor --vault … --repo .` expecting `[OK]`; optionally `hermes mcp add open-second-brain --command o2b --args mcp --vault …` then `hermes gateway restart`; verify `event_log_append` without `agent` stamps `@<chosen-agent-name>` not `@agent` (`after-install.md:7-10`, `after-install.md:33-41`, `after-install.md:48-53`, `after-install.md:73-82`). Update is `hermes plugins update open-second-brain` + gateway restart; uninstall order is `o2b uninstall`, `hermes mcp remove`, `o2b uninstall --apply-local --remove-cli`, `hermes plugins remove`, restart — `--remove-cli` before plugin removal so symlink targets still exist (`after-install.md:88-94`, `after-install.md:104-117`). OpenClaw path is native via `openclaw/index.js` (`package.json` `openclaw.extensions`) with `openclaw config set plugins.entries.open-second-brain.config.{vault,instanceName,agentName}` and doctor checks `[OK] openclaw_manifest`, `[OK] openclaw_package_json`, `[OK] openclaw_package_json_extensions` (`after-install.md:132-148`, `after-install.md:156-158`).

## Hygiene, formatting, linting
`.codexignore` excludes local state/secrets/generated artifacts from the Codex plugin payload: `.env`, `.env.*` (except `!.env.example`), `.open-second-brain.local.yaml`, `.open-second-brain/`, `sandbox-vault/`, `node_modules/`, `.bun/`, `.venv/`, `__pycache__/`, `*.py[cod]`, `build/`, `dist/`, `*.egg-info/`, plus `.codegraph/`, `.code-ranker/`, `.zvec-grep/`, `.worktrees/`, `.apb/runs/`, `.apb/tmp/`, `.DS_Store` (`.codexignore:9-33`). `.gitignore` repeats that set plus editor noise (`.idea/`, `.vscode/`, `*.swp`), `.orphaned_at`, `.claude/scheduled_tasks.lock`, `.claude/settings.local.json`, bench runs, and zg-index note that `oxfmt` reads only `.gitignore` (`.gitignore:2-5`, `.gitignore:20-26`, `.gitignore:42-44`). `.gitattributes` forces `* text=auto eol=lf` for cross-platform byte parity while `*.cmd`/`*.bat` keep `text eol=crlf` because cmd.exe misparses LF-only batch files (`.gitattributes:5`, `.gitattributes:9-10`). `.oxfmtrc.json`: `{ "printWidth": 100 }` (`.oxfmtrc.json:2`).

`oxlint.json`: plugins `typescript` + `unicorn`; `correctness:error`, `perf`/`suspicious`:warn; selected rule overrides (`no-console:off`, six warns); ignores `.codegraph`, `node_modules`, `openclaw/**`, `dist`, `coverage`, `.worktrees`, `.claude/worktrees` (`oxlint.json:3-5`, `oxlint.json:6-16`, `oxlint.json:17-25`).

## TypeScript, tests, policy
`tsconfig.json`: `lib ES2023`, `target ES2022`, `module ESNext`, `moduleResolution bundler`, strict plus `noUncheckedIndexedAccess`, `noImplicitOverride`, `noFallthroughCasesInSwitch`, `skipLibCheck`, `resolveJsonModule`, `isolatedModules`, `esModuleInterop`, `types: ["bun"]`; includes `src/**/*.ts`, `tests/**/*.ts`, `scripts/**/*.ts`, `hooks/**/*.ts`, `plugins/opencode/**/*.ts` (`tsconfig.json:3-5`, `tsconfig.json:6-19`, `tsconfig.json:20-26`). `bunfig.toml` `[test]` preloads `./tests/setup.ts` as the hermetic default config/vault for the suite (`bunfig.toml:1-3`).

`SECURITY.md`: ships from `main`, no backports, update via `docs/updating.md` before reporting; private reports at `/security/advisories/new` with `o2b version`, platform, repro steps, no public issue/PR; locally scoped (vault Markdown, user data dir, only configured embedding/rerank/research calls); third-party host issues belong upstream (`SECURITY.md:5-8`, `SECURITY.md:12-19`, `SECURITY.md:24-28`). `link-ratchet.json`: `schema_version: 1`, `ladder:links-unresolved-after-read-resolution@2`, one subject `templates/brain-starter` with `dangling: 22` (`link-ratchet.json:2-9`).

**Covers:** `__init__.py`, `cli.py`, `.mcp.json`, `plugin.yaml`, `openclaw.plugin.json`, `CLAUDE.md`, `install.md`, `after-install.md`, `.codexignore`, `.gitignore`, `.gitattributes`, `.oxfmtrc.json`, `oxlint.json`, `tsconfig.json`, `bunfig.toml`, `SECURITY.md`, `link-ratchet.json`
