> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Top-Level Files
**In one sentence:** The repository root defines code formatting, build/sync ignore rules, packaging, legacy proxy entrypoint, PR-review automation, contribution/release/security policy, and the multilingual project front door.

## Key points
- `.clang-format` pins C++ style to Google base with `IndentWidth: 2`, `ColumnLimit: 80`, and `PointerAlignment: Left` (`.clang-format:1-9` [chunk:9-36]).
- `.dockerignore` keeps the build context small by excluding `.git`, `__pycache__`, `target/`, `node_modules`, and `web-studio/dist` (`.dockerignore:3-16` [chunk:48-63]).
- `.gitignore` (251 lines) excludes Python/Rust/Node artifacts plus OpenViking-specific paths `/data/*`, `.openviking/media/`, `.openviking/downloads/`, and `.beads/` / `.loopx/` state (`.gitignore:207-218,310-317` [chunk:207-218,310-317]).
- `.gitattributes` marks only directory-installed memory-plugin shared copies as `linguist-generated=true`, while the rest are built at pack time and gitignored (`.gitattributes:4-6` [chunk:74-76]).
- `MANIFEST.in` grafts `src`, vendored `third_party/*`, and `crates/ragfs*` into the sdist while pruning `openviking/bin`, `openviking/lib`, and all `*.so/*.dylib/*.dll/*.exe` binaries (`MANIFEST.in:1-12` [chunk:1182-1204]).
- `Caddyfile` retains only a `:1934` legacy reverse-proxy to `openviking:{$OPENVIKING_SERVER_PORT:1933}` and directs new deployments at port 1933 plus `/studio` (`Caddyfile:23-25` [chunk:613-615]).
- `.pr_agent.toml` (355 lines) configures Qodo PR-Agent with `model = "openai/doubao-seed-2-0-code-preview-260215"`, 8 max findings, and OpenViking-specific custom labels and review rules (`.pr_agent.toml:6-24` [chunk:355-373]).
- `README_CN.md` / `README_JA.md` (337 lines each), `CONTRIBUTING_CN.md` (267 lines) / `CONTRIBUTING_JA.md` (286 lines), `RELEASE.md` (196 lines) / `RELEASE_CN.md` (184 lines), and `SECURITY.md` (12 lines) carry the project pitch, contributor routing, multi-artifact release flows, and private security reporting path (`README_CN.md:1-5`, `RELEASE.md:1-13`, `SECURITY.md:1-2` [chunk:1211-1223,1656-1675,2044-2046]).

---
## Formatting — `.clang-format`
Verbatim excerpt (`.clang-format:1-14` [chunk:9-22]):

```
IndentWidth: 2
TabWidth: 2
Language: Cpp
Standard: Cpp11
BasedOnStyle: Google
AccessModifierOffset: -1
ContinuationIndentWidth: 4
BreakBeforeTernaryOperators: true
BreakBeforeBinaryOperators: false
ColumnLimit: 80
```

Key flags table:

| Flag | Value |
|---|---|
| `BasedOnStyle` | `Google` |
| `Standard` | `Cpp11` |
| `IndentWidth` / `TabWidth` | `2` / `2` |
| `ColumnLimit` | `80` |
| `PointerAlignment` | `Left` (`DerivePointerAlignment: false`) |
| `ConstructorInitializerIndentWidth` | `4` |
| `ConstructorInitializerAllOnOneLineOrOnePerLine` | `true` |
| `AlwaysBreakTemplateDeclarations` | `true` |
| `BreakStringLiterals` | `false` |
| `SortIncludes` | `false` |
| `ReflowComments` | `true` |
| `AllowShortBlocksOnASingleLine` / `AllowShortFunctionsOnASingleLine` / `AllowShortIfStatementsOnASingleLine` / `AllowShortLoopsOnASingleLine` | all `false` |

**Covers:** `.clang-format`

## Build context and ignore rules — `.dockerignore`, `.gitignore`, `.gitattributes`
`.dockerignore` verbatim (`.dockerignore:3-16` [chunk:48-63]):

```
.git
.venv
__pycache__
*.py[cod]
.pytest_cache
.ruff_cache
.coverage
htmlcov
target/
src/build/
docs/.vitepress/dist/
web-studio/node_modules
web-studio/dist
openviking/web_studio/dist
web-studio/.vite
node_modules
*.log
*.tmp
```

`.gitattributes` verbatim, all three rules (`.gitattributes:4-6` [chunk:74-76]):

```
examples/claude-code-memory-plugin/scripts/shared/*.mjs linguist-generated=true
examples/codex-memory-plugin/scripts/shared/*.mjs linguist-generated=true
agent-plugins/servers/shared/*.mjs linguist-generated=true
```

