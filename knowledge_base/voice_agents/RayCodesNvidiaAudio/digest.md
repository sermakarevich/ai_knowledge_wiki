> [[index|Wiki]] | [[summary|Summary]]
# 47thtechcorner/RayCodes_Nvidia_Audio — Digest

## 1. [[wiki/01-overview|Overview]]
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

## 2. [[wiki/02-top-level-files|Top-Level Files]]
**In one sentence:** The top-level files provide the runnable two-turn demo (`main.py`), the full speech-to-speech agent engine (`voicechat_agent.py`), and the ignore rules (`.gitignore`) that keep checkpoints, audio, and bytecode out of version control.
## Key points
- `main.py` is the official pipeline runner that executes two full-duplex speech-to-speech turns — general conversation plus dynamic tool calling — via `VoiceChatAgent` (main.py:22, main.py:33).
- `main.py` initializes the agent with `VoiceChatAgent(checkpoint_dir="./checkpoint")`, downloading the Hugging Face checkpoint if not present (main.py:39).
- `voicechat_agent.py` implements the `VoiceChatAgent` engine for streaming speech understanding, dialogue reasoning, and native tool calling around model `nvidia/NVIDIA-NemotronLabs-VoiceChat-11B` (voicechat_agent.py:73, voicechat_agent.py:92).
- `VoiceChatAgent.__init__` takes `checkpoint_dir: str = "./checkpoint"`, selects `cuda` vs `cpu` with `bfloat16` vs `float32`, then calls `download_checkpoint()` and `_load_model()` (voicechat_agent.py:181).
- `VoiceChatAgent.process_turn(user_audio_wav, output_audio_file="output_response.wav")` runs one spoken dialogue turn and returns `user_audio`, `generated_text`, `tool_call`, `tool_response`, `output_audio_file`, `sample_rate`, and `turn_latency_ms` (voicechat_agent.py:217, voicechat_agent.py:252).
- `execute_tool_call(tool_name, arguments)` executes three live tools — `get_weather` (via `wttr.in`), `get_stock_price`, and `get_top_news` — and returns an error dict for unrecognized names (voicechat_agent.py:119, voicechat_agent.py:172).
- `.gitignore` excludes `assets/`, `checkpoint/`, `__pycache__/`, `*.wav`, `*.mp3`, `*.log`, and `.DS_Store` (`.gitignore:1`).

## The system in five moves
1. A single 11B full-duplex model replaces the ASR → LLM → TTS cascade, unifying streaming understanding, reasoning, and 22.05 kHz synthesis for ~450 ms turns with ~480 ms barge-in yield.
2. The Fast Conformer encoder, Nemotron Nano v2 9B backbone, and neural speech decoder run behind dual output channels so speech and `<TOOLCALL>` JSON stream side by side.
3. A strict tag protocol (`<AVAILABLE_TOOLS>` / `<TOOLCALL>` / `<TOOL_RESPONSE>`) governs when to call a listed tool, answer directly, or decline, with spoken on-hold feedback during live execution.
4. `VoiceChatAgent` boots from the `nvidia/NVIDIA-NemotronLabs-VoiceChat-11B` checkpoint (cuda/bfloat16 vs cpu/float32), and each `process_turn()` encodes 16 kHz input, generates text or `<TOOLCALL>`, executes the live tool, feeds back `<TOOL_RESPONSE>`, and writes the output WAV.
5. `main.py` demonstrates the arc end to end in two turns — general conversation then Mumbai-weather tool calling — while `.gitignore` keeps checkpoints, audio, and bytecode out of the repo.
