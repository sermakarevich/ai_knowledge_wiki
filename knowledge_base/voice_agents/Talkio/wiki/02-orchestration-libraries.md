[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Orchestration Libraries
**In one sentence:** Talkio is a TypeScript, infrastructure-free, bring-your-own-model orchestration library that trades built-in providers and managed hosting for maximum flexibility, portability, and custom-provider extensibility versus LiveKit Agents, Pipecat, OpenAI Agents SDK, and managed platforms.
## Key points
- Talkio is TypeScript-only with no infrastructure and BYO any LLM SDK, versus LiveKit Agents (Python/TypeScript, needs LiveKit Server + SSL + TURN + Redis), Pipecat (Python, needs transport layer), and OpenAI Agents SDK (TypeScript, OpenAI-only).
- Provider lock-in is none for Talkio, LiveKit ecosystem for LiveKit Agents, Daily.co ecosystem for Pipecat, and OpenAI models for OpenAI Agents SDK; custom providers are first-class in Talkio, plugin-based in LiveKit/Pipecat, and unavailable in OpenAI Agents SDK.
- Filler phrases use `ctx.say()` in the LLM in Talkio, `session.say()` in hooks in LiveKit Agents, manual handling in Pipecat, and unknown in OpenAI Agents SDK.
- Managed platforms (Vapi, Retell, Bland AI) charge per-minute fees and manage hosting/scaling/telephony with limited flexibility, while Talkio is free (Apache-2.0), self-deployed anywhere, and could power such a platform's backend.
- Talkio is runtime-, transport-, and platform-agnostic: runs on Bun, Node.js, Deno, and Edge (Cloudflare Workers, Vercel Edge); accepts WebSocket, WebRTC-via-external-library, or HTTP streaming audio; deploys to Cloudflare Workers, Vercel Edge, AWS Lambda, Google Cloud Functions, bare metal, or local dev.
- Design rationale is explicit: an `LLMFunction` interface instead of bundled clients (choice, control over streaming/tool calls, future-proof model swaps), XState for predictable async/parallel (STT, LLM, TTS) state with cancellation and devtools, and separate tree-shakeable provider packages (`talkio` core + `@talkio/deepgram`, both Available).
- Audio and events are fully specified: separate input/output formats (e.g. linear16 16kHz in / 24kHz out mono) across PCM, telephony (mulaw/alaw), compressed, and container encodings, plus lifecycle/human-turn/AI-turn events and `createCustomSTTProvider` / `createCustomLLMProvider` / `createCustomTTSProvider` extension points.
---
## Orchestration Libraries
**Covers:** comparison of orchestration libraries and when to use each.

| Feature | Talkio | LiveKit Agents | Pipecat | OpenAI Agents SDK |
| -------------------- | ------------------ | ----------------------------------- | ------------------- | ----------------- |
| **Language** | TypeScript | Python/TypeScript | Python | TypeScript |
| **Infrastructure** | None | LiveKit Server + SSL + TURN + Redis | Transport layer | None |
| **LLM Integration** | BYO any SDK | Built-in | Built-in plugins | OpenAI only |
| **Provider Lock-in** | None | LiveKit ecosystem | Daily.co ecosystem | OpenAI models |
| **Custom Providers** | First-class | Plugins | Plugins | No |
| **Filler Phrases** | `ctx.say()` in LLM | `session.say()` in hooks | Manual | Unknown |
| **Voice Source** | Agnostic | WebRTC rooms | Transport-dependent | Agnostic |

**When to use each**:
- **Talkio**: TypeScript projects, maximum flexibility, no infrastructure
- **LiveKit Agents**: Already using LiveKit, need WebRTC rooms
- **Pipecat**: Python projects, need 40+ provider integrations
- **OpenAI Agents SDK**: Using OpenAI Realtime API, want guardrails/handoffs

## Managed Platforms
Talkio is not a managed platform — it's a library. Managed platforms like Vapi, Retell, and Bland AI handle everything (hosting, scaling, telephony) but with per-minute costs and less flexibility. Talkio could power the backend of such platforms.

| Aspect | Talkio | Managed Platforms |
| ------------------ | ----------------- | ----------------- |
| **Pricing** | Free (Apache-2.0) | Per-minute fees |
| **Infrastructure** | You manage | They manage |
| **Flexibility** | Maximum | Limited |
| **Deployment** | Anywhere | Their cloud |

## Deployment
Talkio is a pure library — no infrastructure requirements.

### Runtime Agnostic
```typescript
// Bun
Bun.serve({ /* ... */ });

// Node.js
import { createServer } from "http";

// Deno
Deno.serve({ /* ... */ });

// Edge (Cloudflare Workers, Vercel Edge, etc.)
export default {
  fetch(req) { /* ... */ },
};
```

### Transport Agnostic
```typescript
// WebSocket
ws.on("message", (data) => agent.sendAudio(data));

// WebRTC (via external library)
peerConnection.ontrack = (e) => { /* pipe to agent */ };

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
| Package | Description | Status |
| ------------------ | -------------------------- | --------- |
| `talkio` | Core orchestration library | Available |
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
| Category | Encodings |
| ---------- | ---------------------------------------- |
| PCM | `linear16`, `linear32`, `float32` |
| Telephony | `mulaw`, `alaw` |
| Compressed | `opus`, `ogg-opus`, `flac`, `mp3`, `aac` |
| Container | `wav`, `webm`, `ogg`, `mp4` |

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
