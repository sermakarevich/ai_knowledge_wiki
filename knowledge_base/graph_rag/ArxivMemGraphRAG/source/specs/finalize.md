# Finalize: verify all extracted wiki chunks and synthesize the ArxivMemGraphRAG KB folder

## Problem
Four wiki-page chunks for the paper "MemGraphRAG: Memory-based Multi-Agent System for Graph
Retrieval-Augmented Generation" (arXiv 2606.00610, Wu et al., 2026-05) have been extracted by
a local model into `/Users/sergii/.kb/papers/ArxivMemGraphRAG/wiki/`. You are the ONLY
validation step in this pipeline. You must verify each page, requeue/hand-write any bad ones,
and then synthesize the remaining KB artifacts.

Read `kb show summary/get` for the full output conventions (front-matter, wikilink rules,
digest/explainer/questions/critical_thinking/connections specs) before synthesizing.

Output folder (fixed, do not change): `/Users/sergii/.kb/papers/ArxivMemGraphRAG/`

## Step 1: Completeness gate (self-rearm)

List all beads matching `"ArxivMemGraphRAG chunk"` extract (`fleet bd list` or `fleet bd
search`, grep on title) — this also catches any retry beads created by an earlier finalize
round. If ANY are still open/in-progress, this run is premature:
- Create a successor finalize bead: `fleet bd create "ArxivMemGraphRAG finalize: verify + synthesize" --cwd /Users/sergii/.kb --coder claude --model sonnet -p 1 -t task --body-file /Users/sergii/.kb/papers/ArxivMemGraphRAG/source/specs/finalize.md --deps "<the still-open bead ids, comma separated>" --silent`
- Close your own bead: `bd close <own-id> --reason "rearmed as <new-id>: chunks still in flight"`
- Stop.

## Step 2: Verify every wiki page

Expected pages (all under `/Users/sergii/.kb/papers/ArxivMemGraphRAG/wiki/`):
1. `01-motivation-and-problem.md` — covers Abstract, Sec 1, Sec 2, Sec 3
2. `02-memgraphrag-framework.md` — covers Sec 4, Sec 5
3. `03-conclusion-and-additional-experiments.md` — covers Sec 6, Appendix A
4. `04-related-work-and-appendix.md` — covers Appendix B-F

For each: check it exists, is non-trivial (>40 lines), matches the format contract (backlink
line, `# Title`, `**In one sentence:**`, `## Key points` with 5-8 substantive bullets, `---`,
then full detail with subsections), covers the WHOLE chunk (spot-check the chunk's LAST major
topic by reading the corresponding `source/chunks/NN.txt` tail — not just the wiki page's
length), has no meta-junk (no "as an AI" text, no repetition loops padding line count — read
the file's TAIL, not just line count), and embeds its assigned figure(s) as
`![...](images/...)` (see `source/chunks.json` for the exact figure-to-page mapping). Build a
BAD list and a GOOD list.

## Step 3: Handle BAD pages

If BAD is empty, go straight to Step 4.

If BAD is non-empty, for each bad chunk NN:
- Count existing extract beads titled `"ArxivMemGraphRAG chunk NN extract"` (any retry
  suffix) to get its attempt count. `RETRY_BUDGET` = 3.
- Attempt count < 3: delete the bad page file, create ONE retry extract bead reusing
  `source/specs/NN-extract.md` verbatim: `fleet bd create "ArxivMemGraphRAG chunk NN extract retry" --cwd /Users/sergii/.kb --coder opencode --model ollama-rtx/qwen3.8:27b -p 2 -t task --body-file /Users/sergii/.kb/papers/ArxivMemGraphRAG/source/specs/NN-extract.md --silent`. Record its id.
- Attempt count >= 3: this chunk has exhausted reprocessing. Write that one page by hand
  from `source/chunks/NN.txt` (and its figure description files per `chunks.json`),
  following the same format contract as the extract specs. Do not requeue it.

If any retries were created this round: create ONE successor finalize bead depending on all
of them (`--deps "<retry-id-1>,<retry-id-2>,..."`, same command as Step 1's rearm), close your
own bead with reason `"rearmed as <new-id>: N chunk(s) requeued"`, and stop. If every bad
chunk was handled by hand-writing (nothing requeued), continue to Step 4 in this same run.

## Step 4: Synthesize the remaining KB artifacts

Read the 4 wiki pages (small now — do not re-read the raw chunks except to spot-check
quality) and produce, per `kb show summary/get` conventions:

- `index.md` — wiki hub with front-matter (`type: Paper`, title, description, `generated: {by:
  claude/<model-id>, at: <ISO-8601 UTC>}`, sources (arxiv URL + local PDF path), tags), the
  reading ladder, and the wiki table (4 rows, in reading order: motivation → framework →
  conclusion → related work).
- `summary.md` — rung 1, whole paper, shallow (~2 min). Metadata line:
  `**Paper:** [MemGraphRAG: Memory-based Multi-Agent System for Graph Retrieval-Augmented Generation (Wu et al., 2026)](https://arxiv.org/abs/2606.00610)`
- `digest.md` — rung 2, built by copying each wiki page's `**In one sentence:**` line and
  `## Key points` bullets verbatim, in order, plus a closing "The argument in five moves"
  section (5-7 numbered steps).
- `explainer.md` — plain-language layer, no jargon, analogy-first, 80-150 lines, 5-12 term
  jargon decoder table.
- `questions.md` — 6-8 retrieval-practice questions covering all 4 wiki pages evenly, answers
  in collapsed `<details>` callouts, never answered in-session.
- `critical_thinking.md` — claims vs. evidence, applicability (note: this is an AI/ML paper
  about GraphRAG — assess practical applicability generically, not to any specific company),
  what it changes, verdict.
- `connections.md` — links to related entries elsewhere in the KB. Search
  `/Users/sergii/.kb/papers/` and `/Users/sergii/.kb/graph_rag/` (if it exists) for other
  GraphRAG/agentic-RAG papers already ingested and link to them with path-qualified wikilinks,
  e.g. `[[graph_rag/SomePaper/summary|Some Paper]]`.

Wikilink and front-matter rules, folder scaffold, and file templates are all specified in `kb
show summary/get` — follow them exactly.

## Step 5: Report and close

Write a completion report to
`/Users/sergii/.kb/papers/ArxivMemGraphRAG/source/delegation_report.md`: chunks total (4) /
passed first try / requeued (how many rounds) / hand-written after exhausting retries.

Then close: `bd close <own-id> --reason "wiki complete"`.

## Scope & constraints
- Touch ONLY files under `/Users/sergii/.kb/papers/ArxivMemGraphRAG/` and the beads described
  above.
- No git commands — `.kb` auto-syncs.
- Do not run `fleet serve restart` or `fleet run`.
- Do not touch other papers' folders or other tasks' beads.
