> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# AI Native Call Center — In Plain Language

## What is this about?

Imagine calling a company's support line and, instead of hearing
"press 1 for billing, press 2 for…", a helpful voice just answers and
talks with you like a person would.

That is what this project is: an open-source call center where an AI
voice assistant picks up every call by default. There is no phone menu
and no robot reading a fixed script word by word.

The AI listens to you, talks back in real time, and follows a loose
plan — for example "greet the caller, figure out the problem, and pass
them to a human expert if needed." When a human is required, the AI
hands the call to a real agent, who sees everything that was already
said so you never have to repeat yourself.

Everything runs on a simple setup: one main program, a database that
remembers calls and settings, and a telephone switchboard (a tool
called FreeSWITCH) that connects callers, the AI, and agents together.

## Why does it matter?

Anyone who has waited on hold or fought a phone menu knows the pain:

- Missed calls mean missed customers. If nobody picks up, the caller
  hangs up and may never call back.
- Human agents are expensive and limited. They can only handle one
  call at a time and need breaks, training, and sleep.
- Old phone bots feel stupid. Menu trees ("press 3… press 5…") annoy
  people, and older bots that transcribe, think, then speak in three
  separate steps sound slow and clumsy.

This project matters because it removes the menu entirely: every call
is answered immediately by something that can actually hold a
conversation. Routine questions get solved on the spot, and human
agents spend their time only on the calls that truly need a person.

Because the whole conversation — the AI part and the human part — is
kept as one record with one transcript and one recording, managers
get a clear picture of what happened instead of three disconnected
fragments. And because it is open source, any team can run it
themselves rather than renting a black-box service.

## How does it work?

Follow one call from start to finish:

1. **The phone rings at the switchboard.** Your call arrives at
   FreeSWITCH, the piece that handles raw telephone connections.
   It bridges you to the AI, which lives inside the main program.
2. **The AI talks to you directly.** The program opens a live
   voice-to-voice connection to an AI provider (such as OpenAI,
   Gemini, Qwen, or Doubao). Your voice audio is passed straight
   through — no slow chain of separate transcribe-think-speak steps.
3. **A "flow" steers the conversation.** Think of a flow as a set of
   stages: greeting, gathering details, solving, handing over,
   saying goodbye. The AI chooses its own words, but the flow
   decides which stage you are in, which tools are available
   (checking business hours, joining a queue), and when to move on.
   Some stages even hand the AI exact lines to say, like a goodbye.
4. **Handover to a human when needed.** If you need a person, the AI
   places you into a waiting line (a queue). An agent working in
   their web browser gets a pop-up *before* their phone even rings,
   already showing who you are and what you told the AI.
5. **One record for the whole call.** From the moment the call
   starts, it gets one ID. The transcript, the recording, and the
   call log all attach to that ID, whether you spoke only to the AI,
   only to a human, or to both.
6. **Agents use a browser plus a phone add-on.** The web page handles
   presence ("I am available"), call buttons, and callbacks; a small
   Chrome extension handles the actual voice, holding the agent's
   phone login. The page itself has no dial pad — control commands
   travel separately from the audio.

Under the hood, only three pieces run: the single Go program (web
interface included), the PostgreSQL database, and FreeSWITCH. Even
the phone system's own settings — extensions, queues, numbers — are
stored in the database, so adding a queue is a data change, not
rewiring.

## Where can this be used?

- **Small business support lines.** One number that always answers,
  day or night, in English or Chinese — no missed calls after hours.
- **Appointment booking and callbacks.** The AI can take details
  and the system can queue follow-up calls for agents.
- **Billing and order questions.** Routine lookups are handled by
  the AI; tricky disputes transfer to a human with full context.
- **After-hours coverage.** The AI can politely explain a queue is
  closed ("we open at 9") as conversation, not as an error beep.
- **Teams that want self-hosting.** Anyone needing their call data
  on their own servers (rather than in a vendor's cloud) can run
  the Docker setup, which seeds a demo team, queues, bilingual
  flows, and sample history out of the box.
- **Developers extending a phone platform.** New voice providers,
  new conversation flows, and new screens each have a defined
  plug-in path (a provider profile, a validated JSON flow, the web
  design system), and outside systems connect through a backend
  URL rather than custom code inside the project.

One limit to note: each installation uses a single AI provider,
chosen when it starts (for example Qwen or Doubao inside mainland
China, OpenAI or Gemini elsewhere). The caller's language never
switches the provider.

## Conclusions & takeaways

- Answer every call with a talking AI first, not a menu — humans
  join only when they add value.
- Guide without scripting: the AI owns the words, the flow owns
  the stage, and tool results decide when to move on.
- Make handover seamless: the agent sees the caller's story before
  the phone rings.
- Keep one conversation as one record: one log, one transcript,
  one recording.
- Stay simple to run: one program plus a database plus a
  switchboard, configured from the database.
- Skip the old three-step voice pipeline entirely — this design
  deliberately contains no separate transcribe-then-think-then-speak
  chain.
- Treat performance numbers as intentions for now: capacity and
  latency goals exist, but the benchmark campaign has not run yet.

## Jargon decoder

| Term | What it means in plain language |
|---|---|
| Flow | The loose plan for a call: stages like greeting, solving, handing over, goodbye. |
| Phase / stage | One step inside a flow, with its own instructions and allowed tools. |
| Speech-to-speech | The AI hears voice and answers in voice over one live connection, not three separate steps. |
| FreeSWITCH | The open-source telephone switchboard that connects callers, the AI, and agents. |
| Queue | A waiting line for human agents; the AI places you there when a person is needed. |
| CDR (call record) | The single log entry for a whole conversation, AI part and human part together. |
| Transcript | The written text of everything said on the call. |
| SIP endpoint | The AI's "phone extension" inside the program that the switchboard can call. |
| Provider | The outside AI voice service answering calls (e.g. OpenAI, Gemini, Qwen, Doubao); one per installation. |
| ESL event / screen pop | The instant signal that makes the agent's browser show the caller's info before the phone rings. |
