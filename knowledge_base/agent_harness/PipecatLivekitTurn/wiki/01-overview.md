> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Overview

**In one sentence:** This package implements LiveKit Turn Detector v1 as a Pipecat `BaseTurnAnalyzer` on top of LiveKit's cloud end-of-utterance gateway, so `LiveKitTurnAnalyzerV1` drops into any Pipecat pipeline wherever a SmartTurn analyzer would go.

## Key points

- The package fills the gap left by Pipecat's built-in analyzers (SmartTurn family, Krisp Viva) by wrapping LiveKit's end-of-utterance model as `LiveKitTurnAnalyzerV1`, a drop-in `BaseTurnAnalyzer` (README.md:12-16).
- The motivation is accuracy on the `livekit/eot-bench-data` validation set, where Turn Detector v1 outranks the best Pipecat-shipped analyzer, e.g. Hindi AUC 0.9438 vs SmartTurn v3.2's 0.7189 over an identical 952-span set (README.md:20-28).
- Installation is straight from the repository, not PyPI, and requires Python 3.10+ plus `pipecat-ai>=1.8.0` (README.md:35-54).
- Authentication uses a short-lived JWT minted from LiveKit project keys supplied via `LIVEKIT_API_KEY`/`LIVEKIT_API_SECRET` environment variables or passed directly as `api_key`/`api_secret`, and it works with any Pipecat transport since the EOT gateway is a standalone inference endpoint (README.md:58-75).
- The canonical wiring pairs a short Silero VAD `stop_secs` (0.2 s, deciding only *when to ask* the model) with `TurnAnalyzerUserTurnStopStrategy` holding `LiveKitTurnAnalyzerV1(params=LiveKitTurnParams(language="hi"))`, with a full runnable bot in `examples/bot.py` (README.md:90-108).
- Turn-end flow is VAD fires at ~0.2 s, the gateway returns `p(eot)`, and below-threshold keeps the turn open while above-threshold ends it immediately, with `LiveKitTurnParams.stop_secs` (default 3.0 s) as the hard silence fallback regardless of the model (README.md:114-122).
- Configuration is the `pydantic` model `LiveKitTurnParams` (subclass of `BaseTurnParams`) plus constructor arguments on `LiveKitTurnAnalyzerV1`, with per-language `p(eot)` thresholds exported as `CLOUD_THRESHOLDS` (README.md:126-153).

---

## Purpose and fit

