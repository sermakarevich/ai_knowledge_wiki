[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Overview
**In one sentence:** eot-bench is an open, reproducible benchmark for end-of-turn detection that evaluates models at real pauses in real human-to-agent conversations under explicit latency and interruption budgets.
## Key points
- eot-bench answers the per-pause question "is the user done talking?", where answering too early causes talk-overs and too late causes dead air (README.md:16).
- It provides common ground for the field because prior results came from different private datasets and methodologies that are difficult to reproduce or compare (README.md:23).
- It pairs an open benchmark with the first open dataset `livekit/eot-bench-data` of real human-to-agent conversations in 14 languages, evaluated at real pauses under real latency and interruption budgets (README.md:29).
- Each dataset row is a complete user turn annotated with every silence pause of at least 100 ms, where the final pause is the true end of turn and earlier pauses are mid-turn hesitations to listen through (README.md:46).
- Models are ranked by the false-cutoff vs. latency tradeoff, reporting best latency at a fixed false-cutoff budget and vice versa plus the full Pareto frontier, not by single accuracy scores (README.md:122).
- Latency is conversational dead air (how long the policy holds before confident the turn is over), not model inference/compute time (README.md:117).
- LiveKit Turn Detector v1 posts the strongest overall results in English and across all 14 languages, with committed reproducible artifacts under `output/` and an interactive leaderboard (README.md:55).
- A silence-only VAD baseline runs through the identical evaluation/policy grid so every learned and commercial detector is measured against timing alone (README.md:98).
---
## Purpose and problem
> Every voice agent has to answer the same question, over and over, on every
> pause: **is the user done talking?** Answer too early and the agent talks over
> people; answer too late and the conversation fills with dead air. (README.md:16)

> **eot-bench is that common ground.** It's an open, reproducible benchmark, paired
> with the first open dataset of real human-to-agent conversations in 14 languages. (README.md:29)

Built to evaluate `LiveKit Turn Detector v1`, released so anyone building an EoT model measures on the same footing (README.md:33).

## Dataset: 14 languages
The dataset is [`livekit/eot-bench-data`](https://huggingface.co/datasets/livekit/eot-bench-data): real human-to-agent user turns with aligned audio and textual context (README.md:40).

Languages (14): Arabic, Chinese, Dutch, English, French, German, Hindi, Indonesian, Italian, Japanese, Korean, Portuguese, Spanish, and Turkish (README.md:43).

Each row is a complete user turn from a task-oriented conversation, annotated with every silence pause of at least 100 ms; freely available, Apache-2.0 alongside the repo (README.md:46).

## Results leaderboard
LiveKit Turn Detector v1 is strongest overall in English and all 14 languages; full interactive leaderboard at `https://livekit.com/benchmarks/eot-bench` with latency/false-cutoff budget controls, Pareto frontier, and per-language heatmap (README.md:55).

Headline view: dead air at fixed interruption budget — e.g. tuned to interrupt no more than 5% of the time, how long after the user finished does the agent wait before responding; lower is snappier (README.md:68).

English models at four operating points, ordered by false cutoffs at a 300 ms latency budget (best first); lower is better on every metric (README.md:79):

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

`–` means no policy setting reached that latency budget (README.md:98). All numbers generated from reproducible artifacts committed under `output/` (README.md:100).

## Why false cutoffs vs. latency
Two opposing goals (README.md:107):

1. **Never cut the user off** — minimize **false-cutoff rate**: firing on a mid-turn pause that was not the end of turn (README.md:109).
2. **Respond quickly** once the user is done — minimize **latency**: time waited after a true turn ending before taking the floor (README.md:112).

Latency is conversational dead air, not compute: `An instant model that waits 600 ms to be sure still shows 600 ms of latency.` (README.md:117). Either goal alone is trivial (wait forever vs. fire instantly); eot-bench sweeps the endpointing policy and reports the tradeoff plus Pareto frontier, lower-left is better (README.md:122).

## What's included
- Public turn-level dataset `livekit/eot-bench-data` with audio and text context in 14 languages (README.md:133).
- Batch and streaming adapter interfaces for local models and provider APIs, with reference adapters for LiveKit Turn Detector v1 / v1-mini, Deepgram Flux, AssemblyAI, Cartesia Ink 2, Gradium, JoinIn AI Baton, Soniox, OpenAI GPT Realtime, SmartTurn, ultraVAD, and VAP (README.md:135).
- Reproducible prediction artifacts, policy-sweep metrics, Pareto frontiers, operating-point tables, and multilingual heatmaps committed under `output/` (README.md:139).
- CLI commands for running a new adapter against one language or every supported dataset language, plus a Modal runner for scaled batch jobs (README.md:141).

## Quick Start
From the repo root (README.md:144):

```bash
python -m pip install -e ".[dev]"
```

Regenerate committed English comparison artifacts (README.md:152):

```bash
eot-harness compare-models \
  output/livekit__eot-bench-data__validation__min_silence_100ms/en
```

Regenerate multilingual operating-point artifacts (README.md:160):

```bash
eot-harness compare-languages \
  output/livekit__eot-bench-data__validation__min_silence_100ms
```

Badges/licenses declared in `README.md:11` / `pyproject.toml:14`: leaderboard, Hugging Face dataset, Apache-2.0 `LICENSE`, Python 3.10+.

## Evaluation model
Built around the production decision: at each silence, should the assistant respond now or keep listening; evaluates complete turns as causal silence decisions, not offline classification over isolated clips (README.md:168).

### Span-level decisions
Each row includes every silence span of at least 100 ms; final span labeled `eot`, earlier spans labeled `hold` (README.md:176). Adapter receives only audio, transcript context, and messages available by time `t` for a prediction at `t` (README.md:181). Good model assigns high EoT probability to final silence, low through hesitations/mid-turn pauses (README.md:187).

### Policy sweep and operating points
Swept policy knobs (README.md:199):

| Knob | Meaning |
| --- | --- |
| `threshold` | EoT confidence needed to end the user turn |
| `action_delay` | Minimum silence duration before acting on the model score |
| `timeout` | Maximum silence held before ending the turn even if the model has not fired |

Raising `action_delay` reduces false interruptions but adds latency to every true ending; raising `timeout` tolerates longer mid-turn pauses but makes false negatives costlier (README.md:207). Reports focus on operating points under explicit budgets plus the latency/cutoff Pareto frontier, with VAD-only baseline on the same grid (README.md:214). Scalar `auc`/`ap` remain in per-run diagnostics only; they do not rank models (README.md:219).

## Scope and dataset schema
Harness expects an existing dataset in the public EoT benchmark schema; construction, annotation, VAD extraction, and source-specific ingestion live outside the package (README.md:230).

| Field group | Fields |
| --- | --- |
| Required | `id`, `language`, `audio`, `silence_spans` |
| Optional | `messages`, `words` |

`audio` is a Hugging Face `Audio` feature, loaded cast to `Audio(decode=False)` and decoded from raw bytes with `soundfile`, so no `torchcodec` runtime decoder is required (README.md:246).

**Covers:** README.md (benchmark purpose, dataset, results, tradeoff, quick start, evaluation model, scope), pyproject.toml (Python 3.10+), output/ (committed artifacts), LICENSE (Apache-2.0)
