# Technical Analysis: ZhangHe0918/MTR-DuplexBench

**Repository:** https://github.com/ZhangHe0918/MTR-DuplexBench
**Version analyzed:** unknown
**Date:** 2026-09-22
**Wiki:** [[index]]

## 1. Overview / What Problem It Solves

Full-duplex speech language models must handle barge-in, pauses, backchannels, background noise, and multi-round instruction context in real time, but most speech benchmarks score single-turn, half-duplex output. MTR-DuplexBench (accepted to ACL 2026 Findings) fills that gap with a benchmark for multi-round, full-duplex dialogue: it distributes scenario encodings, evaluation audio, and scoring scripts covering four dimensions — Dialogue Quality, Conversational Features, Instruction Following, and Safety (01-overview.md:3-3, 01-overview.md:47-55). The repo itself does not train or serve models; it defines the task inputs (JSON scenario encodings plus per-dimension audio) and the scoring harness (`code/Eval/` scripts) that a model builder runs against their own system's stereo output (01-overview.md:56-61, 01-overview.md:79-85). The primary user is a researcher or engineer evaluating their own full-duplex speech model (e.g. Moshi-, VocalNet-, or Bailing-style systems, per the `envs/` configs) against these four dimensions (01-overview.md:160-166).

## 2. High-Level Architecture

```
Scenarios_encoding/*.json(.l)          data/*/audios + *.mp3/*.wav
 (dialogue structure,                    (per-dimension
  turn-taking, timing)                    user-side prompts)
        │                                            │
        ▼                                            ▼
┌───────────────────┐   stereo WAV/MP3   ┌───────────────────────┐
│ User model        │ ──────────────────► │ Eval/ scripts         │
│ inference (out    │   left=user │       │ Whisper ASR (left/    │
│ of repo)          │   right=model       │ right) + metrics /    │
└───────────────────┘                     │ GPT-4o judge          │
                                          └───────────┬───────────┘
                                                      ▼
                                          results/*.json(l) scores
                                          (per-turn / per-round +
                                           aggregates)
```

Data-flow narrative:

1. The evaluator loads the scenario encoding JSON for the target dimension — turn structure, turn-taking patterns, and timing — e.g. `Scenarios_encoding/single_scenario/scenario_encoding_smooth.json` or the multi-scenario `scenario_encoding_{1,2,3,4}.json` files (01-overview.md:62-76).
2. The evaluator runs their own model inference outside the repo, feeding it the dimension's input audio (`data/Dialogue_Quality/*.mp3`, `data/Conversational_Features/original/*.wav` or `woPAUSE/*.wav`, `data/Instruction_Following/audios/*.wav`, `data/Safety/audios/*.wav`), and produces stereo output with left channel = user audio and right channel = model audio (01-overview.md:79-89, 01-overview.md:91-96, 01-overview.md:112-121, 01-overview.md:131-140).
3. The corresponding `Eval/` script transcribes the stereo output with the shared Whisper utility `asr_incremental_save.py`, which transcribes left/right channels independently with incremental saving and JSON caching (01-overview.md:11-11, 01-overview.md:104-111, 01-overview.md:151-159).
4. Each script computes its dimension's metrics from ASR segments plus timestamps/encodings: 0–5 semantic scores (Dialogue Quality), success/latency/frequency (Conversational Features), binary following rate (Instruction Following), binary safe/unsafe rate (Safety) (01-overview.md:79-80, 01-overview.md:91-96, 01-overview.md:112-130, 01-overview.md:131-150).
5. Results are written to a JSON/JSONL results file (e.g. `results/dialogue_quality_scores.jsonl`, `results/instruction_following_results.json`, `results/safety_results.json`, `results/asr_results.json`) with per-turn/per-round detail and printed or aggregated overall rates (01-overview.md:80-89, 01-overview.md:104-111, 01-overview.md:112-130, 01-overview.md:131-150).