`.gitignore` (251 lines [chunk:79]) — OpenViking-specific block verbatim (`.gitignore:~127-139` [chunk:207-220]):

```
# OpenViking specific
/data/*
/demo_data/*
/benchmark_data/*
.claude
.openviking/media/
.openviking/downloads/
.openviking/config.local.json
*.code-workspace
.openviking.pid
exports/
.local-data/
```

Other `.gitignore` claims present in the chunk: negations preserving shared plugin sources (`!examples/memory-plugin-shared/lib/`, `!examples/opencode-plugin/lib/**`, `!examples/pi-coding-agent-extension/lib/**` [chunk:97-102]); benchmark outputs (`examples/benchmark/outputs/`, `RAGbenchmark/Output/` [chunk:229-235]); Beads/Dolt (`.dolt/`, `*.db`, `.beads/` [chunk:309-314]); LoopX (`.loopx/` [chunk:317]); and pack-time shared copies (`examples/opencode-plugin/lib/shared/`, `examples/dsh-memory-plugin/shared/`, `examples/pi-coding-agent-extension/shared/` [chunk:329-331]).

**Covers:** `.dockerignore`, `.gitignore`, `.gitattributes`

## Packaging — `MANIFEST.in`
Verbatim (25 lines [chunk:1179]; content [chunk:1182-1205]):

```
graft src
graft third_party/leveldb-1.23
graft third_party/spdlog-1.14.1
graft third_party/croaring
graft third_party/rapidjson
include LICENSE
include README.md
include pyproject.toml
include setup.py
include Cargo.toml
include Cargo.lock
graft crates/ragfs
graft crates/ragfs-python
recursive-include openviking *.yaml
# sdist should be source-only: never ship runtime binaries from working tree
prune openviking/bin
prune openviking/lib
recursive-exclude openviking *.so *.dylib *.dll *.exe
global-exclude *.py[cod]
global-exclude __pycache__
global-exclude .git*
global-exclude .DS_Store
prune src/build
```

**Covers:** `MANIFEST.in`

## Reverse proxy — `Caddyfile`
Verbatim entrypoint (26 lines [chunk:588]; block [chunk:613-615]):

```
:1934 {
	reverse_proxy openviking:{$OPENVIKING_SERVER_PORT:1933}
}
```

The header comment states port 1934 is a legacy entrypoint kept for existing deployments and as the upstream target for a TLS-terminating proxy; new deployments connect directly on `OPENVIKING_SERVER_PORT` (1933 by default); Web Studio is served by OV itself at `/studio` with no separate proxy; public HTTPS is added by appending a `{$OPENVIKING_PUBLIC_BASE_URL}` domain block with `reverse_proxy openviking:{$OPENVIKING_SERVER_PORT:1933}` and exposing ports 80/443 (`Caddyfile:1-21` [chunk:591-611]).

**Covers:** `Caddyfile`

## PR automation — `.pr_agent.toml`
355-line Qodo PR-Agent config for the polyglot (Python/TypeScript/Rust) AGPL-3.0 context database [chunk:334-349]. Verbatim global config (`config` [chunk:354-373]):

```toml
[config]
output_relevant_configurations = false
model = "openai/doubao-seed-2-0-code-preview-260215"
fallback_models = []
custom_model_max_tokens = 256000
reasoning_effort = "high"
patch_extra_lines_before = 8
patch_extra_lines_after = 3
allow_dynamic_context = true
response_language = "en-US"
enable_custom_labels = true
```

Ignore globs skip `uv.lock`, `*.lock`, `package-lock.json`, `third_party/**`, `target/**`, `db_test_*/**`, `test_data/**`, `test_data_sync/**`, `.worktrees/**`, `scripts/build_support/**` (`ignore` [chunk:379-397]). Auto-triggers run `/describe`, `/review`, `/improve --pr_code_suggestions.commitable_code_suggestions=false` on open and push (`github_app` [chunk:402-412]). Custom labels present in the chunk: `memory-pipeline`, `async-change`, `embedding-vectorization`, `plugin-bot`, `api-breaking`, `multi-tenant`, `retrieval`, `rust-cli` [chunk:419-442]. Reviewer sets `num_max_findings = 8`, `persistent_comment = true`, `final_update_message = true`, plus `require_score_review`, `require_tests_review`, `require_estimate_effort_to_review`, `require_can_be_split_review`, `require_security_review`, `require_todo_scan`, `require_ticket_analysis_review` (`pr_reviewer` [chunk:446-463]); `extra_instructions` encodes severity classes `[Critical]`/`[Bug]`/`[Perf]`/`[Suggestion]` and rules R1–R11 (async discipline, 6-category memory completeness, quadratic-reprocessing guard, VLM resilience, type safety, license headers, error handling, hook timeout, process lifecycle, API compat, concurrency) [chunk:469-583].

