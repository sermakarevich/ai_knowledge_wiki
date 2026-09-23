# Technical Analysis: livekit/eot-bench

**Repository:** https://github.com/livekit/eot-bench
**Version analyzed:** unknown
**Date:** 2026-09-22
**Wiki:** [[index]]

## 1. Overview

Problem space: every voice agent must decide at each pause whether the user finished speaking. Answering too early produces false cutoffs (talk-overs); answering too late produces conversational dead air (README.md:16, 01-overview.md:6). Prior end-of-turn results were not comparable because they came from different private datasets and methodologies (README.md:23, 01-overview.md:6).

How the repo addresses it: eot-bench is an open, reproducible benchmark plus the first open dataset of real human-to-agent conversations in 14 languages, evaluated at real pauses under explicit latency and interruption budgets (README.md:29, 01-overview.md:7). Each dataset row is a complete user turn annotated with every silence pause of at least 100 ms; the final pause is the true end of turn, earlier pauses are mid-turn hesitations to listen through (README.md:46, 01-overview.md:8). Models are ranked by the false-cutoff vs. latency tradeoff — best latency at a fixed false-cutoff budget and vice versa plus the full Pareto frontier — not by single accuracy scores (README.md:122, 01-overview.md:9). Latency is conversational dead air (hold time before confident the turn is over), not model inference time (README.md:117, 01-overview.md:10).

Primary user: engineers building or selecting end-of-turn detectors for voice agents, including LiveKit Turn Detector v1 authors who built the harness to evaluate that model and released it so others measure on the same footing (README.md:33, 01-overview.md:22).

## 2. High-Level Architecture

```
Dataset (livekit/eot-bench-data) ─► Adapters (batch / streaming) ─► Predictions
        │                                     ▼
        │                              Policy sweep
        │                          (threshold │ action_delay │ timeout)
        ▼                                     ▼
  Silence spans (>=100ms) ──────────► Metrics + Pareto frontier ─► output/ artifacts + leaderboard
```

Data-flow narrative:

1. Load a dataset row: a complete task-oriented user turn with aligned audio and textual context in one of 14 languages (Arabic, Chinese, Dutch, English, French, German, Hindi, Indonesian, Italian, Japanese, Korean, Portuguese, Spanish, Turkish) (README.md:40, README.md:43, 01-overview.md:25-27).
2. Expand the row into causal span-level decisions: every silence span of at least 100 ms; the final span is labeled `eot`, earlier spans `hold` (README.md:176, 01-overview.md:97). Each prediction at time `t` receives only audio, transcript context, and messages available by `t` (README.md:181, 01-overview.md:97).
3. Score each span through an adapter. The harness provides batch and streaming adapter interfaces for local models and provider APIs, with reference adapters for LiveKit Turn Detector v1 / v1-mini, Deepgram Flux, AssemblyAI, Cartesia Ink 2, Gradium, JoinIn AI Baton, Soniox, OpenAI GPT Realtime, SmartTurn, ultraVAD, and VAP (README.md:135, 01-overview.md:66). A silence-only VAD baseline runs through the identical policy grid (README.md:98, 01-overview.md:12).
4. Convert scores to decisions via a swept endpointing policy over `threshold` (EoT confidence needed to end the turn), `action_delay` (minimum silence before acting), and `timeout` (maximum silence held before ending anyway) (README.md:199, 01-overview.md:102-106).
5. Report operating points under explicit budgets (e.g. false cutoffs at 300/600 ms latency; latency at 5%/10% cutoff) plus the latency/cutoff Pareto frontier; scalar `auc`/`ap` remain per-run diagnostics and do not rank models (README.md:214, README.md:219, 01-overview.md:108).
6. Commit reproducible prediction artifacts, policy-sweep metrics, Pareto frontiers, operating-point tables, and multilingual heatmaps under `output/`, surfaced by the interactive leaderboard (README.md:139, README.md:55, 01-overview.md:67, 01-overview.md:31).

