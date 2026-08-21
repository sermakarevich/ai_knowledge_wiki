# Task: Finalize ArxivHiGram — verify wiki pages, requeue if needed, synthesize remaining artifacts

This is the ONLY validation step in the ArxivHiGram summarization pipeline. Follow it exactly.

Paper: "HiGram: Hierarchical Graph Memory for LLM Agents with Path-level Localization and Rewrite" (Yue et al., 2026-08). Source: https://arxiv.org/abs/2608.05095
Output folder: `/Users/sergii/.kb/papers/ArxivHiGram/`

## Step 1: Completeness gate (self-rearm)

List all beads titled matching `"ArxivHiGram chunk"` and `"extract"` (`fleet bd list` or `fleet bd search`, grep for "ArxivHiGram chunk"). This also catches any retry beads created by an earlier finalize round.

If ANY of these beads are still open/in-progress: this run is premature.
- Create a successor finalize bead: `fleet bd create "ArxivHiGram finalize: verify + synthesize" --cwd /Users/sergii/.kb --coder claude --model sonnet -p 1 -t task --body-file /Users/sergii/.kb/papers/ArxivHiGram/source/specs/finalize.md --deps "<the still-open bead ids, comma separated>" --silent`
- Close own bead: `bd close <own-id> --reason "rearmed as <new-id>: chunks still in flight"`
- Stop.

## Step 2: Verify every wiki page

Expected pages (see `/Users/sergii/.kb/papers/ArxivHiGram/source/chunks.json` for the authoritative chunk→page mapping):
- `wiki/01-hierarchical-memory-and-method.md` (from chunk 01)
- `wiki/02-experiments-and-results.md` (from chunk 02)

For each: check it exists, is non-trivial (>40 lines), matches the format contract in the corresponding `source/specs/NN-extract.md` (headline sentence → key-points block → full detail), covers the WHOLE chunk (spot-check the chunk's LAST major topic — e.g. page 01 must cover section 3.3 Coordinated Rewriting, not just the introduction; page 02 must cover the Conclusion, not just Table 1), has no meta-junk, and embeds the figure(s) listed for that chunk in `chunks.json`. Read the file's TAIL, not just its line count — a known local-model failure mode is a repetition loop that pads line count with nonsense.

Build a BAD list and a GOOD list.

## Step 3: Handle BAD pages (if any)

If BAD is empty, go straight to Step 4.

If BAD is non-empty: for each bad chunk NN, count existing extract beads titled `"ArxivHiGram chunk NN extract"` (including any retry suffix) to get its attempt count.
- Attempt count < 3 (RETRY_BUDGET): delete the bad page, create ONE retry extract bead reusing `source/specs/NN-extract.md` verbatim: `fleet bd create "ArxivHiGram chunk NN extract (retry)" --cwd /Users/sergii/.kb --coder opencode --model ollama-rtx/qwen3.8:27b -p 2 -t task --body-file /Users/sergii/.kb/papers/ArxivHiGram/source/specs/NN-extract.md --silent`. Record its id.
- Attempt count >= 3: this chunk has exhausted reprocessing — write that one page by hand from `source/chunks/NN.txt` (last resort only). Do not requeue it.

If any retries were created this round: create ONE successor finalize bead depending on all of them (same command pattern as Step 1), close own bead with reason `"rearmed as <new-id>: N chunk(s) requeued"`, and stop.

If every bad chunk was handled by hand-writing (nothing requeued), continue to Step 4 in this same run.

## Step 4: Synthesize remaining artifacts

Read `kb show summary/get` for the exact conventions (front-matter schema, wikilink rules, progressive-disclosure rungs, source-type labels) and follow them precisely. Produce, reading the wiki pages (not the raw source, except to spot-check quality):

- `index.md` — wiki hub. `type: Paper`. Front-matter `sources` should list `id: original` → `https://arxiv.org/abs/2608.05095` and `id: local-copy` → `source/chunks/` (no single local PDF copy is kept; note the two chunk files). Table of contents links to both wiki pages.
- `summary.md` — rung 1, whole paper, shallow (~2 min read). Metadata line: `**Paper:** [HiGram: Hierarchical Graph Memory for LLM Agents with Path-level Localization and Rewrite (Yue et al., 2026-08)](https://arxiv.org/abs/2608.05095)`.
- `digest.md` — rung 2, derived from the wiki pages' own headline + key-points blocks verbatim (do not write new content here).
- `explainer.md` — plain-language explanation for someone unfamiliar with graph-based agent memory: what problem HiGram solves, how it works intuitively (hierarchy + localization + coordinated rewrite), why it matters.
- `questions.md` — 6-8 retrieval-practice questions with collapsed answers, covering both wiki pages roughly evenly.
- `critical_thinking.md` — claims vs. evidence (only 2 benchmarks, both apparently authors' own/adjacent; baselines' fairness; ablation strength; generalization beyond LoCoMo/MemConflict), applicability, what it changes, verdict.
- `connections.md` — links to related entries elsewhere in this KB. Search `/Users/sergii/.kb/papers/` (grep -il for "graph" "memory" "agent" "RAG" in existing paper folders, e.g. any existing GraphRAG / agent-memory papers already filed) and link using the `[[Folder/summary|Title]]` convention. If nothing relevant is found, say so explicitly rather than inventing links.

## Step 5: Report and close

Write `/Users/sergii/.kb/papers/ArxivHiGram/source/delegation_report.md`:
- chunks total: 2
- passed first try: <N>
- requeued (how many rounds): <N>
- hand-written after exhausting retries: <N>

Then: `bd close <own-id> --reason "wiki complete"`

No git commands anywhere in this task — `.kb` auto-syncs.
