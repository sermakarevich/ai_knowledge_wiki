# Technical Analysis: alphaparkinc/genpark-neural-speech-codec-full-duplex-dialogue-engine-skill

**Repository:** https://github.com/alphaparkinc/genpark-neural-speech-codec-full-duplex-dialogue-engine-skill
**Version analyzed:** 1.0.0
**Date:** 2026-09-22
**Wiki:** [[index]]

## 1. Overview

Problem space: turn-based voice assistants alternate strictly between listening and speaking, which prevents interruption, overlap, and continuous live audio streaming. Natural spoken dialogue requires simultaneous listen-and-synthesize paths with low bidirectional latency and tokenized audio framing. The primary user is an AI-agent developer integrating realtime voice into an agent framework (Claude/Cursor-style tooling) via a drop-in skill.

How the repo addresses it: it packages a Moshi-style full-duplex dialogue contract as a GenPark AI Agent Skill (README.md:11; skill.json:3). A JSON request enters the Skill, is routed to a Core Engine, and returns structured output (README.md:20-24). Concretely the package exposes `NeuralSpeechCodecFullDuplexDialogueEngineClient.stream_duplex_audio_turn` (client.py:2) behind a `skill.json` manifest (skill.json:2-6) with entrypoint `client.py` and example `example_usage.py` (skill.json:36-37), plus an MCP server stub launched via `python mcp_server.py` (README.md:28; mcp_server.py:2-3). The implementation at this snapshot is a deterministic stub returning fixed telemetry, not a working codec.

## 2. High-Level Architecture

```
User / AI Agent
       │
       │ JSON Request (incoming_audio_chunk_bytes, sample_rate_hz)
       ▼
GenPark AI Skill (skill.json manifest ─► client.py entrypoint)
       │
       │ method call: stream_duplex_audio_turn(...)
       ▼
Core Engine (stubbed: fixed dict, no codec/DSP/network)
       │
       │ Structured Output (duplex_turn_id, latency, socket URL, flags)
       ▼
User / AI Agent

Side channel:
Core Engine ─ ► wss://speech.genpark.ai/moshi/7721 (declared string only, never opened)
MCP wrapper: mcp_server.py ─ ► stdout JSON status (no transport loop)
```

Data-flow narrative:

1. Caller constructs `NeuralSpeechCodecFullDuplexDialogueEngineClient` and invokes `stream_duplex_audio_turn(incoming_audio_chunk_bytes=4096, sample_rate_hz=24000)` (client.py:2; example_usage.py:4-5).
2. The Skill layer validates intent against `skill.json` inputs `incoming_audio_chunk_bytes` (skill.json:15-17) and `sample_rate_hz` (skill.json:18-20); no runtime validation code exists.
3. The Core Engine stub ignores the inputs and builds a hardcoded 7-key dict with turn id, codec framerate, latency, token count, timbre loss, duplex flag, and socket URL (client.py:4-10).
4. The caller reads declared outputs `duplex_turn_id` (skill.json:23-25), `bidirectional_latency_ms` (skill.json:26-28), `simultaneous_listening_synthesis_active` (skill.json:29-31), `live_duplex_socket_url` (skill.json:32-34) and prints them (example_usage.py:6-9).
5. The MCP path is orthogonal: `run_mcp_server()` prints a one-shot JSON status payload with `supported_tools` `["execute_skill_action"]` (mcp_server.py:2-3) and exits; no request is routed to the client.

Persistent state: none. No database, cache, file, socket, or session store exists in the snapshot. The only state-like values are hardcoded literals in the return dict (client.py:4-10) and the manifest (skill.json:1-38). `.gitignore` excludes `__pycache__/`, `*.py[cod]`, `.env`, `.venv/`, `venv/`, `*.log`, `.DS_Store` (.gitignore:1-7) but no code reads them.

## 3. The Duplex Turn

The central concept is the duplex turn: a single simultaneous listen-and-synthesize exchange represented as a plain 7-key `dict` returned per call (client.py:3-11). There is no class hierarchy, dataclass, codec frame type, or stream handle; the dict is the entire abstraction.

Named kinds/types (all fields of the single return type, client.py:4-10; mirrored in skill.json outputs where noted):

- `duplex_turn_id: string` = `'msh_dpx_7721'` (client.py:4; skill.json:23-25) — fixed correlation id.
- `codec_framerate_hz: float` = `12.5` (client.py:5) — declared neural-codec frame rate; not in skill.json outputs.
- `bidirectional_latency_ms: integer` = `160` (client.py:6; skill.json:26-28) — declared round-trip budget.
- `inner_monologue_tokens_generated: integer` = `14` (client.py:7) — Moshi-style inner-monologue token count; not in skill.json outputs.
- `audio_timbre_cloning_loss: float` = `0.012` (client.py:8) — voice-cloning quality metric; not in skill.json outputs.
- `simultaneous_listening_synthesis_active: boolean` = `True` (client.py:9; skill.json:29-31) — duplex-active flag.
- `live_duplex_socket_url: string` = `'wss://speech.genpark.ai/moshi/7721'` (client.py:10; skill.json:32-34) — purported live socket; never connected.

