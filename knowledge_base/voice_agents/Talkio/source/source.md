# Talkio
Source: https://github.com/abdufelsayed/talkio
Kind: article
Fetched: 2026-09-22T13:55:21.992198+00:00
Tool: raw-github

# Talkio

Pronounced "TAWK-yo" - like "Tokyo", but starting with "talk".

> **⚠️ Vibe-Engineered** — This package is **not production-ready**. Suitable for prototyping and experimentation. Expect API changes, rough edges, and non-idiomatic patterns. See the [Package Maturity Model](./PACKAGE-MATURITY.md) for details.

> **Alpha Release** — Under active development.

[![npm version](https://img.shields.io/npm/v/talkio.svg)](https://www.npmjs.com/package/talkio)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)

**Voice AI orchestration for TypeScript** — pure orchestration, zero infrastructure lock-in.

Talkio is a voice agent orchestration library that coordinates STT, LLM, and TTS components with automatic turn management, interruption detection, and real-time streaming. It's designed to be the engine powering your voice AI applications, regardless of where the voice comes from or where you deploy.

- **TypeScript-first** — Built for the JavaScript ecosystem, runs anywhere JS runs
- **Voice source agnostic** — Works with phone, web, mobile, microphone, WebRTC
- **Provider agnostic** — BYO any STT/TTS/LLM, or create custom providers for self-hosted models
- **Zero infrastructure** — Pure library, no servers or infrastructure required
- **Filler phrases** — `ctx.say()` for real-time updates during complex workflows (tool calls, reasoning)

## At a Glance

- You bring: STT, LLM, and TTS providers (or custom implementations)
- Talkio handles: turn-taking, interruptions, cancellation, and streaming coordination
- You consume: an event stream (transcripts, tokens/sentences, and audio)

## Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Why Talkio?](#why-talkio)
- [Architecture](#architecture)
- [Why Actors & State Machines?](#why-actors--state-machines)
- [Handling the Hard Cases](#handling-the-hard-cases)
- [Unique Features](#unique-features)
- [Comparison with Alternatives](#comparison-with-alternatives)
- [Deployment](#deployment)
- [Design Philosophy](#design-philosophy)
- [Streaming LLM Example](#streaming-llm-example)
- [Events](#events)
- [Packages](#packages)
- [Audio Configuration](#audio-configuration)
- [Creating Custom Providers](#creating-custom-providers)
- [Examples](#examples)
- [License](#license)

## Installation

```bash
npm install talkio
```

For provider packages:

```bash
npm install @talkio/deepgram
```

## Quick Start

This is the smallest useful setup: wire providers, listen to events, and stream audio in.

```typescript
import { createAgent } from "talkio";

const agent = createAgent({
  stt: mySTT,
  llm: myLLM,
  tts: myTTS,
  onEvent: (event) => {
    switch (event.type) {
      case "human-turn:ended":
        console.log("User:", event.transcript);
        break;
      case "ai-turn:audio":
        // Pipe to speakers / WebRTC / telephony, etc.
        playAudio(event.audio);
        break;
    }
  },
});

agent.start();
agent.sendAudio(audioChunk); // stream audio chunks as they arrive
// agent.stop();
```

For a complete runnable setup (WebSocket server + browser mic), see `examples/simple`.

## Why Talkio?

Building voice AI agents is deceptively complex. You need to coordinate multiple async streams — audio input, speech recognition, language model generation, speech synthesis, audio output — all while handling brittle edge cases:

- **Interruptions**: User speaks while agent is responding
- **Turn-taking**: Detecting when the user is done speaking vs. pausing to think
- **Latency**: Minimizing time-to-first-audio without sacrificing quality
- **Cancellation**: Cleaning up in-flight operations when context changes
- **Race conditions**: Multiple components generating events simultaneously

Existing solutions come with trade-offs:

| Approach              | Trade-off                                                 |
| --------------------- | --------------------------------------------------------- |
| **LiveKit Agents**    | Requires LiveKit Server infrastructure (SSL, TURN, Redis) |
| **Pipecat**           | Python-only, tied to Daily.co transport layer             |
| **OpenAI Agents SDK** | Locked to OpenAI Realtime API                             |
| **Managed platforms** | Per-minute costs, less flexibility                        |

**Talkio takes a different approach**: pure orchestration that runs anywhere JavaScript runs, with no opinions on infrastructure, transport, or providers. Use it as the engine for any voice agent implementation.

## Architecture

Talkio uses a state machine architecture built on [XState](https://xstate.js.org/) with parallel actors:

```
Audio In → [STT Actor] → [Turn Detector] → [LLM Actor] → [TTS Actor] → Audio Out
                ↑                                ↓
           [VAD Actor] ←────── Interruption ──────→ [Audio Streamer]
```

**Six specialized actors** run in parallel with event-based communication:

| Actor              | Responsibility                                         |
| ------------------ | ------------------------------------------------------ |
| **STT Actor**      | Speech-to-text transcription                           |
| **VAD Actor**      | Voice activity detection (optional, falls back to STT) |
| **Turn Detector**  | Semantic turn boundary detection (optional)            |
| **LLM Actor**      | Response generation with filler phrase support         |
| **TTS Actor**      | Text-to-speech synthesis (sentence-level streaming)    |
| **Audio Streamer** | Output audio buffering with backpressure handling      |

**Hierarchical state machine**:

```
idle → running → stopped
         ├── listening (idle ↔ userSpeaking)
         ├── transcribing
         ├── responding
         └── streaming (silent ↔ streaming)
```

## Why Actors & State Machines?

Voice AI involves complex concurrent operations that must coordinate precisely. Traditional async/await patterns quickly become unmanageable with multiple parallel streams, cancellation requirements, and edge cases.

**XState actors provide**:

- **Isolated state per component** — No shared mutable state between STT, LLM, TTS
- **Event-driven communication** — Clean boundaries, explicit message passing
- **Automatic cleanup** — AbortSignal propagation for graceful cancellation
- **Visual debugging** — [XState Inspector](https://stately.ai/docs/inspector) for real-time state visualization

**Practical benefits**:

- Predictable behavior under complex scenarios (interruptions, errors, timeouts)
- Easy to add custom providers — just implement the interface
- Testable transitions — state changes are explicit and observable

## Handling the Hard Cases

### Interruption Detection

Dual-path detection ensures responsive interruptions:

- **VAD-based** (fast, ~100ms) — Dedicated voice activity detection
- **STT-based** (fallback) — Uses STT's built-in speech detection

```typescript
createAgent({
  stt,
  llm,
  tts,
  interruption: {
    enabled: true,
    minDurationMs: 200, // Ignore sounds shorter than 200ms
  },
});
```

### Cancellation

AbortSignal flows through all actors. When the user interrupts:

1. Current LLM generation is cancelled
2. Pending TTS synthesis is aborted
3. Audio queue is cleared
4. Resources are cleaned up

### Timeouts

Configurable timeouts prevent hanging:

- **LLM**: 30s default
- **TTS**: 10s default

### Queue Management

Sentence-level TTS with backpressure detection:

- TTS starts on first complete sentence, not full response
- Audio streamer detects slow consumers and prevents buffer overrun
- Graceful degradation under load

## Unique Features

### Filler Phrases

Keep users engaged during complex workflows. When your agent is calling multiple tools, waiting for slow reasoning models, or processing multi-step tasks, fillers provide real-time updates instead of silence.

The `ctx.say()` API lets you speak contextual updates based on what's happening. Here's a realistic example using [Vercel AI SDK](https://ai-sdk.dev)'s `fullStream` to announce tool calls:

```typescript
import { streamText } from "ai";
import { openai } from "@ai-sdk/openai";

const llm: LLMFunction = async (ctx) => {
  const result = streamText({
    model: openai("gpt-4o"),
    messages: ctx.messages,
    tools: {
      getWeather: {
        /* ... */
      },
      searchFlights: {
        /* ... */
      },
      bookFlight: {
        /* ... */
      },
    },
    abortSignal: ctx.signal,
  });

  let fullText = "";
  let buffer = "";
  let sentenceIndex = 0;

  for await (const event of result.fullStream) {
    switch (event.type) {
      case "tool-call":
        // Contextual filler based on which tool is being called
        if (event.toolName === "getWeather") {
          ctx.say(`Checking the weather in ${event.args.location}...`);
        } else if (event.toolName === "searchFlights") {
          ctx.say("Looking up available flights for you...");
        } else if (event.toolName === "bookFlight") {
          ctx.say("Completing your booking now...");
        }
        break;

      case "text-delta":
        ctx.token(event.textDelta);
        fullText += event.textDelta;
        buffer += event.textDelta;

        const match = buffer.match(/^(.*?[.!?])\s+(.*)$/s);
        if (match) {
          ctx.sentence(match[1], sentenceIndex++);
          buffer = match[2];
        }
        break;
    }
  }

  if (buffer.trim()) ctx.sentence(buffer.trim(), sentenceIndex);
  ctx.complete(fullText);
};
```

The user hears natural progress updates like _"Checking the weather in Tokyo..."_ followed by _"Looking up available flights..."_ instead of silence during tool execution.

**Comparison**: LiveKit supports fillers via `session.say()` in hooks like `on_user_turn_completed`. Talkio provides `ctx.say()` directly in the LLM context — same capability, different ergonomics.

### Sentence-Level Streaming

TTS synthesis begins on the first complete sentence, not the full LLM response. This dramatically reduces time-to-first-audio.

### Built-in Metrics

Comprehensive observability without external tooling:

```typescript
const state = agent.getSnapshot();

// Latency metrics
state.metrics.latency.averageTimeToFirstToken; // LLM latency
state.metrics.latency.averageTimeToFirstAudio; // End-to-end latency
state.metrics.latency.averageTurnDuration;

// Turn tracking
state.metrics.turns.total;
state.metrics.turns.completed;
state.metrics.turns.interrupted;

// Error tracking by source
state.metrics.errors.bySource; // { stt: 0, llm: 1, tts: 0 }
```

## Comparison with Alternatives

### Orchestration Libraries

| Feature              | Talkio             | LiveKit Agents                      | Pipecat             | OpenAI Agents SDK |
| -------------------- | ------------------ | ----------------------------------- | ------------------- | ----------------- |
| **Language**         | TypeScript         | Python/TypeScript                   | Python              | TypeScript        |
| **Infrastructure**   | None               | LiveKit Server + SSL + TURN + Redis | Transport layer     | None              |
| **LLM Integration**  | BYO any SDK        | Built-in                            | Built-in plugins    | OpenAI only       |
| **Provider Lock-in** | None               | LiveKit ecosystem                   | Daily.co ecosystem  | OpenAI models     |
| **Custom Providers** | First-class        | Plugins                             | Plugins             | No                |
| **Filler Phrases**   | `ctx.say()` in LLM | `session.say()` in hooks            | Manual              | Unknown           |
| **Voice Source**     | Agnostic           | WebRTC rooms                        | Transport-dependent | Agnostic          |

**When to use each**:

- **Talkio**: TypeScript projects, maximum flexibility, no infrastructure
- **LiveKit Agents**: Already using LiveKit, need WebRTC rooms
- **Pipecat**: Python projects, need 40+ provider integrations
- **OpenAI Agents SDK**: Using OpenAI Realtime API, want guardrails/handoffs

### Managed Platforms

Talkio is not a managed platform — it's a library. Managed platforms like Vapi, Retell, and Bland AI handle everything (hosting, scaling, telephony) but with per-minute costs and less flexibility. Talkio could power the backend of such platforms.

| Aspect             | Talkio            | Managed Platforms |
| ------------------ | ----------------- | ----------------- |
| **Pricing**        | Free (Apache-2.0) | Per-minute fees   |
| **Infrastructure** | You manage        | They manage       |
| **Flexibility**    | Maximum           | Limited           |
| **Deployment**     | Anywhere          | Their cloud       |

## Deployment

Talkio is a pure library — no infrastructure requirements.

### Runtime Agnostic

```typescript
// Bun
Bun.serve({
  /* ... */
});

// Node.js
import { createServer } from "http";

// Deno
Deno.serve({
  /* ... */
});

// Edge (Cloudflare Workers, Vercel Edge, etc.)
export default {
  fetch(req) {
    /* ... */
  },
};
```

### Transport Agnostic

```typescript
// WebSocket
ws.on("message", (data) => agent.sendAudio(data));

// WebRTC (via external library)
peerConnection.ontrack = (e) => {
  /* pipe to agent */
};

// HTTP streaming
const reader = request.body.getReader();
```

### Platform Agnostic

Deploy anywhere JavaScript runs:

- Cloudflare Workers
- Vercel Edge Functions
- AWS Lambda
- Google Cloud Functions
- Bare metal servers
- Local development

## Design Philosophy

### Why No Built-in LLM?

Talkio provides an `LLMFunction` interface instead of bundling LLM clients. This gives you:

- **Choice**: Use Vercel AI SDK, OpenAI SDK, Anthropic SDK, or any other client
- **Control**: Full access to streaming, tool calls, and model-specific features
- **Future-proof**: Swap models without changing orchestration code

```typescript
// With Vercel AI SDK
import { streamText } from "ai";
import { openai } from "@ai-sdk/openai";

const llm: LLMFunction = async (ctx) => {
  const result = streamText({
    model: openai("gpt-4o"),
    messages: ctx.messages,
    abortSignal: ctx.signal,
  });
  // ... handle streaming
};

// With Anthropic SDK
import Anthropic from "@anthropic-ai/sdk";

const llm: LLMFunction = async (ctx) => {
  const stream = await anthropic.messages.stream({
    model: "claude-sonnet-4-20250514",
    messages: ctx.messages,
  });
  // ... handle streaming
};
```

### Why XState?

Voice AI has inherently complex state. XState provides:

- Predictable async state management
- Built-in support for parallel states (STT, LLM, TTS running simultaneously)
- Clean cancellation patterns
- Devtools for debugging complex state flows

### Why Separate Provider Packages?

Providers are tree-shakeable. Only bundle what you use:

```bash
npm install talkio           # Core orchestration
npm install @talkio/deepgram       # Deepgram STT/TTS
# More providers coming...
```

## Streaming LLM Example

```typescript
import { createAgent, LLMFunction } from "talkio";
import { createDeepgram } from "@talkio/deepgram";
import { streamText } from "ai";
import { openai } from "@ai-sdk/openai";

const deepgram = createDeepgram({ apiKey: process.env.DEEPGRAM_API_KEY });

const llm: LLMFunction = async (ctx) => {
  // Optional: speak while thinking
  ctx.say("Let me check on that...");

  const result = streamText({
    model: openai("gpt-4o-mini"),
    messages: ctx.messages,
    abortSignal: ctx.signal,
  });

  let fullText = "";
  let buffer = "";
  let sentenceIndex = 0;
  for await (const chunk of result.textStream) {
    ctx.token(chunk);
    fullText += chunk;
    buffer += chunk;

    const match = buffer.match(/^(.*?[.!?])\s+(.*)$/s);
    if (match) {
      ctx.sentence(match[1], sentenceIndex++);
      buffer = match[2];
    }
  }

  if (buffer.trim()) ctx.sentence(buffer.trim(), sentenceIndex);
  ctx.complete(fullText);
};

const agent = createAgent({
  stt: deepgram.stt({ model: "nova-3" }),
  llm,
  tts: deepgram.tts({ model: "aura-2-thalia-en" }),
  onEvent: (event) => {
    switch (event.type) {
      case "human-turn:ended":
        console.log("User:", event.transcript);
        break;
      case "ai-turn:audio":
        playAudio(event.audio);
        break;
    }
  },
});

agent.start();
agent.sendAudio(audioChunk); // Float32Array from microphone
agent.stop();
```

## Events

```typescript
// Lifecycle
"agent:started";
"agent:stopped";
"agent:error"; // { error, source: "stt" | "llm" | "tts" }

// Human turn
"human-turn:started";
"human-turn:transcript"; // { text, isFinal }
"human-turn:ended"; // { transcript }

// AI turn
"ai-turn:started";
"ai-turn:token"; // { token }
"ai-turn:sentence"; // { sentence, index }
"ai-turn:audio"; // { audio: ArrayBuffer }
"ai-turn:ended"; // { text, wasSpoken }
"ai-turn:interrupted"; // { partialText }
```

## Packages

| Package            | Description                | Status    |
| ------------------ | -------------------------- | --------- |
| `talkio`           | Core orchestration library | Available |
| `@talkio/deepgram` | Deepgram STT/TTS providers | Available |

More provider packages coming soon.

See [Package Maturity Model](./PACKAGE-MATURITY.md) for information about package maturity levels and current status.

## Audio Configuration

Configure separate input/output formats, or use provider defaults:

```typescript
const agent = createAgent({
  stt: mySTT,
  llm: myLLM,
  tts: myTTS,
  // Optional: specify audio formats (uses provider defaults if omitted)
  audio: {
    input: { encoding: "linear16", sampleRate: 16000, channels: 1 },
    output: { encoding: "linear16", sampleRate: 24000, channels: 1 },
  },
});
```

### Supported Encodings

| Category   | Encodings                                |
| ---------- | ---------------------------------------- |
| PCM        | `linear16`, `linear32`, `float32`        |
| Telephony  | `mulaw`, `alaw`                          |
| Compressed | `opus`, `ogg-opus`, `flac`, `mp3`, `aac` |
| Container  | `wav`, `webm`, `ogg`, `mp4`              |

## Creating Custom Providers

Create providers for self-hosted models or services not yet supported:

```typescript
import { createCustomSTTProvider, createCustomLLMProvider, createCustomTTSProvider } from "talkio";

// Custom STT provider
const sttFormats = [{ encoding: "linear16", sampleRate: 16000, channels: 1 }] as const;

const stt = createCustomSTTProvider({
  name: "MySTT",
  supportedInputFormats: sttFormats,
  defaultInputFormat: sttFormats[0],
  start: (ctx) => {
    // ctx.audioFormat - the selected input format
    // ctx.transcript(text, isFinal)
    // ctx.speechStart(), ctx.speechEnd()
    // ctx.signal - AbortSignal for cancellation
  },
  stop: () => {},
  sendAudio: (audio) => {},
});

// Custom LLM provider
const llm = createCustomLLMProvider({
  name: "MyLLM",
  generate: async (messages, ctx) => {
    // ctx.token(text) - stream tokens
    // ctx.sentence(text, index) - complete sentences for TTS
    // ctx.complete(fullText) - signal completion
    // ctx.say(text) - filler phrases
    // ctx.interrupt() - stop filler
    // ctx.isSpeaking() - check if agent is speaking
    // ctx.signal - AbortSignal
  },
});

// Custom TTS provider
const ttsFormats = [{ encoding: "linear16", sampleRate: 24000, channels: 1 }] as const;

const tts = createCustomTTSProvider({
  name: "MyTTS",
  supportedOutputFormats: ttsFormats,
  defaultOutputFormat: ttsFormats[0],
  synthesize: async (text, ctx) => {
    // ctx.audioFormat - the selected output format
    // ctx.audioChunk(buffer) - stream audio chunks
    // ctx.complete() - signal completion
    // ctx.signal - AbortSignal
  },
});
```

## Examples

See the [`/examples`](./examples) directory for complete working examples:

- [`simple`](./examples/simple) — WebSocket server with Deepgram and OpenAI

## License

Apache-2.0