Persistent state lives in files, not a service: scenario encodings and input audio under `data/`, model output stereo audio in a user-chosen directory, ASR JSON cache files, and results JSON/JSONL under `results/` (01-overview.md:19-41, 01-overview.md:104-111, 01-overview.md:151-159).

## 3. The Scenario Encoding

The repo's central concept is the **scenario encoding**: a JSON (or JSONL for dialogue quality) file that specifies dialogue structure, turn-taking patterns, and timing for a test case, decoupling the benchmark definition from any particular model (01-overview.md:62-69). Encodings exist per dimension: `single_scenario/scenario_encoding_{smooth,interruption,pause,background}.json`, `multi_scenarios/scenario_encoding_{1,2,3,4}.json`, `instruction_following/scenario_encoding_{smooth,interruption}.json`, `safety/scenario_encoding_{smooth,interruption}.json`, and `dialogue_quality/semantic_turned_time_v3.jsonl` (01-overview.md:70-76). The canonical access pattern is a plain JSON load (01-overview.md:62-69):

```python
import json

# Example: load a single-scenario encoding
with open("data/Scenarios_encoding/single_scenario/scenario_encoding_smooth.json") as f:
    encoding = json.load(f)
```

Key query types against an encoding: turn-boundary lookup (which time spans belong to which turn, used by the Dialogue Quality scorer via `--turn_mask_path`), per-dialogue encoding selection for the `eval_N_scenarios()` calls, and per-round start-timestamp lookup (`--round_start_json`) for Instruction Following and Safety (01-overview.md:80-89, 01-overview.md:91-104, 01-overview.md:122-129, 01-overview.md:141-149).

## 4. LLM / External Service Integration

- **Provider:** OpenAI GPT-4o, used as judge in three of four dimensions: Dialogue Quality (0–5 semantic score), Instruction Following (binary 0/1), Safety (binary 0 = safe / 1 = unsafe) (01-overview.md:8-8, 01-overview.md:47-55, 01-overview.md:79-80, 01-overview.md:112-113, 01-overview.md:131-132).
- **Required vs optional:** GPT-4o calls are required for the Dialogue Quality, Instruction Following, and Safety scripts; Conversational Features scripts (`eval_1/2/3/4_scenarios.py`, `eval_single_scenario_*.py`) compute signal-derived metrics (success, latency, frequency) with no LLM judge (01-overview.md:47-55, 01-overview.md:91-96).
- **Speech-to-text dependency:** local OpenAI Whisper (via the `whisper` package) for all ASR, run on a selectable CUDA device in at least the Safety script (01-overview.md:11-11, 01-overview.md:141-149).
- **Env vars:** `OPENAI_API_KEY` must be set for any GPT-4o-judged dimension (01-overview.md:8-8).

## 5. The Three-Step Evaluation Pipeline

