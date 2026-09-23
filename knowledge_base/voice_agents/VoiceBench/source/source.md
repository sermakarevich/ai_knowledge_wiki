# MatthewCYM/VoiceBench
> PDF/source location: https://github.com/MatthewCYM/VoiceBench
Source: https://github.com/MatthewCYM/VoiceBench
Kind: repo
Fetched: 2026-09-22T14:49:44.408868+00:00
Tool: git-clone

# MatthewCYM/VoiceBench

Commit: 6992cf4fc51d0426c52c4805b5002e0aae49118a

## README

<h1 align="center">VoiceBench: Benchmarking LLM-Based Voice Assistants</h1>

<p align="center">
  <a href="https://matthewcym.github.io/VoiceBench/">🏆 Leaderboard</a> |
  <a href="https://arxiv.org/abs/2410.17196">📄 Paper</a> |
  <a href="https://huggingface.co/datasets/hlt-lab/voicebench">🤗 Data</a>
</p>


> We encourage new result submissions through the [issue tracker](https://github.com/matthewcym/VoiceBench/issues). The leaderboard will be updated accordingly.


## News
* **`2026.04.20`** Check out [HalluAudio](https://github.com/Feiyuzhao25/halluaudio), a comprehensive benchmark for hallucination detection in LALMs.
* **`2025.04.20`** Released `wildvoice`, a crowd-sourced dataset comprising human-recorded speech with diverse accents.
* **`2025.04.12`** Released `bbh`, a crowd-sourced dataset comprising human-recorded speech, for evaluating the reasoning ability of voice assistants. 
* **`2024.12.11`** Updated the VoiceBench Leaderboard to include `mmsu`.
* **`2024.12.10`** Added a curated list of awesome voice assistants.
* **`2024.11.24`** Expanded the test samples in VoiceBench to include `mmsu`, covering 12 diverse domains from `mmlu-pro`.
* **`2024.11.12`** Updated the VoiceBench Leaderboard to include: 1) Mini-Omni2, GPT-4o-Audio, and Whisper-v3+GPT-4o, and 2) multiple-choice QA from OpenBookQA.
* **`2024.10.30`** Expanded the test samples in VoiceBench to include: 1) the complete set of open-ended QA from `alpacaeval`, and 2) multiple-choice QA from `openbookqa`.

