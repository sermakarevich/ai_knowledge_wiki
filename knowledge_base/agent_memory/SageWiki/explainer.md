> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# xoai/sage-wiki — In Plain Language

## What is this about?

sage-wiki is a tool that turns a pile of documents into an organized wiki.

You drop in papers, notes, code, emails, and other files. It reads them
and writes clear, linked articles in plain markdown that you can open
in Obsidian, a terminal dashboard, or a web browser.

At the same time it builds a knowledge graph: a map of the ideas inside
your documents and how they connect to each other.

Both people and AI assistants use the same wiki. People read the pages.
Assistants ask questions through 19 built-in tools and get answers with
citations pointing back to the source documents.

The whole thing ships as a single Go program. It can run on your laptop
or grow into a shared team or company knowledge base.

## Why does it matter?

Most knowledge is scattered across files nobody re-reads.

Plain search finds words that look alike, but it cannot answer questions
like "how do these ideas relate?" or "which document claimed this fact?"

sage-wiki matters because it keeps three things together:

- Readable articles a human can browse and edit.
- A map of relationships an assistant can walk across to answer
  multi-step questions.
- Proof for every answer: which document said it and how confident
  the system is.

Answers that have not been checked yet are kept separate until reviewed,
so untrusted output does not silently mix with trusted pages.

In short: instead of a folder of forgotten files, you get a living
reference that both you and your AI tools can share.

## How does it work?

The process has five simple moves.

1. **Drop in sources.** You copy files into a `raw/` folder, or point
   the tool at your existing notes vault.
2. **Compile.** The tool summarizes each source, pulls out the key ideas,
   and writes or updates linked articles. New sources enrich older
   articles instead of just piling up. Re-running the compile skips
   anything that has not changed.
3. **Optionally build the evidence graph.** Extra passes record typed
   facts such as "flash-attention improves self-attention," each with
   supporting text, a confidence score, and the source document. Similar
   names like "K8s" and "Kubernetes" can be merged, but only after a
   human reviews the suggestion.
4. **Ask questions.** Search blends three signals: matching words,
   matching meanings, and nearby ideas in the graph. Relationship
   questions are answered only from recorded facts, with one citation
   per fact.
5. **Share and grow.** One person can run it locally, a team can sync it
   over git or a self-hosted server, and a large organization can store
   it in a shared database with tiered processing for very large vaults.

Old facts are never silently overwritten: when a new document contradicts
an old one, the old link is marked outdated, and you can even ask what
the wiki believed at some date in the past.

## Where can this be used?

- **Personal research vault.** Collect papers and notes on one topic and
  get a linked reference you can search and question.
- **Team handbook.** Keep shared docs, decisions, and guides in one wiki
  that new members can browse and assistants can quote with sources.
- **Engineering memory.** Record how services, tools, and concepts relate,
  and trace any claim back to the document or code that introduced it.
- **Assistant memory layer.** Give a coding or chat assistant a reliable
  place to look things up, save what it learns, and improve over time.
- **Large collections.** Scale the same setup from a few dozen notes to
  tens of thousands of documents using shared storage and staged
  processing.

## Conclusions & takeaways

- sage-wiki is documents in, wiki plus knowledge map out.
- Humans and AI assistants read the same data through different doors:
  pages for people, tools with citations for assistants.
- Every important fact carries its source, so answers can be checked.
- Unchecked output is kept apart until a human or review step approves it.
- Name confusion is fixed openly: merges are proposed, then reviewed,
  never done silently.
- The design scales: one file-based setup on a laptop, shared servers
  for teams, database-backed installs for companies.
- The trade-off is extra processing: the richest features need
  additional automated passes over your documents.

## Jargon decoder

| Term | What it means in plain language |
|------|----------------------------------|
| Knowledge graph | A map of ideas and how they connect, not just a pile of pages. |
| Entity | One thing in that map, e.g. a tool, idea, or document. |
| Typed relation | A labeled link between two things, e.g. "improves" or "uses". |
| Evidence edge | A link that also stores the quote, source file, and confidence behind it. |
| Entity resolution | Noticing "K8s" and "Kubernetes" mean the same thing and merging them. |
| Hybrid search | Searching by matching words, matching meanings, and nearby map links at once. |
| MCP tools | Standard plugs that let an AI assistant search, read, and add to the wiki. |
| Compile pipeline | The automatic read-summarize-link routine that turns raw files into wiki pages. |
| Quarantine | Holding new answers aside until someone checks them. |
| Provenance | A record of which document each fact came from. |
