---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---
> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# Retrieval Practice: alphaparkinc/genpark-neural-speech-codec-full-duplex-dialogue-engine-skill
### Q1. What is this repo's stated purpose and how is it positioned?
> [!tip]- Answer
> This repo packages a GenPark AI Agent Skill implementing a Moshi-style neural speech codec full-duplex dialogue engine and live audio streamer. It targets Python 3.9+, is MIT-licensed, MCP-compatible, and branded as a `neural-voice` GenPark skill. See [[wiki/01-overview|Overview]].
### Q2. What are the two documented entry points and the JSON request flow?
> [!tip]- Answer
> The quick-start entry point is `python example_usage.py` and the MCP entry point is `python mcp_server.py`. Requests flow as JSON from User/AI Agent into the Skill, then to the Core Engine, which returns structured output to the User. See [[wiki/01-overview|Overview]].
### Q3. What identity and I/O contract does `skill.json` declare?
> [!tip]- Answer
> It declares the skill `genpark-neural-speech-codec-full-duplex-dialogue-engine-skill` v1.0.0 in category `neural-voice` by author `genpark`, with tags `moshi`, `kyutai`, `full-duplex-speech`, `neural-codec`, `realtime-voice`. Inputs are `incoming_audio_chunk_bytes` and `sample_rate_hz`; outputs include `duplex_turn_id`, `bidirectional_latency_ms`, the listen/synthesis flag, and socket URL. See [[wiki/02-top-level-files|top-level-files]].
### Q4. What is the exact signature and fixed return payload of `client.py`?
> [!tip]- Answer
> The method is `stream_duplex_audio_turn(self, incoming_audio_chunk_bytes=4096, sample_rate_hz=24000)`. It returns a fixed dict with turn id `msh_dpx_7721`, `codec_framerate_hz` 12.5, `bidirectional_latency_ms` 160, 14 inner-monologue tokens, timbre loss 0.012, `simultaneous_listening_synthesis_active` True, and socket URL `wss://speech.genpark.ai/moshi/7721`. See [[wiki/02-top-level-files|top-level-files]].
### Q5. How does `example_usage.py` exercise the client?
> [!tip]- Answer
> It instantiates `NeuralSpeechCodecFullDuplexDialogueEngineClient` and calls `stream_duplex_audio_turn(8192)`, positionally overriding the 4096 default. It then prints the turn id with latency, the token count with codec rate, the listen/talk flag, and the socket URL. See [[wiki/02-top-level-files|top-level-files]].
### Q6. What do `mcp_server.py`, `requirements.txt`, and `.gitignore` contain?
> [!tip]- Answer
> `mcp_server.py` defines `run_mcp_server()`, which prints a JSON status payload with `mcp_version` 1.0.0 and `supported_tools` `["execute_skill_action"]`. `requirements.txt` declares no external dependencies, Python 3.9+ stdlib only, and `.gitignore` excludes `__pycache__/`, `*.py[cod]`, `.env`, venv dirs, `*.log`, and `.DS_Store`. See [[wiki/02-top-level-files|top-level-files]].
### Q7. Should you treat this repo as a production-ready full-duplex dialogue engine?
> [!tip]- Answer
> No — treat it as a runnable skill stub and interface demo, not a real codec or streaming engine. The client returns a hardcoded payload and the MCP server only prints a status message, so any production choice requires a real model, live socket, and latency validation first. See [[wiki/02-top-level-files|top-level-files]].
