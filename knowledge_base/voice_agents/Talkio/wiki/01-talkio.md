> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Talkio
**In one sentence:** Talkio ("TAWK-yo") is a TypeScript-first, provider- and infrastructure-agnostic voice-AI orchestration library that coordinates BYO STT/LLM/TTS with turn-taking, dual-path interruption detection, AbortSignal cancellation, and sentence-level streaming TTS.
## Key points
- Pure orchestration with zero infrastructure lock-in: runs anywhere JavaScript runs, no servers required, voice-source agnostic (phone, web, mobile, microphone, WebRTC).
- Provider agnostic: you bring STT, LLM, and TTS providers or custom implementations; Talkio handles turn-taking, interruptions, cancellation, and streaming coordination, and you consume an event stream (transcripts, tokens/sentences, audio).
- Architecture is six parallel XState actors (STT, VAD, Turn Detector, LLM, TTS, Audio Streamer) with hierarchical states `idle → running → stopped` containing `listening`, `transcribing`, `responding`, and `streaming`.
- Interruption uses dual-path detection — fast VAD-based (~100ms) with STT-based fallback — plus `minDurationMs: 200` filtering, and on interrupt cancels LLM generation, aborts pending TTS, clears the audio queue, and cleans up resources via AbortSignal propagation.
- Latency strategy is sentence-level streaming (TTS starts on first complete sentence, not full response) with backpressure-aware audio buffering, plus default timeouts of 30s for LLM and 10s for TTS.
- Filler phrases via `ctx.say()` speak contextual progress updates during tool calls/slow reasoning (e.g. "Checking the weather in Tokyo..."), and built-in metrics expose time-to-first-token, time-to-first-audio, turn counts, and per-source errors without external tooling.
- Status is alpha / vibe-engineered, not production-ready: expect API changes, rough edges, and non-idiomatic patterns (see `PACKAGE-MATURITY.md`).
---
## At a Glance
- You bring: STT, LLM, and TTS providers (or custom implementations)
- Talkio handles: turn-taking, interruptions, cancellation, and streaming coordination
- You consume: an event stream (transcripts, tokens/sentences, and audio)

## Installation
```bash
npm install talkio
```
For provider packages:
```bash
npm install @talkio/deepgram
```

## Quick Start
Smallest useful setup — wire providers, listen to events, stream audio in:
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
Verbatim problem statement:

> "Building voice AI agents is deceptively complex. You need to coordinate multiple async streams — audio input, speech recognition, language model generation, speech synthesis, audio output — all while handling brittle edge cases:"

Hard cases listed:
- **Interruptions**: User speaks while agent is responding
- **Turn-taking**: Detecting when the user is done speaking vs. pausing to think
- **Latency**: Minimizing time-to-first-audio without sacrificing quality
- **Cancellation**: Cleaning up in-flight operations when context changes
- **Race conditions**: Multiple components generating events simultaneously

Trade-offs of existing approaches (verbatim table):

| Approach              | Trade-off                                                 |
| --------------------- | --------------------------------------------------------- |
| **LiveKit Agents**    | Requires LiveKit Server infrastructure (SSL, TURN, Redis) |
| **Pipecat**           | Python-only, tied to Daily.co transport layer             |
| **OpenAI Agents SDK** | Locked to OpenAI Realtime API                             |
| **Managed platforms** | Per-minute costs, less flexibility                        |

Verbatim positioning:

> "**Talkio takes a different approach**: pure orchestration that runs anywhere JavaScript runs, with no opinions on infrastructure, transport, or providers. Use it as the engine for any voice agent implementation."

## Architecture
Built on [XState](https://xstate.js.org/) with parallel actors:
```
Audio In → [STT Actor] → [Turn Detector] → [LLM Actor] → [TTS Actor] → Audio Out
                ↑                                ↓
           [VAD Actor] ←────── Interruption ──────→ [Audio Streamer]
```

Six specialized actors (verbatim table):

| Actor              | Responsibility                                         |
| ------------------ | ------------------------------------------------------ |
| **STT Actor**      | Speech-to-text transcription                           |
| **VAD Actor**      | Voice activity detection (optional, falls back to STT) |
| **Turn Detector**  | Semantic turn boundary detection (optional)            |
| **LLM Actor**      | Response generation with filler phrase support         |
| **TTS Actor**      | Text-to-speech synthesis (sentence-level streaming)    |
| **Audio Streamer** | Output audio buffering with backpressure handling      |

Hierarchical state machine:
```
idle → running → stopped
         ├── listening (idle ↔ userSpeaking)
         ├── transcribing
         ├── responding
         └── streaming (silent ↔ streaming)
```

## Why Actors & State Machines?
Verbatim rationale:

> "Voice AI involves complex concurrent operations that must coordinate precisely. Traditional async/await patterns quickly become unmanageable with multiple parallel streams, cancellation requirements, and edge cases."

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
Verbatim: "Keep users engaged during complex workflows. When your agent is calling multiple tools, waiting for slow reasoning models, or processing multi-step tasks, fillers provide real-time updates instead of silence."

The `ctx.say()` API with Vercel AI SDK `fullStream` announces tool calls (e.g. `getWeather` → `ctx.say("Checking the weather in ...")`, `searchFlights` → `"Looking up available flights for you..."`, `bookFlight` → `"Completing your booking now..."`); the user hears e.g. *"Checking the weather in Tokyo..."* followed by *"Looking up available flights..."* instead of silence.

Verbatim comparison: "LiveKit supports fillers via `session.say()` in hooks like `on_user_turn_completed`. Talkio provides `ctx.say()` directly in the LLM context — same capability, different ergonomics."

TypeScript traits used for streaming: `ctx.token(event.textDelta)`, sentence split via `/^(.*?[.!?])\s+(.*)$/s` with `ctx.sentence(...)`, then `ctx.complete(fullText)`.

### Sentence-Level Streaming
Verbatim: "TTS synthesis begins on the first complete sentence, not the full LLM response. This dramatically reduces time-to-first-audio."

### Built-in Metrics
Verbatim: "Comprehensive observability without external tooling:"
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
Chunk ends at the `## Comparison with Alternatives` heading with no body content in this chunk; comparison rows beyond the Why-Talkio trade-off table are not present here.

**Covers:** Covers Talkio overview: voice-AI orchestration, architecture, and core features.
