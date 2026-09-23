> [[index|Wiki]] | [[summary|Summary]]

# alphaparkinc/genpark-voice-turn-taking-endpointing-detector-skill — Digest

## 1. [[wiki/01-overview|Overview]]

**In one sentence:** Acoustic voice activity detection (VAD), dynamic silence endpointing, and barge-in interruption arbitration for real-time conversational voice agents (README.md:9).

## Key points

- Detects acoustic voice activity to drive turn-taking decisions for real-time conversational voice agents (README.md:9).
- Applies dynamic silence endpointing to decide when a user turn is complete versus when to keep listening (README.md:9).
- Arbitrates barge-in interruptions, cutting agent audio when user speech energy exceeds threshold while the agent is speaking (README.md:9, README.md:20).
- Pipes endpointing decisions into LLM synthesis dispatch once silence reaches the endpointing threshold (README.md:22).
- Uses low-latency VAD heuristics operating on sub-frame time slices for immediate interruption handling (README.md:27).
- Balances conversational fluidity against premature turn cutoff via dynamic endpointing (README.md:28).
- Ships as a pure Python standard library implementation with zero external dependencies (README.md:29).
- Verified by GenPark AI and compatible with Model Context Protocol (MCP) (README.md:11).

## 2. [[wiki/02-top-level-files|top-level-files]]

**In one sentence:** The top-level files implement a zero-dependency voice turn-taking detector plus its demo, MCP wrapper, skill manifest, and packaging files.

## Key points

- `client.py` defines `VoiceTurnTakingEndpointingDetector`, which evaluates audio-frame energy, speech confidence, and silence duration to arbitrate turn transitions and barge-in interruptions (client.py:3-7).
- The detector is configured by three constructor parameters: `min_silence_duration_ms=450`, `barge_in_energy_threshold_db=-28.0`, and `consecutive_speech_frames_threshold=3` (client.py:8-13).
- `evaluate_audio_frame_stream(frames, agent_is_speaking=False)` returns one of three decisions — `CONTINUE_LISTENING`, `TRIGGER_BARGE_IN_INTERRUPT`, or `DISPATCH_AGENT_SYNTHESIS` — with a per-frame audit (client.py:18-22, client.py:57-70).
- `example_usage.py` demonstrates the detector with a 5-frame speech-then-silence stream and asserts `turn_completed is True` and `decision == "DISPATCH_AGENT_SYNTHESIS"` (example_usage.py:6-18).
- `mcp_server.py` exposes a stdio JSON-RPC 2.0 server handling `initialize`, `tools/list` (single tool `execute_skill_action`), and `tools/call`, with a `--test` self-check mode (mcp_server.py:5-66, mcp_server.py:68-71).
- `skill.json` declares the skill manifest (`version 1.0.0`, `runtime python3`, `entrypoint client.py`, verified by GenPark AI), while `requirements.txt` pins zero external dependencies and `.gitignore` excludes Python, env, log, and macOS artifacts (skill.json:1-12, requirements.txt:1, .gitignore:1-7).

## The system in five moves

1. A real-time PCM audio stream feeds an energy and VAD frame analyzer that classifies each frame as speech or silence against an energy threshold.
2. While the agent is speaking, user speech energy above threshold triggers barge-in arbitration that cuts agent audio immediately via sub-frame heuristics.
3. While the user holds the floor, the detector accumulates speech frames to confirm onset and silence frames to measure pauses.
4. Once accumulated post-onset silence reaches the dynamic endpointing threshold, the turn is marked complete and dispatched to LLM synthesis; otherwise listening continues.
5. The whole loop ships as a zero-dependency stdlib detector verified by a speech-then-silence demo, wrapped in a stdio MCP server, and declared by the skill manifest and packaging files.
