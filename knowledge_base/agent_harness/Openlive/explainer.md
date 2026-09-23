> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# katipally/openlive — In Plain Language

Think of OpenLive this way: your AI does the thinking, and OpenLive gives it ears, a mouth, and eyes — all running on your own computer.

## What is this about?

OpenLive is an open, on-device voice and vision layer for AI agents.

In plain terms: instead of typing to your AI, you talk to it, interrupt it, and show it things through your camera or screen — and it talks back out loud.

The key idea is "bring your own brain." OpenLive is not itself the smart model. You plug in whatever brain you already use:

- A model you hold an API key for, such as Anthropic, OpenAI, Google, xAI, DeepSeek, or Groq — or a fully local model via Ollama.
- Or a coding agent you already use, such as Claude Code, Codex, Cursor, OpenCode, or Hermes.

Everything around that brain — listening, knowing when you finished speaking, transcribing, speaking the answer, and watching camera or screen frames — runs locally on your machine using your graphics chip (WebGPU).

Only the final text transcript (plus camera or screen frames, only if you turn that on) is sent to the brain you picked. Your raw audio never uploads.

## Why does it matter?

Talking to an AI sounds simple, but making it feel like a real conversation takes a lot of hidden plumbing.

A usable voice assistant has to: notice when someone starts speaking, transcribe speech as it streams in, figure out when the person actually finished their sentence, send that to the model, then speak the reply as it streams out — while letting you interrupt mid-word.

Hosted products such as ElevenLabs Agents, Gemini Live, and OpenAI Realtime rent you that whole pipeline by the minute, in their cloud.

OpenLive matters because it makes that pipeline open and local:

- No per-minute audio fees. You only pay the model costs you would pay anyway. If your brain is a coding agent running under your existing login, there is nothing extra.
- More privacy. Listening, speaking, and watching happen on-device. Nothing spoken leaves the machine except the final transcript.
- Freedom of brain. You are not locked to one provider. Swap models or coding agents per conversation, even mid-call.
- Voice for tools you already use. It turns terminal coding agents into hands-free partners you can talk to while you work.

Under the hood, the repo backs this with ordinary, careful engineering: a pnpm monorepo with shared strict TypeScript settings, one pinned AI-runtime library copy to avoid crashes, one test runner for all packages, and tag-driven releases that build installers for macOS, Windows, and Linux.

## How does it work?

Picture one round trip of conversation, step by step:

1. **Listen.** The microphone feeds a voice-activity detector (Silero VAD) that tells speech apart from silence and background noise.
2. **Write down.** A speech-to-text engine (Whisper) transcribes your speech as you talk, streaming the words out.
3. **Wait for the real pause.** An end-of-turn detector (Smart-Turn) decides whether you actually finished, so it does not cut you off at every small breath.
4. **Think.** The finished text goes to your chosen brain — a keyed model provider, local Ollama, or a coding agent driven locally over a standard protocol (Agent Client Protocol over local stdio).
5. **Speak.** As the reply streams back, a text-to-speech voice (Kokoro with 28 light voices, or Supertonic with 10 higher-quality voices) speaks it sentence by sentence through your speaker.
6. **Interrupt any time.** Barge-in means you can cut in mid-word and it stops talking and listens again.

Two extras ride along:

- **Eyes.** Camera or screen frames ride each turn so the brain can see what you see. A `look` tool grabs a sharp frame on demand. Even a text-only model can borrow a separate vision model's eyes.
- **Your own voice.** In Settings you can clone your voice from a 5- to 30-second recording, preview it with any text, and reuse, rename, export, or delete it. Cloning runs locally.

For coding agents specifically, calls land in the agent's own native sessions (for example, a Claude Code call lands where `claude --resume` finds it), so you can resume from either side. You can switch model and mode mid-call, hear permission requests spoken aloud ("allow this edit?") and answer by voice, follow a narrated plan checklist with a live cost/context chip, shrink to an always-on-top listening pill, and export the whole transcript as Markdown. API keys are encrypted at rest.

Getting started is deliberately simple: install the app, paste a model key or pick an installed coding agent, and start a call. Voice models download once from Hugging Face on first talk (around 200 MB with Kokoro) and are cached. Developers can build from source with `pnpm install` and `pnpm desktop:dev`.

## Where can this be used?

- **Hands-free coding.** Talk to Claude Code or a similar agent while your hands stay on the keyboard: dictate changes, hear plan steps narrated, approve file edits by saying "yes."
- **Cheap voice prototypes.** Build a talking assistant without paying a hosted voice platform per minute.
- **Private dictation and Q&A.** Keep raw audio on the laptop; only text goes to the model.
- **Visual help.** Point the camera at an error on screen, share your screen, or ask it to look closely at something.
- **Personal assistant with your voice and rules.** Custom instructions apply to every brain, with adjustable speaking speed and spoken progress updates.
- **Fully offline setups.** Pair it with Ollama for a local brain plus local ears and mouth.
- **Teams shipping desktop AI apps.** Reuse the pattern: Electron shell plus web UI plus a small local agent server over a warm WebSocket.

## Conclusions & takeaways

- OpenLive is "that voice pipeline, open and local": ears, mouth, and eyes around any brain you bring.
- Its core trade is explicit: a step-by-step cascaded pipeline (speech to text to model to speech) instead of a single full-duplex speech-to-speech model — and that trade is what makes any-brain, all-local, no-audio-fees possible.
- Privacy follows from architecture: local voice loop, text-only uplink, encrypted keys, deletable voice profiles.
- Coding-agent support is a first-class feature, not an afterthought: native sessions, permission relay, narrated plans, costs, and Markdown transcripts.
- If you remember one sentence: your AI thinks, OpenLive lets it listen, speak, and see — on your machine, with the brain of your choice.

## Jargon decoder

| Term | What it really means |
|---|---|
| Voice activity detection (VAD) | The part that notices "someone is speaking now" versus silence or background noise. |
| Speech-to-text (STT) | Turning spoken audio into written words; here done by Whisper on your device. |
| End-of-turn detection | Guessing "are they done, or just pausing?" so the assistant does not jump in too early. |
| Text-to-speech (TTS) | Turning the written reply into spoken audio; here Kokoro, Supertonic, or your cloned voice. |
| Barge-in | Interrupting the assistant mid-sentence; it stops talking and listens. |
| Cascaded pipeline | Doing voice in separate steps (listen, write, think, speak) rather than one giant audio-in-audio-out model. |
| Bring your own brain | You supply the smart model or coding agent; OpenLive supplies everything around it. |
| Agent Client Protocol (ACP) | The standard local language OpenLive uses to drive coding agents, sent over local stdio channels. |
| WebGPU / on-device | Running the listening and speaking AI on your own computer's graphics chip instead of in the cloud. |
| Voice cloning | Teaching the app to sound like you from a short recording, kept locally and deletable. |
| Monorepo | One repository holding several apps and packages together with shared settings and one test runner. |
| Tag-driven release | Shipping new installers simply by pushing a version tag, with automation building all platforms. |
