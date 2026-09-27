> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# streamcoreai/streamcore-server — In Plain Language

## What is this about?
StreamCore is a single program, written in Go, that handles live voice
conversations between people and AI assistants.

Think of it as the "phone system plus stage crew" for talking to AI.
You speak, it listens, it passes your words to an AI, and it plays the
AI's spoken answer back — all fast enough to feel like a phone call.

Importantly, the smart part — the AI's personality, knowledge, tools,
and business rules — lives outside StreamCore. StreamCore owns only the
hard real-time plumbing: getting audio in and out, knowing when it is
your turn to talk, letting you interrupt, and keeping the call alive
when the network wobbles.

You run it as one file on your own computer or server. It listens on
port 8080, and a voice call starts with a single web request to an
address called `/whip`. There is also a `/health` address that simply
answers "ok" and a `/token` address that hands out login passes.

Setup is deliberately simple: copy an example settings file, add your
speech and AI keys, and start the program. If you want everything local,
you can use local models instead of paid cloud services.

## Why does it matter?
Talking to AI sounds easy until you try to make it feel natural.

A normal chatbot can take its time. A voice assistant cannot. If there
is a long silence, if it talks over you, if it cannot hear you interrupt,
or if the call drops when you walk between rooms, people hang up.

StreamCore exists to solve those unglamorous but decisive problems:

- Starting audio instantly without a complicated login dance.
- Reaching phones and browsers even behind home routers and office
  firewalls, without running a separate network helper service.
- Knowing when you have finished a sentence versus just pausing to
  think, so it does not jump in too early or wait too long.
- Letting you interrupt naturally ("wait, stop") while ignoring small
  sounds like "mm-hm" that do not mean "stop".
- Starting to speak before the whole answer is ready, so replies begin
  in a fraction of a second rather than after a long pause.
- Surviving one bad moment — a dropped connection, a crash in one call,
  too many callers at once — without taking down every other call.

It also matters because it does not lock you into one AI company. You
can plug in your own assistant, your own models, or a small built-in
helper, and switch speech providers as prices and quality change.

## How does it work?
A conversation moves through five stages.

1. **Call setup.** Your browser, phone, or device sends one HTTP request
   to `/whip`. That request carries the audio offer. There is no
   permanent chatty signaling connection to babysit. Login is optional
   but supported with standard tokens, and a single request can mint a
   one-hour pass for a caller.

2. **Finding and holding the path.** StreamCore includes its own network
   helper for getting through routers and firewalls. It works over both
   common network styles and can restart the connection on the same call
   if you switch from Wi-Fi to mobile data or your network address
   changes. Each call gets its own ID, and a dropped caller can redial
   with a one-time resume pass to rejoin the same conversation.

3. **Listening and taking turns.** While you speak, a detector watches
   the loudness of your call and learns your background noise level. A
   short pause inside a sentence is merged into one turn; a longer
   quiet period means "they are done, answer now." If you start talking
   while the AI is speaking, it lowers the AI's volume, checks whether
   you really meant to interrupt, and if so cancels the AI's unfinished
   thinking and speaking.

4. **Thinking and speaking in a stream.** Your speech becomes text, the
   text goes to a language model, and the model's answer is turned back
   into voice piece by piece. Playback starts before the whole answer
   is finished, which is what keeps the delay low. Alongside the audio,
   a side channel sends live captions, answers, call state, and timing
   numbers such as how long each step took.

5. **Supervision.** One main program starts everything in a fixed order:
   settings, optional diagnostics, add-ons, search helper, network
   helper, call manager, then the web addresses. If one call crashes,
   only that call ends. When the server stops, it closes add-ons first,
   then calls, then the network, with a five-second safety net.

There are honest limits: no built-in usage dashboards, plain text logs
only, no version number stamped in the program, one computer handles its
own calls with no automatic teamwork across machines, and the built-in
assistant does not remember you between restarts.

## Where can this be used?
Anywhere a person should be able to talk to a machine with their voice:

- **Web voice assistants.** A help or sales button on a website that
  actually talks back, with live captions on screen.
- **Phone systems.** Call centers and appointment lines reached over
  ordinary telephony bridges, where echo control is weak and careful
  interruption logic matters.
- **Mobile apps.** Hands-free helpers that keep working when the phone
  sleeps, moves networks, or briefly loses signal and then rejoins.
- **Internal tools.** Warehouse, clinic, or factory helpers where a
  worker with gloves or busy hands asks questions out loud.
- **Robots and gadgets.** Small devices that can send audio but cannot
  run big AI models themselves.
- **Your own AI projects.** Teams that already have an assistant or
  backend can keep it and use StreamCore only for the voice layer,
  through a web hook, a model server, a small code interface, or
  plug-in tools.

The live demo site runs this same program and even shows the delay of
each step on screen, which is handy for tuning.

## Conclusions & takeaways
StreamCore is plumbing, not a personality. It does one job — real-time
voice between humans and AI — and leaves the intelligence to you.

That split is its biggest strength: one binary, one settings file, many
choices of speech service and AI backend. The turn-taking, interruption,
streaming, and reconnection behavior is where most of the value sits,
because that is what makes a voice bot feel human instead of annoying.

For a newcomer, the mental model is: start the program, point a client
at `/whip`, speak, and watch captions and timing events arrive while
audio plays. Everything else — keys, voices, helpers, limits — is
configuration around that loop.

Go in expecting a solid single-machine voice server with clear gaps
around monitoring, logging, scaling, and memory. If you need one lively
voice front door for an AI you already own, that trade is easy to
understand.

## Jargon decoder
| Term | What it really means |
|---|---|
| WebRTC | The browser's built-in way to send live audio and video directly. |
| WHIP | A simple one-request way to start sending live audio, with no extra chat channel. |
| Opus / RTP | The standard formats for packing voice so it travels well over the internet. |
| STUN / TURN | Helpers that let calls connect through home routers and office firewalls. |
| ICE restart | Re-finding the network path for the same call after Wi-Fi or address changes. |
| VAD (voice activity detection) | Automatic sensing of when a person is actually speaking versus silent. |
| Barge-in | Interrupting the AI mid-sentence and having it stop and listen. |
| Backchannel | Small sounds like "mm-hm" that mean "I'm listening," not "stop talking." |
| STT / LLM / TTS | Hearing (speech to text), thinking (language model), speaking (text to speech). |
| DataChannel | A side text pipe next to the audio for captions, answers, and timing info. |
| JWT | A small signed digital pass that proves a caller is allowed to connect. |
| pprof | An optional hidden diagnostics page for developers, kept off the public site. |
