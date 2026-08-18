# Finalize: verify + synthesize — AIBuilderClubGraphEngineeringGuide2026

This is the ONLY validation step in the whole pipeline. You are a Claude worker running
headless. Follow this spec fully; it is self-contained.

Folder: `/Users/sergii/.kb/papers/AIBuilderClubGraphEngineeringGuide2026/`

Source: AI Builder Club article "Graph Engineering Guide (2026)".
URL: https://www.aibuilderclub.com/blog/graph-engineering-guide-2026

`WORKER_MODEL` = `ollama-rtx/qwen3.8:27b`, `RETRY_BUDGET` = 3 attempts per chunk.

## Step 1: Completeness gate (self-rearm)

List all beads matching "AIBuilderClubGraphEngineeringGuide2026 chunk * extract" (`fleet bd
search` or `fleet bd list` + grep) — this also catches any retry beads created by an earlier
finalize round. If ANY are still open/in-progress, this run is premature: create a successor
finalize bead (same spec file, `--deps <the still-open bead ids>`), close your own bead with
reason `"rearmed as <new-id>: chunks still in flight"`, and stop.

## Step 2: Verify every wiki page

Expected pages (3 total, one per source chunk):

- `wiki/01-what-is-graph-engineering.md` — should cover: the definition of graph engineering
  (nodes/edges/state; graph engineering designs how loops connect); the three things it is NOT
  (knowledge graphs/GraphRAG, a new capability, a default); the X-thread origin of the term in
  mid-July 2026 (Peter Steinberger, @svpino, @rohit4verse, @VaibhavSisinty); the three parts of
  an agent graph (nodes, edges, shared state); the org-chart metaphor and its limits; and the
  starter diagram embedded as an image with a description of what it shows (Researcher → Writer
  → Reviewer with a conditional pass/reject-loop-back edge). Check the image
  `![...](images/01-agent-graph-starter-diagram.png)` is actually embedded in this page (the
  file exists at `wiki/images/01-agent-graph-starter-diagram.png` — a real 2400x1520 PNG,
  already downloaded, do not flag it as missing).
- `wiki/02-when-to-use-a-graph.md` — should cover: the "you probably don't need a graph" default
  answer; the decision-table-as-triggers framing; the over-engineered PDF-summarizer example vs.
  the right-sized market-brief example; the collapse-back-to-one-loop tell; the LangGraph/
  AutoGen GraphFlow/Google ADK/A2A prior-art concession and what's actually new (shared
  vocabulary, not a new paradigm); and the 5-layer AI engineering stack (prompt, context,
  harness, loop, graph) being cumulative.
- `wiki/03-hype-check-and-checklist.md` — should cover: the named skeptics and their specific
  critiques (@RhysSullivan, @DavidKPiano/XState, @PawelHuryn, @NathanFlurry); the article's
  concession that the mechanics are old and much content is slop; the separating move (the
  escalation from one loop to coordinated nodes is real regardless of the label); the 3-question
  filter; the 8-item starting checklist; the FAQ; and the cited sources list.

For each: check it exists, is non-trivial (this is a short article so pages will be shorter than
a book chapter — treat >20 lines as the trivia floor here, not the usual >40), matches the
format contract (backlink line, `**In one sentence:**`, `## Key points`, `---`, detail sections,
`**Covers:**` footer), and covers the whole assigned chunk (not just its opening topic). Read
the file's TAIL, not just its length — a known local-model failure mode is a repetition loop
that pads line count with nonsense. Build a BAD list and a GOOD list.

Only page 01 has a figure; pages 02 and 03 have none — do not flag missing images there as a
defect.

## Step 3: Handle BAD pages

If BAD is empty, go straight to Step 4. If BAD is non-empty: for each bad chunk, count existing
extract beads titled `"AIBuilderClubGraphEngineeringGuide2026 chunk NN extract"` (any retry
suffix) to get its attempt count.

- Attempt count < `RETRY_BUDGET` (3): delete the bad page, create ONE retry extract bead
  reusing `source/specs/NN-extract.md` verbatim (`--coder opencode --model
  ollama-rtx/qwen3.8:27b`), record its id.
- Attempt count >= `RETRY_BUDGET`: this chunk has exhausted reprocessing — write that one page
  by hand from `source/chunks/NN.txt` (and, for chunk 01, `wiki/images/01-description.md`),
  following the same format contract shown in that chunk's own `NN-extract.md` spec file. Do
  not requeue it.

If any retries were created this round: create ONE successor finalize bead depending on all of
them (same spec file, `--cwd /Users/sergii/.kb --coder claude --model sonnet -p 1 -t task`),
close your own bead with reason `"rearmed as <new-id>: N chunk(s) requeued"`, and stop. If every
bad chunk was handled by hand-writing (nothing requeued), continue to Step 4 in this same run.

