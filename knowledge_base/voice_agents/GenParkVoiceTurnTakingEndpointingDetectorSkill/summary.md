# Technical Analysis: alphaparkinc/genpark-voice-turn-taking-endpointing-detector-skill

**Repository:** https://github.com/alphaparkinc/genpark-voice-turn-taking-endpointing-detector-skill
**Version analyzed:** 1.0.0
**Date:** 2026-09-22
**Wiki:** [[index]]

## 1. Overview

Problem space: real-time voice agents must decide, from a continuous PCM frame stream, whether the user is speaking, whether a pause ends the turn, and whether incoming speech should interrupt agent playback. Naive fixed-silence timeouts either cut users off or add dead air; without barge-in arbitration the agent talks over the user.

How the repo addresses it: a zero-dependency Python evaluator (`client.py:3-7`) classifies each frame by energy against a dB threshold, counts consecutive speech frames to confirm onset, accumulates post-onset silence, and emits one of three decisions — `CONTINUE_LISTENING`, `TRIGGER_BARGE_IN_INTERRUPT`, `DISPATCH_AGENT_SYNTHESIS` (`02-top-level-files.md:7`, `client.py:57-70`). Silence reaching the endpointing threshold dispatches LLM synthesis (`01-overview.md:8`); speech energy above threshold while the agent is speaking cuts agent audio (`01-overview.md:7`). The package ships the detector plus a demo (`example_usage.py:6-18`), a stdio MCP wrapper (`mcp_server.py:5-66`), and a skill manifest (`skill.json:1-12`).

Primary user: a developer wiring turn-taking into a voice-agent loop who calls `evaluate_audio_frame_stream` per buffered frame batch and branches on the returned decision.

## 2. High-Level Architecture

```
Real-time PCM frame stream (List[Dict])
        │
        ▼
Energy & VAD Frame Analyzer ── client.py:30-33
        │  is_speech = energy_db >= threshold
        ▼
Agent-Speaking Branch ── client.py:40-41
        │
        ├─► agent_is_speaking=True + speech confirmed ──► TRIGGER_BARGE_IN_INTERRUPT
        │
        └─► agent_is_speaking=False ──► Accumulate speech/silence ── client.py:35-47
                                            │
                                            ▼
                                   Silence >= min_silence_duration_ms?
                                            │
                                     Yes ───┴─── No
                                      │          │
                                      ▼          ▼
                        DISPATCH_AGENT_SYNTHESIS  CONTINUE_LISTENING
```

Data-flow narrative:

1. Caller submits a batch of frame dicts (`energy_db`, `duration_ms`) with an `agent_is_speaking` flag to `evaluate_audio_frame_stream` (`client.py:18-22`).
2. Each frame is normalized to defaults (`energy_db=-60.0`, `duration_ms=20`) and thresholded into `is_speech` (`client.py:30-33`).
3. Consecutive speech frames increment a counter and reset the silence accumulator; reaching `consecutive_speech_frames_threshold` (default 3) latches `speech_started`, and if the agent is speaking also latches `user_interrupted` (`client.py:35-41`).
4. Post-onset non-speech frames accumulate `consecutive_silence_ms`; crossing `min_silence_duration_ms` (default 450) latches `turn_completed` (`client.py:44-47`).
5. Decision precedence applies: `user_interrupted` overrides `turn_completed` overrides default (`client.py:57-61`); the full per-frame audit and counters return in one dict (`client.py:63-70`).

Persistent state: none. The detector instance holds only the three constructor thresholds; all counters (`consecutive_speech`, `consecutive_silence_ms`, flags, `frame_audit`) are locals recomputed per `evaluate_audio_frame_stream` call. No disk, database, or cross-call memory exists.

## 3. The Energy-Gated Turn State

Representation: ephemeral per-call scalar state derived from the input batch — `consecutive_speech: int`, `consecutive_silence_ms: int`, `speech_started: bool`, `user_interrupted: bool`, `turn_completed: bool`, plus a `frame_audit: List[dict]` with per-frame `energy_db`, `is_speech`, `silence_accumulated_ms`, `interrupted`, `turn_completed` (`client.py:49-55`).

Named kinds/types:

- Decisions (3): `CONTINUE_LISTENING`, `TRIGGER_BARGE_IN_INTERRUPT`, `DISPATCH_AGENT_SYNTHESIS` (`client.py:57-70`).
- Thresholds (3): `min_silence_duration_ms: int = 450`, `barge_in_energy_threshold_db: float = -28.0`, `consecutive_speech_frames_threshold: int = 3` (`client.py:8-13`).
- Return payload keys (6): `decision`, `barge_in_detected`, `turn_completed`, `final_silence_ms`, `analyzed_frames_count`, `frame_audit` (`client.py:63-70`).

Key queries: there is one query — evaluate a frame batch:

```python
def evaluate_audio_frame_stream(
    self,
    frames: List[Dict[str, Any]],
    agent_is_speaking: bool = False
) -> Dict[str, Any]:
```

