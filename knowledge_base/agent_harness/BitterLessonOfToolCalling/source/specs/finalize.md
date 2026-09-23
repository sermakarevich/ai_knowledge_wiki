# Finalize: verify + synthesize — "The Bitter Lesson of Tool Calling" wiki

## Problem

An extract-only fleet chain (local model, `ollama-rtx/qwen3.8:27b`) has been writing
6 wiki pages for the arXiv paper "The Bitter Lesson of Tool Calling" (2608.06370)
into `/Users/sergii/.ai/knowledge/research/BitterLessonOfToolCalling/wiki/`. No per-chunk
validation happened — this bead is the ONLY validation + synthesis step in the
whole pipeline. Read `ai show summary/get_local` for full context on this workflow
if anything below is ambiguous (section "Step 5: Create the finalize bead").

Folder: `/Users/sergii/.ai/knowledge/research/BitterLessonOfToolCalling/`
Retry budget per chunk: 3 attempts (initial + 2 retries).
Worker model for requeues: `--coder opencode --model ollama-rtx/qwen3.8:27b`.

## Step 1: Completeness gate (self-rearm)

List all beads whose title matches `"BitterLessonOfToolCalling chunk"` and
`"extract"` (`bd search` or `bd list` + grep) — this also catches any retry beads
from an earlier finalize round. If ANY are still open/in-progress: this run is
premature.
- Create a successor finalize bead reusing this same spec file
  (`--coder claude --model sonnet -p 1 -t task --body-file <this file's absolute
  path> --deps <the still-open bead ids>`).
- `bd close <own-id> --reason "rearmed as <new-id>: chunks still in flight"`.
- Stop (do nothing further in this run).

## Step 2: Verify every wiki page

The 6 expected pages, each mapped to a chunk (see
`source/chunks.json` for the authoritative manifest):

| # | Wiki page | Source sections | Named figures that must be embedded |
|---|---|---|---|
| 01 | wiki/01-introduction-and-related-work.md | Abstract, §1, §2 | none |
| 02 | wiki/02-method.md | §3 (3.1-3.5) | wiki/images/fig1-paradigm-overview.png |
| 03 | wiki/03-experiments.md | §4 (4.1-4.4) | none |
| 04 | wiki/04-analysis.md | §5 (5.1-5.3) | wiki/images/fig2-accuracy-by-model-generation.png |
| 05 | wiki/05-conclusion-and-limitations.md | §6, §7 | none |
| 06 | wiki/06-appendix-details.md | Appendix A/B/C | none |

For each page, check:
- It exists and is non-trivial (>40 lines).
- It matches the format contract in its own `source/specs/NN-extract.md` file
  (backlink line, `# <Topic>`, `**In one sentence:**`, `## Key points` with 5-8
  substantive bullets, `---`, hierarchical `##` detail sections, `**Covers:**`
  footer).
- It covers the WHOLE chunk — spot-check the chunk's LAST major topic (read the
  tail of `source/chunks/NN.txt` and confirm that content appears in the page),
  not just the opening.
- Any figure listed in the table above is actually embedded (`![...](images/...)`).
- **Read the file's TAIL, not just its line count** — a known local-model failure
  mode is a repetition loop that pads line count with repeated/garbled text near
  the end. If the tail looks like nonsense or a loop, treat the page as BAD even if
  it is long.

Build a BAD list and a GOOD list.

## Step 3: Handle BAD pages

If BAD is empty, go straight to Step 4.

If BAD is non-empty, for each bad chunk NN:
- Count existing beads titled `"BitterLessonOfToolCalling chunk NN extract"` (any
  retry suffix) to get its attempt count.
- **Attempt count < 3:** delete the bad page (`wiki/NN-*.md`), create ONE retry
  extract bead reusing `source/specs/NN-extract.md` verbatim: `fleet bd create
  "BitterLessonOfToolCalling chunk NN extract retry" --cwd /Users/sergii/.ai
  --coder opencode --model ollama-rtx/qwen3.8:27b -p 2 -t task --body-file
  <absolute path to source/specs/NN-extract.md> --silent`. Record its id.
- **Attempt count >= 3:** this chunk has exhausted reprocessing. Write that one
  page yourself, by hand, directly from `source/chunks/NN.txt` (and its figure
  description file if any), following the same format contract in
  `source/specs/NN-extract.md`. This is a last resort, not the default path. Do
  not requeue it.

If any retries were created this round: create ONE successor finalize bead
depending on all of them (`--deps <id1,id2,...>`, reusing this same spec file),
`bd close <own-id> --reason "rearmed as <new-id>: N chunk(s) requeued"`, and stop.