Key queries (the only two operations in the snapshot):

```python
class NeuralSpeechCodecFullDuplexDialogueEngineClient:
    def stream_duplex_audio_turn(self, incoming_audio_chunk_bytes=4096, sample_rate_hz=24000):
```

Verbatim signature from client.py:2. The single query pattern is construct-then-call with an optional positional chunk-size override, as in `client.stream_duplex_audio_turn(8192)` (example_usage.py:5). There is no cancel, close, poll, callback, async iterator, or socket-read API.

## 4. LLM / External Service Integration

The repo calls no LLM and no external API. All outputs are locally constructed literals (client.py:4-10); no `requests`, `websocket`, `openai`, `anthropic`, `torch`, `torchaudio`, or audio I/O import appears in the snapshot. The `wss://speech.genpark.ai/moshi/7721` value (client.py:10) is a string constant, never dialed.

- Providers: none.
- Required calls: none.
- Optional calls: none.
- Env vars: none (no `os.environ`/`os.getenv` usage; `.env` is git-ignored at .gitignore:3 but never read).
- Authentication: none.

## 5. The Duplex Streaming Pipeline

Primary workflow: streaming one duplex audio turn through the stub client and printing its telemetry.

1. Import the client class — `from client import NeuralSpeechCodecFullDuplexDialogueEngineClient` (example_usage.py:1). No package init or installer; `requirements.txt` declares stdlib only (requirements.txt:1).
2. Instantiate with no arguments — `client = NeuralSpeechCodecFullDuplexDialogueEngineClient()` (example_usage.py:4). The class defines no `__init__` (client.py:1-2), so construction carries no configuration.
3. Submit an audio chunk — `res = client.stream_duplex_audio_turn(8192)` (example_usage.py:5), overriding the `incoming_audio_chunk_bytes=4096` default while leaving `sample_rate_hz=24000` at default (client.py:2). Inputs are accepted but unused inside the method body (client.py:3-11).
4. Receive the fixed turn dict — keys `duplex_turn_id` through `live_duplex_socket_url` (client.py:4-10). No branching, error path, retry, or streaming chunk is produced.
5. Render turn identity and latency — `print('Neural Duplex Dialogue: ' + res['duplex_turn_id'] + ' (Latency: ' + str(res['bidirectional_latency_ms']) + 'ms)')` (example_usage.py:6).
6. Render codec/token telemetry — `print('Inner Monologue Tokens: ' + str(res['inner_monologue_tokens_generated']) + ' | Codec Rate: ' + str(res['codec_framerate_hz']) + ' Hz')` (example_usage.py:7).
7. Render duplex flag and socket — `print('Simultaneous Listen/Talk: ' + str(res['simultaneous_listening_synthesis_active']))` (example_usage.py:8) and `print('Socket URL: ' + res['live_duplex_socket_url'])` (example_usage.py:9).
8. (Separate entry point) Emit MCP status — `run_mcp_server()` prints `{"mcp_version":"1.0.0","protocol":"Model Context Protocol","status":"ACTIVE_LISTENING","supported_tools":["execute_skill_action"]}` (mcp_server.py:2-3). Not connected to steps 1–7.

Every function in the snapshot: `NeuralSpeechCodecFullDuplexDialogueEngineClient.stream_duplex_audio_turn` (client.py:2), `main` (example_usage.py:3), `run_mcp_server` (mcp_server.py:2).

## 6. Key Files

| File | Lines | What It Does |
|---|---|---|
| README.md | cited 7–33 | Repo title, Python 3.9+/MIT/MCP badges, purpose statement, `example_usage.py` quick start, JSON→Skill→Core-Engine→structured-output diagram, `mcp_server.py` entry point, macro-component list |
| skill.json | 1–38 | Skill manifest: name, version 1.0.0, description, author `genpark`, category `neural-voice`, 5 tags, 2 inputs, 4 outputs, entrypoint `client.py`, example `example_usage.py` |
| client.py | 1–11 | Sole engine file: client class plus `stream_duplex_audio_turn` returning the hardcoded 7-key duplex-turn dict |
| example_usage.py | 1–12 | Runnable demo: instantiates client, calls turn with 8192-byte chunk, prints id/latency/tokens/rate/flag/socket |
| mcp_server.py | 1–5 | MCP stub: `run_mcp_server()` prints one-shot JSON status with `supported_tools`; no server loop or tool dispatch |
| requirements.txt | 1 | Dependency declaration: comment-only line stating stdlib-only, Python 3.9+ |
| .gitignore | 1–7 | Ignore rules for `__pycache__/`, `*.py[cod]`, `.env`, `.venv/`, `venv/`, `*.log`, `.DS_Store` |

