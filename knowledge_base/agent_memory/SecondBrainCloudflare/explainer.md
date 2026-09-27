> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# rahilp/second-brain-cloudflare — In Plain Language

## What is this about?

Second Brain is a personal memory service for AI assistants.

Normally, every AI app forgets you when the chat ends.
Claude does not know what you told ChatGPT.
Cursor does not know what you told Codex.

Second Brain fixes that by giving all of them one shared memory.

You save an idea, a decision, a preference, or a project note once.
Then any connected AI tool can look it up later.

It runs inside your own Cloudflare account, not on someone else's server.
You reach it two ways: through a normal web interface (a dashboard),
or directly from AI tools through standard connections.

Think of it like a notebook that all your AI assistants can read
and write in — with your permission, and under your control.

## Why does it matter?

Without a shared memory, you repeat yourself constantly.

You re-explain your project, your preferences, and your past decisions
to every new chat, every new tool, every new device.

That wastes time and causes mistakes.
The AI gives generic answers because it has lost your context.

A shared memory solves three everyday problems:

1. **No more repeating yourself.** Tell it once, every tool remembers.
2. **Answers fit you better.** The AI can look up what you decided,
   what you prefer, and what is already done.
3. **Nothing important slips.** Dated commitments — things you promised,
   deadlines you set — can surface again when they become due.

For teams, it matters for a second reason: knowledge stays visible.
Instead of decisions buried in one person's chat history,
the team keeps one place where shared facts live.

And because it lives in your own account, you keep ownership.
You can browse, fix, export, or permanently delete anything.

## How does it work?

The whole system is one small program running on Cloudflare.
Cloudflare is a company that runs code for people all over the world,
close to where they are. That program is called a Worker.

The Worker stores your memories in a few helpers around it:

- A database holds the actual memory texts.
- A meaning index lets it find memories by idea, not just exact words.
- A text index handles exact names, ticket numbers, and phrases.
- An AI helper reads, classifies, and compares new memories.
- A small key-value store keeps login and connection details.

When you save something, three steps happen:

1. **Capture.** You save from wherever you already work:
   an AI chat, a command line, a browser button, Obsidian, Notion,
   a calendar, an email, an iPhone shortcut, or the dashboard itself.
2. **Organize.** The system sorts the new memory, checks whether it
   is a duplicate, checks whether it contradicts something older,
   links it to related memories, and files it for later search.
3. **Recall.** When you ask a question in plain words, it finds
   the most relevant memories, follows useful links between them,
   and hands that context back to the AI so it can answer well.

Privacy is built into the shape of the system.
Each person has a private workspace nobody else can read.
There is also one shared team shelf.
A memory starts private and only moves to the shared shelf
when someone deliberately moves it there.
The original author stays visible, and only the author
or an administrator can change or remove it.

On a schedule, the system also tidies itself:
nightly cleanups, hourly imports from connected tools,
and optional weekly summaries of what changed.

If part of the meaning index is temporarily down,
saving and exact-word search keep working,
and the meaning index catches up later.

## Where can this be used?

Anywhere you want an AI assistant to remember context.

- **Daily personal use.** Preferences, ideas, reading notes,
  decisions, and reminders you want every AI tool to know.
- **Software projects.** What was decided, what is in progress,
  what is still an open question — kept per project.
- **Writing and research.** Notes captured from the browser,
  Obsidian, or Notion, then recalled later by meaning.
- **Deadlines and commitments.** Memories with dates attached,
  reviewed as overdue or upcoming, with phone reminders.
- **Team knowledge.** One shared shelf per team for facts
  everyone should see, like "we release on Thursdays."
- **Custom AI setups.** Fixed context cards ("prompt capsules")
  that place stable facts — who you are, your rules, your project's
  current state — in front of every AI request without stuffing
  every memory into every prompt.

Because every client talks to the same Worker,
there is nothing to copy or sync between apps and devices.

## Conclusions & takeaways

Second Brain is a simple idea done carefully:
one memory, shared by all your AI tools, owned by you.

The most important design choices are:

- Shared memory beats per-app memory. Context entered once
  is useful everywhere.
- Meaning search plus exact search covers both kinds of recall:
  "what did I mean?" and "what was the exact name or number?"
- Organizing at save time — sorting, deduplicating, linking —
  is what keeps the memory useful as it grows.
- Private by default, shared by choice, is what makes
  the team feature trustworthy.
- Running in your own account, with export and true delete,
  keeps you in control of your own knowledge.

If you use more than one AI tool, or work across more than
one device, this kind of shared memory removes a whole class
of repeated explanations and lost decisions.

## Jargon decoder

| Term | What it really means |
| --- | --- |
| Worker | A small program that runs on Cloudflare's computers instead of yours, always on and reachable over the internet |
| D1 | Cloudflare's built-in database — the filing cabinet where the memory texts live |
| Vectorize | A meaning index: it turns text into numbers so "release day" can match "when do we ship?" |
| Workers AI | Cloudflare's built-in AI helper used to read, sort, and compare memories |
| KV | A tiny key-value store — like a coat closet for login tokens and settings |
| MCP | A standard plug that lets AI tools talk to outside services such as this memory |
| Semantic search | Finding by meaning rather than exact words |
| Full-text index | Finding by exact words, names, numbers, and phrases |
| Workspace | Who can see a memory: just you (personal) or the whole team (shared) |
| Prompt capsule | A short, fixed summary card placed in front of an AI request: who you are, your rules, project state |
| PWA | A website saved to your phone so it behaves almost like a real app, including reminders |