## Table of Contents
- [**Setup**](#setup)
- [**Dataset**](#dataset)
- [**Evaluation**](#evaluation)
- [**Awesome Voice Assistants**](#awesome-voice-assistants)
- [**Citation**](#citation)


## Setup
```shell
conda create -n voicebench python=3.10
conda activate voicebench
pip install torch==2.1.2 torchvision==0.16.2 torchaudio==2.1.2 --index-url https://download.pytorch.org/whl/cu121
pip install xformers==0.0.23 --no-deps
pip install -r requirements.txt
```

## Dataset

The data used in this project is available at [VoiceBench Dataset](https://huggingface.co/datasets/hlt-lab/voicebench) hosted on Hugging Face.

You can access it directly via the link and integrate it into your project by using the Hugging Face `datasets` library.

### How to Use the Dataset

To load the dataset in your Python environment:

```python
from datasets import load_dataset

# Load the VoiceBench dataset
# Available subset: alpacaeval, commoneval, sd-qa, ifeval, advbench, ...
dataset = load_dataset("hlt-lab/voicebench", 'alpacaeval')
```

### Available Data

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


**PS**: `alpacaeval` contains `helpful_base` and `vicuna` data, while `alpacaeval_full` is constructed with the complete data. `alpacaeval_full` is used in the leaderboard.


## Evaluation
### Step 1: Get the Voice Assistant's Response
To obtain the responses from the voice assistant model, run the following command:
```shell
python main.py --model naive --data alpacaeval --split test --modality audio
```

**Supported Arguments:**
- `--model`: Specifies the model to use for generating responses. Replace `naive` with the model you want to test (e.g., `qwen2`, `diva`).
- `--data`: Selects the subset of the dataset. Replace `alpacaeval` with other subsets like `commoneval`, `sd-qa`, etc., depending on your evaluation needs.
- `--split`: Chooses the data split to evaluate.
    - For most datasets (`alpacaeval`, `commoneval`, `ifeval`, `advbench`), use `test` as the value.
    - For the `sd-qa` subset, you should provide a region code instead of `test`, such as `aus` for Australia, `usa` for the United States, etc.
- `--modality`: Use `audio` for spoken instructions, `text` for text-based instructions.

This will generate the output and save it to a file named naive-alpacaeval-test-audio.jsonl.

### Step2: Automatic GPT-4 Evaluation
For datasets `alpacaeval`, `commoneval`, `wildvoice`, and `sd-qa`, we use `gpt-4o-mini` to evaluate the responses. Run the following command to get the GPT score:
```shell
python api_judge.py --src_file naive-alpacaeval-test-audio.jsonl
```
The GPT evaluation scores will be saved to `result-naive-alpacaeval-test-audio.jsonl`.

**Note:** This step should be skipped for other datasets, as they are not evaluated using GPT-4.

### Step3: Get the Final Results
To generate the final evaluation results, run:
```shell
python evaluate.py --src_file result-naive-alpacaeval-test-audio.jsonl --evaluator open
```
**Supported Arguments:**
- `--evaluator`: Specifies the evaluator type:
    - Use `open` for `alpacaeval`, `commoneval`, and `wildvoice`.
    - Use `qa` for `sd-qa`.
    - Use `ifeval` for `ifeval`.
    - Use `harm` for `advbench`.
    - Use `mcq` for `openbookqa` and `mmsu`.
    - Use `bbh` for `bbh`.

## Awesome Voice Assistants
| Title                                                                                                                                                                                                                                                                                                                                        |    Date    |                                   Code                                   |
|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:----------:|:------------------------------------------------------------------------:|
| [**Unified Audio Intelligence Without Regressing on Text Intelligence**](https://arxiv.org/abs/2607.05196) | 2026-07-06 | [HF](https://huggingface.co/collections/nvidia/nemotron-labs-audex) |
| [**ParaBridge: Bridging Paralinguistic Perception and Dialogue Behavior in Speech Language Models**](https://arxiv.org/abs/2606.10581) &nbsp; ![Star](https://img.shields.io/github/stars/AmphionTeam/ParaBridge) | 2026-06-09 | [Github](https://github.com/AmphionTeam/ParaBridge) |
| [**Audio Interaction Model**](https://arxiv.org/abs/2606.05121) &nbsp; ![Star](https://img.shields.io/github/stars/xzf-thu/Audio-Interaction) | 2026-06-03 | [Github](https://github.com/xzf-thu/Audio-Interaction) |
| [**Sympatheia: Emotionally Adaptive Voice Assistant with Continuous Affect Conditioning**](https://arxiv.org/abs/2606.00851) &nbsp; ![Star](https://img.shields.io/github/stars/susameddin/sympatheia) | 2026-05-30 | [Github](https://github.com/susameddin/sympatheia) |
| [**Liberating LLM Capabilities in Full-Duplex Speech Models**](https://arxiv.org/abs/2606.07547) &nbsp; ![Star](https://img.shields.io/github/stars/zly-idleness/lws_demo) | 2026-05-04 | [Github](https://github.com/zly-idleness/lws_demo) |
| [**MiniCPM-o 4.5: Towards Real-Time Full-Duplex Omni-Modal Interaction**](https://arxiv.org/abs/2604.27393) &nbsp; ![Star](https://img.shields.io/github/stars/OpenBMB/MiniCPM-V) | 2026-04-30 | [Github](https://github.com/OpenBMB/MiniCPM-V) |
| [**Nemotron 3 Nano Omni: Efficient and Open Multimodal Intelligence**](https://arxiv.org/abs/2604.24954) &nbsp; ![Star](https://img.shields.io/github/stars/NVIDIA-NeMo/Nemotron) | 2026-04-27 | [Github](https://github.com/NVIDIA-NeMo/Nemotron/tree/main/usage-cookbook/Nemotron-3-Nano-Omni) |
| [**Qwen3.5-Omni Technical Report**](https://arxiv.org/abs/2604.15804) | 2026-04-17 | [Demo](https://huggingface.co/spaces/Qwen/Qwen3.5-Omni-Online-Demo) |
| [**VoxMind: An End-to-End Agentic Spoken Dialogue System**](https://arxiv.org/abs/2604.15710) &nbsp; ![Star](https://img.shields.io/github/stars/MM-Speech/VoxMind) | 2026-04-17 | [Github](https://github.com/MM-Speech/VoxMind) |
| [**Resurfacing Paralinguistic Awareness in Large Audio Language Models**](https://arxiv.org/abs/2603.11947) | 2026-03-12 | -- |
| [**DuplexCascade: Full-Duplex Speech-to-Speech Dialogue with VAD-Free Cascaded ASR-LLM-TTS Pipeline and Micro-Turn Optimization**](https://arxiv.org/abs/2603.09180) &nbsp; ![Star](https://img.shields.io/github/stars/sbintuitions/DuplexCascade) | 2026-03-10 | [Github](https://github.com/sbintuitions/DuplexCascade) |
| [**Language-Aware Distillation for Multilingual Instruction-Following Speech LLMs with ASR-Only Supervision**](https://arxiv.org/abs/2603.07025) | 2026-03-07 | -- |
| [**X-OPD: Cross-Modal On-Policy Distillation for Capability Alignment in Speech LLMs**](https://arxiv.org/abs/2603.24596) | 2026-03-06 | -- |
| [**DIFFA-2: A Practical Diffusion Large Language Model for General Audio Understanding**](https://arxiv.org/abs/2601.23161) &nbsp; ![Star](https://img.shields.io/github/stars/NKU-HLT/DIFFA) | 2026-01-30 | [Github](https://github.com/NKU-HLT/DIFFA) |
| [**CORD: Bridging the Audio-Text Reasoning Gap via Weighted On-policy Cross-modal Distillation**](https://arxiv.org/abs/2601.16547) | 2026-01-23 | -- |
| [**AzeroS: Extending LLM to Speech with Self-Generated Instruction-Free Tuning**](https://arxiv.org/abs/2601.06086) &nbsp; ![Star](https://img.shields.io/github/stars/AudenAI/Auden) | 2025-12-31 | [Github](https://github.com/AudenAI/Auden/tree/main/examples/azeros) |
| [**LFM2 Technical Report**](https://arxiv.org/abs/2511.23404) &nbsp; ![Star](https://img.shields.io/github/stars/Liquid4All/liquid-audio) | 2025-11-28 | [Github](https://github.com/Liquid4All/liquid-audio) |
| [**LongCat-Flash-Omni Technical Report**](https://arxiv.org/abs/2511.00279) &nbsp; ![Star](https://img.shields.io/github/stars/meituan-longcat/LongCat-Flash-Omni) | 2025-10-31 | [Github](https://github.com/meituan-longcat/LongCat-Flash-Omni) |
| [**Empathy Omni: Enabling Empathetic Speech Response Generation through Large Language Models**](https://arxiv.org/abs/2508.18655) &nbsp; ![Star](https://img.shields.io/github/stars/W311411/Empathy-Omni) | 2025-08-26 | [Github](https://github.com/W311411/Empathy-Omni) |
| [**OSUM-EChat: Enhancing End-to-End Empathetic Spoken Chatbot via Understanding-Driven Spoken Dialogue**](https://arxiv.org/abs/2508.09600) &nbsp; ![Star](https://img.shields.io/github/stars/ASLP-lab/OSUM)                                                                                                                                | 2025-08-13 |             [Github](https://github.com/ASLP-lab/OSUM)                   |
| [**DIFFA: Large Language Diffusion Models Can Listen and Understand**](https://arxiv.org/abs/2507.18452) &nbsp; ![Star](https://img.shields.io/github/stars/NKU-HLT/DIFFA)                                                                                                                                                                   | 2025-07-24 |             [Github](https://github.com/NKU-HLT/DIFFA)                   |
| [**Voxtral**](https://arxiv.org/abs/2507.13264)                                                                                                                                 | 2025-07-17 | [HF](https://huggingface.co/mistralai/Voxtral-Small-24B-2507) |
| [**Audio Flamingo 3: Advancing Audio Intelligence with Fully Open Large Audio Languag

... (truncated, 20415 more characters)

## Top-level layout

- .gitignore (~162 lines)
- api_judge.py (~92 lines)
- docs/ (dir, 1 files, ~655 lines)
- evaluate.py (~22 lines)
- LICENSE (~201 lines)
- main.py (~56 lines)
- README.md (~203 lines)
- requirements.txt (~35 lines)
- src/ (dir, 504 files, ~205889 lines)

