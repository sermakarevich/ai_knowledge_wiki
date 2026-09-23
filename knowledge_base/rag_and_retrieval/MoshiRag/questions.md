---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---
> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# Retrieval Practice: kyutai-labs/moshi-rag

### Q1. What problem does MoshiRAG solve and how does its front-end/back-end split preserve real-time interactivity?
> [!tip]- Answer
> > MoshiRAG adds asynchronous knowledge retrieval to a compact full-duplex Moshi/Mimi speech LM to improve factuality without breaking real-time conversation. The Moshi-based front end keeps listening and speaking continuously while the back end fetches facts in parallel. On a retrieval trigger token the front end bridges the delay with lightweight pre-RAG content like short acknowledgments. See [[wiki/01-overview|Overview]].

### Q2. How does retrieval context flow into and back out of the MoshiRAG back end?
> [!tip]- Answer
> > The text-in/text-out back end takes conversation context combining Moshi inner-monologue text and streaming-ASR user transcription as input. It can use LLM-based or search-based retrieval to produce reference text. That reference text is then encoded and injected back into Moshi as a stream so later response segments are grounded without interrupting the dialogue. See [[wiki/01-overview|Overview]].

### Q3. What are the released Moshika model formats and the local hardware requirements for running MoshiRAG?
> [!tip]- Answer
> > The released model is fine-tuned on the female synthetic voice Moshika in PyTorch bf16 (`kyutai/moshika-rag-pytorch-bf16`) and Rust/Candle bf16 (`kyutai/moshika-rag-candle-bf16`) formats under CC-BY 4.0. Local runs need Python ≥3.10 (3.12 recommended) and a 24GB-class GPU for the PyTorch front end since quantization is unsupported. The Rust backend additionally needs a recent Rust toolchain plus CUDA/`nvcc` for GPU support. See [[wiki/01-overview|Overview]].

### Q4. What are the two cooperating PyTorch processes and which environment variables wire them to retrieval and transcription?
> [!tip]- Answer
> > The main Moshi server (`python -m moshi.moshi.server`) handles full-duplex speech and calls the retrieval LLM over an OpenAI-compatible HTTP API on RAG triggers. The reference text encoder (`python -m moshi.moshi.server_conditioner`) encodes retrieved strings for Moshi's conditioning path. They are wired via `REFERENCE_ENCODER_URL`, `STT_URL`/`STT_API_KEY` for streaming ASR, `LLM_BASE_URL`/`LLM_API_KEY`/`LLM_MODEL_NAME` for retrieval, and optional `MOSHI_RETRIEVAL_LLMS_JSON` for multi-backend profiles. See [[wiki/01-overview|Overview]].

### Q5. What hygiene, lint, and dev-tooling do the MoshiRAG repo-root files define?
> [!tip]- Answer
> > `.gitignore` (199 lines) excludes Python, packaging, test, IDE, and ML/media artifacts plus local secrets and outputs like `results*` and model weights. `.pre-commit-config.yaml` wires `ruff-check`/`ruff-format` at `rev: v0.15.8` plus a local `cargo fmt` hook on `rust/Cargo.toml`. `requirements-dev.txt` pins only `pre-commit>=3.8`, `pyright>=1.1`, and `flake8>=7.1`, while dual `LICENSE-APACHE`/`LICENSE-MIT` files vendor the standard license texts. See [[wiki/02-top-level-files|Top-level files]].

### Q6. How does `swarm-config.yaml` orchestrate the MoshiRAG deployment and route traffic to it?
> [!tip]- Answer
> > The Swarm stack orchestrates `traefik` (TLS via Let's Encrypt), `frontend` built from `client/`, `backend` and `arc_encoder` built from `moshi/`, plus `agent`/`portainer` monitoring. Traefik routes `frontend` on `PathPrefix("/")` at priority 10 and `backend` on `PathPrefix("/api")` at priority 100 behind HTTPS redirect. `backend` and `arc_encoder` each reserve one GPU, and `deploy.sh` rebuilds, pushes, and redeploys the stack over SSH. See [[wiki/02-top-level-files|Top-level files]].

### Q7. (Evaluation) Would you recommend MoshiRAG's async-RAG architecture over a simpler turn-based voice RAG pipeline for a live factual assistant?
> [!tip]- Answer
> > Recommend MoshiRAG's async design when sub-second full-duplex interactivity matters, since trigger-token retrieval with pre-RAG bridging and streamed reference injection grounds answers without pausing conversation. Prefer a simpler turn-based pipeline when GPU budget is tight or retrieval latency is unreliable, because MoshiRAG needs 24GB-class GPUs plus a low-latency (under ~3s) local retrieval LLM to avoid quality loss. The added encoder, ASR, and Swarm deployment complexity is justified only for genuinely real-time use cases. See [[wiki/01-overview|Overview]].
