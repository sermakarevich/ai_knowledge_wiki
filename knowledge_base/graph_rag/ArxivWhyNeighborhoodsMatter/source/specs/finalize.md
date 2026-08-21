# Task: finalize ArxivWhyNeighborhoodsMatter — verify + synthesize wiki

## Problem
An LLM-wiki summary of the paper "Why Neighborhoods Matter: Traversal Context and Provenance in
Agentic GraphRAG" (Terrenzi, von Zastrow, Ayvaz; arXiv 2605.15109, 2026-05) is being built at
`/Users/sergii/.kb/papers/ArxivWhyNeighborhoodsMatter/`. Four extract beads (one per section) write
the wiki pages under `wiki/`. This task is the ONLY validation step and the final synthesis step.

Read `kb show summary/get` and `kb show summary/get_local` for full conventions before proceeding —
follow them for everything not spelled out below (index.md front-matter, digest.md structure,
wikilink rules, source-type labels — this is `type: Paper`).

## Fix — do these steps in order

### Step 1: Completeness gate (self-rearm)
List all beads titled like `"ArxivWhyNeighborhoodsMatter chunk NN extract"` (use `fleet bd list` or
`fleet bd search`, grep for the title prefix) — this also catches any retry beads created by an
earlier finalize round. If ANY are still open/in-progress, this run is premature:
1. Create a successor finalize bead: same spec file (`source/specs/finalize.md`), `--coder claude`,
   `--model sonnet`, `--deps <the still-open bead ids>`.
2. Close own bead: `bd close <own-id> --reason "rearmed as <new-id>: chunks still in flight"`.
3. Stop — do not proceed to Step 2 in this run.

### Step 2: Verify every wiki page
The four expected pages:
- `wiki/01-introduction-and-motivation.md`
- `wiki/02-experimental-design-and-studies.md`
- `wiki/03-results-and-discussion.md`
- `wiki/04-conclusion-and-limitations.md`

For each: check it exists, is non-trivial (>40 lines), contains `**In one sentence:**` and
`## Key points`, covers the WHOLE assigned chunk (spot-check against `source/chunks/NN.txt` — read
the chunk's LAST major topic too, not just its opening), has no meta-junk (no leftover instructions,
no "I cannot..." refusals), and (for page 02 only) embeds both
`images/fig1-agentic-graphrag-systems.png` and `images/fig2-graph-ablations.png`. Read each wiki
file's TAIL, not just its length — a known local-model failure mode is a repetition loop that pads
line count with nonsense.

Build a BAD list and a GOOD list.

### Step 3: Handle BAD pages (only if BAD is non-empty)
For each bad page NN:
- Count existing beads titled `"ArxivWhyNeighborhoodsMatter chunk NN extract"` (including any retry
  suffix) to get its attempt count.
- **Attempt count < 3:** delete the bad wiki file, create ONE retry extract bead reusing
  `source/specs/NN-extract.md` verbatim: `--coder opencode --model ollama-rtx/qwen3.8:27b --cwd
  /Users/sergii/.kb -p 2 -t task --body-file /Users/sergii/.kb/papers/ArxivWhyNeighborhoodsMatter/source/specs/NN-extract.md`.
  Record its id.
- **Attempt count >= 3:** this chunk has exhausted its retry budget — write that one wiki page by
  hand, reading `source/chunks/NN.txt` directly, following the same page structure the extract spec
  describes. Do not requeue it.

If any retries were created this round: create ONE successor finalize bead (same spec file,
`--coder claude --model sonnet`) depending on all of them, close own bead with reason
`"rearmed as <new-id>: N chunk(s) requeued"`, and stop. If every bad page was instead handled by
hand-writing (nothing requeued), continue to Step 4 in this same run.

If BAD was empty in Step 2, go straight to Step 4.

### Step 4: Synthesize the rest of the wiki
Read the (now-verified) wiki pages — not the raw source, except to spot-check quality — and produce:

1. **`index.md`** — front-matter `type: Paper`, title, one-sentence description, `generated: {by:
   claude/sonnet, at: <ISO-8601 UTC timestamp>}`, `sources:` (id `original` → arXiv URL, id
   `local-copy` → `source/full.txt`, plus `source/source.md` provenance pin since the PDF binary
   was not kept — see size guard note in `source/source.md`), tags (e.g. `[graphrag, agentic-rag,
   provenance, citation-faithfulness, knowledge-graphs]`). Body: orientation paragraph, "How to work
   through this" ladder, "Read This Folder" links, wiki table (4 rows, reading order), "Original
   Source" section linking `source/source.md` (no PDF file exists — reference the provenance pin,
   not a missing binary).
