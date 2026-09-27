> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Overview
**In one sentence:** Open Second Brain is an Obsidian-native memory layer for Hermes Agent that stores preferences, signals, evidence, and audit trails as plain Markdown under `Brain/` in the vault you already use (README.md:11-13).
## Key points
- It plugs into Hermes Agent and exposes the vault as a memory layer the agent reads and writes through deterministic CLI / MCP tools (README.md:13).
- Preferences, signals, evidence, and audit trails are real `.md` files under `Brain/`, greppable, git-versionable, searchable in Obsidian, and hand-editable with no daemon, no vector black box, and no hidden state outside the vault (README.md:13).
- Release 1.57.0 runs natively on Windows 10 and 11, keeps files under `%LOCALAPPDATA%\open-second-brain`, ships `.cmd` launchers beside bash ones, and supports `o2b install-cli` and MCP host configs there (README.md:19).
- Release 1.56.0 added self-description via `o2b version`, `second_brain_wiring` views for linked projects and host health, and an instruction block rendered from the granted capability window (README.md:21).
- Releases 1.55.0 and 1.54.0 made every note write an attributable and revertible event (write record, before-image store, digest-sealed planned revert, fleet-freeze guard, per-shard hash chain) and turned `visibility:` from a label into a boundary enforced at the three roots every read surface uses (README.md:23).
- Release 1.46.0 added opt-in indexing scope via `vault.include_paths` (absent by default, changes nothing) plus recall telemetry carrying which channel delivered and named suggestions for unknown tool arguments instead of silent ignores (README.md:41).
- Release 1.43.0 put agent-extracted entities from untrusted sources in a quarantine lane, gated caller-named writes by `_brain.yaml` path prefixes, added idempotent/validated/template note creation, body-declared-date ranking, `--dry-run` schema previews, and kernel on-disk evidence beside agent outcome claims (README.md:47).
---
## README
Identity stated verbatim as `An [Obsidian](https://obsidian.md)-native memory layer for your AI agent. Plain Markdown you own, in the same vault you already use.` (README.md:11), with the poster image path `docs/images/readme-poster.jpg` (README.md:9).
Storage model is verbatim `Brain/` real `.md` files: `Preferences, signals, evidence, and audit trails are real \`.md\` files under \`Brain/\`` (README.md:13). Operations named verbatim: `grep them, version them with git, search them in Obsidian, edit them by hand` (README.md:13). Negations stated verbatim: `No daemon, no vector black box, no hidden state outside the vault.` (README.md:13).
Integration stated verbatim: `plugs into [Hermes Agent](https://github.com/NousResearch/hermes-agent)` and `reads and writes through deterministic CLI / MCP tools` (README.md:13).
## What is new
Verbatim release markers present in the chunk (README.md:19-49):
- `1.57.0` — `runs natively on Windows 10 and 11`, `%LOCALAPPDATA%\open-second-brain`, `.cmd` launchers, `o2b install-cli`, MCP host configs — see `install/windows.md` (README.md:19).
- `1.56.0` — `o2b version`, `second_brain_wiring` views, instruction block from the capability window; detail pointer `[CHANGELOG](CHANGELOG.md)` (README.md:21).
- `1.55.0` and `1.54.0` — `write record`, `before-image store`, `planned revert sealed by a digest`, `fleet freeze refused at the one guard every content writer passes`, `per-shard hash chain`, `visibility:` enforced `at the three roots every read surface reaches page content through` (README.md:23).
- `1.53.1` / `1.53.0`, `1.52.0`, `1.51.0`, `1.48.0`–`1.43.0` entries summarize dedup/merge-cycle fixes, Hermes recall query handling, honesty-wave write/search/import rules, salience gates, progress/interrupt handling, capability wiring, retrieval-path values, and provenance boundaries; each points to `[CHANGELOG](CHANGELOG.md)` for detail (README.md:25-49).
| Name verbatim from chunk | Meaning stated in chunk |
|---|---|
| `vault.include_paths` | Say what you want indexed instead of listing exclusions; absent, it changes nothing (README.md:41) |
| `visibility:` | Turned from a label into a boundary enforced at the three roots (README.md:23); 1.52.0 census documented `visibility: private` as a view filter, with `o2b search check` saying so (README.md:29) |
| `o2b search check` / `o2b search restamp` | Measures pending-vector count, audits embedder dimension drift, repairs provider-free drift (README.md:29) |
| `o2b version` / `second_brain_wiring` | Self-description and linked-project / host-health views (README.md:21) |
| `o2b install-cli` | Works on Windows alongside MCP host configs (README.md:19) |
| `origin_channel` | Server-derived Brain record field no caller can supply (README.md:29) |
| `target_unreadable` / `allow_empty` | Unreadable note raises instead of parsing as empty; blank-over-non-empty needs explicit flag (README.md:29) |
## Macro components
Chunk lists only one entry verbatim: `top-level-files/` (README.md:55). No further components are enumerated in the provided source.
Truncation note: the chunk cuts off mid-sentence at `Previous release, 1` (01-overview.md:51) and the macro-component list ends after `top-level-files/` (01-overview.md:55-56); contents beyond those cut points are not guessed here.
**Covers:** README.md, CHANGELOG.md, install/windows.md, docs/images/readme-poster.jpg, top-level-files/ (list truncated in source)
