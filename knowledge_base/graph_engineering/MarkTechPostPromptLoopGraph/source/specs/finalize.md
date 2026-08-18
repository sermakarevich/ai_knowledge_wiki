# Finalize: verify + synthesize — MarkTechPostPromptLoopGraph

This is the ONLY validation step in the whole pipeline. You are a Claude worker running
headless. Follow this spec fully; it is self-contained.

Folder: `/Users/sergii/.kb/papers/MarkTechPostPromptLoopGraph/`

Source: MarkTechPost article "Prompt Engineering vs Loop Engineering vs Graph Engineering:
What Changes at Each Layer" by Asif Razzaq, 2026-07-29.
URL: https://www.marktechpost.com/2026/07/29/prompt-engineering-vs-loop-engineering-vs-graph-engineering/

`WORKER_MODEL` = `ollama-rtx/qwen3.8:27b`, `RETRY_BUDGET` = 3 attempts per chunk.

## Step 1: Completeness gate (self-rearm)

List all beads matching "MarkTechPostPromptLoopGraph chunk * extract" (`fleet bd search` or
`fleet bd list` + grep) — this also catches any retry beads created by an earlier finalize
round. If ANY are still open/in-progress, this run is premature: create a successor finalize
bead (same spec file, `--deps <the still-open bead ids>`), close your own bead with reason
`"rearmed as <new-id>: chunks still in flight"`, and stop.

## Step 2: Verify every wiki page

Expected pages (3 total, one per source chunk):

- `wiki/01-prompt-and-loop-layers.md` — should cover: the gist of the three nested layers
  (prompt/loop/graph as units of control), why layers get added (breakdown of manual review
  at volume/multi-step/no-grader conditions), the loop layer's building blocks (automations,
  worktrees, skills, connectors, checker sub-agent, external state), and the stop-condition
  thesis.
- `wiki/02-graph-layer.md` — should cover: the org-graph vs. work-graph distinction and what
  each answers, skepticism about the term's novelty (LangGraph/Anthropic precedent), what the
  article claims is actually new (shared node/edge/state vocabulary), and the edge-carries-
  state failure mode.
- `wiki/03-decision-framework-and-numbers.md` — should cover: the four-question ordered
  checklist for choosing a layer, the layers-compose-not-replace claim, the operator-skill
  caution, the headline cost/performance numbers (+90% eval gain at ~15x token cost, ~80%
  variance explained by token spend), and the list of cited sources.

For each: check it exists, is non-trivial (this is a short article so pages will be shorter
than a book chapter — treat >20 lines as the trivia floor here, not the usual >40), matches
the format contract (backlink line, `**In one sentence:**`, `## Key points`, `---`, detail
sections, `**Covers:**` footer), and covers the whole assigned chunk (not just its opening
topic). Read the file's TAIL, not just its length — a known local-model failure mode is a
repetition loop that pads line count with nonsense. Build a BAD list and a GOOD list.

There are no figures/images for this source (it is a short text article with no diagrams
extracted) — do not flag missing images as a defect.

## Step 3: Handle BAD pages

If BAD is empty, go straight to Step 4. If BAD is non-empty: for each bad chunk, count
existing extract beads titled `"MarkTechPostPromptLoopGraph chunk NN extract"` (any retry
suffix) to get its attempt count.

- Attempt count < `RETRY_BUDGET` (3): delete the bad page, create ONE retry extract bead
  reusing `source/specs/NN-extract.md` verbatim (`--coder opencode --model
  ollama-rtx/qwen3.8:27b`), record its id.
- Attempt count >= `RETRY_BUDGET`: this chunk has exhausted reprocessing — write that one
  page by hand from `source/chunks/NN.txt`, following the same format contract shown in that
  chunk's own `NN-extract.md` spec file. Do not requeue it.

If any retries were created this round: create ONE successor finalize bead depending on all
of them (same spec file, `--cwd /Users/sergii/.kb --coder claude --model sonnet -p 1 -t
task`), close your own bead with reason `"rearmed as <new-id>: N chunk(s) requeued"`, and
stop. If every bad chunk was handled by hand-writing (nothing requeued), continue to Step 4 in
this same run.