Only seven files are documented in the wiki snapshot (02-top-level-files.md:113); no additional source, test, config, or asset files are covered.

## 7. Dependencies

| Package | Version constraint | Purpose |
|---|---|---|
| *(none — stdlib only)* | `Python 3.9+` (requirements.txt:1) | Runtime baseline; exact declaration is the comment `# No external dependencies required -- Python 3.9+ stdlib only` |
| `json` (stdlib) | *(bundled with Python 3.9+)* | Serializes the MCP status payload in `mcp_server.py` (mcp_server.py:1-3) |

No third-party, audio, ML, network, or MCP-SDK packages are declared or imported.

## 8. CLI / Usage Surface

Entry points:

| Entry point | Command | Effect |
|---|---|---|
| Demo | `python example_usage.py` (README.md:15) | Runs `main()` (example_usage.py:3): one stub duplex turn with chunk size 8192, prints 4 lines (example_usage.py:6-9) |
| MCP stub | `python mcp_server.py` (README.md:28) | Runs `run_mcp_server()` (mcp_server.py:2): prints single JSON status line to stdout and exits |
| Library | `from client import NeuralSpeechCodecFullDuplexDialogueEngineClient` (example_usage.py:1) | Importable class; single method `stream_duplex_audio_turn(incoming_audio_chunk_bytes=4096, sample_rate_hz=24000)` (client.py:2) |

Env vars: none. No variable is read or documented.

Config (skill.json manifest):

| Field | Value |
|---|---|
| `name` (skill.json:2) | `genpark-neural-speech-codec-full-duplex-dialogue-engine-skill` |
| `version` (skill.json:3) | `1.0.0` |
| `author` (skill.json:5) | `genpark` |
| `category` (skill.json:6) | `neural-voice` |
| `tags` (skill.json:7-13) | `moshi`, `kyutai`, `full-duplex-speech`, `neural-codec`, `realtime-voice` |
| `input incoming_audio_chunk_bytes` (skill.json:15-17) | integer |
| `input sample_rate_hz` (skill.json:18-20) | integer |
| `output duplex_turn_id` (skill.json:23-25) | string |
| `output bidirectional_latency_ms` (skill.json:26-28) | integer |
| `output simultaneous_listening_synthesis_active` (skill.json:29-31) | boolean |
| `output live_duplex_socket_url` (skill.json:32-34) | string |
| `entrypoint` (skill.json:36) | `client.py` |
| `example` (skill.json:37) | `example_usage.py` |

## 9. Extensibility Points

- Real codec + streaming transport → replace the body of `NeuralSpeechCodecFullDuplexDialogueEngineClient.stream_duplex_audio_turn` in `client.py` (client.py:2-11); add `__init__` for sample rate, frame size, socket/auth, and yield or callback per chunk instead of returning one dict.
- New turn fields or corrected schema → extend the return dict in `client.py` (client.py:4-10) and mirror them in `skill.json` inputs/outputs (skill.json:15-34); note three returned keys (`codec_framerate_hz`, `inner_monologue_tokens_generated`, `audio_timbre_cloning_loss`) currently have no manifest output entry.
- Real MCP tool surface → rewrite `run_mcp_server` in `mcp_server.py` (mcp_server.py:2-3) on top of the MCP Python SDK with a persistent transport and an `execute_skill_action` handler that delegates to the client; the current `print`-and-exit cannot serve tools.
- New demos/benchmarks → copy `example_usage.py` `main()` (example_usage.py:3-9) into per-scenario scripts (latency sweep, interruption test, socket round-trip) without touching the client signature.
- Dependency or version policy → edit `requirements.txt` (requirements.txt:1) to pin the codec/audio/network stack and align the `Python 3.9+` floor with actual minimum features used.

## 10. Limitations and Gotchas

- **Stubbed physics: every call returns identical telemetry.** `duplex_turn_id`, latency 160 ms, 14 tokens, 12.5 Hz, loss 0.012, and socket URL are literals (client.py:4-10); inputs `incoming_audio_chunk_bytes`/`sample_rate_hz` (client.py:2) are ignored, so no latency, quality, or interruption claim is measurable.
- **Manifest schema is a subset of the returned dict.** `skill.json` declares 4 outputs (skill.json:23-34) but the client returns 7 keys (client.py:4-10); consumers validating strictly against the manifest will drop `codec_framerate_hz`, `inner_monologue_tokens_generated`, and `audio_timbre_cloning_loss` that the demo prints (example_usage.py:7).
- **MCP server is print-and-exit, not a server.** `run_mcp_server()` emits one JSON line with `status: ACTIVE_LISTENING` (mcp_server.py:2-3) but opens no port, holds no session, and dispatches no `execute_skill_action`; pointing an MCP client at it will fail after the first line.
- **No error handling, types, tests, or audio path.** There is no validation of chunk size/sample rate, no exception path, no type annotations, no test file, and no microphone/speaker/socket code — passing `0`, negative, or non-integer chunk sizes behaves identically to the demo's `8192` (example_usage.py:5).
- **Socket URL implies liveness that does not exist.** `wss://speech.genpark.ai/moshi/7721` (client.py:10) is never opened and embeds a fixed session id matching the fixed turn id (client.py:4); treating it as a connectable endpoint will produce connection failures unrelated to any real service.

