> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# vectorize-io/hindsight — In Plain Language

## What is this about?

Hindsight is a memory system for AI agents.

Most AI assistants forget everything between chats, or just scroll
back through old messages when they need something. Hindsight tries
something different: it helps agents actually learn over time, the way
a good assistant learns your preferences, your projects, and how you
like things done.

Instead of treating memory as a pile of old chat logs, it saves small
pieces of learned knowledge — facts about the world, facts about your
experience together, and bigger-picture patterns it has noticed.

Think of it this way: a normal chatbot is like a colleague with no
notebook who forgets you every Monday. An agent with Hindsight is like
a colleague who keeps a tidy notebook, reviews it before meetings, and
gets more useful the longer you work together.

## Why does it matter?

Forgetting is one of the biggest limits on useful AI agents.

Without long-term memory, you have to repeat yourself constantly: who
you are, what your project is, what you already decided. That gets
tiring fast, and it makes agents unreliable for work that stretches
over days or weeks.

Older fixes only go so far. Saving full chat history gets bulky and
noisy. Simple search over pasted documents often returns the wrong
passage. Hand-built webs of facts are powerful but fiddly to maintain.

Hindsight matters because it claims a better trade-off: learning that
is automatic, searchable, and tested. Its headline evidence is a top
score on LongMemEval, a benchmark for long-term memory, with the
results independently reproduced by collaborators at Virginia Tech and
The Washington Post. It is also reported to be running in production
at large companies and AI startups, not just as a research demo.

## How does it work?

The core idea is simple, even if the machinery underneath is complex.

Everything revolves around three actions, applied inside a separate
memory box called a bank:

1. Retain — save something worth remembering, like "Alice works at
   Google as a software engineer."
2. Recall — search those memories later with a plain question, like
   "Where does Alice work?"
3. Reflect — ask for an answer shaped by what the agent knows, rather
   than just a list of matching notes.

You talk to Hindsight through a small server. You can start that
server with Docker, install it directly on a machine, run it on
Kubernetes, or skip hosting entirely and use a managed cloud version.
The server exposes an API on one port and a visual dashboard on
another, so you can inspect what the agent remembers.

Agents connect to that server from the language they already use:
Python, JavaScript, Go, a command-line tool, or a plain web API. There
is also an embedded mode that runs everything inside your own program
with no separate server, which is handy for laptops and small scripts.

The laziest — and most popular — route is the wrapper. You keep writing
normal AI code, but you swap in a wrapped version of your usual client.
From then on, every call automatically saves useful memories and pulls
relevant ones back in, with per-request knobs for which memory box to
use, how much to retrieve, and whether to reflect instead of recall.
Under the hood this covers over a hundred models.

Behind the scenes, the repository pins down all the boring-but-important
details: which AI provider and model to use, how strict or creative
each step should be, how to handle images versus text, and how to fail
over between models. Memories themselves live in a database with
search-friendly storage, and every database change ships in two flavors
so both PostgreSQL and Oracle enterprise setups stay in step.

## Where can this be used?

Anywhere an agent needs to remember you across sessions.

A coding assistant can remember your stack, your style rules, and past
fixes instead of re-learning them each session. A support or sales
agent can remember who a customer is and what was already promised.
A research helper can build up a picture of a topic over many chats.

Setup effort scales with your needs. Solo developers can run the
embedded mode or a local Docker container in minutes. Teams can share
one hosted server with separate memory banks per user or project.
Larger shops can deploy to Kubernetes with backups, dashboards, and
enterprise database support.

Adoption is eased by more than sixty ready-made integrations with
popular coding tools and agent frameworks, most needing no code
changes, plus a docs helper that installs with a single command.

## Conclusions & takeaways

The one-line takeaway: Hindsight turns agent memory from replaying old
chats into accumulating useful knowledge.

Three things to remember: it organizes memory around learning rather
than raw history; it packages that learning as a server plus clients
plus an automatic wrapper, so teams can start small and grow; and it
backs its accuracy claims with public benchmark numbers and independent
reproduction rather than vibes alone.

The trade-off is operational: to get memory that improves over time,
you run one more service, pick models and settings, and curate what
gets saved. For throwaway chats that is overkill. For ongoing work with
the same agent, that is exactly the point.

## Jargon decoder

| Term | What it means in plain language |
|---|---|
| Agent memory | The agent's ability to carry knowledge from one chat to the next |
| Bank | A separate labeled memory box, e.g. one per user or project |
| Retain | Saving a useful fact into a bank |
| Recall | Searching a bank for relevant memories |
| Reflect | Answering in a way shaped by those memories, not just listing them |
| World fact | General knowledge, like where someone works |
| Experience fact | Something learned from working with you specifically |
| Mental model | A bigger-picture pattern the agent builds up over time |
| Embedding | A number-based fingerprint that lets the system find similar meanings |
| Benchmark | A standard test used to compare accuracy, speed, and cost fairly |
