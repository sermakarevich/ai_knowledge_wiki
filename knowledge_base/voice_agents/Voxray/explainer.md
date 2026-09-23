> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# Voxray-AI/Voxray — In Plain Language

## What is this about?

Voxray is an open-source server, written in Go, for building voice assistants
you can actually talk to in real time.

Think of it as a switchboard for conversations. You speak into a browser or a
phone call, and Voxray carries your voice through three steps — hearing what
you said, thinking of a reply, and speaking that reply back — fast enough that
it feels like a phone call, not a chatbot with long pauses.

The big idea is that all of this is defined in a single settings file. You
pick which hearing, thinking, and speaking services to use, which voices and
models you want, and how the call should behave. Change one line in that file
and you have swapped providers — no rewiring of audio code needed.

Out of the box it supports a wide menu: more than 10 hearing services, more
than 20 language models, and more than 15 voice services. It talks to users
over the web (WebSocket or WebRTC) and over phone networks through services
like Twilio, Telnyx, Plivo, Exotel, and Daily.co.

## Why does it matter?

Building a voice assistant from scratch is normally painful. You have to
connect microphone audio, detect when someone starts and stops talking, stream
audio to a transcription service, feed text to a language model, stream the
answer to a voice service, and play it back — all without awkward delays, and
while letting people interrupt.

Voxray does that plumbing once, so every new voice project does not reinvent
it. A team can go from an empty folder to a working voice agent in minutes by
copying an example config file and adding API keys.

It also matters because it avoids lock-in. Since each stage (hearing,
thinking, speaking) is interchangeable, you are not stuck with one vendor. If
a better or cheaper transcription service appears, or you need a voice that
speaks Hindi well, you change a name in the config instead of rebuilding.

Finally, it is self-hostable and production-minded: it includes call
recording, saved transcripts, usage metrics, and an optional API key, so it
can run on your own servers rather than only inside someone else's cloud.

## How does it work?

Picture a single phone call. Inside the Voxray server, that call gets its own
little assembly line:

1. **Listen.** Audio arrives from the browser, app, or phone call.
2. **Notice speech.** A voice-activity detector watches the audio stream and
   decides when you have started and finished speaking.
3. **Hear.** The speech clip is sent to a speech-to-text service, which
   returns words.
4. **Think.** Those words, plus a personality instruction like "keep replies
   brief and conversational," go to a language model, which streams back a
   reply word by word.
5. **Speak.** The reply text goes to a text-to-speech service, which streams
   audio back to the caller as it is generated.
6. **Deliver.** A transport layer carries the audio home — either WebSocket
   or WebRTC for browsers, or a phone-network bridge for calls.

One HTTP server fronts all of this, with routes for starting sessions,
exchanging connection details, checking health, viewing metrics, and reading
API docs. Each call is a session: you create one, connect audio to it, and
Voxray runs the assembly line for as long as the call lasts.

Extra features ride on top of the same line. A caller can interrupt the agent
mid-sentence ("barge in"). The language model can call outside tools through
a standard tool interface. Each session can save a mixed-audio recording to
cloud storage and save its transcript to a database. Operators can watch
Prometheus metrics and structured logs to see how the system is doing.

Developers control all of this without editing code: one JSON file sets the
host and port, the providers and models, the voice, the speech-detection
sensitivity, whether interruptions are allowed, recording and database
settings, and more. Any setting can also be overridden with an environment
variable, which is handy for secrets and deployments.

Running it is deliberately simple. The plain web version needs only a modern
Go toolchain. The high-quality browser-call version additionally needs a C
compiler on PATH for audio encoding. Standard commands build, run, and test
the project, and live tests for some providers are skipped unless you provide
their API key.

## Where can this be used?

- **Customer-support voice bots.** Answer common questions by phone or on a
  website, with interruption support so callers do not have to wait through
  long robot speeches.
- **Hands-free helpers.** In-car, kitchen, or warehouse assistants where
  typing is impractical and replies must be short and spoken.
- **Phone-call automation.** Appointment reminders, order updates, or simple
  surveys delivered through Twilio-style phone integrations.
- **Multilingual services.** Teams serving Indian languages, for example, can
  pick providers and voices tuned for those languages with a config change.
- **Prototyping new voices.** Product teams can A/B test voices and language
  models in an afternoon by editing the settings file instead of rebuilding.
- **Self-hosted deployments.** Banks, hospitals, or governments that must
  keep audio and transcripts inside their own network can run Voxray in their
  own data center and store recordings and transcripts themselves.
- **Tool-using agents.** Assistants that need to look something up or trigger
  an action mid-call can let the language model call outside tools while the
  caller waits on the line.

## Conclusions & takeaways

Voxray's core bet is that voice AI should be assembled, not hand-wired: one
config file plus a streaming pipeline replaces a pile of custom audio code.

The assembly line itself is simple to picture — microphone to speech
detection to hearing to thinking to speaking to speaker — and every stage can
be swapped like a Lego brick.

The surrounding details are what make it production-ready rather than a demo:
two web transports plus phone networks, interruption handling, tool calls,
recordings, transcripts, metrics, logs, plugins, and a documented,
versioned API with a simple optional key.

If you remember three things: it is config-driven, it streams everything for
low delay, and it runs on your own infrastructure with your choice of AI
providers.

## Jargon decoder

| Term | What it really means |
|------|----------------------|
| STT (speech-to-text) | The "ears": turns spoken audio into written words. |
| LLM (large language model) | The "brain": reads the words and writes a reply. |
| TTS (text-to-speech) | The "mouth": turns the reply text into spoken audio. |
| VAD (voice activity detection) | Notices when someone starts and stops talking, so the system knows when to listen and when to answer. |
| Barge-in / interruption | Letting the caller cut off the agent mid-sentence, like in a natural conversation. |
| WebSocket | A steady two-way connection between browser and server, used here to carry call audio and control messages. |
| WebRTC | A browser standard for real-time calls with low delay; the higher-quality call option here. |
| Turn detection | Deciding when the speaker has finished a turn, so the agent knows it is its turn to talk. |
| MCP tool call | A standard way for the language model to ask an outside program to do something, such as look up data. |
| Prometheus metrics | Built-in counters and stats operators can monitor, e.g. how many calls are running. |
| Config-driven | Behavior is set by editing a settings file, not by rewriting code. |
| Self-hostable | You can run the whole thing on your own servers instead of renting someone else's service. |