## 11. How It Compares to Alternatives

- **Kyutai Moshi (kyutai/moshi):** the reference full-duplex speech-text model with a real neural audio codec (Mimi, ~12.5 Hz framing), inner-monologue text stream, and interruption handling. This repo borrows Moshi's vocabulary (12.5 Hz, inner-monologue tokens, `msh_` turn prefix at client.py:4-7) but implements none of the model, codec, or streaming; use Moshi for actual research-grade duplex dialogue.
- **LiveKit Agents + Realtime Voice:** production voice-agent stack with WebRTC transport, VAD/interruption, telephony/SIP, and pluggable STT/LLM/TTS. This repo declares a websocket URL string (client.py:10) with no transport; use LiveKit when a deployable realtime call path is required.
- **Pipecat (pipecat-ai/pipecat):** open-source orchestration framework for realtime voice/multimodal pipelines with component-level pipeline, transport, and MCP-adjacent tool patterns. This repo's "pipeline" is a single synchronous function (client.py:2); use Pipecat for composable production pipelines.
- **OpenAI Realtime API:** managed full-duplex speech-to-speech WebSocket API with function calling and server-side VAD. This repo's MCP stub (mcp_server.py:2-3) exposes only a status line with no tool dispatch; use the Realtime API for a hosted duplex endpoint with tool use.

Positioning: this repo is a skill-packaging sketch — manifest plus stub client plus demo plus MCP placeholder — signalling Moshi-style duplex intent with zero dependencies, whereas each alternative above ships a working audio/transport/model path.

## Appendix: Selected Code Snippets

1. Stub duplex-turn return payload (client.py:1-11):

```python
class NeuralSpeechCodecFullDuplexDialogueEngineClient:
    def stream_duplex_audio_turn(self, incoming_audio_chunk_bytes=4096, sample_rate_hz=24000):
        return {
            'duplex_turn_id': 'msh_dpx_7721',
            'codec_framerate_hz': 12.5,
            'bidirectional_latency_ms': 160,
            'inner_monologue_tokens_generated': 14,
            'audio_timbre_cloning_loss': 0.012,
            'simultaneous_listening_synthesis_active': True,
            'live_duplex_socket_url': 'wss://speech.genpark.ai/moshi/7721'
        }
```

2. Demo usage (example_usage.py:1-12):

```python
from client import NeuralSpeechCodecFullDuplexDialogueEngineClient

def main():
    client = NeuralSpeechCodecFullDuplexDialogueEngineClient()
    res = client.stream_duplex_audio_turn(8192)
    print('Neural Duplex Dialogue: ' + res['duplex_turn_id'] + ' (Latency: ' + str(res['bidirectional_latency_ms']) + 'ms)')
    print('Inner Monologue Tokens: ' + str(res['inner_monologue_tokens_generated']) + ' | Codec Rate: ' + str(res['codec_framerate_hz']) + ' Hz')
    print('Simultaneous Listen/Talk: ' + str(res['simultaneous_listening_synthesis_active']))
    print('Socket URL: ' + res['live_duplex_socket_url'])

if __name__ == '__main__':
    main()
```

3. MCP server stub (mcp_server.py:1-5):

```python
import json
def run_mcp_server():
    print(json.dumps({"mcp_version":"1.0.0","protocol":"Model Context Protocol","status":"ACTIVE_LISTENING","supported_tools":["execute_skill_action"]}))
if __name__ == "__main__":
    run_mcp_server()
```

4. Skill manifest (skill.json:1-38, comment line excluded):

```json
{
  "name": "genpark-neural-speech-codec-full-duplex-dialogue-engine-skill",
  "version": "1.0.0",
  "description": "GenPark AI Agent Skill - Neural speech codec full duplex dialogue engine streaming tokenized audio with simultaneous listening and synthesis.",
  "author": "genpark",
  "category": "neural-voice",
  "tags": ["moshi", "kyutai", "full-duplex-speech", "neural-codec", "realtime-voice"],
  "entrypoint": "client.py",
  "example": "example_usage.py"
}
```
