[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# top-level-files
**In one sentence:** The repository root defines agent rules, thin launch wrappers, build/test/security metadata, and the macOS one-click installer that together frame Row-Bot as a local-first desktop assistant.
## Key points
- `AGENTS.md` is the canonical instruction file for AI coding agents, declaring Row-Bot a local-first desktop assistant and ranking protection of local data/secrets above all else (AGENTS.md:1-7).
- Root launchers `app.py` and `launcher.py` contain no application logic; both only prepend `src/` to `sys.path` and delegate to `row_bot.app` / `row_bot.launcher.main` (app.py:12-18, launcher.py:12-19).
- `pyproject.toml` is canonical for dependencies, `uv.lock` is the locked resolution, and `requirements.txt` is a generated installer export that must not be hand-edited (AGENTS.md:92-93, requirements.txt:1-4).
- `scripts/run_test_matrix.py` is the executable source of truth for testing, with `fast`, `changed`, `pr`, and `release` tiers plus focused lanes (contracts, subsystem, deterministic, installer-contracts, app-smoke) (AGENTS.md:119-139).
- `pytest.ini` fixes `testpaths = tests` and `pythonpath = src` and declares the `live_provider`, `contract`, `subsystem`, `snapshot`, `installer`, `mcp_transport`, `integration`, `smoke`, `slow`, and `e2e` markers (pytest.ini:1-17).
- `Start Row-Bot.command` implements a fast-path launch versus first-install setup: it reuses an existing `.venv`, starts Ollama when present, performs a version-aware upgrade, and otherwise installs Python/Ollama/venv/packages/Chromium before writing `~/.row-bot/` state (Start Row-Bot.command:43-63).
- `osv-scanner.toml` holds only narrow, time-bound OSV exceptions (`setuptools` 81.0.0, `torch` 2.11.0 / 2.11.0+cpu, npm `image-size` 2.0.2), all expiring 2026-09-30 (osv-scanner.toml:1-37).
- `SECURITY.md` routes vulnerability reports to email instead of public issues, lists shell/browser/prompt-injection/file-access/updater/channel/key scope, and supports only the latest stable release (SECURITY.md:3-37).
---
## Agent instructions (AGENTS.md, CLAUDE.md)
Verbatim identity and priority block:
```
Row-Bot is a local-first desktop AI assistant with provider-aware agent
runtimes, tools, workflows, durable memory/knowledge graph data, MCP, plugins,
skills, channels, voice, Developer Studio, Designer Studio, and platform
installers.
```
(AGENTS.md:7-11). Priorities in order: protect local user data/secrets/local-first defaults; avoid surprise network/provider/channel calls; preserve approval gates and graceful recovery; add deterministic tests; keep Windows and macOS first-class with Linux browser/server healthy (AGENTS.md:13-19).
Ground rules include: no first-party telemetry or hidden phone-home; never commit secrets, tokens, paths, or user data; default tests must not depend on live providers/MCP/channels/network/Ollama models; never hand-edit `requirements.txt`; no runtime code in root wrappers such as `app.py` or `launcher.py` (AGENTS.md:21-44). `CLAUDE.md` is a 7-line pointer: `@AGENTS.md` is canonical and followed first (CLAUDE.md:1-7).
Before-editing sequence: read source and nearby tests; identify subsystem owner and test lane; prefer existing helpers; use structured parsers; add focused tests; update `tests/helpers/source_test_map.py` on cross-subsystem changes; treat sandbox/import/shell/MCP/updater/installer/signing/release as security-sensitive (AGENTS.md:78-88). Release flow: branch changes, `python scripts/cut_release.py X.Y.Z`, run the `pr` matrix, merge after CI, trigger `release.yml` manually, review artifacts/checksums, run `installer-verify.yml`, then local Windows signing, macOS notarization, and clean-machine smoke checks (AGENTS.md:220-232).
## Root launch wrappers (app.py, launcher.py, build_linux_app.sh)
Both Python wrappers only adjust the import path and delegate:
```
ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
```
(app.py:8-11, launcher.py:9-12). Dispatch lines are exact:
```
runpy.run_module("row_bot.app", run_name="__main__")   # app.py:16
from row_bot.launcher import main                        # launcher.py:15
main()                                                   # launcher.py:19 (under __main__)
```
`build_linux_app.sh` is a 7-line convenience wrapper that forwards all arguments to the real builder (build_linux_app.sh:1-7):
```
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec "$SCRIPT_DIR/installer/build_linux_app.sh" "$@"
```
## Test configuration (pytest.ini, test matrix)
`pytest.ini` verbatim core settings (pytest.ini:1-5):
```
testpaths = tests
pythonpath = src
addopts = --ignore=tests/test_output_log.txt --basetemp=.tmp/pytest_tmp_current
cache_dir = .tmp/pytest_cache_current
```
Marker table (pytest.ini:6-17):
| Marker | Meaning in this repo |
|---|---|
| `live_provider` | Opt-in live provider matrix with real calls |
| `contract` | Deterministic interface contracts (fakes, providers, channels, transports) |
| `subsystem` | Deterministic subsystem tests with fakes |
| `snapshot` | Stable rendered/exported snapshot checks |
| `installer` | Installer, launcher, CLI, smoke-test contracts |
| `mcp_transport` | MCP transport and tool-safety contracts |
| `integration` | Deterministic cross-subsystem tests, possibly slower |
| `smoke` | Process-level startup and package smoke checks |
| `slow` | Deterministic but slower tests outside the tight loop |
| `e2e` | Opt-in tests needing real local services |
Matrix commands: focused change `uv run python scripts/run_test_matrix.py fast`; path-scoped `changed --base origin/main`; cross-subsystem/security-sensitive/dependency/installer/release change `pr`; release preflight `release`; focused tiers include `contracts`, `subsystem`, `contract-subsystem`, `coverage`, `deterministic`, `installer-contracts`, `app-smoke`, `legacy-inventory` (AGENTS.md:119-139). Coverage tier measures selected migrated subsystem modules only, writing `.tmp/coverage/migrated-subsystems.xml` against a 55% baseline, not whole-app coverage (AGENTS.md:142-144). Retired shims that must not gain substantive tests: `tests/test_suite.py`, `tests/integration_tests.py`, `tests/test_memory_e2e.py` (AGENTS.md:36-38).
## Dependency and vulnerability metadata (requirements.txt, osv-scanner.toml)
`requirements.txt` header is verbatim (requirements.txt:1-4):
```
# This file is generated from pyproject.toml and uv.lock.
# Do not edit by hand.
# Regenerate with: python scripts/export_locked_requirements.py
# Export command: uv export --locked --all-extras --no-dev --no-hashes --no-emit-project --output-file requirements.txt
```
It pins a 305-line set on the PyTorch CPU extra index (`--extra-index-url https://download.pytorch.org/whl/cpu`), including `nicegui==3.12.1`, `playwright==1.62.0`, `torch==2.11.0` / `2.11.0+cpu`, `setuptools==81.0.0`, plus provider, channel, MCP, voice, and document packages with platform markers (requirements.txt:5-305). `osv-scanner.toml` exception table:
| Package | Version | Ecosystem | Effective until | Reason given |
|---|---|---|---|---|
| `setuptools` | 81.0.0 | PyPI | 2026-09-30 | Torch 2.11 requires setuptools<82 (osv-scanner.toml:6-12) |
| `torch` | 2.11.0 | PyPI | 2026-09-30 | No matching Torchaudio 2.13 CPU release (osv-scanner.toml:14-20) |
| `torch` | 2.11.0+cpu | PyPI | 2026-09-30 | Same Torchaudio pairing reason (osv-scanner.toml:22-28) |
| `image-size` | 2.0.2 | npm | 2026-09-30 | Docusaurus-resolved, docs-build only (osv-scanner.toml:30-37) |
## Ignore and attribute metadata (.dockerignore, .gitignore, .gitattributes, NOTICE)
`.dockerignore` (40 lines) excludes VCS, venv, bytecode/caches, build outputs, frontend artifacts, secrets/keys, databases/logs, and runtime data dirs, including verbatim `src/row_bot/static/client-v2`, `installer/build`, `tests`, `docs`, `docs-content`, `**/.row-bot`, and `**/row-bot-data` (.dockerignore:1-40). `.gitignore` (92 lines) adds Python/Node/installer-signing/user-data/backup/dev-script/test-trace entries, including `api_keys.json`, `installer/apple_signing/`, `installer/windows_signing/`, `vector_store/`, `workflows.py` (replaced by tasks.py in v3.5.0), `.streamlit/` (replaced by NiceGUI in v3.0.0), `monorepo/`, and `frontend/tsconfig.tsbuildinfo` (.gitignore:1-92). `.gitattributes` (36 lines) forces `eol=lf` for `*.sh`, frontend files, workflows/docs/scripts/tests Python and YAML/Markdown, and docs-site assets, while marking generated docs trees (`docs/assets`, `docs/docs`, `docs/img`, `docs/pagefind` with `-whitespace`, `docs/search`, `docs/llms*.txt`, `docs/sitemap.xml`) as `linguist-generated=true` (.gitattributes:1-36). `NOTICE` is verbatim 5 lines: `Row-Bot`, `Copyright 2026 Row-Bot Contributors`, Apache License 2.0 (NOTICE:1-5).
## Security policy (SECURITY.md)
Reports go to `siddsachar@gmail.com`, never a public GitHub issue, with version/commit, OS, reproduction steps, severity, and logs/screenshots/PoC; acknowledgement targeted within 7 days with coordinated fix, security release when needed, and reporter credit unless declined (SECURITY.md:3-19). In-scope areas are verbatim: shell execution and approval gates; browser automation; prompt-injection defenses; local file access and workspace isolation; auto-update manifest, SHA256 verification, and code-signature checks; channel adapters and webhook/tunnel handling; API key storage and OAuth flows (SECURITY.md:21-31). Only the latest stable release is actively supported; critical fixes may be backported when practical (SECURITY.md:33-37).
## macOS entrypoint (Start Row-Bot.command)
The 417-line script is a double-click installer and launcher for Apple Silicon and Intel Macs (Start Row-Bot.command:1-9). It prepends `/opt/homebrew/bin` and `/usr/local/bin` to `PATH` for Finder launches, defines `info`/`ok`/`warn`/`fail` log helpers, resolves `PROJECT_DIR`, `.venv`, `~/.row-bot`, and reads the version from `src/row_bot/version.py` with fallback `4.9.1` (Start Row-Bot.command:13-41). Fast path: when `.venv/bin/activate` exists, it activates, starts Ollama via `ollama serve` when installed but not listening on port 11434, applies a version-aware upgrade (`pip install -r requirements.txt`, `python -m playwright install chromium`, writes `installed_version`) when `INSTALLED_VERSION != ROW_BOT_VERSION`, then `exec python launcher.py` (Start Row-Bot.command:43-63). Install path: requires Python 3.10+ (`find_python` over `python3.12/3.11/3.10/3/python`), offers Homebrew installation, installs Ollama via Homebrew or continues cloud-only with a warning, creates the venv, upgrades pip, installs `requirements.txt`, installs Playwright Chromium, records `row_bot_home` and `installed_version` under `~/.row-bot/`, and scaffolds `Row-Bot.app/Contents` with an `Info.plist` (`ai.row-bot.assistant`) before the file truncates (Start Row-Bot.command:122-200). This file was cut in the chunk: ~4093 trailing characters after the `Info.plist` version-string stanza are not present, so launch/finish steps beyond that point are not summarised.
## Release notes (RELEASE_NOTES.md)
The chunk carries a 5701-line `RELEASE_NOTES.md` but only its head is present; v4.9.1 documents diagnostics-based Computer Use readiness, an optional Calculator confidence check, canonical `Windows Calculator` identity handling, setup-recovery wording, and regression/docs coverage with no migration, CLI, driver, telemetry, or download changes (RELEASE_NOTES.md:1-40). v4.9.0 covers the managed Browser service, native Computer Use on reviewed Cua Driver 0.20.0, desktop Buddy overlay, race-safe conversation cleanup, and live xAI image discovery before the chunk truncates mid-section (RELEASE_NOTES.md:41-190). This file was cut in the chunk: roughly 475410 trailing characters after the Buddy lifecycle section are absent, so later releases and older history are not summarised.
**Covers:** `.dockerignore`, `.gitattributes`, `.gitignore`, `AGENTS.md`, `app.py`, `build_linux_app.sh`, `CLAUDE.md`, `launcher.py`, `NOTICE`, `osv-scanner.toml`, `pytest.ini`, `RELEASE_NOTES.md` (head only, truncated), `requirements.txt`, `SECURITY.md`, `Start Row-Bot.command` (head only, truncated)
