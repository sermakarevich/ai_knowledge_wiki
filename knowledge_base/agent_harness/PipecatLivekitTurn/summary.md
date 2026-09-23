# Technical Analysis: priamjain/pipecat-livekit-turn

**Repository:** https://github.com/priamjain/pipecat-livekit-turn
**Version analyzed:** unknown
**Date:** 2026-09-22
**Wiki:** [[index]]

## 1. Overview / What Problem It Solves

Voice agents must decide when a user has finished speaking versus merely pausing. Fixed-silence VAD thresholds either cut in too early (mid-thought pauses in non-English speech) or add dead air. Pipecat's shipped analyzers (SmartTurn family, Krisp Viva) underperform outside English: on `livekit/eot-bench-data` Hindi validation (952 spans) SmartTurn v3.2 scores AUC 0.7189 / AP 0.5608 against LiveKit Turn Detector v1 at AUC 0.9438 / AP 0.9149 (README.md:20-28).

This repo wraps LiveKit's hosted end-of-utterance gateway as `LiveKitTurnAnalyzerV1`, a drop-in Pipecat `BaseTurnAnalyzer` usable wherever a SmartTurn analyzer would go (README.md:12-16). It separates two concerns: Silero VAD with short `stop_secs` (0.2 s) decides *when to ask* the model, and the analyzer decides *whether the turn ends*, with `LiveKitTurnParams.stop_secs` (3.0 s) as silence fallback (README.md:112-122). Audio streams continuously via `append_audio` so each decision costs one inference round trip, and failures degrade to plain VAD by returning `COMPLETE` (README.md:163-172). Primary user: a Pipecat pipeline builder adding multilingual turn-taking without changing transport (WebRTC, Daily, Twilio all work since the EOT gateway is standalone) (README.md:72-75).

## 2. High-Level Architecture

```
Mic / Transport ─► SileroVAD (stop_secs=0.2) ─► LLMUserAggregator ─► LiveKitTurnAnalyzerV1 ─► TurnAnalyzerUserTurnStopStrategy ─► Pipeline
                         │                                │                              │ ▼
                         │                                │                     append_audio ─► LiveKit Cloud EOT gateway (wss, JWT)
                         │                                │                              │ ▼
                         │                                │                     p(eot) vs CLOUD_THRESHOLDS ─► COMPLETE / INCOMPLETE + TurnMetricsData
                         │                                ▼
                         └───────────────── stop_secs=3.0 fallback ─► force COMPLETE on sustained silence
```

Data flow:

1. Transport delivers PCM frames to `LLMUserAggregatorPair`; Silero VAD with `stop_secs=0.2` emits a candidate stop shortly after speech energy drops (README.md:97-115). This trigger only schedules a model query.
2. Buffered audio has already been forwarded chunk-by-chunk through `append_audio` to the LiveKit EOT websocket session, so no bulk upload occurs at decision time (README.md:163-167).
3. `analyze_end_of_turn` awaits one gateway prediction `p(eot)` bounded by `inference_timeout_secs` (2.0 s); `TurnMetricsData.e2e_processing_time_ms` records the round trip when `PipelineParams(enable_metrics=True)` (README.md:135-144, README.md:177-179).
4. The probability is compared against the per-language entry in `CLOUD_THRESHOLDS` (or explicit `threshold` override); above threshold ends the turn immediately, below keeps it open (README.md:120-122, README.md:147-159).
5. If the websocket is down or inference times out, the analyzer logs a warning and returns `COMPLETE`, equivalent to VAD-only behavior; `_ensure_connected` re-establishes the session on the next audio chunk (README.md:169-175).
6. If silence reaches `LiveKitTurnParams.stop_secs` (default 3.0 s), the turn ends regardless of model output (README.md:116-118).

Persistent state lives in two places: (a) the gateway websocket session, which accumulates streamed audio context across `append_audio` calls and is *not* flushed by `clear()` (README.md:183-189); (b) analyzer-side configuration (`LiveKitTurnParams`, credentials, `sample_rate`) held on `LiveKitTurnAnalyzerV1` for the pipeline lifetime (README.md:126-146).

## 3. Turn Analyzer: LiveKitTurnAnalyzerV1 and LiveKitTurnParams

Representation: a stateful `BaseTurnAnalyzer` subclass plus a `pydantic` params model subclassing `BaseTurnParams` (README.md:126). The analyzer holds connection state (websocket session, JWT, sample rate) and exposes the Pipecat turn-analyzer interface (`append_audio`, `analyze_end_of_turn`, `clear`); the params object holds decision policy (language/threshold, timeouts).

Named kinds/types with grounding:

