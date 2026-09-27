> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# vedantnimbarte/IRA — In Plain Language

## What is this about?

IRA is a voice assistant for your computer that you talk to out loud — and, crucially, you can interrupt.

Think of it like Siri or Alexa, but one that runs on your own machine as a single program. You say a wake phrase ("hey Jarvis"), hear a chirp, and just talk. It listens, turns your speech into text, asks a language model for an answer, and speaks the answer back to you — all in a flowing conversation.

What makes it different from most voice assistants is that it treats conversation like humans do:

- You do not need to repeat the wake phrase for follow-up questions. After answering, it leaves the floor open for about 2 seconds in case you want to continue.
- You can cut it off mid-sentence. If it starts saying something wrong or something you already know, just start talking and it stops.
- It can *do things*, not just chat: it connects to tools (small programs on your machine or network services) that can look things up or change things for you.
- Anything risky — anything that changes state rather than just reading — gets asked about out loud first. Only an explicit spoken "yes" lets it go ahead.
- While it works, a small on-screen display (plus a floating globe, called the orb) shows what it is doing, so you are never guessing.

## Why does it matter?

Speech recognition itself has been good enough for years. What still feels broken about voice assistants is the *turn-taking*:

- You pause to think, and the assistant jumps in too early and cuts you off.
- The assistant starts a long wrong answer, and you have to sit through it because there is no polite way to interrupt.

IRA's core bet is simple: a slightly slower model that yields the floor correctly is better than a smarter one that talks over you.

Three consequences follow from that bet:

1. **Interruption is structural, not a hack.** The whole program shares one cancellation switch across listening, thinking, and speaking. Interrupting means flipping that one switch: drop the model's reply stream and clear the queued-up audio in the same instant.
2. **Safety is spoken, not buried in a dialog box.** Before running anything that changes something, IRA reads the action back and waits for an out-loud yes. Silence, a vague answer, or interrupting the question all count as "no."
3. **Everything stays visible.** The screen and the orb read the same live event stream, so what you hear and what you see never drift apart.

## How does it work?

A conversation moves through a small state machine — a fixed set of stages with clear rules for moving between them:

1. **Idle — waiting for the wake phrase.** A small on-device model (openWakeWord) listens continuously for "hey Jarvis." Nothing leaves your machine at this stage.
2. **Listening — capturing your sentence.** Once woken, it watches the microphone in tiny 32-millisecond slices using a voice-activity detector (Silero). A short 200 ms pause is enough to start transcribing in the background; 700 ms of silence means you are done and the turn is over.
3. **Holding — thinking and speaking at once.** Your transcribed words go to the language model, which streams its reply back word by word. IRA does not wait for the whole answer: it chops the stream into sentences and starts speaking each sentence (via the Piper voice engine) while the rest is still being written. Barge-in stays armed the whole time — if it hears you, it first ducks the volume, then cuts off completely once it is sure.
4. **Confirming (only when needed) — asking permission.** If fulfilling your request needs a tool that changes something, IRA asks out loud and listens for yes or no. Anything other than a clear yes is a no.
5. **Open floor — a 2-second grace period.** After answering, it keeps the floor open briefly for a follow-up, then goes back to Idle.

Under the hood, a handful of parts each do one job: audio capture, wake-word detection, voice-activity detection, speech-to-text (cloud or local), streaming model replies, the tool registry with its confirmation gate, the screen and orb display, and storage (your keys go to the operating system's secure keyring; machine settings go to a local database).

Starting it for the first time downloads the voice and listening models, saves your API key securely, and runs a self-check (models, microphone, keys) before the microphone ever opens — so a missing key stops the program immediately instead of failing silently mid-sentence.

One practical warning from the project: there is no echo cancellation. On loudspeakers, the microphone hears IRA's own voice and she interrupts herself — so wear headphones or switch to press-to-talk mode.

## Where can this be used?

- **Hands-free computer control.** Trigger announcements from scripts or background jobs (for example, "the build finished") that politely wait for a pause instead of talking over you.
- **Coding alongside a terminal agent.** IRA can talk to Wingman, a terminal coding agent, over its local HTTP API — so you can discuss code out loud while you work.
- **Extending with your own tools.** Open the settings screen and plug in a new capability two ways: write a small built-in tool, or connect an external tool server. Either way it shows up in the same list with an on/off switch and a test box.
- **Scripting and automation setups.** Terminal commands let you add tools, manage keys, and check system health over SSH or in provisioning scripts, without needing the graphical screen.
- **Custom dashboards and integrations.** A tiny local web surface exposes the current status, a live event stream, and a speech-trigger endpoint, so other programs on your machine can ask IRA to say something or show what is happening.

## Conclusions & takeaways

- Turn-taking is the product: wake word, fast endpointing, overlapping transcription, sentence-at-a-time speech, and one-switch interruption add up to a conversation that feels human.
- One process, one cancellation token: keeping microphone, model stream, and speaker in a single program is what makes interruption instant and reliable.
- Spoken confirmation before state changes keeps a powerful tool setup safe without pop-ups or fine print.
- Visibility is a feature: the screen, the orb, and the event stream all read the same source of truth.
- The trade-offs are honest: first start means large model downloads, keys and a microphone are mandatory, and you need headphones or press-to-talk without echo cancellation.

## Jargon decoder

| Term | What it means in plain language |
|---|---|
| Wake word | The trigger phrase ("hey Jarvis") that tells the assistant to start listening. |
| Endpointing | Deciding when you have started and finished speaking, using pauses and silence. |
| Voice-activity detection (VAD) | The component that tells speech apart from background noise, checked many times per second. |
| Speech-to-text (STT) | Turning recorded audio of your voice into written words the model can read. |
| Barge-in | Interrupting the assistant mid-reply by simply starting to talk. |
| Cancellation token | A single shared "stop" switch that halts listening, thinking, and speaking all at once. |
| Tool / tool registry | An extra capability IRA can call (built-in or external); the registry is the master list of all of them. |
| MCP server | An external program offering tools over a standard plug-in protocol, added via the settings screen. |
| Confirmation gate | The rule that state-changing tools need an explicit spoken "yes" before running. |
| Orb | The small floating globe on screen that mirrors what IRA is doing. |
| Keyring | The operating system's secure vault where IRA keeps API keys instead of files. |
