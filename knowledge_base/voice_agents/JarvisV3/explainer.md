> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# CarverXx/jarvis-v3 — In Plain Language

## What is this about?

JARVIS v3 is a voice assistant inspired by Iron Man's Jarvis that lives
entirely on one computer in your home or office.

You say "Hey Jarvis," ask a question out loud, and it answers back in its
own cloned voice — no cloud account, no subscription, no audio sent to a
big tech company.

Under the hood it has "two brains": one fast brain that chats with you,
and one slower brain that does real work like searching your notes or
checking the weather on the web.

Think of it like a receptionist and a researcher sharing one desk. The
receptionist greets you instantly; the researcher disappears into the
back room when a question needs digging, then hands the receptionist a
short note to read aloud.

## Why does it matter?

Most voice assistants send every word you say to the cloud. That means
latency, fees, outages, and privacy worries.

JARVIS v3 flips that deal: the speech recognition, the language model,
and the voice itself all run locally on one Linux machine with a strong
graphics card.

The only thing that ever leaves the house is an explicit web search.
Everything else — your voice, your questions, your personal notes —
stays on your own hardware.

It also solves a classic assistant dilemma. One language model cannot be
both instant and thorough, so the project splits the job: quick replies
in under a second, deeper tool-using work in 5 to 30 seconds, with a
little "working on it" beep in between so you know it heard you.

## How does it work?

A conversation moves through five steps, like an assembly line:

1. **Wake word.** The microphone listens all day for "Hey Jarvis" using
   a small, cheap detector plus a personal voice check trained on about
   20 samples of your own voice. This cuts false alarms from the TV or
   family members.
2. **Hearing.** Once woken, it records what you say until you pause, then
   turns the audio into text with a local speech-recognition model.
3. **Fast brain (Subconscious).** A large language model decides: is this
   small talk I can answer directly ("hello", simple math), or real work
   (weather, notes, system status)? Small talk gets a one- or two-sentence
   reply in about 300 milliseconds.
4. **Slow brain (Hermes).** For real work, the fast brain hands off a task
   note. The slow brain runs an agent loop: it can search your notes, read
   files, search the web, check services, retry when tools fail, and then
   summarize the result. This can take up to two minutes for hard tasks.
5. **Speaking.** A voice-cloning speaker reads the short answer aloud in
   a Jarvis-like voice, built from a single 4–8 second reference clip.

Six small programs cooperate on one machine: the language model, the
hearer, the speaker, the worker, the toolbox, and the main coordinator.
A six-panel terminal dashboard shows what each part is doing live, so
you can watch the state, microphone, transcript, thinking, tool work,
and speech as it happens.

Clever plumbing keeps it stable: the microphone mutes while Jarvis
speaks (so it does not hear itself), input is flushed between turns, and
a short cool-down after each answer breaks self-trigger loops.

## Where can this be used?

- **Private home assistant.** Answer questions, read notes, check weather
  or news, without sending household audio to the cloud.
- **Personal knowledge desk.** Point it at a folder of Markdown notes and
  ask questions in plain speech; it searches and reads the files for you.
- **Workshop or lab machine.** Run it on a Linux server with a USB
  microphone and speaker as an always-on helper that survives restarts.
- **Privacy-sensitive offices.** Keep meetings, notes, and voice data on
  local hardware while still getting spoken answers.
- **Learning project.** Study how wake words, speech recognition, language
  models, tool agents, and speech synthesis fit together, since every
  piece and setting is visible in one configuration file.

You will need a beefy computer (tens of gigabytes of graphics memory),
Linux with a microphone and speaker, and some patience to install models
and tune the microphone.

## Conclusions & takeaways

JARVIS v3 shows you do not need the cloud to get a natural voice
assistant — you need careful choreography of local parts.

Its big idea is the two-brain split: be fast when you can, be thorough
when you must, and always tell the user which mode you are in.

Its second idea is that setup details matter as much as AI: microphone
gain, pause detection, echo muting, personal wake-word training, and a
live dashboard are what make the difference between a demo and a tool
you can leave running all day.

If you remember one sentence: a fast talker plus a slow worker, both
living on your own machine, sharing one cloned voice.

## Jargon decoder

| Term | What it really means |
|---|---|
| Local-first | Everything runs on your own computer, not on someone else's servers. |
| Dual-brain / Subconscious + Hermes | A fast chatterbox that replies instantly, plus a slower helper that uses tools for hard questions. |
| Wake word | A magic phrase ("Hey Jarvis") that tells the assistant to start listening. |
| ASR (speech recognition) | The "ears": turns your spoken audio into written text. |
| TTS (speech synthesis) | The "mouth": turns written answers into spoken audio. |
| VAD (voice activity detection) | A gatekeeper that decides when you started and stopped speaking by spotting silence. |
| Agent loop / tool-calling | The slow brain trying tools one by one (search notes, read a file, search the web) until the job is done. |
| MCP tool server | A shared toolbox the slow brain can call: files, notes search, web search, system checks. |
| Voice cloning | Copying a voice's sound from a short sample clip so the assistant speaks in that voice. |
| State machine | The assistant's moods in order: idle, listening, thinking, answering, then briefly listening for follow-ups. |
