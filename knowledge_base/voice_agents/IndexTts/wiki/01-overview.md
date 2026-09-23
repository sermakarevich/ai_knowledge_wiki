> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Overview
**In one sentence:** IndexTTS is a zero-shot text-to-speech system that clones a voice from a single reference audio clip, with the latest IndexTTS-2.5 release adding multilingual and fine-grained controllable synthesis (README.md:24-28).
## Key points
- IndexTTS performs zero-shot voice cloning from a single reference audio clip, positioned as an industrial-level controllable and efficient TTS system (README.md:14-24).
- IndexTTS-2.5 supports Chinese, English, Japanese, Spanish and Arabic, with fine-grained emotion control, speaking-speed control, pronunciation control (Pinyin / CMU phonemes / Japanese Kana), and faster inference than IndexTTS-2 (README.md:25-28).
- The repo maintains four released model lines — IndexTTS, IndexTTS-1.5, IndexTTS-2, IndexTTS-2.5 — each with demos, papers, and ModelScope/HuggingFace distributions (README.md:32-39).
- IndexTTS-2.5 (2026/08/10) adds cross-lingual and timbre-emotion disentanglement, improved Pinyin/CMU/Kana controllability, `duration_factor` speed control (0.5x–2.0x duration), and vLLM production deployment (README.md:43-47).
- Installation is managed with `uv` (`uv sync --all-extras`), models are fetched via `huggingface-cli` / `modelscope` into `checkpoints` / `checkpoints_2`, and GPU setup is diagnosed with `tools/gpu_check.py` (README.md:85-95, README.md:129-151, README.md:170-172).
- Daily use has three paths: WebUI (`uv run webui.py`, browser at `http://127.0.0.1:7860`), production serving via the vLLM recipe, and Python API (`indextts/infer_v2.py`, `indextts/infer_v2_5.py`) with `spk_audio_prompt`, `emo_audio_prompt`, `emo_alpha`, and `lang` parameters (README.md:178-184, README.md:209-218, README.md:240-258).
- Emotion control supports a separate emotional reference audio plus `emo_alpha` intensity (range `0.0-1.0`, default `1.0`), or an 8-float emotion vector in the order `[happy, angry, sad, afraid, disgusted, melancholic, surprised, calm]` (README.md:272-291).
---
## Model Zoo
Four model generations are listed with demo, paper, ModelScope, and HuggingFace links (README.md:32-39):

| Model | Demos | Paper | ModelScope | HuggingFace |
| :--- | :---: | :---: | :---: | :---: |
| **IndexTTS-2.5** | Demo page, ModelScope Studio, HuggingFace Space | arXiv 2601.03888 | IndexTeam/IndexTTS-2.5 | IndexTeam/IndexTTS-2.5 |
| **IndexTTS-2** | Demo page | arXiv 2506.21619 | IndexTeam/IndexTTS-2 | IndexTeam/IndexTTS-2 |
| **IndexTTS-1.5** | Demo page | arXiv 2502.05512 | IndexTeam/IndexTTS-1.5 | IndexTeam/IndexTTS-1.5 |
| **IndexTTS** | Demo page | arXiv 2502.05512 | IndexTeam/Index-TTS | IndexTeam/Index-TTS |

## Releases and Demos
Release history from the News section (README.md:41-53):
- `2026/08/10` — IndexTTS-2.5: five languages, faster inference than IndexTTS-2, Pinyin/CMU/Kana controllability, `duration_factor` speaking-speed control, vLLM deployment.
- `2025/09/08` — IndexTTS-2: first autoregressive TTS model with precise synthesis duration control (controllable and uncontrollable modes, not yet enabled in that release) plus multi-modality emotion control.
- `2025/05/14` — IndexTTS-1.5: stability and English performance improvements.
- `2025/03/25` — IndexTTS-1.0: model weights and inference code.
- `2025/02/12` — paper submitted to arXiv; demos and test sets released.

Video demos for IndexTTS-2.5 and IndexTTS-2 are linked via bilibili covers (README.md:55-67).

## Getting Started
Prerequisites — install `git`, then clone (README.md:71-78):
```bash
git clone https://github.com/index-tts/index-tts.git && cd index-tts
```
Example audio is downloaded on demand from HuggingFace/ModelScope on first WebUI start, so Git LFS is no longer required (README.md:80-81).

Install with `uv`, which is required for reliable installation (README.md:85-98):
```bash
pip install -U uv
uv sync --all-extras
```
This creates `.venv` and installs the correct Python and dependencies; China-mirror variants use `--default-index "https://mirrors.aliyun.com/pypi/simple"` or `--default-index "https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple"` (README.md:97-106).

| Flag / extra | Meaning (README.md:108-115) |
|---|---|
| `--all-extras` | Adds every extra feature below |
| `--extra webui` | Adds WebUI support (recommended) |
| `--extra deepspeed` | Adds DeepSpeed support (may speed up inference on some systems) |

