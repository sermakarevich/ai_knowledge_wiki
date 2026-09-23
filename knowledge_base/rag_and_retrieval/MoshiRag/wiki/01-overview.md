[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Overview
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
---
## Organisation of the repository
This repository includes two main codebases (README.md:21-24):
- **[PyTorch](#pytorch-implementation)** for research and experimentation, located in `moshi/`.
- **[Rust](#rust-implementation)** for production use, located in `rust/`.

> Finally, the code for the web UI client is provided in the `client/` directory. (README.md:26)

## System design
MoshiRAG uses a modular front-end/back-end design (README.md:30-32):
- **Front-end** is a full-duplex speech model based on Moshi that handles real-time conversation.
- **Back end** is an asynchronous retrieval system running in parallel to fetch factual information when needed.

> The front end keeps listening and speaking continuously. When the model predicts a retrieval trigger token, conversation context is sent to the retrieval back end while the dialogue continues. During this period, the model can produce lightweight pre-RAG content (for example, short acknowledgments or coarse responses) so the interaction stays natural. (README.md:34)

> The back end is text-in/text-out and can be implemented with different retrieval methods (LLM-based retrieval or search-based retrieval, etc). The retrieval back end takes conversation context (derived by combining the text predicted by Moshi inner monologue and the user transcription predicted by a streaming ASR component) as inputs, and then returns the reference text. Once the retrieval is completed, the reference text is encoded and injected back into Moshi as a stream, allowing later response segments to be grounded in external knowledge without interrupting the ongoing conversation. (README.md:36)

Illustrations referenced (README.md:38-44):
- `front_back_end.png` — `<ret>` token triggers async back-end call; result injected into Moshi with no interruption.
- `streams.png` — text/audio token streams; retrieval representation is summed with other stream embeddings over several time steps.

## Models
> We release the MoshiRAG model fine-tuned on a female synthetic voice (Moshika). (README.md:49)

| Format | HuggingFace repo |
| --- | --- |
| PyTorch (bf16) | `kyutai/moshika-rag-pytorch-bf16` (README.md:51) |
| Rust/Candle (bf16) | `kyutai/moshika-rag-candle-bf16` (README.md:52) |

> All models are released under the CC-BY 4.0 license. (README.md:54)

## Requirements
- Python at least 3.10, 3.12 recommended (README.md:58).
- Install PyTorch/MLX clients with (README.md:61-64):

```bash
pip install -U -e "git+https://git@github.com/kyutai-labs/moshi-rag.git#egg=moshi&subdirectory=moshi"
pip install rustymimi  # mimi, rust implementation with Python bindings from PyPI
```

- Non-3.12 Python may fail installing `rustymimi`; then install the Rust toolchain or switch to Python 3.12 (README.md:66).
- PyTorch version has no quantization support, needs a GPU with significant memory (24GB) for the front-end Moshi model; reference encoder can share that GPU with enough VRAM or use a second GPU; a locally run back end needs an additional GPU (README.md:68).
- Rust backend needs a recent Rust toolchain; GPU support additionally needs CUDA with `nvcc` (README.md:70-71).

## PyTorch implementation
> The PyTorch based API can be found in the `moshi` directory. (README.md:75)

### Back end (retrieval LLM)
> It is recommended to run a local OpenAI-compatible LLM with vLLM so retrieval stays low-latency and stable. MoshiRAG is sensitive to retrieval delays over 3 seconds; slower or flaky APIs can hurt response quality. (README.md:79)

```bash
vllm serve google/gemma-3-27b-it --host 0.0.0.0 --port 8002
```

Serve on port `8002`; set `LLM_BASE_URL` to `http://localhost:8002/v1` and `LLM_MODEL_NAME` to `google/gemma-3-27b-it` (README.md:81-85). Online APIs can be used instead by configuring `LLM_BASE_URL`, `LLM_API_KEY`, and `LLM_MODEL_NAME`; prefer a low-latency provider (README.md:87).

### Front end (main Moshi server + reference encoder)
Two cooperating processes (README.md:91-94):
1. **Main Moshi server** (`python -m moshi.moshi.server`) — full-duplex speech model; calls the retrieval LLM over HTTP (OpenAI-compatible API) on RAG triggers.
2. **Reference text encoder** (`python -m moshi.moshi.server_conditioner`) — encodes retrieved reference strings for injection into Moshi's conditioning path (`REFERENCE_ENCODER_URL` points at this service).

> The Moshi model and reference encoder can run on the same GPU if you have enough memory, or on separate GPUs (but ideally on the same machine). The main server also streams user audio to an STT (speech-to-text / streaming ASR) endpoint to transcribe user speech into text. (README.md:96)

| Variable | Role (README.md:100-108) |
| --- | --- |
| `REFERENCE_ENCODER_URL` | Base URL of the reference text conditioner (e.g. `http://localhost:8001`). |
| `STT_URL` | Streaming ASR API. Recommended Gradium `wss://eu.api.gradium.ai/api/speech/asr`. Unneeded without `--gradium-stt` (local STT used instead). |
| `STT_API_KEY` | API key for Gradium STT. Unneeded without `--gradium-stt`. |
| `LLM_BASE_URL` | Base URL of the OpenAI-compatible API used for retrieval; local VLLM server recommended. |
| `LLM_API_KEY` | API key for the retrieval LLM. |
| `LLM_MODEL_NAME` | Model id passed to the retrieval API. |
| `MOSHI_RETRIEVAL_LLMS_JSON` | Optional multi-backend retrieval config; overrides single-backend selection. |

Start the reference encoder (config/checkpoints from Hugging Face) (README.md:110-119):

```bash
python -m moshi.moshi.server_conditioner \
    --config hf://kyutai/moshika-rag-pytorch-bf16/config.json \
    --moshi-weight hf://kyutai/moshika-rag-pytorch-bf16/model.safetensors \
    --cuda-device 0 \
    --conditioner reference_with_time \
    --port 8001
```

Start the main server (README.md:121-136):

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

Multiple retrieval backends via `MOSHI_RETRIEVAL_LLMS_JSON`, which overrides single `LLM_BASE_URL`/`LLM_MODEL_NAME` selection (README.md:138-142):

```bash
export MOSHI_RETRIEVAL_LLMS_JSON='[{"id": "gpt-oss-20b", "base_url": "https://api.groq.com/openai/v1", "model": "openai/gpt-oss-20b", "prompt_style": "simplified"},  {"id": "gemma-3-27b-it", "base_url": "http://localhost:8002/v1", "model": "google/gemma-3-27b-it", "default": true, "prompt_style": "original"}]'
```

- Each array item is one retrieval profile (`id`, `base_url`, `model`, optional `api_key`, optional `prompt_style`) (README.md:154).
- `default: true` marks the fallback profile (exactly one required with 2+ profiles) used if any retrieval model fails (README.md:155).
- `prompt_style` selects the bundled reference prompt template for that profile (`original` or `simplified`; default `original` for local LLM instances) (README.md:156).
- A profile omitting `api_key` uses the global `LLM_API_KEY` (README.md:157).
- Run conditioner, local retrieval LLM, and main server on the same machine when possible to reduce networking issues and simplify debugging (README.md:159).

### Web UI
- Access the web UI on `localhost:8998` (README.md:163).
- Remote-GPU caveat: HTTP sites cannot use the microphone; workarounds are SSH `-L` port forwarding of 8998 to localhost, or `--gradio-tunnel` (tunnel via US can add up to 500ms latency from Europe; `--gradio-tunnel-token` pins a reusable address) (README.md:164-171).
- Accessing a non-localhost server over http may break microphone use in some browsers (https-only) (README.md:173-175).

### Inference script
> We also provide an inference script which runs the PyTorch MoshiRAG pipeline on a folder of WAV audio files, and writes output WAVs and JSON logs to the specified destination. (README.md:179)

```bash
export REFERENCE_ENCODER_URL=http://localhost:8001
export LLM_BASE_URL=http://localhost:8002/v1
export LLM_API_KEY=dummy
export LLM_MODEL_NAME=google/gemma-3-27b-it

python -m moshi.moshi.run_inference \
  --input-dir INPUT_DIR \
  --output-dir OUTPUT_DIR \
  --max-consecutive-silence-frames 40
```

Set `LLM_BASE_URL`, `LLM_API_KEY`, `LLM_MODEL_NAME` as before to obtain reference text (README.md:179).

## Rust implementation
Truncated in chunk: the Rust run instructions are cut off mid-sentence at "use the following command from within the `rust` dire" (chunk lines 194-197). What is present: set `LLM_BASE_URL`, `LLM_API_KEY`, and `LLM_MODEL_NAME`, then run the Rust inference server from within the `rust` directory (README.md:196).

**Covers:** README.md (overview, organisation, system design, models, requirements, PyTorch and Rust run instructions); `moshi/`; `rust/`; `client/`; `front_back_end.png`; `streams.png`