If every bad chunk was handled by hand-writing (nothing requeued this round),
continue to Step 4 in this same run.

## Step 4: Synthesize the remaining artifacts

Read the 6 wiki pages (small, ~40-150 lines each) — not the raw PDF, except to
spot-check quality if something is unclear. Produce, per `ai show summary/get`
conventions (Shared Output Conventions section):

1. **`summary.md`** — the A2-template: Human Readable TL;DR, TL;DR, Problem &
   Motivation, Main Original Ideas, Key Findings (include a results table),
   Suggestions & Future Directions, Authors & Institutions, optional Figures
   section. Metadata line: `**Paper:** [The Bitter Lesson of Tool Calling (Patel,
   Sen, Lumer, Subbiah, 2026)](https://arxiv.org/abs/2608.06370)`. Under 300 lines.

2. **`digest.md`** — copy each wiki page's `**In one sentence:**` line and `## Key
   points` bullets verbatim, in reading order (pages 01-06), then close with
   `## The argument in five moves` (5-7 numbered steps, the paper's own synthesis).

3. **`index.md`** — OKF front-matter (`type: Paper`, `title`, `description`,
   `generated: {by: claude/sonnet, at: <ISO-8601 UTC timestamp>}`, `sources:
   [{id: original, resource: https://arxiv.org/abs/2608.06370}, {id: local-copy,
   resource: source/2608.06370.pdf}]`, `tags:` 2-5 lowercase topical tags e.g.
   `[llm-agents, tool-calling, benchmarking, code-generation]`), orientation
   paragraph, "How to work through this" ladder, "Read This Folder" links, wiki
   table (6 rows, reading order), "Original Source" link with retrieval date
   (today's date). Note in the orientation or a short aside that the bibliography
   was intentionally not reproduced as a wiki page (see
   `source/chunks.json` -> `excluded`).

4. **`explainer.md`** — plain-language layer per the Shared Output Conventions
   template (What is this about? / Why does it matter? / How does it work? / Where
   can this be used? / Conclusions & takeaways / Jargon decoder with 5-12 terms,
   e.g. "tool calling", "JSON tool calling", "programmatic tool calling / codemode",
   "BFCL", "context rot", "fan-out"). 80-150 lines.

5. **`questions.md`** — 6-8 retrieval-practice questions (short paper: see Scaling
   by source size table), at least ONE per wiki page (6 pages -> at least 6
   questions), mix ~half core recall / ~a third elaboration / rest transfer plus
   one evaluation question drawing on `critical_thinking.md` (write that file
   first, in the next artifact, so this question has something to link to — or
   write both together and cross-reference). Answers ONLY inside collapsed
   `> [!tip]- Answer` callouts, each linking its covering wiki page.

6. **`critical_thinking.md`** — per the Shared Output Conventions template: Claims
   vs. evidence (assess the benchmark choice, sample sizes n=31-52 in ablations,
   the noted 20% evaluator-human misalignment in BFCL v4's LLM-judge mode, the
   echo-return-stub limitation), Genuinely new vs. repackaged, Weaknesses and blind
   spots, Applicability, "Relevance to my work" (2-4 bullets for an AI/ML engineer
   building agentic systems — Sergii's context: agent harness / tool-calling
   design, e.g. relevance to Fleet's own coder-worker tool use), What this changes,
   Verdict (end with one of adopt / trial / watch / skip + the single strongest
   reason). 60-120 lines.

7. **`connections.md`** — read `/Users/sergii/.ai/knowledge/structured_papers/index.md`, skim 2-3
   plausible category files (e.g. agent harness / tool use / LLM theory
   categories) for candidate related entries, and `ls /Users/sergii/.ai/knowledge/research/`
   for unfiled recent entries. Select 2-6 genuinely related entries (builds-on,
   contradicts, same-problem-different-method, shares-technique,
   applies-in-practice). If nothing is genuinely related, write:
   `_No related entries found in the KB as of <date>._` Do not force links.

All wikilinks use Obsidian `[[...]]` syntax; every sub-file gets a backlink line to
`index` and `summary` (see Shared Output Conventions in `ai show summary/get`).

## Step 5: Report + close

Write `/Users/sergii/.ai/knowledge/research/BitterLessonOfToolCalling/source/delegation_report.md`:
chunks total (6) / passed first try / requeued (how many rounds, if any) / hand-
written after exhausting retries (if any). Then:

`bd close <own-id> --reason "wiki complete"`

No git commands anywhere in this task — `.ai` auto-syncs on its own.
