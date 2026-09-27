> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# AgriciDaniel/claude-obsidian — In Plain Language

## What is this about?

Imagine you ask an AI assistant to research a topic, and a week later
you cannot tell which answer came from which source — or whether any
of it was even true. This project fixes that problem.

claude-obsidian is a system that turns source material — articles,
files, notes — into a personal knowledge base inside Obsidian, the
popular note-taking app. Every note it creates points back to the
source it came from, and every important claim records how confident
the system is, what supports it, and what contradicts it.

Think of it like a careful research assistant with a strict rule:
never throw away the evidence, never hide uncertainty, and never
rearrange your filing cabinet without asking first.

The whole thing is local-first. Your notes live as ordinary files on
your own computer — plain Markdown text you can read, copy, and back
up yourself. Nothing is locked in a cloud database or hidden inside
a plugin. Going online (for web research, for example) is always a
separate, explicit decision, never something that happens silently.

## Why does it matter?

Most AI answers are disposable: helpful in the moment, then gone, and
impossible to check later. That creates three everyday pains:

- You forget where an answer came from and cannot verify it.
- Contradictions get smoothed over instead of staying visible.
- Each new chat starts from zero instead of building on what you
  already collected.

This project matters because it treats knowledge as something that
should compound. Each time you use it, the vault — your collection
of linked notes — should get more useful, not messier. Sources are
kept before anything is summarized, so the summary never replaces
the evidence. Doubt stays on the page: unsupported claims and
disagreements between sources remain visible instead of being
quietly dropped.

It also matters for trust. When several AI helpers work at once,
they can overwrite each other's notes. Here they are not allowed to:
helpers only propose drafts, and one coordinator reviews and applies
a single safe update. If anything goes wrong halfway through, the
previous state can be restored.

## How does it work?

The work follows a simple loop with four steps:

1. **Keep the source.** You drop material into a visible inbox folder,
   and the system stores an unchangeable copy with a fingerprint
   (a SHA-256 hash) before writing any summary.
2. **Check the claims.** Two record books — a source ledger and a
   claim ledger — track who said what, how fresh it is, what backs
   it up, what argues against it, and whether anyone has reviewed it.
3. **Connect the ideas.** Notes are linked together into indexes,
   topic maps, and visual Canvas boards, filed by the method you
   prefer (simple folders, topic maps, project-based, or atomic
   linked notes).
4. **Reuse what you know.** Later questions are answered from the
   notes already in the vault, and regular check-ups (linting,
   rollups) keep links, indexes, and history healthy.

Safety comes from a "one job, one safe update" rule. Each change is
planned first: the system records what it expects each file to look
like, bundles all edits into one package, lets you inspect and
approve it, and only then applies it once — reporting exactly what
changed. A changed file mid-operation counts as a conflict, never a
silent overwrite.

Day to day you drive it with short commands (called skills): one to
bring sources in, one to ask questions using only vault evidence, one
to save a single insight, one to check the vault's health, plus
extras for web research, visual maps, and search. Setup also previews
every step before applying it, and the vault is always chosen
explicitly — if the system is unsure which vault you mean, it stops
rather than writing to the wrong place.

## Where can this be used?

- **Personal research library.** Collect readings on a topic and get
  answers that cite the notes they came from.
- **Study and writing projects.** Keep people, ideas, terms, and open
  questions as linked notes that grow over months.
- **Team or community knowledge.** Share a folder of plain files where
  claims carry their evidence and review state with them.
- **AI-assisted workflows.** Let parallel helpers draft in safety while
  one coordinator applies a single reviewed update.
- **Long-lived reference.** Reuse past work — queries, summaries, and
  history logs — instead of re-asking from scratch every session.

What it is not: it does not record transcripts automatically, sync to
a cloud, guarantee facts are true, or replace your own backups. High
stakes claims need two independent sources, and the system prefers an
honest "I cannot prove this" over a made-up citation.

## Conclusions & takeaways

- Keep the evidence, not just the summary — durable sources make
  every later answer checkable.
- Show uncertainty on the page — support, contradiction, and review
  state are part of the note, not hidden.
- Make knowledge compound — file, link, query, and tidy in one loop
  so the vault improves with use.
- Guard every change — one reviewed, recoverable update beats many
  silent overwrites, especially with parallel helpers.
- Stay local and explicit — ordinary files, clear vault choice, and
  opt-in online steps keep you in control.

## Jargon decoder

| Term | What it means in plain language |
|---|---|
| Vault | Your knowledge folder: ordinary notes and files on your computer. |
| Inbox | The visible intake tray where new source material lands first. |
| Content-addressed copy | An unchangeable stored copy, filed under its fingerprint. |
| Source ledger | The record book of where each source came from and how fresh it is. |
| Claim ledger | The record book of each claim, its support, doubts, and review state. |
| Transaction | One planned, reviewed, recoverable update applied all at once. |
| SHA-256 hash | A unique fingerprint of a file's contents used to detect changes. |
| Lint | An automated health check for broken links, orphans, and stale pages. |
| Map of Content | A curated overview page that links a topic's key notes together. |
| Skill | A named command, such as ingest, query, or save, that does one job. |
