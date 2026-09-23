# Technical Analysis: kyutai-labs/moshi-rag

**Repository:** https://github.com/kyutai-labs/moshi-rag
**Version analyzed:** unknown
**Date:** 2026-09-22
**Wiki:** [[index]]

## 1. Overview / What Problem It Solves

Full-duplex speech language models respond in real time but hallucinate on
factual questions, and naive retrieval blocks the audio stream while the
system waits for context. The repository addresses this with an asynchronous
front-end/back-end split: a Moshi-based full-duplex speech model sustains the
conversation while a parallel text-in/text-out retrieval back end fetches
reference material, which is then encoded and injected into Moshi as a
stream so later response segments are grounded without interrupting speech
(README.md:30-36). The primary user is a researcher or engineer deploying a
real-time voice assistant that must answer knowledge-intensive questions;
the repo ships both a PyTorch tree for experimentation (`moshi/`) and a Rust
tree for production (`rust/`), plus the web client (`client/`)
(README.md:21-26). Released weights are the Moshika female synthetic voice in
PyTorch bf16 (`kyutai/moshika-rag-pytorch-bf16`) and Rust/Candle bf16
(`kyutai/moshika-rag-candle-bf16`) under CC-BY 4.0 (README.md:49-54).

## 2. High-Level Architecture

```
User audio ──► Moshi front-end (full-duplex speech LM, moshi/)
│                  │
│                  ▼
│           <ret> trigger predicted
│                  │
│                  ├──► conversation continues (pre-RAG ack / coarse reply)
│                  │
│                  ▼
│           context assembly (Moshi inner-monologue text + streaming-ASR
│           user transcription) ──► async retrieval back end (LLM or search,
│                  text-in/text-out) ──► reference text
│                                            │
│                                            ▼
│                              reference encoder (server_conditioner)
│                                            │
│                                            ▼
│           Moshi conditioning path ◄── encoded reference stream (summed
│                  with other stream embeddings over time steps)
│                  │
│                  ▼
└── grounded speech reply ──► web client (client/, localhost:8998)
```

Data flow in five steps. (1) The front end listens and speaks continuously
as a full-duplex Moshi model (README.md:30-34). (2) On predicting a
retrieval trigger token, it ships conversation context — Moshi
inner-monologue text combined with streaming-ASR transcription — to the
back end while the dialogue continues, optionally emitting lightweight
pre-RAG acknowledgments (README.md:34-36). (3) The back end, LLM-based or
search-based, returns reference text (README.md:36). (4) The reference text
encoder (`server_conditioner`) encodes the reference and injects it into
Moshi's conditioning path as a stream, summed with other stream embeddings
over several time steps (README.md:36; `streams.png`, README.md:38-44).
(5) Subsequent response segments are grounded in the injected reference and
streamed to the web UI (README.md:36, README.md:163). Persistent state lives
outside the processes: model weights/checkpoints pulled from Hugging Face
(`hf://kyutai/moshika-rag-pytorch-bf16/...`), served-model caches and named
volumes (`/scratch/models:/models`, `huggingface-cache`, `uv-cache`) in the
Swarm deployment (swarm-config.yaml:63-67, swarm-config.yaml:130-136); the
wiki documents no database or on-disk conversation store.

## 3. The Retrieval-Conditioned Stream

The central concept is a retrieval-conditioned audio/text stream: dialogue
continues uninterrupted while external knowledge is fetched asynchronously
and merged into generation. Representation is threefold. First, a trigger:
the `<ret>` token predicted by the front end initiates the back-end call
(`front_back_end.png`, README.md:38-44). Second, a context object assembled
from two text sources — the text predicted by Moshi inner monologue and the
user transcription from the streaming ASR component (README.md:36). Third,
an injected conditioning stream: the returned reference text is encoded and
fed back into Moshi as a stream whose representation is summed with other
stream embeddings over several time steps (`streams.png`,
README.md:38-44). Named kinds, with wiki citations: the **front end**
(full-duplex Moshi speech model, README.md:30-32); the **retrieval back
end** (text-in/text-out, LLM-based or search-based, README.md:36); the
**reference text conditioner** (`reference_with_time`, started via
`server_conditioner`, README.md:110-119); **retrieval profiles** (`id`,
`base_url`, `model`, optional `api_key`, `prompt_style`, README.md:154);
**prompt styles** (`original`, `simplified`, README.md:156). Key mechanism,
verbatim as relayed by the wiki:

