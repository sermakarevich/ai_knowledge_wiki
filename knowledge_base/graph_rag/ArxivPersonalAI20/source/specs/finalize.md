# Task: Finalize — verify + synthesize ArxivPersonalAI20

You are the finalize worker for a KB paper-summarization pipeline (`kb show summary/get_local`). This is the ONLY validation step in the whole run. Read `kb show summary/get` and `kb show summary/get_local` first for full conventions if unfamiliar — but the essential rules are repeated below.

**Paper:** PersonalAI 2.0: Enhancing knowledge graph traversal/retrieval with planning mechanism for Personalized LLM Agents (Menschikov et al., 2026). Source: https://arxiv.org/abs/2605.13481

**Folder:** `/Users/sergii/.kb/papers/ArxivPersonalAI20/`

**Config:** `WORKER_MODEL=ollama-rtx/qwen3.8:27b`, `RETRY_BUDGET=3` attempts per chunk (initial + 2 retries).

## Step 1: Completeness gate (self-rearm)

List all beads matching `"ArxivPersonalAI20 chunk"` extract (`fleet bd list` or `fleet bd search`, grep for the title pattern) — this also catches any retry beads created by an earlier finalize round. If ANY are still open/in-progress, this run is premature:
- Create a successor finalize bead: `fleet bd create "ArxivPersonalAI20 finalize: verify + synthesize" --cwd /Users/sergii/.kb --coder claude --model sonnet -p 1 -t task --body-file /Users/sergii/.kb/papers/ArxivPersonalAI20/source/specs/finalize.md --deps "<still-open bead ids>" --silent`
- Close own bead: `bd close <own-id> --reason "rearmed as <new-id>: chunks still in flight"`
- Stop.

## Step 2: Verify every wiki page

There are 8 expected wiki pages:
1. `wiki/01-introduction-and-related-work.md`
2. `wiki/02-methods-pai2-pipeline.md` (must embed `images/figure1-qa-pipeline.png`)
3. `wiki/03-experimental-setup-and-evaluation.md`
4. `wiki/04-experiments-and-results.md`
5. `wiki/05-conclusions-limitations-future-work.md`
6. `wiki/06-appendix-prompts-pipeline-stages.md`
7. `wiki/07-appendix-pseudocode-datasets-hyperparams-judge.md`
8. `wiki/08-appendix-graph-stats-ablations-mine1-humaneval.md` (must embed `images/figure2-mine1-distribution.png`)

For each: check it exists, is non-trivial (>40 lines), matches the format contract (backlink line, `**In one sentence:**`, `## Key points`, `---`, subsections, `**Covers:**` footer), covers the WHOLE chunk (spot-check against `source/chunks/NN.txt` — especially the chunk's LAST major topic, not just the opening), has no meta-junk ("As an AI..." preambles, repeated boilerplate), and embeds any named figures (pages 02 and 08). Read the file's TAIL, not just its length — a known local-model failure mode is a repetition loop that pads line count with nonsense.

Build a BAD list and a GOOD list.

## Step 3: Handle BAD pages

If BAD is empty, go straight to Step 4.

If BAD is non-empty: for each bad chunk NN, count existing extract beads titled `"ArxivPersonalAI20 chunk NN extract"` (any retry suffix) to get its attempt count.
- Attempt count < 3: delete the bad wiki page file, create ONE retry extract bead reusing `source/specs/NN-extract.md` verbatim: `fleet bd create "ArxivPersonalAI20 chunk NN extract (retry)" --cwd /Users/sergii/.kb --coder opencode --model ollama-rtx/qwen3.8:27b -p 2 -t task --body-file /Users/sergii/.kb/papers/ArxivPersonalAI20/source/specs/NN-extract.md --silent`. Record its id.
- Attempt count >= 3: this chunk has exhausted reprocessing — write that one page by hand from `source/chunks/NN.txt`, following the same format contract as its spec file. Do not requeue it.

If any retries were created this round: create ONE successor finalize bead depending on all of them (same command pattern as Step 1), close own bead with reason `"rearmed as <new-id>: N chunk(s) requeued"`, and stop.

If every bad chunk was handled by hand-writing (nothing requeued), continue to Step 4 in this same run.

## Step 4: Synthesize the remaining artifacts

Read the 8 wiki pages (small now — do not re-read the raw source except to spot-check quality) and produce every remaining artifact per `kb show summary/get` conventions, all directly under `/Users/sergii/.kb/papers/ArxivPersonalAI20/`:

- `summary.md` — rung 1, whole source, shallow (~2 min read). Metadata line: `**Paper:** [PersonalAI 2.0: Enhancing knowledge graph traversal/retrieval with planning mechanism for Personalized LLM Agents (Menschikov et al., 2026)](https://arxiv.org/abs/2605.13481)`.
- `digest.md` — rung 2, built by copying each wiki page's `**In one sentence:**` line and `## Key points` bullets verbatim, in order (pages 01–08), plus a closing `## The argument in five moves` section (5-7 numbered steps, one clause each).
- `index.md` — wiki hub with OKF-style front-matter (`type: Paper`, `title`, `description`, `generated: {by: claude/sonnet, at: <ISO-8601 UTC timestamp>}`, `sources` block with `original` = the arxiv URL above and `local-copy` = `source/` — note: no PDF binary is kept, see Gotcha below, so point `local-copy` at `source/chunks/`), `tags`, orientation paragraph, "How to work through this" ladder, "Read This Folder" list, a Wiki table (all 8 pages in order with one-line descriptions), and "Original Source" section.
- `explainer.md` — plain-language explainer (80-150 lines): what GraphRAG is, why iterative planning over a flat retriever matters, how the PAI-2 pipeline works step by step in plain terms, applications, conclusions, jargon decoder (5-12 terms e.g. GraphRAG, knowledge graph, LLM-as-a-Judge, BeamSearch, multi-hop QA, clue-query, MINE-1).
- `questions.md` — 8-12 retrieval-practice questions with collapsed answers (`<details><summary>Answer</summary>...</details>` or the KB's usual collapsed-callout convention), covering all 8 wiki pages evenly — do not cluster all questions on the main-body pages and skip the appendices.
- `critical_thinking.md` — claims vs. evidence, applicability, what it changes, verdict. Use the actual Limitations section (wiki page 05) as primary material — do not soften stated limitations.
- `connections.md` — links to related entries elsewhere in this KB. Search `/Users/sergii/.kb/papers/` and especially the `graph_rag` category (if it exists) for related GraphRAG papers (e.g. LightRAG, RAPTOR, HippoRAG, other agentic-GraphRAG papers ingested recently) and link them using path-qualified wikilinks, e.g. `[[graph_rag/SomePaper/summary|Some Paper]]`.

Follow wikilink rules from `kb show summary/get` (Obsidian `[[..]]` syntax, backlink line at top of every sub-file).

## Step 5: Report and close

Write a completion report to `/Users/sergii/.kb/papers/ArxivPersonalAI20/source/delegation_report.md`: chunks total (8) / passed first try / requeued (how many rounds) / hand-written after exhausting retries.

Then `bd close <own-id> --reason "wiki complete"`.

No git commands anywhere in this task — `.kb` auto-syncs on its own schedule.
