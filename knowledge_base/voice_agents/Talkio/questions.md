---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: Talkio

### Q1. What is Talkio's three-way contract, maturity status, and install?

> [!tip]- Answer
> You bring STT, LLM, and TTS providers (or custom implementations); Talkio handles turn-taking, interruptions, cancellation, and streaming coordination; you consume an event stream of transcripts, tokens/sentences, and audio. It is a vibe-engineered alpha ("TAWK-yo") that is explicitly not production-ready, with Apache-2.0 license, installed via `npm install talkio` plus `npm install @talkio/deepgram`. See [[wiki/01-latest-commit|Latest commit]].

### Q2. Name the six parallel XState actors and the hierarchical state machine.

> [!tip]- Answer
> The actors are STT (transcription), VAD (voice activity detection, optional with STT fallback), Turn Detector (semantic turn boundaries, optional), LLM (response generation with filler support), TTS (sentence-level streaming synthesis), and Audio Streamer (output buffering with backpressure handling). The hierarchy is `idle → running → stopped`, with `running` containing `listening` (idle ↔ userSpeaking), `transcribing`, `responding`, and `streaming` (silent ↔ streaming). See [[wiki/01-talkio|Talkio]].

### Q3. How do interruption detection and cancellation work, including the numbers?

> [!tip]- Answer
> Detection is dual-path: fast VAD-based (~100 ms) with STT-based fallback, gated by `minDurationMs: 200` so shorter sounds are ignored. On interrupt an AbortSignal propagates through all actors — LLM generation is cancelled, pending TTS is aborted, the audio queue is cleared, and resources are cleaned up — backed by default timeouts of 30 s (LLM) and 10 s (TTS). See [[wiki/01-talkio|Talkio]].

### Q4. How does Talkio cut perceived latency, and what observability comes built in?

> [!tip]- Answer
> TTS synthesis starts on the first complete sentence rather than the full LLM response, the audio streamer applies backpressure-aware buffering with graceful degradation, and `ctx.say()` speaks filler updates (e.g. "Checking the weather in Tokyo...") during tool calls or slow reasoning. `agent.getSnapshot()` exposes latency (time-to-first-token, time-to-first-audio, turn duration), turn counts (total, completed, interrupted), and per-source errors without external tooling. See [[wiki/01-talkio|Talkio]].

### Q5. When should a team pick Talkio over LiveKit Agents, Pipecat, OpenAI Agents SDK, or a managed platform?

> [!tip]- Answer
> Pick Talkio for TypeScript projects wanting maximum flexibility with no infrastructure: BYO any LLM SDK, no provider lock-in, first-class custom providers, and runtime/transport/platform agnosticism (Bun, Node, Deno, Edge; WebSocket, WebRTC-via-external-library, HTTP streaming). Choose LiveKit Agents when already on LiveKit/WebRTC rooms, Pipecat for Python with 40+ provider integrations, OpenAI Agents SDK for the Realtime API with guardrails/handoffs, and managed platforms (Vapi, Retell, Bland AI) only when per-minute fees are worth hands-off hosting, scaling, and telephony. See [[wiki/02-orchestration-libraries|Orchestration Libraries]].

### Q6. Why does Talkio ship an `LLMFunction` interface instead of bundling LLM clients, and how do you extend it?

> [!tip]- Answer
> The interface gives choice (Vercel AI SDK, OpenAI SDK, Anthropic SDK, any client), control (full access to streaming, tool calls, model-specific features), and future-proof model swaps without touching orchestration code. Inside it the `ctx` object offers `token`, `sentence`, `complete`, `say`/`interrupt`, `isSpeaking`, `messages`, and `signal`, as shown in the worked `gpt-4o-mini` + Deepgram `nova-3`/`aura-2-thalia-en` streaming example that splits text on `/^(.*?[.!?])\s+(.*)$/s`. Unsupported or self-hosted models plug in via `createCustomSTTProvider`, `createCustomLLMProvider`, and `createCustomTTSProvider`, while providers stay tree-shakeable (`talkio` core plus only what you install). See [[wiki/02-why-no-built-in-llm|Why no built-in LLM]].

### Q7. A TypeScript team asks whether to build their voice prototype on Talkio — what do you recommend?

> [!tip]- Answer
> Recommend it for a maximum-flexibility prototype with no infrastructure, where BYO providers, `ctx.say()` fillers, and deploy-anywhere portability matter — while making the alpha caveats explicit: vibe-engineered and not production-ready, expect API changes, only one provider package so far, and `PACKAGE-MATURITY.md` as required reading. Steer teams needing WebRTC rooms, Python ecosystems, OpenAI guardrails, or hands-off telephony toward LiveKit, Pipecat, OpenAI Agents SDK, or a managed platform per the README's own comparison. See [[wiki/02-orchestration-libraries|Orchestration Libraries]].
