PDF: https://github.com/47thtechcorner/RayCodes_Nvidia_Audio
# 47thtechcorner/RayCodes_Nvidia_Audio
Source: https://github.com/47thtechcorner/RayCodes_Nvidia_Audio
Kind: repo
Fetched: 2026-09-22T14:38:45.985824+00:00
Tool: git-clone

# 47thtechcorner/RayCodes_Nvidia_Audio

Commit: 57cfb1e24f7f7e534b108e8722b57cbade24833f

## README

<div align="center">
  <a href="https://youtu.be/1fNTkBh1T2s">
    <img src="https://img.youtube.com/vi/1fNTkBh1T2s/0.jpg" alt="NVIDIA Nemotron 11B Voice AI: Zero-Latency Local ElevenLabs Alternative">
  </a>
  <h3>📺 <a href="https://youtu.be/1fNTkBh1T2s">Watch the full tutorial on YouTube</a></h3>
</div>

# 🌐 NVIDIA Nemotron VoiceChat Assistant

[![License: OpenMDW 1.1](https://img.shields.io/badge/License-OpenMDW__1.1-76B900.svg)](https://github.com/OpenMDW/OpenMDW/blob/main/1.1/LICENSE.OpenMDW-1.1)
[![Architecture: Hybrid Mamba-Transformer](https://img.shields.io/badge/Architecture-Hybrid__Mamba--Transformer-14B8A6.svg)](https://github.com/NVIDIA-NeMo/Speech/tree/nemotron-labs-voicechat)
[![VoiceBench: #2 Global](https://img.shields.io/badge/VoiceBench-%232__Global-A855F7.svg)](https://arxiv.org/abs/2410.17196)

NVIDIA NemotronLabs VoiceChat is an 11B parameter end-to-end, real-time speech full-duplex (FD) foundation model for conversational AI. Unlike traditional cascaded stacks (ASR &rarr; LLM &rarr; TTS), it unifies streaming speech understanding, dialogue reasoning, and speech synthesis into a single architecture, eliminating multi-model API handoffs and pipeline latency.

---

## ⚡ Key Highlights & Metrics

- 🛠️ **Single Unified Model:** Eliminates API handoffs and cuts turn-taking latency to **~450 ms**.
- 🎙️ **1st Open FD with Native Tool Calling:** Executes structured function calls (`<TOOLCALL>`) while maintaining speech stream.
- 🛑 **Barge-in / User Interruption:** Yields speech immediately (**~480 ms**) when the user cuts in.
- 🗣️ **Spoken On-Hold Feedback:** Speaks immediate acknowledge phrases during live tool parameter execution.
- 🏆 **VoiceBench Ranking:** Ranked **#2 globally** among open full-duplex conversational models.

| Specification | Technical Detail |
|---|---|
| Model Architecture | Hybrid Mamba / Transformer (Fast Conformer + Nemotron Nano V2 9B + Neural TTS) |
| Parameter Count | 11 Billion Parameters |
| Audio Input Format | 16 kHz WAV / WebAudio (User Speech) |
| Audio Output Format | 22.05 kHz WAV / Neural Codec (Agent Speech) |
| Turn-Taking Latency | ~450 ms Response Time |
| Interruption Latency | ~480 ms Yield Latency |
| Tool Selection Accuracy | 82.5% (Full-Duplex-Bench v3) |
| Irrelevance Filtering | 89.6% Accuracy (AU Harness BFCL-v3) |
| Governing License | OpenMDW License 1.1 |

---

## 🧠 Architecture Components

1. 📻 **Fast Conformer Speech Encoder:** Streaming 16 kHz audio encoder (`Nemotron-Speech-Streaming-En-0.6b`).
2. 🧠 **LLM Backbone:** `NVIDIA Nemotron Nano v2 9B` for multi-turn dialogue reasoning and tool parameter selection.
3. 🔊 **Neural Speech Decoder:** NVIDIA neural TTS decoder & acoustic codec predicting 22.05 kHz audio codes.
4. 💻 **Dual Output Channels:** Dedicated streaming text output channel for `<TOOLCALL>` JSON scripts.

---

## 🖥️ Infrastructure & Hardware Setup

Optimized for high-throughput GPU acceleration engines:
- **Runtime Engine:** vLLM & Triton Inference Server
- **Supported GPUs:** NVIDIA A100, H100, H200, B100, B200, RTX-6000
- **Supported OS:** Linux (Ubuntu 22.04 LTS recommended)
- **Deployment Interfaces:** Bidirectional WebSockets (interactive) & PyTorch pipeline (offline testing)

---

## 🔧 Tool Calling Tag Protocol

System prompts and tool responses use clean ASCII formatting:

```text
<AVAILABLE_TOOLS>[
  {
    "name": "get_weather",
    "description": "Get current weather for a city",
    "parameters": {
      "type": "object",
      "properties": {"city": {"type": "string"}},
      "required": ["city"]
    }
  }
]</AVAILABLE_TOOLS>

<TOOLCALL>[{"name": "get_weather", "arguments": {"city": "Tokyo"}}]</TOOLCALL>
<TOOL_RESPONSE>[{"temp": "72F", "condition": "Sunny"}]</TOOL_RESPONSE>
```

---

## 💻 Python Code Architecture

```text
.
├── main.py                # Pipeline runner executing multi-turn speech turns
├── voicechat_agent.py     # NVIDIA Nemotron VoiceChat 11B pipeline & neural audio decoder
├── README.md              # Project documentation
└── assets/                # HTML presentation & matching Markdown overview
```

| Module File | Purpose & Responsibilities | Key Functions / Classes |
|---|---|---|
| [`voicechat_agent.py`](voicechat_agent.py) | **Official NVIDIA Nemotron 11B Engine:** Downloads official checkpoint (`nvidia/NVIDIA-NemotronLabs-VoiceChat-11B`), initializes PyTorch CUDA models, parses predicted `<TOOLCALL>` tags, and executes dynamic live tool functions (`execute_tool_call()`). | `VoiceChatAgent`, `process_turn()`, `download_checkpoint()`, `execute_tool_call()` |
| [`main.py`](main.py) | **Pipeline Execution Runner:** Initializes `VoiceChatAgent` and executes multi-turn conversational scenarios. | `run_voicechat_demo()` |

---

## 🚀 Quick Start & Execution

### Prerequisites

```bash
pip install torch torchaudio transformers huggingface-hub
```

### Running the Official 11B Pipeline

```bash
python main.py
```

---

## 🎯 5 Core Production Use Cases

1. 📞 **Enterprise Support Agents:** Real-time customer support with instant tool calls (order tracking, appointment booking).
2. 🔧 **Field Service Voice Assistant:** Hands-free diagnostic tool for engineers querying equipment telemetry via live voice.
3. 🎓 **Interactive Speech Tutor:** Real-time conversational practice with sub-500ms feedback and immediate turn yield.
4. 🚑 **Emergency Call Routing:** High-availability emergency response coordinator executing live dispatch tools.
5. 🏠 **Smart Home Controller:** Direct voice control for IoT devices with spoken confirmation and zero-latency execution.

---

## 🔮 5 Roadmap Enhancements

1. 👥 **Multi-Speaker Diarization:** Real-time speaker attribution during multi-party voice calls.
2. ⚡ **Sub-300ms Speculative Decoding:** Parallel speech token generation for instantaneous response.
3. 🎭 **Dynamic Tone & Emotion Control:** Real-time pitch adaptation based on conversational context.
4. 📡 **Low-Bitrate Neural Codec:** Bandwidth optimizations for streaming audio over cellular networks.
5. 🌐 **Multilingual Voice Cloning:** Cross-lingual speech synthesis across 30+ spoken languages.

---

## 🔗 Official Platforms & Resources

- 🐙 **[Official GitHub Repository](https://github.com/NVIDIA-NeMo/Speech/tree/nemotron-labs-voicechat):** Core source code, NeMo Speech scripts, and WebSocket instructions.
- 📦 **[Hugging Face Checkpoint](https://huggingface.co/nvidia/NVIDIA-NemotronLabs-VoiceChat-11B):** Model weights, tokenizer configs, and offline inference samples.
- 🧠 **[Nemotron Nano V2 Backbone](https://huggingface.co/nvidia/NVIDIA-Nemotron-Nano-9B-v2):** 9B LLM backbone for high-speed multi-token prediction.
- 📄 **[OpenMDW 1.1 License](https://github.com/OpenMDW/OpenMDW/blob/main/1.1/LICENSE.OpenMDW-1.1):** Model usage terms and research governance guidelines.

---

## 🏷️ Keywords & Search Tags

`nvidia-nemotron` `voicechat-11b` `full-duplex-ai` `speech-to-speech` `fast-conformer` `elevenlabs-alternative` `zero-latency-audio` `tool-calling-voice` `openmdw-1.1` `vllm-speech`


## Top-level layout

- .gitignore (~7 lines)
- main.py (~46 lines)
- README.md (~146 lines)
- voicechat_agent.py (~189 lines)

