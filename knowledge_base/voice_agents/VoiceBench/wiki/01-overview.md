[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Overview
**In one sentence:** VoiceBench is a benchmark harness for LLM-based voice assistants that pairs a multi-subset spoken-instruction dataset suite with a three-step generate-then-judge-then-score evaluation flow.
## Key points
- VoiceBench benchmarks LLM-based voice assistants via spoken (and text) instructions, exposing a leaderboard, paper, and Hugging Face dataset from the repo header (README.md:7-13).
- The dataset suite is hosted as `hlt-lab/voicebench` on Hugging Face and loaded with `load_dataset("hlt-lab/voicebench", '<subset>')` (README.md:48-62).
- The suite covers 11 subsets spanning open-ended QA, multiple-choice QA, reference-based QA, multi-turn QA, instruction following, reasoning, and safety, with Google TTS or human audio sources (README.md:66-79).
- Response generation runs via `python main.py --model <name> --data <subset> --split <split> --modality <audio|text>`, writing e.g. `naive-alpacaeval-test-audio.jsonl` (README.md:87-99).
- GPT-based judging with `gpt-4o-mini` via `api_judge.py` applies only to `alpacaeval`, `commoneval`, `wildvoice`, and `sd-qa`, and is skipped for all other subsets (README.md:101-108).
- Final scoring runs via `python evaluate.py --src_file <judged-file> --evaluator <open|qa|ifeval|harm|mcq|bbh>` with a per-subset evaluator mapping (README.md:111-122).
- Setup pins `python=3.10`, `torch==2.1.2` / `torchvision==0.16.2` / `torchaudio==2.1.2` (cu121) plus `xformers==0.0.23 --no-deps` and `requirements.txt` (README.md:37-44).
---
## Setup
Conda environment and pinned dependencies (README.md:37-44):
```shell
conda create -n voicebench python=3.10
conda activate voicebench
pip install torch==2.1.2 torchvision==0.16.2 torchaudio==2.1.2 --index-url https://download.pytorch.org/whl/cu121
pip install xformers==0.0.23 --no-deps
pip install -r requirements.txt
```

## Dataset suite
Data lives at the [VoiceBench Dataset](https://huggingface.co/datasets/hlt-lab/voicebench) and integrates via the Hugging Face `datasets` library (README.md:48-50). Load pattern (README.md:56-62):
```python
from datasets import load_dataset

# Load the VoiceBench dataset
# Available subset: alpacaeval, commoneval, sd-qa, ifeval, advbench, ...
dataset = load_dataset("hlt-lab/voicebench", 'alpacaeval')
```
Available subsets (README.md:66-79):

| Subset          | # Samples | Audio Source |       Task Type       |
|-----------------|:---------:|:------------:|:---------------------:|
| alpacaeval      |    199    |  Google TTS  |     Open-Ended QA     |
| alpacaeval_full |    636    |  Google TTS  |     Open-Ended QA     |
| commoneval      |    200    |    Human     |     Open-Ended QA     |
| wildvoice       |   1,000   |    Human     |     Open-Ended QA     |
| openbookqa      |    455    |  Google TTS  |  Multiple-Choice QA   |
| mmsu            |   3,074   |  Google TTS  |  Multiple-Choice QA   |
| sd-qa           |    553    |    Human     |  Reference-Based QA   |
| mtbench         |    46     |  Google TTS  |     Multi-Turn QA     |
| ifeval          |    345    |  Google TTS  | Instruction Following |
| bbh             |   1,000   |    Human     |       Reasoning       |
| advbench        |    520    |  Google TTS  |        Safety         |

Note: `alpacaeval` contains `helpful_base` and `vicuna` data, while `alpacaeval_full` is the complete data; `alpacaeval_full` is used in the leaderboard (README.md:81).

## Evaluation flow
Three steps: get responses, GPT-4 judging (subset-gated), final scoring (README.md:85-114).
### Step 1: Get the Voice Assistant's Response
```shell
python main.py --model naive --data alpacaeval --split test --modality audio
```
Flags (README.md:91-97):

| Flag | Meaning |
|---|---|
| `--model` | Model for generating responses (e.g. `naive`, `qwen2`, `diva`) |
| `--data` | Dataset subset (e.g. `alpacaeval`, `commoneval`, `sd-qa`) |
| `--split` | Data split; `test` for most sets (`alpacaeval`, `commoneval`, `ifeval`, `advbench`), region code (e.g. `aus`, `usa`) for `sd-qa` |
| `--modality` | `audio` for spoken instructions, `text` for text-based instructions |

Output is saved as e.g. `naive-alpacaeval-test-audio.jsonl` (README.md:99).
### Step 2: Automatic GPT-4 Evaluation
For `alpacaeval`, `commoneval`, `wildvoice`, and `sd-qa` only, scored with `gpt-4o-mini` (README.md:102-108):
```shell
python api_judge.py --src_file naive-alpacaeval-test-audio.jsonl
```
Scores are saved to `result-naive-alpacaeval-test-audio.jsonl` (README.md:106); this step is skipped for all other datasets (README.md:108).
### Step 3: Get the Final Results
```shell
python evaluate.py --src_file result-naive-alpacaeval-test-audio.jsonl --evaluator open
```
Evaluator mapping (README.md:115-122):

| `--evaluator` | Subsets |
|---|---|
| `open` | `alpacaeval`, `commoneval`, `wildvoice` |
| `qa` | `sd-qa` |
| `ifeval` | `ifeval` |
| `harm` | `advbench` |
| `mcq` | `openbookqa`, `mmsu` |
| `bbh` | `bbh` |

## News and Awesome Voice Assistants
News entries record dataset/leaderboard updates from `2024.10.30` through `2026.04.20`, including `wildvoice`, `bbh`, `mmsu`, `openbookqa`/`alpacaeval` expansions and the HalluAudio pointer (README.md:19-27). The `Awesome Voice Assistants` section is a large Title/Date/Code table of external voice-assistant projects (README.md:124-149).

Truncated in chunk: the `Awesome Voice Assistants` table is cut off mid-row at the `Audio Flamingo 3` entry (README.md:149); contents past that point are not covered here.

**Covers:** README.md (project header, News, Setup, Dataset, Evaluation, Awesome Voice Assistants); macro-component pointer to `top-level-files/`