1. **Load scenario encoding** — `json.load` of the dimension's file under `data/Scenarios_encoding/` (e.g. `single_scenario/scenario_encoding_smooth.json`) to obtain dialogue structure and timing (01-overview.md:62-76). Function: user code, no repo function; example at 01-overview.md:62-69.
2. **Run own-model inference to stereo audio** — feed the dimension's input audio to the model under test and write stereo files (left = user, right = model); Dialogue Quality uses stereo MP3 (`data/Dialogue_Quality/*.mp3` in, stereo MP3 out), the other three dimensions use stereo WAV with per-dimension naming (`dialogue_instruction_following_*_round_*_*.wav`, `dialogue_safety_*_round_*_*.wav`) (01-overview.md:77-78, 01-overview.md:79-89, 01-overview.md:91-96, 01-overview.md:112-121, 01-overview.md:131-140).
3. **Transcribe with the shared ASR utility** — `asr_incremental_save.py` transcribes left/right channels independently with incremental saving and JSON cache (`--audio_dir`, `--output_file`, `--user_channel`, `--cache_file`) (01-overview.md:104-111, 01-overview.md:151-159). Function: `asr_incremental_save.py` entry point (01-overview.md:151-159).
4. **Score Dialogue Quality** — `gpt4o_mark_in_turn_GT_condor.py --jsonl_file_path --turn_mask_path --audio_path` writes per-turn 0–5 scores to JSONL and prints the average model-turn score (01-overview.md:80-89). Function: `gpt4o_mark_in_turn_GT_condor.py` entry point (01-overview.md:80-89).
5. **Score Conversational Features** — call `eval_N_scenarios()` from `eval_1_scenario.py` / `eval_2_scenarios.py` / `eval_3_scenarios.py` / `eval_4_scenarios.py` (layered hierarchy delegating to lower ones) or the single-scenario variants `eval_single_scenario_pause_handling.py` / `eval_single_scenario_background.py`, passing ASR segments and timestamps, then aggregate success/latency/frequency (01-overview.md:91-104). Functions: `eval_1_scenario.py`, `eval_2_scenarios.py`, `eval_3_scenarios.py`, `eval_4_scenarios.py`, `eval_single_scenario_pause_handling.py`, `eval_single_scenario_background.py` entry points (01-overview.md:91-104).
6. **Score Instruction Following / Safety** — `instruction_following_evaluation.py --instruction_following_output_dir --output_file --user_channel` and `safety_evaluation.py --safety_output_dir --output_file --user_channel`, each with optional `--asr_cache_file`, `--round_start_json`, `--max_round`, `--analyze_only`, `--analysis_output` (plus `--cuda_device` for Safety), producing per-round JSON and overall following / safe-unsafe rates (01-overview.md:113-130, 01-overview.md:132-150). Functions: `instruction_following_evaluation.py`, `safety_evaluation.py` entry points (01-overview.md:113-150).

## 6. Key Files

| File | Lines | What It Does |
| :--- | :--- | :--- |
| `code/Eval/asr_incremental_save.py` | n/a (line counts not in wiki) | Shared Whisper ASR: independent left/right transcription, incremental save, JSON cache |
| `code/Eval/gpt4o_mark_in_turn_GT_condor.py` | n/a | Dialogue Quality scorer: GPT-4o 0–5 per-turn semantic scores, JSONL output |
| `code/Eval/eval_1_scenario.py` | n/a | Single-scenario (smooth turn-taking) Conversational Features scorer; base of hierarchy |
| `code/Eval/eval_2_scenarios.py` | n/a | Two-scenario Conversational Features scorer, delegates to lower layer |
| `code/Eval/eval_3_scenarios.py` | n/a | Three-scenario Conversational Features scorer, delegates to lower layer |
| `code/Eval/eval_4_scenarios.py` | n/a | Four-scenario (all combined) Conversational Features scorer |
| `code/Eval/eval_single_scenario_pause_handling.py` | n/a | Single-scenario pause-handling scorer (success, latency, frequency) |
| `code/Eval/eval_single_scenario_background.py` | n/a | Single-scenario background-noise scorer (success, latency, frequency) |
| `code/Eval/instruction_following_evaluation.py` | n/a | Instruction Following scorer: ASR + GPT-4o binary judge, per-round JSON |
| `code/Eval/safety_evaluation.py` | n/a | Safety scorer: ASR + GPT-4o binary safe/unsafe judge, per-round JSON |
| `data/Scenarios_encoding/` | n/a | All scenario encodings per dimension (single, multi, instruction, safety, dialogue quality) |
| `data/Conversational_Features/original/*.wav`, `woPAUSE/*.wav` | n/a | Conversational Features input audio |
| `data/Dialogue_Quality/*.mp3` | n/a | Dialogue Quality input audio |
| `data/Instruction_Following/audios/*.wav`, `instruction_following_data.json` | n/a | Instruction Following prompts and metadata |
| `data/Safety/audios/*.wav`, `safety_data.json` | n/a | Safety prompts and metadata |
| `envs/bailing/`, `envs/moshi/`, `envs/vocalnet/`, `envs/freeze_and_eval/` | n/a | Per-model conda/requirements environment configs |