> The back end is text-in/text-out and can be implemented with different retrieval methods (LLM-based retrieval or search-based retrieval, etc). The retrieval back end takes conversation context (derived by combining the text predicted by Moshi inner monologue and the user transcription predicted by a streaming ASR component) as inputs, and then returns the reference text. Once the retrieval is completed, the reference text is encoded and injected back into Moshi as a stream, allowing later response segments to be grounded in external knowledge without interrupting the ongoing conversation. (README.md:36)

## 4. LLM / External Service Integration

The repo calls external LLM and speech services over HTTP/WebSocket; there
is no vendored retrieval model. The retrieval back end is any
OpenAI-compatible chat API: a local vLLM instance is recommended
(`vllm serve google/gemma-3-27b-it --host 0.0.0.0 --port 8002`,
README.md:79-85), and online APIs are supported by setting `LLM_BASE_URL`,
`LLM_API_KEY`, `LLM_MODEL_NAME` with preference for a low-latency provider
(README.md:87). Multiple backends are configured through
`MOSHI_RETRIEVAL_LLMS_JSON`, which overrides the single-backend variables;
each profile carries `id`, `base_url`, `model`, optional `api_key`, and
optional `prompt_style`, with exactly one `default: true` profile as
fallback when two or more are defined (README.md:138-157). The streaming
ASR leg defaults to a local STT and optionally uses Gradium over
`wss://eu.api.gradium.ai/api/speech/asr` when `--gradium-stt` is passed
(README.md:96-108). The reference conditioner is an internal HTTP service
(`REFERENCE_ENCODER_URL`, e.g. `http://localhost:8001`) that the main server
calls to encode retrieved text (README.md:100-108). Required calls at
runtime: retrieval LLM on every RAG trigger, and the reference encoder;
optional: Gradium STT (without the flag, local STT is used). Env vars
(`LLM_BASE_URL`, `LLM_API_KEY`, `LLM_MODEL_NAME`,
`MOSHI_RETRIEVAL_LLMS_JSON`, `REFERENCE_ENCODER_URL` / `ARC_ENCODER_URL`,
`STT_URL`, `STT_API_KEY`, `HF_TOKEN`/`HUGGING_FACE_HUB_TOKEN`) are the full
integration surface (README.md:100-108; swarm-config.yaml:53-60).

## 5. The Asynchronous Retrieval Dialogue Loop

The primary workflow is the trigger → retrieve → encode → inject loop
across two cooperating processes. The wiki documents it at process and
command level, not function level, so steps cite the README ranges the wiki
provides. (1) Serve a retrieval LLM, locally via vLLM on port 8002 or via
an online OpenAI-compatible endpoint, and export `LLM_BASE_URL`,
`LLM_API_KEY`, `LLM_MODEL_NAME` (README.md:79-87). (2) Start the reference
encoder with `python -m moshi.moshi.server_conditioner --config
hf://kyutai/moshika-rag-pytorch-bf16/config.json --moshi-weight
hf://kyutai/moshika-rag-pytorch-bf16/model.safetensors --conditioner
reference_with_time --port 8001` (README.md:110-119). (3) Start the main
server with `python -m moshi.moshi.server`, pointing `REFERENCE_ENCODER_URL`
at the conditioner and passing STT/LLM variables, so that on each RAG
trigger it calls the retrieval API over HTTP while continuing to speak
(README.md:91-96, README.md:121-136). (4) For multi-backend setups, export
`MOSHI_RETRIEVAL_LLMS_JSON` to select and fail over between retrieval
profiles instead of the single-backend variables (README.md:138-157).
(5) For offline batch use, run `python -m moshi.moshi.run_inference
--input-dir INPUT_DIR --output-dir OUTPUT_DIR` over a folder of WAVs to
produce output WAVs plus JSON logs (README.md:179). (6) Serve the client
from `./client/dist` (or the Swarm `frontend` service) on port 8998
(README.md:107-112, README.md:163; swarm-config.yaml:35-46).

## 6. Key Files

