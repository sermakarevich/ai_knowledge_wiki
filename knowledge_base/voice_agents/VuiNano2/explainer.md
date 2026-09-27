> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# fluxions-ai/vui — In Plain Language

Think of Vui (pronounced "vooey", short for "Voice User Interface") as a talk-to-your-computer kit: you speak into a browser page, it listens, thinks, and talks back in a natural voice. Vui Nano is the small voice engine at its center.

## What is this about?

Most computer voices read one sentence at a time, in isolation, which is why they sound flat. Vui Nano instead remembers the whole conversation so far — your words and the actual sound of your voice — and generates each reply inside that context.

The headline facts are simple:

- Vui Nano is a small speech model: 219 million active parameters out of 305 million total, released under the open Apache 2.0 license.
- It does voice cloning, live streaming, and even runs on a plain CPU with no GPU.
- It was trained on real two-person conversations, not read-aloud audiobooks.

Around the model sits a complete assistant served from a single Python server: microphone input over WebRTC, speech recognition, a local language model, and speech output back to your speaker.

You can try it several ways:

- A one-line installer that clones the project into `~/vui` and sets everything up.
- A Python package (`vui-tts` for the voice engine alone, `vui-tts[server]` for the full assistant).
- A Docker Compose setup paired with a local language model.
- A standalone demo page for playing with voices, or a dependency-free pure-C build for CPUs.

Voice and model files download automatically on first use, so installing stays lightweight.

## Why does it matter?

Real speech has breaths, laughter, hesitations, and interruptions. Read-aloud recordings do not. Because Vui Nano learned from genuine two-speaker conversations, it reproduces those human touches and carries tone across turns instead of resetting every sentence.

The size is the surprise. The few other open models that listen to dialogue audio this way are roughly ten times bigger and need powerful graphics cards. Vui Nano does it at 219M active parameters, streams about nine times faster than realtime on a card like an RTX 4090, and still runs on a CPU or a Mac. That makes conversational voice practical for hobbyists, small teams, and private on-device setups.

It is also a complete package rather than just a weights file: a voice assistant, a demo playground, standard API endpoints, and a CPU fallback all live in one repository.

In short: small enough to run anywhere, human enough to hold a conversation, and open enough to build on.

## How does it work?

Picture the loop: microphone → WebRTC → voice-activity detection → speech-to-text → chat model → Vui Nano speech → speaker. A "thoughts" stream watches each turn and routes your intent to about fifteen tools such as saving a memory, searching the web, setting timers, or handing work to a helper agent.

Three tricks keep it feeling live:

- Voice-activity detection handles turn-taking, and the chat model starts drafting while you are still speaking.
- Speech is synthesized sentence by sentence with backpressure, so audio starts playing before the full reply is ready.
- Barge-in: interrupt, and the current reply is cancelled so the assistant listens to you instead.

Under the hood, the dialogue lives in a memory called the KV cache holding roughly six minutes of conversation. Each new reply is generated from that cache — including the audio of your turn, not just its transcript — with an explicit speaker-change marker so prosody, breaths, laughter, and overlap carry across. The model itself is a compact Llama-style network with a layered audio head over a 12 Hz speech codec that turns codes back into 24 kHz sound.

Quality knobs travel with the model: six speech-quality channels plus a speaking-rate (words-per-second) control, and four shipped voice presets (`maeve`, `abraham`, `rhian`, `harry`) for cloning by example.

For developers, the moving parts are explicit: the streaming server runs on port 8080, an optional task sidecar on 8642, speech recognition swaps between faster-whisper (GPU) and Moonshine (CPU), and the chat model can be Ollama, vLLM, or any OpenAI-compatible endpoint — switchable live from the UI. Facts persist across sessions in a memories file; setup is managed by scripts that never need administrator privileges and auto-detect Docker versus native install plus your GPU type.

## Where can this be used?

- Personal voice assistant in the browser: talk hands-free, set timers, look up facts with built-in web search, keep simple cross-session memories.
- Custom voices: clone a voice from a short reference recording via the demo page, one command, or a few lines of Python.
- Apps and gadgets: an OpenAI Realtime-compatible WebSocket plus a one-call voice-note endpoint suit bots, phone shortcuts, and home automation.
- Low-power and private settings: the CPU build, Mac support, and local models fit offline, low-budget, or privacy-sensitive deployments.
- Delegated work: an optional helper sidecar takes on slow multi-step jobs like email, calendar, or research while the voice loop stays responsive.
- Demos and content: two-speaker dialogues, expressive monologues, and disfluency-marked reads (laughs, sighs, hesitations) for podcasts, narration, and testing.

## Conclusions & takeaways

Vui Nano shows that conversational, human-sounding speech does not require a giant model — it requires the right context. By keeping the dialogue's sound in memory, a small model can breathe, laugh, hesitate, and stay in character.

The repository turns that idea into something you can actually run: one command, a browser tab, and you are talking.

The honest trade-offs:

- Quality still depends on clean reference audio and light tuning of the quality and rate controls.
- The easy path assumes a Linux machine with an NVIDIA GPU; other platforms use fallback math or the CPU build.
- There is no committed test suite, so changes are verified end-to-end through the running assistant or demo rendering.

But for open, local, realtime voice, it is a remarkably complete and approachable package: model, assistant, API, and CPU fallback in one place.

## Jargon decoder

| Term | Plain definition |
|---|---|
| Text-to-speech (TTS) | Technology that turns written text into spoken audio. |
| Parameters | The model's learned numbers; more usually means bigger and more capable, but slower. |
| Active vs total params | Weights on disk versus the ones doing math each step; lookup tables cost memory but no compute. |
| Context / KV cache | The model's short-term memory of the conversation so far, reused so it need not re-read everything. |
| Speech codec | A compressor that turns audio into compact codes the model can predict, then back into sound. |
| Voice cloning | Copying a speaker's voice from a short reference recording plus its transcript. |
| ASR (speech recognition) | Technology that turns your spoken audio into text the chat model can read. |
| VAD | Voice-activity detection: notices when someone is actually speaking versus silence. |
| WebRTC | Browser technology for live microphone and speaker audio over the network. |
| Barge-in | Interrupting the assistant mid-reply; it stops talking and listens. |
| Backpressure | Slowing down speech generation when playback falls behind, so nothing piles up. |
| LLM backend | The chat model service (Ollama, vLLM, or similar) that writes the reply text Vui speaks. |
