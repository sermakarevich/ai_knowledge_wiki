# VoiceBlender/voiceblender — In Plain Language

> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

## What is this about?

VoiceBlender is a Go service that connects different kinds of voice calls
into shared conversations.

Think of it as a universal switchboard: an old office phone (SIP), a browser
call (WebRTC), a WhatsApp call, or a program sending audio over a WebSocket
can all end up talking to each other in the same room.

Each incoming or outgoing call is called a "leg." Legs are placed into
"rooms," where their audio is mixed together so everyone can hear each other.

On top of basic calling it adds the extras a voice app usually needs:
recording, playing announcements, converting text to speech and speech to
text, plugging in AI voice agents, detecting answering machines, and sending
live notifications (webhooks) when things happen.

You control all of it through a REST API (default port 8080) and a live
event-plus-command stream called VSI. Everything is configured with
environment variables — there is no config file to edit.

## Why does it matter?

Mixing phone networks and internet voice is normally painful.

Classic phone systems speak SIP with codecs like PCMU, PCMA, or G.722.
Browsers speak WebRTC with SDP and ICE. WhatsApp needs encrypted SIP-TLS
plus secure audio. Each world has its own dialing, holding, and audio rules.

VoiceBlender hides that mess behind one uniform idea — legs and rooms —
plus one API for dialing, answering, muting, holding, recording, and talking
to AI services.

That matters because most teams do not want to become experts in SIP
session timers, early media, re-INVITEs, SDP negotiation, jitter buffers,
or codec quirks. They want "call this number, put these three people
together, record it, transcribe it, hand it to an AI agent."

It also matters operationally: the API contract is written down in API.md
plus generated OpenAPI and AsyncAPI specs, configuration is explicit
environment variables, and there are unit plus integration tests — so the
behavior is predictable and scriptable rather than click-and-hope.

## How does it work?

Picture five steps from a phone ringing to a finished recording.

1. **A call arrives or is dialed as a leg.** SIP legs negotiate a codec,
   prove identity with digest auth, and keep the call alive with session
   timers. WebRTC legs exchange SDP offers/answers with trickle ICE.
   WhatsApp legs use SIP-TLS with encrypted audio. WebSocket legs stream
   raw audio frames. Each leg gets an ID, a type, a state, and flags like
   muted, deaf, held, plus a free-form role tag.

2. **Legs join rooms that mix audio.** A room is a shared mixer running at
   8, 16, or 48 kHz (16 kHz by default). Everyone hears everyone else
   except themselves ("mixed-minus-self," so you do not hear your own echo).
   Two rooms at the same sample rate can be bridged, and a who-hears-whom
   matrix by role can shape who hears whom — applied when each leg joins.

3. **Call controls run over REST.** Dialing, answering, holding, muting,
   transferring, sending keypad tones (DTMF), playing a WAV/MP3, starting
   recording, or attaching speech-to-text are simple HTTP calls. Calls that
   trigger real phone-network actions answer `202 Accepted` ("got it,
   working on it") and later report success or failure as events, because
   the phone network may take seconds to respond.

4. **Media and AI services plug into legs or rooms.** Recordings are stereo
   WAV files that can pause, resume, and upload to S3 or Google Cloud
   Storage. Text-to-speech can pre-synthesize a reply and hold it before
   playing it. Speech-to-text streams back partial transcripts. AI agents
   (ElevenLabs, VAPI, Pipecat, Deepgram) can join a leg or room, and extra
   messages can be injected mid-conversation. Answering-machine detection
   guesses human vs. machine vs. silence.

5. **Your app follows along in real time.** Every important moment emits an
   event — ringing, connected, on hold, disconnected with a call summary,
   transcript chunk, DTMF digit. Events arrive as signed webhooks (with
   retry) or over the VSI WebSocket stream, which also accepts commands
   like mute, hold, or move-leg-to-room. Metrics flow to Prometheus.

Security note in plain terms: the HTTP API itself has no passwords or API
keys. Access is limited only by an IP allowlist (ALLOWED_IPS) plus where
you place it on the network — so it must sit behind a firewall or reverse
proxy in production.

## Where can this be used?

- **AI call centers and voice bots.** Dial out, detect voicemail, play a
  prompt with text-to-speech, transcribe the reply, hand the call to an AI
  agent, record everything.
- **Conference and support bridges.** Pull a SIP desk phone, a browser user,
  and a WhatsApp caller into one mixed room; bridge two rooms for
  escalations.
- **Call recording and compliance.** Capture per-person or whole-room audio,
  store it locally or in S3/GCS, and keep the disconnect summary as a call
  record. SIPREC support covers classic recording-server setups.
- **Interactive phone menus (IVR).** Play announcements, listen for keypad
  tones or spoken answers, route by role.
- **Live captions and accessibility.** Stream real-time transcripts and
  real-time text (RTT) alongside the audio.
- **Custom telephony backends.** Use the REST + VSI stream as the
  programmable core behind a helpdesk, dispatch, or outreach tool instead
  of renting a black-box telephony platform.
- **Labs and experiments.** The optional Media-over-QUIC leg and
  multi-stream SIP support give a testbed for newer transport ideas.

## Conclusions & takeaways

- VoiceBlender is a "join everything into one conversation" box: many
  kinds of voice in, one mixed conversation out, one API to rule it.
- The legs-and-rooms model is the key simplification — learn those two
  ideas and the rest (mute, hold, record, transcribe, AI agent) slots in.
- Async-by-design is honest engineering: the API says "accepted" fast and
  tells you the real phone-network outcome later via events.
- The whole system is configured by environment variables and described by
  generated specs, which makes it reproducible but means you must manage
  that env file and IP allowlist carefully.
- If you remember one caution: never expose port 8080 directly to the
  internet — there is no login, only the IP allowlist and your network.

## Jargon decoder

| Term | What it means in plain language |
|---|---|
| Leg | One call connection (incoming or outgoing, any kind) that can be put in a room. |
| Room / mixer | A shared conversation; the mixer blends everyone's voice so all can hear. |
| SIP | The classic internet-phone signaling language for dialing, ringing, holding up. |
| WebRTC | Browser-voice technology; lets a web page join a call with mic and speaker. |
| SDP / ICE | The "here is my audio setup" note and the "find a network path" dance browsers do. |
| Codec (PCMU, Opus, …) | The recipe for squeezing voice into bytes; both ends must agree on one. |
| DTMF | Telephone keypad tones (0–9, *, #) sent as audio signals. |
| TTS / STT | Text-to-speech (robot reads text aloud) and speech-to-text (transcribes voice). |
| Webhook / VSI | A webhook is an automatic "it happened" web ping; VSI is the live WebSocket feed of the same events plus commands. |
| 202 Accepted | HTTP for "request looks fine, still working on it — I will tell you the outcome later." |
