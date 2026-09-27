PDF-Location: https://github.com/itechmeat/open-second-brain (no local source.pdf; kind repo via git-clone)
# itechmeat/open-second-brain
Source: https://github.com/itechmeat/open-second-brain
Kind: repo
Fetched: 2026-09-26T13:41:53.209359+00:00
Tool: git-clone
Research-Target: /Users/sergii/.ai/knowledge/research_topics/agent_memory/research/AgentBrain
Topic: agent_memory

# itechmeat/open-second-brain

Commit: f6212cd247d0b2a9077e9bb3c703f2b3d284a454

## README

# Open Second Brain

![Open Second Brain - your knowledge, amplified by AI](docs/images/readme-poster.jpg)

> An [Obsidian](https://obsidian.md)-native memory layer for your AI agent. Plain Markdown you own, in the same vault you already use.

Open Second Brain plugs into [Hermes Agent](https://github.com/NousResearch/hermes-agent) and turns your Obsidian vault into a memory layer the agent reads and writes through deterministic CLI / MCP tools. Preferences, signals, evidence, and audit trails are real `.md` files under `Brain/` in the vault you already open in Obsidian every day. You can grep them, version them with git, search them in Obsidian, edit them by hand. No daemon, no vector black box, no hidden state outside the vault.



## What is new

Open Second Brain 1.57.0 runs natively on Windows 10 and 11. It keeps its files under `%LOCALAPPDATA%\open-second-brain`, ships `.cmd` launchers beside the bash ones, and `o2b install-cli` and the MCP host configs work there - see [`install/windows.md`](install/windows.md). Getting there fixed habits that POSIX forgives and Windows does not: SQLite handles that outlive `close()`, renames onto files another process holds open, tar walks in `readdir` order, and paths split on `/`. Several of those were never Windows bugs, just nondeterminism every platform had. The suite passes with 0 failures on Linux and on native Windows, and a `windows-latest` CI job keeps it that way.

Previous release, 1.56.0, taught this install to answer questions about itself: `o2b version`, `second_brain_wiring` views for linked projects and host health, and an instruction block rendered from the capability window the host actually granted. The [CHANGELOG](CHANGELOG.md) has the detail.

Previous releases, 1.55.0 and 1.54.0, made every note write an attributable and revertible event - a write record, a before-image store, a planned revert sealed by a digest, a fleet freeze refused at the one guard every content writer passes, and a per-shard hash chain under every append-only ledger - and turned `visibility:` from a label into a boundary enforced at the three roots every read surface reaches page content through. The [CHANGELOG](CHANGELOG.md) has the detail on both.

Previous releases, 1.53.1 and 1.53.0, closed a dedup pass that proposed the same merge forever and could write a merge cycle, and taught Hermes recall to carry the turn's query without leaving the curated lane that makes injection safe. The [CHANGELOG](CHANGELOG.md) has the detail on both.

Previous release, 1.52.0, was the honesty wave: nothing writes silently, nothing degrades silently. Nine tracker cards were read against the live source before anything was designed, and the reading did most of the work - one card described a feature that had already shipped end to end, one asked for privacy by riding a predicate that is inert in every default install, and four more had premises the source contradicted. What survived is one rule applied eight ways.

A note update now refuses to destroy what it could not read - an unreadable note raises `target_unreadable` instead of parsing as empty, and a blank body over a non-empty note needs an explicit `allow_empty`. `o2b search check` measures instead of inferring: a real pending-vector count replaces a recommendation that told fully embedded vaults to compute their first vectors, an embedder record audit reports when the recorded dimension contradicts the stored data, and `o2b search restamp` repairs the one drift that needs no provider. Every structured Brain record carries a server-derived `origin_channel` no caller can supply; Brain status derives `log_events_since_dream` from the shards it already reads and names an unreadable shard a lower bound; imports read back what they claim and report every missing key by name, and the sessions lane resumes an interrupted transcript at the turn boundary; the three note-producing envelope lanes hand the generating agent a bounded, ownership-filtered wikilink candidate manifest; a failed multi-artifact write leaves a durable dead letter; and a standing census documented - truthfully, at the time - that `visibility: private` was a view filter rather than a privacy boundary, with `o2b search check` saying so on vaults that use the field. That census is the coverage map 1.54.0 built the enforcement against.

The units speak one vocabulary on purpose: attempted, found, and missing with every missing key named, one pure module consumed by the import census, the write accounting, and the embedder audit, pinned by the same census that guards the project's other closed vocabularies. An independent reviewer given the finished branch returned two blocking findings and eleven non-blocking ones, all applied; the [CHANGELOG](CHANGELOG.md) names each.

Previous release, 1.51.0, was about which memories earn their keep: a deterministic salience gate in front of the dream pass's expensive fold, session mining that can only reach the speculative inbox, a provenance-following note delete under one snapshot and an exact count guard, expiration settable and changeable through one normalizer, vault pages staged as Agent Skill drafts that leave the vault only on explicit accept, an architect overview that names its grounding, and the shared needs-llm-step envelope type under all of it. Before it, 1.49.0 through 1.50.3 made a label into a real boundary, taught the installer to see what the machine already has, and fixed a Hermes bridge that discarded the one line of stderr naming why it could not start - the [CHANGELOG](CHANGELOG.md) has the detail.

Previous release, 1.48.0, was about work you can watch, bound and stop: the long passes emit progress and observe interrupts where an interrupt can physically be observed, a successful install states what it measured rather than what it hoped, the project scanner stopped entering what the repository ignores (24148 files visited became 2729), and five independent reviewers returned forty-four reproduced findings against the finished branch, all resolved by measurement rather than argument.

Previous release, 1.47.0, wired what already existed: nine capabilities that were exported, tested and used elsewhere, each with a site that needed them and did not call them - a destructive-operation gate with two call sites against roughly twenty-five destructive operations, and a ranker that read a document's authoring instant nine lines after ranking on the file's modification time.

Previous release, 1.46.0, was about claims the code could not back up. Nine units, four of them reported on the public tracker, and what they have in common is not a subsystem: in every one, the information needed to tell two cases apart either existed already and was thrown away, or cost one filesystem call nobody made. A search that returned nothing could not tell you whether the corpus was empty or the embedder was down, though fifteen degradation signals were being computed and then flattened into prose or dropped. Entity intake decided whether to trust a source from the shape of a string, never asking whether a file was behind it - and the caller supplying that string is the same agent that read the material being classified. Two concurrent writers racing for the same filename lost one of the records outright, measured at twelve dropped events out of twenty-four. The Hermes plugin and the core resolved different vaults while a docstring claimed they were identical, which is why a setup that worked showed as unconfigured for five weeks with nobody able to say why.

You can now say what you want indexed instead of listing everything you do not, with `vault.include_paths`; absent, it changes nothing, and that is measured against the previous release rather than asserted. A write tells you what is wrong with the page it just wrote, instead of deferring to a sweep that may never run. Recall telemetry carries which channel delivered, so a hook that was never installed and a hook that ran and stayed quiet stop looking identical. Every advertised tool parameter is documented and CI keeps it that way, and an unknown argument is named back to you with a suggestion rather than silently ignored.

Some of what was asked for is not here, and the absence is a decision. There was no registry of embedding-provider shutdown dates, because the only way to build one is a hand-maintained table over an open set of endpoints that would rot in place and be believed - a decision 1.48.0 reverses above, having answered that objection rather than set it aside. The schema-completeness guard covers input schemas only, because the output vocabulary declares union-typed fields with no type on purpose and the rule would demand a lie there. And the fix the intake issue asked for - let the host supply the trust verdict instead of the caller - is unbuildable, because no unforgeable caller identity exists in this surface, a conclusion this project had already reached elsewhere and not applied here. What shipped instead removes the free bypass and makes the claim auditable; it does not make the claim true, and the code says so. Four reviewers were then given the finished branch with no knowledge of how it was built, and told that a comment is a claim rather than evidence. They found twelve defects, two of them regressions this work introduced and invisible to its own tests. All are fixed, and the [CHANGELOG](CHANGELOG.md) names them.

Previous release, 1.45.1, fixed a Hermes flush that had been discarded at the boundary since 0.32.0 and a starter vault that went stale ninety days after it was authored. Before it, 1.45.0 was about silence not being an answer, and 1.44.0 about what the index already knew: thirteen units on the retrieval path, most of them values the system computed and discarded before anything could see them. Details for all three live in the [CHANGELOG](CHANGELOG.md).

Previous release, 1.43.0, was about provenance at the boundary: what enters your vault, under whose authority, validated against what, and backed by what proof. Entities an agent extracts from an untrusted source - a scraped page, a fetched article - now land in a quarantine lane instead of becoming first-class Brain entities, and trust is derived from the shape of the source identity rather than from any word list. You can declare in `_brain.yaml` which path prefixes a caller-named write may touch, and a write outside them is refused with the command that resolves it; its authority is the config file, not the caller, because a caller can name itself anything. Note creation gains an idempotent skip whose result tells you which happened, validation before the write lands, and a template mode with a deliberately small grammar. A back-dated note - an imported log, a meeting record - now ranks by the date its body declares rather than by when the file was touched, with the source of that date recorded beside it. Schema mutations can be previewed before they touch the vault, which matters more than it sounds: `--dry-run` was previously parsed and ignored. And an outcome an agent posts about its own work now carries the kernel's own on-disk evidence beside the claim, with a mismatch recorded rather than resolved.

Two things 1.43.0 deliberately did not build are worth knowing about, because their absence was a decision rather than an omission. There is no independent verifier, because agent identity here is an unauthenticated string and two records asserting two names chosen by one process are not two actors. And there is no pack fetched by URL, because a schema pack has no portable representation and no registry to install into. Five independent reviewers were given the finished branch and found thirty defects, nine of them introduced by this work and three of them mechanisms nothing could make fire; one of those three was removed rather than repaired. The [CHANGELOG](CHANGELOG.md) has the detail, including what was found and deliberately left open.

Previous release, 1

... (truncated, 25430 more characters)

## pyproject.toml

```
[build-system]
requires = ["setuptools>=77"]
build-backend = "setuptools.build_meta"

# Open Second Brain v0.7+ runs on the Bun TypeScript runtime; the canonical
# version lives in package.json. This pyproject.toml exists only so the
# Hermes Python shim (`plugins/hermes/__init__.py`) and the root entry
# (`__init__.py`) are addressable as a Python package — Hermes loads them
# in-process as part of its plugin lifecycle. No runtime dependencies, no
# CLI entry points (those moved to `package.json` `bin`).
[project]
name = "open-second-brain"
version = "1.58.2"
description = "Hermes Python shim for Open Second Brain. Most of the project (CLI, MCP server, OpenClaw plugin) is TypeScript on Bun; see package.json."
readme = "README.md"
requires-python = ">=3.11"
license = "MIT"
authors = [{ name = "Open Second Brain contributors" }]
keywords = ["second-brain", "obsidian", "agents", "hermes-plugin"]
dependencies = []

[tool.setuptools]
packages = ["plugins.hermes"]

```

## package.json

```
{
  "name": "open-second-brain",
  "version": "1.58.2",
  "private": false,
  "description": "Second brain for AI agents using Obsidian-compatible Markdown vaults. Works with Hermes, Claude Code, Codex, and OpenClaw.",
  "keywords": [
    "agents",
    "mcp",
    "obsidian",
    "openclaw-plugin",
    "second-brain"
  ],
  "homepage": "https://github.com/itechmeat/open-second-brain",
  "license": "MIT",
  "repository": {
    "type": "git",
    "url": "https://github.com/itechmeat/open-second-brain.git"
  },
  "bin": {
    "o2b": "./scripts/o2b",
    "o2b-mcp": "./scripts/o2b-mcp",
    "vault-log": "./scripts/vault-log"
  },
  "files": [
    "bin/",
    "openclaw/",
    "src/",
    "skills/",
    "scripts/",
    "plugins/",
    "openclaw.plugin.json",
    "README.md",
    "LICENSE",
    "pyproject.toml"
  ],
  "type": "module",
  "scripts": {
    "build:openclaw": "bun build src/openclaw/index.ts --outfile openclaw/index.js --target=node --format=esm --external openclaw/plugin-sdk/plugin-entry",
    "test": "bash scripts/test",
    "lint": "oxlint -c oxlint.json",
    "lint:fix": "oxlint -c oxlint.json --fix",
    "fmt": "oxfmt --write '**/*.{ts,js,json}' '.oxfmtrc.json' '!**/openclaw/index.js' '!.claude/**' --no-error-on-unmatched-pattern",
    "fmt:check": "oxfmt --check '**/*.{ts,js,json}' '.oxfmtrc.json' '!**/openclaw/index.js' '!.claude/**' --no-error-on-unmatched-pattern",
    "typecheck": "tsc --noEmit",
    "validate": "bun run typecheck && bun run lint && bun run test",
    "validate:fix": "bun run lint:fix && bun run fmt",
    "sync-version": "bun run scripts/sync-version.ts",
    "sync-version:check": "bun run scripts/sync-version.ts --check",
    "sync-plugin-mirrors": "bun run scripts/sync-plugin-mirrors.ts",
    "sync-plugin-mirrors:check": "bun run scripts/sync-plugin-mirrors.ts --check",
    "link-ratchet": "bun run scripts/link-ratchet.ts",
    "link-ratchet:check": "bun run scripts/link-ratchet.ts --check",
    "check:paths": "bun run scripts/check-hardcoded-paths.ts",
    "check:paths:strict": "bun run scripts/check-hardcoded-paths.ts --strict",
    "check:hermes-scan": "bun run scripts/hermes-plugin-scan.ts",
    "hooks:install": "git config core.hooksPath .githooks && echo 'git hooks enabled (core.hooksPath=.githooks)'",
    "prepare": "bun scripts/prepare.ts || exit 0"
  },
  "dependencies": {
    "proper-lockfile": "^4.1.2"
  },
  "devDependencies": {
    "@types/bun": "^1.1.0",
    "@types/node": "^22.0.0",
    "@types/proper-lockfile": "^4.1.4",
    "oxfmt": "0.47.0",
    "oxlint": "1.62.0",
    "typescript": "^5.5.0"
  },
  "optionalDependencies": {
    "@node-rs/jieba": "^2.0.1",
    "sqlite-vec": "^0.1.9",
    "tiny-segmenter": "^0.2.0"
  },
  "openclaw": {
    "extensions": [
      "./openclaw/index.js"
    ]
  }
}

```

## Top-level layout

- .agents/ (dir, 1 files, ~20 lines)
- .ai-notes/ (dir, 1 files, ~1 lines)
- .apb/ (dir, 42 files, ~3171 lines)
- .claude-plugin/ (dir, 2 files, ~32 lines)
- .codex-plugin/ (dir, 1 files, ~15 lines)
- .codexignore (~25 lines)
- .gitattributes (~10 lines)
- .githooks/ (dir, 2 files, ~70 lines)
- .github/ (dir, 4 files, ~477 lines)
- .gitignore (~44 lines)
- .mcp.json (~13 lines)
- .oxfmtrc.json (~3 lines)
- __init__.py (~35 lines)
- after-install.md (~175 lines)
- bin/ (dir, 1 files, ~4 lines)
- bun.lock (~186 lines)
- bunfig.toml (~3 lines)
- CHANGELOG.md (~7877 lines)
- CLAUDE.md (~69 lines)
- cli.py (~18 lines)
- docs/ (dir, 582 files, ~105553 lines)
- hooks/ (dir, 18 files, ~3100 lines)
- install/ (dir, 15 files, ~1416 lines)
- install.md (~116 lines)
- LICENSE (~21 lines)
- link-ratchet.json (~10 lines)
- openclaw/ (dir, 1 files, ~3689 lines)
- openclaw.plugin.json (~66 lines)
- oxlint.json (~27 lines)
- package.json (~80 lines)
- plugin.yaml (~13 lines)
- plugins/ (dir, 20 files, ~4613 lines)
- pyproject.toml (~23 lines)
- README.md (~200 lines)
- schemas/ (dir, 4 files, ~153 lines)
- scripts/ (dir, 21 files, ~1536 lines)
- SECURITY.md (~30 lines)
- skills/ (dir, 5 files, ~560 lines)
- src/ (dir, 1042 files, ~251136 lines)
- templates/ (dir, 23 files, ~1660 lines)
- tests/ (dir, 1312 files, ~247239 lines)
- tsconfig.json (~30 lines)
- uv.lock (~8 lines)

