# Finalize: ARES paper wiki — verify + synthesize

## Problem
This is the last bead in a fleet chain that summarized the paper "ARES: An Automated
Evaluation Framework for Retrieval-Augmented Generation Systems" (Saad-Falcon, Khattab,
Potts, Zaharia; NAACL 2024; https://arxiv.org/abs/2311.09476) into an LLM-wiki folder at
`/Users/sergii/.kb/papers/ArxivARESRAGEvaluation/`. Local-model workers wrote 5 wiki pages
from source chunks. This bead is the ONLY validation step in the whole pipeline, then
synthesizes the remaining top-level files.

## Context
- Folder: `/Users/sergii/.kb/papers/ArxivARESRAGEvaluation/`
- Expected wiki pages (5): `wiki/01-introduction-and-related-work.md`,
  `wiki/02-ares-method.md`, `wiki/03-experimental-setup.md`,
  `wiki/04-results-and-analysis.md`, `wiki/05-appendix-details.md`
- Chunk manifest: `source/chunks.json` (maps each chunk to its wiki page and topic)
- Extract specs (reuse verbatim for any retry): `source/specs/01-extract.md` through
  `source/specs/05-extract.md`
- Figure images already extracted: `wiki/images/01-fig1-overview.png`,
  `wiki/images/02-fig2-3-nq-eval.png` (with `wiki/images/01-description.md` and
  `wiki/images/02-description.md` as reference vision-model descriptions)
- Original PDF and full extracted text: `source/paper.pdf`, `source/raw_text.txt`
- `WORKER_MODEL` for any retries: `ollama-rtx/qwen3.8:27b` via
  `--coder opencode --model ollama-rtx/qwen3.8:27b`
- `RETRY_BUDGET`: 3 attempts per chunk (initial + 2 retries)
- Source-type metadata for `index.md` / `summary.md`: `type: Paper`,
  `**Paper:** [ARES: An Automated Evaluation Framework for Retrieval-Augmented Generation
  Systems (Saad-Falcon et al., 2024)](https://arxiv.org/abs/2311.09476)`

## Fix — do these steps in order

### 1. Completeness gate (self-rearm)
List all beads matching "ArxivARESRAGEvaluation chunk" extract (`fleet bd list` or
`fleet bd search`, filtered by title). If ANY are still open/in-progress, this run is
premature:
- Create a successor finalize bead with the same spec file (`--body-file
  /Users/sergii/.kb/papers/ArxivARESRAGEvaluation/source/specs/finalize.md`), `--deps`
  set to the still-open bead id(s), `--coder claude --model sonnet -p 1 -t task --cwd
  /Users/sergii/.kb --silent`.
- Close this bead: `bd close <own-id> --reason "rearmed as <new-id>: chunks still in
  flight"`.
- Stop.

### 2. Verify every wiki page
For each of the 5 expected wiki pages: check it exists, is non-trivial (>40 lines),
matches the format contract (backlink line, `**In one sentence:**`, `## Key points` with
5-8 bullets, `---` divider, `**Covers:**` footer), covers the WHOLE chunk (spot-check
against the chunk's LAST major subsection listed in `chunks.json`'s `topic` field, not
just the opening), has no meta-junk (no "as an AI" text, no leftover instructions), and
embeds its named figure if `chunks.json` lists one for that chunk (`01-fig1-overview.png`
for chunk 02 / wiki page 02, `02-fig2-3-nq-eval.png` for chunk 05 / wiki page 05). Read
the file's TAIL, not just its length — a known local-model failure mode is a repetition
loop that pads line count with nonsense.

Build a BAD list and a GOOD list.

### 3. Handle BAD pages
If BAD is empty, go straight to step 4.

If BAD is non-empty, for each bad chunk NN:
- Count existing extract beads titled "ArxivARESRAGEvaluation chunk NN extract" (any
  retry suffix) to get its attempt count.
- Attempt count < 3 (RETRY_BUDGET): delete the bad wiki page file, create ONE retry
  extract bead reusing `source/specs/NN-extract.md` verbatim (`--coder opencode --model
  ollama-rtx/qwen3.8:27b -p 2 -t task --cwd /Users/sergii/.kb --body-file
  /Users/sergii/.kb/papers/ArxivARESRAGEvaluation/source/specs/NN-extract.md --silent`),
  record its id.
- Attempt count >= 3: this chunk has exhausted reprocessing — write that one wiki page by
  hand yourself from `source/chunks/NN.txt`, following the same format contract used in
  the extract specs. Do not requeue it.

