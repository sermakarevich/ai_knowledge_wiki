> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Why no built-in LLM
**In one sentence:** Talkio ships an `LLMFunction` interface instead of bundling LLM clients — plus XState actors for concurrency, tree-shakeable provider packages, and custom-provider factories — so you keep full control of streaming, tool calls, and model choice while the library owns orchestration only.
## Key points
- Talkio provides an `LLMFunction` interface instead of bundling LLM clients, giving choice of SDK (Vercel AI SDK, OpenAI SDK, Anthropic SDK, any other client), full control of streaming/tool calls/model-specific features, and future-proof model swaps without changing orchestration code.
- XState is chosen because voice AI has inherently complex concurrent state: predictable async state management, built-in parallel states (STT, LLM, TTS running simultaneously), clean cancellation patterns, and devtools for debugging complex state flows.
- Providers are separate tree-shakeable packages so you only bundle what you use (`talkio` core plus `@talkio/deepgram`); more provider packages are coming soon.
- The `LLMFunction` context exposes `ctx.token`, `ctx.sentence`, `ctx.complete`, `ctx.say` (filler phrases), `ctx.interrupt`, `ctx.isSpeaking`, `ctx.messages`, and `ctx.signal` (AbortSignal).
- Custom providers are built with `createCustomSTTProvider`, `createCustomLLMProvider`, and `createCustomTTSProvider` factories for self-hosted models or unsupported services.
- The worked streaming example wires Deepgram `nova-3` STT and `aura-2-thalia-en` TTS with a `gpt-4o-mini` LLM via Vercel AI SDK `streamText`, splitting the text stream into sentences with a `/^(.*?[.!?])\s+(.*)$/s` regex.
---
## Why no built-in LLM?
Per README, Talkio provides an `LLMFunction` interface instead of bundling LLM clients:

> "Choice: Use Vercel AI SDK, OpenAI SDK, Anthropic SDK, or any other client"
> "Control: Full access to streaming, tool calls, and model-specific features"
> "Future-proof: Swap models without changing orchestration code"

Vercel AI SDK example:

> 'constllm: LLMFunction=async(ctx)=>{constresult=streamText({model: openai("gpt-4o"),messages: ctx.messages,abortSignal: ctx.signal,});}'

Anthropic SDK example:

> 'constllm: LLMFunction=async(ctx)=>{conststream=awaitanthropic.messages.stream({model: "claude-sonnet-4-20250514",messages: ctx.messages,});}'

## Why XState?
Per README, voice AI has inherently complex state and XState provides:

> "Predictable async state management"
> "Built-in support for parallel states (STT, LLM, TTS running simultaneously)"
> "Clean cancellation patterns"
> "Devtools for debugging complex state flows"

Practical benefits quoted: "Predictable behavior under complex scenarios (interruptions, errors, timeouts). Easy to add custom providers — just implement the interface. Testable transitions — state changes are explicit and observable."

## Why separate provider packages?
Per README: "Providers are tree-shakeable. Only bundle what you use." Install lines:

> "npm install talkio           # Core orchestration"
> 'npm install @talkio/deepgram       # Deepgram STT/TTS # More providers coming...'

## Streaming LLM example
Full worked example from the README: Deepgram STT (`nova-3`) and TTS (`aura-2-thalia-en`) with a `gpt-4o-mini` LLM through Vercel AI SDK `streamText`, including an optional thinking filler `ctx.say("Let me check on that...")`, per-chunk `ctx.token(chunk)`, sentence splitting via the `/^(.*?[.!?])\s+(.*)$/s` regex with `ctx.sentence(match[1],sentenceIndex++)`, remainder flush with `ctx.sentence(buffer.trim(),sentenceIndex)`, and `ctx.complete(fullText)` at the end. Audio in is a `Float32Array` from the microphone via `agent.sendAudio(audioChunk)`; audio out arrives on the `ai-turn:audio` event.

The filler-phrase tool-call variant announces each tool as it fires — `ctx.say("Checking the weather in ...")` on `tool-call` for `getWeather`, "Looking up available flights for you..." for `searchFlights`, "Completing your booking now..." for `bookFlight` — while `text-delta` events feed the same token/sentence/complete pipeline.

## LLM context API
The `ctx` object available inside an `LLMFunction`, as documented by the custom-provider signatures:

> "ctx.token(text) - stream tokens"
> "ctx.sentence(text, index) - complete sentences for TTS"
> "ctx.complete(fullText) - signal completion"
> "ctx.say(text) - filler phrases"
> "ctx.interrupt() - stop filler"
> "ctx.isSpeaking() - check if agent is speaking"
> "ctx.signal - AbortSignal"

## Creating custom providers
Factories for self-hosted models or services not yet supported:

> "import{createCustomSTTProvider,createCustomLLMProvider,createCustomTTSProvider}from\"talkio\""

Custom STT shape: `createCustomSTTProvider({name, supportedInputFormats, defaultInputFormat, start: (ctx)=>{...}, stop: ()=>{}, sendAudio: (audio)=>{}})` where the start context exposes `ctx.audioFormat`, `ctx.transcript(text, isFinal)`, `ctx.speechStart()`, `ctx.speechEnd()`, and `ctx.signal`.

Custom LLM shape: `createCustomLLMProvider({name, generate: async(messages,ctx)=>{...}})` with the token/sentence/complete/say/interrupt/isSpeaking/signal context above.

Custom TTS shape: `createCustomTTSProvider({name, supportedOutputFormats, defaultOutputFormat, synthesize: async(text,ctx)=>{...}})` where the context exposes `ctx.audioFormat`, `ctx.audioChunk(buffer)`, `ctx.complete()`, and `ctx.signal`.

## Package maturity pointer
The README defers maturity detail: "See Package Maturity Model for information about package maturity levels and current status" (`PACKAGE-MATURITY.md` in the repo root).
