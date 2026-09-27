> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Top-level-files
**In one sentence:** The repo root defines the AI-agent integration contract, the lint/security/typecheck hooks, the ignored build artifacts, and the release-please versioning for the Python and TypeScript packages.
## Key points
- `AGENT.md` is the implementation contract for app/extension integration with `stimm`, covering the dual-agent runtime and provider onboarding wizard alignment (AGENT.md:1-4).
- Integration must use `get_provider_catalog()` for wizard discovery UI and must not build discovery UI from `list_runtime_providers()` (AGENT.md:14-15).
- Install commands are derived via `required_extras_for_selection(...)` or `extras_install_command(...)`, installed in the same environment that runs the app, followed by a Python process restart (AGENT.md:16-19).
- App config must never store provider module paths/constructors and never expose secrets in logs, telemetry, or UI snapshots (AGENT.md:20-21).
- Pre-commit runs `ruff format`, `ruff check --fix`, `bandit -r src/`, and `pip-audit` for Python plus `npm run check` in `packages/protocol-ts` for TypeScript changes (.pre-commit-config.yaml:5-9, .pre-commit-config.yaml:10-14, .pre-commit-config.yaml:15-20, .pre-commit-config.yaml:22-27, .pre-commit-config.yaml:32-40).
- Release state is pinned in `.release-please-manifest.json` at `.`: `0.1.13` and `packages/protocol-ts`: `0.1.3`, with `release-please-config.json` linking the two packages for joint versioning (.release-please-manifest.json:2-3, release-please-config.json:19-21).
- `.gitignore` excludes env/venv (`.env`, `.venv/`, `venv/`, `.stimm-build-venv/`), Python build outputs, Node/website build outputs, caches, logs, and the root-owned v1 leftover `bin/` (.gitignore:1-5, .gitignore:7-19, .gitignore:21-26, .gitignore:37-43, .gitignore:45-47).
---
## AGENT.md — integration contract
Objectives verbatim (AGENT.md:6-10):
```
- Integrate Stimm's dual-agent runtime into an existing app.
- Keep provider onboarding wizard aligned with Stimm source-of-truth.
- Avoid runtime/import drift by using Stimm public APIs only.
```
Hard rules verbatim (AGENT.md:13-21):
```
- Use `get_provider_catalog()` for wizard discovery UI.
- Do not build discovery UI from `list_runtime_providers()`.
- Use `required_extras_for_selection(...)` or `extras_install_command(...)` to
  derive install commands.
- Install extras in the same environment that will run the app.
- Restart Python process after extras installation.
- Never store provider module paths/constructors in app config.
- Never expose secrets (API keys/tokens) in logs, telemetry, or UI snapshots.
```
Integration flow (AGENT.md:23-60): Phase 1 (Discover and Configure) installs the base package with `python -m pip install stimm` (AGENT.md:29), reads `catalog = get_provider_catalog()` (AGENT.md:35-36), renders wizard sections from `catalog["stt"]`, `catalog["llm"]`, and `catalog["tts"]` (AGENT.md:40-41), and applies parameter rendering rules for `type` containing `Literal[...]`, `presets`, `required`, `default`, and `description` (AGENT.md:43-47). Phase 2 (Install and Activate) computes the command with exact parameter names `stt`, `tts`, `llm` (AGENT.md:51-56):
```python
from stimm import extras_install_command
cmd = extras_install_command(stt=chosen_stt, tts=chosen_tts, llm=chosen_llm)
```
then executes the install, restarts the process, and instantiates provider classes (AGENT.md:57-60).
Only user choices and parameter values are persisted (AGENT.md:64-65), e.g. verbatim (AGENT.md:67-76):
```json
{
  "stt_provider": "deepgram",
  "tts_provider": "openai",
  "llm_provider": "azure-openai",
  "stt_params": {"model": "nova-3"},
  "tts_params": {"voice": "ash"},
  "llm_params": {"model": "gpt-4o-mini"}
}
```
Troubleshooting notes: too few model values is expected for docs-only providers, a "static" provider list is expected source-of-truth behavior, and post-selection runtime failures mean the extras install or process restart was missed (AGENT.md:78-83). References point to `README.md` and `website/docs/integrations/wizard.md` (AGENT.md:85-88).
## .pre-commit-config.yaml — hooks
All hooks use `language: system` with `uv run` or `bash -c` entries (.pre-commit-config.yaml:5-40). `semgrep` is noted as CI-only due to an incompatible opentelemetry dependency in the local venv (.pre-commit-config.yaml:22).
| Hook id | Entry | Scope (file filter) |
|---|---|---|
| `ruff-format` | `uv run ruff format --force-exclude` (.pre-commit-config.yaml:5-7) | `types: [python]` (.pre-commit-config.yaml:9) |
| `ruff` | `uv run ruff check --fix --force-exclude` (.pre-commit-config.yaml:10-12) | `types: [python]` (.pre-commit-config.yaml:14) |
| `bandit` | `uv run bandit -r src/` (.pre-commit-config.yaml:15-17) | `types: [python]`, `files: ^src/` (.pre-commit-config.yaml:19-20) |
| `pip-audit` | `uv run pip-audit` (.pre-commit-config.yaml:22-24) | `pass_filenames: false` (.pre-commit-config.yaml:27) |
| `protocol-ts-typecheck` (`protocol-ts typecheck`) | `bash -c 'cd packages/protocol-ts && npm run check'` (.pre-commit-config.yaml:32-35) | `files: ^packages/protocol-ts/src/`, `pass_filenames: false` (.pre-commit-config.yaml:38-40) |
## .release-please-manifest.json — pinned versions
Verbatim (.release-please-manifest.json:1-4):
```json
{
  ".": "0.1.13",
  "packages/protocol-ts": "0.1.3"
}
```
## release-please-config.json — release wiring
Top-level `$schema` points at the release-please config schema and `bootstrap-sha` is `dedebf1` (release-please-config.json:2-3). Two packages are configured under `packages` (release-please-config.json:4-18):
| Package key | `release-type` | `package-name` | `changelog-path` |
|---|---|---|---|
| `.` | `python` (release-please-config.json:6) | `stimm` (release-please-config.json:7) | `CHANGELOG.md` (release-please-config.json:8) |
| `packages/protocol-ts` | `node` (release-please-config.json:12) | `@stimm/protocol` (release-please-config.json:13) | `CHANGELOG.md` (release-please-config.json:14) |
Both set `bump-minor-pre-major: true` and `bump-patch-for-minor-pre-major: true` (release-please-config.json:9-10, release-please-config.json:15-16). `linked-versions` ties them together verbatim (release-please-config.json:19-21):
```json
"linked-versions": [
  [".", "packages/protocol-ts"]
]
```
## .gitignore — excluded paths
| Group | Entries |
|---|---|
| Environment (.gitignore:1-5) | `.env`, `.venv/`, `venv/`, `.stimm-build-venv/` |
| Python (.gitignore:7-19) | `__pycache__/`, `*.pyc`, `*.pyo`, `*.pyd`, `*.so`, `*.egg`, `*.egg-info/`, `dist/`, `build/`, `stimm.egg-info/`, `.coverage`, `htmlcov/` |
| Node/TypeScript (.gitignore:21-26) | `node_modules/`, `packages/protocol-ts/dist/`, `website/node_modules/`, `website/build/`, `website/.docusaurus/` |
| OS (.gitignore:28-31) | `.DS_Store`, `*.swp`, `*.swo` |
| IDE (.gitignore:33-35) | `.vscode/`, `.idea/` |
| Cache (.gitignore:37-41) | `.cache/`, `.mypy_cache/`, `.ruff_cache/`, `.pytest_cache/` |
| Logs (.gitignore:43-44) | `*.log` |
| v1 leftovers, root-owned, cannot delete without sudo (.gitignore:46-47) | `bin/` |
The chunk lists 5 source files in full; it notes no truncated files.
**Covers:** `.gitignore`, `.pre-commit-config.yaml`, `.release-please-manifest.json`, `AGENT.md`, `release-please-config.json`