| File | Lines | What It Does |
|---|---|---|
| `README.md` | n/a (wiki cites to README.md:196) | System design, models, requirements, all run instructions |
| `moshi/` | dir | PyTorch implementation for research/experimentation (README.md:21-24, README.md:75) |
| `rust/` | dir | Rust/Candle implementation for production use (README.md:21-24, README.md:196) |
| `client/` | dir | Web UI client, served as static `./client/dist` (README.md:26, README.md:107-112) |
| `swarm-config.yaml` | 148 | Docker Swarm stack: traefik, frontend, backend, arc_encoder, monitoring (swarm-config.yaml:1-148) |
| `moshi/Dockerfile.arc_encoder` | n/a (referenced swarm-config.yaml:85-102) | Build file for the `arc_encoder` (reference encoder) image |
| `deploy.sh` | 8 | Cleans venv/dist/target, rebuilds/pushes, redeploys stack over SSH (deploy.sh:1-7) |
| `.pre-commit-config.yaml` | 14 | ruff-check/ruff-format at rev v0.15.8 plus local cargo fmt hook (.pre-commit-config.yaml:1-12) |
| `requirements-dev.txt` | 3 | Dev-only pins: pre-commit, pyright, flake8 (requirements-dev.txt:1-3) |
| `.gitignore` | 199 | Excludes Python, packaging, safetensors/media, secrets, outputs (.gitignore:1-198) |
| `LICENSE-APACHE` | 202 | Vendored Apache-2.0 text (LICENSE-APACHE:1-77) |
| `LICENSE-MIT` | 24 | Vendored MIT grant plus AS-IS disclaimer (LICENSE-MIT:1-23) |
| `front_back_end.png` | binary | Diagram: `<ret>` trigger, async back-end call, injection without interruption (README.md:38-44) |
| `streams.png` | binary | Diagram: text/audio token streams, summed retrieval embeddings (README.md:38-44) |

## 7. Dependencies

| Package | Version constraint | Purpose |
|---|---|---|
| python | `>=3.10` (3.12 recommended) | Runtime for PyTorch front end (README.md:58) |
| moshi (pip, git subdirectory) | `git+https://git@github.com/kyutai-labs/moshi-rag.git#egg=moshi&subdirectory=moshi` (unpinned) | PyTorch MoshiRAG package, editable install (README.md:61-64) |
| rustymimi | unpinned (`pip install rustymimi`) | Mimi codec Rust bindings from PyPI (README.md:61-64) |
| google/gemma-3-27b-it (via vLLM) | unpinned model id | Reference local retrieval LLM (README.md:79-85) |
| Rust toolchain + CUDA/nvcc | `recent` / GPU builds need `nvcc` | Rust backend build and GPU support (README.md:70-71) |
| pre-commit | `pre-commit>=3.8` | Dev: hook runner (requirements-dev.txt:1) |
| pyright | `pyright>=1.1` | Dev: type checking (requirements-dev.txt:2) |
| flake8 | `flake8>=7.1` | Dev: linting (requirements-dev.txt:3) |
| ruff-pre-commit | `rev: v0.15.8` | Dev: ruff-check/ruff-format hooks (.pre-commit-config.yaml:1-5) |
| traefik | `traefik:v3.6.7` | Swarm edge router with Let's Encrypt (swarm-config.yaml:3-28) |
| portainer/agent | `portainer/agent:lts` | Swarm monitoring agent (swarm-config.yaml:108-113) |
| portainer/portainer-ce | `portainer/portainer-ce:lts` | Swarm management UI (swarm-config.yaml:118-127) |

Runtime Python (`torch`, `safetensors`, server deps) and Rust (`Cargo.toml`)
dependency manifests are not covered by the wiki pages, so exact runtime
pins are unknown from this source.

## 8. CLI / Usage Surface

Entry points: `python -m moshi.moshi.server` (main full-duplex server),
`python -m moshi.moshi.server_conditioner` (reference encoder),
`python -m moshi.moshi.run_inference` (offline WAV-folder inference), `vllm
serve` (local retrieval LLM), and the Rust inference server run from within
`rust/` (README.md:79-96, README.md:179, README.md:196). Deployment entry
points are `deploy.sh` and `docker -H ssh://root@moshi-rag.kyutai.org stack
deploy -c ./swarm-config.yaml` (deploy.sh:1-7).

