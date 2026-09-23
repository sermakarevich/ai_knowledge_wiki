---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: 47thtechcorner/RayCodes_Nvidia_Audio

### Q1. What is NVIDIA NemotronLabs VoiceChat and how does it differ from a cascaded voice stack?

> [!tip]- Answer
> It is an 11B-parameter end-to-end real-time full-duplex speech model that unifies streaming speech understanding, dialogue reasoning, and speech synthesis in a single architecture instead of an ASR → LLM → TTS cascade. The unified design with no API handoffs cuts turn-taking latency to ~450 ms and yields speech in ~480 ms when the user barges in. See [[wiki/01-overview|Overview]].

### Q2. What are the three model components plus the fourth output mechanism, and what audio formats do they use?

> [!tip]- Answer
> The Fast Conformer speech encoder streams 16 kHz user audio, the Nemotron Nano v2 9B backbone handles multi-turn reasoning and tool parameter selection, and the neural speech decoder predicts 22.05 kHz audio codes for agent speech. A dedicated dual streaming text output channel carries `<TOOLCALL>` JSON scripts side by side with speech. See [[wiki/01-overview|Overview]].

### Q3. What is the exact tool-calling tag protocol and its three decision rules?

> [!tip]- Answer
> The tags are `<AVAILABLE_TOOLS>` (tool list with `name`, `description`, `parameters`, `properties`, `required`), `<TOOLCALL>` (e.g. `[{"name": "get_weather", "arguments": {"city": "Tokyo"}}]`), and `<TOOL_RESPONSE>` (tool results). The agent must call a listed tool when the request matches it, answer general-knowledge questions directly, and politely decline external actions no tool covers; it must never invent tool names, guess missing arguments, or retry a failed tool for the same request. See [[wiki/01-overview|Overview]].

### Q4. What benchmarks, deployment targets, and license govern this repo?

> [!tip]- Answer
> It ranks #2 among open full-duplex conversational models on VoiceBench, with 82.5% tool selection accuracy on Full-Duplex-Bench v3 and 89.6% irrelevance filtering on AU Harness BFCL-v3. Deployment targets vLLM and Triton on A100/H100/H200/B100/B200/RTX-6000 under Ubuntu 22.04 via bidirectional WebSockets or an offline PyTorch pipeline. It is governed by the OpenMDW License 1.1. See [[wiki/01-overview|Overview]].

### Q5. What do the two `main.py` demo turns execute?

> [!tip]- Answer
> `run_voicechat_demo()` initializes `VoiceChatAgent(checkpoint_dir="./checkpoint")`, downloading the Hugging Face checkpoint when absent. Scenario 1 runs a general-knowledge turn from `general_conversation.wav`, and scenario 2 runs a Mumbai-weather tool-calling turn from `mumbai_weather_tool_call.wav`, each via `agent.process_turn()` with its own output WAV. See [[wiki/02-top-level-files|Top-Level Files]].

### Q6. How do `execute_tool_call()` and `VoiceChatAgent.process_turn()` work?

> [!tip]- Answer
> `execute_tool_call(tool_name, arguments)` runs `get_weather` via `wttr.in` (with a 28°C fallback on exception), `get_stock_price`, and `get_top_news`, returning an error dict for unknown tools. `process_turn()` builds the system prompt, generates up to 256 tokens, parses `<TOOLCALL>` with regex, executes the tool, wraps the result as `<TOOL_RESPONSE>`, and returns `user_audio`, `generated_text`, `tool_call`, `tool_response`, `output_audio_file`, `sample_rate`, and `turn_latency_ms`. See [[wiki/02-top-level-files|Top-Level Files]].

### Q7. A team wants a sub-500 ms barge-in-capable enterprise support agent with live order-tracking tool calls and spoken on-hold feedback — should they adopt this repo's approach and what should they watch out for?

> [!tip]- Answer
> Yes, adopt it because the unified full-duplex model delivers ~450 ms turns, ~480 ms barge-in yield, native in-stream `<TOOLCALL>` execution, and spoken acknowledge phrases during live calls, matching support-desk needs. Watch out for GPU requirements (A100-class hardware via vLLM/Triton), the OpenMDW 1.1 license terms, and the demo's limits: only three toy tools exist, stock/news handlers return stub data, and production order-tracking tools plus multi-speaker diarization from the roadmap must still be built. See [[wiki/01-overview|Overview]].
