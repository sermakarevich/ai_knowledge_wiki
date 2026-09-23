> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Overview
**In one sentence:** Moshi is a full-duplex speech-text foundation model with the Mimi streaming codec, shipped as three inference stacks (PyTorch, MLX, Rust) plus a web UI client.
## Key points
- Moshi is a speech-text foundation model and full-duplex spoken dialogue framework built on the Mimi streaming neural audio codec (README.md:14-15).
- The repo holds three inference stacks: PyTorch in `moshi/` for research, MLX in `moshi_mlx/` for on-device Mac/iPhone, and Rust in `rust/` for production including a Rust Mimi with `rustymimi` Python bindings (README.md:20-27).
- The web UI client used by the Moshi demo lives in `client/`, and fine-tuning lives in the separate `kyutai-labs/moshi-finetune` repo (README.md:29-31).
- Moshi models two audio streams (Moshi + user) plus text tokens for its own speech as an inner monologue, using a small Depth Transformer per timestep and a large 7B-parameter Temporal Transformer (README.md:41-45).
- Theoretical latency is 160ms (80ms Mimi frame size + 80ms acoustic delay), with practical overall latency as low as 200ms on an L4 GPU (README.md:45-46).
- Mimi processes 24 kHz audio to a 12.5 Hz representation at 1.1 kbps in fully streaming manner (80ms frame-size latency), using encoder/decoder Transformers, 12.5 Hz strides, WavLM distillation into the first codebook, and adversarial + feature-matching loss only (README.md:55-67).
- Three checkpoints are released — Moshiko (male synthetic voice), Moshika (female synthetic voice), and Mimi — under CC-BY 4.0, with per-backend HuggingFace repos and quantization variants (README.md:77-92).
---
## Repository organisation
Three separate inference stacks plus client (README.md:20-29):
| Stack | Directory | Purpose |
|---|---|---|
| PyTorch | `moshi/` | Research and tinkering (README.md:23) |
| MLX | `moshi_mlx/` | On-device inference on iPhone and Mac (README.md:24) |
| Rust | `rust/` | Production; contains Rust Mimi with `rustymimi` Python bindings (README.md:25-27) |
| Web UI client | `client/` | Client used in the Moshi demo (README.md:29) |
Verbatim (README.md:23-29):
```text
- **[PyTorch](#pytorch-implementation): for research and tinkering.** The code is in the [`moshi/`](moshi/) directory.
- **[MLX](#mlx-implementation-for-local-inference-on-macos): for on-device inference on iPhone and Mac.** The code is in the [`moshi_mlx/`](moshi_mlx/) directory.
- **[Rust](#rust-implementation): for production.** The code is in the [`rust/`](rust/) directory.
```
Related models reusing the multi-stream architecture (README.md:35-37): Hibiki simultaneous speech translation (`kyutai-labs/hibiki`) and Kyutai TTS/STT (`kyutai-labs/delayed-streams-modeling`).
## Model architecture
Moshi models two audio streams — Moshi speaking and the user speaking — and predicts text tokens for its own speech as an inner monologue, which improves generation quality (README.md:41-43). A small Depth Transformer models inter-codebook dependencies per timestep while a large 7B-parameter Temporal Transformer models temporal dependencies (README.md:44-45). Latency budget (README.md:45-46):
| Quantity | Value |
|---|---|
| Mimi frame size | 80ms |
| Acoustic delay | 80ms |
| Theoretical total | 160ms |
| Practical overall on L4 GPU | as low as 200ms |
At inference the user audio stream comes from audio input and the Moshi stream is sampled from model output (README.md:49-50).
## Mimi codec
Mimi is a streaming neural audio codec: 24 kHz in, 12.5 Hz representation, 1.1 kbps bandwidth, 80ms frame-size latency, outperforming non-streaming SpeechTokenizer (50 Hz, 4 kbps) and SemantiCodec (50 Hz, 1.3 kbps) per the README comparison (README.md:55-58). Design points (README.md:60-67):
- Builds on SoundStream and EnCodec, adding a Transformer in encoder and decoder with strides for 12.5 Hz overall frame rate (README.md:60-62).
- 12.5 Hz rate stays close to text-token rate (~3-4 Hz), limiting Moshi autoregressive steps (README.md:62-63).
- Distillation loss aligns first-codebook tokens with WavLM self-supervised representation, modeling semantic and acoustic info in one model (README.md:64-65).
- Uses only adversarial training loss plus feature matching, improving subjective quality at low bitrate (README.md:65-67).
## Released models
Three models released (README.md:77-80): Moshi fine-tuned on male synthetic voice (Moshiko), Moshi fine-tuned on female synthetic voice (Moshika), and Mimi. Mimi is bundled in each model repo with the same checkpoint format (README.md:83). Per-backend repos and formats (README.md:85-90):
| Backend | Repos |
|---|---|
| PyTorch (bf16, int8) | `kyutai/moshika-pytorch-bf16`, `kyutai/moshika-pytorch-q8` (experimental), `kyutai/moshiko-pytorch-bf16`, `kyutai/moshiko-pytorch-q8` (experimental) |
| MLX (int4, int8, bf16) | `kyutai/moshika-mlx-q4`, `kyutai/moshika-mlx-q8`, `kyutai/moshika-mlx-bf16`, `kyutai/moshiko-mlx-q4`, `kyutai/moshiko-mlx-q8`, `kyutai/moshiko-mlx-bf16` |
| Rust/Candle (int8, bf16) | `kyutai/moshika-candle-q8`, `kyutai/moshika-candle-bf16`, `kyutai/moshiko-candle-q8`, `kyutai/moshiko-candle-bf16` |
All models under CC-BY 4.0 license (README.md:92).
## Requirements
Needs at least Python 3.10, 3.12 recommended; per-backend details in individual backend directories (README.md:96). Install (README.md:99-107):
```bash
pip install -U moshi      # moshi PyTorch, from PyPI
pip install -U moshi_mlx  # moshi MLX, from PyPI, best with Python 3.12.
pip install -U -e "git+https://git@github.com/kyutai-labs/moshi.git#egg=moshi&subdirectory=moshi"
pip install -U -e "git+https://git@github.com/kyutai-labs/moshi.git#egg=moshi_mlx&subdirectory=moshi_mlx"
pip install rustymimi  # mimi, rust implementation with Python bindings from PyPI
```
Non-3.12 Python may fail installing `moshi_mlx` or `rustymimi`; then install the Rust toolchain or switch to 3.12 (README.md:109-110). No official Windows support; MLX tested on MacBook Pro M3; PyTorch has no quantization support so needs a ~24GB GPU (README.md:112-114). Rust backend needs a recent Rust toolchain, plus CUDA with `nvcc` for GPU support (README.md:116-117).
## PyTorch inference stack
Streaming audio tokenizer (mimi) plus language model (moshi) API in the `moshi` directory (README.md:121-122). Interactive mode requires a model server plus web UI or CLI client (README.md:124-125):
```bash
python -m moshi.server [--gradio-tunnel] [--hf-repo kyutai/moshika-pytorch-bf16]
python -m moshi.client [--url URL_TO_GRADIO]
```
Web UI served at `http://localhost:8998` (README.md:132). Remote-GPU microphone workarounds (README.md:133-140): forward remote port 8998 via ssh `-L`, or use `--gradio-tunnel` (goes through US, up to 500ms added latency from Europe; `--gradio-tunnel-token` pins a reusable address). `--hf-repo` selects a different pretrained model (README.md:142). Non-localhost HTTP servers may break browser microphone access, which some browsers allow only over https (README.md:144-146). The CLI client is barebones: no echo cancellation, no lag-compensating frame skipping (README.md:152-153). Further API use in `moshi/README.md` (README.md:155-156).
## MLX local inference
```bash
python -m moshi_mlx.local -q 4   # weights quantized to 4 bits
python -m moshi_mlx.local -q 8   # weights quantized to 8 bits
python -m moshi_mlx.local -q 4 --hf-repo kyutai/moshika-mlx-q4
python -m moshi_mlx.local -q 8 --hf-repo kyutai/moshika-mlx-q8
```
Always match `-q` with `--hf-repo` (README.md:161-167). CLI is barebone with no echo cancellation or lag-compensating frame skipping (README.md:170-171). `python -m moshi_mlx.local_web` serves the web UI at `http://localhost:8998` (README.md:173-174).
## Rust inference server
From within the `rust` directory (README.md:179-184):
```bash
cargo run --features cuda --bin moshi-backend -r -- --config moshi-backend/config.json standalone
```
On macOS replace `--features cuda` with `--features metal` (README.md:186). Use `config-q8.json` instead of `config.json` for the quantized q8 model; select another pretrained model (e.g. Moshika) via the `"hf_repo"` key in either file (README.md:188-190). After `standalone worker listening` is printed, use the web UI; the Rust server uses https by default at `https://localhost:8998`, accepting the browser unsafe-site warning (README.md:192-198).
## Clients
Web UI recommended for its additional echo cancellation aiding model quality; most commands serve the UI directly at the provided URL (README.md:202-204). Command-line interfaces also exist for Rust and Python using the same protocol as the web UI (README.md:206-208).
**Covers:** README.md (repo organisation, Moshi/Mimi architecture, released models, requirements, PyTorch/MLX/Rust inference, clients); directories `moshi/`, `moshi_mlx/`, `rust/`, `client/`