| Command | Purpose |
|---|---|
| `vllm serve google/gemma-3-27b-it --host 0.0.0.0 --port 8002` | Serve local retrieval LLM (README.md:79-85) |
| `python -m moshi.moshi.server_conditioner --config ... --moshi-weight ... --cuda-device 0 --conditioner reference_with_time --port 8001` | Start reference encoder (README.md:110-119) |
| `python -m moshi.moshi.server --gradio-tunnel --static "./client/dist" --init-active-speaker model --gradium-stt` | Start main server with UI and Gradium STT (README.md:121-136) |
| `python -m moshi.moshi.run_inference --input-dir INPUT_DIR --output-dir OUTPUT_DIR --max-consecutive-silence-frames 40` | Batch inference over WAVs to WAVs + JSON logs (README.md:179) |

| Env var | Role |
|---|---|
| `REFERENCE_ENCODER_URL` | Base URL of the reference conditioner, e.g. `http://localhost:8001` (README.md:100-108) |
| `STT_URL` / `STT_API_KEY` | Gradium streaming ASR endpoint and key; unneeded without `--gradium-stt` (README.md:100-108) |
| `LLM_BASE_URL` / `LLM_API_KEY` / `LLM_MODEL_NAME` | Retrieval LLM endpoint, key, model id (README.md:100-108) |
| `MOSHI_RETRIEVAL_LLMS_JSON` | Optional multi-backend profile array; overrides single-backend vars (README.md:138-157) |
| `ARC_ENCODER_URL` | In-stack conditioner URL `http://arc_encoder:80` (swarm-config.yaml:53-60) |
| `HF_TOKEN` / `HUGGING_FACE_HUB_TOKEN` | Checkpoint download auth (swarm-config.yaml:53-60) |

| Config | Values |
|---|---|
| Checkpoints | `hf://kyutai/moshika-rag-pytorch-bf16/config.json` + `model.safetensors` (README.md:110-119) |
| Conditioner | `reference_with_time` (README.md:110-119) |
| Retrieval profiles | `id`, `base_url`, `model`, optional `api_key`, `prompt_style: original \| simplified`, one `default: true` (README.md:154-157) |
| Server flags | `--gradio-tunnel [--gradio-tunnel-token]`, `--static`, `--init-active-speaker model`, `--gradium-stt` (README.md:107-112, README.md:164-171) |
| Routing | `frontend` on `PathPrefix("/")` prio 10, `backend` on `PathPrefix("/api")` prio 100, TLS via Let's Encrypt (swarm-config.yaml:35-82) |

## 9. Extensibility Points

- New retrieval source: implement any text-in/text-out back end (LLM or
  search) behind an OpenAI-compatible endpoint and register it as a profile
  in `MOSHI_RETRIEVAL_LLMS_JSON` (README.md:36, README.md:138-157).
- Prompt behavior per backend: add or select a bundled reference prompt
  template through the profile `prompt_style` field (`original` vs
  `simplified`) (README.md:156).
- Fallback policy: designate exactly one profile `default: true` so its
  model serves when any other retrieval model fails (README.md:155).
- Conditioning: replace or extend the reference encoder behind
  `REFERENCE_ENCODER_URL` / `server_conditioner --conditioner` to change how
  reference text is embedded into Moshi's conditioning path
  (README.md:100-119).
- Speech input: swap the STT leg between local transcription and Gradium by
  toggling `--gradium-stt` and `STT_URL`/`STT_API_KEY` (README.md:96-108).
- Front end: fork `moshi/` (PyTorch) for research changes or `rust/` for a
  production serving path (README.md:21-26).
- UI and deployment: modify `client/` for the web UI and `swarm-config.yaml`
  services, routing rules, GPU reservations, and volumes for new topology
  (swarm-config.yaml:35-136).

## 10. Limitations and Gotchas

- **24 GB-class GPU required for the PyTorch front end.** Quantization is
  unsupported, the model and reference encoder compete for VRAM, and a
  locally run retrieval back end needs an additional GPU (README.md:68).
- **Retrieval latency over ~3 seconds degrades response quality.**
  Slow or flaky APIs hurt grounding, which is why a co-located local vLLM
  server is recommended over remote endpoints (README.md:79-87).
