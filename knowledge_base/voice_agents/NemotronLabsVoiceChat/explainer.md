> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# NemotronLabs VoiceChat: An Open Full-duplex Speech-to-Speech Model with Tool Calling Capabilities — In Plain Language

## What is this about?

This paper introduces NemotronLabs VoiceChat, an open voice-chat system you can talk to naturally, like a person on a phone call.

Most voice assistants today work in strict turns: wait until you finish, then think, then speak. VoiceChat instead listens and speaks at the same time, so it can handle pauses, overlaps, quick "uh-huh" remarks, and interruptions gracefully.

What makes it unusual is that it can also use tools while talking — for example, looking something up or running a calculation — without breaking the flow of conversation.

The model and checkpoint are openly released (paper: NVIDIA, arXiv:2609.21967, Sept 2026), so other researchers can inspect, reuse, and build on it.

In the paper's tests it is compared against open rivals (Moshi, Freeze-Omni, PersonaPlex) and closed services (Gemini Live, GPT Realtime) on interruption handling, general voice intelligence, and spoken tool use.

## Why does it matter?

Human conversation is not turn-by-turn. We nod along, say "yeah" while someone talks, jump in, hesitate, and pause mid-sentence — and none of that ends the conversation.

Today's typical voice assistant pipeline (speech recognition, then a chatbot, then a synthetic voice, gated by a silence detector) misses all of that. It either cuts you off too early or waits too long, and it goes silent while fetching information.

Earlier full-duplex research fixed some of the timing problems but mostly ignored tool use. Commercial systems that do support live tool calls are closed. VoiceChat is presented as the first fully open full-duplex speech model with general tool calling built in.

Good test results here would mean one open system can be smart, natural-sounding, accurate at hearing you, and useful — all at once, in real time.

## How does it work?

Think of VoiceChat as three teammates sharing one pair of ears.

**One shared ear.** A streaming audio encoder listens to your voice continuously, slicing sound into small pieces (one snapshot every 80 milliseconds) using only past audio, never peeking ahead. That keeps delays low.

**A brain with two pens.** A large language model (Nemotron-Nano-9B-v2-Base) reads those snapshots and writes two things in parallel: (a) the words the assistant should say, and (b) structured tool requests, such as "get the weather for Tokyo." Keeping speech and tool calls on separate tracks means a tool request never jams up the conversation.

**A transcriber and a voice box.** A small auxiliary transcriber writes down what you said as you speak (a live caption), and a separate streaming voice generator turns the assistant's planned words into audible speech — including staying quiet when it should and stopping promptly when interrupted.

Simple frame-by-frame rules teach manners: one signal means "start talking," another means "stop," and a default means "stay silent."

Training happens in stages. First the listening-and-talking backbone learns from huge amounts of synthetic spoken dialogues, then it is fine-tuned on real-style conversations, instructions, safety examples, and tool-use dialogues — including artificially added interruptions, backchannels, background noise, and room echoes. The transcriber and the voice box are each trained separately and plugged in at the end.

At call time there are practical tricks: the assistant says a short filler ("Let me check that for you") to cover tool delays, and a backup rule watches the live transcript to force a start or stop if the main model hesitates.

## Where can this be used?

Anywhere a spoken helper needs to sound natural and get things done:

- Customer-service phone agents that can interrupt, apologize, clarify, and check an order status mid-call.
- Hands-free assistants for driving, cooking, or lab work, where "stop, wait, what?" has to work instantly.
- Tutoring and language practice, where backchannels ("uh-huh") should encourage rather than derail the speaker.
- Accessibility tools offering live captions plus spoken answers from a single system.
- Voice control for smart homes, robots, or cars, where a command like "what's the weather in Tokyo?" needs a real lookup, not a guess.
- Research prototypes for studying overlap, politeness, and timing in spoken dialogue, since the checkpoint is open and reusable.

The authors suggest keeping the tool list short (about five or fewer per session) and note the system remembers roughly two minutes of audio context — so short, task-focused calls fit best today.

Open models also let small teams experiment without depending on a closed realtime API: they can add their own tools, filler phrases, and voices.

## Conclusions & takeaways

- VoiceChat shows that listening, speaking, transcribing, reasoning, and tool use can live in one open, real-time system without ruining conversational timing.
- On turn-taking tests it is polite under pressure: lowest needless takeovers during pauses among open models, always yields appropriately to interruptions with high-quality recovery (4.33/5), and correctly keeps talking through backchannels 93% of the time.
- It is reasonably smart for its class (VoiceBench average 55.1, about tied with Freeze-Omni) and good at picking the right tool (82.5% tool-selection score, ahead of the tested Gemini Live endpoints).
- The weak spot is follow-through: getting the exact tool settings right and completing multi-step tool jobs (argument accuracy 42.2%, end-to-end success 33.0%) still lag behind closed systems.
- Known limits: short memory (~2 minutes), shaky with many tools at once or several tools in parallel, occasional made-up settings or answered-from-memory instead of calling the tool, no interruption while a tool is running, and sensitivity to noise and overlapping voices.
- The voice itself holds up well: clear first impressions that stay stable across turns, though unfamiliar cloned voices can drift slightly over long chats.
- Bottom line: natural timing plus open tool use is now demonstrated — the next hurdle is precise, reliable tool execution.

## Jargon decoder

| Term | Plain meaning |
|---|---|
| Full-duplex | Listening and speaking at the same time, like a phone call, not walkie-talkie turns. |
| Half-duplex / cascaded stack | The old design: transcribe, then think, then speak, switching on silence detection. |
| Turn-taking (takeover rate) | Who speaks when; takeover rate measures how often the assistant grabs or yields the floor. |
| Backchannel | A short listener sound ("uh-huh", "yeah") that means "I'm following," not "it's my turn." |
| Barge-in / interruption | When you start talking over the assistant and it should stop and listen. |
| Tool calling (function call) | The assistant asking an external app or service to do something, e.g. fetch weather. |
| Argument accuracy | Whether the assistant filled in the tool's details (which city? which date?) correctly. |
| Streaming encoder | The part that converts incoming audio into compact snapshots as it arrives. |
| RNN-T transcription branch | A small add-on that writes live captions of your speech from the same audio snapshots. |
| TTS / codec decoder | The voice box that turns planned words into audible speech, piece by piece. |
| Voice activity detection (VAD) | A simple silence sensor old systems use to decide "the user finished, my turn now." |
| End-to-end success (Pass@1) | The whole job done right on the first try: right tool plus exactly right details. |
