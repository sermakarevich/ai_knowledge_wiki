> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Is this one of the best
**In one sentence:** TEN Framework is an open-source runtime for real-time multi-model conversational voice AI, built as a graph of extensions rather than a text-first STT-to-LLM-to-TTS chain, so it can handle streaming audio, interruptions, turn detection, and parallel tool use — at the cost of heavier setup.
## Key points
- TEN is framed as an open-source runtime for building real-time multi-model conversational AI agents, with voice as the main focus plus vision, avatars, telephony, and edge deployments.
- The core architecture claim is agents as a graph of extensions (STT, LLM, TTS, memory, tools, VAD, turn detection) instead of a straight chain, because real conversations are messy and users interrupt.
- Simple chained pipelines (audio in → STT → LLM → TTS readback) work for simple setups but fall apart in real conversation since audio keeps streaming while the model thinks and the agent must stop speaking, cancel generation, detect silence, or call tools in parallel.
- Extensions can be written in Python, C++, Go, Rust, or TypeScript, each with one job (e.g., speech recognition, LLM, TTS, VAD).
- Setup requires API keys for Agora (real-time audio), Deepgram (speech recognition), an LLM like OpenAI, and ElevenLabs (voice), then one command with Docker Compose up, which takes a few minutes the first time.
- TEN ships several ready-made configurations, including a Deepgram TTS assistant (presented as the best option), a voice assistant alternative, and XAI-based ones described as not as good for interruption handling.
- Live interruption tests show the agent can be cut off mid-sentence without collapsing, but answers were imperfect — e.g., it confused the question with TensorFlow and could not state its own purpose or tell the weather in Paris.
---
## What TEN is
**Covers:** intro framing: whether TEN is a top open-source real-time voice-AI framework

TEN Framework ("10 framework") is introduced with the open question:

> "Is this one of the best open-source frameworks for real-time voice AI agents? I don't know, but we're going to find out."

Per the chunk, it handles streaming audio, interruptions, turn detection, avatars, telephony, and multi-model agents. Unlike most agent frameworks, it is "not text first with voice dropped on top" but "built for actual live conversations." The test plan is stated as: "Can I interrupt it mid sentence without the whole thing falling apart?"

## Graph of extensions, not a chain
Most voice agents start as a chain: audio comes in, speech-to-text turns it into text, the LLM writes an answer, TTS reads it back. The chunk says for a simple setup "honestly, it works," but "for a real conversation, that will probably just fall apart and collapse over time because real users interrupt."

TEN instead treats agents as graphs, not chains. Each extension has one job — one handles speech recognition, one for LLM, one for TTS, one for VAD — all working together. The big idea: "Instead of forcing everything into one pipeline, 10 lets you build an agent as a graph of extensions. So, your STT, LLM, TTS, memory, tools, all that stuff can all be separated pieces."

| Approach | Flow | Interruption behavior per chunk |
|---|---|---|
| Simple chain | Audio → STT → LLM → TTS | Falls apart when users interrupt; audio keeps streaming while the model is thinking |
| TEN graph | Extensions (STT, LLM, TTS, memory, tools, VAD, turn detection) as connected nodes | Agent can stop speaking, cancel generation, detect silence, call tools in parallel |

Extensions can be built in Python, C++, Go, Rust, or TypeScript.

## Setup and configurations
To get running, the chunk lists required API keys:

| Key | Purpose per chunk |
|---|---|
| Agora | Real-time audio (RTC) |
| Deepgram | Speech recognition |
| An LLM like OpenAI | Language model (OpenAI used here) |
| ElevenLabs | Voice |

Once keys are added, start with Docker: "one command with just Docker Compose up. It takes a few minutes the first time." TEN comes with several ready-made configurations: the Deepgram TTS assistant ("This is going to be the best one"), a voice assistant as second-best alternative, and others "using XAI, but they are not as good."

## Interruption tests (verbatim exchanges)
The presenter selects the Deepgram configuration and connects. Agent greeting:

> "10 agent connected. How can I help you today?"

Test 1 — asking what TEN is good at; the agent mishears as TensorFlow:

> "Hey, can you tell me what 10 framework is really good at?"
> "Hello. The term 10 frame"
> "I didn't interrupt you at all. Keep talking."
> "Certainly. TensorFlow is a powerful and versatile framework designed for a wide range of machine"
> "No, I didn't even talk about TensorFlow, yet you start talking about TensorFlow. How about you just stop talking?"
> "I'm sorry for the confusion earlier. If you have any other questions or need assistance with a different topic, feel free to let me know. I'm here to help."

Presenter's verdict on test 1: "you can see it's not perfect here since I can't explain the purpose of itself, so it kind of cut off there. I do have the ability to interrupt, so when I started talking, we got to interrupt, which is really cool."

Test 2 — fresh chat, weather question plus repeated interruptions:

> "10 agent connected. How can I help you today?"
> "Can you tell me the weather in Paris? Okay, so you're not able to tell me the weather. I just interrupted you, I know. What can you do?"
> "I can assist with a wide range of topics."
> "Okay, that's too long, so I'm going to cut you off right now again. Okay, thank you. Let's just stop here."
> "No problem. If you have any other questions or need assistance with something specific, feel free to let me know."

## Designer tool and strengths
The TEN manager designer tool shows how everything is connected for the chosen model (Deepgram TTS assistant), including the audio frame using Agora RTC, with clickable flows for the normal voice assistant and XAI variants. The chunk argues the visual designer matters "not because we actually need drag and drop to build things, but because real-time voice systems are actually kind of hard to debug. A graph lets you see what is connected, where the data is flowing, and where things may be slowing down."

Stated strong points: conversation quality via VAD and turn detection in real-time streaming ("They care about the agent that listens and then talks back when needed"); the visual designer for debugging; many ready-made examples (voice assistants, avatar, SIP telephony, ESP32 hardware, speaker diarization); open source with flexible deployment. Framing quote: "10 does not remove the complexity of real-time voice AI. No, it gives that complexity an architecture."

## Should you use it
Use TEN if building a production voice agent or real prototype that needs to feel natural — when interruptions, low latency, multimodal input, or flexible deployment matter, or if you already tried stitching STT, LLMs, TTS, and audio streaming yourself. Do not use it for a simple text agent ("this is too much, right? The setup is too much"); for the fastest voice prototype with least setup friction, "LiveKit Agents or Pipe Chat is probably going to get you there faster."

**Covers:** intro framing: whether TEN is a top open-source real-time voice-AI framework