## Step 4: Synthesize the rest of the wiki

Read `kb show summary/get` (Shared Output Conventions section) for the exact file specs, then
produce, reading only the wiki pages (small, 3 of them) and NOT the raw source except to
spot-check quality:

- `index.md` — front-matter with `type: Article`, title, one-sentence description,
  `generated: {by: claude/sonnet, at: <ISO-8601 UTC timestamp>}`, `sources:` with
  `id: original` (the URL above) and `id: local-copy` (`source/article.md`), 2-5 tags (e.g.
  `[agentic-systems, graph-engineering, loop-engineering, prompt-engineering, multi-agent]`).
  Orientation paragraph, "How to work through this" ladder, "Read This Folder" links, wiki
  table (3 rows, reading order), "Original Source" link to `source/article.md`.
- `summary.md` — the A2-template from `summary/get` (Human Readable TL;DR, TL;DR, Problem &
  Motivation, Main Original Ideas, Key Findings, Suggestions & Future Directions, Authors &
  Institutions). Use `**Article:** [<Title>](<url>) — MarkTechPost, 2026-07-29` as the
  metadata line. No Figures section (none exist). Keep under 300 lines (this is a short
  article — summary.md should land well under 100 lines).
- `digest.md` — copy each wiki page's `**In one sentence:**` line and `## Key points` bullets
  verbatim, in order (3 sections), then a short `## The argument in five moves` closing spine
  (5-7 numbered clauses). Target ~40-60 lines given the short source.
- `explainer.md` — plain-language layer per the shared spec: What is this about? / Why does it
  matter? / How does it work? / Where can this be used? / Conclusions & takeaways / Jargon
  decoder (5-8 terms: e.g. loop, graph, stop condition, org graph, work graph, StateGraph,
  node, edge). Target 80-120 lines.
- `questions.md` — 6-8 retrieval-practice questions (this is a short article per the Scaling
  by source size table), at least one per wiki page (so at least 2 per page given 3 pages),
  mixing core recall, elaboration ("why is the stop condition the hard part of a loop, not the
  cycle itself?"), transfer, and one evaluation question drawing on `critical_thinking.md`.
  Answers ONLY inside collapsed `> [!tip]- Answer` callouts.
- `critical_thinking.md` — per the shared spec (Claims vs. evidence, Genuinely new vs.
  repackaged, Weaknesses and blind spots, Applicability with a "Relevance to my work"
  subsection for Sergii's AI/ML engineering and agentic-systems context, What this changes,
  Verdict ending in adopt/trial/watch/skip). Target 60-90 lines given the short source — do
  not pad.
- `connections.md` — read `/Users/sergii/.kb/ai_papers/index.md` and check
  `/Users/sergii/.kb/papers/` for related entries. Several directly relevant candidates are
  already known to exist: `/Users/sergii/.kb/papers/TuringPostIsGraphEngineeringReal/`,
  `/Users/sergii/.kb/papers/GraphEngineeringVsLoopEngineering/`,
  `/Users/sergii/.kb/papers/LangGraph3YearsGraphEngineering/`,
  `/Users/sergii/.kb/papers/LoopEngineeringAnthropicPlaybook/`, and
  `/Users/sergii/.kb/papers/LoopEngineeringClearlyExplained/` — read their `summary.md` files
  and link the ones genuinely related to this article's specific claims (same
  prompt/loop/graph layering discourse), plus any other 0-4 genuinely related entries found.
  Do not force links beyond what is genuinely related.

## Step 5: Report + close

Write a completion report to
`/Users/sergii/.kb/papers/MarkTechPostPromptLoopGraph/source/delegation_report.md`: chunks
total (3) / passed first try / requeued (how many rounds, if any) / hand-written after
exhausting retries (if any). Then:

`bd close <own-id> --reason "wiki complete"`

No git commands anywhere in this spec — `.kb` auto-syncs.