Truncation note: the chunk cuts `.pr_agent.toml` at chunk line 585 with 4940 more characters noted, so the tail of the cross-cutting rules (R11 onward) is not summarised here.

**Covers:** `.pr_agent.toml`

## Contribution guides — `CONTRIBUTING_CN.md`, `CONTRIBUTING_JA.md`
`CONTRIBUTING_CN.md` (267 lines [chunk:618]) and `CONTRIBUTING_JA.md` (286 lines [chunk:889]) are the Chinese and Japanese mirrors of the English guide. Claims present in the chunk:

- One PR solves one cohesive problem; reuse the owning module; no speculative fallbacks/flags/abstractions; delete superseded code/tests/compat paths (`CONTRIBUTING_CN.md` [chunk:639-644]).
- Review priority (not a hard limit): ≤100 changed lines reviewed sooner, ≤200 lines prioritised over larger PRs; generated/vendor/lock files excluded from size; never drop tests/docs to hit a size target (`CONTRIBUTING_CN.md` [chunk:649-656]).
- Pre-implementation Issue/discussion required for public REST/SDK/CLI/MCP/config semantics, storage schema/VFS paths/encrypted files, async task ownership/queues, resource import/Session/memory extraction, retrieval levels/sort, tenant/account/user/peer boundaries, and multi-owner refactors (`CONTRIBUTING_CN.md` [chunk:665-673]).
- Module-routing table dated 2026-06-24–08-24 activity (routes, not exclusive ownership), e.g. `openviking/server` + `openviking/service` → `@qin-ctx`; `openviking/session` → `@chenjw`/`@heaoxiang-ai`/`@fujiajie666`; `openviking/retrieve` → `@zhoujh01`/`@t0saki`; `openviking/storage` + `crates/ragfs*` → `@baojun-zhang` (`CONTRIBUTING_CN.md` [chunk:687-704]).
- Environment: Python 3.10+, Rust 1.91.1+ (source builds/bindings/`ov` CLI), Go 1.22+ (only `sdk/go`), C++17 compiler, CMake 3.15+; `uv sync --all-extras`; `openviking-server init` / `doctor` (`CONTRIBUTING_CN.md` [chunk:708-748]).
- Style: Ruff format+lint and mypy at 100 columns (`uv run ruff format/check`, `uv run mypy`); public APIs get short docstrings (`CONTRIBUTING_CN.md` [chunk:802-813]).
- Tests: verify the smallest meaningful public contract and failure boundaries; prefer updating high-value contract tests; default to no new unit tests/files; repro scripts go in `test_scripts/` (`CONTRIBUTING_CN.md` [chunk:820-828]).
- PRs use Conventional Commits (`feat(parser): …`, `fix(retrieval): …`) with before/after behaviour, root cause, owner module, compat impact, and actual verification commands (`CONTRIBUTING_CN.md` [chunk:847-864]).

**Covers:** `CONTRIBUTING_CN.md`, `CONTRIBUTING_JA.md`

## Project front door — `README_CN.md`, `README_JA.md`
Both 337 lines ([chunk:1208,1439]). Claims present in the chunk:

- OpenViking is an open-source context database for AI agents holding knowledge, memory, and skills in a `viking://` virtual filesystem browsable with `ls`/`tree`/`read`/`write`/`grep`, each directory carrying auto-generated summaries (`README_CN.md` [chunk:1251-1255]).
- Layout excerpt (`viking://` [chunk:1276-1296]) shows `resources/my_project/{docs,src}` alongside `user/{user_id}/{memories,resources,skills,peers}`; loading tiers are L0 abstract (~100 tokens), L1 overview (~2k tokens), L2 full content (`.abstract.md` / `.overview.md` pattern) (`README_CN.md` [chunk:1298-1316]).
- 0.3.22 benchmarks cover LoCoMo and tau2-bench with repro scripts in `./benchmark` (LoCoMo 80–83% with OpenViking vs 24–57% native; tau2 Retail +6.87pp, Airline +11.87pp) (`README_CN.md` [chunk:1320-1330]).
- Quickstart: Python 3.10+ plus embedding model and VLM; `pip install openviking --upgrade`, `openviking-server init` (writes `~/.openviking/ov.conf`), `doctor`, then `ov add-resource` / `ov ls` / `ov tree` / `ov find` / `ov grep`; SDKs under `sdk/python`, `sdk/go`, `sdk/typescript` plus HTTP API (`README_CN.md` [chunk:1334-1360]).
- Agent integrations table (Claude, Codex, Cursor, TRAE, OpenClaw, Hermes, OpenCode, pi, DeerFlow, DSH, Doubao Work, LangChain) plus generic Agent Plugins 1.0 and MCP clients (`README_CN.md` [chunk:1366-1434]).

