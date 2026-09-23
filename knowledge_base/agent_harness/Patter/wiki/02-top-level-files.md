> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Top-Level Files
**In one sentence:** These nine root files define the repo's editor/Git conventions, ignored artifacts, local credential template, runtime pins, commit hygiene and secret scanning, AI-agent contribution contract, and vulnerability reporting policy.
## Key points
- `.editorconfig` enforces UTF-8, LF endings, final newline, space indent size 2 (4 for `*.py`, tabs for `Makefile`), with `trim_trailing_whitespace = false` for markdown (`.editorconfig:1-18`).
- `.env.example` is the local-mode credential template copied via `cp .env.example .env`, requiring one telephony carrier (Twilio active, Telnyx/Plivo commented) plus `OPENAI_API_KEY` by default (`.env.example:4-12`, `.env.example:26-27`).
- `.gitattributes` normalizes all checkins to LF (`* text=auto eol=lf`) and marks lock/minified files linguist-generated and media/font/audio extensions binary (`.gitattributes:1-8`, `.gitattributes:10-18`).
- `.gitignore` keeps secrets, runtimes, and artifacts local: `.env`/`.env.*` (except `.env.example`), `.venv/`, `call-logs/`, `.claude/`/`CLAUDE.md`, `.agents/`/`.crush/`/`.goose/`, `node_modules/`, build/coverage outputs (`.gitignore:7-9`, `.gitignore:23-30`).
- Runtime pins are Node `20` (`.nvmrc:1`) and Python `3.12` (`.python-version:1`).
- `.pre-commit-config.yaml` runs hygiene hooks (trailing-whitespace, end-of-file-fixer, check-yaml/json, large-file cap 3000KB, debug-statements, private-key detection, LF enforcement) plus gitleaks on every commit, while Python ruff is commented out pending a cleanup PR and TS lint is deferred to CI (`.pre-commit-config.yaml:31-33`, `.pre-commit-config.yaml:41-49`, `.pre-commit-config.yaml:52-55`).
- `AGENTS.md` makes feature parity (both SDKs, same PR, `snake_case` ↔ `camelCase`), `CHANGELOG.md` under `## Unreleased`, opt-in backward compatibility, real-path tests with provider-boundary-only mocks, no secrets/PII, no foreign license headers, and async-only I/O blocking requirements, validated by `scripts/pr-validate.sh` (AGENTS.md:13-26, AGENTS.md:38-41).
- `SECURITY.md` routes vulnerability reports to `security@getpatter.com` with 48h acknowledgment / 7-day assessment / 90-day fix targets, scopes in telephony/auth/credential/injection/SSRF issues, and requires coordinated disclosure (SECURITY.md:6-14, SECURITY.md:18-24, SECURITY.md:38-39).
---
## Editor And Git Conventions
`.editorconfig` (19 lines) sets the repo-wide style baseline (`.editorconfig:1-18`):
```
root = true

[*]
charset = utf-8
end_of_line = lf
insert_final_newline = true
trim_trailing_whitespace = true
indent_style = space
indent_size = 2

[*.py]
indent_size = 4

[*.{md,mdx}]
trim_trailing_whitespace = false

[Makefile]
indent_style = tab
```
`.gitattributes` (19 lines) normalizes endings and classifies generated/binary files (`.gitattributes:1-12`):
```
* text=auto eol=lf
package-lock.json linguist-generated=true
*.min.js linguist-generated=true
*.min.css linguist-generated=true
```
Binary set: `*.png`, `*.jpg`, `*.jpeg`, `*.gif`, `*.ico`, `*.woff`, `*.woff2`, `*.mp3`, `*.wav` (`.gitattributes:10-18`).
`.gitignore` (44 lines) excludes, by group:
| Group | Entries (`.gitignore:1-44`) |
|---|---|
| Python/build | `__pycache__/`, `*.py[cod]`, `*.egg-info/`, `dist/`, `build/`, `.eggs/`, `*.egg` |
| Secrets/env | `.env`, `.env.*`, `!.env.example` |
| Runtimes | `.venv/`, `venv/`, `node_modules/` |
| Data/logs | `*.db`, `*.sqlite`, `*.log`, `call-logs/` (per-call transcripts with caller PII, never commit) |
| Caches/coverage | `.pytest_cache/`, `.mypy_cache/`, `.ruff_cache/`, `.coverage`, `htmlcov/`, `coverage/`, `*.tsbuildinfo`, `*.tgz` |
| Agent/system local state | `.claude/`, `CLAUDE.md`, `.agents/`, `.crush/`, `.goose/`, `skills-lock.json`, `.DS_Store`, `settings.json`, `.worktrees/`, `docs/internal/`, legacy `sdk/` |
## Local Credential Template
`.env.example` (39 lines) is copied with `cp .env.example .env` and then filled in (`.env.example:4-5`). Carrier is required — pick one; voice defaults to OpenAI Realtime (`.env.example:7`, `.env.example:24-27`):
| Variable | Role (`.env.example:9-38`) |
|---|---|
| `TWILIO_ACCOUNT_SID` / `TWILIO_AUTH_TOKEN` / `TWILIO_PHONE_NUMBER` | Active default carrier (Twilio) |
| `TELNYX_API_KEY` / `TELNYX_CONNECTION_ID` / `TELNYX_PHONE_NUMBER` | Commented alternative (DTMF, transfer, recording) |
| `PLIVO_AUTH_ID` / `PLIVO_AUTH_TOKEN` / `PLIVO_PHONE_NUMBER` | Commented alternative (WS audio streaming, mu-law 8 kHz, V3 signature) |
| `OPENAI_API_KEY` | Default voice provider (OpenAI Realtime, all-in-one STT + LLM + TTS) |
| `DEEPGRAM_API_KEY` / `ELEVENLABS_API_KEY` | Commented pipeline-mode STT/TTS alternative |
| `ANTHROPIC_API_KEY` | Optional custom LLM for pipeline mode with `on_message` |
| `WEBHOOK_URL` | Omit to auto-tunnel via Cloudflare |
| `PORT` | Commented, default `8000` |
## Runtime Pins
Two one-line pins with no other content (`.nvmrc:1`, `.python-version:1`):
```
20
```
```
3.12
```
## Commit Hygiene And Secret Scanning
`.pre-commit-config.yaml` (70 lines) documents install/usage (`pip install pre-commit && pre-commit install`, `pre-commit run --all-files`) (`.pre-commit-config.yaml:5-8`). Active hooks:
| Repo / rev | Hook | Scope (`.pre-commit-config.yaml:41-55`) |
|---|---|---|
| `pre-commit-hooks v4.6.0` | `trailing-whitespace`, `end-of-file-fixer` | All files except `.(ogg\|onnx\|png\|jpg\|jpeg\|pdf\|ico\|lock)` |
| `pre-commit-hooks v4.6.0` | `check-yaml` / `check-json` | Excluding lockfiles / `tsconfig.*.json` (comments allowed) |
| `pre-commit-hooks v4.6.0` | `check-added-large-files --maxkb=3000` | 3MB cap, excluding `.(onnx\|ogg)` vendored assets |
| `pre-commit-hooks v4.6.0` | `debug-statements` | `^libraries/python/.*\.py$` only |
| `pre-commit-hooks v4.6.0` | `detect-private-key`, `mixed-line-ending --fix=lf` | All files |
| `gitleaks v8.18.4` | `gitleaks` | Secret scan on every commit |
Deliberately disabled: Python `ruff`/`ruff-format` (`astral-sh/ruff-pre-commit v0.6.9`) is commented out because its first run produced 132 findings including 14 fixture/side-effect-import-breaking `F401` removals, pending a dedicated cleanup PR (`.pre-commit-config.yaml:12-18`); TypeScript lint is skipped here on purpose and covered by the `typescript` job in `.github/workflows/test.yml` (`npm ci + npm run lint`) to avoid provisioning a second node install (`.pre-commit-config.yaml:26-30`). No `default_language_version` pin because CI runners are not guaranteed `python3.11` and the hooks work on any Python >= 3.8 (`.pre-commit-config.yaml:32-37`); the `.githooks/pre-push` full test run complements this file (`.pre-commit-config.yaml:39`).
## Agent Contribution Contract
`AGENTS.md` (68 lines) is the agent-readable form of `CONTRIBUTING.md`, to be read before opening a PR; Patter is open-source telephony infrastructure shipping two SDKs at full parity — Python (`pip install getpatter`, `libraries/python/`) and TypeScript (`npm install getpatter`, `libraries/typescript/`) (AGENTS.md:4-10). Non-negotiables (CI/reviewers block): feature parity in both SDKs in the same PR with `snake_case` ↔ `camelCase` mapping and matching field order/defaults/error classes; `CHANGELOG.md` entry under `## Unreleased` (`Added`/`Changed`/`Fixed`/`Deprecated`/`Removed`/`Security`); opt-in backward-compatible config; authentic tests mocking only the paid/external boundary (Python `@pytest.mark.mocked`, TS `*.mocked.test.ts`); no secrets/PII; no external license headers or `ported from` comments (naming integrated providers is fine); async-only I/O with `logging.getLogger("getpatter")` / `getLogger()`, never `print()` / bare `console.*` (AGENTS.md:13-26). Validation mirrors PR-blocking CI (Python 3.11/3.12/3.13, TypeScript 20/22, pre-commit/lint, security) (AGENTS.md:38-41):
```bash
bash scripts/pr-validate.sh          # mirrors PR-blocking CI (~3-5 min)
bash scripts/pr-validate.sh --quick  # pre-commit + lint (~30 s)
```
Layout: `libraries/python/getpatter/` (`client.py`, `models.py`, `server.py`, `telephony/`, `providers/`, `services/`), `libraries/typescript/src/` (`client.ts`, `types.ts`, `server.ts`, `stream-handler.ts`, `telephony/`), `docs/` (Mintlify site), `scripts/pr-validate.sh`; per-SDK quickstarts at `libraries/python/CLAUDE.md` and `libraries/typescript/CLAUDE.md` (AGENTS.md:45-55). Commits are Conventional (`feat:`, `fix:`, `perf:`, `docs:`, `chore:`, `refactor:`, `test:`); branch off `main`, PR against `main`, never push to `main` directly, and fill the PR template checklist honestly (AGENTS.md:59-64). No truncated files in this chunk; all nine files are shown in full.
## Security Policy
`SECURITY.md` (41 lines) directs reports to `security@getpatter.com` with description, reproduction steps, impact, and suggested fix (SECURITY.md:6-14). Response targets: acknowledgment within 48 hours, initial assessment within 7 days, fix within 90 days with critical issues prioritized (SECURITY.md:18-24). In scope: auth bypass, API key/credential exposure, SQL/command/prompt injection, SSRF/webhook issues, telephony abuse (toll fraud, caller ID spoofing), dashboard XSS; out of scope: feature requests (GitHub Issues), non-security bugs, social engineering, DoS (SECURITY.md:26-35). Coordinated disclosure: no public disclosure until a fix is released and affected users notified (SECURITY.md:38-39).
**Covers:** `.editorconfig`, `.env.example`, `.gitattributes`, `.gitignore`, `.nvmrc`, `.pre-commit-config.yaml`, `.python-version`, `AGENTS.md`, `SECURITY.md`