Persistent state lives in committed artifacts under `output/` (e.g. `output/livekit__eot-bench-data__validation__min_silence_100ms/en`), not in a database (README.md:100, 01-overview.md:54, 01-overview.md:80-84). Local working state excluded from version control includes Hugging Face caches (`.hf_datasets_cache/`, `.hf_home/`, `.hf_tmp/`), `.cache/`, `eot_harness/output/`, `eot_harness/notebooks/`, and `tmp/` (`.gitignore:2-4`, `.gitignore:10`, `.gitignore:12-14`, 02-top-level-files.md:8-10).

## 3. The Silence Span

Representation: a dataset row is a complete user turn carrying `id`, `language`, `audio`, and `silence_spans`, with optional `messages` and `words` (README.md:230, 01-overview.md:113-116). `audio` is a Hugging Face `Audio` feature, cast to `Audio(decode=False)` and decoded from raw bytes with `soundfile`, so no `torchcodec` runtime decoder is required (README.md:246, 01-overview.md:118). Every silence span of at least 100 ms is annotated; the minimum-silence threshold is visible in artifact paths as `min_silence_100ms` (README.md:46, 01-overview.md:8, 01-overview.md:81).

Named kinds/types with file:line:

- `eot` — the final silence span of a turn, the true end of turn (README.md:176, 01-overview.md:97).
- `hold` — any earlier silence span, a mid-turn hesitation the policy must listen through (README.md:176, 01-overview.md:97).
- `threshold` — EoT confidence needed to end the user turn (README.md:199, 01-overview.md:103).
- `action_delay` — minimum silence duration before acting on the model score (README.md:199, 01-overview.md:104).
- `timeout` — maximum silence held before ending the turn even if the model has not fired (README.md:199, 01-overview.md:106).
- `false-cutoff rate` — firing on a mid-turn pause that was not the end of turn (README.md:109, 01-overview.md:59).
- `latency` — time waited after a true turn ending before taking the floor; conversational dead air, not compute (README.md:112, README.md:117, 01-overview.md:60-62).

Key queries: the policy-grid tradeoff is queried at fixed budgets rather than by threshold tuning. Verbatim:

> `An instant model that waits 600 ms to be sure still shows 600 ms of latency.` (README.md:117, 01-overview.md:62)

> Every voice agent has to answer the same question, over and over, on every pause: **is the user done talking?** Answer too early and the agent talks over people; answer too late and the conversation fills with dead air. (README.md:16, 01-overview.md:16-17)

The wiki pages consulted do not document the Python class or function names that implement spans, so no class-level `file:line` beyond the schema fields above can be grounded.

## 4. LLM / External Service Integration

Providers: the harness defines batch and streaming adapter interfaces for local models and provider APIs; reference adapters cover LiveKit Turn Detector v1 / v1-mini, Deepgram Flux, AssemblyAI, Cartesia Ink 2, Gradium, JoinIn AI Baton, Soniox, OpenAI GPT Realtime, SmartTurn, ultraVAD, and VAP (README.md:135, 01-overview.md:66). The evaluated commercial set therefore includes Deepgram, AssemblyAI, Cartesia, Gradium, JoinIn AI, Soniox, and OpenAI endpoints, plus the local VAP and ultraVAD/SmartTurn detectors (README.md:79, 01-overview.md:38-52).

Required vs optional calls: every adapter, including the silence-only VAD baseline, is required to run through the identical evaluation/policy grid so learned and commercial detectors are measured against timing alone (README.md:98, 01-overview.md:12). No single provider call is required to reproduce the committed English comparison artifacts; `eot-harness compare-models` and `compare-languages` recompute metrics from artifacts under `output/` without re-calling providers (README.md:152, README.md:160, 01-overview.md:80-88).

Env vars: the wiki documents only that secrets are kept out of version control — `eot_harness/.env`, `.env`, `/.env` are git-ignored (`.gitignore:11`, `.gitignore:16-17`, 02-top-level-files.md:9) — and that `python-dotenv>=1.0.0` is a pinned dependency (requirements.txt:9, 02-top-level-files.md:12). Per-provider API keys and endpoint URLs are not enumerated in the wiki pages consulted, so they are not listed here.

## 5. The Evaluation Pipeline

Step by step, with the function-level `file.py:line` caveat below:

1. Install the harness: `python -m pip install -e ".[dev]"` from the repo root (README.md:144, 01-overview.md:74).
2. Load the public turn-level dataset `livekit/eot-bench-data` (audio plus text context, 14 languages, Apache-2.0) (README.md:133, README.md:40, 01-overview.md:25, 01-overview.md:65).
3. Run a new adapter against one language or every supported dataset language via the CLI, plus a Modal runner for scaled batch jobs (README.md:141, 01-overview.md:68).
4. Score every silence span of at least 100 ms causally (final span `eot`, earlier spans `hold`), using only context available by time `t` (README.md:176, README.md:181, 01-overview.md:97). A good model assigns high EoT probability to the final silence and low scores through hesitations (README.md:187, 01-overview.md:97).
5. Sweep the three-knob policy (`threshold`, `action_delay`, `timeout`); raising `action_delay` reduces false interruptions but adds latency to every true ending, raising `timeout` tolerates longer mid-turn pauses but makes false negatives costlier (README.md:199, README.md:207, 01-overview.md:102-108).
6. Emit operating-point tables (false cutoffs at 300/600 ms latency budgets; latency at 5%/10% cutoff budgets), the Pareto frontier, per-language heatmaps, and per-run `auc`/`ap` diagnostics, committed under `output/` (README.md:79, README.md:139, README.md:219, 01-overview.md:36-52, 01-overview.md:67).
7. Regenerate published views without re-running models: `eot-harness compare-models output/livekit__eot-bench-data__validation__min_silence_100ms/en` for the English comparison and `eot-harness compare-languages output/livekit__eot-bench-data__validation__min_silence_100ms` for multilingual operating points (README.md:152, README.md:160, 01-overview.md:80-88).

File:line grounding limit: the two wiki pages consulted cite `README.md`, `pyproject.toml`, `output/`, `LICENSE`, `.gitignore`, and `requirements.txt` line ranges only (01-overview.md:120, 02-top-level-files.md:81). They do not expose harness module paths or function definitions, so per-function `file.py:line` references cannot be grounded and are omitted rather than invented.

## 6. Key Files

| File | Lines | What It Does |
| --- | --- | --- |
| README.md | cited 16–246 | Benchmark purpose, dataset, results, tradeoff definition, quick start, evaluation model, scope and schema |
| output/livekit__eot-bench-data__validation__min_silence_100ms/en | artifact dir | Committed English prediction artifacts and comparison inputs for `compare-models` |
| output/livekit__eot-bench-data__validation__min_silence_100ms | artifact dir | Committed multilingual artifacts and comparison inputs for `compare-languages` |
| pyproject.toml | 14 lines cited | Package metadata: badges/licenses, Python 3.10+ floor |
| LICENSE | — | Apache-2.0 license, shared with dataset |
| requirements.txt | 14 | Pins data/audio/eval/infra dependency stack |
| .gitignore | 20 | Excludes caches, virtualenvs, secrets, generated outputs |
| eot_harness/.env (ignored) | — | Local secrets for provider adapters, never committed |
| eot_harness/output/ (ignored) | — | Local working-tree outputs excluded from git |
| eot_harness/notebooks/ (ignored) | — | Local notebooks excluded from git |
| tmp/ (ignored) | — | Scratch working directory excluded from git |
| .hf_datasets_cache/ / .hf_home/ / .hf_tmp/ / .cache/ (ignored) | — | Hugging Face and generic local caches |

The table is limited to files attested in the wiki pages consulted (01-overview.md:120, 02-top-level-files.md:81). Harness package modules, adapter implementations, and Modal runner files are referenced only by role in the wiki prose (batch/streaming adapters, CLI, Modal runner) without file paths, so they are not listed.

## 7. Dependencies