(Scope note: the wiki component page reports file roles and flags but no line counts; the "Lines" column is therefore marked n/a rather than invented. Coverage: 01-overview.md:19-55, 01-overview.md:160-166.)

## 7. Dependencies

| Package | Version constraint | Purpose |
| :--- | :--- | :--- |
| `openai` | unpinned (`pip install openai`, no version in wiki) | GPT-4o judge API client |
| `whisper` | unpinned (`pip install whisper`, no version in wiki) | Local ASR for stereo channel transcription |
| `torch` | unpinned (`pip install torch`, no version in wiki) | Whisper/model compute backend |
| per-model conda/requirements in `envs/` | per-file (see `envs/bailing/`, `envs/moshi/`, `envs/vocalnet/`, `envs/freeze_and_eval/`) | Reproduce each reference model's runtime |

(Source: 01-overview.md:42-46, 01-overview.md:160-160.)

## 8. CLI / Usage Surface

Entry points are the `Eval/` scripts, run from `cd Eval` (01-overview.md:80-150). There is no packaged CLI or config file; configuration is CLI flags plus input/output directory conventions.

| Command | Purpose | Key flags |
| :--- | :--- | :--- |
| `python gpt4o_mark_in_turn_GT_condor.py` | Dialogue Quality scoring | `--jsonl_file_path`, `--turn_mask_path`, `--audio_path` |
| `python asr_incremental_save.py` | Standalone/shared ASR pass | `--audio_dir`, `--output_file`, `--user_channel`, `--cache_file` |
| `python instruction_following_evaluation.py` | Instruction Following scoring | `--instruction_following_output_dir`, `--output_file`, `--user_channel` (+ `--asr_cache_file`, `--round_start_json`, `--max_round`, `--analyze_only`, `--analysis_output`) |
| `python safety_evaluation.py` | Safety scoring | `--safety_output_dir`, `--output_file`, `--user_channel` (+ `--asr_cache_file`, `--cuda_device`, `--round_start_json`, `--max_round`, `--analyze_only`, `--analysis_output`) |
| `eval_1/2/3/4_scenarios()`, `eval_single_scenario_*` | Conversational Features scoring (library-style calls after ASR) | ASR segments + timestamps + per-dialogue encoding |

Env vars:

| Variable | Required for | Description |
| :--- | :--- | :--- |
| `OPENAI_API_KEY` | Dialogue Quality, Instruction Following, Safety | Authenticates GPT-4o judge calls |

Config inputs (by convention, not schema-validated in the wiki): scenario encoding JSON under `data/Scenarios_encoding/`; model output stereo audio (left = user, right = model) with per-dimension naming; optional ASR cache JSON and round-start-timestamp JSON (01-overview.md:62-78, 01-overview.md:122-129, 01-overview.md:141-149).

## 9. Extensibility Points

- **New turn-taking scenario:** add an encoding JSON under `data/Scenarios_encoding/` following the existing `{smooth,interruption,pause,background}` / `{1,2,3,4}` shapes, and add or reuse an `eval_*_scenario*.py` scorer that consumes ASR segments plus timestamps (01-overview.md:70-76, 01-overview.md:91-104).
- **New scoring metric:** extend the relevant `Eval/` script (`gpt4o_mark_in_turn_GT_condor.py` for quality, `eval_N_scenarios.py` family for conversational features, `instruction_following_evaluation.py`, `safety_evaluation.py`) where aggregation of success/latency/frequency or judge scores happens (01-overview.md:91-104, 01-overview.md:112-150).
- **Alternative judge or ASR backend:** swap the GPT-4o call site in the three judge scripts or the Whisper call in `asr_incremental_save.py`; downstream scripts already accept `--asr_cache_file` so a new transcriber only needs to emit the same JSON shape (01-overview.md:122-129, 01-overview.md:141-159).
- **New reference model environment:** add a directory under `envs/` with conda YAML plus requirements, mirroring `bailing/`, `moshi/`, `vocalnet/`, `freeze_and_eval/` (01-overview.md:160-160).
- **Offline/analyze-only reporting:** reuse `--analyze_only` + `--analysis_output` in the Instruction Following and Safety scripts to recompute reports from existing result JSON without re-running judges (01-overview.md:122-129, 01-overview.md:141-149).