- `LiveKitTurnAnalyzerV1` — analyzer class, drop-in `BaseTurnAnalyzer` over the cloud EOT gateway (README.md:12-16); constructor args `params`, `sample_rate`, `api_key`, `api_secret`, `base_url` (README.md:135-146).
- `LiveKitTurnParams(BaseTurnParams)` — configuration model with fields `language` (default `"en"`), `threshold` (default `None`, overrides language default), `stop_secs` (default `3.0`), `inference_timeout_secs` (default `2.0`) (README.md:126-136).
- `CLOUD_THRESHOLDS` — exported per-language `p(eot)` threshold map copied from `livekit.agents.inference.eot.languages.CLOUD_LANGUAGES` (README.md:147-149); entries `ar` 0.355, `de` 0.495, `en` 0.560, `es` 0.590, `fr` 0.575, `hi` 0.575, `id` 0.470, `it` 0.640, `ja` 0.370, `ko` 0.695, `nl` 0.750, `pt` 0.665, `tr` 0.650, `zh` 0.590 (README.md:151-153); unknown language falls back to English, region subtags stripped (`"en-US"` → `"en"`) (README.md:155-156).
- `TurnAnalyzerUserTurnStopStrategy` / `UserTurnStrategies(stop=[...])` — Pipecat wiring that binds the analyzer into `LLMUserAggregatorParams` (README.md:97-110).
- `TurnMetricsData(is_complete, probability, e2e_processing_time_ms)` — per-prediction metric struct (README.md:177-179).
- `BaseSmartTurn` — Pipecat reference behavior for `clear()` (flushes local buffer), contrasted with this analyzer where audio lives server-side (README.md:183-189).

Key queries (verbatim from wiki, README.md:12-16):

> Pipecat ships turn analyzers for the SmartTurn family and Krisp Viva, but none
> for LiveKit's end-of-utterance model. This package fills that gap: it
> implements `BaseTurnAnalyzer` on top of LiveKit's cloud EOT gateway, so
> `LiveKitTurnAnalyzerV1` drops into any Pipecat pipeline wherever a SmartTurn
> analyzer would go.

## 4. LLM / External Service Integration

Provider: LiveKit Cloud end-of-utterance gateway serving the hosted `turn-detector-v1` audio checkpoint (README.md:163-167, README.md:190-191). No LLM chat/STT/TTS call originates in this repo; the only network dependency is the EOT inference websocket.

- Required call: streaming inference — `append_audio` forwards each buffer as it arrives; `analyze_end_of_turn` resolves one prediction round trip per VAD trigger, yielding `p(eot)` compared against `CLOUD_THRESHOLDS` (README.md:120-122, README.md:163-167). Authentication is a short-lived JWT minted from project keys (README.md:58-64).
- Optional calls: none. Reconnect via `_ensure_connected` is internal session management, not a separate service (README.md:174-175).
- Failure semantics: connection failure or `inference_timeout_secs` expiry returns `COMPLETE` with a warning, degrading to VAD (README.md:169-172).

| Env var | Required | Purpose |
|---|---|---|
| `LIVEKIT_API_KEY` | yes, unless `api_key` passed directly | LiveKit project key for JWT minting (README.md:58-70) |
| `LIVEKIT_API_SECRET` | yes, unless `api_secret` passed directly | LiveKit project secret for JWT minting (README.md:58-70) |
| `LIVEKIT_INFERENCE_URL` | no (defaults to hosted gateway) | Override gateway `base_url` (README.md:139-146) |

Constructor equivalents: `LiveKitTurnAnalyzerV1(api_key=..., api_secret=..., base_url=...)` override the three variables above (README.md:66-70, README.md:139-146). Keys are obtained from the LiveKit Cloud dashboard; transport need not be LiveKit (README.md:72-75).

## 5. End-of-Turn Decision Pipeline

Canonical wiring pairs `SileroVADAnalyzer(stop_secs=0.2)` with `TurnAnalyzerUserTurnStopStrategy(turn_analyzer=LiveKitTurnAnalyzerV1(params=LiveKitTurnParams(language="hi")))` inside `LLMContextAggregatorPair`, with a runnable reference in `examples/bot.py` (README.md:90-115).

