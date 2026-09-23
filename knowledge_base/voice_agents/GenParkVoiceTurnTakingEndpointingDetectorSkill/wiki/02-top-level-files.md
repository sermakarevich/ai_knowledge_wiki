> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# top-level-files
**In one sentence:** The top-level files implement a zero-dependency voice turn-taking detector plus its demo, MCP wrapper, skill manifest, and packaging files.
## Key points
- `client.py` defines `VoiceTurnTakingEndpointingDetector`, which evaluates audio-frame energy, speech confidence, and silence duration to arbitrate turn transitions and barge-in interruptions (client.py:3-7).
- The detector is configured by three constructor parameters: `min_silence_duration_ms=450`, `barge_in_energy_threshold_db=-28.0`, and `consecutive_speech_frames_threshold=3` (client.py:8-13).
- `evaluate_audio_frame_stream(frames, agent_is_speaking=False)` returns one of three decisions — `CONTINUE_LISTENING`, `TRIGGER_BARGE_IN_INTERRUPT`, or `DISPATCH_AGENT_SYNTHESIS` — with a per-frame audit (client.py:18-22, client.py:57-70).
- `example_usage.py` demonstrates the detector with a 5-frame speech-then-silence stream and asserts `turn_completed is True` and `decision == "DISPATCH_AGENT_SYNTHESIS"` (example_usage.py:6-18).
- `mcp_server.py` exposes a stdio JSON-RPC 2.0 server handling `initialize`, `tools/list` (single tool `execute_skill_action`), and `tools/call`, with a `--test` self-check mode (mcp_server.py:5-66, mcp_server.py:68-71).
- `skill.json` declares the skill manifest (`version 1.0.0`, `runtime python3`, `entrypoint client.py`, verified by GenPark AI), while `requirements.txt` pins zero external dependencies and `.gitignore` excludes Python, env, log, and macOS artifacts (skill.json:1-12, requirements.txt:1, .gitignore:1-7).
---
## client.py — turn-taking and endpointing detector
`VoiceTurnTakingEndpointingDetector` docstring (client.py:3-7):
```python
class VoiceTurnTakingEndpointingDetector:
    """
    Evaluates real-time audio frame energy levels, speech confidence, and silence duration
    to arbitrate conversational turn transitions and barge-in interruptions.
    """
```
Constructor with exact parameter names and defaults (client.py:8-13):
```python
def __init__(
    self,
    min_silence_duration_ms: int = 450,
    barge_in_energy_threshold_db: float = -28.0,
    consecutive_speech_frames_threshold: int = 3
):
```
| Parameter | Type | Default | Role |
|---|---|---|---|
| `min_silence_duration_ms` | `int` | `450` | Silence accumulated after speech onset required to set `turn_completed` (client.py:44-47) |
| `barge_in_energy_threshold_db` | `float` | `-28.0` | Per-frame energy threshold for `is_speech` classification (client.py:31-33) |
| `consecutive_speech_frames_threshold` | `int` | `3` | Consecutive speech frames required to set `speech_started` and, when `agent_is_speaking`, `user_interrupted` (client.py:35-41) |
Entry point signature (client.py:18-22):
```python
def evaluate_audio_frame_stream(
    self,
    frames: List[Dict[str, Any]],
    agent_is_speaking: bool = False
) -> Dict[str, Any]:
```
Core loop logic (client.py:30-56): defaults each frame to `energy_db=-60.0` and `duration_ms=20` (client.py:30-31); classifies `is_speech = energy_db >= barge_in_energy_threshold_db` (client.py:33); on speech increments `consecutive_speech` and resets silence (client.py:35-37); on `consecutive_speech >= threshold` sets `speech_started=True` (client.py:38-39); sets `user_interrupted=True` only when `agent_is_speaking` is true (client.py:40-41); on non-speech after onset accumulates `consecutive_silence_ms += duration_ms` (client.py:44-45) and sets `turn_completed=True` once `>= min_silence_duration_ms` (client.py:46-47). Each frame appends `energy_db`, `is_speech`, `silence_accumulated_ms`, `interrupted`, `turn_completed` to `frame_audit` (client.py:49-55).
Decision precedence (client.py:57-61):
```python
decision = "CONTINUE_LISTENING"
if user_interrupted:
    decision = "TRIGGER_BARGE_IN_INTERRUPT"
elif turn_completed:
    decision = "DISPATCH_AGENT_SYNTHESIS"
```
Return payload keys (client.py:63-70): `decision`, `barge_in_detected`, `turn_completed`, `final_silence_ms`, `analyzed_frames_count`, `frame_audit`.
## example_usage.py — verification demo
Instantiates with an overridden silence threshold (example_usage.py:6):
```python
detector = VoiceTurnTakingEndpointingDetector(min_silence_duration_ms=400)
```
Simulated stream (example_usage.py:8-14): three speech frames (`-22.0`, `-20.0`, `-24.0` dB at 100 ms each) followed by two silence frames (`-55.0` dB / 200 ms, `-60.0` dB / 250 ms), evaluated with `agent_is_speaking=False` (example_usage.py:15). Verifies (example_usage.py:18-20):
```python
assert result["turn_completed"] is True
assert result["decision"] == "DISPATCH_AGENT_SYNTHESIS"
```
## mcp_server.py — stdio JSON-RPC wrapper
Dispatcher `handle_mcp_request(payload)` reads `method` and `id` (mcp_server.py:5-7) and serves:
| Method | Response |
|---|---|
| `initialize` | `protocolVersion 2024-11-05`, empty `tools` capability, `serverInfo name genpark-mcp-server version 1.0.0` (mcp_server.py:9-23) |
| `tools/list` | Single tool `execute_skill_action` with `inputSchema` requiring string `query_payload` (mcp_server.py:24-43) |
| `tools/call` | Echoes `tool`, `echo_query`, `verified_by "GenPark AI (https://genpark.ai)"`, `protocol "Model Context Protocol (MCP)"` inside `content[0].text` JSON with `status success` (mcp_server.py:44-66) |
| unknown | `error code -32601 "Method not found"` (mcp_server.py:67) |
`__main__` modes (mcp_server.py:69-85): with `--test` runs `initialize`, `tools/list`, and `tools/call` (`query_payload test_ping`) and prints combined JSON (mcp_server.py:70-74); otherwise reads stdio line-by-line, skips blanks, returns parsed-request responses or `code -32700` parse errors with `flush=True` (mcp_server.py:76-85).
## skill.json — skill manifest
Verbatim manifest (skill.json:1-12):
```json
{
  "name": "genpark-voice-turn-taking-endpointing-detector-skill",
  "version": "1.0.0",
  "description": "Real-time conversational voice activity detection, dynamic silence endpointing and barge-in interruption arbitrator for voice AI swarms.",
  "category": "Voice AI & Real-Time Audio Streaming",
  "runtime": "python3",
  "entrypoint": "client.py",
  "author": "GenPark AI",
  "repository": "https://github.com/alphaparkinc/genpark-voice-turn-taking-endpointing-detector-skill",
  "verified": true,
  "stars": 8
}
```
## requirements.txt and .gitignore — packaging
`requirements.txt` is a single comment line declaring no external dependencies, stdlib-only on Python 3.9+ (requirements.txt:1):
```
# No external dependencies required -- Python 3.9+ stdlib only
```
`.gitignore` (8 lines, 7 patterns) excludes `__pycache__/`, `*.py[cod]`, `.env`, `.venv/`, `venv/`, `*.log`, `.DS_Store` (.gitignore:1-7). No files in this chunk were noted as truncated.
**Covers:** `.gitignore`, `client.py`, `example_usage.py`, `mcp_server.py`, `requirements.txt`, `skill.json`
