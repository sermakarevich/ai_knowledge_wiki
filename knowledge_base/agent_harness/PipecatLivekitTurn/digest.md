> [[index|Wiki]] | [[summary|Summary]]

# priamjain/pipecat-livekit-turn — Digest

## 1. [[wiki/01-overview|Overview]]

**In one sentence:** This package implements LiveKit Turn Detector v1 as a Pipecat `BaseTurnAnalyzer` on top of LiveKit's cloud end-of-utterance gateway, so `LiveKitTurnAnalyzerV1` drops into any Pipecat pipeline wherever a SmartTurn analyzer would go.

## Key points

- The package fills the gap left by Pipecat's built-in analyzers (SmartTurn family, Krisp Viva) by wrapping LiveKit's end-of-utterance model as `LiveKitTurnAnalyzerV1`, a drop-in `BaseTurnAnalyzer` (README.md:12-16).
- The motivation is accuracy on the `livekit/eot-bench-data` validation set, where Turn Detector v1 outranks the best Pipecat-shipped analyzer, e.g. Hindi AUC 0.9438 vs SmartTurn v3.2's 0.7189 over an identical 952-span set (README.md:20-28).
- Installation is straight from the repository, not PyPI, and requires Python 3.10+ plus `pipecat-ai>=1.8.0` (README.md:35-54).
- Authentication uses a short-lived JWT minted from LiveKit project keys supplied via `LIVEKIT_API_KEY`/`LIVEKIT_API_SECRET` environment variables or passed directly as `api_key`/`api_secret`, and it works with any Pipecat transport since the EOT gateway is a standalone inference endpoint (README.md:58-75).
- The canonical wiring pairs a short Silero VAD `stop_secs` (0.2 s, deciding only *when to ask* the model) with `TurnAnalyzerUserTurnStopStrategy` holding `LiveKitTurnAnalyzerV1(params=LiveKitTurnParams(language="hi"))`, with a full runnable bot in `examples/bot.py` (README.md:90-108).
- Turn-end flow is VAD fires at ~0.2 s, the gateway returns `p(eot)`, and below-threshold keeps the turn open while above-threshold ends it immediately, with `LiveKitTurnParams.stop_secs` (default 3.0 s) as the hard silence fallback regardless of the model (README.md:114-122).
- Configuration is the `pydantic` model `LiveKitTurnParams` (subclass of `BaseTurnParams`) plus constructor arguments on `LiveKitTurnAnalyzerV1`, with per-language `p(eot)` thresholds exported as `CLOUD_THRESHOLDS` (README.md:126-153).

## 2. [[wiki/02-top-level-files|Top-level-files]]

**In one sentence:** The top-level-files component captured in this chunk consists solely of the repository's `.gitignore`, which excludes Python bytecode, packaging, virtual-environment, secret, cache, and OS artifacts from version control.

## Key points

- The chunk grounds exactly one top-level file, `.gitignore`, and no source, packaging, example, or test files appear in it (`.gitignore:1-11`).
- It excludes Python bytecode artifacts via `__pycache__/` (`.gitignore:1`) and `*.py[cod]` (`.gitignore:2`), keeping compiled output out of the repo.
- It excludes Python packaging outputs via `*.egg-info/` (`.gitignore:3`), `build/` (`.gitignore:4`), and `dist/` (`.gitignore:5`).
- It excludes local virtual environments via both `.venv/` (`.gitignore:6`) and `venv/` (`.gitignore:7`).
- It excludes local secrets and configuration via `.env` (`.gitignore:8`), so environment-provided credentials are never committed.
- It excludes tool caches (`.pytest_cache/` at `.gitignore:9`, `.ruff_cache/` at `.gitignore:10`) and the macOS `.DS_Store` file (`.gitignore:11`).

## The system in five moves

1. Pipecat lacks a LiveKit end-of-utterance analyzer, so this package wraps Turn Detector v1 as the drop-in `LiveKitTurnAnalyzerV1`.
2. The payoff is benchmark accuracy, notably on non-English languages such as Hindi on `livekit/eot-bench-data`.
3. Setup is a repo install plus LiveKit project keys, working with any Pipecat transport via the standalone cloud gateway.
4. At runtime Silero VAD decides when to ask, the gateway scores `p(eot)` against per-language thresholds, and `stop_secs` forces the turn end as fallback.
5. The repo hygiene is minimal — the top level captured here is only a `.gitignore` keeping bytecode, packaging, venvs, secrets, and caches out of version control.