- **Run everything on the same machine when possible.** The conditioner,
  local retrieval LLM, and main server are latency-sensitive to networking,
  and co-location simplifies debugging (README.md:159).
- **Browser microphone breaks over remote plain HTTP.** Use SSH `-L`
  forwarding of port 8998 to localhost or `--gradio-tunnel`; tunneled US
  routing can add up to 500 ms latency from Europe, mitigated with
  `--gradio-tunnel-token` pinning (README.md:163-175).
- **Python version fragility.** Below 3.12, `rustymimi` may fail to install,
  forcing a Rust toolchain install or an upgrade to 3.12 (README.md:66).
- **Rust run documentation is truncated in the wiki source.** Only the env
  vars and the instruction to run from within `rust/` survive; the exact
  Rust server command is cut off mid-sentence, so the Rust path cannot be
  reproduced from the wiki alone (README.md:194-197 as relayed).

## 11. How It Compares to Alternatives

The wiki names one direct comparator and two in-repo option axes, and no
external speech-RAG competitors. Against **upstream Moshi
(kyutai-labs/moshi)**, from which this repo is derived (README.md:16),
MoshiRAG trades a small amount of system complexity (an extra encoder
service plus a retrieval endpoint) for factual grounding the base
full-duplex model lacks. On the retrieval axis the repo itself offers the
choice the wiki documents: **LLM-based vs search-based** text-in/text-out
back ends, with multi-profile fallback so a cheap local model
(`google/gemma-3-27b-it` under vLLM) can pair with a remote API profile
(README.md:36, README.md:138-157). On the serving axis it offers
**PyTorch (`moshi/`) vs Rust/Candle (`rust/`)** builds of the same Moshika
voice, i.e. research flexibility against production efficiency, with
matching `*-pytorch-bf16` / `*-candle-bf16` checkpoint formats
(README.md:21-26, README.md:49-54). Positioning: this is the async-RAG
variant of the Moshi stack — it keeps Moshi's real-time full-duplex
interaction model intact and confines factuality work to a parallel,
stream-injected path rather than restructuring generation around
tool calls.

## Appendix: Selected Code Snippets

1. Main server startup with retrieval and STT wiring (README.md:121-136):

```bash
export REFERENCE_ENCODER_URL=http://localhost:8001
export STT_URL=wss://eu.api.gradium.ai/api/speech/asr
export STT_API_KEY=YOUR_API_KEY
export LLM_BASE_URL=http://localhost:8002/v1
export LLM_API_KEY=dummy
export LLM_MODEL_NAME=google/gemma-3-27b-it

python -m moshi.moshi.server \
  --gradio-tunnel \
  --static "./client/dist" \
  --init-active-speaker model \
  --gradium-stt
```

2. Multi-backend retrieval configuration overriding single-backend selection
(README.md:138-142):

```bash
export MOSHI_RETRIEVAL_LLMS_JSON='[{"id": "gpt-oss-20b", "base_url": "https://api.groq.com/openai/v1", "model": "openai/gpt-oss-20b", "prompt_style": "simplified"},  {"id": "gemma-3-27b-it", "base_url": "http://localhost:8002/v1", "model": "google/gemma-3-27b-it", "default": true, "prompt_style": "original"}]'
```

3. Swarm backend environment and GPU reservation (swarm-config.yaml:53-60,
swarm-config.yaml:78-82):

```yaml
environment:
  - "PORT=80"
  - "HF_TOKEN=${HUGGING_FACE_HUB_TOKEN}"
  - "HUGGING_FACE_HUB_TOKEN=${HUGGING_FACE_HUB_TOKEN}"
  - "LLM_BASE_URL=${LLM_BASE_URL}"
  - "LLM_API_KEY=${LLM_API_KEY}"
  - "LLM_MODEL_NAME=${LLM_MODEL_NAME}"
  - "ARC_ENCODER_URL=http://arc_encoder:80"
  - "STT_URL=wss://eu.api.gradium.ai/api/speech/asr"
  - "STT_API_KEY=${STT_API_KEY}"
```

```yaml
resources:
  reservations:
    generic_resources:
      - discrete_resource_spec:
          kind: gpu
          value: 1
```
