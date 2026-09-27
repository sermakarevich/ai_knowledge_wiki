> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Overview
**In one sentence:** TurnGuide is an end-to-end full-duplex speech language model that generates coherent, meaningful full-duplex dialogues via dynamic turn-level text-speech interleaving, released with an inference demo and Fisher/Candor test splits for benchmarking.
## Key points
- TurnGuide introduces an end-to-end full-duplex speech language model for coherent, meaningful full-duplex dialogues (README.md:21).
- The initial release provides test splits from the Fisher and Candor datasets to support fair benchmarking (README.md:21).
- The repository includes the TurnGuide inference demo plus GLM-4-Voice code modules needed to run it (README.md:25).
- The inference stack consists of `turnguide_inference.py`, `turnguide_inference_reproducible.py`, `flow_inference.py`, `speech_tokenizer/`, `cosyvoice/`, and `third_party/Matcha-TTS/` (README.md:27-29).
- Model weights are not included; the GLM-4-Voice decoder must be downloaded separately and model paths passed explicitly (README.md:31).
- Two TurnGuide checkpoints differ only in text:speech token loss ratio — `qqjz/turnguide_loss_2_1` (2:1) versus `qqjz/turnguide_loss_3_1` (3:1) — selectable via `--model-path` (README.md:35-45).
- The tested runtime is Python 3.10 with PyTorch 2.5.0, torchaudio 2.5.0, CUDA 12.1, and transformers 4.44.1 (README.md:49-70).
- Inference runs on mono user-audio WAV files, exemplified by `examples/audio/fe_03_05844_first_2min_left.wav`, with outputs written to `--output-dir` (README.md:84-94).
---
## Purpose and status
TurnGuide is described as (README.md:17-21):
> Github repository for paper: [TurnGuide: Enhancing Meaningful Full Duplex Spoken Interactions via Dynamic Turn-Level Text-Speech Interleaving](https://arxiv.org/abs/2508.07375)
> This work introduces an end-to-end full-duplex speech language model and strengthens its capabilities to generate coherent, meaningful full duplex dialogues. As an initial release, we provide the test splits from the Fisher and Candor datasets to support fair and straightforward benchmarking for future research.

Status and links (README.md:13-19):
- Accepted to the Interspeech 2026 Long Paper Track (README.md:15).
- Demo: `https://dreamtheater123.github.io/TurnGuide-Demo/` (README.md:19).
- Paper: `https://arxiv.org/abs/2508.07375` (README.md:17).

## Inference demo and checkpoints
Repository inference contents (README.md:25-29):
- `turnguide_inference.py`: the current TurnGuide inference script.
- `turnguide_inference_reproducible.py`: a legacy/reproducible inference variant.
- `flow_inference.py`, `speech_tokenizer/`, `cosyvoice/`, and `third_party/Matcha-TTS/`: supporting code from GLM-4-Voice and its decoder stack.

Model assets — weights not included (README.md:31-38):

| Asset | Identifier / path (README.md:35-38) |
|---|---|
| TurnGuide checkpoint, loss ratio 2:1 | `qqjz/turnguide_loss_2_1` |
| TurnGuide checkpoint, loss ratio 3:1 | `qqjz/turnguide_loss_3_1` |
| GLM-4-Voice tokenizer | `zai-org/glm-4-voice-tokenizer` |
| GLM-4-Voice decoder | `zai-org/glm-4-voice-decoder` |

Checkpoint selection (README.md:40-45):
> The two TurnGuide checkpoints differ only in the training loss ratio between text tokens and speech tokens:
> - `qqjz/turnguide_loss_2_1`: text:speech token loss ratio = 2:1
> - `qqjz/turnguide_loss_3_1`: text:speech token loss ratio = 3:1
> Both checkpoints can be used with the same inference script by changing `--model-path`.

## Environment and runtime
Recommended setup (README.md:49-54):
```bash
conda env create -f environment.yml
conda activate turnguide
```
The recommended environment is exported from the tested `torch250cu121` setup and uses Python 3.10, PyTorch 2.5.0, torchaudio 2.5.0, and CUDA 12.1 (README.md:49).

Environment notes (README.md:56):
- Pins `mkl=2021.4.0` because newer MKL builds can break PyTorch 2.5.0 imports with an `iJIT_NotifyEvent` symbol error.
- Includes `tiktoken` for the TurnGuide tokenizer remote code.
- Includes `ruamel.yaml==0.18.6` for GLM-4-Voice decoder config loading through HyperPyYAML.

Version check (README.md:60-71):
```bash
python -c "import torch, torchaudio, transformers; print(torch.__version__); print(torch.version.cuda); print(torchaudio.__version__); print(transformers.__version__); print(torch.cuda.is_available())"
```
Expected core versions:

| Package | Expected version (README.md:66-71) |
|---|---|
| torch | 2.5.0 |
| CUDA | 12.1 |
| torchaudio | 2.5.0 |
| transformers | 4.44.1 |

Pip-only alternative when a CUDA 12.1 PyTorch environment already exists (README.md:73-77):
```bash
pip install -r requirements.txt
```

## Run inference
Command (README.md:82-90):
```bash
git clone https://huggingface.co/zai-org/glm-4-voice-decoder

python turnguide_inference.py \
  --input-audio examples/audio/fe_03_05844_first_2min_left.wav \
  --model-path qqjz/turnguide_loss_2_1 \
  --tokenizer-path zai-org/glm-4-voice-tokenizer \
  --flow-path ./glm-4-voice-decoder \
  --output-dir ./turnguide_demo_output
```

| Flag | Value in example (README.md:84-90) |
|---|---|
| `--input-audio` | `examples/audio/fe_03_05844_first_2min_left.wav` |
| `--model-path` | `qqjz/turnguide_loss_2_1` |
| `--tokenizer-path` | `zai-org/glm-4-voice-tokenizer` |
| `--flow-path` | `./glm-4-voice-decoder` |
| `--output-dir` | `./turnguide_demo_output` |

Notes (README.md:92-94):
- To use the 3:1 checkpoint, replace `--model-path qqjz/turnguide_loss_2_1` with `--model-path qqjz/turnguide_loss_3_1`.
- A local checkpoint directory can also be passed to `--model-path`.
- The repository includes `examples/audio/fe_03_05844_first_2min_left.wav` as example input; it can be replaced with any mono user-audio WAV file.

## Data
Examples (README.md:98-105):
- Fisher: `fe_03_11632_60_180.wav`
  - ID: `fe_03_11632`
  - Time segment: 60-180s
- Candor: `46f8e9b8-f80a-48cf-90a0-2e29908202c0_420.0_540.0.wav`
  - ID: `46f8e9b8-f80a-48cf-90a0-2e29908202c0`
  - Time segment: 420-540s

Full datasets must be downloaded separately: Fisher from `https://catalog.ldc.upenn.edu/LDC2004S13` and Candor from `https://guscooney.com/candor-dataset/` (README.md:107).

## Acknowledgements and citation
- This code release builds on [GLM-4-Voice](https://github.com/THUDM/GLM-4-Voice) (README.md:111).
- Included GLM-4-Voice code is licensed under Apache-2.0; GLM-4-Voice model weights are governed by their own model license and must be downloaded separately (README.md:111).

Citation (README.md:115-122):
```bibtex
@article{turnguide2026,
  title={TurnGuide: Enhancing Meaningful Full Duplex Spoken Interactions via Dynamic Turn-Level Text-Speech Interleaving},
  author={Cui, Wenqian and Zhu, Lei and Li, Xiao-Hui and Guo, Zhihan and Bai, Haoli and Hou, Lu and King, Irwin},
  journal={arXiv preprint arXiv:2508.07375},
  year={2026}
}
```

**Covers:** README.md (repo overview, inference demo, checkpoints, environment, inference command, data, license/citation); macro-component marker `top-level-files/` deferred to `02-top-level-files.md`
