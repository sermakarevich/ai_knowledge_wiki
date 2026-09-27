> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# JetXu-LLM/DocMason — In Plain Language

## What is this about?
DocMason is a local helper for asking hard questions over your own work files.

You drop in the messy real-world stuff — slide decks, spreadsheets, PDFs,
Word docs, emails, Markdown notes — and it turns them into a tidy,
file-based knowledge base that lives in a folder on your machine.

When you ask a question, an AI agent (ChatGPT Work, Codex mode, or
Claude Code) reads that knowledge base and answers — but every claim
points back to the exact file and page it came from.

There is no hidden cloud service and no upload step. The folder of files
is the app; the agent is the engine.

In one line: put private documents in, get traceable answers out, all
on your own computer.

## Why does it matter?
Normal AI tools flatten your documents into plain text, and that flattening
loses meaning.

A slide's layout, a chart's labels, a presenter's notes, red text that
means "risk", indentation that means hierarchy, formulas that span several
spreadsheet tabs — all of that gets thrown away by simple copy-and-paste
or upload-and-chat pipelines.

That is how you get confident-sounding answers that quietly mix up sources
or invent facts spanning two documents.

DocMason exists because of one belief: answers over private work files
must be strictly traceable.

Instead of text blobs, it keeps structured "evidence bundles" that preserve
layout, visual cues, and cross-document links — so an answer like "the main
rollout risks are X, Y, Z" can show you exactly which documents support it.

It also matters for privacy: your corpus, the compiled knowledge base, and
the run history stay local and out of git by design.

## How does it work?
The workflow has five moves, in plain terms:

1. **Drop files in.** You put documents into a folder called `original_doc/`.
   Supported types include PDF, PowerPoint, Word, Excel, Markdown, plain
   text, email files, CSV, and similar everyday formats.
2. **Prepare the workspace.** On a first run you tell the agent something
   like "Please prepare the DocMason environment." It sets up a local
   Python environment and guides you to install LibreOffice, which is used
   to render Office files faithfully.
3. **Build the knowledge base.** For small piles of files this can happen
   automatically in the background when you ask your first question. For
   bigger collections you explicitly say "Please build the knowledge base,"
   and DocMason stages, compiles, validates, and publishes the evidence.
4. **Ask through one front door.** Ordinary questions all go through a
   single default route called `ask`. Setup, checkups, status, syncing,
   and log review are separate explicit routes you call by name.
5. **Get answers with receipts.** Replies carry exact source identity and
   a provenance trail — which file, which page, which evidence bundle —
   so you can verify the answer instead of taking it on faith.

Behind the scenes, strict rules keep this honest: deterministic processing,
validation-gated publishing (bad data fails the build rather than slipping
through), incremental sync when files change, and a review surface of logs
and saved answers under a `runtime/` folder.

DocMason itself makes no AI model calls and sends nothing over the network;
your agent host does the reasoning, under file-based contracts.

## Where can this be used?
Anywhere people drown in multi-file, multi-format office work:

- **Rollout and risk reviews.** Ask "what are the main rollout risks across
  these documents, and which sources support them?" over governance papers,
  proposals, and guidance — the demo use case is UK public-sector
  ICO + GCS materials.
- **Proposal synthesis.** Pull together multi-part proposals that are split
  across decks, spreadsheets, and emails into one coherent picture.
- **Compliance and audit checks.** Trace every statement back to its source
  file and page, which auditors and reviewers need.
- **Team knowledge bases.** Stage a whole department folder once, then let
  colleagues ask questions without re-reading everything.
- **Private research.** Work with sensitive documents that should never be
  uploaded to a cloud ingestion service.

It fits best on macOS with ChatGPT Desktop (Work/Codex) or Claude Code,
for small-to-large local corpora a team wants to question repeatedly.

## Conclusions & takeaways
DocMason's core idea is simple: the repo holds the truth, the agent does
the reasoning, and every answer must show its work.

It trades convenience (just upload and chat) for trust: local files only,
structured evidence instead of flat text, deterministic builds, failed
builds instead of silent bad data, and exact provenance on every answer.

The price is setup effort — environment prep, LibreOffice, an explicit
build step for large corpora — and a rule-bound workflow with one default
question route plus named operator routes.

If your problem is "too many private Office files, need answers I can
defend," that tradeoff makes sense. If you just want a quick summary of
one public file, it is overkill.

Bottom line: a local, evidence-first way to turn messy work files into
analyst-grade answers you can audit.

## Jargon decoder
| Term | What it actually means |
|---|---|
| Repo-native | The project folder itself is the app — files, folders, and scripts, not a remote server. |
| Knowledge base | The compiled, searchable copy of your documents that the agent answers from. |
| Evidence bundle | A structured package of text plus layout/visual context, richer than a plain-text extract. |
| Provenance | The receipt trail showing exactly which file and page each answer came from. |
| `original_doc/` | The inbox folder where you drop source files to be compiled. |
| `ask` route | The single default workflow for ordinary questions to the agent. |
| Validation-gated build | Bad or broken data fails the build instead of quietly producing weak answers. |
| Incremental sync | Only changed files get rebuilt and republished, not the whole collection. |
| Local-first / file-only | Everything runs on your machine with files; no cloud ingestion or hidden backend. |
| Source identity | A strict label tying each fact to its exact document origin. |
