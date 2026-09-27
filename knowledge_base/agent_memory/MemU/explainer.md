> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# NevaMind-AI/memU — In Plain Language

Imagine every AI assistant you use — on your laptop, your desktop,
your phone — sharing one notebook about you and your work.
That notebook is memU: personal memory, stored as a wiki,
that follows you across sessions, agents, and devices.

## What is this about?

Most AI assistants are forgetful. Each chat starts from zero,
and what one assistant learns never reaches the others.

memU fixes that with a small shared memory layer that sits
beside your assistants. It watches your past sessions,
writes down the useful lessons as short readable notes,
and hands those notes back the next time any assistant
faces a similar task.

The whole core is deliberately tiny — about 500 lines —
so an ordinary person (or their agent) can read it,
understand it, and change it. Nothing is hidden
in a giant black box.

In short: memU turns your scattered AI chats into
one growing wiki of reusable skills.

## Why does it matter?

Without shared memory, you repeat yourself endlessly:
re-explaining your project, your preferences, your past decisions
to every new chat window. That wastes time and loses hard-won lessons. A fix you discovered
with one assistant on Monday is gone by Friday when you ask
a different assistant a similar question.

memU matters because it:

- remembers once, reuses everywhere — a lesson learned on one
  machine shows up on your other machines too;
- saves durable know-how, not just chat logs — it distills
  messy history into clean step-by-step skills with pitfalls
  and edge cases included;
- keeps judgment with the agent, not a hidden service —
  the memory service only stores and finds notes, it never
  secretly makes AI decisions behind your back;
- stays inspectable — the notes are plain Markdown you can
  read, edit, or delete, and uninstalling keeps your memory
  unless you explicitly ask for erasure.

## How does it work?

Think of memU as a helpful librarian sitting next to each
of your AI assistants. Each assistant gets its own small
helper program (one per host, such as Claude Code or Cursor),
and all helpers share one memory store on your machine
or in the memU Cloud.

The librarian does two jobs, over and over:

**1. Record — writing things down.**

A scheduled background task regularly re-reads recent
session history: your messages plus what the assistant did.
It slices each session into a small self-contained job and
asks the agent: is there anything here worth keeping?

The agent has three choices: do nothing, fix an existing note,
or write a brand-new skill note with a name, a description,
and a reusable workflow. Changed notes are then committed
and indexed so they can be searched later.

**2. Inject — bringing things back.**

A standing instruction tells each assistant: before you answer,
look up relevant memories first. The assistant runs a retrieve
command with the current question, memU searches its notes
by meaning (not just keywords), and the best matches are
fed back into the conversation.

Setup follows the same pattern everywhere: install one package,
pick your assistant's helper, point it at a shared backend,
register the background task, and patch one instruction file.
A built-in health check verifies the whole loop — settings,
backend choice, and a live test retrieval.

You can run privately on one device with a local database file,
or across devices with a hosted account and an API key.
Under the hood there are three storage options: throwaway
in-memory for tests, a simple local file database, and a
bigger shared database for heavy or concurrent use.

## Where can this be used?

Anywhere you use AI assistants repeatedly and want them
to get smarter about you over time:

- **Software projects** — remember build steps, coding style,
  deployment gotchas, and per-project setup across editors
  like Cursor, Claude Code, or Codex.
- **Multiple machines** — start work on a laptop, continue
  on a desktop, and have both assistants see the same notes.
- **Teams of agents** — let different assistants (say, a coding
  agent and a research agent) share one pool of lessons
  instead of each learning alone.
- **App builders** — apps that already keep their own chat
  history can feed past sessions in and get back searchable
  memory, skill, and resource updates.
- **Personal routines** — recurring tasks such as release
  checklists, writing templates, or data-cleaning recipes
  become one-line retrievals instead of re-inventions.

It already plugs into many popular hosts on macOS, Windows,
and Linux, and an auto-detect mode sniffs out session logs
for anything else.

## Conclusions & takeaways

memU is not another chatbot. It is the memory behind your
chatbots: a thin, readable, shared wiki that learns from
what you already do and pays it back as timely reminders.

Three ideas carry most of the design:

1. Small is a feature — a 500-line core plus plain-text notes
   beats a huge opaque system you cannot audit.
2. Two seams do all the work — record what happened, inject
   what matters — and everything else is plumbing.
3. One backend per machine keeps it sane — every assistant
   on the same computer reads and writes the same store,
   so knowledge compounds instead of fragmenting.

If you remember one sentence: memU lets your AI assistants
learn once from your history and remember together.

## Jargon decoder

| Term | What it really means |
| --- | --- |
| Wiki memory | A collection of short readable notes any assistant can look up, like a personal Wikipedia. |
| Skill | One reusable how-to note: a name, a description, and steps including traps to avoid. |
| Sidecar | A small helper program that runs alongside your main assistant and handles memory chores. |
| Record seam | The background habit of mining old chats and saving the useful bits. |
| Inject seam | The foreground habit of looking up saved notes before answering a new question. |
| Bridging task | The scheduled job that carries lessons from past sessions into the wiki. |
| Embedding | A way of turning text into numbers so similar meanings can be found by similarity. |
| Backend / store | Where the notes physically live: a throwaway cache, a local file, or a shared database. |
| Host adapter | The per-assistant connector that knows where that assistant keeps logs and settings. |
| Doctor check | A one-command health test that confirms settings and proves retrieval actually works. |
