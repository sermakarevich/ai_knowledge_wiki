> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Overview
**In one sentence:** NVIDIA NemotronLabs VoiceChat is an 11B-parameter end-to-end real-time full-duplex speech model that unifies streaming speech understanding, dialogue reasoning, and speech synthesis in a single architecture instead of an ASR → LLM → TTS cascade (README.md:20).
## Key points
- Unifies streaming speech understanding, dialogue reasoning, and speech synthesis in one architecture, eliminating multi-model API handoffs and pipeline latency (README.md:20).
- Single unified model cuts turn-taking latency to ~450 ms with no API handoffs (README.md:26, README.md:38).
- Supports barge-in/user interruption, yielding speech in ~480 ms when the user cuts in (README.md:28, README.md:39).
- Performs native tool calling in the speech stream via structured `<TOOLCALL>` function calls plus a dedicated streaming text output channel for `<TOOLCALL>` JSON scripts (README.md:27, README.md:51).
- Gives spoken on-hold feedback with immediate acknowledge phrases during live tool parameter execution (README.md:29).
- Ranked #2 globally among open full-duplex conversational models on VoiceBench (README.md:30).
- Scores 82.5% tool selection accuracy on Full-Duplex-Bench v3 and 89.6% irrelevance-filtering accuracy on AU Harness BFCL-v3 (README.md:40–41).
- Governed by the OpenMDW License 1.1 (README.md:42).
---
## Unified model
End-to-end, real-time, full-duplex (FD) foundation model for conversational AI at 11B parameters (README.md:20). The stated contrast is explicit: unlike traditional cascaded stacks (ASR → LLM → TTS), it keeps understanding, reasoning, and synthesis in one architecture (README.md:20).
## Architecture components
1. 📻 **Fast Conformer Speech Encoder:** streaming 16 kHz audio encoder (`Nemotron-Speech-Streaming-En-0.6b`) (README.md:48).
2. 🧠 **LLM Backbone:** `NVIDIA Nemotron Nano v2 9B` for multi-turn dialogue reasoning and tool parameter selection (README.md:49).
3. 🔊 **Neural Speech Decoder:** NVIDIA neural TTS decoder and acoustic codec predicting 22.05 kHz audio codes (README.md:50).
4. 💻 **Dual Output Channels:** dedicated streaming text output channel for `<TOOLCALL>` JSON scripts (README.md:51).
## Specifications and metrics
| Specification | Technical Detail (README.md:33–42) |
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
## Infrastructure and deployment
Optimized for high-throughput GPU acceleration engines (README.md:57):
- **Runtime Engine:** vLLM and Triton Inference Server (README.md:58).
- **Supported GPUs:** NVIDIA A100, H100, H200, B100, B200, RTX-6000 (README.md:59).
- **Supported OS:** Linux (Ubuntu 22.04 LTS recommended) (README.md:60).
- **Deployment Interfaces:** Bidirectional WebSockets (interactive) and PyTorch pipeline (offline testing) (README.md:61).
## Tool-calling tag protocol
System prompts and tool responses use clean ASCII formatting (README.md:67). Verbatim protocol excerpt (README.md:69–84):
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
Exact tag names are `<AVAILABLE_TOOLS>`, `<TOOLCALL>`, and `<TOOL_RESPONSE>` with parameter fields `name`, `description`, `parameters`, `properties`, `required`, and `arguments` (README.md:70–83).
## Code layout and entry points
Verbatim layout excerpt (README.md:90–96):
```text
.
├── main.py                # Pipeline runner executing multi-turn speech turns
├── voicechat_agent.py     # NVIDIA Nemotron VoiceChat 11B pipeline & neural audio decoder
├── README.md              # Project documentation
└── assets/                # HTML presentation & matching Markdown overview
```
| Module File | Purpose and Responsibilities | Key Functions / Classes (README.md:98–101) |
|---|---|---|
| `voicechat_agent.py` | Official NVIDIA Nemotron 11B engine: downloads official checkpoint (`nvidia/NVIDIA-NemotronLabs-VoiceChat-11B`), initializes PyTorch CUDA models, parses predicted `<TOOLCALL>` tags, executes dynamic live tool functions (`execute_tool_call()`). | `VoiceChatAgent`, `process_turn()`, `download_checkpoint()`, `execute_tool_call()` |
| `main.py` | Pipeline execution runner: initializes `VoiceChatAgent` and executes multi-turn conversational scenarios. | `run_voicechat_demo()` |
### Quick start
Prerequisites command (README.md:109–111):
```bash
pip install torch torchaudio transformers huggingface-hub
```
Run command (README.md:115–117):
```bash
python main.py
```
## Production use cases
1. 📞 Enterprise Support Agents: real-time customer support with instant tool calls (order tracking, appointment booking) (README.md:123).
2. 🔧 Field Service Voice Assistant: hands-free diagnostic tool for engineers querying equipment telemetry via live voice (README.md:124).
3. 🎓 Interactive Speech Tutor: real-time conversational practice with sub-500ms feedback and immediate turn yield (README.md:125).
4. 🚑 Emergency Call Routing: high-availability emergency response coordinator executing live dispatch tools (README.md:126).
5. 🏠 Smart Home Controller: direct voice control for IoT devices with spoken confirmation and zero-latency execution (README.md:127).
## Roadmap
1. 👥 Multi-Speaker Diarization: real-time speaker attribution during multi-party voice calls (README.md:133).
2. ⚡ Sub-300ms Speculative Decoding: parallel speech token generation for instantaneous response (README.md:134).
3. 🎭 Dynamic Tone and Emotion Control: real-time pitch adaptation based on conversational context (README.md:135).
4. 📡 Low-Bitrate Neural Codec: bandwidth optimizations for streaming audio over cellular networks (README.md:136).
5. 🌐 Multilingual Voice Cloning: cross-lingual speech synthesis across 30+ spoken languages (README.md:137).
## Official resources
- Official GitHub repository (NeMo Speech scripts, WebSocket instructions) (README.md:143).
- Hugging Face checkpoint with model weights, tokenizer configs, and offline inference samples (README.md:144).
- Nemotron Nano V2 Backbone for high-speed multi-token prediction (README.md:145).
- OpenMDW 1.1 License terms and research governance guidelines (README.md:146).
**Covers:** README.md (project overview, metrics, architecture, infrastructure, tool-call protocol, code layout, quick start, use cases, roadmap, resources)
