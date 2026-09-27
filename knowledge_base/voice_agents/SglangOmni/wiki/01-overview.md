[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Overview
**In one sentence:** SGLang-Omni is a multi-stage serving runtime for omni, speech, and TTS models that owns pipeline topology, stage lifecycle, inter-stage transport, and an OpenAI-compatible serving surface while composing with SGLang for autoregressive execution.
## Key points
- SGLang-Omni is a multi-stage serving runtime for omni, speech, and TTS models whose design target is multi-stage decoding split across heterogeneous stages (README.md:47).
- It owns the pipeline topology, stage lifecycle, inter-stage transport, model-family integration layer, and OpenAI-compatible serving surface, while composing with SGLang for high-performance autoregressive scheduling and model execution where applicable (README.md:47).
- It models generation as coordinated stages: preprocessing, encoders, autoregressive engines, talkers, decoders, vocoders, and aggregators (README.md:49).
- Each stage runs behind a scheduler matched to its workload, from SGLang-backed autoregressive scheduling to lightweight preprocessing and streaming vocoder loops (README.md:50).
- A control plane coordinates requests while the relay data plane moves tensor payloads across shared-memory, NCCL, NIXL, and Mooncake backends (README.md:51).
- OpenAI-compatible endpoints expose multimodal chat, speech generation, batch speech, streaming speech, uploaded voices, and transcription (README.md:52).
- Hardware coverage is NVIDIA CUDA as the supported default backend with full model coverage, plus experimental Apple Silicon and Intel GPU (XPU) paths (README.md:66).
---
## About
> SGLang-Omni is a multi-stage serving runtime for omni, speech, and TTS models. Its design target is multi-stage decoding: generation split across heterogeneous stages with different compute patterns, dependency structures, and resource needs. SGLang-Omni owns the pipeline topology, stage lifecycle, inter-stage transport, model-family integration layer, and OpenAI-compatible serving surface, while composing with [SGLang](https://github.com/sgl-project/sglang) for high-performance autoregressive scheduling and model execution where applicable. (README.md:47)

Stage model (README.md:49-52):

- **Multi-stage runtime**: SGLang-Omni models generation as coordinated stages: preprocessing, encoders, autoregressive engines, talkers, decoders, vocoders, and aggregators.
- **Stage-specialized scheduling**: Each stage runs behind a scheduler matched to its workload, from SGLang-backed autoregressive scheduling to lightweight preprocessing and streaming vocoder loops.
- **Transport-aware execution**: A control plane coordinates requests while the relay data plane moves tensor payloads across shared-memory, NCCL, NIXL, and Mooncake backends.
- **API surface**: OpenAI-compatible endpoints expose multimodal chat, speech generation, batch speech, streaming speech, uploaded voices, and transcription.

## What SGLang-Omni Serves
- **Omni chat and speech**: `Qwen3-Omni`, `Ming-Omni` — multimodal in, text/audio out (README.md:56).
- **Music generation**: `MiniMax Music 3` — lyrics + caption → 32 kHz stereo song (README.md:57).
- **Speech generation**: `Higgs Audio v3`, `MOSS-TTS`, `MOSS-TTS Local`, `Fish Speech S2-Pro`, `Qwen3-TTS`, `Voxtral TTS`, `Ming-Omni-TTS`, `dots.tts`, `ZONOS2` — `/v1/audio/speech`, batch, streaming, uploaded voices (README.md:58).
- **Audio transcription and diarization**: `Qwen3-ASR`, `Fun-ASR`, `ARK-ASR`, `MOSS-Transcribe-Diarize` via `/v1/audio/transcriptions`; MOSS-TD supports speaker labels and timestamps (`response_format=verbose_json`) (README.md:59).
- **SGLang-Omni Router**: Multi-worker OpenAI-compatible front door — health, readiness, lifecycle, capability discovery (README.md:60).

## Hardware Support
Verbatim hardware matrix (README.md:64-68):

| Backend | Status | Notes |
|---------|--------|-------|
| **NVIDIA CUDA** | Supported | Default backend with full model coverage. |
| **Apple Silicon** | Experimental | Qwen3-ASR runs through native MLX or Torch MPS on macOS arm64. Install with [`install.sh`](./install.sh) and follow the [Qwen3-ASR guide](./docs/cookbook/qwen3_asr.md#apple-silicon-mlx). |
| **Intel GPU (XPU)** | Experimental | Intel Arc GPUs via PyTorch XPU. **Qwen3-ASR, Qwen3-TTS, and Qwen3-Omni serve end-to-end** (Omni thinker via multi-XPU tensor parallelism). Install per [Intel XPU guide](./docs/get_started/installation_xpu.md); the backend is auto-detected. |

Additional model guides, including experimental and research-oriented paths, are available in the Cookbook (README.md:70).

## Quick Start and Community
Entry points (README.md:74-81):

- **macOS Apple Silicon:** from a checkout, run `./install.sh` for a one-command Homebrew + uv setup.
- `Installation`, `TTS usage`, `Qwen3-Omni usage`, `Qwen3-ASR cookbook`, `MOSS-Transcribe-Diarize cookbook`, `Omni router`, `Developer reference`.

SGLang-Omni welcomes contributors working on inference systems, kernels, scheduling, inter-stage communication, model runners and cache efficiency, model integration, benchmarking, production deployment (README.md:85).

**Covers:** README.md (About, What SGLang-Omni Serves, Hardware Support, Quick Start, Community & Support, Acknowledgments)
