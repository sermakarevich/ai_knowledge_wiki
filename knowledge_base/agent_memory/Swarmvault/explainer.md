> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# swarmclawai/swarmvault — In Plain Language

## What is this about?

SwarmVault is a tool that turns a messy pile of information into an organized, searchable notebook.

Imagine you have documents, code, meeting transcripts, notes, and web links scattered everywhere. SwarmVault reads all of that and builds two things: a set of interlinked markdown pages (a wiki) you can read, and a machine-readable map of ideas and how they connect (a knowledge graph).

It runs mostly on your own computer ("local-first"). You point it at a folder or a public GitHub repository, run one command, and it produces the wiki, the graph, and a visual overview you can share.

The simplest way to start needs no setup and no paid services:

```bash
npm install -g @swarmvaultai/cli
swarmvault quickstart ./your-repo
```

If you have nothing to feed it yet, `swarmvault demo` builds a sample vault so you can see what the output looks like. A helper command called `swarmvault next` then tells you what to do next: add material, rebuild, ask questions, or review new ideas.

## Why does it matter?

Most knowledge tools have one of three problems: they forget things, they mix up guesses with facts, or they fall apart once you add hundreds of pages.

SwarmVault is built to handle all three.

First, it remembers. Instead of answering from a single chat window that disappears, it saves everything as durable pages plus a graph, so knowledge compounds over time.

Second, it labels confidence. Every connection in the graph is marked as directly found in the sources, inferred by the software, or uncertain. It also flags contradictions and holds new or risky ideas in a staging area until you approve them.

Third, it is designed to scale. It combines fast keyword search with meaning-based search, keeps generated summaries within a fixed size budget, and offers graph questions like "how are A and B connected?" instead of dumping hundreds of pages on you.

Finally, it works offline on day one. A built-in simple extractor needs no API keys, and you can upgrade to a free local model or a cloud model later without changing your workflow.

## How does it work?

Think of SwarmVault as three shelves that work together.

**Shelf 1: raw sources.** Everything you ingest — files, code, transcripts, URLs — is copied unchanged into a `raw/` folder. This shelf is never edited, so you always have the originals.

**Shelf 2: the wiki.** The software reads the raw material and writes readable markdown pages into a `wiki/` folder: summaries of sources, pages for people and concepts, cross-references, dashboards, and ready-made context packs for AI assistants.

**Shelf 3: the schema.** A file called `swarmvault.schema.md` records the conventions: how pages should be organized, what matters most, and what the vocabulary of the domain is. It starts simple and improves over time as you and the tool refine it.

The typical loop looks like this:

1. **Ingest** — copy material in: `swarmvault ingest ./src`, `swarmvault add https://example.com/article`.
2. **Compile** — turn raw material into wiki pages and update the graph: `swarmvault compile`.
3. **Ask and explore** — search it: `swarmvault query "How does login work?"`, or open the visual map: `swarmvault graph serve`.
4. **Review** — check proposed new pages and approve or reject them, and run health checks with `swarmvault doctor` and conflict checks with `swarmvault lint --conflicts`.
5. **Refresh** — re-run ingestion and compilation as sources change, manually or on a schedule.

Under the hood, the graph is stored as `state/graph.json`, search indexes live in `state/retrieval/`, and quality controls (confidence labels, contradiction flags, approval bundles) sit between compilation and publication.

## Where can this be used?

Because the input can be almost anything — books, articles, notes, transcripts, emails, calendars, spreadsheets, slides, screenshots, URLs, code — the same pattern fits many jobs:

- **Personal notes:** turn years of scattered notes into one searchable wiki.
- **Research:** collect papers and articles on a topic and ask questions across all of them.
- **Book companions:** build a chapter-by-chapter guide with character, theme, and concept pages.
- **Code documentation:** map a codebase — what calls what, where the auth flow lives, which modules depend on which.
- **Team memory:** keep meeting transcripts, decisions, and docs in a shared vault backed by git.
- **AI assistant context:** generate bounded, relevant context packs so an agent starts a task already briefed instead of reading the whole repo.

Teams can sync vaults through git, run automatic refreshes on a schedule or file change, and let AI agents query the vault through a standard connector (an MCP server) or generated helper files.

## Conclusions & takeaways

- SwarmVault turns scattered sources into lasting knowledge: readable pages for humans plus a queryable graph for software.
- Its three-layer design (untouched originals, generated wiki, evolving conventions) keeps the system trustworthy as it grows.
- Confidence labels, contradiction detection, and an approval step are the core defense against confidently wrong answers.
- Search combines keywords with meaning, and output sizes are capped, so large vaults stay fast and usable.
- It starts free and offline with one command, then scales to teams and agents via git, scheduling, and AI integrations.
- If you remember one sentence: feed it messy inputs, get back an organized wiki plus a map of how everything connects.

## Jargon decoder

| Term | What it means in plain language |
|---|---|
| Vault | The working folder where SwarmVault keeps your sources, wiki pages, and graph. |
| Wiki | The readable output: interlinked markdown pages summarizing your material. |
| Knowledge graph | A map of things (people, concepts, files) and how they relate to each other. |
| Ingest | Copying new material into the vault without changing the original. |
| Compile | The step that reads ingested material and (re)builds wiki pages and the graph. |
| Schema | A short rulebook file describing how this vault should be organized. |
| Edge (extracted / inferred / ambiguous) | A single connection in the graph, labeled by confidence: found verbatim, guessed by software, or uncertain. |
| Candidate | A proposed new page held in a staging area until a human approves it. |
| Context pack | A small, fixed-size bundle of the most relevant pages for one task or question. |
| MCP server | A standard connector that lets AI assistants query the vault directly. |
| Hybrid search | Searching by both exact keywords and meaning (embeddings) at the same time. |
| Contradiction detection | Automatic flagging when two sources disagree with each other. |