Truncation note: the chunk cuts `README_CN.md` at chunk line 1436 (5399 more characters) and `README_JA.md` at chunk line 1650 (6730 more characters); content past those points (remaining integration tables and later sections) is not summarised here.

**Covers:** `README_CN.md`, `README_JA.md`

## Releases — `RELEASE.md`, `RELEASE_CN.md`
`RELEASE.md` (196 lines [chunk:1653]) is the English release guide; `RELEASE_CN.md` (184 lines [chunk:1853]) is its Chinese counterpart (the English page additionally documents TypeScript SDK, plugin-npm, and control-plane MCP flows [chunk:1802-1806] that the Chinese page's chunk excerpt does not show). Claims present in the chunk:

- A release publishes a related asset set, not one artifact: `openviking` main package, `openviking-sdk`, Docker images (GHCR + Docker Hub), TOS assets, Rust CLI/npm `ov`, OpenClaw/ClawHub plugin, `@openviking/sdk`, `@openviking/opencode-plugin`, control-plane MCP, and VikingBot via `openviking[bot]`/Docker image (`RELEASE.md` [chunk:1662-1673]).
- Tag conventions verbatim (`RELEASE.md` [chunk:1681-1688]):

| Artifact | Recommended tag / version | Notes |
|---|---|---|
| `openviking` main package | `vX.Y.Z` | Main release tag, for example `v0.3.26`. |
| `openviking-sdk` | `python-sdk@X.Y.Z` | SDK-only tag, for example `python-sdk@0.1.3`. |
| `@openviking/sdk` (TypeScript) | `typescript-sdk@X.Y.Z` | TypeScript SDK tag. |
| Rust CLI / npm CLI | `cli@X.Y.Z` | CLI-only tag, for example `cli@0.2.0`. |
| ClawHub plugin latest | `YYYY.M.D` or `YYYY.M.D-N` | Generated by the workflow or specified manually. |
| ClawHub plugin dev | `YYYY.M.D-dev.N` | Used for the dev channel. |

- Main version resolves from Git tags via `setuptools_scm` (SDK matches only `python-sdk@*`); formal main flow tags `vX.Y.Z`, publishes a GitHub Release, and runs the `03. Release` workflow (build sdist/multi-platform wheels → PyPI → multi-arch Docker → TOS upload) (`RELEASE.md` [chunk:1690-1710]).
- Manual dispatch targets `none`/`testpypi`/`pypi`/`both`; failed publishes recover via `_Publish Distribution` with a build run id; standalone Docker workflow rebuilds images but the formal source of truth stays `03. Release` (`RELEASE.md` [chunk:1714-1735]).
- SDK flow: merge, push `python-sdk@X.Y.Z`, `setuptools_scm` version check, build `sdk/python` → PyPI (`RELEASE.md` [chunk:1750-1767]); CLI flow: push `cli@X.Y.Z` → platform npm packages plus `@openviking/cli` wrapper, skipping already-published versions (`RELEASE.md` [chunk:1769-1782]); ClawHub flow takes `version`/`channel`(`auto`/`dev`/`latest`)`/changelog` inputs (`RELEASE.md` [chunk:1784-1798]); VikingBot ships via `pip install "openviking[bot]"` and the official image (`--without-bot` / `OPENVIKING_WITH_BOT=0` to disable), with no standalone `bot/pyproject.toml` (`RELEASE.md` [chunk:1808-1818]).
- Pre-release checklist (merged changes, green CI, unpublished version, correct tag, synced deps/docs, secrets, notes) and post-release verification (`pip install`, Docker manifests, TOS paths, npm packages, ClawHub channel) plus no-overwrite rule for PyPI/npm (`RELEASE.md` [chunk:1820-1850]).

**Covers:** `RELEASE.md`, `RELEASE_CN.md`

## Security — `SECURITY.md`
12 lines [chunk:2041]. Verbatim reporting path (SECURITY.md [chunk:2044-2046]):

> If you discover potential security issues in the project, or believe you may have found a security issue, please notify the ByteDance security team through our [security center](https://security.bytedance.com/src) or [vulnerability reporting email](mailto:src@bytedance.com). Please do not create public GitHub Issues.

Vulnerabilities are assessed under CVSS 3.1 with coordinated, non-public disclosure until remediation; bounty rules live at the ByteDance Security Response Center (`SECURITY.md` [chunk:2047-2054]).

**Covers:** `SECURITY.md`

**Covers:** `.clang-format`, `.dockerignore`, `.gitattributes`, `.gitignore`, `.pr_agent.toml`, `Caddyfile`, `CONTRIBUTING_CN.md`, `CONTRIBUTING_JA.md`, `MANIFEST.in`, `README_CN.md`, `README_JA.md`, `RELEASE.md`, `RELEASE_CN.md`, `SECURITY.md`
