> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# CodeVoice: AI-Powered Technical Interview Simulator — In Plain Language

## What is this about?

CodeVoice is a practice tool for technical job interviews that talks to you out loud.

Instead of typing answers into a chat box, you open a web page, connect
your microphone, and have a spoken conversation with an AI interviewer.

The AI greets you, asks a coding question — for example, "Can you explain
the difference between a process and a thread?" — then listens to your
answer and replies with the next question or follow-up, all in real time.

It is a small public project on GitHub built from a `src` code folder,
Docker setup files, a requirements list, and a README.

In short: a voice-to-voice mock interviewer that runs in the browser.

## Why does it matter?

Technical interviews are stressful, and most people get little chance to
rehearse the spoken part.

You may know the right answer but stumble when you have to say it clearly,
handle a follow-up, or think while someone is listening.

CodeVoice matters because it gives you a patient, always-available partner
to practice exactly that skill: explaining technical ideas out loud.

For builders, it also matters as a working example of how to glue together
modern voice-AI pieces — speech recognition, a language model, and speech
synthesis — into one low-delay conversation loop instead of three separate
demos.

It shows the plumbing, not just the idea.

## How does it work?

Think of it as a phone call with four participants: you, a switchboard,
a robot brain, and an organizer.

1. **You (the browser).** A test page plus real-time audio streaming
   captures your microphone and plays back the AI's voice.
2. **The switchboard (LiveKit server).** A real-time audio/video router,
   running in Docker on port 7880, carries sound both ways with minimal
   delay. You join a room called `interview-room-1` as `human-candidate`;
   the bot joins the same room as `ai-interviewer`.
3. **The robot brain (Pipecat pipeline).** The heart of the app, in
   `src/apps/simulation/bot.py`, runs a five-step loop for every turn:
   listen to audio, convert speech to text, think up a reply with a
   language model, convert the reply back to speech, and send the audio out.
4. **The organizer (Django backend).** Handles user accounts, interview
   sessions, a database, and background jobs, so the voice loop is not
   doing bookkeeping on its own.

Two helper commands start the show: one launches the bot, the other prints
a login token you paste into the browser page to join the room.

A smart turn-detector waits until you actually finish speaking before the
AI jumps in, so it does not cut you off mid-sentence.

The greeting is scripted — "Hello! I'm your AI interviewer. Let's begin…"
— and after that the language model carries the conversation.

## Where can this be used?

- **Interview practice.** Rehearse explaining algorithms, systems design,
  or past projects out loud before a real interview.
- **Coding bootcamps and classes.** Give every student unlimited mock
  interviews without scheduling human volunteers.
- **Hiring teams.** Run a consistent first-round screening where every
  candidate gets the same opening questions.
- **Language and communication coaching.** Practice clear, calm technical
  explanations under mild time pressure.
- **Voice-AI prototyping.** Reuse the same listen-think-speak loop for
  tutoring bots, customer-support voice agents, or hands-free coding help.

Anywhere a spoken question-and-answer loop is useful, this pattern fits.

## Conclusions & takeaways

CodeVoice is not a big product; it is a clear, small blueprint.

Its main lesson is architectural: keep the fast audio path (browser to
switchboard to voice pipeline) separate from the slow bookkeeping path
(user accounts, sessions, database), and connect them loosely.

Its second lesson is about manners: real-time voice lives or dies on
turn-taking, so waiting for a full pause before answering matters as much
as giving a smart answer.

If you remember one thing, remember the loop: hear, write down, think,
speak, repeat — fast enough that it feels like a conversation.

## Jargon decoder

| Term | Plain meaning |
|---|---|
| LiveKit | The real-time switchboard that carries live audio/video between browser and bot |
| Pipecat | A toolkit for chaining voice-AI steps (listen, think, speak) into one pipeline |
| STT (speech-to-text) | Software that turns your spoken words into written text; here provided by Deepgram |
| LLM (large language model) | The AI brain that reads the transcript and writes the interviewer's next reply |
| TTS (text-to-speech) | Software that turns the written reply into a spoken voice; here a Deepgram voice |
| WebRTC | The browser technology that streams microphone audio with very low delay |
| Turn detection | The logic that decides when you have finished speaking so the bot can reply |
| Room / identity | A named call space plus a screen name inside it, e.g. `interview-room-1` with `ai-interviewer` |
| Token | A long secret string that proves you are allowed to join the call |
| Django control plane | The behind-the-scenes website code managing users, sessions, and the database |
| Celery + Redis | A to-do list system that runs slow background jobs outside the live call |
