> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Overview
**In one sentence:** MTR-DuplexBench is an ACL 2026 Findings benchmark that evaluates full-duplex speech language models on multi-round conversations by running a scenario-encoding → stereo-audio inference → Eval-script scoring pipeline.
## Key points
- MTR-DuplexBench was accepted by ACL 2026 Findings and distributes paper, HuggingFace dataset, and evaluation scripts for user-model evaluation (01-overview.md:9-13).
- The cloned tree has three top-level areas: `code/` evaluation scripts under `Eval/`, `data/` evaluation data, and `envs/` environment configurations (01-overview.md:30-51).
- Evaluation covers four dimensions — Dialogue Quality, Conversational Features (single/multi scenario), Instruction Following, and Safety — each with its own scripts, audio format, and judge (01-overview.md:67-75).
- GPT-4o is the LLM judge for Dialogue Quality, Instruction Following, and Safety, requiring `OPENAI_API_KEY` to be set (01-overview.md:61-61).
- The standard workflow is three steps: read JSON scenario encodings from `Scenarios_encoding/`, run own-model inference to stereo audio, then run `Eval/` scripts that handle Whisper ASR plus metric computation (01-overview.md:81-85, 01-overview.md:88-90, 01-overview.md:110-117, 01-overview.md:119-121).
- Model output must be stereo audio with left channel = user audio and right channel = model audio, following per-dimension naming conventions (01-overview.md:112-117).
- Whisper-based `asr_incremental_save.py` is the shared ASR utility with independent left/right transcription, incremental saving, and JSON caching (01-overview.md:275-281).
---
## Repo layout
Source distribution is cloned from HuggingFace including data and code (01-overview.md:19-26):
```bash
git lfs install
git clone https://huggingface.co/datasets/Jeff0918/MTR-DuplexBench
```
Expected structure (01-overview.md:28-51):
```
MTR-DuplexBench/
├── code/                             # This directory — evaluation scripts
│   └── Eval/
│       ├── asr_incremental_save.py
│       ├── eval_1_scenario.py
│       ├── eval_2_scenarios.py
│       ├── eval_3_scenarios.py
│       ├── eval_4_scenarios.py
│       ├── eval_single_scenario_background.py
│       ├── eval_single_scenario_pause_handling.py
│       ├── gpt4o_mark_in_turn_GT_condor.py
│       ├── instruction_following_evaluation.py
│       └── safety_evaluation.py
├── data/                             # Evaluation data
│   ├── Conversational_Features/
│   ├── Instruction_Following/
│   ├── Safety/
│   ├── Dialogue_Quality/
│   └── Scenarios_encoding/
└── envs/                             # Environment configurations
```
Core dependencies install directly (01-overview.md:53-58):
```bash
pip install openai whisper torch
```
Per-model conda/requirements configs live in `envs/` (01-overview.md:53-55, 01-overview.md:293-295).
## Evaluation dimensions
Four dimensions with distinct scripts, audio formats, and judges (01-overview.md:65-75):
| Dimension | Evaluation Script(s) | Audio Format | LLM Judge |
| :--- | :--- | :--- | :--- |
| **Dialogue Quality** | `gpt4o_mark_in_turn_GT_condor.py` | MP3 | GPT-4o |
| **Conversational Features** (Single Scenario) | `eval_single_scenario_*.py`, `eval_1/2_scenario.py` | WAV | — |
| **Conversational Features** (Multi Scenario) | `eval_1/2/3/4_scenarios.py` | WAV | — |
| **Instruction Following** | `instruction_following_evaluation.py` | WAV | GPT-4o |
| **Safety** | `safety_evaluation.py` | WAV | GPT-4o |
## Three-step pipeline
General workflow (01-overview.md:81-86):
```
1. Read scenario encoding  →  2. Model inference  →  3. Run evaluation code
   (Scenarios_encoding/)       (your own pipeline)     (Eval/ scripts)
```
Scenario encodings are JSON files defining dialogue structure, turn-taking patterns, and timing (01-overview.md:88-90). Example load (01-overview.md:92-98):
```python
import json

# Example: load a single-scenario encoding
with open("data/Scenarios_encoding/single_scenario/scenario_encoding_smooth.json") as f:
    encoding = json.load(f)
```
Encoding files by dimension (01-overview.md:100-108):
| Dimension | Encoding Path |
| :--- | :--- |
| Conversational Features (single) | `Scenarios_encoding/single_scenario/scenario_encoding_{smooth,interruption,pause,background}.json` |
| Conversational Features (multi) | `Scenarios_encoding/multi_scenarios/scenario_encoding_{1,2,3,4}.json` |
| Instruction Following | `Scenarios_encoding/instruction_following/scenario_encoding_{smooth,interruption}.json` |
| Safety | `Scenarios_encoding/safety/scenario_encoding_{smooth,interruption}.json` |
| Dialogue Quality | `Scenarios_encoding/dialogue_quality/semantic_turned_time_v3.jsonl` |
Inference must output stereo audio: left channel user, right channel model (01-overview.md:110-117). Evaluation scripts then run Whisper ASR and metric computation automatically (01-overview.md:119-121).
## Dialogue Quality
Scores whether model turns are semantically meaningful on a 0–5 scale using GPT-4o (01-overview.md:127-129). Inference input is `data/Dialogue_Quality/*.mp3` plus turn boundaries in `data/Scenarios_encoding/dialogue_quality/semantic_turned_time_v3.jsonl`; output is stereo MP3 files (left=user, right=model) (01-overview.md:131-135). Run (01-overview.md:139-146):
```bash
cd Eval

python gpt4o_mark_in_turn_GT_condor.py \
  --jsonl_file_path results/dialogue_quality_scores.jsonl \
  --turn_mask_path ../data/Scenarios_encoding/dialogue_quality/semantic_turned_time_v3.jsonl \
  --audio_path path/to/your/model/output/audio/
```
Output is a JSONL file with per-turn scores and a printed average model turn score (01-overview.md:148-148). Exact flags are `--jsonl_file_path`, `--turn_mask_path`, `--audio_path` (01-overview.md:142-145).
## Conversational Features
Evaluates turn-taking behavior including latency, backchannel frequency, and correct handling of interruptions, pauses, and background noise (01-overview.md:152-154). Input audio is `data/Conversational_Features/original/*.wav` or `data/Conversational_Features/woPAUSE/*.wav` with single- or multi-scenario encodings; output is stereo WAV (left=user, right=model) (01-overview.md:156-160). Single-scenario script selection (01-overview.md:162-170):
| Scenario | Script | Metrics |
| :--- | :--- | :--- |
| smooth-turntaking | `eval_1_scenario.py` | success, latency, frequency |
| pause-handling | `eval_single_scenario_pause_handling.py` | success, latency, frequency |
| background | `eval_single_scenario_background.py` | success, latency, frequency |
Multi-scenario scripts form a layered hierarchy delegating to lower ones (01-overview.md:174-181):
| # Scenarios | Script | Description |
| :--- | :--- | :--- |
| 1 | `eval_1_scenario.py` | Single: smooth-turntaking |
| 2 | `eval_2_scenarios.py` | Two: e.g., smooth-turntaking + interruption |
| 3 | `eval_3_scenarios.py` | Three: e.g., smooth-turntaking + pause-handling + background |
| 4 | `eval_4_scenarios.py` | Four: all scenarios combined |
Usage pattern is library-style: run ASR via `asr_incremental_save.py`, load per-dialogue encodings, call `eval_N_scenarios()` with ASR segments and timestamps, aggregate success/latency/frequency (01-overview.md:183-188). ASR step (01-overview.md:190-196):
```bash
# Step 1: Run ASR on model output audio
python asr_incremental_save.py \
  --audio_dir path/to/your/output/audio/ \
  --output_file results/asr_results.json \
  --user_channel left
```
## Instruction Following
Evaluates whether the model follows user instructions in audio conversations with GPT-4o as binary (0/1) judge (01-overview.md:202-204). Inputs are `data/Instruction_Following/audios/*.wav`, `data/Instruction_Following/instruction_following_data.json`, and `Scenarios_encoding/instruction_following/`; outputs are stereo WAV files named `dialogue_instruction_following_*_round_*_*.wav` (01-overview.md:206-211). Run (01-overview.md:215-222):
```bash
cd Eval

python instruction_following_evaluation.py \
  --instruction_following_output_dir path/to/your/output/audio/ \
  --output_file results/instruction_following_results.json \
  --user_channel left
```
Optional arguments (01-overview.md:224-232):
| Argument | Default | Description |
| :--- | :--- | :--- |
| `--asr_cache_file` | None | Path to ASR cache file for incremental processing |
| `--round_start_json` | None | JSON file with per-round start timestamps |
| `--max_round` | 10 | Maximum round number for analysis |
| `--analyze_only` | False | Skip evaluation, only analyze existing results |
| `--analysis_output` | None | Output file for analysis report |
Output is JSON with per-round scores and an overall following rate (01-overview.md:234-234).
## Safety
Evaluates whether responses to harmful user requests are safe with GPT-4o as binary judge (0=safe, 1=unsafe) (01-overview.md:238-240). Inputs are `data/Safety/audios/*.wav`, `data/Safety/safety_data.json`, and `Scenarios_encoding/safety/`; outputs are stereo WAV files named `dialogue_safety_*_round_*_*.wav` (01-overview.md:242-247). Run (01-overview.md:251-258):
```bash
cd Eval

python safety_evaluation.py \
  --safety_output_dir path/to/your/output/audio/ \
  --output_file results/safety_results.json \
  --user_channel left
```
Optional arguments (01-overview.md:260-269):
| Argument | Default | Description |
| :--- | :--- | :--- |
| `--asr_cache_file` | None | Path to ASR cache file for incremental processing |
| `--cuda_device` | 0 | CUDA device ID for ASR |
| `--round_start_json` | None | JSON file with per-round start timestamps |
| `--max_round` | 10 | Maximum round number for analysis |
| `--analyze_only` | False | Skip evaluation, only analyze existing results |
| `--analysis_output` | None | Output file for analysis report |
Output is JSON with per-round safety scores and safe/unsafe rate statistics (01-overview.md:271-271).
## ASR utility and environments
`asr_incremental_save.py` supports independent left/right channel transcription, incremental result saving, and JSON-based caching (01-overview.md:275-281). Invocation (01-overview.md:283-289):
```bash
python asr_incremental_save.py \
  --audio_dir path/to/audio/ \
  --output_file results/asr_results.json \
  --user_channel left \
  --cache_file results/asr_cache.json
```
`envs/` holds conda YAML plus requirements for specific models (01-overview.md:293-303):
| Environment | Model |
| :--- | :--- |
| `bailing/` | Bailing |
| `freeze_and_eval/` | Frozen model evaluation |
| `moshi/` | Moshi |
| `vocalnet/` | VocalNet |
Contact is via GitHub issues / HuggingFace Community or `zhanghe_0918@163.com` / `wenqian.cui@link.cuhk.edu.hk` (01-overview.md:306-311). No truncated files were noted in the chunk; the chunk reports no component directories beyond this overview (01-overview.md:326-328).
**Covers:** `README` (Quick Start, Evaluation Overview, Evaluation Pipeline, Per-Dimension Guide, ASR Utility, Environment Configurations, Contact, Citation); repo layout `code/Eval/`, `data/`, `envs/`
