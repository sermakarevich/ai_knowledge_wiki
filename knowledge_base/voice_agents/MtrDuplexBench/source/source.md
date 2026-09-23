# ZhangHe0918/MTR-DuplexBench
> PDF location (no source.pdf bundled, under 2 MB rule): https://github.com/ZhangHe0918/MTR-DuplexBench
Source: https://github.com/ZhangHe0918/MTR-DuplexBench
Kind: repo
Fetched: 2026-09-22T14:24:26.344007+00:00
Tool: git-clone

# ZhangHe0918/MTR-DuplexBench

Commit: 6d7c125db26822c8309cb9f73c87a889e10b6451

## README

# MTR-DuplexBench: Towards a Comprehensive Evaluation of Multi-Round Conversations for Full-Duplex Speech Language Models

🎉🎉 **MTR-DuplexBench has been accepted by ACL 2026 Findings!** 

 📄 [Paper](https://arxiv.org/abs/2511.10262) | 🤗 [HuggingFace Dataset](https://huggingface.co/datasets/Jeff0918/MTR-DuplexBench)

This directory contains the evaluation scripts for MTR-DuplexBench. Follow the guide below to set up and run evaluations for your own models.

---

## Quick Start

### 1. Download Data and Code

Clone the dataset from HuggingFace, which includes both the evaluation data and the code:

```bash
git lfs install
git clone https://huggingface.co/datasets/Jeff0918/MTR-DuplexBench
```

After cloning, you should have the following structure:

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

### 2. Install Dependencies

Each model's environment configuration is provided in `envs/`. You can also install the core dependencies directly:

```bash
pip install openai whisper torch
```

> **Note:** GPT-4o is used as the LLM judge for Dialogue Quality, Instruction Following, and Safety evaluations. Make sure your `OPENAI_API_KEY` environment variable is set.

---

## Evaluation Overview

MTR-DuplexBench evaluates models across four dimensions. Each dimension uses different evaluation scripts and requires a different inference pipeline:

| Dimension | Evaluation Script(s) | Audio Format | LLM Judge |
| :--- | :--- | :--- | :--- |
| **Dialogue Quality** | `gpt4o_mark_in_turn_GT_condor.py` | MP3 | GPT-4o |
| **Conversational Features** (Single Scenario) | `eval_single_scenario_*.py`, `eval_1/2_scenario.py` | WAV | — |
| **Conversational Features** (Multi Scenario) | `eval_1/2/3/4_scenarios.py` | WAV | — |
| **Instruction Following** | `instruction_following_evaluation.py` | WAV | GPT-4o |
| **Safety** | `safety_evaluation.py` | WAV | GPT-4o |

---

## Evaluation Pipeline

The general workflow for evaluating your model consists of three steps:

```
1. Read scenario encoding  →  2. Model inference  →  3. Run evaluation code
   (Scenarios_encoding/)       (your own pipeline)     (Eval/ scripts)
```

### Step 1: Read Scenario Encoding

Each evaluation dimension has corresponding scenario encoding files under `data/Scenarios_encoding/`. These JSON files define the dialogue structure, turn-taking patterns, and timing information that your model needs to follow during inference.

```python
import json

# Example: load a single-scenario encoding
with open("data/Scenarios_encoding/single_scenario/scenario_encoding_smooth.json") as f:
    encoding = json.load(f)
```

**Encoding files by dimension:**

| Dimension | Encoding Path |
| :--- | :--- |
| Conversational Features (single) | `Scenarios_encoding/single_scenario/scenario_encoding_{smooth,interruption,pause,background}.json` |
| Conversational Features (multi) | `Scenarios_encoding/multi_scenarios/scenario_encoding_{1,2,3,4}.json` |
| Instruction Following | `Scenarios_encoding/instruction_following/scenario_encoding_{smooth,interruption}.json` |
| Safety | `Scenarios_encoding/safety/scenario_encoding_{smooth,interruption}.json` |
| Dialogue Quality | `Scenarios_encoding/dialogue_quality/semantic_turned_time_v3.jsonl` |

### Step 2: Model Inference

Build your own inference pipeline that feeds the audio and scenario information into the model you want to evaluate. The key requirement is that the model's output must be saved as **stereo audio**:

- **Left channel**: User audio
- **Right channel**: Model audio

Save the output audio files following the naming conventions expected by the evaluation scripts (see details per dimension below).

### Step 3: Run Evaluation

After inference, run the corresponding evaluation script on the output audio. The scripts handle ASR transcription (via Whisper) and metric computation automatically.

---

## Per-Dimension Guide

### 1. Dialogue Quality

Evaluates whether model turns are semantically meaningful on a 0–5 scale using GPT-4o.

**Inference input:**
- Source audio: `data/Dialogue_Quality/*.mp3`
- Turn boundaries: `data/Scenarios_encoding/dialogue_quality/semantic_turned_time_v3.jsonl`

**Inference output:** Stereo audio files (MP3, left=user, right=model) from your model.

**Run evaluation:**

```bash
cd Eval

python gpt4o_mark_in_turn_GT_condor.py \
  --jsonl_file_path results/dialogue_quality_scores.jsonl \
  --turn_mask_path ../data/Scenarios_encoding/dialogue_quality/semantic_turned_time_v3.jsonl \
  --audio_path path/to/your/model/output/audio/
```

**Output:** JSONL file with per-turn scores and a printed average model turn score.

---

### 2. Conversational Features

Evaluates turn-taking behavior including latency, backchannel frequency, and whether the model correctly handles conversational scenarios (interruptions, pauses, background noise).

**Inference input:**
- Source audio: `data/Conversational_Features/original/*.wav` or `data/Conversational_Features/woPAUSE/*.wav`
- Scenario encoding: `data/Scenarios_encoding/single_scenario/` or `data/Scenarios_encoding/multi_scenarios/`

**Inference output:** Stereo WAV files (left=user, right=model).

#### Single Scenario

Choose the script based on the scenario type:

| Scenario | Script | Metrics |
| :--- | :--- | :--- |
| smooth-turntaking | `eval_1_scenario.py` | success, latency, frequency |
| pause-handling | `eval_single_scenario_pause_handling.py` | success, latency, frequency |
| background | `eval_single_scenario_background.py` | success, latency, frequency |

#### Multi Scenarios

Scripts form a layered hierarchy — higher-numbered scripts delegate to lower ones:

| # Scenarios | Script | Description |
| :--- | :--- | :--- |
| 1 | `eval_1_scenario.py` | Single: smooth-turntaking |
| 2 | `eval_2_scenarios.py` | Two: e.g., smooth-turntaking + interruption |
| 3 | `eval_3_scenarios.py` | Three: e.g., smooth-turntaking + pause-handling + background |
| 4 | `eval_4_scenarios.py` | Four: all scenarios combined |

**Usage pattern:** These scripts are library modules. You typically write a runner script that:

1. Runs ASR on your output audio using `asr_incremental_save.py`
2. Loads the scenario encoding for each dialogue
3. Calls the appropriate `eval_N_scenarios()` function with the ASR segments and timestamps
4. Aggregates success, latency, and frequency metrics

```bash
# Step 1: Run ASR on model output audio
python asr_incremental_save.py \
  --audio_dir path/to/your/output/audio/ \
  --output_file results/asr_results.json \
  --user_channel left
```

Then use the ASR results and scenario encodings as input to the `eval_*_scenarios()` functions programmatically.

---

### 3. Instruction Following

Evaluates whether the model follows user instructions in audio conversations. Uses GPT-4o as a binary (0/1) judge.

**Inference input:**
- Source audio: `data/Instruction_Following/audios/*.wav`
- Dialogue metadata: `data/Instruction_Following/instruction_following_data.json`
- Scenario encoding: `data/Scenarios_encoding/instruction_following/`

**Inference output:** Stereo WAV files named `dialogue_instruction_following_*_round_*_*.wav` (left=user, right=model).

**Run evaluation:**

```bash
cd Eval

python instruction_following_evaluation.py \
  --instruction_following_output_dir path/to/your/output/audio/ \
  --output_file results/instruction_following_results.json \
  --user_channel left
```

**Optional arguments:**

| Argument | Default | Description |
| :--- | :--- | :--- |
| `--asr_cache_file` | None | Path to ASR cache file for incremental processing |
| `--round_start_json` | None | JSON file with per-round start timestamps |
| `--max_round` | 10 | Maximum round number for analysis |
| `--analyze_only` | False | Skip evaluation, only analyze existing results |
| `--analysis_output` | None | Output file for analysis report |

**Output:** JSON file with per-round instruction following scores and an overall following rate.

---

### 4. Safety

Evaluates whether model responses to harmful user requests are safe. Uses GPT-4o as a binary judge (0=safe, 1=unsafe).

**Inference input:**
- Source audio: `data/Safety/audios/*.wav`
- Dialogue metadata: `data/Safety/safety_data.json`
- Scenario encoding: `data/Scenarios_encoding/safety/`

**Inference output:** Stereo WAV files named `dialogue_safety_*_round_*_*.wav` (left=user, right=model).

**Run evaluation:**

```bash
cd Eval

python safety_evaluation.py \
  --safety_output_dir path/to/your/output/audio/ \
  --output_file results/safety_results.json \
  --user_channel left
```

**Optional arguments:**

| Argument | Default | Description |
| :--- | :--- | :--- |
| `--asr_cache_file` | None | Path to ASR cache file for incremental processing |
| `--cuda_device` | 0 | CUDA device ID for ASR |
| `--round_start_json` | None | JSON file with per-round start timestamps |
| `--max_round` | 10 | Maximum round number for analysis |
| `--analyze_only` | False | Skip evaluation, only analyze existing results |
| `--analysis_output` | None | Output file for analysis report |

**Output:** JSON file with per-round safety scores and safe/unsafe rate statistics.

---

## ASR Utility

`asr_incremental_save.py` provides Whisper-based ASR for stereo audio files and is used by all evaluation dimensions. It supports:

- Independent left/right channel transcription
- Incremental result saving (avoids re-computation on reruns)
- JSON-based caching

```bash
python asr_incremental_save.py \
  --audio_dir path/to/audio/ \
  --output_file results/asr_results.json \
  --user_channel left \
  --cache_file results/asr_cache.json
```

---

## Environment Configurations

The `envs/` directory contains conda environment YAML and requirements files for evaluating specific models:

| Environment | Model |
| :--- | :--- |
| `bailing/` | Bailing |
| `freeze_and_eval/` | Frozen model evaluation |
| `moshi/` | Moshi |
| `vocalnet/` | VocalNet |

---

## Contact

If you have any questions, feel free to reach out through the following channels:

- Open an issue on [GitHub](https://github.com/ZhangHe0918/MTR-DuplexBench/issues) or start a discussion on [HuggingFace Community](https://huggingface.co/datasets/Jeff0918/MTR-DuplexBench)
- Email: zhanghe_0918@163.com or wenqian.cui@link.cuhk.edu.hk

---

## Citation

```bibtex
@inproceedings{mtr_duplexbench_2026,
  title={MTR-DuplexBench: A Comprehensive Audio Dataset for Multi-Turn Dialogue Evaluation},
  author={He Zhang, Wenqian Cui, Haoning Xu, Xiao-Hui Li, Lei Zhu, Haoli Bai, Irwin King, Shaohua Ma},
  booktitle={Proceedings of the 60th Annual Meeting of the Association for Computational Linguistics (ACL)},
  year={2026}
}
```


## Top-level layout

- envs/ (dir, 8 files, ~1963 lines)
- Eval/ (dir, 10 files, ~2281 lines)
- LICENSE (~201 lines)
- README.md (~318 lines)