1. `append_audio(buffer)` — forward each incoming audio chunk to the gateway session as it arrives, amortizing upload so decision time is one RTT (README.md:163-167).
2. VAD trigger — Silero `stop_secs=0.2` fires a candidate stop; this only schedules a model query, not a turn end (README.md:114-115).
3. `analyze_end_of_turn()` — request `p(eot)` from the gateway, bounded by `LiveKitTurnParams.inference_timeout_secs` (2.0 s); emit `TurnMetricsData(is_complete, probability, e2e_processing_time_ms)` when metrics are enabled (README.md:135-136, README.md:177-179).
4. Threshold compare — resolve effective threshold from explicit `threshold` or `CLOUD_THRESHOLDS[language]` (region-stripped, English fallback); `p(eot)` below threshold keeps the turn open, above ends it immediately (README.md:120-122, README.md:130-134, README.md:155-159).
5. `clear()` — Pipecat turn-reset hook; contrasted with `BaseSmartTurn.clear()` it does *not* currently flush gateway-side session audio, leaving prior-turn audio in the context window (README.md:183-189).
6. `_ensure_connected()` — on next audio chunk after a drop, restart the websocket session automatically (README.md:174-175); any hard failure in steps 3–4 returns `COMPLETE` as VAD fallback (README.md:169-172).

## 6. Key Files

Wiki component coverage grounds three repo paths directly; remaining rows are framework touchpoints named in the wiring excerpt, marked External.

| File | Lines | What It Does |
|---|---|---|
| `README.md` | 1–206 (chunk) | Sole design/usage spec: gap statement, benchmark table, install, credentials, wiring, VAD split, params/thresholds, behavior, limitations, dev, license (01-overview.md:9-187) |
| `examples/bot.py` | referenced at README.md:108 | Full runnable bot wiring VAD + analyzer + stop strategy (01-overview.md:115) |
| `.gitignore` | 1–11 | Excludes `__pycache__/`, `*.py[cod]`, `*.egg-info/`, `build/`, `dist/`, `.venv/`, `venv/`, `.env`, `.pytest_cache/`, `.ruff_cache/`, `.DS_Store` (02-top-level-files.md:5-11) |
| `pipecat_livekit_turn` package (External ref) | via README.md:87 | Import root exporting `LiveKitTurnAnalyzerV1`, `LiveKitTurnParams` (README.md:86-87) |
| Analyzer module e.g. `turn_analyzer.py` (External ref) | via README.md:135-144 | Implements `LiveKitTurnAnalyzerV1`: `append_audio`, `analyze_end_of_turn`, `clear`, `_ensure_connected` (README.md:163-175) |
| Params model (External ref) | via README.md:126-136 | `LiveKitTurnParams(BaseTurnParams)`: `language`, `threshold`, `stop_secs`, `inference_timeout_secs` (README.md:128-136) |
| Threshold table (External ref) | via README.md:147-153 | `CLOUD_THRESHOLDS` per-language map copied from `livekit.agents.inference.eot.languages.CLOUD_LANGUAGES` (README.md:147-153) |
| `pipecat.audio.vad.silero.SileroVADAnalyzer` (External) | via README.md:88-101 | VAD trigger with `VADParams(stop_secs=0.2)`; decides when to ask the model (README.md:97-115) |
| `pipecat.processors.aggregators.llm_response_universal.LLMContextAggregatorPair` (External) | via README.md:90-97 | Hosts user/assistant aggregation; `LLMUserAggregatorParams` carries VAD + strategies (README.md:97-112) |
| `pipecat.turns.user_stop.TurnAnalyzerUserTurnStopStrategy` (External) | via README.md:94-104 | Stop strategy binding `turn_analyzer` into `UserTurnStrategies(stop=[...])` (README.md:103-110) |

Note: wiki chunks attest only `README.md`, `examples/bot.py`, and `.gitignore` by path; manifest (`pyproject.toml`), package module paths, and test files are not grounded in the provided wiki pages.

## 7. Dependencies

| Package | Version constraint | Purpose |
|---|---|---|
| `pipecat-ai` | `>=1.8.0` | Required. Provides `BaseTurnAnalyzer`/`BaseTurnParams`, aggregators, VAD and stop-strategy interfaces (README.md:54) |
| Python | `>=3.10` | Required runtime floor (README.md:54) |
| `pydantic` | transitive via Pipecat (no direct constraint stated) | Required. Base of `LiveKitTurnParams`/`BaseTurnParams` config model (README.md:126) |
| `livekit.agents` (`inference.eot.languages.CLOUD_LANGUAGES`) | reference copy, no version pinned in wiki | Required at build time. Source from which `CLOUD_THRESHOLDS` values were copied (README.md:147-149) |
| `silero-vad` (via `pipecat.audio.vad.silero`) | transitive via Pipecat (no direct constraint stated) | Required in canonical wiring. Short-window VAD trigger (`stop_secs=0.2`) (README.md:88-115) |
| `pytest` (+ dev extra `.[dev]`) | no constraint stated | Development/test only: `pip install -e ".[dev]"` then `pytest` (README.md:172-179) |
| `ruff` | no constraint stated (cache entry only) | Development lint cache (`.ruff_cache/` ignored) (02-top-level-files.md:10) |

