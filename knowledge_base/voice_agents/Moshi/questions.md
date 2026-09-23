---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---
> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# Retrieval Practice: kyutai-labs/moshi

### Q1. What is Moshi, and how is the repository organised?
> [!tip]- Answer
> Moshi is a speech-text foundation model and full-duplex spoken dialogue framework built on the Mimi streaming neural audio codec. The repo holds three inference stacks — PyTorch in `moshi/` for research, MLX in `moshi_mlx/` for on-device iPhone/Mac inference, and Rust in `rust/` for production — plus the web UI client in `client/`. See [[wiki/01-overview|Overview]].

### Q2. How does Moshi model a live conversation, and what do its two Transformers do?
> [!tip]- Answer
> Moshi jointly models two audio streams, one for Moshi speaking and one for the user, and predicts text tokens for its own speech as an inner monologue that improves generation quality. A small Depth Transformer models inter-codebook dependencies within each timestep, while a large 7B-parameter Temporal Transformer models dependencies across time. See [[wiki/01-overview|Overview]].

### Q3. What latency does Moshi claim, and how do the Mimi codec's specs support it?
> [!tip]- Answer
> Moshi claims 160ms theoretical latency (80ms Mimi frame size plus 80ms acoustic delay), with overall latency as low as 200ms in practice on an L4 GPU. Mimi compresses 24 kHz audio to a 12.5 Hz representation at 1.1 kbps in a fully streaming manner, and that near-text-rate frame rate limits the number of autoregressive steps Moshi must take. See [[wiki/01-overview|Overview]].

### Q4. Which design and training choices distinguish the Mimi codec?
> [!tip]- Answer
> Mimi builds on SoundStream and EnCodec by adding a Transformer in both encoder and decoder, with strides giving a 12.5 Hz overall frame rate. It distills first-codebook tokens toward a WavLM self-supervised representation so one model captures semantic and acoustic information, and it trains with only adversarial plus feature-matching loss for better subjective quality at low bitrate. See [[wiki/01-overview|Overview]].

### Q5. What checkpoints are released, and how do you run each inference stack?
> [!tip]- Answer
> Three checkpoints are released under CC-BY 4.0: Moshi fine-tuned on a male synthetic voice (Moshiko), on a female synthetic voice (Moshika), and the Mimi codec, with per-backend HuggingFace repos including quantized variants. PyTorch runs via `python -m moshi.server` plus a web UI or CLI client on port 8998, MLX via `python -m moshi_mlx.local -q 4|8` with matching `--hf-repo`, and Rust via `cargo run --features cuda --bin moshi-backend` (metal on macOS, `config-q8.json` for quantized). See [[wiki/01-overview|Overview]].

### Q6. What do the repo's top-level files define for hygiene, checks, deployment, and limits?
> [!tip]- Answer
> Repo hygiene comes from `.dockerignore` (only `moshi/.venv/*`) and a Python-template `.gitignore` extended with model artifacts, traces, and secrets, while `.pre-commit-config.yaml` defines five local hooks linting and testing `moshi` and `moshi_mlx`. Deployment is a Docker Swarm stack of traefik, a frontend, and one-GPU backend defined in `swarm-config.yml` and pushed by `deploy.sh` over SSH. The FAQ bounds the system: English-only, no training-data release, finetuning in a separate repo, no quantized PyTorch, and ~5-minute fixed-buffer caps on MLX/Rust. See [[wiki/02-top-level-files|Top-level-files]].

### Q7. You must serve Moshi in production on a GPU server but prototype cheaply on a MacBook: which stacks would you choose for each, and why?
> [!tip]- Answer
> I would prototype on the MacBook with the MLX stack because it is explicitly built for on-device Mac inference with 4-bit and 8-bit quantized checkpoints, avoiding PyTorch's ~24GB GPU demand. For production serving I would choose the Rust backend with CUDA and the int8 checkpoint, since it is framed for production and supports quantization that PyTorch lacks. This judgment rests on the documented stack purposes and FAQ limits, so the final pick should be validated against the Moshiko/Moshika checkpoints before committing. See [[wiki/01-overview|Overview]].
