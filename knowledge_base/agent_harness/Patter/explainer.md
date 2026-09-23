> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# PatterAI/Patter — In Plain Language

## What is this about?

Patter is an open-source toolkit that gives your AI assistant a real phone number.

In plain terms: you write a few lines of code describing how your
assistant should behave — for example, "you are a friendly receptionist" —
and Patter connects that assistant to the actual phone network so it can
answer and place calls.

Its core promise is simple: you build the agent, and Patter handles
everything between that agent and the phone network.

That "everything in between" is the hard part of a phone call: running
the listen-think-speak loop, understanding what the caller says,
deciding what to reply, speaking the reply out loud, cleaning up
the audio, and staying connected through a phone carrier.

Patter ships in two popular programming languages — Python
(`pip install getpatter`) and TypeScript (`npm install getpatter`) —
with the same features, hooks, and events in both.

## Why does it matter?

Building a phone-capable assistant from scratch means wiring together
many separate pieces: a language model, speech recognition, voice
synthesis, audio cleanup, and a telephony provider.

Patter matters because it owns that whole stack for you, so a solo
builder can go from zero to a working phone agent quickly instead
of integrating each layer by hand.

Three practical reasons stand out:

1. **No lock-in per layer.** You pick which provider handles each job —
   the brain, the ears, the voice, and the phone carrier — and you can
   swap any of them later with roughly one line of code.
2. **Same behavior everywhere.** Built-in tools, call transfer, and safety
   guardrails work identically no matter which phone carrier you use.
3. **Resilience and visibility.** If your main AI provider fails mid-call,
   an automatic fallback chain can switch to a backup, and every call
   leaves a vendor-neutral trace you can debug the same way.

In short: it lowers the barrier to phone-capable AI while keeping
provider choice and control in the builder's hands.

## How does it work?

Think of a phone call as an assembly line with replaceable stations.
Patter runs the assembly line and lets you pick the machine at each station.

There are three ways to arrange the line:

- **Realtime mode:** one all-in-one voice engine handles listening,
  thinking, and speaking together. Lowest delay, simplest setup.
- **Pipeline mode:** separate specialists for each job — one service
  transcribes speech, another decides the reply, a third speaks it.
  More control over voices and quality.
- **Hybrid mode:** a mix of the two approaches.

Together the project claims 27+ provider integrations, 3 voice modes,
and 2 SDKs at full parity.

The stations you can choose from include:

- **The brain:** OpenAI, Anthropic, Google Gemini, Groq, or Cerebras.
- **The ears (speech-to-text):** Deepgram, AssemblyAI, Cartesia,
  Soniox, Speechmatics, Whisper, or Fish Audio.
- **The voice (text-to-speech):** ElevenLabs, OpenAI, Cartesia, LMNT,
  Rime, Telnyx, or Fish Audio.
- **All-in-one realtime engines:** OpenAI Realtime, Gemini Live,
  Ultravox, or ElevenLabs ConvAI.
- **The phone carrier:** Twilio, Telnyx, or Plivo.
- **Audio cleanup:** Silero VAD, Krisp, or DeepFilterNet.

Two cross-cutting features sit on top: automatic failover between
language-model providers mid-call, and an OpenTelemetry trace of each
call that works the same regardless of vendor.

For everyday development, you put your keys in environment variables,
run with `tunnel: true`, and Patter creates a temporary internet address
for your local code plus a built-in dashboard to watch calls.
You can even simulate a whole call from the terminal with no phone at all.
For production you point your number at a fixed address instead.

There are also ready-made starter projects for inbound answering,
outbound calling, tool calling, custom voices, per-caller personalization,
bringing your own model, monitoring, and a full production setup —
each available in both Python and TypeScript.

## Where can this be used?

- **Small-business receptionist:** answer calls as a booking assistant,
  for example for a restaurant, and take reservations after hours.
- **Outbound reminders and follow-ups:** place calls automatically,
  detect answering machines, and leave a voicemail drop.
- **Customer support with real data:** look up a caller in a CRM system
  or create a support ticket during the call via webhook tools.
- **Personalized callers:** tailor the greeting or script per caller
  using data about who is calling.
- **Custom voices and models:** use a favorite voice provider or plug in
  your own language model instead of the defaults.
- **Operations and monitoring:** watch live calls with cost and latency
  tracking, record calls, and enforce guardrails.
- **AI coding assistants:** install the published Agent Skills bundle so
  supported coding agents can scaffold Patter projects for you.

## Conclusions & takeaways

Patter's core idea is simple: a phone number should be a few lines
of code, not a large integration project.

The practical takeaway is that one builder can pick a carrier, pick
a voice engine, write a prompt, and run locally behind a tunnel —
then keep the freedom to swap providers, add failover, and trace
every call later.

The honest caveats from the same picture: you still need accounts and
secret keys for whichever providers you pick, supplied as environment
variables, and the SDK collects anonymous opt-out usage statistics —
only version and bucketed provider, model, and call facts, never call
content, prompts, phone numbers, or keys — which you can disable.

If you want a phone-capable assistant while owning the stack between
your code and the phone network, this is the starting point the project
aims to be.

## Jargon decoder

| Term | What it means in plain language |
|---|---|
| SDK | A ready-made code toolkit you install so you don't build everything from scratch. |
| LLM | The "brain" that decides what the assistant says next. |
| STT (speech-to-text) | The "ears" that turn the caller's spoken words into text. |
| TTS (text-to-speech) | The "voice" that turns the assistant's text reply into spoken audio. |
| Realtime engine | An all-in-one service that listens, thinks, and speaks in one step for lower delay. |
| Carrier (Twilio, Telnyx, Plivo) | The phone company that connects your code to real phone numbers. |
| VAD | Detection of when someone starts or stops speaking, so interruptions feel natural. |
| Agent loop | The repeating listen-think-speak cycle that keeps a call going. |
| Tunnel | A temporary public address for your local test code so the carrier can reach it. |
| OpenTelemetry trace | A standard, provider-neutral record of a call used for debugging. |
