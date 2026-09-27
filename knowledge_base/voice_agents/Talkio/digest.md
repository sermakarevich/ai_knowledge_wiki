> [[index|Wiki]] | [[summary|Summary]]

# Talkio — Digest

## 1. [[wiki/01-talkio|Talkio]]
**In one sentence:** Talkio ("TAWK-yo") is a TypeScript-first, provider- and infrastructure-agnostic voice-AI orchestration library that coordinates BYO STT/LLM/TTS with turn-taking, dual-path interruption detection, AbortSignal cancellation, and sentence-level streaming TTS.
- Pure orchestration with zero infrastructure lock-in: runs anywhere JavaScript runs, no servers required, voice-source agnostic (phone, web, mobile, microphone, WebRTC).
- Provider agnostic: you bring STT, LLM, and TTS providers or custom implementations; Talkio handles turn-taking, interruptions, cancellation, and streaming coordination, and you consume an event stream (transcripts, tokens/sentences, audio).
- Architecture is six parallel XState actors (STT, VAD, Turn Detector, LLM, TTS, Audio Streamer) with hierarchical states `idle → running → stopped` containing `listening`, `transcribing`, `responding`, and `streaming`.
- Interruption uses dual-path detection — fast VAD-based (~100ms) with STT-based fallback — plus `minDurationMs: 200` filtering, and on interrupt cancels LLM generation, aborts pending TTS, clears the audio queue, and cleans up resources via AbortSignal propagation.
- Latency strategy is sentence-level streaming (TTS starts on first complete sentence, not full response) with backpressure-aware audio buffering, plus default timeouts of 30s for LLM and 10s for TTS.
- Filler phrases via `ctx.say()` speak contextual progress updates during tool calls/slow reasoning (e.g. "Checking the weather in Tokyo..."), and built-in metrics expose time-to-first-token, time-to-first-audio, turn counts, and per-source errors without external tooling.
- Status is alpha / vibe-engineered, not production-ready: expect API changes, rough edges, and non-idiomatic patterns (see `PACKAGE-MATURITY.md`).

## 2. [[wiki/02-orchestration-libraries|Orchestration Libraries]]
**In one sentence:** Talkio is a TypeScript, infrastructure-free, bring-your-own-model orchestration library that trades built-in providers and managed hosting for maximum flexibility, portability, and custom-provider extensibility versus LiveKit Agents, Pipecat, OpenAI Agents SDK, and managed platforms.
- Talkio is TypeScript-only with no infrastructure and BYO any LLM SDK, versus LiveKit Agents (Python/TypeScript, needs LiveKit Server + SSL + TURN + Redis), Pipecat (Python, needs transport layer), and OpenAI Agents SDK (TypeScript, OpenAI-only).
- Provider lock-in is none for Talkio, LiveKit ecosystem for LiveKit Agents, Daily.co ecosystem for Pipecat, and OpenAI models for OpenAI Agents SDK; custom providers are first-class in Talkio, plugin-based in LiveKit/Pipecat, and unavailable in OpenAI Agents SDK.
- Filler phrases use `ctx.say()` in the LLM in Talkio, `session.say()` in hooks in LiveKit Agents, manual handling in Pipecat, and unknown in OpenAI Agents SDK.
- Managed platforms (Vapi, Retell, Bland AI) charge per-minute fees and manage hosting/scaling/telephony with limited flexibility, while Talkio is free (Apache-2.0), self-deployed anywhere, and could power such a platform's backend.
- Talkio is runtime-, transport-, and platform-agnostic: runs on Bun, Node.js, Deno, and Edge (Cloudflare Workers, Vercel Edge); accepts WebSocket, WebRTC-via-external-library, or HTTP streaming audio; deploys to Cloudflare Workers, Vercel Edge, AWS Lambda, Google Cloud Functions, bare metal, or local dev.
- Design rationale is explicit: an `LLMFunction` interface instead of bundled clients (choice, control over streaming/tool calls, future-proof model swaps), XState for predictable async/parallel (STT, LLM, TTS) state with cancellation and devtools, and separate tree-shakeable provider packages (`talkio` core + `@talkio/deepgram`, both Available).
- Audio and events are fully specified: separate input/output formats (e.g. linear16 16kHz in / 24kHz out mono) across PCM, telephony (mulaw/alaw), compressed, and container encodings, plus lifecycle/human-turn/AI-turn events and `createCustomSTTProvider` / `createCustomLLMProvider` / `createCustomTTSProvider` extension points.

