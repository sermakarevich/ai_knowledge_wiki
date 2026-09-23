> [[index|Wiki]] | [[summary|Summary]]
# alphaparkinc/genpark-neural-speech-codec-full-duplex-dialogue-engine-skill — Digest
## 1. [[wiki/01-overview|Overview]]
**In one sentence:** This repo packages a GenPark AI Agent Skill that implements a Moshi-style neural speech codec full-duplex dialogue engine and live audio streamer (README.md:11).
## Key points
- The repo is named `genpark-neural-speech-codec-full-duplex-dialogue-engine-skill` (README.md:7).
- It targets Python 3.9+, is MIT-licensed, MCP-compatible, and branded as a GenPark AI Agent Skill (README.md:9).
- Its whole job is neural speech codec full-duplex dialogue plus live audio streaming in the Moshi style (README.md:11).
- The quick-start entry point is `python example_usage.py` (README.md:15).
- Requests flow as JSON from User/AI Agent into the Skill, then to the Core Engine, which returns structured output to the User (README.md:20-24).
- The MCP entry point is `python mcp_server.py` (README.md:28).
- The documented macro component at this level is `top-level-files/` (README.md:33).
## 2. [[wiki/02-top-level-files|top-level-files]]
**In one sentence:** The six top-level files define the skill manifest, duplex-dialogue client, usage example, MCP server stub, dependency declaration, and ignore rules (skill.json:1-38).
## Key points
- `skill.json` declares the skill `genpark-neural-speech-codec-full-duplex-dialogue-engine-skill` v1.0.0 in category `neural-voice` by author `genpark` (skill.json:2-6).
- `client.py` exposes `NeuralSpeechCodecFullDuplexDialogueEngineClient.stream_duplex_audio_turn(incoming_audio_chunk_bytes=4096, sample_rate_hz=24000)` returning a fixed duplex-turn dict (client.py:1-2).
- The client's returned dict reports `codec_framerate_hz` 12.5, `bidirectional_latency_ms` 160, 14 inner-monologue tokens, timbre loss 0.012, and an active listen/synthesis flag with a live socket URL (client.py:4-10).
- `example_usage.py` instantiates the client, calls `stream_duplex_audio_turn(8192)`, and prints the turn id, latency, token count, codec rate, listen/talk flag, and socket URL (example_usage.py:4-9).
- `mcp_server.py` defines `run_mcp_server()` which prints a JSON status payload with `mcp_version` 1.0.0 and `supported_tools` `["execute_skill_action"]` (mcp_server.py:2-3).
- `requirements.txt` declares no external dependencies, Python 3.9+ stdlib only (requirements.txt:1).
- `.gitignore` excludes `__pycache__/`, `*.py[cod]`, `.env`, `.venv/`, `venv/`, `*.log`, and `.DS_Store` (.gitignore:1-7).
## The system in five moves
1. A GenPark AI Agent Skill packages a Moshi-style neural speech codec full-duplex dialogue engine and live audio streamer for Python 3.9+.
2. JSON requests flow from User/AI Agent into the Skill and Core Engine, which returns structured output, via `python example_usage.py` and `python mcp_server.py`.
3. The `skill.json` manifest declares the skill identity, neural-voice category, Moshi/Kyutai tags, `client.py` entrypoint, and duplex-turn inputs/outputs.
4. The client streams one duplex audio turn with a fixed payload — 12.5 Hz codec framing, 160 ms bidirectional latency, 14 inner-monologue tokens, timbre loss 0.012, and a live duplex socket URL.
5. The usage example, MCP server stub, stdlib-only requirements, and ignore rules complete the runnable, MCP-compatible skill package.
