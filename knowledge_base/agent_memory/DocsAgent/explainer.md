> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# docsagent/docsagent — In Plain Language

## What is this about?

DocsAgent is a small helper that lets an AI assistant search your own
research library — the papers, books, and notes you keep in Zotero.

Normally an assistant like Claude or Cursor can only see the web or the
files you paste in. DocsAgent changes that: it connects the assistant
directly to the thousands of PDFs sitting on your own computer, so you
can ask questions and get answers quoted from your own collection.

Think of it like giving the assistant a private librarian who knows
exactly where everything on your shelves is.

Nothing is uploaded anywhere. The whole thing runs on your machine,
and your library never leaves it.

## Why does it matter?

Anyone who does serious reading quickly drowns in PDFs. You remember
reading something, but not where — which paper, which page, which note.

Web search cannot help, because these are your private files. Asking a
chatbot cannot help either, because it has never seen your library and
may simply make up an answer.

DocsAgent solves that gap. It gives the assistant fast, honest access
to what you actually own, with page-level quotes it can cite.

It also matters because it is fast and light. Searching more than a
thousand papers takes about 15 milliseconds — far quicker than a blink.
It uses only around 160–230 MB of memory, so it can sit quietly in the
background on an ordinary laptop.

Finally, it is careful with changes: reading is always allowed, but
adding or editing library entries is switched off unless you opt in.

## How does it work?

There are three pieces, and each does one job.

**1. The engine: a fast reader that lives on your computer.**

A small program written in C++ reads your Zotero folder directly — the
database file plus the stored PDFs. It builds its own index, which is
like the index at the back of a textbook: for every word, a list of
where it appears.

When you ask a question, it ranks matching passages with a proven
method called BM25. In plain terms: rare, distinctive words count more
than common ones, and short, focused matches beat long rambling ones.
You get back the best few paragraphs, not whole books.

This engine runs once in the background and stays running, even when
you close and reopen your assistant.

**2. The translator: a shell the assistant can talk to.**

AI assistants cannot talk to the engine directly. They speak a common
plug-in language for assistants. DocsAgent provides a translator — one
version in TypeScript, one in Python — that exposes 8 simple actions:

- Look up what sources exist (always call this first).
- Search across everything by keywords, with filters for tags, years,
  authors, or item type.
- Read one entry, either as best passages or as full text page by page.
- Fetch details: summary, abstract, highlights, notes, or a ready-made
  citation.
- Browse by collection, tag, saved search, or loose notes.
- Three optional write actions: import a new PDF, add a note, or tidy
  up many items at once.

Every request is checked against a strict shape, duplicate results are
removed, and long answers are trimmed to fit the assistant's budget.

**3. The safety rules.**

Write actions have three locks. First, they do not even appear unless
you turn them on. Second, an unconfirmed request only returns a preview
— "here is what I would do" — without doing anything. Third, confirmed
changes are limited to about 30 per hour, so a confused assistant
cannot wreck your library.

For everyday use you start the engine, then tell your assistant where
the translator is. After that, questions like "what do my papers say
about local encryption?" just work.

## Where can this be used?

- **Literature reviews.** Ask across your whole collection at once
  instead of opening papers one by one.
- **Writing papers.** Pull exact quotes and ready-made citations in
  standard formats without retyping references.
- **Studying notes.** Search your own highlights and margin notes,
  not just the papers themselves.
- **Organising a messy library.** Import new PDFs by file or by
  identifier, add notes, and retag or refile many items in bulk.
- **Working offline.** Because everything is local, it works on a
  plane, in a lab, or anywhere you would not send private files to
  the cloud.
- **Team and remote setups.** It can also run over a network with
  logins and per-user permissions, plus a health check, so a lab
  server can serve one shared engine.
- **Any assistant that speaks the plug-in language.** That includes
  Claude Desktop, Cursor, Cline, Qwen Code, and similar tools.

## Conclusions & takeaways

DocsAgent is not a chatbot and not a search engine for the web. It is
the missing link between the assistant you already use and the library
you already own.

The big ideas are simple: keep your data on your machine, make search
so fast you forget it is there, let any assistant plug in through one
shared contract, and make dangerous actions hard to trigger by accident.

If you remember one sentence: it turns "I know I read that somewhere"
into an answered, quoted question in milliseconds — privately.

## Jargon decoder

| Term | What it really means |
|---|---|
| Zotero | A free app researchers use to collect papers, books, and notes in one library. |
| MCP (Model Context Protocol) | A standard plug-in language that lets assistants call outside tools. |
| MCP server / shell | The translator program that offers the 8 library actions to the assistant. |
| Resident engine / core | The background search program that stays running and answers in milliseconds. |
| BM25 ranking | A scoring recipe: rare matching words count more than common ones. |
| Passage retrieval | Returning the best paragraphs, not whole documents. |
| Inverted index | A word-to-location list, like a book index, so search skips reading everything. |
| Token budget | A cap on answer length so results fit what the assistant can handle. |
| Write safety gate | The three locks (opt-in, preview first, hourly limit) that protect your library. |
| Transport (stdio / HTTP) | How the assistant reaches the tool: directly on your machine, or over a network. |