Install is from git, not PyPI: `pip install git+https://github.com/priamjain/pipecat-livekit-turn`, pin with `@<commit-sha>`, or `pip install -e ./pipecat-livekit-turn` for local edit (README.md:35-52).

## 8. CLI / Usage Surface

No CLI. The surface is a library plus one example bot and environment/config inputs.

Entry points:

| Entry | Form | Effect |
|---|---|---|
| `from pipecat_livekit_turn import LiveKitTurnAnalyzerV1, LiveKitTurnParams` | Python import | Analyzer + params for pipeline wiring (README.md:86-87) |
| `examples/bot.py` | `python examples/bot.py` (with creds set) | Full runnable voice bot demonstrating VAD + analyzer wiring (README.md:108) |
| `pip install git+https://github.com/priamjain/pipecat-livekit-turn` | shell | Install latest from repo (README.md:35-36) |
| `pip install "git+https://github.com/priamjain/pipecat-livekit-turn@<commit-sha>"` | shell | Pinned reproducible install (README.md:41-45) |
| `pip install -e ".[dev]" && pytest` | shell | Dev checkout test loop (README.md:172-179) |

Environment variables:

| Variable | Default | Meaning |
|---|---|---|
| `LIVEKIT_API_KEY` | none (or `api_key` arg) | Project key for gateway JWT (README.md:58-70) |
| `LIVEKIT_API_SECRET` | none (or `api_secret` arg) | Project secret for gateway JWT (README.md:58-70) |
| `LIVEKIT_INFERENCE_URL` | hosted gateway (or `base_url` arg) | Gateway URL override (README.md:139-146) |

Configuration (`LiveKitTurnParams` + constructor):

| Key | Default | Meaning |
|---|---|---|
| `language` | `"en"` | Selects per-language `p(eot)` threshold; subtags stripped, unknown → English (README.md:130-134, README.md:155-156) |
| `threshold` | `None` | Explicit `p(eot)` cutoff overriding language default; lower = snappier, higher = more patient (README.md:130-134, README.md:158-159) |
| `stop_secs` | `3.0` | Hard silence fallback ending turn regardless of model (README.md:130-134, README.md:116-118) |
| `inference_timeout_secs` | `2.0` | Max wait for prediction before VAD fallback (README.md:130-136) |
| `sample_rate` | `None` (from transport) | Fixed audio rate override on `LiveKitTurnAnalyzerV1` (README.md:139-142) |

## 9. Extensibility Points

- New language threshold: extend/override the `CLOUD_THRESHOLDS` map (values copied from `livekit.agents.inference.eot.languages.CLOUD_LANGUAGES`) or pass explicit `threshold` in `LiveKitTurnParams` rather than forking the table (README.md:130-153).
- Snappiness vs. patience tuning: adjust `threshold` down (interrupt sooner) or up (wait longer) on `LiveKitTurnParams` without touching analyzer code (README.md:158-159).
- Silence policy: change `stop_secs` on `LiveKitTurnParams` for the hard fallback, and keep Silero `VADParams(stop_secs)` short (0.2 s) so VAD remains a trigger, not a decider (README.md:114-118).
- Credentials/endpoint: subclass or wrap `LiveKitTurnAnalyzerV1` constructor (`api_key`, `api_secret`, `base_url`) to inject per-tenant keys or a self-hosted-compatible gateway URL (README.md:66-70, README.md:139-146).
- Transport swap: reuse the same analyzer under any Pipecat transport (WebRTC, Daily, Twilio) since inference is a standalone endpoint; only `sample_rate` may need fixing (README.md:72-75, README.md:139-142).
- Session-flush fix: implement gateway `session_flush` signaling inside the analyzer's `clear()` path (currently missing) following LiveKit's reference agent protocol (README.md:183-189).
- Observability: enable `PipelineParams(enable_metrics=True)` and consume `TurnMetricsData(is_complete, probability, e2e_processing_time_ms)` for threshold calibration (README.md:177-179).

## 10. Limitations and Gotchas