| Package | Version constraint | Purpose |
| --- | --- | --- |
| datasets | >=3.2.0 | Dataset loading (`livekit/eot-bench-data`) |
| pandas | >=2.2.0 | Metrics tables and operating-point reporting |
| pyarrow | >=18.0.0 | Tabular/artifact interchange backing `datasets`/`pandas` |
| numpy | <2 | Numeric base pinned below major v2 |
| scikit-learn | >=1.5.0 | Eval metrics (`auc`/`ap` diagnostics, sweeps) |
| librosa | >=0.10.0 | Audio handling |
| soundfile | >=0.12.1 | Audio decoding from raw bytes without `torchcodec` |
| matplotlib | >=3.8.0 | Pareto-frontier and comparison plots |
| seaborn | >=0.13.0 | Heatmaps and statistical plots |
| modal | >=1.0.0 | Scaled batch-job runner |
| websockets | >=15.0.0 | Streaming adapter transport |
| huggingface_hub | >=0.30.0 | Dataset/model-hub access |
| python-dotenv | >=1.0.0 | `.env` secret loading |

All constraints are exact strings from requirements.txt:1-14 (02-top-level-files.md:49-64). The wiki also attests Python 3.10+ via pyproject.toml:14 and Apache-2.0 via LICENSE (01-overview.md:91). Dev-extras contents of `pip install -e ".[dev]"` beyond this list are not enumerated in the wiki pages consulted.

## 8. CLI / Usage Surface

Entry points (from the repo root):

| Command | Input | Output |
| --- | --- | --- |
| `python -m pip install -e ".[dev]"` | repo root | Installed harness with dev extras (README.md:144) |
| `eot-harness compare-models output/livekit__eot-bench-data__validation__min_silence_100ms/en` | committed English artifacts | Regenerated English comparison artifacts (README.md:152) |
| `eot-harness compare-languages output/livekit__eot-bench-data__validation__min_silence_100ms` | committed multilingual artifacts | Regenerated multilingual operating-point artifacts (README.md:160) |

The wiki additionally attests CLI commands for running a new adapter against one language or every supported dataset language, plus a Modal runner for scaled batch jobs, without quoting their exact argv strings (README.md:141, 01-overview.md:68). Those strings are therefore not tabulated here.

Env-var and config surface attested in the wiki:

| Key | Source | Meaning |
| --- | --- | --- |
| `eot_harness/.env`, `.env`, `/.env` | `.gitignore:11`, `.gitignore:16-17` | Local secret files, excluded from git |
| `threshold` | README.md:199 | EoT confidence needed to end the user turn |
| `action_delay` | README.md:199 | Minimum silence duration before acting on the model score |
| `timeout` | README.md:199 | Maximum silence held before ending the turn anyway |
| `min_silence_100ms` | artifact path segment | Silence-span extraction threshold (100 ms) selecting the evaluated span set |
| `auc` / `ap` | README.md:219 | Per-run scalar diagnostics; do not rank models |

Dataset schema config: required `id`, `language`, `audio`, `silence_spans`; optional `messages`, `words` (README.md:230, 01-overview.md:113-116).

## 9. Extensibility Points

| Extension | Where to extend |
| --- | --- |
| New detector (batch or streaming) | Add a batch/streaming adapter behind the documented adapter interfaces covering local models and provider APIs (README.md:135) |
| New provider endpoint | Add a reference-style adapter alongside the existing LiveKit, Deepgram, AssemblyAI, Cartesia, Gradium, JoinIn AI, Soniox, OpenAI, SmartTurn, ultraVAD, and VAP adapters (README.md:135) |
| New language or dataset split | Supply data in the public EoT benchmark schema (required `id`, `language`, `audio`, `silence_spans`; optional `messages`, `words`) and run the per-language / all-language CLI plus Modal runner (README.md:230, README.md:141) |
| New policy regime | Extend the `threshold` / `action_delay` / `timeout` sweep grid and re-run `compare-models` / `compare-languages` over `output/` artifacts (README.md:199, README.md:152, README.md:160) |
| New published view | Extend the committed `output/` artifacts path (prediction artifacts, sweep metrics, Pareto frontiers, operating-point tables, multilingual heatmaps) and the leaderboard budget controls (README.md:139, README.md:55) |

File/class-level extension targets are not named in the wiki pages consulted; the table is grounded at the interface/artifact level attested there.

## 10. Limitations and Gotchas