Platform notes: on Windows DeepSpeed may be difficult to install (drop `--all-extras` and add flags manually); on Linux/Windows a CUDA error means installing NVIDIA CUDA Toolkit 12.8 or newer (README.md:117-123).

Download models with `uv tool` (README.md:125-151):
```bash
uv tool install "huggingface-hub"
hf download IndexTeam/IndexTTS-2.5 --local-dir=checkpoints
hf download IndexTeam/IndexTTS-2 --local-dir=checkpoints_2
```
```bash
uv tool install "modelscope"
modelscope download --model IndexTeam/IndexTTS-2.5 --local_dir checkpoints
modelscope download --model IndexTeam/IndexTTS-2 --local_dir checkpoints_2
```
Small models download automatically on first run; for slow HuggingFace access set `export HF_ENDPOINT="https://hf-mirror.com"` (README.md:157-163).

Check GPUs with (README.md:165-172):
```bash
uv run tools/gpu_check.py
```

## Usage: WebUI and Serving
Web demo entry points (README.md:178-186):
```bash
# IndexTTS-2.5 (default)
uv run webui.py

# IndexTTS-2
uv run webui.py --version 2 --model_dir ./checkpoints_2
```
Open `http://127.0.0.1:7860`; all options via `uv run webui.py -h` (README.md:186-193).

| Inference option | Effect / caveat (README.md:188-205) |
|---|---|
| BF16 (2.5) / FP16 (2) | Faster, lower VRAM, very small quality loss |
| DeepSpeed | May speed up or slow down depending on hardware/drivers/OS — try both |
| Compiled CUDA kernels | Speed improvement |
| `uv` invocation | Automatically activates the per-project venv; do not manually activate an environment first |

Production deployment is via the vLLM recipe for IndexTTS (README.md:207-209).

## Usage: Python API
Run inside the `uv` environment, adding the repo root to `PYTHONPATH` where needed (README.md:211-223):
```bash
PYTHONPATH="$PYTHONPATH:." uv run indextts/infer_v2_5.py \
  --cfg_path checkpoints/config.yaml \
  --model_dir checkpoints \
  --text "Hello world" \
  --lang EN
```
Default `--prompt_wav` lives in `examples/`, populated on first WebUI start; without the WebUI fetch it via `from indextts.utils.examples_downloader import ensure_examples_available; ensure_examples_available()` (README.md:225-230). `indextts/infer_v2.py` runs a benchmark loop against a hardcoded `checkpoints/` directory, not the `checkpoints_2` layout (README.md:232-234).

Initialize (README.md:236-246):
```python
# IndexTTS2
from indextts.infer_v2 import IndexTTS2
tts = IndexTTS2(cfg_path="checkpoints_2/config.yaml", model_dir="checkpoints_2", use_fp16=False, use_cuda_kernel=False, use_deepspeed=False)

# IndexTTS2.5
from indextts.infer_v2_5 import IndexTTS2
tts = IndexTTS2(cfg_path="checkpoints/config.yaml", model_dir="checkpoints", use_bf16=True)
```

Voice cloning with a single reference (README.md:248-258):
```python
text = "Translate for me, what is a surprise!"
# IndexTTS2
tts.infer(spk_audio_prompt='examples/voice_01.wav', text=text, output_path="gen.wav", verbose=True)
# IndexTTS2.5 (multilingual, with language selection)
tts.infer(spk_audio_prompt='examples/voice_01.wav', text=text, lang="EN", output_path="gen.wav", verbose=True)
```

Emotion control with a separate reference (README.md:260-269):
```python
text = "酒楼丧尽天良，开始借机竞拍房间，哎，一群蠢货。"
# IndexTTS2
tts.infer(spk_audio_prompt='examples/voice_07.wav', text=text, output_path="gen.wav", emo_audio_prompt="examples/emo_sad.wav", verbose=True)
# IndexTTS2.5
tts.infer(spk_audio_prompt='examples/voice_07.wav', text=text, lang="ZH", output_path="gen.wav", emo_audio_prompt="examples/emo_sad.wav", verbose=True)
```

Emotion intensity via `emo_alpha`, valid range `0.0 - 1.0`, default `1.0` (100%), only when an emotional reference audio is specified (README.md:272-285):
```python
tts.infer(spk_audio_prompt='examples/voice_07.wav', text=text, output_path="gen.wav", lang="ZH", emo_audio_prompt="examples/emo_sad.wav", emo_alpha=0.9, verbose=True)
```

Vector-based emotion control omits the emotional reference audio and passes an 8-float list in the order `[happy, angry, sad, afraid, disgusted, melancholic, surprised, calm]`, with `use_random` to introduce stochasticity (README.md:287-292).

Truncation note: the source chunk is cut mid-sentence at `Use \`use_random\` to introduce stoc` (README.md:292) and the trailing `Macro components` list is cut after `top-level-files/` (chunk 01-overview.md:294-297); no claims are made about content beyond the cut.

**Covers:** README.md (repo root overview, model zoo, news, demos, install, WebUI/vLLM/Python API usage)
