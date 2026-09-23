> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# TEN Framework: Voice AI That Can Actually Be Interrupted — In Plain Language

## What is this about?

Imagine calling a voice assistant and trying to cut in with "wait, that's
not what I meant" — and it just keeps talking over you, or freezes up.

That is the problem TEN Framework tries to solve. TEN is a free, open-source
toolkit for building voice assistants that can hold a live conversation:
listening and speaking at the same time, the way real people do.

Most simple voice assistants are built like an assembly line. Your voice goes
in one end, gets turned into text, the AI writes an answer, and a robot voice
reads it back. That works fine for a quick demo, but it falls apart the
moment you interrupt, because the assembly line was never designed for two
people talking at once.

TEN replaces the assembly line with a team of specialists working in parallel.
One part listens, one part thinks, one part speaks, one part watches for
silences and interruptions — and they coordinate in real time.

The video puts it to the test with one simple question: can I interrupt the
agent mid-sentence without the whole thing falling apart? The short answer is
yes — it stops, listens, and picks up again, even though its actual answers
are still imperfect.

## Why does it matter?

Talking is the most natural way humans communicate, and we interrupt each
other constantly. We say "uh-huh," we jump in early, we change our minds
halfway through a sentence. A voice assistant that cannot handle that feels
rude, slow, and robotic.

Today, many voice bots are really text chatbots with a microphone taped on.
They wait for you to finish, go quiet for a few seconds while they think, and
then read out a paragraph. If you try to stop them, they get confused.

That matters because voice is showing up everywhere: customer support lines,
phone systems, smart speakers, in-car assistants, video-game characters, and
little gadgets like the ESP32 hobby boards. All of these need fast responses
and graceful interruptions.

TEN matters because it gives this messy real-time problem a proper structure.
It does not pretend the complexity goes away — it gives developers a way to
organize it, see it, and debug it, instead of duct-taping four separate
services together and hoping for the best.

## How does it work?

Think of a restaurant kitchen instead of a factory line.

In the factory-line version, one worker takes your order, walks it to the
kitchen, waits for the food, and then brings it back. Nobody else can do
anything until that whole trip finishes.

In TEN's kitchen version, there is a listener at the door, a cook in the
back, a speaker at the counter, and a manager watching the room. They all
work at once and pass notes to each other continuously.

Here is what happens when you talk to a TEN agent:

1. You speak. A listener part (speech recognition) turns your voice into
   words as you go, not just at the end.
2. A watcher part listens for pauses, background noise, and signs you have
   started talking again. This is called voice activity detection and turn
   detection — basically, "is the human speaking, and is it my turn?"
3. A thinker part (the language model) drafts a reply in small pieces,
   streaming it out instead of waiting for the whole answer.
4. A speaker part (voice synthesis) starts reading the reply aloud right
   away, while the rest is still being written.
5. If you interrupt, the watcher signals "stop!" The speaker goes quiet,
   the thinker throws away the unfinished sentence, and the listener focuses
   on your new words.

Each of these jobs is a separate plug-in, called an extension. Developers can
write extensions in Python, C++, Go, Rust, or TypeScript, and snap them
together into a graph — a map of who talks to whom. A visual designer tool
shows that map, so you can see where audio flows and where things slow down.

Getting started takes some setup: you need keys for real-time audio (Agora),
speech recognition (Deepgram), a language model (like OpenAI), and a voice
service (ElevenLabs), then one Docker Compose command to launch everything.
TEN ships with ready-made recipes, and the video finds the Deepgram-based
assistant handles interruptions best.

## Where can this be used?

Anywhere a voice assistant needs to feel natural rather than robotic:

- Customer support phone lines, where callers interrupt to correct details
  or ask follow-up questions.
- Smart speakers and in-car assistants that must respond quickly and stop
  talking when you say "never mind."
- Video calls and avatars, where a virtual character listens, speaks, and
  reacts in real time.
- Phone-system bridges (SIP telephony), connecting AI agents to regular
  phone networks.
- Small hardware gadgets and edge devices, such as ESP32 boards, where the
  assistant runs close to the user instead of only in the cloud.
- Meeting helpers like speaker diarization — figuring out who said what
  when several people talk.

It is a poor fit when you just need a simple text chatbot, a one-off demo,
or the fastest possible prototype. For those, lighter tools get you running
with far less setup.

## Conclusions & takeaways

- Real conversation is messy: people interrupt, pause, and talk over each
  other. A straight-line pipeline cannot cope with that; a parallel team
  of specialists can.
- TEN's big idea is simple: build voice agents as a connected graph of
  single-job parts, not one long chain, so the agent can stop speaking,
  cancel a half-written answer, and listen again.
- Live tests confirm the core promise. The agent can be cut off mid-sentence
  without crashing — though its answers are still limited by the underlying
  AI models, as when it confused TEN with TensorFlow.
- The price is complexity. Multiple API keys, Docker, and a graph to manage
  make TEN heavier than simpler frameworks like LiveKit Agents.
- Rule of thumb: choose TEN when interruptions, low delay, or phone, avatar,
  or edge deployment matter. Skip it when you want a quick text bot or the
  fastest voice demo.
- The memorable line: TEN does not remove the complexity of real-time voice
  AI — it gives that complexity an architecture.

## Jargon decoder

| Term | What it really means |
|---|---|
| TEN Framework | A free toolkit for building live voice assistants that can listen and speak at the same time. |
| Extension | One plug-in teammate with a single job, such as listening, thinking, or speaking. |
| Graph of extensions | A map showing how all the plug-ins connect and pass information, instead of one straight line. |
| STT (speech-to-text) | The listener: turns your spoken words into written text the computer can use. |
| LLM (large language model) | The thinker: writes the reply, like OpenAI's models do. |
| TTS (text-to-speech) | The speaker: turns the written reply into a voice you can hear. |
| VAD (voice activity detection) | The ears: notices whether anyone is currently speaking or the room is silent. |
| Turn detection | The manners: decides when the human has finished and it is the assistant's turn to talk. |
| Interruption handling | The ability to stop mid-sentence, throw away the rest, and listen to you instead. |
| Docker Compose | A single-command launcher that starts all the pieces of the project at once. |
