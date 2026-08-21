# Finalize task: verify + synthesize ArxivGraphRAGSurvey wiki

## Problem

Seven local-model workers have (or will have) each extracted one wiki page for the LLM-wiki folder `/Users/sergii/.kb/papers/ArxivGraphRAGSurvey/` from "Graph Retrieval-Augmented Generation: A Survey" (Peng et al., 2024, arXiv:2408.08921). This is the ONLY validation step in the whole pipeline -- no per-chunk validation happened. You must verify every page, retry/hand-write any bad ones, then synthesize the remaining artifacts.

Read `kb show summary/get` and `kb show summary/get_local` first for full conventions (output structure, file specs, wikilink rules, source-type labels) -- this spec only gives the finalize-specific steps and paths.

## Fix

### Step 1: Completeness gate (self-rearm)

List all beads matching `"ArxivGraphRAGSurvey chunk"` extract (`fleet bd list` or `fleet bd search`, grep for the title pattern) -- this also catches any retry beads created by an earlier finalize round. If ANY are still open/in-progress, this run is premature:
- Create a successor finalize bead: `fleet bd create "ArxivGraphRAGSurvey finalize: verify + synthesize" --cwd /Users/sergii/.kb --coder claude --model sonnet -p 1 -t task --body-file /Users/sergii/.kb/papers/ArxivGraphRAGSurvey/source/specs/finalize.md --deps "<the still-open bead ids>" --silent`
- Close your own bead: `bd close <own-id> --reason "rearmed as <new-id>: chunks still in flight"`
- Stop.

### Step 2: Verify every wiki page

The 7 expected wiki pages (see `/Users/sergii/.kb/papers/ArxivGraphRAGSurvey/source/chunks.json` for the chunk-to-page mapping and source section coverage):

```
wiki/01-introduction-and-related-work.md
wiki/02-preliminaries-and-framework.md
wiki/03-graph-based-indexing.md
wiki/04-graph-guided-retrieval.md
wiki/05-graph-enhanced-generation.md
wiki/06-training-applications-evaluation.md
wiki/07-future-directions-and-conclusion.md
```

For each: check it exists, is non-trivial (>40 lines), matches the format contract (backlink line, `# Topic`, `**In one sentence:**`, `## Key points` with 5-8 substantive bullets, `---`, hierarchical detail sections, `**Covers:**` footer), covers the WHOLE chunk (spot-check against the corresponding `source/chunks/NN.txt` file's LAST major topic, not just its opening -- read the file's TAIL, not just its length, since a known local-model failure mode is a repetition loop that pads line count with nonsense), and embeds any named figures (chunks 01-06 each have one figure listed in `chunks.json` under `images`; the file must exist at `wiki/images/<name>.png` and be referenced with `![...](images/<name>.png)` in the page). Build a BAD list and a GOOD list.

### Step 3: Handle BAD pages

If BAD is empty, go straight to Step 4.

If BAD is non-empty: for each bad chunk NN, count existing beads titled `"ArxivGraphRAGSurvey chunk NN extract"` (any retry suffix) to get its attempt count (RETRY_BUDGET = 3).

- Attempt count < 3: delete the bad wiki page file, create ONE retry extract bead reusing `/Users/sergii/.kb/papers/ArxivGraphRAGSurvey/source/specs/NN-extract.md` verbatim: `fleet bd create "ArxivGraphRAGSurvey chunk NN extract (retry)" --cwd /Users/sergii/.kb --coder opencode --model ollama-rtx/qwen3.8:27b -p 2 -t task --body-file /Users/sergii/.kb/papers/ArxivGraphRAGSurvey/source/specs/NN-extract.md --silent`. Record its id.
- Attempt count >= 3: exhausted -- write that one page by hand from `source/chunks/NN.txt`, following the same format contract embedded in that chunk's spec file. Do not requeue it.

If any retries were created this round: create ONE successor finalize bead depending on all of them (same `--body-file` as this spec), close your own bead with reason `"rearmed as <new-id>: N chunk(s) requeued"`, and stop. If every bad chunk was handled by hand-writing (nothing requeued), continue to Step 4 in this same run.

### Step 4: Synthesize the remaining artifacts

Per `kb show summary/get` conventions, using the now-verified wiki pages (read them, not the raw source, except to spot-check quality):

- `index.md` -- front-matter (`type: Paper`), orientation paragraph, "How to work through this" ladder, Read This Folder links, wiki table (7 rows, reading order), Original Source link to `source/2408.08921.pdf`.
- `summary.md` -- the A2-template structure. Metadata line: `**Paper:** [Graph Retrieval-Augmented Generation: A Survey (Peng et al., 2024)](https://arxiv.org/abs/2408.08921)`.
- `digest.md` -- copies each page's `**In one sentence:**` and `## Key points` verbatim, in order, plus a closing `## The argument in five moves`.
- `explainer.md` -- plain-language layer, 80-150 lines, 5-12 jargon-decoder terms.
- `questions.md` -- 8-12 retrieval-practice questions (Long paper tier), at least one per wiki page, answers only inside collapsed `> [!tip]-` callouts.
- `critical_thinking.md` -- skeptical appraisal ending in one of adopt/trial/watch/skip.
- `connections.md` -- read `/Users/sergii/.kb/ai_papers/index.md` and skim 2-3 plausible category files plus `ls /Users/sergii/.kb/papers/` for related entries (other GraphRAG-collection papers being ingested in parallel may not exist yet -- link to what's actually there, don't force it).

### Step 5: Report + close

Write a completion report to `/Users/sergii/.kb/papers/ArxivGraphRAGSurvey/source/delegation_report.md`: chunks total (7) / passed first try / requeued (how many rounds) / hand-written after exhausting retries.

Then `bd close <own-id> --reason "wiki complete"`.

## Tests

- `ls /Users/sergii/.kb/papers/ArxivGraphRAGSurvey/wiki/*.md` shows 7 files
- `ls /Users/sergii/.kb/papers/ArxivGraphRAGSurvey/*.md` shows index.md, summary.md, digest.md, explainer.md, questions.md, critical_thinking.md, connections.md
- `cat /Users/sergii/.kb/papers/ArxivGraphRAGSurvey/source/delegation_report.md` exists and reports counts

## DoD

1. All BAD chunks resolved (retried within budget or hand-written) before synthesis.
2. All 7 wiki pages + all top-level artifacts written.
3. `source/delegation_report.md` written.
4. `bd close <own-id> --reason "wiki complete"` -- never exit rc=0 without closing.

## Scope & constraints

- Touch ONLY files under `/Users/sergii/.kb/papers/ArxivGraphRAGSurvey/` and the beads you create/close.
- No git commands -- `.kb` auto-syncs.
- Do not run `fleet serve restart` or `fleet run`.
- cwd: /Users/sergii/.kb
