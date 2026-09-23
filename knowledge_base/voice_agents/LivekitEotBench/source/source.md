> PDF location (no local PDF under 2 MB archived): https://github.com/livekit/eot-bench
# livekit/eot-bench
Source: https://github.com/livekit/eot-bench
Kind: repo
Fetched: 2026-09-22T14:15:26.604936+00:00
Tool: git-clone

# livekit/eot-bench

Commit: 9ee21b52840e167c58bb4d67fbf2d13fb26240b5

## README

# eot-bench

### The open benchmark for end-of-turn detection

[![Live leaderboard](https://img.shields.io/badge/leaderboard-live-2ea44f)](https://livekit.com/benchmarks/eot-bench)
[![Hugging Face Dataset](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Dataset-ffcc4d)](https://huggingface.co/datasets/livekit/eot-bench-data/)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-3776ab)](pyproject.toml)

Every voice agent has to answer the same question, over and over, on every
pause: **is the user done talking?** Answer too early and the agent talks over
people; answer too late and the conversation fills with dead air. End-of-turn
(EoT) detection is the difference between an agent that feels like a
conversation and one that feels like a walkie-talkie, and it has been one of the
hardest open problems in voice AI since the first agents shipped.

It has also been hard to measure as a field. There's a lot of strong work on
end-of-turn detection, but no shared, public way to compare it: results come
from different private datasets and different methodologies, which makes them
difficult to reproduce or line up side by side. What's been missing is common
ground.

**eot-bench is that common ground.** It's an open, reproducible benchmark, paired
with the first open [dataset](https://huggingface.co/datasets/livekit/eot-bench-data)
of real human-to-agent conversations in 14 languages. Instead of scoring models
on isolated clips, it evaluates them the way a live voice agent does: at real
pauses, under real latency and interruption budgets. We built it to evaluate
[LiveKit Turn Detector v1](https://livekit.com/blog/solving-end-of-turn-detection),
and we're releasing it so anyone building an EoT model can measure on the same
footing.

## The dataset: real conversations, 14 languages

[**`livekit/eot-bench-data`**](https://huggingface.co/datasets/livekit/eot-bench-data) is
the first open dataset of its kind for end-of-turn detection: **real
human-to-agent user turns**, with **aligned audio and textual context**, across
**14 languages**: Arabic, Chinese, Dutch, English, French, German, Hindi,
Indonesian, Italian, Japanese, Korean, Portuguese, Spanish, and Turkish.

Each row is a complete user turn from a task-oriented conversation, annotated
with every silence pause of at least 100 ms. The final pause is the true end of
the turn; every earlier pause is a mid-turn hesitation the agent should listen
through. That structure is what lets the benchmark score a model on the *actual*
decisions a voice agent faces, rather than on isolated clips. It's freely
available for download and evaluation, Apache-2.0 alongside this repo.

## Results

LiveKit Turn Detector v1 posts the strongest overall results of any model we
evaluated, in English and across all 14 languages. Explore the full
**[interactive leaderboard »](https://livekit.com/benchmarks/eot-bench)**. Set a
latency or false-cutoff budget and watch every model re-rank on the Pareto
frontier and the per-language heatmap.

<a href="https://livekit.com/benchmarks/eot-bench">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/leaderboard_dark.png">
    <img alt="End-of-turn detection leaderboard: Pareto frontier, ranking, and per-language heatmap" src="assets/leaderboard_light.png">
  </picture>
</a>

The clearest single view is how much dead air each model leaves at a fixed
interruption budget. Tuned to interrupt the user no more than 5% of the time,
how long after the user has actually finished does the agent wait before
responding? Lower means a snappier conversation. (This is endpointing delay, not
model inference time.)

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/headline_latency_en_dark.png">
  <img alt="End-of-turn delay at a 5% false-cutoff budget, English" src="assets/headline_latency_en_light.png">
</picture>

English models at four operating points, ordered by false cutoffs at a 300 ms
latency budget (best first). Lower is better on every metric:

| Model | False cutoffs @ 300 ms | False cutoffs @ 600 ms | Latency @ 5% cutoff | Latency @ 10% cutoff |
| --- | ---: | ---: | ---: | ---: |
| **LiveKit Turn Detector v1** | **9.9%** | **4.5%** | **543 ms** | **295 ms** |
| JoinIn AI Baton | 12.3% | 4.8% | 577 ms | 350 ms |
| Deepgram Flux | 12.9% | 9.9% | 1151 ms | 548 ms |
| ultraVAD | 27.7% | 11.9% | 899 ms | 663 ms |
| LiveKit Turn Detector v1-mini | 27.8% | 12.1% | 1070 ms | 698 ms |
| SmartTurn v3.2 | 35.2% | 14.8% | 1051 ms | 739 ms |
| VAP (silent agent) | 46.9% | 14.6% | 1131 ms | 749 ms |
| AssemblyAI | 49.4% | 14.6% | 1049 ms | 713 ms |
| Gradium | 55.6% | 12.6% | 913 ms | 656 ms |
| Soniox | – | 5.5% | 647 ms | 512 ms |
| Cartesia Ink 2 | – | – | 1056 ms | 911 ms |
| OpenAI GPT Realtime 2 | – | – | 1143 ms | 824 ms |
| VAD baseline | 55.6% | 21.7% | 1600 ms | 1000 ms |

A `–` means no policy setting reached that latency budget. The silence-only
**VAD baseline** runs through the identical evaluation, so every learned and
commercial detector is always measured against timing alone. All numbers are
generated from the reproducible artifacts committed under [`output/`](output/).
The [interactive leaderboard](https://livekit.com/benchmarks/eot-bench) adds the
full Pareto frontier and the breakdown across all 14 languages.

## Why false cutoffs vs. latency

A good turn detector has to satisfy two goals that pull against each other.

The first is to **never cut the user off**. Interrupting before someone has
finished a thought is the most jarring failure a voice agent can make, so the
primary objective is to minimize the **false-cutoff rate**: firing on a mid-turn
pause that wasn't actually the end of the turn. The second is to **respond
quickly** once the user *is* done, so the conversation keeps flowing instead of
filling with dead air. That's **latency**: the time the agent waits after a true
turn ending before taking the floor.

Latency here is conversational dead air, not compute. It's how long the policy
holds before it's confident the turn is over, not how fast the model runs
inference. An instant model that waits 600 ms to be sure still shows 600 ms of
latency. Minimizing it means deciding correctly *sooner*, not computing faster.

You can trivially win either goal alone: wait forever and you'll never interrupt;
fire instantly and you'll never lag. What matters is the **tradeoff** between
them. eot-bench measures that tradeoff directly. For every model it sweeps the
endpointing policy, then reports the best latency achievable at a fixed
false-cutoff budget (and vice versa), plus the full Pareto frontier. Lower-left
is better: fewer interruptions, faster responses. A single accuracy score can't
capture this, which is why the benchmark is built around the tradeoff instead.
See [Evaluation Model](#evaluation-model) for the full methodology.

## What's included

- The public turn-level dataset [`livekit/eot-bench-data`](https://huggingface.co/datasets/livekit/eot-bench-data):
  real human-to-agent turns with audio and text context in 14 languages.
- Batch and streaming adapter interfaces for local models and provider APIs,
  with reference adapters for LiveKit Turn Detector v1 / v1-mini, Deepgram Flux,
  AssemblyAI, Cartesia Ink 2, Gradium, JoinIn AI Baton, Soniox, OpenAI GPT
  Realtime, SmartTurn, ultraVAD, and VAP.
- Reproducible prediction artifacts, policy-sweep metrics, Pareto frontiers,
  operating-point tables, and multilingual heatmaps committed under `output/`.
- CLI commands for running a new adapter against one language or every supported
  dataset language, plus a Modal runner for scaled batch jobs.

## Quick Start

From the repo root:

```bash
python -m pip install -e ".[dev]"
```

Regenerate the committed English comparison artifacts:

```bash
eot-harness compare-models \
  output/livekit__eot-bench-data__validation__min_silence_100ms/en
```

Regenerate the multilingual operating-point artifacts:

```bash
eot-harness compare-languages \
  output/livekit__eot-bench-data__validation__min_silence_100ms
```

## Evaluation Model

The evaluation is built around the decision an EoT model has to support in a
production voice agent: at each silence, should the assistant respond now or
keep listening? Instead of treating EoT detection as offline classification over
isolated clips, the harness evaluates complete turns as causal silence
decisions, then compares the policies those scores can support.

### Span-Level Decisions

Each dataset row is a complete human user turn from a task-oriented
conversation. The row includes every silence span of at least 100 ms. The final
silence span is the true end of the user's turn and is labeled `eot`; every
earlier silence span is a mid-turn pause and is labeled `hold`.

The harness asks each model to score those spans causally. For a prediction at
time `t`, the adapter receives only the audio, transcript context, and messages
that would have been available by `t`. This matters because EoT errors
usually happen at ambiguous pauses inside a real turn, not at isolated clips
where the model can implicitly rely on future context or offline segmentation.

Span-level evaluation turns each user turn into the actual decision points a
voice system sees. A good model assigns high EoT probability to the final
silence while keeping probability low through ordinary hesitations and mid-turn
pauses.

### Policy Sweep and Operating Points

Raw model scores are not enough to compare models. Production systems apply a
policy on top of the score, and that policy determines the user-visible
tradeoff between responding quickly and avoiding false cutoffs. The harness
sweeps the policy space instead of judging one hand-picked threshold or timeout.

The swept policy has three knobs:

1. `threshold`: the EoT confidence needed to end the user turn.
2. `action_delay`: the minimum silence duration before the system is allowed to
   act on the model score.
3. `timeout`: the maximum silence duration the system will hold before ending
   the turn even if the model has not fired.

The harness evaluates these knobs together. Raising `action_delay` can reduce
false interruptions by ignoring short mid-turn pauses, but it adds the same
latency to every correctly detected true turn ending. Raising `timeout` lets the
system tolerate longer mid-turn pauses, but it makes false negatives more
expensive because a missed true end-of-turn leaves the assistant waiting until
the timeout expires.

Comparison reports focus on operating points under explicit false-cutoff and
latency budgets, plus the latency/cutoff Pareto frontier. They also include a
VAD-only baseline evaluated on the same policy grid, so learned EoT models are
compared against silence timing alone.

Scalar classification metrics such as `auc` and `ap` remain available in
per-run diagnostics, but they do not rank models or drive comparison reports.
They answer a different question from deployment behavior and can be misleading
for streaming APIs that expose events after an internal server-side hold or
action delay. Short mid-turn pauses may look correctly rejected without putting
the corresponding latency cost on an explicit policy knob. The policy sweep
keeps that cost visible in the latency/cutoff frontier and named operating
points.

## Scope

The harness expects an existing dataset in the public EoT benchmark schema.
Dataset construction, annotation, VAD extraction, and source-specific ingestion
live outside this package.

Required dataset fields:

- `id`
- `language`
- `audio`
- `silence_spans`

Optional dataset fields:

- `messages`
- `words`

`audio` is a Hugging Face [`Audio`](https://huggingface.co/docs/datasets/about_dataset_features#audio-feature)
feature. The harness loads it with the column cast to `Audio(decode=False)` — so
no `torchcodec` runtime decoder is required — and decodes the raw bytes itself
with `soundfile`

... (truncated, 19478 more characters)

## pyproject.toml

```
[build-system]
requires = ["setuptools>=69", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "eot-bench"
version = "0.1.0"
description = "Small end-of-turn evaluation harness for model adapter comparisons."
readme = "README.md"
license = { file = "LICENSE" }
requires-python = ">=3.10"
dependencies = [
    "aiohttp>=3.9.0",
    "datasets>=3.2.0",
    "huggingface_hub>=0.30.0",
    "librosa>=0.10.0",
    "livekit-agents>=1.6.0rc2",
    "matplotlib>=3.8.0",
    "modal>=1.0.0",
    "numpy<2",
    "pandas>=2.2.0",
    "pyarrow>=18.0.0",
    "python-dotenv>=1.0.0",
    "scikit-learn>=1.5.0",
    "seaborn>=0.13.0",
    "soundfile>=0.12.1",
    "websockets>=15.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
]
vap = [
    "einops==0.8.1",
    "torch==2.7.0",
    "torchaudio==2.7.0",
    "vap @ git+https://github.com/ErikEkstedt/VoiceActivityProjection.git@f39a78b23a6dccdbedd106e00b48c410b8739f5d",
]

[project.scripts]
eot-harness = "eot_harness.cli:main"

[tool.setuptools.packages.find]
include = ["eot_harness*"]

[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["."]

```

## Top-level layout

- .github/ (dir, 2 files, ~126 lines)
- .gitignore (~19 lines)
- assets/ (dir, 4 files, ~0 lines)
- eot_harness/ (dir, 26 files, ~6745 lines)
- LICENSE (~201 lines)
- output/ (dir, 797 files, ~36134 lines)
- pyproject.toml (~49 lines)
- README.md (~743 lines)
- requirements.txt (~13 lines)
- scripts/ (dir, 1 files, ~290 lines)
- site/ (dir, 26 files, ~3623 lines)
- tests/ (dir, 19 files, ~3170 lines)
- uv.lock (~4145 lines)

