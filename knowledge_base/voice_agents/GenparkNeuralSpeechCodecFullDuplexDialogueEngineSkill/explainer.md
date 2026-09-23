> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# alphaparkinc/genpark-neural-speech-codec-full-duplex-dialogue-engine-skill — In Plain Language

Imagine calling a friend who can listen and talk at the exact same moment —
never asking you to "please hold" while they think. This project packages
exactly that idea as a small, plug-in voice skill: a Moshi-style engine that
streams a live phone-call-like conversation, listening and speaking
simultaneously instead of taking turns.

## What is this about?

- This repo is a **GenPark AI Agent Skill**: a small, standardized plug-in
  that gives an AI agent a new ability — here, live voice conversation.
- That ability is **neural speech codec full-duplex dialogue** in the style
  of **Moshi** (the open voice model from Kyutai): raw microphone audio is
  squeezed into compact tokens, and the engine talks back while still
  listening, plus a **live audio streamer** over a socket connection.
- Everything lives in just six top-level files: a skill manifest
  (`skill.json`), a dialogue client (`client.py`), a runnable demo
  (`example_usage.py`), a server stub (`mcp_server.py`), a dependency file
  (`requirements.txt`), and ignore rules (`.gitignore`).
- It targets **Python 3.9+**, needs **no external dependencies** (standard
  library only), is **MIT-licensed**, and is **MCP-compatible**, so other
  agent tools can discover and call it.
- The quick start is one command: `python example_usage.py`. The agent-tool
  entry point is `python mcp_server.py`.

## Why does it matter?

- Normal voice bots are **half-duplex walkie-talkies**: you speak, then wait
  in silence, then they answer. Humans hate that pause — we interrupt,
  say "uh-huh," and overlap constantly.
- **Full-duplex** (both directions at once) is what makes a voice agent feel
  alive instead of robotic. This skill is a template for exactly that
  behavior: simultaneous listening and synthesis.
- The headline numbers in the demo payload tell the story: **160 ms
  bidirectional latency** (fast enough to feel conversational) and a
  **12.5 Hz codec framerate** (audio compressed into a small stream of
  tokens per second, cheap to move across a network).
- It also demonstrates two modern agent patterns in miniature: a
  **skill manifest** (`skill.json` declares name, version, category
  `neural-voice`, tags, entrypoint, and inputs/outputs) and an **MCP
  server stub** (a standard way for tools like Claude or other agents to
  find and invoke the skill with `execute_skill_action`).
- Because it runs on the standard library alone, it is easy to read, copy,
  and use as scaffolding: the shape of a real-time voice skill without a
  heavy install.

## How does it work?

Think of it as a three-stop relay, exactly as the README diagram shows:

1. **You (or an AI agent) send a JSON request.** The inputs are tiny: how
   big an audio chunk to process (`incoming_audio_chunk_bytes`, default
   4096) and at what quality (`sample_rate_hz`, default 24000).
2. **The Skill hands it to the Core Engine.** The manifest (`skill.json`)
   routes the call to the entrypoint, `client.py`, whose single method
   `stream_duplex_audio_turn()` handles one back-and-forth moment of the
   call — one "duplex turn."
3. **The engine returns structured output.** The demo turn comes back as a
   dictionary: a turn id (`msh_dpx_7721`), the codec rate (12.5 Hz), the
   round-trip latency (160 ms), 14 generated inner-monologue tokens, a
   voice-cloning quality score (timbre loss 0.012, where lower means the
   cloned voice sounds closer), a flag confirming listen-and-talk mode is
   on, and a live socket URL (`wss://speech.genpark.ai/moshi/7721`) where
   the continuous audio flows.

- The demo (`example_usage.py`) shows the whole loop: create the client,
  call `stream_duplex_audio_turn(8192)` with a bigger chunk, and print the
  turn id, latency, token count, codec rate, listen/talk flag, and socket.
- The MCP stub (`mcp_server.py`) does one simple thing: when started, it
  prints a JSON status payload (`mcp_version` 1.0.0, status
  `ACTIVE_LISTENING`, supported tool `execute_skill_action`) announcing
  that the skill is ready to receive tool calls.

## Where can this be used?

- **Conversational voice assistants** that must handle interruptions:
  customer-support lines, in-car helpers, or smart-speaker skills where
  the caller talks over the bot.
- **Live translation or meeting aides** that listen to a speaker while
  simultaneously whispering the translation or summary in your ear.
- **Game characters and virtual companions** whose charm depends on
  reacting mid-sentence — laughing, back-channeling ("mm-hm"), or cutting
  in — rather than waiting for silence.
- **Agent-tool ecosystems**: any MCP-compatible assistant can advertise
  this skill in its tool list, so a text-based agent can "pick up the
  phone" by calling `execute_skill_action`.
- **Teaching and prototyping**: because the package is dependency-free and
  fully declared in `skill.json`, it works well as a starter template for
  "how do I wrap a streaming model as a skill?"

## Conclusions & takeaways

- This is **scaffolding, not a full voice model**: the client returns a
  fixed example payload rather than doing real neural encoding. Treat it
  as the wiring and contract for a Moshi-style engine, not the engine
  itself.
- The core lesson is architectural: a real-time voice skill needs only a
  **manifest** (what it is, what goes in/out), a **streaming turn method**
  (one listen-and-speak step), and a **discovery hook** (the MCP status
  payload) — everything else is the model behind the socket.
- If you remember three numbers, remember these: **160 ms** (the latency
  budget that makes overlap feel natural), **12.5 Hz** (how aggressively
  the audio is compressed into tokens), and **24000 Hz** (the default
  audio sampling quality going in).
- Next step for a builder: swap the fixed demo payload for a real codec
  and model behind `stream_duplex_audio_turn()`, keep the same
  inputs/outputs, and every MCP client keeps working unchanged.

## Jargon decoder

| Term | What it really means |
|---|---|
| Neural speech codec | Software that squeezes raw voice audio into a small stream of tokens (numbers) a model can process, then rebuilds voice from them. |
| Full-duplex dialogue | A call where both sides can speak and hear at the same time, like a phone call — the opposite of walkie-talkie turn-taking. |
| Moshi / Kyutai | Moshi is an open real-time voice AI model; Kyutai is the lab that built it. Here they name the style being imitated. |
| Inner-monologue tokens | Extra tokens the model generates as silent "thinking" alongside speech, used to plan what to say next. |
| Codec framerate (12.5 Hz) | How many compressed audio snapshots are produced per second — fewer means less bandwidth but coarser audio. |
| Bidirectional latency (160 ms) | The round-trip delay to hear you and start replying; under ~200 ms feels like natural conversation. |
| Timbre cloning loss (0.012) | A quality score for voice cloning: how far the synthetic voice is from the target voice — lower is better. |
| Skill manifest (`skill.json`) | A small ID card for the plug-in: its name, version, category, tags, entrypoint, and expected inputs/outputs. |
| MCP (Model Context Protocol) | A standard way for AI agents to discover and call outside tools; this repo's stub announces itself over MCP. |
| Duplex turn / socket URL | One back-and-forth moment of the live call, plus the persistent web address (`wss://…`) carrying the audio stream. |
