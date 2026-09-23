> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# 🎙️ AI Voice Agent — Mission Control — In Plain Language

Imagine calling customer support and talking to a computer that actually
listens, understands, answers out loud, and files your support ticket —
all without an expensive monthly platform bill. That is what this project is:
a do-it-yourself voice assistant for customer support, with a flashy
control-room dashboard.

## What is this about?

This project is a complete, working phone-call-style assistant that runs
in your web browser.

You click a button labeled **Start Call**, speak into your microphone,
and the system talks back to you with a spoken answer — like a support
agent on the other end of the line.

Under the hood it is three steps chained together: it turns your speech
into text, figures out a helpful reply, and then turns that reply back
into spoken audio.

On top of that talking loop, it has two extra skills. First, it can read
your company's manuals and answer questions based on them. Second, it can
create and update customer support tickets, the same way a human agent
would log your problem.

Everything is shown on a dark, cyberpunk-style dashboard called Mission
Control, with live sound waves, ticket updates, and system health lights.

## Why does it matter?

Normally, if a business wants a voice assistant, it rents one from a
specialized company — names like Retell AI, Vapi, or Synthflow.

Those services are convenient, but they add a large markup on top of the
raw cost of the underlying AI. This project claims you can cut that
operating cost by up to **90%** by building the same loop yourself.

The trick is using parts that are free or cheap: speech recognition that
runs on your own computer, a fast low-cost language model in the cloud,
and a free voice-synthesis service.

That matters for small teams, hobbyists, and anyone who wants full control:
no vendor lock-in, no per-minute surprises, and every piece can be
inspected and swapped.

It also matters as a learning example. Instead of a black box, you get a
fully visible pipeline — microphone to answer — that you can study,
tinker with, and extend.

## How does it work?

Think of it as a relay race with six runners, passing the baton from your
voice to the computer's voice:

1. **You speak.** Your browser captures your voice as simple, raw audio
   (16kHz PCM16 — just a standard, no-frills sound format) and sends it
   to the server over a fast, always-open connection called a WebSocket.
2. **It notices you are talking.** An energy detector (called voice
   activity detection) watches the loudness of the incoming sound and
   decides when a real sentence has started, so silence is ignored.
3. **It writes down what you said.** A local program called Faster-Whisper
   (the `small.en` version) converts your speech into text, right on your
   own machine — no paid transcription service needed.
4. **It thinks of a reply.** A large language model (Llama 3.3 with 70
   billion parameters, running on the Groq cloud) reads your words, checks
   the manuals if needed, and drafts an answer plus any ticket updates.
5. **It speaks, one sentence at a time.** Instead of waiting for the whole
   answer, a voice synthesizer (Edge TTS) reads each sentence aloud as soon
   as it is ready, so you start hearing the reply almost immediately.
6. **The sound is packed for travel.** A tool called PyAV converts the
   voice into small audio chunks and streams them back to your browser,
   where they play through your speakers.

Two thoughtful details make it feel human. If you interrupt mid-answer,
the system stops talking and listens to you instead — this is called
barge-in. And when it manages tickets, it updates the existing ticket for
your problem rather than piling up duplicates.

The supporting cast is deliberately simple: Python with FastAPI on the
server, plain HTML/CSS/JavaScript in the browser, a small SQLite database
for records, and a single API key (Groq) in a `.env` file. You start it
with `python main.py`, open `http://127.0.0.1:8000`, and talk.

To teach it your business, you just drop manuals (`.txt`, `.md`, or
`.pdf` files) into a folder named `knowledge/`. On startup the server
reads them, turns them into numerical summaries called embeddings, and
searches them in milliseconds whenever a question arrives.

## Where can this be used?

- **Small-business phone support.** Answer common questions — opening
  hours, prices, return policies — spoken aloud, around the clock.
- **Help desks that drown in manuals.** Drop product guides into the
  knowledge folder and let the agent quote the right page instead of a
  human flipping through PDFs.
- **Ticket triage.** Let the agent take the first call, log the problem,
  and update the same ticket on follow-up calls instead of spawning
  five copies of one issue.
- **Prototypes and demos.** A team evaluating voice AI can get a working
  demo running locally before committing to an expensive platform.
- **Classrooms and makerspaces.** Because every stage is visible and
  replaceable, it is a great hands-on way to learn how modern voice
  assistants actually fit together.

## Conclusions & takeaways

The big idea is simple: a voice support agent is just speech-to-text,
a smart reply, and text-to-speech — plus memory (manuals) and paperwork
(tickets) — wrapped in a live dashboard.

You do not need an expensive middleman to connect those pieces. With
local transcription, a fast cloud model, and free voice synthesis, an
individual or small team can run the whole loop for a fraction of the cost.

The trade-off is that you own the setup: you install Python 3.9+,
provide one API key, and keep the manuals fresh. In return you get
transparency, low latency from sentence-by-sentence speech, natural
interruptions, and tidy ticket handling.

If you remember one thing, let it be this: talk in, think fast, speak
back sentence by sentence — and keep the receipts in the knowledge
folder and the ticket list.

## Jargon decoder

| Term | What it really means |
|---|---|
| Speech-to-Text (STT) | Turning spoken words into written text so the computer can read them. |
| Text-to-Speech (TTS) | Turning written words into spoken audio so the computer can talk. |
| LLM (large language model) | The "brain" that reads your question and writes a human-like reply. |
| Groq / Llama 3.3 70B | A fast cloud service (Groq) running a big AI model (Llama 3.3) that does the reasoning here. |
| Faster-Whisper | A free program that converts speech to text on your own machine. |
| RAG (Retrieval-Augmented Generation) | Looking up your manuals first, then letting the AI answer using what it found. |
| Embedding | A list of numbers that captures the meaning of a piece of text, used for fast searching. |
| Cosine similarity | A math trick for asking "how close in meaning are these two texts?" |
| VAD (voice activity detection) | The loudness watchdog that decides when you have started speaking. |
| Barge-in / full duplex | You can interrupt the agent mid-sentence and it stops to listen, like a real conversation. |
| WebSocket | An always-open line between browser and server so audio flows instantly both ways. |
| SQLite / SQLAlchemy | A tiny built-in database (SQLite) plus a helper library (SQLAlchemy) that stores tickets and records. |