## 3. [[wiki/03-why-no-built-in-llm|Why no built-in LLM]]
**In one sentence:** Talkio ships an `LLMFunction` interface instead of bundling LLM clients — plus XState actors for concurrency, tree-shakeable provider packages, and custom-provider factories — so you keep full control of streaming, tool calls, and model choice while the library owns orchestration only.
- Talkio provides an `LLMFunction` interface instead of bundling LLM clients, giving choice of SDK (Vercel AI SDK, OpenAI SDK, Anthropic SDK, any other client), full control of streaming/tool calls/model-specific features, and future-proof model swaps without changing orchestration code.
- XState is chosen because voice AI has inherently complex concurrent state: predictable async state management, built-in parallel states (STT, LLM, TTS running simultaneously), clean cancellation patterns, and devtools for debugging complex state flows.
- Providers are separate tree-shakeable packages so you only bundle what you use (`talkio` core plus `@talkio/deepgram`); more provider packages are coming soon.
- The `LLMFunction` context exposes `ctx.token`, `ctx.sentence`, `ctx.complete`, `ctx.say` (filler phrases), `ctx.interrupt`, `ctx.isSpeaking`, `ctx.messages`, and `ctx.signal` (AbortSignal).
- Custom providers are built with `createCustomSTTProvider`, `createCustomLLMProvider`, and `createCustomTTSProvider` factories for self-hosted models or unsupported services.
- The worked streaming example wires Deepgram `nova-3` STT and `aura-2-thalia-en` TTS with a `gpt-4o-mini` LLM via Vercel AI SDK `streamText`, splitting the text stream into sentences with a `/^(.*?[.!?])\s+(.*)$/s` regex.

## The argument in five moves
1. The repo snapshot grounds what Talkio is: a 39-commit, 2-star alpha on `main` — a vibe-engineered, TypeScript-first voice-AI orchestration library that is provider, transport, and infrastructure agnostic.
2. Voice AI is deceptively complex because interruptions, turn-taking, latency, cancellation, and race conditions must be coordinated across async audio, STT, LLM, and TTS streams, and existing approaches trade this away via infrastructure lock-in (LiveKit), transport lock-in (Pipecat), model lock-in (OpenAI Agents SDK), or per-minute managed-platform costs.
3. Talkio answers with pure orchestration: six parallel XState actors (STT, VAD, Turn Detector, LLM, TTS, Audio Streamer) under idle → running → stopped, with dual-path (VAD-fast plus STT-fallback) interruption detection, AbortSignal cancellation, timeouts, sentence-level streaming TTS, backpressure-aware audio buffering, filler phrases via `ctx.say()`, and built-in latency/turn/error metrics.
4. Against orchestration libraries and managed platforms, Talkio trades built-in providers and managed hosting for maximum flexibility and portability: TypeScript-only, no infrastructure, BYO any LLM SDK, first-class custom providers, and runtime/transport/platform agnosticism from Edge workers to bare metal.
5. That trade is made concrete by the design philosophy: an `LLMFunction` interface instead of bundled clients for choice, control, and future-proof swaps; XState for predictable concurrent state and cancellation; and separate tree-shakeable provider packages plus `createCustomSTT/LLM/TTSProvider` factories.
6. The contract closes the loop for builders: you bring STT/LLM/TTS, Talkio owns turn-taking, interruptions, cancellation, and streaming coordination, and you consume a fully specified event stream (lifecycle, human-turn, AI-turn) with explicit audio formats and extension points such as Deepgram nova-3/aura-2 plus a gpt-4o-mini streaming example.
