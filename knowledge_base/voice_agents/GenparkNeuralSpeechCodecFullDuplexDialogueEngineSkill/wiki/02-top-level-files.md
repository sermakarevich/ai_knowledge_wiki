> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# top-level-files
**In one sentence:** The six top-level files define the skill manifest, duplex-dialogue client, usage example, MCP server stub, dependency declaration, and ignore rules (skill.json:1-38).
## Key points
- `skill.json` declares the skill `genpark-neural-speech-codec-full-duplex-dialogue-engine-skill` v1.0.0 in category `neural-voice` by author `genpark` (skill.json:2-6).
- `client.py` exposes `NeuralSpeechCodecFullDuplexDialogueEngineClient.stream_duplex_audio_turn(incoming_audio_chunk_bytes=4096, sample_rate_hz=24000)` returning a fixed duplex-turn dict (client.py:1-2).
- The client's returned dict reports `codec_framerate_hz` 12.5, `bidirectional_latency_ms` 160, 14 inner-monologue tokens, timbre loss 0.012, and an active listen/synthesis flag with a live socket URL (client.py:4-10).
- `example_usage.py` instantiates the client, calls `stream_duplex_audio_turn(8192)`, and prints the turn id, latency, token count, codec rate, listen/talk flag, and socket URL (example_usage.py:4-9).
- `mcp_server.py` defines `run_mcp_server()` which prints a JSON status payload with `mcp_version` 1.0.0 and `supported_tools` `["execute_skill_action"]` (mcp_server.py:2-3).
- `requirements.txt` declares no external dependencies, Python 3.9+ stdlib only (requirements.txt:1).
- `.gitignore` excludes `__pycache__/`, `*.py[cod]`, `.env`, `.venv/`, `venv/`, `*.log`, and `.DS_Store` (.gitignore:1-7).
---
## skill.json
Verbatim manifest (skill.json:1-38):
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
Full tag list is `moshi`, `kyutai`, `full-duplex-speech`, `neural-codec`, `realtime-voice` (skill.json:7-13). Entrypoint is `client.py` and example is `example_usage.py` (skill.json:36-37).

| Field | Name | Type |
|---|---|---|
| input | `incoming_audio_chunk_bytes` | integer (skill.json:15-17) |
| input | `sample_rate_hz` | integer (skill.json:18-20) |
| output | `duplex_turn_id` | string (skill.json:23-25) |
| output | `bidirectional_latency_ms` | integer (skill.json:26-28) |
| output | `simultaneous_listening_synthesis_active` | boolean (skill.json:29-31) |
| output | `live_duplex_socket_url` | string (skill.json:32-34) |

## client.py
Exact signature with parameter names and defaults (client.py:2):
```python
class NeuralSpeechCodecFullDuplexDialogueEngineClient:
    def stream_duplex_audio_turn(self, incoming_audio_chunk_bytes=4096, sample_rate_hz=24000):
```
Verbatim return payload (client.py:3-11):
```python
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

| Return key | Value |
|---|---|
| `duplex_turn_id` | `'msh_dpx_7721'` (client.py:4) |
| `codec_framerate_hz` | `12.5` (client.py:5) |
| `bidirectional_latency_ms` | `160` (client.py:6) |
| `inner_monologue_tokens_generated` | `14` (client.py:7) |
| `audio_timbre_cloning_loss` | `0.012` (client.py:8) |
| `simultaneous_listening_synthesis_active` | `True` (client.py:9) |
| `live_duplex_socket_url` | `'wss://speech.genpark.ai/moshi/7721'` (client.py:10) |

## example_usage.py
Verbatim usage (example_usage.py:1-12):
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
The example passes positional `8192` for `incoming_audio_chunk_bytes`, overriding the `4096` default (example_usage.py:5; client.py:2).

## mcp_server.py
Verbatim server stub (mcp_server.py:1-5):
```python
import json
def run_mcp_server():
    print(json.dumps({"mcp_version":"1.0.0","protocol":"Model Context Protocol","status":"ACTIVE_LISTENING","supported_tools":["execute_skill_action"]}))
if __name__ == "__main__":
    run_mcp_server()
```

## requirements.txt
Verbatim declaration (requirements.txt:1):
```
# No external dependencies required -- Python 3.9+ stdlib only
```

## .gitignore
Verbatim ignore rules (.gitignore:1-7):
```
__pycache__/
*.py[cod]
.env
.venv/
venv/
*.log
.DS_Store
```

**Covers:** skill.json, client.py, example_usage.py, mcp_server.py, requirements.txt, .gitignore (no truncated files noted in chunk)
