> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Nishal77/Pipeline — In Plain Language

## What is this about?

PipeLine is an "AI phone-office" for solo plumbers in the United States.

Think of a one-person plumbing business. The owner spends the day
under sinks, not near a phone. When a customer calls about a leak,
nobody picks up — and that job goes to a competitor.

PipeLine is built to answer those calls instead. It is a software
system that picks up the phone, talks with the caller, books the job,
and shows the business owner what happened.

At the time described in the notes, the project is a starter kit
rather than a finished product. The folders, the database shape,
the rules for the phone agent, and the test setup are in place.
The live decisions — which voice technology to use, which phone
carrier to use, and several business registrations — are still open.

The plan comes from a product document (PRD v2.0), with the roadmap
in a file called `claude.md` and step-by-step build plans in `spec/`.

## Why does it matter?

A solo tradesperson loses money on every missed call.

Hiring a receptionist is expensive and rarely makes sense for a
one-person shop. An automated receptionist that answers every call,
day or night, directly protects income.

Three details make this project practical rather than just a demo:

- It is designed around booking real jobs, not just chatting.
  The phone agent works through a fixed contract of actions
  (the "agent tool contract"), so the voice system and the web
  backend agree on exactly how a booking is created.
- Customer data is separated per business. The database rules
  (per-account row-level security) mean one plumber cannot see
  another plumber's customers or jobs.
- Big choices are tested before they are locked in. There is a
  benchmark harness that compares two voice approaches head to
  head on speed, and an architecture decision record for the
  voice setup, so the team picks with measurements, not hunches.

In short: fewer missed calls, booked jobs, and a system the owner
can check from a phone app.

## How does it work?

Picture the system as four rooms plus a shared rulebook.

1. The phone room (`apps/voice`). This handles the actual call:
   hearing the caller, figuring out what they need, speaking back,
   and triggering a booking. It also holds the speed test that
   compares the two voice approaches described below.

2. The office backend (`apps/api`). This is the server that stores
   and serves bookings and owner-app data. It connects to the
   database and currently has basic health checks; it grows into
   the full booking system in later phases.

3. The owner app (`apps/web`). This is the phone-friendly web app
   the plumber checks to see jobs and messages. It arrives in
   Phase 4 and is still a placeholder for now.

4. The database (`supabase/migrations`). This is schema version 1:
   the tables for the business records, with per-account access
   rules so each shop only sees its own data.

5. The shared rulebook (`packages/shared`). This holds the database
   row shapes and the single agent tool contract both the voice
   system and the backend use, so a booking means the same thing
   everywhere.

Two ways of building the voice are kept side by side:

- Option A: realtime speech-to-speech (one service listens and
  speaks in a single flow).
- Option B: a chain of three steps — speech-to-text, then a
  language model that decides the reply, then text-to-speech.

Getting started is deliberately simple: copy the example settings
file, fill in real keys, install dependencies, then run the
typecheck, lint, and test commands.

What is finished in Phase 1: the repository, the automated checks,
the database schema, the agent tool contracts, and the voice test
setup. What still needs live keys or paperwork: running the voice
speed test for real, choosing Option A or B, choosing between the
Twilio and Telnyx phone carriers, registering the US business,
opening payments in test mode, filing the bulk-texting approval,
and verifying call forwarding with real carriers.

## Where can this be used?

The direct use is the one it was designed for:

- A solo plumber (or similar tradesperson) who wants every call
  answered, jobs booked automatically, and a simple app showing
  what came in while they were on a job.

The pattern transfers to nearby cases:

- Other solo home-service businesses — electricians, HVAC techs,
  appliance repair — with the same "hands busy, phone ringing"
  problem.
- Small shops that need after-hours coverage without hiring
  overnight staff.
- Anyone evaluating phone-agent technology who wants a concrete
  example of benchmarking two voice stacks, recording the decision,
  and sharing one action contract between voice and backend.

It is not yet a drop-in product: the notes describe scaffolding
plus open credential and legal steps, not a deployed service.

## Conclusions & takeaways

- PipeLine is a phone-answering and job-booking system for solo
  US plumbers, currently at the scaffolded-foundation stage.
- Its structure is a monorepo with clear jobs: voice, backend,
  owner app, shared contracts, database, and decision docs.
- One shared action contract keeps the voice agent and the backend
  consistent about what a booking is.
- Per-business database rules keep each shop's data private.
- The team measures before committing: a latency benchmark picks
  the voice approach, and a decision record captures the reasoning.
- The remaining work is mostly real-world activation — live keys,
  carrier tests, payments, and registrations — not missing code
  structure.

## Jargon decoder

| Term | What it means in plain language |
|---|---|
| Monorepo | One big code folder that holds several related mini-projects side by side. |
| pnpm workspace | The tool setup that links those mini-projects so they share installs and versions. |
| Fastify backend | The behind-the-scenes server program that stores data and answers app requests. |
| Next.js PWA | The owner-facing web app, built to work well on a phone's browser. |
| Supabase | The hosted database service where business records are stored. |
| Row-level security (RLS) | Database rules so each business account only sees its own rows. |
| Voice pipeline | The chain that turns a caller's speech into a reply: hear, think, speak. |
| Speech-to-speech | One service that listens and talks back in a single realtime flow (Option A). |
| STT / LLM / TTS | Hear (speech-to-text), think (language model), speak (text-to-speech) chained together (Option B). |
| Agent tool contract | The fixed list of actions the phone agent is allowed to trigger, like booking a job. |
| ADR | A short written record of an important technical decision and why it was made. |
| A2P 10DLC | The official approval needed to send business text messages to US phones. |
