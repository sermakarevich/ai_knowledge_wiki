> [[index|Wiki]] | [[summary|Summary]]
# kyutai-labs/moshi — Digest
## 1. [[wiki/01-overview|Overview]]
**In one sentence:** Moshi is a full-duplex speech-text foundation model with the Mimi streaming codec, shipped as three inference stacks (PyTorch, MLX, Rust) plus a web UI client.
## Key points
- Moshi is a speech-text foundation model and full-duplex spoken dialogue framework built on the Mimi streaming neural audio codec (README.md:14-15).
- The repo holds three inference stacks: PyTorch in `moshi/` for research, MLX in `moshi_mlx/` for on-device Mac/iPhone, and Rust in `rust/` for production including a Rust Mimi with `rustymimi` Python bindings (README.md:20-27).
- The web UI client used by the Moshi demo lives in `client/`, and fine-tuning lives in the separate `kyutai-labs/moshi-finetune` repo (README.md:29-31).
- Moshi models two audio streams (Moshi + user) plus text tokens for its own speech as an inner monologue, using a small Depth Transformer per timestep and a large 7B-parameter Temporal Transformer (README.md:41-45).
- Theoretical latency is 160ms (80ms Mimi frame size + 80ms acoustic delay), with practical overall latency as low as 200ms on an L4 GPU (README.md:45-46).
- Mimi processes 24 kHz audio to a 12.5 Hz representation at 1.1 kbps in fully streaming manner (80ms frame-size latency), using encoder/decoder Transformers, 12.5 Hz strides, WavLM distillation into the first codebook, and adversarial + feature-matching loss only (README.md:55-67).
- Three checkpoints are released — Moshiko (male synthetic voice), Moshika (female synthetic voice), and Mimi — under CC-BY 4.0, with per-backend HuggingFace repos and quantization variants (README.md:77-92).
## 2. [[wiki/02-top-level-files|Top-level-files]]
**In one sentence:** The top-level files define repo hygiene (ignores), licensing, dev/test hooks, the Docker Swarm deployment topology, and the user-facing FAQ.
## Key points
- `.dockerignore` excludes only `moshi/.venv/*` from Docker build contexts (`.dockerignore:1`).
- `.gitignore` is a standard Python template plus Moshi-specific entries for model audio/artifacts (`*.safetensors` at `.gitignore:182`, `*.wav` at `.gitignore:183`, `*.mp3` at `.gitignore:191`), traces (`trace*.json` at `.gitignore:184`, `timings.json` at `.gitignore:197`, `mlx-trace.json` at `.gitignore:198`), and secrets/config (`*.pem` at `.gitignore:189`, `/moshi-demo/config.sh` at `.gitignore:193`, `/scripts/token.txt` at `.gitignore:199`).
- `.pre-commit-config.yaml` defines five local hooks: `flake8-moshi`, `tests-moshi`, `ruff-moshi_mlx`, `ruff-format-moshi_mlx`, `pyright-moshi_mlx` (`.pre-commit-config.yaml:7-39`).
- `deploy.sh` builds/pushes the Swarm stack and deploys it over SSH to `root@moshi-chat.kyutai.org` using short `COMMIT_SHA` as the image tag (`deploy.sh:3-7`).
- `FAQ.md` states Moshi is English-only, training data will not be released, finetuning lives in `moshi-finetune`, quantized PyTorch is unsupported, and MLX/Rust stop after ~5 min due to a fixed buffer (`FAQ.md:5-7`, `FAQ.md:11-13`, `FAQ.md:24-30`, `FAQ.md:33-36`).
- `swarm-config.yml` deploys `traefik` (80/443, Let's Encrypt), `frontend` (port 5173, path `/`), and `backend` (port 8998, path `/api`, 1 GPU reservation, `NO_TORCH_COMPILE=1`) plus Portainer monitoring (`swarm-config.yml:1-65`).
- Licensing is dual Apache-2.0 (`LICENSE-APACHE:1-202`) and MIT (`LICENSE-MIT:1-24`); dev tooling pins are `pre-commit>=3.8`, `pyright>=1.1`, `flake8>=7.1` (`requirements-dev.txt:1-3`).
## The system in five moves
1. Moshi frames spoken dialogue as joint modeling of two streaming audio channels plus an inner-monologue text stream over a low-rate Mimi codec.
2. Mimi compresses 24 kHz audio to 12.5 Hz tokens so the 7B Temporal plus per-step Depth Transformers can stay within a 160ms theoretical latency budget.
3. The same model ships as three inference stacks — PyTorch for research, MLX for on-device Mac/iPhone, Rust for production — with Moshiko/Moshika voice checkpoints per backend.
4. Day-to-day use runs through a model server plus web UI or CLI client, with port-forwarding, tunnel, and HTTPS workarounds for remote-GPU microphone access.
5. Repo hygiene, lint/test hooks, and the Docker Swarm topology (traefik + frontend + GPU backend) turn the research stacks into the deployed moshi-chat demo.
6. The FAQ bounds the system: English-only, no training-data release, finetuning elsewhere, no quantized PyTorch, and fixed-buffer 5-minute caps on MLX/Rust.
