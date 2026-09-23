> [[index|Wiki]] | [[summary|Summary]]

# TEN Framework: Voice AI That Can Actually Be Interrupted — Digest

## 1. [[wiki/01-is-this-one-of-the-best|Is this one of the best]]

**In one sentence:** TEN Framework is an open-source runtime for real-time multi-model conversational voice AI, built as a graph of extensions rather than a text-first STT-to-LLM-to-TTS chain, so it can handle streaming audio, interruptions, turn detection, and parallel tool use — at the cost of heavier setup.

## Key points

- TEN is framed as an open-source runtime for building real-time multi-model conversational AI agents, with voice as the main focus plus vision, avatars, telephony, and edge deployments.
- The core architecture claim is agents as a graph of extensions (STT, LLM, TTS, memory, tools, VAD, turn detection) instead of a straight chain, because real conversations are messy and users interrupt.
- Simple chained pipelines (audio in → STT → LLM → TTS readback) work for simple setups but fall apart in real conversation since audio keeps streaming while the model thinks and the agent must stop speaking, cancel generation, detect silence, or call tools in parallel.
- Extensions can be written in Python, C++, Go, Rust, or TypeScript, each with one job (e.g., speech recognition, LLM, TTS, VAD).
- Setup requires API keys for Agora (real-time audio), Deepgram (speech recognition), an LLM like OpenAI, and ElevenLabs (voice), then one command with Docker Compose up, which takes a few minutes the first time.
- TEN ships several ready-made configurations, including a Deepgram TTS assistant (presented as the best option), a voice assistant alternative, and XAI-based ones described as not as good for interruption handling.
- Live interruption tests show the agent can be cut off mid-sentence without collapsing, but answers were imperfect — e.g., it confused the question with TensorFlow and could not state its own purpose or tell the weather in Paris.

## The argument in five moves

1. Real voice conversation is streaming and interrupt-driven, so the naive STT → LLM → TTS chain that works for simple demos collapses once users talk over the agent.
2. TEN answers this by modeling agents as a graph of single-job extensions (STT, LLM, TTS, VAD, turn detection, memory, tools) that can stop speech, cancel generation, and act in parallel.
3. That architecture comes with real setup cost — multiple API keys (Agora, Deepgram, LLM, ElevenLabs) plus Docker Compose — offset by ready-made configs and a visual designer that makes the streaming dataflow debuggable.
4. Live tests confirm the core promise (mid-sentence interruption without collapse) while showing answer quality is still bounded by the underlying models, not the framework.
5. Therefore TEN is worth it for production-grade natural voice agents needing interruption, low latency, or multimodal/edge deployment, but overkill for simple text agents or fastest-path voice prototypes.