2. **`summary.md`** — the standard paper template (see `kb show summary/get` A2-template): title,
   `**Paper:** [Why Neighborhoods Matter... (Terrenzi et al., 2026)](https://arxiv.org/abs/2605.15109)`,
   Human Readable TL;DR (analogy-first, zero jargon), TL;DR (technical), Problem & Motivation, Main
   Original Ideas, Key Findings (include Table 1 / Table 2 numbers from `wiki/03-*.md`), Suggestions
   & Future Directions (from limitations), Authors & Institutions, Figures section embedding both
   images with relative paths `wiki/images/...`. Under 300 lines.
3. **`digest.md`** — one section per wiki page copying its `**In one sentence:**` line and
   `## Key points` bullets verbatim, in reading order, plus a closing "## The argument in five moves"
   (5-7 numbered steps synthesizing the whole paper's arc).
4. **`explainer.md`** — plain-language layer (What is this about? / Why does it matter? / How does
   it work? / Where can this be used? / Conclusions & takeaways / Jargon decoder table with 5-12
   terms e.g. "agentic GraphRAG", "provenance", "ablation", "citation faithfulness"). 80-150 lines.
5. **`questions.md`** — 6-8 retrieval-practice questions (this is a short paper, <30pp), at least one
   per wiki page, answers ONLY inside collapsed `> [!tip]- Answer` callouts, each answer linking its
   covering wiki page. Mix: ~half recall, ~a third elaboration, rest transfer + one evaluation
   question drawing on `critical_thinking.md` (write critical_thinking.md first, see next item).
6. **`critical_thinking.md`** — claims vs. evidence (assess the 3 ablation studies' evidence
   strength — sample size/scale caveats, since the paper uses a synthetic subgraph example in Figure
   2), genuinely new vs. repackaged, weaknesses/blind spots, applicability, "Relevance to my work"
   (2-4 bullets for an AI/ML engineer building agentic/graph-RAG systems), what this changes, and a
   Verdict ending in one of adopt/trial/watch/skip. 60-120 lines.
7. **`connections.md`** — read `/Users/sergii/.kb/ai_papers/index.md` and skim 2-3 plausible
   category files, plus `ls /Users/sergii/.kb/papers/` for other agentic-GraphRAG entries ingested in
   this same batch (folder names likely start with `Arxiv...GraphRAG`, `ArxivGraphReasoning...`,
   `ArxivGraphScout`, etc.) — select 2-6 genuinely related entries (shares-technique / same-problem-
   different-method / builds-on). If nothing is related yet, write
   `_No related entries found in the KB as of <date>._`

All seven files need the backlink line `> [[../index|Wiki]] | [[../summary|Summary]]` per the
wiring rules (wiki pages already have it) and use Obsidian `[[wikilink]]` syntax throughout.

### Step 5: Report + close
Write `source/delegation_report.md`: chunks total (4) / passed first try / requeued (how many
rounds) / hand-written after exhausting retries. Then:
`bd close <own-id> --reason "wiki complete"`.

No git commands anywhere in this task — `.kb` auto-syncs.

## Tests
- `ls /Users/sergii/.kb/papers/ArxivWhyNeighborhoodsMatter/` shows `index.md summary.md digest.md
  explainer.md questions.md critical_thinking.md connections.md source/ wiki/`
- `grep -c "In one sentence" /Users/sergii/.kb/papers/ArxivWhyNeighborhoodsMatter/digest.md` → 4

## DoD
1. All steps above completed for this run (either full synthesis, or a clean rearm).
2. `source/delegation_report.md` written (only on the run that reaches Step 5).
3. `bd close <own-id> --reason "wiki complete"` (only on the run that reaches Step 5) — never exit
   rc=0 without closing (a rearming run closes with the rearm reason instead).

## Scope & constraints
- Touch ONLY files under `/Users/sergii/.kb/papers/ArxivWhyNeighborhoodsMatter/` and beads you create
  yourself for this paper's chain.
- Do not run `fleet serve restart` or `fleet run`.
- cwd: /Users/sergii/.kb