- **Turn-boundary context leaks across turns.** `clear()` does not send the protocol's `session_flush` to the gateway, so the next prediction can see previous-turn audio; Pipecat's `BaseSmartTurn` flushes locally but this analyzer's buffer is server-side (README.md:183-189).
- **VAD `stop_secs` and analyzer `stop_secs` are routinely confused.** Silero 0.2 s only schedules the query; `LiveKitTurnParams.stop_secs` (3.0 s) is the actual silence cutoff — setting VAD long adds latency to every model decision (README.md:114-118).
- **Cloud-only, audio v1 only.** No local/ONNX path and neither the text-based nor `-mini` EOT variants are wrapped, so offline or text-feature deployments are out of scope (README.md:190-192).
- **Failure mode is silent patience loss.** Any websocket drop or `inference_timeout_secs` (2.0 s) expiry returns `COMPLETE`, i.e. the system silently becomes plain VAD; transient cloud issues manifest as premature cut-ins, not errors (README.md:169-172).
- **Per-decision cloud RTT on every VAD trigger.** Streaming avoids bulk upload but each prediction still costs roughly one LiveKit Cloud round trip; regions far from the gateway pay it on every pause (README.md:163-167).
- **Thresholds are static copies.** `CLOUD_THRESHOLDS` was copied from `livekit.agents` and can drift from upstream; unrecognized languages silently use the English 0.560 cutoff (README.md:147-156).

## 11. How It Compares to Alternatives

- **Pipecat SmartTurn family (v2/v3.2):** shipped analyzers with local/server options; cited Hindi AUC 0.7189 vs. 0.9438 here, so SmartTurn is the zero-extra-credential default while this repo trades a cloud dependency for multilingual accuracy (README.md:12-16, README.md:20-28).
- **Pipecat Krisp Viva analyzer:** the other Pipecat-shipped option named in the gap statement; same drop-in `BaseTurnAnalyzer` slot, different vendor model, without this repo's per-language LiveKit threshold table (README.md:12-16, README.md:147-153).
- **`livekit.agents` Turn Detector v1 (reference):** upstream LiveKit implementation including the `session_flush` protocol this wrapper lacks; using it directly avoids Pipecat but loses Pipecat pipeline/transport portability (README.md:147-149, README.md:183-189).
- **Plain Silero VAD (`stop_secs`-only turn-taking):** no model call, no credentials, lowest latency variance; fails on mid-utterance pauses that the gateway's `p(eot)` + 3.0 s fallback handles, which is why the canonical wiring keeps both (README.md:112-122).

Positioning: use this package when a Pipecat pipeline must keep its transport and VAD but buy LiveKit's multilingual end-of-utterance accuracy as a hosted dependency; stay with SmartTurn/Viva or raw VAD when offline operation, minimal dependencies, or English-only traffic dominate.

## Appendix: Selected Code Snippets

1. Canonical wiring, `README.md:86-112`:

```python
from pipecat_livekit_turn import LiveKitTurnAnalyzerV1, LiveKitTurnParams
from pipecat.audio.vad.silero import SileroVADAnalyzer
from pipecat.audio.vad.vad_analyzer import VADParams
from pipecat.processors.aggregators.llm_response_universal import (
    LLMContextAggregatorPair,
    LLMUserAggregatorParams,
)
from pipecat.turns.user_stop import TurnAnalyzerUserTurnStopStrategy
from pipecat.turns.user_turn_strategies import UserTurnStrategies

user_aggregator, assistant_aggregator = LLMContextAggregatorPair(
    context=context,
    user_params=LLMUserAggregatorParams(
        # Keep VAD's stop_secs short — it only decides *when to ask* the model.
        vad_analyzer=SileroVADAnalyzer(params=VADParams(stop_secs=0.2)),
        user_turn_strategies=UserTurnStrategies(
            stop=[
                TurnAnalyzerUserTurnStopStrategy(
                    turn_analyzer=LiveKitTurnAnalyzerV1(
                        params=LiveKitTurnParams(language="hi")
                    )
                )
            ]
        ),
    ),
)
```

2. Credentials, `README.md:58-70`:

```bash
export LIVEKIT_API_KEY=APIxxxxxxxx
export LIVEKIT_API_SECRET=xxxxxxxxxxxx
```

```python
LiveKitTurnAnalyzerV1(api_key="APIxxxxxxxx", api_secret="...")
```

3. Install variants, `README.md:35-52`:

```bash
pip install git+https://github.com/priamjain/pipecat-livekit-turn
pip install "git+https://github.com/priamjain/pipecat-livekit-turn@<commit-sha>"
git clone https://github.com/priamjain/pipecat-livekit-turn
pip install -e ./pipecat-livekit-turn
```

4. Repository ignore policy, `.gitignore:1-11`:

```
__pycache__/
*.py[cod]
*.egg-info/
build/
dist/
.venv/
venv/
.env
.pytest_cache/
.ruff_cache/
.DS_Store
```
