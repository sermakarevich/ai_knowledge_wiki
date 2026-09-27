> [[index|Wiki]] | [[summary|Summary]]
# stimm-ai/stimm — Digest
## 1. [[wiki/01-overview|Overview]]
**In one sentence:** Stimm is an Optimistic VUI runtime built on livekit-agents where one agent talks fast and one agent thinks deep, collaborating in real time.
## Key points
- Stimm is an Optimistic VUI runtime built on `livekit-agents` that brings optimistic-UI thinking to voice: acknowledge early, speak early, keep reasoning in parallel (README.md:36-38).
- The conversational loop is a low-latency `VAD -> STT -> fast LLM -> TTS` pipeline with pre-TTS buffering before speech output (README.md:46, README.md:79-84).
- The runtime uses a dual-agent architecture: `VoiceAgent` owns the live turn while `Supervisor` watches the transcript, reasons asynchronously, and steers without blocking the first response (README.md:94-96, README.md:192-198).
- Agents exchange typed protocol messages (`StimmProtocol`) over LiveKit data channels, with a typed protocol for Python and TypeScript supervisors (README.md:48, README.md:197-198).
- Runtime behavior is controlled by mode (`autonomous` / `relay` / `hybrid` default) and pre-TTS buffering level (`NONE` / `LOW` / `MEDIUM` default / `HIGH`) (README.md:207-217).
- Onboarding is wizard-first: the catalog API displays providers and parameters, then extras are derived from the user selection and installed as `stimm[...]` extras, never vendored in the wheel (README.md:50, README.md:114-115, README.md:174-184).
- The local dev contract is `pip install -e ".[dev]"`, `docker compose up -d`, `bash scripts/dev_build.sh`, then `pytest` / `ruff` plus catalog/contract checks (README.md:222-244).
## 2. [[wiki/02-top-level-files|Top-level-files]]
**In one sentence:** The repo root defines the AI-agent integration contract, the lint/security/typecheck hooks, the ignored build artifacts, and the release-please versioning for the Python and TypeScript packages.
## Key points
- `AGENT.md` is the implementation contract for app/extension integration with `stimm`, covering the dual-agent runtime and provider onboarding wizard alignment (AGENT.md:1-4).
- Integration must use `get_provider_catalog()` for wizard discovery UI and must not build discovery UI from `list_runtime_providers()` (AGENT.md:14-15).
- Install commands are derived via `required_extras_for_selection(...)` or `extras_install_command(...)`, installed in the same environment that runs the app, followed by a Python process restart (AGENT.md:16-19).
- App config must never store provider module paths/constructors and never expose secrets in logs, telemetry, or UI snapshots (AGENT.md:20-21).
- Pre-commit runs `ruff format`, `ruff check --fix`, `bandit -r src/`, and `pip-audit` for Python plus `npm run check` in `packages/protocol-ts` for TypeScript changes (.pre-commit-config.yaml:5-9, .pre-commit-config.yaml:10-14, .pre-commit-config.yaml:15-20, .pre-commit-config.yaml:22-27, .pre-commit-config.yaml:32-40).
- Release state is pinned in `.release-please-manifest.json` at `.`: `0.1.13` and `packages/protocol-ts`: `0.1.3`, with `release-please-config.json` linking the two packages for joint versioning (.release-please-manifest.json:2-3, release-please-config.json:19-21).
- `.gitignore` excludes env/venv (`.env`, `.venv/`, `venv/`, `.stimm-build-venv/`), Python build outputs, Node/website build outputs, caches, logs, and the root-owned v1 leftover `bin/` (.gitignore:1-5, .gitignore:7-19, .gitignore:21-26, .gitignore:37-43, .gitignore:45-47).
## The system in five moves
1. Stimm starts from Optimistic VUI: acknowledge immediately and speak early instead of blocking on the full reasoning chain.
2. The fast path is a low-latency VAD -> STT -> fast LLM -> buffered TTS loop with tunable pre-TTS buffering and hybrid/autonomous/relay modes.
3. A dual-agent split keeps VoiceAgent on the live turn while the Supervisor reasons, plans, and steers asynchronously over typed StimmProtocol messages on LiveKit data channels.
4. Provider onboarding stays wizard-first: discover via the catalog API, install only the selected stimm[...] extras, then restart before instantiating plugins.
5. App integrators follow the AGENT.md contract — public APIs only, no stored module paths or leaked secrets.
6. Repo hygiene backs it all: pre-commit lint/security/typecheck hooks, git-ignored build artifacts, and linked release-please versioning for the Python and TypeScript packages.
