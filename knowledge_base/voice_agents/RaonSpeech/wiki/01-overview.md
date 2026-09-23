> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Overview
**In one sentence:** Raon-Speech is a 9B bilingual (English/Korean) SpeechLM family with an offline track (`TTS`, `STT`, `SpeechChat`, `TextQA`) and a real-time full-duplex track (Raon-SpeechChat) sharing one core model and processor stack under `src/raon/`.
## Key points
- The repo contains two tracks sharing the same core family and processor stack under `src/raon/`: Raon-Speech (Offline SpeechLM: `TTS`, `STT`, `SpeechChat`, `TextQA`) and Raon-SpeechChat (Offline/Realtime Full-Duplex) (README.md:37-43).
- Raon-Speech is a 9B bilingual English/Korean SpeechLM for speech understanding, answering, and generation, trained on 1M+ hours of curated speech-text data and evaluated across 42 speech and text benchmarks; Raon-SpeechChat is continually trained on 116K hours of time-aligned dialogue data (README.md:47-49).
- Raon-SpeechChat extends Raon-Speech to real-time full-duplex conversation via causal streaming, interleaved speech-text modeling, explicit interaction-state modeling, and text lookahead, with strength in turn-taking, backchanneling, and interruption handling (README.md:48-50).
- The system is distributed with Hugging Face Transformers integration via `AutoModel.from_pretrained(..., trust_remote_code=True)` plus an open release of checkpoints, training/inference pipeline, interactive demo, and three Korean benchmarks (KVoiceBench, KOpenAudioBench, KMMAU) (README.md:52-53).
- All model entry points accept either a local checkpoint directory or a Hugging Face `repo_id` (e.g. `KRAFTON/Raon-Speech-9B`, `KRAFTON/Raon-SpeechChat-9B`), loaded via `RaonPipeline(..., device="cuda", dtype="bfloat16")` or `bash scripts/infer.sh` / `bash scripts/duplex_infer.sh` (README.md:83-105).
- Two execution modes exist: with `raon` installed (all entry points: `scripts/*.sh`, demos, `from raon import RaonPipeline`) versus without install (only Hub-remote-code Gradio demo and pure-Transformers flow; `python -m raon.*` and the full-duplex realtime runtime are not supported as-is) (README.md:115-164).
- The package backbone is one shared `RaonModel` (LM backbone + audio encoder + Mimi codec path) with two model types, `raon` (Raon-Speech) and `raon_duplex` (Raon-SpeechChat), and trainable blocks `input_adaptor`, `output_adaptor`, `audio_lm_head`, `proj_code`, `code_predictor` (README.md:225-231).
---
## Model family and tracks
Two tracks share the same core model family and processor stack under `src/raon/` (README.md:43):
- `Raon-Speech (Offline SpeechLM)`: `TTS`, `STT`, `SpeechChat`, `TextQA` (README.md:40).
- `Raon-SpeechChat (Offline/Realtime Full-Duplex)` (README.md:41).
Links (README.md:29-35):
| Artifact | URL |
|---|---|
| GitHub | `https://github.com/krafton-ai/Raon-Speech` |
| Official Demo | `https://raon.krafton.ai` |
| Hugging Face Org | `https://huggingface.co/KRAFTON` |
| Speech model card | `https://huggingface.co/KRAFTON/Raon-Speech-9B` |
| SpeechChat model card | `https://huggingface.co/KRAFTON/Raon-SpeechChat-9B` |
| Technical Report | `.../Raon-Speech-9B/resolve/main/Technical_Report_Raon_Speech.pdf` |
## Benchmarks and latency
Raon-Speech targets low-latency real-time generation while covering ASR, speech generation, spoken QA, audio understanding, and text QA; Raon-SpeechChat is rated on pause handling, backchanneling, smooth turn-taking, interruption handling, overlap robustness, and multi-turn dialogue (README.md:63-65). Single-GPU streaming TTS on LibriSpeech `test-clean` (README.md:65-71):
| Metric | RTX 6000 Pro Blackwell | L40S |
|---|---:|---:|
| `RTF` | `0.27` (`3.7x` real-time) | `0.45` (`2.2x` real-time) |
| `TTFT` | `617 ms` | `887 ms` |
| `TBT` | `135 ms` | `233 ms` |
Definitions verbatim (README.md:73-75): `RTF`: Real-Time Factor (below `1.0` = faster than real time); `TTFT`: Time to First Token; `TBT`: Time Between Tokens.
## Requirements and setup
Requirements (README.md:77-81): Python `>=3.11`; CUDA GPU recommended (`bfloat16` / `float16`); PyTorch + Torchaudio matching CUDA. Setup (README.md:168-195):
```bash
git clone https://github.com/krafton-ai/Raon-Speech
cd Raon-Speech
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
# or: uv sync
pip install -e ".[demo]"   # extra: sglang, gradio, fastapi, uvicorn
pip install flash-attn     # optional, training only
```
## Model loading and execution modes
Entry points accept a local checkpoint directory or a Hub `repo_id` (README.md:83-88):
```python
from raon import RaonPipeline

pipe = RaonPipeline("KRAFTON/Raon-Speech-9B", device="cuda", dtype="bfloat16")
# or
pipe = RaonPipeline("KRAFTON/Raon-SpeechChat-9B", device="cuda", dtype="bfloat16")
```
Pre-download (README.md:107-113): `hf download KRAFTON/Raon-Speech-9B --local-dir /path/to/model_dir`. Mode 1 (`raon` installed via `pip install -e .` or `uv sync`) supports `scripts/infer.sh`, `scripts/duplex_infer.sh`, `scripts/train.sh`, `scripts/duplex_train.sh`, `demo/run_gradio_demo.sh`, `demo/run_gradio_duplex_demo.sh`, and `from raon import RaonPipeline` (README.md:117-124). Mode 2 (no install) supports only the Raon-Speech Gradio demo fallback and the pure-Transformers Hub-remote-code flow with `trust_remote_code=True` (see `examples/message_example.ipynb`, `examples/duplex_example.ipynb`); `python -m raon.*` commands and the `demo/gradio_duplex_demo.py` realtime runtime are not supported as-is because they import `raon.*` (README.md:126-164).
## Project layout and architecture
Layout verbatim (README.md:205-223):
```text
Raon-Speech/
├── src/raon/                 # package code
│   ├── models/               # RaonModel / RaonDuplexModel
│   ├── modules/              # audio encoder, tokenizer, speaker encoder, etc.
│   ├── utils/                # processor, datasets, losses, prompts, special tokens
│   ├── train.py              # SpeechLLM training entry
│   ├── duplex_train.py       # Full-duplex training entry
│   ├── generate.py           # SpeechLLM JSONL inference entry
│   ├── duplex_generate.py    # Full-duplex inference entry
│   └── pipeline.py           # high-level API (RaonPipeline)
├── scripts/                  # shell wrappers
├── demo/                     # Gradio demos
├── config/                   # inference configs
├── data/                     # sample datasets
└── examples/                 # notebooks and scripts
```
Architecture: one shared backbone `RaonModel` (LM backbone + audio encoder + Mimi codec path); model types `raon` and `raon_duplex`; main trainable blocks `input_adaptor`, `output_adaptor`, `audio_lm_head`, `proj_code`, `code_predictor` (README.md:225-231).
## SpeechLLM tasks
JSONL data format, one sample per line, sample eval data under `data/speechllm/eval` (README.md:235-247):
| Field | Type | Description |
|---|---|---|
| `conversations` | `list[dict]` | turns with `from` (`human`/`gpt`) and `value` |
| `audios` | `list[str]` | audio paths consumed by `<audio>` tags in order |
| `speaker_ref_audios` | `list[str]` | optional speaker reference audio for TTS |
| `channel` | `str` | `tts`, `stt`, `speech-chat`, `textqa` |
| `system` | `str` | optional system prompt |
Inference: `bash scripts/infer.sh` with task defaults from `config/infer.yaml`; `--attn_implementation` controls the attention backend (default `sdpa`, `fa` for FlashAttention); `--data_dir` is scanned for JSONL files (README.md:249-258). Advanced CLI (README.md:260-270):
```bash
python -m raon.generate \
  --model_path /path/to/model \
  --data_dir /path/to/data_dir \
  --output_dir /path/to/output_dir \
  --config /path/to/config.yaml \
  --batch_size 4 \
  --attn_implementation sdpa
```
Pipeline API verbatim (README.md:272-295):
```python
pipe = RaonPipeline("/path/to/model", device="cuda", dtype="bfloat16", config="/path/to/config.yaml")

text = pipe.stt("/path/to/stt.wav")
audio, sr = pipe.tts("Hello!", speaker_audio="/path/to/speaker_ref.wav")
ans1 = pipe.speech_chat("/path/to/speech-chat.wav")
ans2 = pipe.textqa("What did the speaker say?", audio="/path/to/textqa.wav")

pipe.save_audio((audio, sr), "/path/to/tts.wav")

audio, sr = pipe.tts_continuation(
    target_text="Continue this sentence.",
    ref_audio="/path/to/speaker_ref.wav",
    ref_text="Optional transcription of ref audio.",
)
```
Training: `bash scripts/train.sh`; preset variables at top of script; `NPROC_PER_NODE` controls multi-GPU torchrun; `MASTER_PORT` sets the rendezvous port; `USE_SPEAKER_EMBEDDING` toggles speaker-conditioning inputs; current code freezes `audio_encoder`, `input_adaptor`, `output_adaptor`, `audio_lm_head`, `proj_code`, `code_predictor`, `speaker_encoder`; default attention is `sdpa`, `fa` for FlashAttention (README.md:302-318). See `examples/message_example.py` and `examples/message_example.ipynb` (README.md:297-300).
## Full-duplex data format (truncated in chunk)
Training (`duplex_train.py`) expects one JSON object per line with stereo audio metadata; required top-level fields given before the cut (README.md:322-333):
| Field | Type | Description |
|---|---|---|
| `audio_path` | `str` | Path to stereo wav (`2` channels). |
| `language` | `str` | Language code (for prompt selection), e.g. `eng`, `kor`. |
| `channel` | `str` | Duplex channel type, e.g. `full_duplex` or `duplex_instruct`. |
| `speak_first` | `list[int or bool]` | Per-channel initial speaking mode (cut off mid-description in chunk). |
Truncation note: the chunk ends mid-sentence in the `speak_first` row (chunk line 333-334) and then lists only the macro-component pointer `top-level-files/` (chunk lines 335-337); no further Full-Duplex inference/training details are present in this chunk, so they are not covered here.
**Covers:** README.md (repo overview: links, two tracks, key features, benchmarks/latency table, requirements, model loading, execution modes, environment setup, project layout, model architecture, SpeechLLM data format/inference/pipeline API/training, Full-Duplex data format up to the `speak_first` truncation); macro-component pointer `top-level-files/` is out of scope for this page.