If any retries were created this round: create ONE successor finalize bead depending on
all of them (`--deps "id1,id2,..."`), close own bead with reason "rearmed as <new-id>: N
chunk(s) requeued", and stop. If every bad chunk was handled by hand-writing (nothing
requeued), continue to step 4 in this same run.

### 4. Synthesize the remaining artifacts
Once all 5 wiki pages pass, read them (they are small — do NOT re-read the raw source
except to spot-check a specific claim) and produce, per `kb show summary/get`
conventions:

- **`index.md`** — OKF-style hub with the exact front-matter keys (`type: Paper`, title,
  description, `generated: {by: claude/<model-id>, at: <ISO-8601 UTC timestamp>}`,
  `sources:` with `id: original` → the arxiv URL and `id: local-copy` →
  `source/paper.pdf`, `tags:`), orientation paragraph, the three-rung reading ladder, and
  the wiki table (5 rows, reading order).
- **`summary.md`** — rung 1, whole paper, shallow, ~2 min read. Metadata line: `**Paper:**
  [ARES: An Automated Evaluation Framework for Retrieval-Augmented Generation Systems
  (Saad-Falcon et al., 2024)](https://arxiv.org/abs/2311.09476)`.
- **`digest.md`** — rung 2, built by copying each wiki page's `**In one sentence:**` line
  and `## Key points` bullets verbatim, in reading order (01 through 05), plus a closing
  "The argument in five moves" section (5-7 numbered steps).
- **`explainer.md`** — plain-language layer, no jargon, 80-150 lines, 5-12 term
  jargon-decoder table (e.g. RAG, LLM judge, PPI, context relevance, answer faithfulness,
  KILT, DeBERTa, FLAN-T5).
- **`questions.md`** — 8-12 retrieval-practice questions (this paper is a long
  paper/report at 17 pages), at least one per wiki page, mixing core recall / elaboration
  / transfer, plus one evaluation question drawing on `critical_thinking.md`. Answers in
  collapsed `> [!tip]-` callouts, each linking its covering wiki page. Front-matter:
  `type: Retrieval Prompts`, `last_reviewed: null`, `review_count: 0`.
- **`critical_thinking.md`** — skeptical-expert critique: claims vs. evidence (the
  headline accuracy-vs-RAGAS numbers, the AIS attribution accuracy, and whether the
  KILT/SuperGLUE/AIS benchmark choices and the ~150-datapoint validation-set size are
  adequate), genuinely new vs. repackaged (vs. RAGAS, EXAM, generic LLM-as-judge),
  weaknesses/blind spots (English-only scope, compute requirements, reliance on
  FLAN-T5/DeBERTa staying representative of modern RAG judge needs), applicability
  (including 2-4 bullets on relevance to Sergii's AI/ML engineering and agentic-systems
  work), what this changes, and a verdict ending in one of adopt/trial/watch/skip.
- **`connections.md`** — read `/Users/sergii/.kb/ai_papers/index.md`, skim
  `/Users/sergii/.kb/ai_papers/*/*.md` category files and `ls /Users/sergii/.kb/papers/`
  for related RAG/GraphRAG/evaluation entries (this paper is part of a GraphRAG top-10
  collection currently being ingested — look for sibling entries like ArxivLightRAG,
  ArxivGraphRAGBench, ArxivRAGvsGraphRAG, or similar RAG-evaluation entries), and link
  2-6 genuinely related entries with the relationship explained in 1-2 sentences each. If
  none found, say so explicitly with today's date.

Embed figures inline in the wiki pages only (already done by the extract workers) — do
not re-embed images in the top-level files.

### 5. Report + close
Write a completion report to
`/Users/sergii/.kb/papers/ArxivARESRAGEvaluation/source/delegation_report.md`: chunks
total (5) / passed first try / requeued (how many rounds) / hand-written after exhausting
retries. Then `bd close <own-id> --reason "wiki complete"`.

## No git commands
`.kb` auto-syncs — do not run any git commands in this task.

## Scope & constraints
- Touch ONLY files under `/Users/sergii/.kb/papers/ArxivARESRAGEvaluation/`.
- Do not run `fleet serve restart` or `fleet run`.
- Do not touch any other paper's folder or any other task's beads.

## DoD
1. All 5 wiki pages pass verification (directly or after hand-writing).
2. `index.md`, `summary.md`, `digest.md`, `explainer.md`, `questions.md`,
   `critical_thinking.md`, `connections.md` all written under
   `/Users/sergii/.kb/papers/ArxivARESRAGEvaluation/`.
3. `source/delegation_report.md` written.
4. `bd close <own-id> --reason "wiki complete"`.
