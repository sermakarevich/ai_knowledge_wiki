> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# Andrew Southall | What Codex Actually Delivered in Truly Analytics — In Plain Language

## What is this about?

This is the story of one experienced engineer, Andrew Southall, building a real
product — Truly Analytics, a privacy-friendly replacement for Google Analytics —
from an empty folder to a working v1.0 in just six weeks.

His helper was Codex (the GPT 5.3-codex coding agent from OpenAI). Codex did not
work on its own. It worked inside a locked-down helper system that gave it code,
let it write new code, then put that code into a review request for the human to
accept or reject. It never touched secrets, the live database, or the main code
directly.

After launch, instead of guessing how useful the AI had been, Southall measured
the project's saved history (137 saved checkpoints, 21,031 lines of code written)
and asked a simple question: how much of the AI's code actually survived into the
finished product?

The headline answer: Codex wrote a lot (8,886 lines, about 42% of everything
written), but less than half of it survived (4,133 lines, a 46.5% survival rate).
The human wrote 12,145 lines and over 72% of those survived. In the final v1.0,
roughly one-third of the code is AI-written and two-thirds is human-written.

## Why does it matter?

Big companies often claim "most of our code is now AI-written." This project
tests that claim with real numbers from a finished, shipped product.

It shows the useful measure is not "how much code did the AI write?" but "how
much of that code was good enough to keep?" Over half of Codex's code was
replaced or deleted, mostly rewritten by the human. Very little human code
(only 4.5%) was rewritten by the AI.

In short: the AI was fast at producing first drafts, but the human did most of
the deciding, fixing, deleting, and finishing. That is a much more honest picture
of AI coding help than raw generation counts.

## How does it work?

Think of the setup in three parts: the guardrails, the scoreboard, and the
division of labour.

**The guardrails.** Every Codex contribution arrived as a review request (30 in
total). 25 were accepted, 5 rejected (about 1 in 6). Rejected ones included a
trivial styling-version change, a debugging attempt based on a wrong instruction
(400 lines added, almost nothing removed), one built on an out-of-date copy of
the code, and two cases of the AI over-complicating simple things — a timing
measurement feature and a trial-account check the human redid in about 10 minutes.

**The scoreboard.** Early on, the AI dumped in big chunks (two commits over 1,000
lines each). The human followed with even bigger commits that both added and
deleted a lot (one added 1,414 lines while deleting over 1,000). The pattern was
consistent: AI piles code in and rarely deletes; the human prunes boldly,
including one commit that deleted 900+ lines and added nothing.

**The division of labour.** Codex kept its work where the job was routine and
followed well-known patterns: server routes, database plumbing, short-term memory
(cache) handling, email sending, and the admin-panel screens. The human owned the
tricky and risky parts: the small analytics script sent to every visitor's
browser (which must be fast, tiny, and reliable), data cleaning and enrichment,
event handling, and all setup files for servers and deployments.

## Where can this be used?

This is a practical template for anyone using an AI coding assistant on a real
project:

- **Small routine pieces:** admin screens, standard server plumbing, boring
  boilerplate, first drafts of docs. Let the AI draft them, then review.
- **Breaking through a blank page:** when a project feels huge, an AI first draft
  gives you something to reshape instead of starting from nothing.
- **Throwaway and side tools:** research help, typing automation, one-off scripts,
  charts and analysis scaffolding.
- **Keep humans in charge of:** anything novel, customer-facing and
  performance-critical, security-sensitive, or load-bearing infrastructure. That
  is where judgment, product knowledge, and operational experience decide.
- **Always use guardrails:** an isolated workspace, review of every AI change,
  and no direct AI access to secrets or live systems. The author says he would
  not repeat the experiment without that pipeline.

The author also explains his tool choice: he stays with ChatGPT/Codex because his
saved instruction libraries are tuned for them. He rejects alternatives on
practical grounds and sees local models as a possible later step for private,
routine office work.

## Conclusions & takeaways

1. AI as accelerator, not replacement. Six weeks from zero to v1.0 was possible
   with AI help, but it was still the human's product, decisions, and clean-up.
2. Survival beats volume. 42% of lines written but only 32% of the shipped
   product tells the real story.
3. Routine work is the sweet spot. Conventional, widely-copied patterns survive;
   novel logic and tiny, fast browser code mostly had to be human-written.
4. Review everything. A ~17% rejection rate plus heavy rewriting of accepted
   code means unchecked AI output would have shipped bloat and bugs.
5. Guardrails turn a risk into a gain. Isolation and review "turned it into a
   gain" instead of a loss; without them one bad AI action could wipe out the
   benefit.
6. At $20/month, worth it — with eyes open. Great for momentum and tedious typing,
   not yet capable of independent, novel, sensible engineering on its own.

## Jargon decoder

| Term | What it means in plain language |
|---|---|
| Codex / coding agent | An AI helper that reads your code and writes new code for you, following your instructions. |
| Survival rate | Share of written lines still present in the finished v1.0; the rest was deleted or replaced. |
| Pull request (PR) | A packaged proposal: "here are my changes, please review and merge them in." |
| Isolated pipeline / wrapper | A safety cage: the AI works in a sealed copy and can only hand back code, never touch live systems or secrets. |
| Scaffolding / boilerplate | Standard, repetitive setup code that looks similar in every project. |
| ORM | A helper library that translates between database rows and program objects; here replaced by hand-written, AI-drafted plumbing. |
| Data enrichment | Cleaning up and adding useful context to raw collected data before storing or showing it. |
| Client analytics script | The tiny program sent to each visitor's browser to measure page views; must be fast and lightweight. |
| Kubernetes / Ansible manifests | Recipe files that describe how to set up and run servers automatically. |
| Over-engineering | Making a simple job far more complicated than it needs to be, hurting readability and maintenance. |