## Step 4: Synthesize the rest of the wiki

Read `kb show summary/get` (Shared Output Conventions section) for the exact file specs, then
produce, reading only the wiki pages (small, 3 of them) and NOT the raw source except to
spot-check quality:

- `index.md` — front-matter with `type: Article`, title, one-sentence description, `generated:
  {by: claude/sonnet, at: <ISO-8601 UTC timestamp>}`, `sources:` with `id: original` (the URL
  above) and `id: local-copy` (`source/article.md`), 2-5 tags (e.g. `[agentic-systems,
  graph-engineering, loop-engineering, multi-agent, ai-engineering]`). Orientation paragraph,
  "How to work through this" ladder, "Read This Folder" links, wiki table (3 rows, reading
  order), "Original Source" link to `source/article.md`.
- `summary.md` — the A2-template from `summary/get` (Human Readable TL;DR, TL;DR, Problem &
  Motivation, Main Original Ideas, Key Findings, Suggestions & Future Directions, Authors &
  Institutions — this article has no named individual author; attribute to "AI Builder Club").
  Use `**Article:** [Graph Engineering Guide (2026)](https://www.aibuilderclub.com/blog/graph-engineering-guide-2026) — AI Builder Club, 2026` as the metadata line. Include a brief Figures
  section noting the one starter-diagram image. Keep under 300 lines (this is a short article —
  summary.md should land well under 100 lines).
- `digest.md` — copy each wiki page's `**In one sentence:**` line and `## Key points` bullets
  verbatim, in order (3 sections), then a short `## The argument in five moves` closing spine
  (5-7 numbered clauses). Target ~40-60 lines given the short source.
- `explainer.md` — plain-language layer per the shared spec: What is this about? / Why does it
  matter? / How does it work? / Where can this be used? / Conclusions & takeaways / Jargon
  decoder (5-8 terms: e.g. node, edge, shared state, org chart, StateGraph, A2A, fan-out/fan-in,
  stop condition). Target 80-120 lines.
- `questions.md` — 6-8 retrieval-practice questions (this is a short article per the Scaling by
  source size table), at least one per wiki page (so at least 2 per page given 3 pages), mixing
  core recall, elaboration ("why is a loop a special case of a graph rather than something
  different?"), transfer, and one evaluation question drawing on `critical_thinking.md`. Answers
  ONLY inside collapsed `> [!tip]- Answer` callouts.
- `critical_thinking.md` — per the shared spec (Claims vs. evidence, Genuinely new vs.
  repackaged, Weaknesses and blind spots, Applicability with a "Relevance to my work" subsection
  for Sergii's AI/ML engineering and agentic-systems context, What this changes, Verdict ending
  in adopt/trial/watch/skip). Target 60-90 lines given the short source — do not pad. Note this
  source is unusually self-skeptical (it quotes its own critics at length), which should sharpen
  the "genuinely new vs. repackaged" analysis rather than substitute for it.
- `connections.md` — read `/Users/sergii/.kb/ai_papers/index.md` and check
  `/Users/sergii/.kb/papers/` for related entries. Several directly relevant candidates are
  already known to exist: `/Users/sergii/.kb/papers/TuringPostIsGraphEngineeringReal/`,
  `/Users/sergii/.kb/papers/GraphEngineeringVsLoopEngineering/`,
  `/Users/sergii/.kb/papers/LangGraph3YearsGraphEngineering/`,
  `/Users/sergii/.kb/papers/MarkTechPostPromptLoopGraph/`,
  `/Users/sergii/.kb/papers/LoopEngineeringAnthropicPlaybook/`,
  `/Users/sergii/.kb/papers/LoopEngineeringClearlyExplained/`, and
  `/Users/sergii/.kb/papers/Graphify/` — read their `summary.md` files and link the ones
  genuinely related to this article's specific claims (same prompt/loop/graph layering
  discourse, same July 2026 X-thread origin story), plus any other 0-4 genuinely related entries
  found (e.g. harness-related entries under `/Users/sergii/.kb/papers/*Harness*`). Do not force
  links beyond what is genuinely related.

## Step 5: Report + close

Write a completion report to
`/Users/sergii/.kb/papers/AIBuilderClubGraphEngineeringGuide2026/source/delegation_report.md`:
chunks total (3) / passed first try / requeued (how many rounds, if any) / hand-written after
exhausting retries (if any). Then:

`bd close <own-id> --reason "wiki complete"`

No git commands anywhere in this spec — `.kb` auto-syncs.
