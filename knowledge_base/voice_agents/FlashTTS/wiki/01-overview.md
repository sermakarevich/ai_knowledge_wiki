[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Overview
**In one sentence:** FlashTTS is an open-source low-latency streaming TTS framework that combines a lagged multi-track architecture with parallel MTP and X-pred mean-flow decoding to reach 2-NFE token-to-mel at 325ms first-packet latency.
## Key points
- FlashTTS natively processes streaming text and speech inputs via a lagged multi-track architecture, eliminating sentence-level buffering (README.md:16).
- Acoustic generation integrates parallel Multi-Token Prediction (MTP) with an X-pred mean flow matching decoder for token-to-mel in exactly two function evaluations (README.md:16).
- First-packet latency is 325ms versus robust streaming baselines while preserving zero-shot voice cloning and multi-lingual intelligibility (README.md:16).
- The inference pipeline is `Text/Speech Input → [Text Tokenizer] + [Speaker Extractor] → [LLM Decoder with MTP] → [Mean Flow X-pred Module] (2-NFE) → [HiFi-GAN Vocoder] → 24kHz audio` (README.md:50).
- Streaming uses a first chunk of 24 tokens, then 18-token hop with 6-token lookahead per step (24-token context, 18 tokens output per chunk) (README.md:74).
- Entry points are `examples/inference.py` with `--mode flash_tts` (text + reference wav) or `--mode meanflow_only` (token file + reference wav), plus `--stream` for chunked mode (README.md:86).
- Core layout splits into `cosyvoice/` (LLM, tokenizer, frontend), `jit_meanflow_xpred/` (token2mel + vocoder), `third_party/` (CAMPPlus, Matcha-TTS), and `examples/` (README.md:192).
---
## Framework identity
Open-source, low-latency streaming TTS framework (README.md:16):
> "FlashTTS is an open-source, low-latency streaming TTS framework that addresses these limitations." (README.md:16)
Key features claimed (README.md:22):
- Native Streaming: lagged multi-track architecture without sentence-level buffering (README.md:22)
- MTP + X-pred Mean Flow: parallel prediction with flow distillation for fast decoding (README.md:23)
- 2-NFE acoustic generation in exactly two function evaluations (README.md:24)
- 325ms first-packet latency (README.md:25)
- Zero-shot voice cloning from reference audio (README.md:26)
- Cross-lingual intelligibility (README.md:27)
- Open-source code and checkpoints (README.md:28)
Upstream debts: CosyVoice (backbone/LLM decoder), F5-TTS (flow matching), HiFi-GAN (vocoder), CAMPPlus (speaker embedding) (README.md:293).
## Pipeline stages
Verbatim stage chain (README.md:50):
```
Text/Speech Input
    ↓
[Text Tokenizer] + [Speaker Extractor]
    ↓
[LLM Decoder with MTP Acceleration]
    ↓
[Mean Flow X-pred Module] (2-NFE)
    ↓
[HiFi-GAN Vocoder]
    ↓
Audio Output (24kHz)
```
Component details (README.md:64):
| # | Component | Role |
|---|---|---|
| 1 | FlashTTS (cosyvoice) | Core TTS inference: text tokenizer, CAMPPlus speaker embedding, decoder-only transformer with MTP, streaming-input stacking of text and speech tracks, LLM + MeanFlow + vocoder inference-only model (README.md:64) |
| 2 | jit_meanflow_xpred | Mean flow matching for 2-NFE mel generation with X-pred training objective (README.md:70) |
| 3 | Streaming | First chunk 24 tokens; 18-token hop with 6-token lookahead, 24-token context, 18 tokens output per chunk (README.md:74) |
| 4 | Vocoder | HiFi-GAN waveform generation at 24kHz (README.md:76) |
## Usage
Recommended example script from repo root (README.md:82):
```bash
# FlashTTS: text-to-speech with voice cloning (needs model_dir with LLM + MeanFlow/vocoder)
python examples/inference.py --mode flash_tts --text "Hello, world." --prompt_wav path/to/ref.wav --output_dir out

# MeanFlow-only: token file + reference wav -> wav (no LLM; for testing acoustic model)
python examples/inference.py --mode meanflow_only --token_path path/to/tokens.npy --prompt_wav path/to/ref.wav --output_dir out

# With streaming (MeanFlow 24/18/6 token chunks)
python examples/inference.py --mode meanflow_only --token_path tokens.npy --prompt_wav ref.wav --output_dir out --stream
```
Options `--model_dir` and `--pretrained_model_dir` are documented in `examples/inference.py` (README.md:95).
Basic FlashTTS call uses a config YAML defining only `llm` (no `flow`/`hift`); the MeanFlow backend loads automatically (README.md:111):
```python
from cosyvoice.cli.cosyvoice import FlashTTS

# model_dir: path to your model dir (with llm.pt, cosyvoice2*.yaml, etc.)
# pretrained_model_dir: base dir for configs and MeanFlow/vocoder assets
model = FlashTTS('model_dir', pretrained_model_dir='path/to/pretrained')

# Zero-shot voice cloning
prompt_wav = 'path/to/prompt_audio.wav'  # 16kHz reference
text = "Hello, this is a text-to-speech example."
for output in model.inference_zero_shot(text, "", prompt_wav):
    audio = output['tts_speech']  # [1, samples]
```
MeanFlow efficient inference (X-pred, 2 steps) with exact parameter names `token`, `spk_emb`, `prompt_mel`, `steps`, `cfg_strength`, `device` (README.md:131):
```python
from jit_meanflow_xpred.infer.infer_meanflow_jit_xpred import (
    inference_meanflow, initialize_model, initialize_vocoder
)
import torch

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Load models
model = initialize_model(config_path, checkpoint_path, device)
vocoder = initialize_vocoder(vocoder_config, vocoder_ckpt, device)

# Run inference with 2 step (MeanFlow = ultra-fast)
wav, inference_time = inference_meanflow(
    model=model,
    vocoder=vocoder,
    token=token_tensor,           # [B, seq_len]
    spk_emb=speaker_embedding,    # [B, 192]
    prompt_mel=reference_mel,     # [B, T, 80]
    steps=2,                       # MeanFlow: 2 ODE step
    cfg_strength=2.0,              # Classifier-free guidance strength
    device=device
)
```
Batch and streaming CLI variants (README.md:162):
```bash
# Batch inference
python -m jit_meanflow_xpred.infer.infer_meanflow_jit_xpred \
  --prompt_wav ./wav_dir \
  --token_path ./tokens.jsonl \
  --output_dir ./outputs \
  --batch \
  --steps 1

# Streaming inference (24-token first chunk, 18-token hop, 6-token lookahead)
python -m jit_meanflow_xpred.infer.infer_meanflow_jit_xpred \
  --prompt_wav ref.wav \
  --token_path tokens.npy \
  --output_dir ./outputs \
  --stream \
  --steps 1
```
Install (README.md:99):
```bash
# Clone repository
git clone <repo-url>
cd flashtts_opensource

# Install dependencies
pip install -r requirements.txt
```
## Configuration
Model config in `jit_meanflow_xpred/configs/` (README.md:238), verbatim excerpt (README.md:240):
```yaml
model:
  arch:
    num_layers: 16              # Transformer layers
    hidden_size: 768           # Hidden dimension
    num_heads: 16               # Attention heads
    vocab_size: 6563            # Token vocabulary
  text_num_embeds: 4096
  mel_dim: 80                    # Mel-spectrogram dimension

inference:
  steps: 2                       # MeanFlow: single step ODE
  cfg_strength: 2.0              # Classifier-free guidance scale
  chunk_size: 0                  # 0 = full sequence, >0 = chunk mel frames
```
Speaker embedding via CAMPPlus (README.md:258):
| Flag | Value |
|---|---|
| Output dimension | 192 (README.md:259) |
| Input requirement | 16kHz, single-channel audio (README.md:260) |
| Processing | Mel-spectrogram → DTDNN layers → 192-dim embedding (README.md:261) |
Core dependencies: PyTorch >= 1.13.0, torchaudio >= 0.13.0, numpy >= 1.21.0, scipy >= 1.7.0, onnxruntime >= 1.12.0, omegaconf, hyperpyyaml; full list in `requirements.txt` (README.md:277).
## Performance and languages
Latency table (README.md:267):
| Metric | Value | Notes |
|--------|-------|-------|
| First-Packet Latency | 325ms | With streaming architecture (README.md:269) |
| Mean Flow Steps | 2 | X-pred mean flow: few ODE steps (README.md:270) |
| Token-to-Mel Time | ~100ms | On NVIDIA 4090 GPU (README.md:271) |
| Mel-to-Wave Time | ~50ms | HiFi-GAN vocoding (README.md:272) |
Supported languages: Chinese (Mandarin), English, French, German, Japanese, Korean (README.md:180).
Project structure excerpt: `cosyvoice/cli/{cosyvoice.py, model.py, frontend.py}`, `cosyvoice/{llm, tokenizer, transformer, utils, hifigan, vllm}`, `jit_meanflow_xpred/{model, infer, eval, configs}`, `third_party/{campplus, Matcha-TTS}`, `examples/{grpo, huawei, libritts, magicdata-read}`, `asset/flashtts_overview.jpg` (README.md:191). License is Apache 2.0 (README.md:289). No truncated files were noted in the chunk.
**Covers:** README.md (FlashTTS overview, pipeline, usage, config, performance, structure)