- **Tight latency budgets are unreachable for several commercial systems.** Soniox reaches no 300 ms setting, and Cartesia Ink 2 and OpenAI GPT Realtime reach neither 300 ms nor 600 ms settings, recorded as `–` in the English table (README.md:98, 01-overview.md:49-52, 01-overview.md:54). Comparing them at 300 ms therefore compares absence, not quality.
- **The VAD-only baseline is weak at tight budgets and flatters lazy policies elsewhere.** It posts 55.6% false cutoffs at 300 ms, 21.7% at 600 ms, and 1600/1000 ms latency at 5%/10% cutoff budgets (README.md:79, README.md:98, 01-overview.md:38-52). Any detector near those numbers is exploiting timing alone.
- **Latency is dead air, not inference time, and scalar metrics do not rank.** An instant model that waits 600 ms still shows 600 ms latency, and `auc`/`ap` are per-run diagnostics only (README.md:117, README.md:219, 01-overview.md:62, 01-overview.md:108). Optimizing AUC without moving the Pareto frontier does not improve the benchmark standing.
- **Construction and ingestion live outside the harness.** Dataset construction, annotation, VAD extraction, and source-specific ingestion are out of scope; the harness only consumes datasets already in the EoT schema (README.md:230, 01-overview.md:111). Span-label noise or VAD-threshold effects (100 ms floor) propagate silently into scores.
- **Local state is easy to confuse with committed state.** `eot_harness/output/`, `eot_harness/notebooks/`, `tmp/`, HF caches, `.env` files, virtualenvs, and bytecode are all git-ignored (`.gitignore:1-20`, 02-top-level-files.md:15-36). Only `output/` committed artifacts reproduce the leaderboard numbers (README.md:100, 01-overview.md:54).

## 11. How It Compares to Alternatives

The benchmark's English table itself functions as the comparison set; all systems below run through the same span sets and policy grid (README.md:79, README.md:98, 01-overview.md:36-54):

- **LiveKit Turn Detector v1 (9.9% @ 300 ms; 543/295 ms @ 5%/10%)** — strongest overall in English and all 14 languages; the reference the harness was built to evaluate (README.md:33, README.md:55, README.md:79).
- **JoinIn AI Baton (12.3% @ 300 ms; 577/350 ms @ 5%/10%)** — closest follower on both axes, the only other system near LiveKit v1 at tight budgets (README.md:79).
- **Deepgram Flux (12.9% @ 300 ms; 1151/548 ms @ 5%/10%)** — competitive on false cutoffs at 300 ms but pays roughly double the dead air at the 5% cutoff budget (README.md:79).
- **Silence-only VAD baseline (55.6% @ 300 ms; 1600/1000 ms @ 5%/10%)** plus SmartTurn v3.2, ultraVAD, VAP (silent agent), AssemblyAI, Gradium, Soniox, Cartesia Ink 2, OpenAI GPT Realtime, and LiveKit v1-mini — the long tail and timing floor showing what silence duration alone achieves versus learned or commercial detection (README.md:79, README.md:98, 01-overview.md:42-52).

Positioning sentence: eot-bench does not propose another detector; it provides the common causal-span, budget-based ground on which detectors — from VAD timing floors to commercial streaming endpoints to LiveKit v1 — are compared by interruption/latency tradeoff rather than by isolated accuracy (README.md:29, README.md:122, 01-overview.md:7-9).

## Appendix: Selected Code Snippets

1. Install from the repo root (README.md:144, 01-overview.md:72-75):

```bash
python -m pip install -e ".[dev]"
```

2. Regenerate committed English comparison artifacts (README.md:152, 01-overview.md:77-82):

```bash
eot-harness compare-models \
  output/livekit__eot-bench-data__validation__min_silence_100ms/en
```

3. Regenerate multilingual operating-point artifacts (README.md:160, 01-overview.md:84-89):

```bash
eot-harness compare-languages \
  output/livekit__eot-bench-data__validation__min_silence_100ms
```

4. Repository ignore rules for caches, secrets, and generated trees, verbatim (`.gitignore:1-20`, 02-top-level-files.md:15-36):

```
.DS_Store
.cache/
.hf_datasets_cache/
.hf_home/
.hf_tmp/
.pytest_cache/
.venv/
__pycache__/
*.py[cod]
eot_harness/.env
eot_harness/output/
eot_harness/notebooks/
tmp/

.env
/.env
.venv-test/

*egg-info
```
