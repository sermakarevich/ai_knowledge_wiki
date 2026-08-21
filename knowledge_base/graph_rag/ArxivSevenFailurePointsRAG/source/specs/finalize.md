# Task: finalize — verify + synthesize "Seven Failure Points When Engineering a Retrieval Augmented Generation System"

You are the last bead in a fleet chain building an LLM-wiki KB folder for an academic paper. You are the ONLY validation step in this pipeline. Follow this spec exactly; it is self-contained.

## Paper metadata
- Title: Seven Failure Points When Engineering a Retrieval Augmented Generation System
- Authors: Scott Barnett, Stefanus Kurniawan, Srikanth Thudumu, Zach Brannelly, Mohamed Abdelrazek (Deakin University, Applied AI Institute)
- Venue: CAIN 2024 (3rd International Conference on AI Engineering — Software Engineering for AI)
- Year: 2024
- URL: https://arxiv.org/abs/2401.05856
- Source type: `Paper`

## Folder
`/Users/sergii/.kb/papers/ArxivSevenFailurePointsRAG/`
- `source/paper.pdf`, `source/full_text.md` — original artifacts, already in place
- `source/chunks/01.txt` — the paper's full text (single chunk; short paper)
- `wiki/images/01-figure1-rag-pipeline.png` + `wiki/images/01-description.md` — Figure 1 (RAG indexing/query pipeline) already extracted
- Expected wiki pages (one per extract bead):
  - `wiki/01-background-and-rag-pipeline.md`
  - `wiki/02-case-studies.md`
  - `wiki/03-seven-failure-points.md`
  - `wiki/04-lessons-and-future-research.md`
- Extract spec files (reuse verbatim if a chunk needs retry): `source/specs/01-extract.md` .. `source/specs/04-extract.md`
- WORKER_MODEL for any retries: `ollama-rtx/qwen3.8:27b`, coder `opencode`
- RETRY_BUDGET: 3 attempts per chunk

## Step 1: Completeness gate (self-rearm)
List all beads matching `"ArxivSevenFailurePointsRAG chunk" extract` (e.g. `fleet bd search` or `fleet bd list` + grep on title). This also catches any retry beads a prior finalize round may have created.
- If ANY matching bead is still open/in-progress: this run is premature. Create a successor finalize bead reusing this exact spec file, with `--deps` set to the still-open bead id(s). Close your own bead with reason `"rearmed as <new-id>: chunks still in flight"`. Stop here.
- If all four are closed, proceed to Step 2.

## Step 2: Verify every wiki page
For each of the 4 expected wiki pages, check:
- File exists and is non-trivial (>40 lines).
- Matches the format contract: backlink line, `# Title`, `**In one sentence:**` line, `## Key points` (5-8 substantive bullets), `---`, then full detail with source-mirroring subsections, footer `**Covers:** ...` line.
- Covers the WHOLE assigned scope — read the file's TAIL, not just its length, to check the last subsection is actually present and coherent (a known local-model failure mode is a repetition loop that pads line count with nonsense near the end).
- Page 1 (`01-background-and-rag-pipeline.md`) embeds Figure 1 via `![...](images/01-figure1-rag-pipeline.png)` — this is mandatory since the page discusses it by name.
- Page 3 (`03-seven-failure-points.md`) actually names and details all 7 failure points, not fewer.
- No meta-junk (no "as an AI language model", no leftover instructions from the spec, no empty subsections).

Build a GOOD list and a BAD list.

## Step 3: Handle BAD pages (if any)
If BAD is empty, skip to Step 4.

For each bad page, count existing extract beads titled `"ArxivSevenFailurePointsRAG chunk NN extract"` (including retries) to get its attempt count:
- Attempt count < 3: delete the bad wiki page file, create ONE retry extract bead reusing the corresponding `source/specs/NN-extract.md` file verbatim (`--coder opencode --model ollama-rtx/qwen3.8:27b`), record its id.
- Attempt count >= 3: exhausted. Write that one page by hand yourself, following the same format contract, reading `source/chunks/01.txt` directly for that page's assigned section scope (see the corresponding extract spec for scope). Do not requeue it.

If any retries were created this round: create ONE successor finalize bead (reuse this spec file) depending on all newly-created retry bead ids, close your own bead with reason `"rearmed as <new-id>: N chunk(s) requeued"`, and stop. If every bad page was instead hand-written (nothing requeued), continue to Step 4 in this same run.

## Step 4: Synthesize the remaining artifacts
Read the 4 wiki pages (small, ~40-150 lines each) — not the raw PDF/full_text.md, except to spot-check something specific. Follow `kb show summary/get` conventions exactly for each of the following (front-matter, wikilinks, backlinks, progressive-disclosure rules):

1. **`index.md`** — wiki hub. Front-matter `type: Paper`. `sources:` block: `id: original` → `https://arxiv.org/abs/2401.05856`, `id: local-copy` → `source/paper.pdf`. Wiki table listing all 4 pages in reading order.
2. **`summary.md`** — rung 1, whole paper, shallow (~2 min read). Metadata line: `**Paper:** [Seven Failure Points When Engineering a Retrieval Augmented Generation System (Barnett et al., 2024)](https://arxiv.org/abs/2401.05856)`.
3. **`digest.md`** — rung 2, built by copying each wiki page's `**In one sentence:**` line and `## Key points` bullets verbatim, in order, plus a closing "The argument in five moves" section (5-7 numbered steps, synthesis).
4. **`explainer.md`** — plain-language layer, no jargon, analogies, 80-150 lines, jargon decoder table (RAG, chunking, embeddings, reranker, hallucination, vector database, etc.).
5. **`questions.md`** — 6-8 retrieval-practice questions with collapsed-answer callouts, front-matter `type: Retrieval Prompts`, `last_reviewed: null`, `review_count: 0`. Even coverage across all 4 wiki pages — at least one question per page.
6. **`critical_thinking.md`** — claims vs evidence (note this is an experience report / practitioner case-study paper, not a controlled benchmark study — 3 case studies, qualitative), applicability, what it changes, honest verdict.
7. **`connections.md`** — links to related entries elsewhere in this KB. Search `/Users/sergii/.kb/papers/` and `/Users/sergii/.kb/` broadly for other RAG/GraphRAG papers already ingested (e.g. GraphRAG survey, LightRAG, HippoRAG, GraphRAG-Bench if present) and link to them with path-qualified wikilinks, e.g. `[[papers/ArxivGraphRAGSurvey/summary|GraphRAG Survey]]`. If none exist yet, say so plainly rather than inventing links.

Use `date` on the shell to get today's date for `generated: { by: claude/sonnet, at: <ISO-8601 UTC timestamp> }` in `index.md`'s front-matter — do not guess it.

## Step 5: Report + close
Write a completion report to `source/delegation_report.md`: chunks total (4) / passed first try / requeued (how many rounds, if any) / hand-written after exhausting retries (if any).

Then `bd close <own-bead-id> --reason "wiki complete"`.

## Constraints
- No git commands anywhere in this task — `.kb` auto-syncs.
- Touch only files under `/Users/sergii/.kb/papers/ArxivSevenFailurePointsRAG/` and the beads you create/close.
- Do not run `fleet serve restart` or `fleet run`.
