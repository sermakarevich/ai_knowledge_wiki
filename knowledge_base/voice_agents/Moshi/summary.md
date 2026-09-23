# Technical Analysis: kyutai-labs/moshi

**Repository:** https://github.com/kyutai-labs/moshi
**Version analyzed:** unknown
**Date:** 2026-09-22
**Wiki:** [[index]]

## 1. Overview / What Problem It Solves

The problem space is real-time full-duplex spoken dialogue: a system must listen and speak simultaneously with low enough latency that interruption, overlap, and backchanneling work, while preserving voice quality at low bitrate and keeping semantic coherence. Half-duplex turn-taking pipelines (STT → LLM → TTS) cannot do this; they serialize listening and speaking and accumulate stage latency.

The repo addresses it by shipping Moshi, a speech-text foundation model, together with Mimi, a streaming neural audio codec, as three interchangeable inference stacks plus a web client. Moshi models two concurrent audio streams (Moshi speaking, user speaking) and predicts text tokens for its own speech as an inner monologue to improve generation quality (README.md:41-43). Mimi compresses 24 kHz audio to a 12.5 Hz representation at 1.1 kbps with 80 ms frame-size latency, keeping the autoregressive step rate near the text-token rate of ~3-4 Hz (README.md:55-63). Theoretical latency is 160 ms (80 ms frame + 80 ms acoustic delay) with ~200 ms practical overall latency on an L4 GPU (README.md:45-46). The primary user is a researcher or deployment engineer building a live voice-dialogue demo: PyTorch (`moshi/`) for research and tinkering, MLX (`moshi_mlx/`) for on-device Mac/iPhone inference, Rust (`rust/`) for production, and `client/` as the demo web UI (README.md:20-29).

## 2. High-Level Architecture

```text
Microphone / Browser ──► Web UI client (`client/`)
        │                          │
        │ PCM 24 kHz               │ echo cancellation (web UI)
        ▼                          ▼
PyTorch server (`moshi/`) ◄──► Mimi encoder/decoder ◄──► Moshi Temporal (7B) + Depth Transformer
        │                          │
        │ alternate stacks         │
        ├─► MLX local (`moshi_mlx/`) ──► local speaker/mic
        │                          │
        └─► Rust backend (`rust/`) ──► Candle inference + `rustymimi` bindings
                                       │
                                       ▼
                              Swarm deploy: traefik ─► frontend (:5173, `/`) ─► backend (:8998, `/api`)
```

Data-flow narrative:

