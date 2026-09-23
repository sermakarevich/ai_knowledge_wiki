> [[index|Wiki]] | [[summary|Summary]]
# kyutai-labs/moshi-rag — Digest

## 1. [[wiki/01-overview|Overview]]
**In one sentence:** MoshiRAG is a compact full-duplex speech language model built on Moshi/Mimi that adds asynchronous knowledge retrieval to improve factuality without breaking real-time interactivity.
## Key points
- MoshiRAG is a compact **full-duplex** speech LM augmented with asynchronous knowledge retrieval to improve factuality without sacrificing real-time interactivity (README.md:14).
- The repo is based on the Moshi repo, augmented with RAG-related implementation (README.md:16).
- The repository holds two main codebases: PyTorch for research/experimentation in `moshi/` and Rust for production use in `rust/`, plus the web UI client in `client/` (README.md:21-26).
- The system uses a modular front-end/back-end design: a full-duplex Moshi-based speech model for real-time conversation plus an asynchronous retrieval system running in parallel (README.md:30-32).
- On a predicted retrieval trigger token the front end keeps talking while conversation context is sent to the back end, optionally emitting lightweight pre-RAG content such as short acknowledgments (README.md:34).
- The back end is text-in/text-out (LLM-based or search-based), takes conversation context combining Moshi inner-monologue text and streaming-ASR user transcription, and its returned reference text is encoded and injected back into Moshi as a stream (README.md:36).
- Released model is MoshiRAG fine-tuned on a female synthetic voice (Moshika) in PyTorch bf16 (`kyutai/moshika-rag-pytorch-bf16`) and Rust/Candle bf16 (`kyutai/moshika-rag-candle-bf16`) formats under CC-BY 4.0 (README.md:49-54).
- Running locally needs Python ≥3.10 (3.12 recommended), a 24GB-class GPU for the PyTorch front end since quantization is unsupported, and a recent Rust toolchain plus CUDA/`nvcc` for the Rust backend (README.md:58-71).

## 2. [[wiki/02-top-level-files|Top-level files]]
**In one sentence:** The repo root defines hygiene, lint, licensing, dev tooling, and Swarm deployment for the Moshi-RAG system.
## Key points
- `.gitignore` (199 lines) excludes Python, packaging, test, IDE, and ML/media artifacts plus local secrets and outputs (`.gitignore:1-4`, `.gitignore:168-179`, `.gitignore:186-187`).
- `.pre-commit-config.yaml` (14 lines) wires `ruff-check`/`ruff-format` at `rev: v0.15.8` and a local `cargo fmt --all --manifest-path rust/Cargo.toml` hook (`.pre-commit-config.yaml:1-5`, `.pre-commit-config.yaml:9-12`).
- `deploy.sh` (8 lines) cleans `./moshi/.venv ./moshi/dist ./rust/target`, rebuilds/pushes via `swarm-config.yaml`, and redeploys the `moshi-rag` stack over SSH (`deploy.sh:1`, `deploy.sh:3-4`, `deploy.sh:7`).
- Dual licensing is vendored as `LICENSE-APACHE` (202 lines, Version 2.0) and `LICENSE-MIT` (24 lines, AS-IS) (`LICENSE-APACHE:1`, `LICENSE-MIT:1`).
- `requirements-dev.txt` pins only three dev tools: `pre-commit>=3.8`, `pyright>=1.1`, `flake8>=7.1` (`requirements-dev.txt:1-3`).
- `swarm-config.yaml` (148 lines) orchestrates `traefik`, `frontend` (from `client/`), `backend` (from `moshi/`), `arc_encoder` (via `Dockerfile.arc_encoder`), plus `agent`/`portainer` monitoring (`swarm-config.yaml:1`, `swarm-config.yaml:35-37`, `swarm-config.yaml:49-51`, `swarm-config.yaml:85-88`, `swarm-config.yaml:108-118`).
- Routing exposes `frontend` on `PathPrefix("/")` (priority 10) and `backend` on `PathPrefix("/api")` (priority 100) behind TLS with Let's Encrypt, while `backend` and `arc_encoder` each reserve one `gpu` (`swarm-config.yaml:41-46`, `swarm-config.yaml:71-82`, `swarm-config.yaml:19`).

## The system in five moves
1. MoshiRAG starts as a compact full-duplex speech LM on Moshi/Mimi that must gain factuality without losing real-time interactivity.
2. It splits into a continuously listening/speaking Moshi front end and a parallel asynchronous text-in/text-out retrieval back end.
3. A predicted retrieval trigger sends combined inner-monologue plus streaming-ASR context to the back end while the front end bridges the gap with lightweight pre-RAG content.
4. Returned reference text is encoded and streamed back into Moshi so later response segments are grounded in external knowledge.
5. This ships as the Moshika-voiced bf16 weights (PyTorch and Rust/Candle, CC-BY 4.0) with 24GB-class GPU and local-LLM runtime requirements.
6. The repo root wraps the system in hygiene, ruff/cargo-fmt lint, MIT/Apache licensing, minimal dev pins, and a Traefik-fronted Swarm stack deploying frontend, backend, and arc_encoder with GPU reservations.
