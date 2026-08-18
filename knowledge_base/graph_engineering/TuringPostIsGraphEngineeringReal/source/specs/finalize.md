# Finalize: verify + synthesize — TuringPostIsGraphEngineeringReal

This is the ONLY validation step in the whole pipeline. You are a Claude worker running
headless. Follow this spec fully; it is self-contained.

Folder: `/Users/sergii/.kb/papers/TuringPostIsGraphEngineeringReal/`

Source: Turing Post article "FOD#159: Is Graph Engineering Real? Why Everyone Is Talking
About It" by Ksenia Se, 2026-07-20.
URL: https://www.turingpost.com/p/is-graph-engineering-real-why-everyone-is-talking-about-it

`WORKER_MODEL` = `ollama-rtx/qwen3.8:27b`, `RETRY_BUDGET` = 3 attempts per chunk.

## Step 1: Completeness gate (self-rearm)

List all beads matching "TuringPostIsGraphEngineeringReal chunk * extract" (`fleet bd
search` or `fleet bd list` + grep) — this also catches any retry beads created by an
earlier finalize round. If ANY are still open/in-progress, this run is premature: create a
successor finalize bead (same spec file, `--deps <the still-open bead ids>`), close your
own bead with reason `"rearmed as <new-id>: chunks still in flight"`, and stop.

## Step 2: Verify every wiki page

Expected pages (3 total, one per source chunk):

- `wiki/01-core-argument-and-definitions.md` — should cover: the loop-vs-graph framing,
  the "graph engineering displaced loop engineering after ~6 weeks" observation, and the
  node/edge/state definitions.
- `wiki/02-four-graph-types-and-fact-check.md` — should cover: the four graph types table
  (control graph, knowledge graph, execution trace, improvement graph) and the fact-check
  of both viral claims (Microsoft/Stanford/Anthropic adoption claim; 18%/85% figures).
- `wiki/03-practical-guidance-and-industry-shift.md` — should cover: "if linear, keep it
  linear" guidance, the three conditions that justify a graph, and the prompt-centric to
  system-centric framing.

For each: check it exists, is non-trivial (this is a short article so pages will be
shorter than a book chapter — treat >20 lines as the trivia floor here, not the usual
>40), matches the format contract (backlink line, `**In one sentence:**`, `## Key points`,
`---`, detail sections, `**Covers:**` footer), and covers the whole assigned chunk (not
just its opening topic). Read the file's TAIL, not just its length — a known local-model
failure mode is a repetition loop that pads line count with nonsense. Build a BAD list and
a GOOD list.

There are no figures/images for this source (it is a short text article with no diagrams
extracted) — do not flag missing images as a defect.

## Step 3: Handle BAD pages

If BAD is empty, go straight to Step 4. If BAD is non-empty: for each bad chunk, count
existing extract beads titled `"TuringPostIsGraphEngineeringReal chunk NN extract"` (any
retry suffix) to get its attempt count.

- Attempt count < `RETRY_BUDGET` (3): delete the bad page, create ONE retry extract bead
  reusing `source/specs/NN-extract.md` verbatim (`--coder opencode --model
  ollama-rtx/qwen3.8:27b`), record its id.
- Attempt count >= `RETRY_BUDGET`: this chunk has exhausted reprocessing — write that one
  page by hand from `source/chunks/NN.txt`, following the same format contract shown in
  that chunk's own `NN-extract.md` spec file. Do not requeue it.

If any retries were created this round: create ONE successor finalize bead depending on
all of them (same spec file, `--cwd /Users/sergii/.kb --coder claude --model sonnet -p 1
-t task`), close your own bead with reason `"rearmed as <new-id>: N chunk(s) requeued"`,
and stop. If every bad chunk was handled by hand-writing (nothing requeued), continue to
Step 4 in this same run.

## Step 4: Synthesize the rest of the wiki

Read `kb show summary/get` (Shared Output Conventions section) for the exact file specs,
then produce, reading only the wiki pages (small, 3 of them) and NOT the raw source except
to spot-check quality:

- `index.md` — front-matter with `type: Article`, title, one-sentence description,
  `generated: {by: claude/sonnet, at: <ISO-8601 UTC timestamp>}`, `sources:` with
  `id: original` (the URL above) and `id: local-copy` (`source/article.md`), 2-5 tags
  (e.g. `[agentic-systems, graph-engineering, multi-agent, llm-ops]`). Orientation
  paragraph, "How to work through this" ladder, "Read This Folder" links, wiki table (3
  rows, reading order), "Original Source" link to `source/article.md`.
- `summary.md` — the A2-template from `summary/get` (Human Readable TL;DR, TL;DR, Problem
  & Motivation, Main Original Ideas, Key Findings, Suggestions & Future Directions,
  Authors & Institutions). Use `**Article:** [<Title>](<url>) — Turing Post, 2026-07-20`
  as the metadata line. No Figures section (none exist). Keep under 300 lines (this is a
  short article — summary.md should land well under 100 lines).
- `digest.md` — copy each wiki page's `**In one sentence:**` line and `## Key points`
  bullets verbatim, in order (3 sections), then a short `## The argument in five moves`
  closing spine (5-7 numbered clauses). Target ~40-60 lines given the short source.
- `explainer.md` — plain-language layer per the shared spec: What is this about? / Why
  does it matter? / How does it work? / Where can this be used? / Conclusions & takeaways
  / Jargon decoder (5-8 terms: e.g. node, edge, state, control graph, knowledge graph,
  GraphRAG, DSPy). Target 80-120 lines.
- `questions.md` — 6-8 retrieval-practice questions (this is a short article per the
  Scaling by source size table), at least one per wiki page (so at least 2 per page given
  3 pages), mixing core recall, elaboration ("why does keeping a linear workflow linear
  matter?"), transfer, and one evaluation question drawing on `critical_thinking.md`.
  Answers ONLY inside collapsed `> [!tip]- Answer` callouts.
- `critical_thinking.md` — per the shared spec (Claims vs. evidence, Genuinely new vs.
  repackaged, Weaknesses and blind spots, Applicability with a "Relevance to my work"
  subsection for Sergii's AI/ML engineering and agentic-systems context, What this
  changes, Verdict ending in adopt/trial/watch/skip). Target 60-90 lines given the short
  source — do not pad.
- `connections.md` — read `/Users/sergii/.kb/ai_papers/index.md` and check
  `/Users/sergii/.kb/papers/` for related entries. Two directly relevant candidates are
  already known to exist: `/Users/sergii/.kb/papers/GraphEngineeringVsLoopEngineering/`
  and `/Users/sergii/.kb/papers/LangGraph3YearsGraphEngineering/` — read their `summary.md`
  files and link both if genuinely related (this article is explicitly about the same
  graph-vs-loop-engineering discourse), plus any other 0-4 genuinely related entries found.
  Do not force links beyond what is genuinely related.

## Step 5: Report + close

Write a completion report to
`/Users/sergii/.kb/papers/TuringPostIsGraphEngineeringReal/source/delegation_report.md`:
chunks total (3) / passed first try / requeued (how many rounds, if any) / hand-written
after exhausting retries (if any). Then:

`bd close <own-id> --reason "wiki complete"`

No git commands anywhere in this spec — `.kb` auto-syncs.