## 10. Limitations and Gotchas

- **Model inference is out of scope and format-strict:** the repo provides no inference runner; output must be stereo with left = user and right = model, MP3 for Dialogue Quality and WAV (with exact `dialogue_*_*_round_*_*.wav` names) elsewhere — a mono file or swapped channels silently invalidates scoring (01-overview.md:77-78, 01-overview.md:79-89, 01-overview.md:112-140).
- **Three dimensions depend on a paid external judge:** Dialogue Quality, Instruction Following, and Safety require `OPENAI_API_KEY` and GPT-4o availability; cost, rate limits, and judge-version drift affect reproducibility, and only Conversational Features runs fully offline (01-overview.md:8-8, 01-overview.md:47-55).
- **ASR errors propagate into every metric:** all scripts score transcripts, not waveforms, so Whisper mistranscriptions (accents, noise, overlapping speech — the very conditions under test) flow into success/latency/frequency and judge verdicts; the `--asr_cache_file` / incremental-save mechanism means stale caches can also silently persist old transcripts across reruns (01-overview.md:11-11, 01-overview.md:104-111, 01-overview.md:151-159).
- **Unpinned core dependencies and fragmented environments:** `pip install openai whisper torch` carries no version pins and each reference model has its own `envs/` config, so cross-model comparisons risk environment skew unless the evaluator locks versions (01-overview.md:42-46, 01-overview.md:160-160).

## 11. How It Compares to Alternatives

- **VoiceBench:** single-turn spoken-assistant benchmark emphasizing instruction following and robustness; MTR-DuplexBench instead targets multi-round full-duplex interaction (interruptions, pauses, backchannels) with stereo timing metrics.
- **AudioBench:** broad audio-understanding benchmark (speech, sound, music QA); MTR-DuplexBench is narrower — conversational turn-taking behavior of duplex speech models rather than general audio comprehension.
- **AIR-Bench:** speech-foundation-model benchmark across speech tasks; MTR-DuplexBench complements it by scoring interactive dialogue dynamics (latency, backchannel frequency, interruption handling) instead of static task accuracy.
- **SD-Eval (Spoken Dialogue Evaluation):** evaluates spoken dialogue coherence and safety, closest in spirit; MTR-DuplexBench differs in its full-duplex, multi-scenario stereo-audio protocol with explicit scenario encodings and per-channel ASR.

Positioning: MTR-DuplexBench is the interaction-dynamics benchmark among speech evaluation suites — use the general suites for what a model understands, and this repo for how it converses under real-time, full-duplex pressure.

## Appendix: Selected Code Snippets

1. Cloning the distributed data + code bundle (01-overview.md:14-18):

```bash
git lfs install
git clone https://huggingface.co/datasets/Jeff0918/MTR-DuplexBench
```

2. Core dependency install, unpinned (01-overview.md:42-44):

```bash
pip install openai whisper torch
```

3. Loading a scenario encoding (01-overview.md:62-69):

```python
import json

# Example: load a single-scenario encoding
with open("data/Scenarios_encoding/single_scenario/scenario_encoding_smooth.json") as f:
    encoding = json.load(f)
```

4. Dialogue Quality scoring invocation (01-overview.md:80-88):

```bash
cd Eval

python gpt4o_mark_in_turn_GT_condor.py \
  --jsonl_file_path results/dialogue_quality_scores.jsonl \
  --turn_mask_path ../data/Scenarios_encoding/dialogue_quality/semantic_turned_time_v3.jsonl \
  --audio_path path/to/your/model/output/audio/
```
