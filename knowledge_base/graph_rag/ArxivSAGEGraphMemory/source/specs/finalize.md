# Finalize task — SAGE paper (ArxivSAGEGraphMemory)

You are the last bead in an extraction chain for the KB folder
`/Users/sergii/.kb/papers/ArxivSAGEGraphMemory/`. This is the ONLY validation
step in the whole pipeline. Read `kb show summary/get` and
`kb show summary/get_local` if you need the full conventions; this spec
summarizes what you need.

Source: SAGE: A Self-Evolving Agentic Graph-Memory Engine for Structure-Aware
Associative Memory (Wang et al., 2026), https://arxiv.org/abs/2605.12061 — a
62-page paper (long paper tier: 5-8 wiki pages).

## Step 1: Completeness gate (self-rearm)

List all beads titled like "ArxivSAGEGraphMemory chunk NN extract" (any retry
suffix) — `fleet bd list` or `fleet bd search`. If ANY are still open/in-progress,
this run is premature:
- Create a successor finalize bead: `fleet bd create "ArxivSAGEGraphMemory finalize: verify + synthesize" --cwd /Users/sergii/.kb --coder claude --model sonnet -p 1 -t task --body-file /Users/sergii/.kb/papers/ArxivSAGEGraphMemory/source/specs/finalize.md --deps "<still-open bead ids>" --silent`
- Close your own bead: `bd close <own-id> --reason "rearmed as <new-id>: chunks still in flight"`
- Stop.

## Step 2: Verify every wiki page

Expected wiki pages (7 total), each covering the source chunk of the same number
(manifest: `/Users/sergii/.kb/papers/ArxivSAGEGraphMemory/source/chunks.json`):

1. `wiki/01-challenges-and-related-work.md` — Intro, Related Work, Preliminary
2. `wiki/02-method-writer-and-reader.md` — Method (writer + reader)
3. `wiki/03-experiments-and-conclusion.md` — Experiments, Conclusion
4. `wiki/04-appendix-writer-analysis-snr.md` — Appendix A, B
5. `wiki/05-appendix-calibration-stability-theory.md` — Appendix C-G
6. `wiki/06-appendix-ablations-and-implementation.md` — Appendix H-O
7. `wiki/07-appendix-additional-results-case-studies.md` — Appendix P

For each: check it exists, is non-trivial (>40 lines), matches the format
contract (headline sentence, Key points block, `---`, full detail, `**Covers:**`
footer), covers the WHOLE assigned chunk (spot-check the chunk's last major
topic against the chunk file, not just the opening), has no meta-junk or
repetition-loop garbage (read the file's TAIL, not just line count), and embeds
any named figure it discusses (figures live in `wiki/images/`, named
`NN-fig*.png`; chunks 01/02/03/04/05/07 each have one assigned image per
`chunks.json`). Build a BAD list and a GOOD list.

## Step 3: Handle BAD chunks

If BAD is empty, go to Step 4.

If BAD is non-empty, for each bad chunk NN:
- Count existing extract beads titled "ArxivSAGEGraphMemory chunk NN extract"
  (including retries) to get its attempt count. Retry budget = 3.
- Attempt count < 3: delete the bad wiki page, create ONE retry extract bead
  reusing `source/specs/NN-extract.md` verbatim:
  `fleet bd create "ArxivSAGEGraphMemory chunk NN extract (retry)" --cwd /Users/sergii/.kb --coder opencode --model ollama-rtx/qwen3.8:27b -p 2 -t task --body-file /Users/sergii/.kb/papers/ArxivSAGEGraphMemory/source/specs/NN-extract.md --silent`
  Record its id.
- Attempt count >= 3: exhausted — write that one page by hand from
  `source/chunks/NN.txt` (last resort only). Do not requeue it.

If any retries were created this round: create ONE successor finalize bead
depending on all of them (`--deps "<retry-id-1>,<retry-id-2>,..."`), close your
own bead with reason "rearmed as <new-id>: N chunk(s) requeued", and stop.

If every bad chunk was handled by hand-writing (nothing requeued), continue to
Step 4 in this same run.

## Step 4: Synthesize

Read all 7 wiki pages (small now — do not re-read the raw chunk files except to
spot-check quality) and produce, per `kb show summary/get` conventions, in
`/Users/sergii/.kb/papers/ArxivSAGEGraphMemory/`:

- `summary.md` — rung 1, whole paper, shallow (~2 min). Metadata line:
  `**Paper:** [SAGE: A Self-Evolving Agentic Graph-Memory Engine for Structure-Aware Associative Memory (Wang et al., 2026)](https://arxiv.org/abs/2605.12061)`
- `digest.md` — rung 2, built from each wiki page's headline + key points
  verbatim, in order, closing with "The argument in five moves".
- `index.md` — wiki hub with front-matter (`type: Paper`), orientation, reading
  ladder, wiki table (7 rows, reading order), Original Source section pointing
  to `source/full_text.md` and noting the PDF was not retained (see Gotchas).
- `explainer.md` — plain-language layer, 80-150 lines, jargon decoder (this
  paper: graph memory, GFM/graph foundation model reader, RL writer, structural
  gating, associative retrieval — decode these and any others used).
- `questions.md` — 8-12 retrieval-practice questions, answers in collapsed
  callouts, covering all 7 wiki pages evenly (including the appendix pages —
  do not concentrate all questions on Sections 1-3).
- `critical_thinking.md` — claims vs evidence, applicability, what it changes,
  verdict.
- `connections.md` — links to related entries in `/Users/sergii/.kb/ai_papers/graph_rag/`
  and other papers/ folders already in the KB dealing with GraphRAG / agent
  memory (search the KB for HippoRAG, GraphRAG, LightRAG, RAPTOR, and any
  recently-filed `Arxiv*` graph-memory papers under `papers/`).

Use `wiki/images/*-description.md` files (already generated) as the caption
source for any figure you reference in these synthesis files.

## Step 5: Report and close

Write a completion report to
`/Users/sergii/.kb/papers/ArxivSAGEGraphMemory/source/delegation_report.md`:
chunks total (7) / passed first try / requeued (how many rounds) / hand-written
after exhausting retries.

Then `bd close <own-id> --reason "wiki complete"`.

## Gotchas

- The original PDF was downloaded to `/tmp/sage.pdf` and is NOT stored in this
  repo (size-guard policy — PDFs are not committed to `.kb`). `source/full_text.md`
  (pymupdf4llm extraction) is the retained local copy; cite it as the
  `local-copy` source in `index.md` front-matter, and the arxiv URL as
  `original`.
- The paper is 62 pages, not 24 — `file /tmp/sage.pdf` under-reports; trust
  `fitz.open(...)` page count if you need to re-check anything.
- Figures: 6 were rasterized as full PDF pages at 200dpi (Figures 6 and 7 share
  one page image, `06-fig6-fig7-casestudy.png`). Raw embedded-image extraction
  via `page.get_images()` produced ~50 useless vector-icon fragments and was
  discarded — do not re-extract images from the PDF (which no longer exists
  locally anyway); the 6 PNGs in `wiki/images/` are the only figures available.
- No git commands anywhere in this pipeline — `.kb` auto-syncs.
