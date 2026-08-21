# Task: Finalize ArxivHippoRAG wiki — verify all chunks, requeue/hand-write bad ones, synthesize remaining artifacts

This is the ONLY validation step in this pipeline. Follow this spec exactly. Paper: "HippoRAG: Neurobiologically Inspired Long-Term Memory for Large Language Models" (NeurIPS 2024), https://arxiv.org/abs/2405.14831. Folder: `/Users/sergii/.kb/papers/ArxivHippoRAG/`.

## Step 1: Completeness gate (self-rearm if premature)

List all beads matching `"ArxivHippoRAG chunk"` extract (`fleet bd search` or `fleet bd list` + grep — this also catches retry beads from an earlier finalize round). If ANY are still open/in-progress:
- Create a successor finalize bead with the same spec file (this file), `--deps <the still-open bead ids>`.
- Close own bead: `bd close <own-id> --reason "rearmed as <new-id>: chunks still in flight"`.
- Stop.

## Step 2: Verify every wiki page

Expected wiki pages (6 total), from `/Users/sergii/.kb/papers/ArxivHippoRAG/source/chunks.json`:
- `wiki/01-introduction.md`
- `wiki/02-methodology.md`
- `wiki/03-experiments-results.md`
- `wiki/04-discussions.md`
- `wiki/05-related-work-conclusion.md`
- `wiki/06-appendix-pipeline-errors.md`

For each: check it exists, is non-trivial (>40 lines), matches the format contract (backlink line, `**In one sentence:**`, `## Key points` block, `---`, full detail sections, footer `**Covers:**` line), covers the WHOLE chunk (spot-check against `source/chunks/NN.txt` — read the chunk's last major topic, not just its opening, and confirm the wiki page addresses it), has no meta-junk (no "as an AI...", no mention of the extraction task itself), and embeds every figure it names (chunks 01, 02 each need one figure; chunk 06 needs all 7 — check `![...](images/figureN.png)` references actually appear and the referenced PNG file exists in `wiki/images/`). Read the file's TAIL, not just its length — a known local-model failure mode is a repetition loop that pads line count with nonsense.

Build a BAD list and a GOOD list.

## Step 3: Handle BAD pages (if any)

If BAD is empty, go straight to Step 4.

For each bad chunk NN:
- Count existing extract beads titled `"ArxivHippoRAG chunk NN extract"` (any retry suffix) to get its attempt count. `RETRY_BUDGET` = 3 attempts (initial + 2 retries).
- Attempt count < 3: delete the bad `wiki/NN-*.md` page, create ONE retry extract bead reusing `source/specs/NN-extract.md` verbatim (`--coder opencode --model ollama-rtx/qwen3.8:27b`), record its id.
- Attempt count >= 3: this chunk has exhausted reprocessing. Write that one wiki page by hand from `source/chunks/NN.txt` (and its figure description files if any), following the same format contract as in `source/specs/NN-extract.md`. Do not requeue it.

If any retries were created this round: create ONE successor finalize bead depending on all of them (same spec = this file), close own bead with reason `"rearmed as <new-id>: N chunk(s) requeued"`, and stop.

If every bad chunk was handled by hand-writing (nothing requeued this round), continue to Step 4 in this same run.

## Step 4: Synthesize remaining artifacts

Read `kb show summary/get` for the exact specs of each file below (front-matter schema, wikilink rules, progressive-disclosure ladder). Read the wiki pages (small, already extracted) — not the raw source — except to spot-check quality against `source/full.md` or `source/chunks/*.txt` if something looks off.

Source type: **Paper**. Title: "HippoRAG: Neurobiologically Inspired Long-Term Memory for Large Language Models". Authors: Bernal Jiménez Gutiérrez, Yiheng Shu, Yu Gu, Michihiro Yasunaga, Yu Su. Venue: NeurIPS 2024. URL: https://arxiv.org/abs/2405.14831.

Produce:
1. `summary.md` — rung 1, whole paper, shallow (~2 min read). Metadata line: `**Paper:** [HippoRAG: Neurobiologically Inspired Long-Term Memory for Large Language Models (Gutiérrez et al., 2024)](https://arxiv.org/abs/2405.14831)`.
2. `digest.md` — rung 2, built by copying each wiki page's `**In one sentence:**` line and `## Key points` bullets verbatim, in order, plus a closing "## The argument in five moves" section (5-7 numbered steps).
3. `index.md` — wiki hub with the exact front-matter schema from `summary/get` (`type: Paper`, title, description, `generated: {by: claude/sonnet, at: <ISO-8601 UTC timestamp>}`, `sources:` with `id: original` → the arxiv URL and `id: local-copy` → `source/paper.pdf`, tags), orientation paragraph, reading ladder, and the wiki table (6 rows, reading order).
4. `explainer.md` — plain-language layer, 80-150 lines, 5-12 jargon-decoder terms (e.g. OpenIE, Personalized PageRank, node specificity, multi-hop QA, knowledge graph, hippocampal indexing theory).
5. `questions.md` — retrieval-practice questions with collapsed answers, at least one question per wiki page (6 pages → aim for 8-12 questions), even coverage across all pages.
6. `critical_thinking.md` — claims vs. evidence, applicability, what it changes, honest limitations (the paper's own Section 7 limitations plus your own assessment), verdict.
7. `connections.md` — links to related entries elsewhere in this KB. Check for existing GraphRAG-related entries under `/Users/sergii/.kb/papers/` (e.g. other GraphRAG papers already ingested — GraphRAG, LightRAG, Think-on-Graph, GraphRAG survey) and link to them with path-qualified wikilinks (e.g. `[[papers/ArxivGraphRAGSurvey/summary|GraphRAG Survey]]`) if such folders exist; note HippoRAG's relationship to RAPTOR, MemWalker, and Microsoft GraphRAG as discussed in `wiki/05-related-work-conclusion.md`.

All wikilinks use Obsidian `[[...]]` syntax per `summary/get` conventions. Every file starts with a backlink line to `index` and `summary` (except `index.md` and `summary.md` themselves per the convention).

## Step 5: Report and close

Write a completion report to `/Users/sergii/.kb/papers/ArxivHippoRAG/source/delegation_report.md`: chunks total (6) / passed first try / requeued (how many rounds) / hand-written after exhausting retries.

Then: `bd close <own-id> --reason "wiki complete"`.

No git commands anywhere in this task — `.kb` auto-syncs.

## Scope

Touch only files under `/Users/sergii/.kb/papers/ArxivHippoRAG/` and the fleet beads described above (retry/successor-finalize creation, own `bd close`).