[LiveKit Turn Detector v1](https://docs.livekit.io/agents/build/turns/turn-detector/) as a Pipecat turn analyzer (README.md:9-10).

Verbatim (README.md:12-16):

> Pipecat ships turn analyzers for the SmartTurn family and Krisp Viva, but none
> for LiveKit's end-of-utterance model. This package fills that gap: it
> implements `BaseTurnAnalyzer` on top of LiveKit's cloud EOT gateway, so
> `LiveKitTurnAnalyzerV1` drops into any Pipecat pipeline wherever a SmartTurn
> analyzer would go.

### Why: benchmark claim

On the [`livekit/eot-bench-data`](https://huggingface.co/datasets/livekit/eot-bench-data) validation set, Turn Detector v1 outranks the best analyzer Pipecat ships today — dramatically so outside English (README.md:20-23). Hindi, over an identical 952-span set (README.md:22-23):

| model | AUC | AP |
|---|---|---|
| LiveKit Turn Detector v1 | **0.9438** | **0.9149** |
| SmartTurn v3.2 | 0.7189 | 0.5608 |

If the agent speaks anything other than English, this is usually the more accurate choice (README.md:30-31).

## Install

Not on PyPI — install straight from the repository (README.md:35-36):

```bash
pip install git+https://github.com/priamjain/pipecat-livekit-turn
```

Pin a commit for reproducible builds (README.md:41-45):

```bash
pip install "git+https://github.com/priamjain/pipecat-livekit-turn@<commit-sha>"
```

For a local checkout intended for editing (README.md:47-52):

```bash
git clone https://github.com/priamjain/pipecat-livekit-turn
pip install -e ./pipecat-livekit-turn
```

Requires Python 3.10+ and `pipecat-ai>=1.8.0` (README.md:54).

## Credentials

The analyzer authenticates to LiveKit Cloud with a short-lived JWT minted from project keys, set in the environment (README.md:58-64):

```bash
export LIVEKIT_API_KEY=APIxxxxxxxx
export LIVEKIT_API_SECRET=xxxxxxxxxxxx
```

Or passed directly (README.md:66-70):

```python
LiveKitTurnAnalyzerV1(api_key="APIxxxxxxxx", api_secret="...")
```

Get keys from the [LiveKit Cloud dashboard](https://cloud.livekit.io/) (README.md:72). LiveKit need not be the transport — the EOT gateway is a standalone inference endpoint, so this works with a WebRTC, Daily, Twilio, or any other Pipecat transport (README.md:72-75).

## Usage

Verbatim wiring (README.md:79-106):

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

A full runnable bot is in [`examples/bot.py`](examples/bot.py) (README.md:108).

### How it fits with VAD

Both a VAD and this analyzer are involved, and they do different jobs (README.md:112):

- **Silero VAD's `stop_secs`** decides *when the model gets asked*. Keep it short (0.2 s is a good default). It is not the turn-end decision (README.md:114-115).
- **`LiveKitTurnParams.stop_secs`** is the hard fallback. If the user has been silent this long, the turn ends regardless of what the model says. Default 3.0 s (README.md:116-118).

So a pause produces: VAD fires at 0.2 s → gateway returns `p(eot)` → below threshold means the turn stays open and the agent keeps waiting; above it, the turn ends immediately (README.md:120-122).

## Configuration

`LiveKitTurnParams` (a `pydantic` model, subclass of `BaseTurnParams`) (README.md:126):

| field | default | meaning |
|---|---|---|
| `language` | `"en"` | Picks the per-language `p(eot)` threshold. |
| `threshold` | `None` | Explicit threshold; overrides the language default. |
| `stop_secs` | `3.0` | Silence after which the turn ends regardless of the model. |
| `inference_timeout_secs` | `2.0` | Wait for a prediction before falling back. |

Constructor arguments on `LiveKitTurnAnalyzerV1` (README.md:135-144):

| argument | default | meaning |
|---|---|---|
| `params` | `LiveKitTurnParams()` | Configuration above. |
| `sample_rate` | `None` | Fixed sample rate; otherwise taken from the transport. |
| `api_key` | `$LIVEKIT_API_KEY` | LiveKit project key. |
| `api_secret` | `$LIVEKIT_API_SECRET` | LiveKit project secret. |
| `base_url` | `$LIVEKIT_INFERENCE_URL` | Gateway URL. |

### Thresholds

`p(eot)` thresholds are language-specific and are exported as `CLOUD_THRESHOLDS`, copied from `livekit.agents.inference.eot.languages.CLOUD_LANGUAGES` (README.md:147-149):

`ar` 0.355 · `de` 0.495 · `en` 0.560 · `es` 0.590 · `fr` 0.575 · `hi` 0.575 · `id` 0.470 · `it` 0.640 · `ja` 0.370 · `ko` 0.695 · `nl` 0.750 · `pt` 0.665 · `tr` 0.650 · `zh` 0.590 (README.md:151-153).

An unrecognized language falls back to the English threshold; region subtags are stripped, so `"en-US"` resolves to `"en"` (README.md:155-156).

Lower the threshold to end turns sooner (snappier, more interruptions of a still-thinking user); raise it to wait longer (more patient, higher latency) (README.md:158-159).

## Behavior notes

- **Audio streams continuously.** Every `append_audio` call forwards the buffer to the gateway as it arrives, so an end-of-turn decision costs one inference round trip rather than an audio upload; expect roughly one RTT to LiveKit Cloud per prediction and `TurnMetricsData.e2e_processing_time_ms` reports the measured value (README.md:163-167).
- **Failures degrade to VAD.** If the websocket is down, the connection fails, or inference exceeds `inference_timeout_secs`, `analyze_end_of_turn` logs a warning and returns `COMPLETE`, so a broken detector behaves like plain VAD instead of stranding the user in a turn that never ends (README.md:169-172).
- **Reconnects are automatic.** `_ensure_connected` restarts the session on the next audio chunk after a drop (README.md:174-175).
- **Metrics.** Each prediction returns `TurnMetricsData` with `is_complete`, `probability`, and `e2e_processing_time_ms`; enable with `PipelineParams(enable_metrics=True)` (README.md:177-179).

## Known limitations

- **Turn-boundary session state is not flushed.** Pipecat's `BaseSmartTurn` clears its local audio buffer when a turn completes, but here the audio lives in the gateway's websocket session and `clear()` does not currently tell the gateway to drop it — so a prediction may see audio from the previous turn in its context window; the protocol has a `session_flush` message that is the likely fix, unverified against LiveKit's reference agent and tracked as an open issue (README.md:183-189).
- **Cloud only.** This wraps the hosted `turn-detector-v1` checkpoint; there is no local/ONNX path here (README.md:190-191).
- **v1 audio model only.** The text-based and `-mini` variants are not wrapped (README.md:192).

## Development

```bash
git clone https://github.com/priamjain/pipecat-livekit-turn
cd pipecat-livekit-turn
pip install -e ".[dev]"
pytest
```

(README.md:196-201.)

## License

BSD 2-Clause. Portions adapted from [Pipecat](https://github.com/pipecat-ai/pipecat) (Copyright 2024-2026, Daily), under the same license (README.md:205-206).

No truncated files were noted in the chunk; all claims above are grounded in the chunk's README excerpt.

**Covers:** `README.md`, `examples/bot.py` (referenced runnable bot)
