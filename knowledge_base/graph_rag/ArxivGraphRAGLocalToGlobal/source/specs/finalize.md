# Task: Finalize ArxivGraphRAGLocalToGlobal — verify + synthesize

You are the last bead in a fleet extraction chain for the paper "From Local to Global: A Graph RAG Approach to Query-Focused Summarization" (Edge et al., Microsoft Research, 2024), source https://arxiv.org/abs/2404.16130. Five local-model workers each extracted one wiki page from a chunk of the source PDF into:

```
/Users/sergii/.kb/papers/ArxivGraphRAGLocalToGlobal/wiki/01-introduction-and-background.md
/Users/sergii/.kb/papers/ArxivGraphRAGLocalToGlobal/wiki/02-graphrag-methodology.md
/Users/sergii/.kb/papers/ArxivGraphRAGLocalToGlobal/wiki/03-experimental-setup-and-results.md
/Users/sergii/.kb/papers/ArxivGraphRAGLocalToGlobal/wiki/04-discussion-and-conclusion.md
/Users/sergii/.kb/papers/ArxivGraphRAGLocalToGlobal/wiki/05-appendix-prompts-and-additional-experiments.md
```

You are the ONLY validation step in this pipeline. Read `kb show summary/get_local` and `kb show summary/get` for full context on the conventions below if anything here is ambiguous.

Manifest of what each chunk covers: `/Users/sergii/.kb/papers/ArxivGraphRAGLocalToGlobal/source/chunks.json`
Extract specs (reuse verbatim if requeuing): `/Users/sergii/.kb/papers/ArxivGraphRAGLocalToGlobal/source/specs/NN-extract.md`
Figure images already extracted: `/Users/sergii/.kb/papers/ArxivGraphRAGLocalToGlobal/wiki/images/*.png` with matching `*-description.md` vision descriptions.

WORKER_MODEL = `ollama-rtx/qwen3.8:27b`, RETRY_BUDGET = 3 attempts per chunk.

## Step 1: Completeness gate (self-rearm)

List all beads matching `"ArxivGraphRAGLocalToGlobal chunk" extract` (`fleet bd search` or `fleet bd list` + grep) — this also catches any retry beads created by an earlier finalize round. If ANY are still open/in-progress, this run is premature:
- Create a successor finalize bead: `fleet bd create "ArxivGraphRAGLocalToGlobal finalize: verify + synthesize" --cwd /Users/sergii/.kb --coder claude --model sonnet -p 1 -t task --body-file /Users/sergii/.kb/papers/ArxivGraphRAGLocalToGlobal/source/specs/finalize.md --deps "<the still-open bead ids>" --silent`
- Close your own bead: `bd close <own-id> --reason "rearmed as <new-id>: chunks still in flight"`
- Stop.

## Step 2: Verify every wiki page

