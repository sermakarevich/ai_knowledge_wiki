> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Overview

**In one sentence:** X-Talk is an open-source, full-duplex, cascaded spoken dialogue system framework for low-latency, interruptible speech interaction (01-overview.md:20).

## Key points

- X-Talk is an open-source full-duplex cascaded spoken dialogue system framework (01-overview.md:20).
- Speech flow is optimized for low latency, supports natural user interruption during interaction, and encodes paralinguistic information (e.g. environment noise, emotion) in parallel (01-overview.md:21-24).
- New models and relevant logic can be added within one Python script and integrated with the default pipeline (01-overview.md:25-26).
- The framework backend is pure Python with nothing to build and install beyond `pip install` (01-overview.md:27-28).
- Concurrency is provided through an asynchronous backend and websocket-based implementation for deployment from web browsers to edge devices (01-overview.md:29-31).
- The documented quickstart path uses AliCloud APIs, a JSON model config, and the `examples/sample_app/configurable_server.py` startup script serving the demo at `http://localhost:7635` (01-overview.md:114-161).
- The project is in active prototyping with interfaces subject to change, and points to a live demo, demo videos, and readthedocs docs (01-overview.md:18, 01-overview.md:47-50, 01-overview.md:166-168).

---

## Features

X-Talk advertises four properties (01-overview.md:20-31):

- **Low-Latency, Interruptible, Human-Like Speech Interaction:** optimized speech flow for low latency, natural user interruption, parallel paralinguistic encoding (environment noise, emotion) for understanding and empathy (01-overview.md:21-24).
- **Researcher Friendly:** new models and relevant logic added within one Python script and seamlessly integrated with the default pipeline (01-overview.md:25-26).
- **Super Lightweight:** framework backend is pure Python; nothing to build and install beyond `pip install` (01-overview.md:27-28).
- **Production Ready:** concurrency through asynchronous backend; websocket-based implementation for deployment from web browsers to edge devices (01-overview.md:29-31).
- Active-prototyping warning: interfaces and functions are subject to change, with an effort to keep interfaces stable (01-overview.md:18).

## Demo and docs

- Online demo link is given, running on a 4090 cluster with 8-bit quantized *SenseVoice* as speech recognizer, *IndexTTS 1.5* as speech generator, and 4-bit quantized *Qwen3-30B-A3B* as language model (01-overview.md:47-50).
- Tour-guiding demos use *Qwen3-Next-80B-A3B-Instruct* as language model while the other eight demos match the online demo setting; larger language models trade latency for intelligence (01-overview.md:98).
- Demo videos are embedded as a video grid in the README (01-overview.md:54-96).
- Docs link points to `https://xtalk.readthedocs.io/` (01-overview.md:166-168).
- Contents list covers Demo, Installation, Quickstart, Docs, Contributing, Acknowledgements, License (01-overview.md:34-42).

## Installation

Verbatim (01-overview.md:105-107):

```bash
pip install git+https://github.com/xcc-zach/xtalk.git@main
```

## Quickstart

Uses AliCloud APIs to demonstrate basic capability (01-overview.md:114). Verbatim dependency install (01-overview.md:117-119):

```bash
pip install "xtalk[ali,example] @ git+https://github.com/xcc-zach/xtalk.git@main"
```

Then obtain an API key from the AliCloud Bailian Platform (free-tier service, currently); online service may be unstable with high latency, so locally deployed models are recommended (01-overview.md:121-123).

Create a JSON config specifying the models and fill in `<API_KEY>` (01-overview.md:125-152):

```json
{
    "asr": {
        "type": "Qwen3ASRFlashRealtime",
        "params": {
            "api_key": "<API_KEY>"
        }
    },
    "llm_agent": {
        "type": "DefaultAgent",
        "params": {
            "model": {
                "api_key": "<API_KEY>",
                "model": "qwen-plus-2025-12-01",
                "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1"
            }
        }
    },
    "tts": {
        "type": "CosyVoice",
        "params": {
            "api_key": "<API_KEY>"
        }
    }
}
```

Config keys used (01-overview.md:128-151):

| Section | `type` | `params` fields |
|---|---|---|
| `asr` | `Qwen3ASRFlashRealtime` | `api_key` |
| `llm_agent` | `DefaultAgent` | `model.api_key`, `model.model` (`qwen-plus-2025-12-01`), `model.base_url` |
| `tts` | `CosyVoice` | `api_key` |

Start the server with the config file and a custom port (01-overview.md:154-159):

```bash
git clone https://github.com/xcc-zach/xtalk.git
cd xtalk
python examples/sample_app/configurable_server.py  --port 7635 --config <PATH_TO_CONFIG>.json
```

Startup flags used (01-overview.md:158):

| Flag | Meaning |
|---|---|
| `--port 7635` | custom port for the demo server |
| `--config <PATH_TO_CONFIG>.json` | path to the JSON config created above |

The demo is then ready at `http://localhost:7635` for viewing in the browser (01-overview.md:161).

No truncated files are noted in the chunk; the chunk ends with a macro-component pointer to `top-level-files/` (01-overview.md:170-172), which is covered by the separate `02-top-level-files` page.

**Covers:** `README.md` (repo root overview, features, demo, installation, quickstart, docs) as reproduced in `chunks/01-overview.md`