1. Capture and transport. The web UI in `client/` captures microphone audio and streams it to whichever backend is running; the PyTorch interactive mode requires a model server plus web UI or CLI client (README.md:121-125). The web UI is recommended because its additional echo cancellation aids model quality (README.md:202-204).
2. Streaming tokenization. Mimi encodes 24 kHz input into 12.5 Hz tokens in a fully streaming manner (README.md:55-58). At inference the user audio stream comes from audio input while the Moshi stream is sampled from model output (README.md:49-50).
3. Dual-stream language modeling. Per timestep a small Depth Transformer models inter-codebook dependencies and a large 7B-parameter Temporal Transformer models temporal dependencies across the two audio streams plus the text inner monologue (README.md:41-45).
4. Synthesis and playback. The Moshi output stream is decoded by Mimi and played back; total budget is 80 ms frame plus 80 ms acoustic delay (160 ms theoretical, ~200 ms practical on L4) (README.md:45-46).
5. Deployment routing. In production the Swarm topology terminates TLS at traefik (80/443, Let's Encrypt) and routes `/` to the frontend (port 5173) and `/api` to the GPU backend (port 8998) (swarm-config.yml:1-70).
6. Checkpoint loading. Each stack pulls its own quantized or full-precision checkpoint family (PyTorch bf16/int8, MLX int4/int8/bf16, Rust/Candle int8/bf16) from per-backend HuggingFace repos, with Mimi bundled in each model repo in the same checkpoint format (README.md:83-90).

Persistent state lives in four places: (a) model checkpoint files on disk / HuggingFace cache (shared `hf-cache` volume in swarm-config.yml:98-116; `*.safetensors` ignored in git per .gitignore:182), (b) the fixed-size conversational buffer that bounds MLX/Rust sessions (FAQ.md:28-33), (c) deployment state in Swarm volumes (`letsencrypt`, `portainer_data`, `hf-cache`, `uv-cache` per swarm-config.yml:98-116), and (d) TLS key material (`*.pem` per .gitignore:189; self-signed cert generation per FAQ.md:46-48). No database is defined in the wiki pages.

## 3. The Dual-Stream Codebook Dialogue

The central abstraction is a timestep-aligned triple: user audio tokens, Moshi audio tokens, and Moshi text tokens (inner monologue). Representation is discrete: Mimi emits codebook tokens at 12.5 Hz from 24 kHz audio at 1.1 kbps, a rate chosen to stay close to the text-token rate (~3-4 Hz) so autoregressive steps stay bounded (README.md:55-63). Semantic grounding comes from distilling the first codebook against a WavLM self-supervised representation; quality at low bitrate comes from adversarial plus feature-matching loss only (README.md:64-67). The encoder/decoder each contain a Transformer with strides reaching 12.5 Hz overall, building on SoundStream and EnCodec (README.md:60-62).

Named kinds and types, with file:line:

- User audio stream — live input tokens; inference sources it from audio input (README.md:49-50).
- Moshi audio stream — sampled output tokens; inference samples it from model output (README.md:49-50).
- Text inner monologue — Moshi's own speech predicted as text tokens alongside audio; stated to improve generation quality (README.md:41-43).
- Depth Transformer — small per-timestep model of inter-codebook dependencies (README.md:44-45).
- Temporal Transformer — large 7B-parameter model of temporal dependencies (README.md:44-45).
- Mimi codec — streaming tokenizer/detokenizer triple (encoder, quantizer/codebooks, decoder) with 80 ms frame-size latency (README.md:55-58).
- Checkpoint voices — Moshiko (male synthetic voice), Moshika (female synthetic voice), and Mimi proper (README.md:77-80).
- Backend-specific weight formats — PyTorch bf16/int8 (experimental q8), MLX q4/q8/bf16, Rust/Candle q8/bf16 (README.md:85-90).

Key queries are selection queries over this triple: which checkpoint voice, which backend format, and which latency/quality tradeoff. Verbatim (README.md:23-29):

```text
- **[PyTorch](#pytorch-implementation): for research and tinkering.** The code is in the [`moshi/`](moshi/) directory.
- **[MLX](#mlx-implementation-for-local-inference-on-macos): for on-device inference on iPhone and Mac.** The code is in the [`moshi_mlx/`](moshi_mlx/) directory.
- **[Rust](#rust-implementation): for production.** The code is in the [`rust/`](rust/) directory.
```

## 4. LLM / External Service Integration

The repo calls no third-party LLM or paid inference API; Moshi itself is the generative model and all decoding is local to whichever stack is running. External services are infrastructure, not model providers:

- HuggingFace Hub (required at model-fetch time): per-backend repos for `moshika`/`moshiko` in PyTorch (`-bf16`, `-q8` experimental), MLX (`-q4`, `-q8`, `-bf16`), and Candle (`-q8`, `-bf16`) (README.md:85-90). Selected via `--hf-repo` (PyTorch server, README.md:142; MLX local, README.md:161-167) or the `"hf_repo"` key in Rust config (README.md:188-190).
- Gradio tunnel (optional): `python -m moshi.server --gradio-tunnel` exposes a remote-GPU server to a local browser microphone; traffic routes through the US and can add up to 500 ms from Europe; `--gradio-tunnel-token` pins a reusable address (README.md:133-140).
- Let's Encrypt via traefik (production): `acme.email=gabriel@kyutai.org`, HTTP→HTTPS redirect, entrypoints 80/443 (swarm-config.yml:1-33).
- Docker registry + SSH deploy host (operations): images tagged by short `COMMIT_SHA` and deployed over SSH to `root@moshi-chat.kyutai.org` (deploy.sh:3-7).

Env vars and config keys attested in the wiki:

| Name | Required? | Purpose |
|---|---|---|
| `COMMIT_SHA` | build-time (set by `deploy.sh`) | image tag for frontend/backend Swarm images (deploy.sh:3-7) |
| `NO_TORCH_COMPILE=1` | deployment default | disables torch.compile in Swarm backend service (swarm-config.yml:47-70) |
| `--hf-repo` / `"hf_repo"` | optional (has defaults) | selects Moshika vs Moshiko checkpoint and precision (README.md:142; README.md:188-190) |
| `--gradio-tunnel` / `--gradio-tunnel-token` | optional | remote-microphone tunneling and stable tunnel address (README.md:133-140) |
| `-q 4\|8` | required with MLX | must match the `--hf-repo` quantization (README.md:161-167) |

## 5. The Full-Duplex Inference Pipeline

Primary workflow is live spoken dialogue through one of three backends behind the web UI. Each step cites the wiki-grounded location:

1. Install the stack — `pip install -U moshi` for PyTorch, `pip install -U moshi_mlx` for MLX, `pip install rustymimi` for the Rust Mimi Python bindings (README.md:99-107). Editable installs from git subdirectories are the alternative (README.md:99-107). Needs at least Python 3.10, 3.12 recommended (README.md:96).
2. Start the PyTorch server — `python -m moshi.server [--gradio-tunnel] [--hf-repo kyutai/moshika-pytorch-bf16]` (README.md:124-125). Serves the web UI at `http://localhost:8998` (README.md:132). SSH-forward remote port 8998 (`-L`) or use `--gradio-tunnel` when the GPU is remote (README.md:133-140).
3. Attach a client — `python -m moshi.client [--url URL_TO_GRADIO]` for the barebones CLI, or a browser on the served web UI (README.md:124-125). CLI has no echo cancellation and no lag-compensating frame skipping (README.md:152-153). Non-localhost plain-HTTP servers may lose browser microphone access, which some browsers allow only over https (README.md:144-146).
4. Run the MLX local path instead (Mac) — `python -m moshi_mlx.local -q 4` or `-q 8`, with `--hf-repo` matched to `-q` (README.md:161-167). `python -m moshi_mlx.local_web` serves the web UI at `http://localhost:8998` (README.md:173-174). Same barebone CLI caveats apply (README.md:170-171).
5. Run the Rust production path instead — from `rust/`: `cargo run --features cuda --bin moshi-backend -r -- --config moshi-backend/config.json standalone` (README.md:179-184); `--features metal` on macOS (README.md:186); `config-q8.json` for the quantized model and `"hf_repo"` key to switch voices (README.md:188-190). Wait for `standalone worker listening`, then open the web UI over `https://localhost:8998` and accept the browser warning (README.md:192-198).
6. Operate and deploy — `deploy.sh:3-7` builds/pushes the Swarm stack and deploys it to `moshi-chat.kyutai.org`; traefik routes `/` to the frontend and `/api` to the GPU backend (swarm-config.yml:34-70). Prefer the web UI in production for its echo cancellation (README.md:202-204).

## 6. Key Files

| File | Lines | What It Does |
|---|---|---|
| `README.md` | ~208 (cited 14-208) | Architecture, Mimi/Moshi design, checkpoints, all three backend runbooks |
| `moshi/` | dir | PyTorch research stack: streaming tokenizer (mimi) + language model (moshi) API, server/client (README.md:121-122) |
| `moshi_mlx/` | dir | MLX on-device stack for iPhone/Mac, local and local_web entry points (README.md:24; README.md:161-174) |
| `rust/` | dir | Production Rust stack incl. Rust Mimi and `rustymimi` bindings (README.md:25-27; README.md:179-198) |
| `client/` | dir | Web UI demo client with echo cancellation; also Swarm frontend build context (README.md:29; swarm-config.yml:34-46) |
| `FAQ.md` | 65 | Operational FAQ: language, dataset, quantization, 5-min buffer, GPU sizing, certs (FAQ.md:5-52) |
| `swarm-config.yml` | 116 | Swarm topology: traefik, frontend, GPU backend, Portainer, encrypted overlays/volumes (swarm-config.yml:1-116) |
| `deploy.sh` | 7 | Build/push/deploy over SSH with `COMMIT_SHA` tag (deploy.sh:3-7) |
| `.pre-commit-config.yaml` | 39 | Five local hooks: flake8/tests for `moshi`, ruff/format/pyright for `moshi_mlx` (.pre-commit-config.yaml:7-39) |
| `requirements-dev.txt` | 3 | Dev tooling pins: pre-commit, pyright, flake8 (requirements-dev.txt:1-3) |
| `.gitignore` | ~202 | Python template plus `*.safetensors`, audio, traces, pem, token exclusions (.gitignore:181-202) |
| `.dockerignore` | 1 | Excludes `moshi/.venv/*` from build contexts (.dockerignore:1) |
| `LICENSE-APACHE` | 202 | Apache-2.0 grant text (LICENSE-APACHE:1-202) |
| `LICENSE-MIT` | 24 | MIT grant text (LICENSE-MIT:1-24) |

## 7. Dependencies

Required runtime/install dependencies first, then dev and deployment:

| Package | Version constraint | Purpose |
|---|---|---|
| `moshi` (PyPI) | `pip install -U moshi` (no pinned version in wiki) | PyTorch research stack distribution (README.md:99-107) |
| `moshi_mlx` (PyPI) | `pip install -U moshi_mlx` (no pinned version in wiki) | MLX on-device stack distribution, best with Python 3.12 (README.md:99-110) |
| `rustymimi` (PyPI) | `pip install rustymimi` (no pinned version in wiki) | Rust Mimi implementation with Python bindings (README.md:99-107) |
| `python` | `>=3.10`, `3.12` recommended | interpreter floor and recommended version (README.md:96) |
| Rust toolchain | `recent` (no pinned version in wiki) | builds Rust backend; CUDA builds additionally need `nvcc` (README.md:116-117) |
| `pre-commit` | `pre-commit>=3.8` | hook runner for lint/test/typecheck (requirements-dev.txt:1-3) |
| `pyright` | `pyright>=1.1` | typecheck for `moshi_mlx` hook (requirements-dev.txt:1-3) |
| `flake8` | `flake8>=7.1` | lint for `moshi` hook (requirements-dev.txt:1-3) |
| `traefik` | `traefik:v3.6.7` | Swarm edge router, TLS, Let's Encrypt (swarm-config.yml:1-33) |
| `portainer/agent` | `portainer/agent:lts` | Swarm monitoring agent, global mode (swarm-config.yml:74-96) |
| `portainer/portainer-ce` | `portainer/portainer-ce:lts` | monitoring UI on 9443 (swarm-config.yml:74-96) |
| `ruff` (via `uvx`) | unpinned in wiki | lint and format-check for `moshi_mlx` hooks (.pre-commit-config.yaml:7-39) |
| `pytest` | unpinned in wiki | test runner invoked by `tests-moshi` hook (.pre-commit-config.yaml:7-39) |

## 8. CLI / Usage Surface

Entry points:

| Command | Stack | Purpose |
|---|---|---|
| `python -m moshi.server [--gradio-tunnel] [--hf-repo REPO]` | PyTorch | start interactive model server (README.md:124-125) |
| `python -m moshi.client [--url URL_TO_GRADIO]` | PyTorch | barebones CLI client (README.md:124-125) |
| `python -m moshi_mlx.local -q 4\|8 [--hf-repo REPO]` | MLX | local quantized inference (README.md:161-167) |
| `python -m moshi_mlx.local_web` | MLX | serve web UI at `http://localhost:8998` (README.md:173-174) |
| `cargo run --features cuda --bin moshi-backend -r -- --config moshi-backend/config.json standalone` | Rust | production backend; `metal` on macOS, `config-q8.json` for q8 (README.md:179-190) |
| `bash deploy.sh` | ops | build/push/deploy Swarm stack to `moshi-chat.kyutai.org` (deploy.sh:3-7) |

Commands and flags:

| Flag / arg | Command | Effect |
|---|---|---|
| `--gradio-tunnel` | `moshi.server` | expose remote GPU via Gradio tunnel for local mic; +latency from Europe up to 500 ms (README.md:133-140) |
| `--gradio-tunnel-token` | `moshi.server` | pin reusable tunnel address (README.md:133-140) |
| `--hf-repo` | `moshi.server`, `moshi_mlx.local` | select checkpoint (default Moshika bf16-class repo); MLX `-q` must match repo (README.md:142; README.md:161-167) |
| `-q 4\|8` | `moshi_mlx.local` | weight quantization width (README.md:161-167) |
| `--url` | `moshi.client` | point CLI at Gradio tunnel URL (README.md:124-125) |
| `--features cuda\|metal` | `cargo run` | GPU backend selection; `metal` on macOS (README.md:179-186) |
| `--config moshi-backend/config.json\|config-q8.json` | `moshi-backend` | full vs quantized server config (README.md:188-190) |

Env-var and config tables:

| Variable | Set where | Effect |
|---|---|---|
| `COMMIT_SHA` | `deploy.sh:3-7` (from `git rev-parse --short HEAD`) | tags frontend/backend images |
| `NO_TORCH_COMPILE=1` | `swarm-config.yml:47-70` | disables torch.compile in backend service |

| Config key/file | Stack | Effect |
|---|---|---|
| `"hf_repo"` | Rust `config.json` / `config-q8.json` | selects Moshika vs Moshiko pretrained model (README.md:188-190) |
| `/api` route, port `8998`, 1 GPU reservation | `swarm-config.yml:47-70` | backend routing and GPU scheduling |
| `/` route, port `5173` | `swarm-config.yml:34-46` | frontend routing |

## 9. Extensibility Points

- New inference behavior or research variant: extend the PyTorch stack in `moshi/` (research and tinkering stack per README.md:23); lint with the `flake8-moshi` hook and cover with the `tests-moshi` (`cd moshi && pytest tests`) hook (.pre-commit-config.yaml:7-39).
- On-device / Apple-silicon optimization: extend `moshi_mlx/`; must satisfy `ruff-moshi_mlx`, `ruff-format-moshi_mlx`, and `pyright-moshi_mlx` hooks (.pre-commit-config.yaml:7-39). Requires care past 4-bit quantization, which degrades quality sharply (FAQ.md:19-22).
- Production serving path: extend the Rust backend in `rust/` (production stack per README.md:25-27), including the Rust Mimi exposed via `rustymimi` bindings; add support files under `rust/` and select configs via `moshi-backend/config.json` vs `config-q8.json` (README.md:188-190).
- Demo UX (echo cancellation, latency compensation): extend `client/` (web UI client per README.md:29); the CLI clients are explicitly barebones with no echo cancellation or lag-compensating frame skipping (README.md:152-153; README.md:170-171), so improvements belong in the web client or protocol handlers shared with Rust/Python CLIs (README.md:206-208).
- New voice or personality: fine-tune in the separate `kyutai-labs/moshi-finetune` repo, not here; in-repo voice change without fine-tuning is stated as not currently supported (README.md:29-31; FAQ.md:5-7; FAQ.md:15-17).
- Deployment topology: extend `swarm-config.yml` services, GPU reservations, routes, and volumes (swarm-config.yml:1-116); ship via `deploy.sh` (deploy.sh:3-7).
- Related-architecture reuse: Hibiki simultaneous translation (`kyutai-labs/hibiki`) and Kyutai TTS/STT (`kyutai-labs/delayed-streams-modeling`) reuse the multi-stream architecture (README.md:35-37); cross-pollination belongs upstream in the shared modeling, not in backend glue.

## 10. Limitations and Gotchas

- **MLX and Rust stop after ~5 minutes by design.** Both use a fixed buffer; only PyTorch runs unbounded, and even it degrades without an attention sink (FAQ.md:28-33).
- **Quantized PyTorch is unsupported and small-GPU operation is narrow.** Beyond-4-bit quantization gives a dramatic quality drop (FAQ.md:19-22); quantized PyTorch is unsupported and the suggested fallback is the Rust int8/CUDA backend (FAQ.md:24-26). 12 GB GPUs are possible per issue #54 but 8 GB is stated as not possible (FAQ.md:50-52); unquantized PyTorch needs ~24 GB (README.md:112-114).
- **Remote-microphone setup is fragile.** Non-localhost plain HTTP can lose browser microphone access (https-only in some browsers) (README.md:144-146); the `Cannot read properties of undefined (reading 'addModule')` blank-server symptom means the same remote-http audio block and is fixed by SSH-tunneling port 8998 to localhost (FAQ.md:35-44). Gradio tunneling works but adds up to 500 ms from Europe (README.md:133-140).
- **Platform and toolchain coupling is tight.** No official Windows support; MLX is tested on MacBook Pro M3; non-3.12 Python may fail installing `moshi_mlx` or `rustymimi` without a Rust toolchain or a 3.12 switch (README.md:109-114). Rust GPU builds need a recent toolchain plus CUDA `nvcc` (README.md:116-117).
- **Training data and English-only scope.** Moshi only speaks English and the pre-training dataset will not be released (FAQ.md:9-13); voice/personality change requires unsupported fine-tuning (FAQ.md:15-17).
- **CLI clients hide no latency.** Both Python and MLX CLI clients lack echo cancellation and lag-compensating frame skipping, so measured quality lags the web UI (README.md:152-153; README.md:170-171; README.md:202-204).

## 11. How It Compares to Alternatives

- SoundStream / EnCodec (Google/Meta neural codecs): the direct codec predecessors Mimi builds on by adding encoder/decoder Transformers and 12.5 Hz strides (README.md:60-62). They establish the streaming-codec baseline; Mimi differentiates on lower rate (12.5 Hz, 1.1 kbps), WavLM-distilled semantics in the first codebook, and adversarial-plus-feature-matching-only training (README.md:55-67).
- SpeechTokenizer (50 Hz, 4 kbps) / SemantiCodec (50 Hz, 1.3 kbps): non-streaming reference points the README compares against; Mimi claims to outperform both while streaming at a quarter of their frame rate (README.md:55-58).
- Hibiki (`kyutai-labs/hibiki`): sibling project reusing Moshi's multi-stream architecture for simultaneous speech translation rather than open dialogue (README.md:35-37). Shares machinery, differs in task head and data regime.
- Kyutai TTS/STT (`kyutai-labs/delayed-streams-modeling`): sibling reuse of the same multi-stream modeling for synthesis/recognition instead of full-duplex conversation (README.md:35-37). Fine-tuning entry point `kyutai-labs/moshi-finetune` is adjacent rather than competing (README.md:29-31; FAQ.md:5-7).

Positioning sentence: among streaming codecs and dialogue stacks, Moshi occupies the full-duplex niche — Mimi trades raw bitrate for streamability plus distilled semantics, and the three-backend packaging trades a single canonical server for research (PyTorch), on-device (MLX), and production (Rust) targets sharing one checkpoint lineage.

## Appendix: Selected Code Snippets

1. Backend selection (`README.md:23-29`):

```text
- **[PyTorch](#pytorch-implementation): for research and tinkering.** The code is in the [`moshi/`](moshi/) directory.
- **[MLX](#mlx-implementation-for-local-inference-on-macos): for on-device inference on iPhone and Mac.** The code is in the [`moshi_mlx/`](moshi_mlx/) directory.
- **[Rust](#rust-implementation): for production.** The code is in the [`rust/`](rust/) directory.
```

2. Install matrix (`README.md:99-107`):

```bash
pip install -U moshi      # moshi PyTorch, from PyPI
pip install -U moshi_mlx  # moshi MLX, from PyPI, best with Python 3.12.
pip install -U -e "git+https://git@github.com/kyutai-labs/moshi.git#egg=moshi&subdirectory=moshi"
pip install -U -e "git+https://git@github.com/kyutai-labs/moshi.git#egg=moshi_mlx&subdirectory=moshi_mlx"
pip install rustymimi  # mimi, rust implementation with Python bindings from PyPI
```

3. Swarm deploy (`deploy.sh:1-7`):

```text
set -ex

export COMMIT_SHA=$(git rev-parse --short HEAD)

docker compose -f swarm-config.yml build --push

docker -H ssh://root@moshi-chat.kyutai.org stack deploy -c swarm-config.yml --with-registry-auth moshi
```

4. HTTPS self-signed cert workaround (`FAQ.md:46-48`):

```text
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes -subj "/CN=localhost"
```