For each of the 5 wiki pages: check it exists, is non-trivial (>40 lines), matches the format contract (backlink line, `# Title`, `**In one sentence:**` line, `## Key points` block with 4-8 substantive bullets, `---`, full-detail subsections, footer `**Covers:**` line), covers the WHOLE chunk (spot-check the chunk's last major topic per `chunks.json`, not just the opening), has no meta-junk ("as an AI...", repeated boilerplate), and embeds any figures listed in `chunks.json` for that chunk (`images/*.png` markdown embeds actually present, not just named).

Read the file's TAIL, not just its length — a known local-model failure mode is a repetition loop that pads line count with nonsense.

Build a BAD list and a GOOD list.

## Step 3: Handle BAD pages

If BAD is empty, go straight to Step 4.

If BAD is non-empty: for each bad chunk NN, count existing extract beads titled `"ArxivGraphRAGLocalToGlobal chunk NN extract"` (any retry suffix) to get its attempt count.
- Attempt count < 3 (RETRY_BUDGET): delete the bad `wiki/NN-*.md` page, create ONE retry extract bead reusing `source/specs/NN-extract.md` verbatim: `fleet bd create "ArxivGraphRAGLocalToGlobal chunk NN extract (retry)" --cwd /Users/sergii/.kb --coder opencode --model ollama-rtx/qwen3.8:27b -p 2 -t task --body-file /Users/sergii/.kb/papers/ArxivGraphRAGLocalToGlobal/source/specs/NN-extract.md --silent`. Record its id.
- Attempt count >= 3: this chunk has exhausted reprocessing — write that one wiki page by hand yourself, reading `source/chunks/NN.txt` directly, following the same format contract in `source/specs/NN-extract.md`. Do not requeue it.

If any retries were created this round: create ONE successor finalize bead depending on all of them (same command pattern as Step 1), close your own bead with reason `"rearmed as <new-id>: N chunk(s) requeued"`, and stop.

If every bad chunk was handled by hand-writing (nothing requeued), continue to Step 4 in this same run.

## Step 4: Synthesize the rest of the KB folder

Per `kb show summary/get` conventions, produce (reading the wiki pages — small now — not the raw source, except to spot-check quality against `source/graphrag_2404.16130.pdf` or the chunk texts if something seems off):

- `summary.md` — rung 1, whole paper, shallow (~2 min read). Metadata line: `**Paper:** [From Local to Global: A Graph RAG Approach to Query-Focused Summarization (Edge et al., 2024)](https://arxiv.org/abs/2404.16130)`
- `digest.md` — rung 2, built from wiki pages' `**In one sentence:**` lines and `## Key points` bullets verbatim, in order, plus a closing "## The argument in five moves" synthesis section
- `index.md` — wiki hub with OKF front-matter (`type: Paper`, title, description, `generated: {by: claude/sonnet, at: <ISO-8601 UTC timestamp>}`, sources (original URL + local-copy path `source/graphrag_2404.16130.pdf`), 2-5 tags e.g. `[graphrag, rag, knowledge-graphs, query-focused-summarization, sensemaking]`), orientation paragraph, reading ladder, wiki table listing all 5 pages in order
- `explainer.md` — plain-language explanation (80-150 lines): what GraphRAG is via analogy, why global sensemaking queries break vector RAG, how the pipeline works step by step in plain terms, where it can be used, conclusions, and a jargon decoder table (5-12 terms: RAG, sensemaking, knowledge graph, community detection, Leiden algorithm, map-reduce summarization, community summary, LLM-as-judge, etc.)
- `questions.md` — 6-8 retrieval-practice questions spanning Bloom's taxonomy, answers in collapsed callouts, with front-matter `type: Retrieval Prompts`, `last_reviewed: null`, `review_count: 0`. Ensure even coverage across all 5 wiki pages — do not draw all questions from the first two pages.
- `critical_thinking.md` — critical appraisal: claims vs. evidence (e.g. only 2 datasets, GPT-4-turbo only, no ablation isolating community detection choice, LLM-as-judge potential bias), applicability, what it changes, verdict
- `connections.md` — links to related GraphRAG-category entries in this KB if any exist yet (check `/Users/sergii/.kb/papers/` and any `graph_rag` category index for sibling papers — e.g. HippoRAG, LightRAG, Think-on-Graph, if present); if the category doesn't exist yet or has no siblings, note that plainly rather than inventing links

Use Obsidian `[[wikilink]]` syntax throughout per the wikilink rules in `kb show summary/get`. Every sub-file starts with its backlink line.

## Step 5: Report and close

Write a completion report to `/Users/sergii/.kb/papers/ArxivGraphRAGLocalToGlobal/source/delegation_report.md`: chunks total (5) / passed first try / requeued (how many rounds) / hand-written after exhausting retries.

Then: `bd close <own-id> --reason "wiki complete"`

No git commands anywhere in this task — `.kb` auto-syncs.

## Scope

Touch only files under `/Users/sergii/.kb/papers/ArxivGraphRAGLocalToGlobal/`, plus `fleet bd` commands for beads related to this chain.
