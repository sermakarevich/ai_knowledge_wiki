> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# soniqo/speech-core — In Plain Language

Think of speech-core as a toolbox for giving gadgets ears and a voice,
without ever calling the cloud.

## What is this about?

This project is on-device speech infrastructure written in C++17.
It covers the whole spoken-conversation loop in one place.

In plain terms, it handles:

- Noticing when someone is actually speaking (voice activity detection).
- Turning speech into text, both from recordings and live microphone input.
- Figuring out who spoke when, when several people talk.
- Turning text back into spoken audio.
- Connecting all of that into a voice agent that can listen, think, answer, and act.

The whole thing runs locally on an ordinary CPU.
There is no cloud service, no Python needed when it runs,
and your audio never leaves the machine.

A full offline voice demo fits in about 1.2 GB on Android,
which is small enough for a phone.

## Why does it matter?

Most voice assistants today send your voice to someone else's servers.
That creates three problems: privacy risk, internet dependence, and delay.

This project matters because it removes that trade-off:

- Privacy: everything happens on your own device, so conversations stay yours.
- Offline use: it works on planes, in factories, in rural areas, anywhere without reliable internet.
- Speed: there is no round trip to a data center, so interruptions and answers feel natural.
- Control: app makers choose their own speech models instead of being locked to one vendor.
- Reach: the same core works on Linux, Windows, macOS, and Android phones.

In short, it makes private, responsive voice assistants practical
on hardware people already own.

## How does it work?

Imagine a restaurant kitchen. One person takes orders, others do the cooking.
Here, a small "manager" layer runs the conversation,
and replaceable "cooks" do the heavy listening and speaking work.

The manager layer is the orchestration core. It owns:

- Turn detection: deciding when you started and finished speaking.
- Interruption handling: letting you cut in, just like with a human.
- Audio utilities: buffering, resampling, and cleaning up sound.
- Conversation state: remembering what was said earlier in the chat.
- Tool calls: letting the assistant do things, like checking a calendar.

The manager itself knows nothing about any particular AI model.
That is deliberate. The app plugs in whatever models it wants
through simple abstract interfaces for listening, speaking,
speech detection, turn completion, and cleanup.

There are two ready-made sets of "cooks":

- An ONNX Runtime backend for desktops, servers, and phones.
- A LiteRT backend aimed at efficient on-device phones and embedded machines.

You can use one, both, neither, or write your own.
Switching is a build-time choice, not a rewrite of your app.

For live conversation, the core is built for responsiveness.
It transcribes eagerly while you are still talking,
shows partial transcripts, detects the end of your turn,
lets you barge in, and starts speaking back in a stream
rather than waiting for a whole sentence to finish.

Streaming speech recognition uses a modern design
with memory of what it just heard, smart guessing among
several possible wordings, detection of when an utterance ends,
and hints from expected phrases like names or commands.

The portable surface is native C++ plus a simpler C interface,
so it can be called from Android apps, Apple apps,
embedded Linux boxes, and command-line tools.

Releases ship as Linux packages or a Windows ZIP
that bundle the runtime libraries but never the AI models.
You download the models separately, which keeps packages small
and licensing clean.

## Where can this be used?

Anywhere you want a device to listen and talk without the cloud:

- Phone assistants that work in airplane mode.
- Car dashboards that take voice commands with no signal.
- Smart-home hubs that keep family conversations inside the house.
- Customer-service kiosks and robots that answer on the spot.
- Accessibility tools that transcribe or speak for users locally.
- Factory or hospital devices where privacy rules forbid recordings leaving the room.
- Hobby and embedded projects on small Linux boards.
- Local demos and developer tools, including a command line
  that can transcribe files, detect turns, speak text,
  clone a voice from a short sample, or serve speech over a local web API.

Because the core has zero machine-learning dependencies by itself,
even tiny or locked-down targets can use the conversation logic
and add only the models they need.

## Conclusions & takeaways

- Speech-core is plumbing, not a chatbot: it is the reusable
  ears, mouth, and timing layer that voice apps share.
- Local-first is the headline feature: CPU-only, offline,
  private by construction.
- Separation is the big design idea: a small model-agnostic manager
  plus swappable ONNX or LiteRT model backends.
- Live behavior is built in, not bolted on: turn-taking,
  interruptions, partial results, streaming speech, and tool use.
- Shipping is taken seriously: tested on several operating systems,
  with packaged releases and clear rules about what is bundled.
- If you remember one sentence: it lets ordinary devices hold
  natural spoken conversations entirely on their own.

## Jargon decoder

| Term | What it really means |
|---|---|
| On-device / local-first | Everything runs on your own hardware; no internet or cloud needed. |
| VAD (voice activity detection) | Deciding which bits of audio contain human speech versus silence or noise. |
| STT (speech-to-text) | Turning spoken words into written text. |
| TTS (text-to-speech) | Turning written text into spoken audio. |
| Diarization | Labeling who spoke when in a recording with several speakers. |
| Turn detection | Deciding when the speaker has finished so the assistant may reply. |
| Barge-in | Letting the user interrupt the assistant mid-sentence. |
| ONNX Runtime / LiteRT | Two popular engines for running AI models efficiently on devices. |
| Orchestration layer | The small manager that coordinates listening, thinking, and speaking. |
| Abstract interface | A plug socket: any model that fits the shape can be plugged in. |
