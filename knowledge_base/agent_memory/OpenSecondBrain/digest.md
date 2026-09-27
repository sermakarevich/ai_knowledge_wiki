> [[index|Wiki]] | [[summary|Summary]]
# itechmeat/open-second-brain — Digest

## 1. [[wiki/01-overview|Overview]]
**In one sentence:** Open Second Brain is an Obsidian-native memory layer for Hermes Agent that stores preferences, signals, evidence, and audit trails as plain Markdown under `Brain/` in the vault you already use (README.md:11-13).
- It plugs into Hermes Agent and exposes the vault as a memory layer the agent reads and writes through deterministic CLI / MCP tools (README.md:13).
- Preferences, signals, evidence, and audit trails are real `.md` files under `Brain/`, greppable, git-versionable, searchable in Obsidian, and hand-editable with no daemon, no vector black box, and no hidden state outside the vault (README.md:13).
- Release 1.57.0 runs natively on Windows 10 and 11, keeps files under `%LOCALAPPDATA%\open-second-brain`, ships `.cmd` launchers beside bash ones, and supports `o2b install-cli` and MCP host configs there (README.md:19).
- Release 1.56.0 added self-description via `o2b version`, `second_brain_wiring` views for linked projects and host health, and an instruction block rendered from the granted capability window (README.md:21).
- Releases 1.55.0 and 1.54.0 made every note write an attributable and revertible event (write record, before-image store, digest-sealed planned revert, fleet-freeze guard, per-shard hash chain) and turned `visibility:` from a label into a boundary enforced at the three roots every read surface uses (README.md:23).
- Release 1.46.0 added opt-in indexing scope via `vault.include_paths` (absent by default, changes nothing) plus recall telemetry carrying which channel delivered and named suggestions for unknown tool arguments instead of silent ignores (README.md:41).
- Release 1.43.0 put agent-extracted entities from untrusted sources in a quarantine lane, gated caller-named writes by `_brain.yaml` path prefixes, added idempotent/validated/template note creation, body-declared-date ranking, `--dry-run` schema previews, and kernel on-disk evidence beside agent outcome claims (README.md:47).

## 2. [[wiki/02-top-level-files|Top-level-files]]
**In one sentence:** The repository-root layer that exposes the Hermes plugin entrypoints, runtime manifests, install router/verification docs, and shared versioning, hygiene, and toolchain defaults around the Obsidian-vault core.
- Root `__init__.py` re-exports `OpenSecondBrainMemoryProvider`, `check_health`, `health`, `register`, `register_cli` from `.plugins.hermes` so the Hermes gateway loads the repo root first (`__init__.py:12-16`).
- Root `cli.py` re-exports `register_cli, run` from `.plugins.hermes.cli` as a lightweight Hermes CLI-discovery shim that avoids executing root `__init__.py` (`cli.py:14-16`).
- `.mcp.json` declares two stdio servers, `open-second-brain` (`o2b mcp`) and always-loaded `open-second-brain-writer` (`o2b mcp --scope writer`) (`.mcp.json:5-12`).
- `plugin.yaml` declares `memory_provider: true` plus seven hooks (`system_prompt_block`, `prefetch`, `sync_turn`, `on_pre_compress`, `on_session_end`, `on_memory_write`, `shutdown`) (`plugin.yaml:5-13`).
- `openclaw.plugin.json` declares plugin id `open-second-brain` v`1.58.2` with five contracted tools and a `configSchema` of `vault`, `instanceName`, `agentName`, `timezone`, `mcpEnabled` (`openclaw.plugin.json:2-5`, `openclaw.plugin.json:7-13`, `openclaw.plugin.json:14-31`).
- `CLAUDE.md` makes `package.json` `version` the single source of truth propagated by `bun run scripts/sync-version.ts`, and requires Codex-mirror regeneration via `bun run sync-plugin-mirrors` (`CLAUDE.md:5-12`, `CLAUDE.md:20-23`).
- `install.md` routes per-runtime installs (nine `o2b install --target <name> --apply` rows plus four pipeline runtimes) and defines `o2b install --check` exit codes `0`/`3`/`5`; `after-install.md` sequences symlink publish, `o2b init`, `o2b doctor`, MCP registration, and `@agent` identity verification (`install.md:22-28`, `install.md:41-46`, `after-install.md:7-10`).
- Hygiene/toolchain roots pin LF checkouts with CRLF batch launchers, shared ignore lists, `printWidth: 100`, oxlint `correctness:error` gate, strict `ES2022`/bundler TS config, and a hermetic Bun test preload (` .gitattributes:5`, `.gitignore:20-22`, `.oxfmtrc.json:2`, `oxlint.json:5-7`, `tsconfig.json:3-5`, `bunfig.toml:3`).

## The system in five moves
1. Start from the vault you already use: preferences, signals, evidence, and audit trails live as plain Markdown under `Brain/`, greppable, versionable, and hand-editable with no daemon or hidden state.
2. Plug that vault into Hermes Agent as a memory layer reached only through deterministic CLI / MCP tools, so every read and write passes a known surface.
3. Expose the repo root as the Hermes load-first entrypoint, with `__init__.py` / `cli.py` shims re-exporting the provider, health, registration, and CLI hooks from `plugins/hermes`.
4. Declare the runtime contracts around that core: two MCP stdio servers, a `memory_provider` manifest with seven lifecycle hooks, and the OpenClaw plugin id, tools, and vault/identity/timezone config schema.
5. Keep releases attributable and revertible: write records, before-images, digest-sealed reverts, hash chains, quarantine lanes, and `visibility:` enforced as a boundary, with version truth in `package.json` and mirrored manifests.
6. Ship and verify per runtime through the `o2b install` router, `init` / `doctor` / `--check` gates, Windows-native paths and launchers, and pinned hygiene/toolchain defaults.
