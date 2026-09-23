# priamjain/pipecat-livekit-turn
PDF location: https://github.com/priamjain/pipecat-livekit-turn
Source: https://github.com/priamjain/pipecat-livekit-turn
Kind: repo
Fetched: 2026-09-22T14:33:21.238973+00:00
Tool: git-clone

# priamjain/pipecat-livekit-turn

Commit: c2272db3f618f1c82e305abd18659a456aa1e486

## README

# pipecat-livekit-turn

[LiveKit Turn Detector v1](https://docs.livekit.io/agents/build/turns/turn-detector/)
as a Pipecat turn analyzer.

Pipecat ships turn analyzers for the SmartTurn family and Krisp Viva, but none
for LiveKit's end-of-utterance model. This package fills that gap: it
implements `BaseTurnAnalyzer` on top of LiveKit's cloud EOT gateway, so
`LiveKitTurnAnalyzerV1` drops into any Pipecat pipeline wherever a SmartTurn
analyzer would go.

## Why

On the [`livekit/eot-bench-data`](https://huggingface.co/datasets/livekit/eot-bench-data)
validation set, Turn Detector v1 outranks the best analyzer Pipecat ships
today — dramatically so outside English. Hindi, over an identical 952-span
set:

| model | AUC | AP |
|---|---|---|
| LiveKit Turn Detector v1 | **0.9438** | **0.9149** |
| SmartTurn v3.2 | 0.7189 | 0.5608 |

If your agent speaks anything other than English, this is usually the more
accurate choice.

## Install

Not on PyPI — install straight from the repository:

```bash
pip install git+https://github.com/priamjain/pipecat-livekit-turn
```

Pin a commit if you want reproducible builds:

```bash
pip install "git+https://github.com/priamjain/pipecat-livekit-turn@<commit-sha>"
```

Or, for a local checkout you intend to edit:

```bash
git clone https://github.com/priamjain/pipecat-livekit-turn
pip install -e ./pipecat-livekit-turn
```

Requires Python 3.10+ and `pipecat-ai>=1.8.0`.

## Credentials

The analyzer authenticates to LiveKit Cloud with a short-lived JWT minted from
your project keys. Set them in the environment:

```bash
export LIVEKIT_API_KEY=APIxxxxxxxx
export LIVEKIT_API_SECRET=xxxxxxxxxxxx
```

Or pass them directly:

```python
LiveKitTurnAnalyzerV1(api_key="APIxxxxxxxx", api_secret="...")
```

Get keys from the [LiveKit Cloud dashboard](https://cloud.livekit.io/). You do
**not** need to use LiveKit as your transport — the EOT gateway is a standalone
inference endpoint, so this works with a WebRTC, Daily, Twilio, or any other
Pipecat transport.

## Usage

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

A full runnable bot is in [`examples/bot.py`](examples/bot.py).

### How it fits with VAD

Both a VAD and this analyzer are involved, and they do different jobs:

- **Silero VAD's `stop_secs`** decides *when the model gets asked*. Keep it
  short (0.2 s is a good default). It is not the turn-end decision.
- **`LiveKitTurnParams.stop_secs`** is the hard fallback. If the user has been
  silent this long, the turn ends regardless of what the model says. Default
  3.0 s.

So a pause produces: VAD fires at 0.2 s → gateway returns `p(eot)` → below
threshold means the turn stays open and the agent keeps waiting; above it, the
turn ends immediately.

## Configuration

`LiveKitTurnParams` (a `pydantic` model, subclass of `BaseTurnParams`):

| field | default | meaning |
|---|---|---|
| `language` | `"en"` | Picks the per-language `p(eot)` threshold. |
| `threshold` | `None` | Explicit threshold; overrides the language default. |
| `stop_secs` | `3.0` | Silence after which the turn ends regardless of the model. |
| `inference_timeout_secs` | `2.0` | Wait for a prediction before falling back. |

Constructor arguments on `LiveKitTurnAnalyzerV1`:

| argument | default | meaning |
|---|---|---|
| `params` | `LiveKitTurnParams()` | Configuration above. |
| `sample_rate` | `None` | Fixed sample rate; otherwise taken from the transport. |
| `api_key` | `$LIVEKIT_API_KEY` | LiveKit project key. |
| `api_secret` | `$LIVEKIT_API_SECRET` | LiveKit project secret. |
| `base_url` | `$LIVEKIT_INFERENCE_URL` | Gateway URL. |

### Thresholds

`p(eot)` thresholds are language-specific and are exported as
`CLOUD_THRESHOLDS`, copied from
`livekit.agents.inference.eot.languages.CLOUD_LANGUAGES`:

`ar` 0.355 · `de` 0.495 · `en` 0.560 · `es` 0.590 · `fr` 0.575 · `hi` 0.575 ·
`id` 0.470 · `it` 0.640 · `ja` 0.370 · `ko` 0.695 · `nl` 0.750 · `pt` 0.665 ·
`tr` 0.650 · `zh` 0.590

An unrecognized language falls back to the English threshold. Region subtags
are stripped, so `"en-US"` resolves to `"en"`.

Lower the threshold to end turns sooner (snappier, more interruptions of a
still-thinking user); raise it to wait longer (more patient, higher latency).

## Behavior notes

**Audio streams continuously.** Every `append_audio` call forwards the buffer
to the gateway as it arrives, so an end-of-turn decision costs one inference
round trip rather than an audio upload. Expect roughly one RTT to LiveKit Cloud
per prediction; `TurnMetricsData.e2e_processing_time_ms` reports the measured
value.

**Failures degrade to VAD.** If the websocket is down, the connection fails, or
inference exceeds `inference_timeout_secs`, `analyze_end_of_turn` logs a
warning and returns `COMPLETE`. A broken detector makes the agent behave like
plain VAD instead of stranding the user in a turn that never ends.

**Reconnects are automatic.** `_ensure_connected` restarts the session on the
next audio chunk after a drop.

**Metrics.** Each prediction returns `TurnMetricsData` with `is_complete`,
`probability`, and `e2e_processing_time_ms`. Enable it with
`PipelineParams(enable_metrics=True)`.

## Known limitations

- **Turn-boundary session state is not flushed.** Pipecat's `BaseSmartTurn`
  clears its local audio buffer when a turn completes. Here the audio lives in
  the gateway's websocket session, and `clear()` does not currently tell the
  gateway to drop it — so a prediction may see audio from the previous turn in
  its context window. The protocol has a `session_flush` message that is the
  likely fix; this is unverified against LiveKit's reference agent and tracked
  as an open issue.
- **Cloud only.** This wraps the hosted `turn-detector-v1` checkpoint. There is
  no local/ONNX path here.
- **v1 audio model only.** The text-based and `-mini` variants are not wrapped.

## Development

```bash
git clone https://github.com/priamjain/pipecat-livekit-turn
cd pipecat-livekit-turn
pip install -e ".[dev]"
pytest
```

## License

BSD 2-Clause. Portions adapted from [Pipecat](https://github.com/pipecat-ai/pipecat)
(Copyright 2024-2026, Daily), under the same license.


## pyproject.toml

```
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "pipecat-livekit-turn"
version = "0.1.0"
description = "LiveKit Turn Detector v1 end-of-turn analyzer for Pipecat pipelines"
readme = "README.md"
requires-python = ">=3.10"
license = { file = "LICENSE" }
authors = [{ name = "Priam Jain" }]
keywords = [
    "pipecat",
    "livekit",
    "turn-detection",
    "end-of-turn",
    "voice-ai",
    "eou",
]
dependencies = [
    "pipecat-ai>=1.8.0",
    "livekit-api>=1.2.0",
    "livekit-protocol>=1.1.26",
    "aiohttp>=3.9",
    "protobuf>=5.0",
    "loguru>=0.7",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "pytest-asyncio>=0.24",
    "ruff>=0.6",
]

[project.urls]
Homepage = "https://github.com/priamjain/pipecat-livekit-turn"
Repository = "https://github.com/priamjain/pipecat-livekit-turn"
Issues = "https://github.com/priamjain/pipecat-livekit-turn/issues"

[tool.hatch.build.targets.wheel]
packages = ["src/pipecat_livekit_turn"]

[tool.ruff]
line-length = 100
target-version = "py310"

[tool.ruff.lint]
select = ["E", "F", "W", "I", "UP", "B"]
# The analyzer deliberately swallows every gateway failure and degrades to VAD,
# so broad excepts are the design, not an oversight.
ignore = ["B904"]

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]

```

## Top-level layout

- .github/ (dir, 1 files, ~23 lines)
- .gitignore (~11 lines)
- examples/ (dir, 2 files, ~164 lines)
- LICENSE (~28 lines)
- pyproject.toml (~57 lines)
- README.md (~200 lines)
- src/ (dir, 2 files, ~396 lines)
- tests/ (dir, 1 files, ~144 lines)