(`client.py:18-22`). Classification inside the loop is a single comparison: `is_speech = energy_db >= barge_in_energy_threshold_db` (`client.py:33`).

## 4. LLM / External Service Integration

The repo calls no LLM or external API. Turn completion is a signal for the caller to dispatch synthesis downstream (`README.md:22`), but no HTTP, SDK, or model-inference call exists in `client.py`, `example_usage.py`, or `mcp_server.py`. The MCP server's `tools/call` echoes the input payload rather than invoking a tool (`mcp_server.py:44-66`).

| Item | Value |
|---|---|
| Providers | none |
| Required calls | none |
| Optional calls | none (downstream LLM dispatch is the caller's responsibility) |
| Env vars | none |

## 5. The Stream Evaluation and Dispatch Pipeline

Step by step, all functions in `client.py`:

1. `VoiceTurnTakingEndpointingDetector.__init__` (`client.py:8-13`) — stores the three thresholds; no validation or I/O.
2. `VoiceTurnTakingEndpointingDetector.evaluate_audio_frame_stream` (`client.py:18-22`) — iterates frames; per frame applies defaults (`client.py:30-31`), computes `is_speech` (`client.py:33`), updates speech counter and latches onset/interrupt (`client.py:35-41`), or accumulates silence and latches completion (`client.py:44-47`), appends the audit row (`client.py:49-55`).
3. Decision resolution, same function (`client.py:57-61`) — `CONTINUE_LISTENING` default, overridden by `TRIGGER_BARGE_IN_INTERRUPT` if `user_interrupted`, else `DISPATCH_AGENT_SYNTHESIS` if `turn_completed`.
4. Payload assembly, same function (`client.py:63-70`) — returns the six-key dict.
5. Demo verification in `example_usage.py` (`example_usage.py:6-20`) — constructs the detector with `min_silence_duration_ms=400`, feeds 3× speech + 2× silence frames with `agent_is_speaking=False`, asserts `turn_completed is True` and `decision == "DISPATCH_AGENT_SYNTHESIS"`.
6. MCP transport in `mcp_server.py:handle_mcp_request` (`mcp_server.py:5-67`) — dispatches `initialize`, `tools/list`, `tools/call`, or `-32601`; `__main__` (`mcp_server.py:69-85`) runs `--test` self-check or a stdio JSON-RPC loop with `-32700` parse-error handling.

## 6. Key Files

| File | Lines | What It Does |
|---|---|---|
| `client.py` | ~70 | `VoiceTurnTakingEndpointingDetector`: energy classification, onset/silence counters, three-way decision |
| `example_usage.py` | ~20 | Demo stream (3 speech + 2 silence frames) with assertions on turn completion |
| `mcp_server.py` | ~85 | Stdio JSON-RPC 2.0 wrapper: `initialize`, `tools/list`, `tools/call`, `--test` mode |
| `skill.json` | 12 | Skill manifest: name, version 1.0.0, runtime python3, entrypoint client.py, verified flag |
| `requirements.txt` | 1 | Declares zero external dependencies, Python 3.9+ stdlib only |
| `.gitignore` | 7-8 | Excludes `__pycache__/`, `*.py[cod]`, `.env`, venv dirs, `*.log`, `.DS_Store` |
| `README.md` | ~29 | Repo overview, mermaid pipeline diagram, decision table, feature list |

## 7. Dependencies

| Package | Version constraint | Purpose |
|---|---|---|
| Python (stdlib only: `json`, `sys`, typing) | `Python 3.9+` (from `requirements.txt:1`) | Runtime; no third-party packages required |
| (none — no optional dependencies) | — | `requirements.txt` is a single comment line |

## 8. CLI / Usage Surface

Entry points: library import (`client.py`), demo script (`example_usage.py`), MCP stdio server (`mcp_server.py`). No argument parser beyond a `--test` flag.

| Command | Effect |
|---|---|
| `python example_usage.py` | Runs 5-frame demo; asserts dispatch decision |
| `python mcp_server.py --test` | Runs `initialize` + `tools/list` + `tools/call` self-check, prints combined JSON (`mcp_server.py:70-74`) |
| `python mcp_server.py` | Stdio JSON-RPC loop; blank lines skipped, parse errors return `-32700` (`mcp_server.py:76-85`) |

| MCP method | Input | Output |
|---|---|---|
| `initialize` | `{"method":"initialize","id":…}` | `protocolVersion 2024-11-05`, `serverInfo genpark-mcp-server 1.0.0` (`mcp_server.py:9-23`) |
| `tools/list` | `{"method":"tools/list","id":…}` | Single tool `execute_skill_action`, `inputSchema` requires string `query_payload` (`mcp_server.py:24-43`) |
| `tools/call` | `{"method":"tools/call","params":{"name":…,"arguments":{"query_payload":…}}}` | Echo JSON with `tool`, `echo_query`, `verified_by`, `protocol`, `status success` (`mcp_server.py:44-66`) |

| Env var | Required | Effect |
|---|---|---|
| (none) | — | No environment variables are read |

| Config | Location | Effect |
|---|---|---|
| `min_silence_duration_ms=450` | `client.py:8-13` constructor | Post-onset silence needed for `turn_completed` |
| `barge_in_energy_threshold_db=-28.0` | `client.py:8-13` constructor | Per-frame speech/silence boundary |
| `consecutive_speech_frames_threshold=3` | `client.py:8-13` constructor | Speech frames needed for onset/interrupt |
| `agent_is_speaking=False` | `client.py:18-22` per-call flag | Gates `user_interrupted` latching |
| `skill.json` manifest | `skill.json:1-12` | Name, version, runtime, entrypoint metadata |

## 9. Extensibility Points

- New VAD logic (spectral features, adaptive noise floor, ML scores): replace the threshold comparison in `client.py:33` inside `evaluate_audio_frame_stream`; keep the `is_speech` boolean contract so counters are unaffected.
- New turn-taking policy (hangover, max-turn cap, confidence weighting): extend the silence/onset block in `client.py:35-47` or subclass `VoiceTurnTakingEndpointingDetector` and override `evaluate_audio_frame_stream`.
- New decisions or priorities: edit the precedence chain in `client.py:57-61` and the payload keys in `client.py:63-70`; update the demo assertions in `example_usage.py:18-20` to match.
- Real tool execution behind MCP: replace the echo body in `mcp_server.py:44-66` with a dispatch that instantiates the detector and returns its result; add the tool schema in `mcp_server.py:24-43`.
- Stateful streaming (cross-chunk counters): add instance attributes in `client.py:8-13` and move the per-call locals out of `evaluate_audio_frame_stream`; add a `reset()` method since none exists today.

## 10. Limitations and Gotchas

- **Energy-only classification misfires on noise.** `is_speech` is a single dB comparison (`client.py:33`) with no spectral, SNR, or model-based discrimination; loud non-speech trips barge-in and quiet speech is dropped as silence.
- **No cross-call state; callers must re-feed history.** All counters reset per `evaluate_audio_frame_stream` invocation, so chunked streaming without re-sending the window loses onset and silence accumulation; long pauses split across calls never reach the threshold.
- **Barge-in and completion flags latch without reset.** Once `user_interrupted` or `turn_completed` is set within a batch, the decision applies to the whole batch (`client.py:57-61`); there is no per-frame decision stream or partial-interrupt timestamp.
- **MCP wrapper does not execute the skill.** `tools/call` echoes `query_payload` (`mcp_server.py:44-66`) rather than running the detector, so MCP clients get no endpointing result until the handler is replaced.
- **Frame-duration accounting trusts caller metadata.** Missing `duration_ms` defaults to 20 ms and missing `energy_db` to −60.0 (`client.py:30-31`); mislabeled durations silently shift the `min_silence_duration_ms` comparison.

## 11. How It Compares to Alternatives

- Silero VAD (PyTorch): neural per-frame speech probabilities with tunable sensitivity; heavier runtime and a model dependency versus this repo's threshold heuristic and zero dependencies.
- WebRTC VAD (Google): frame-level GMM-based voiced/unvoiced classification in native code with aggressiveness modes; lower-level signal processing without turn-taking policy, whereas this repo adds endpointing and barge-in decisions on top of a cruder detector.
- LiveKit Agents VAD / turn detection: production pipeline combining VAD, endpointing, and interruption handling with streaming state and configurable minimum-delay parameters; stateful and framework-coupled versus this repo's stateless single-function evaluator.
- Picovoice Cobra: proprietary neural VAD with noise robustness and cross-platform SDKs; higher accuracy under noise at the cost of a binary dependency and licensing, versus this repo's auditable stdlib-only heuristic.

Positioning: this repo is a minimal, dependency-free reference policy for energy-gated endpointing and barge-in arbitration, suitable as a stub or teaching implementation; production voice stacks replace its classifier with a neural VAD while keeping its three-way decision shape.

## Appendix: Selected Code Snippets

`client.py:8-13` — constructor thresholds:

```python
def __init__(
    self,
    min_silence_duration_ms: int = 450,
    barge_in_energy_threshold_db: float = -28.0,
    consecutive_speech_frames_threshold: int = 3
):
```

`example_usage.py:6-14` — detector setup and simulated stream:

```python
detector = VoiceTurnTakingEndpointingDetector(min_silence_duration_ms=400)
```

```python
assert result["turn_completed"] is True
assert result["decision"] == "DISPATCH_AGENT_SYNTHESIS"
```

`client.py:57-61` — decision precedence:

```python
decision = "CONTINUE_LISTENING"
if user_interrupted:
    decision = "TRIGGER_BARGE_IN_INTERRUPT"
elif turn_completed:
    decision = "DISPATCH_AGENT_SYNTHESIS"
```

`skill.json:1-12` — manifest:

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
