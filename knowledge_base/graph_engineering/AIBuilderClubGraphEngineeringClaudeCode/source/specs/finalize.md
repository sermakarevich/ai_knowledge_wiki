# Finalize: verify + synthesize — AIBuilderClubGraphEngineeringClaudeCode

This is the ONLY validation step in the whole pipeline. You are a Claude worker running
headless. Follow this spec fully; it is self-contained.

Folder: `/Users/sergii/.kb/papers/AIBuilderClubGraphEngineeringClaudeCode/`

Source: AI Builder Club article "Graph Engineering with Claude Code: Anthropic's Agent Graph"
(by Shirley, published July 24 2026, updated August 3 2026).
URL: https://www.aibuilderclub.com/blog/graph-engineering-with-claude-code

`WORKER_MODEL` = `ollama-rtx/qwen3.8:27b`, `RETRY_BUDGET` = 3 attempts per chunk.

## Step 1: Completeness gate (self-rearm)

List all beads matching "AIBuilderClubGraphEngineeringClaudeCode chunk * extract" (`fleet bd
search` or `fleet bd list` + grep) — this also catches any retry beads created by an earlier
finalize round. If ANY are still open/in-progress, this run is premature: create a successor
finalize bead (same spec file, `--deps <the still-open bead ids>`), close your own bead with
reason `"rearmed as <new-id>: chunks still in flight"`, and stop.

## Step 2: Verify every wiki page

Expected pages (2 total, one per source chunk):

- `wiki/01-claude-code-as-a-graph-engine.md` — should cover: the framing that Claude Code
  already ships graph-engineering primitives and that Anthropic's five "Building Effective
  Agents" patterns are graphs under a plainer name; the three-part mapping (nodes → subagents,
  edges → the orchestrator's runtime routing, shared state → returned results flowing back to
  the orchestrator); the three primitives in order of commitment (`.claude/agents/` subagent
  files, hooks as deterministic edges, the Claude Agent SDK `agents` parameter) and the
  hand-roll-then-lift-into-the-SDK ordering; and Anthropic's own multi-agent research system as
  existing proof, with the specific numbers preserved (90.2% improvement over a single-agent
  Claude Opus 4 baseline, ~15x the token cost of a normal chat turn, early over-spawning).
- `wiki/02-wiring-your-first-graph.md` — should cover: the step-by-step first-graph recipe
  (pick a splittable job, one narrow subagent per node, orchestrator routing with a loop-back
  edge on rejection, fan-out/fan-in for parallel work, hooks for edges that must always fire);
  the "when not to reach for a graph" caution (a graph of weak nodes is "slop produced in
  parallel"; nail the single loop first); the Related Content list; the full FAQ (5 questions);
  and the Sources & Verification list.

For each: check it exists, is non-trivial (this is a short article so pages will be shorter
than a book chapter — treat >20 lines as the trivia floor here, not the usual >40), matches the
format contract (backlink line, `**In one sentence:**`, `## Key points`, `---`, detail
sections, `**Covers:**` footer), and covers the whole assigned chunk (not just its opening
topic). Read the file's TAIL, not just its length — a known local-model failure mode is a
repetition loop that pads line count with nonsense. Build a BAD list and a GOOD list.

Neither chunk has an associated figure — do not flag missing images as a defect on this
source.

## Step 3: Handle BAD pages

If BAD is empty, go straight to Step 4. If BAD is non-empty: for each bad chunk, count
existing extract beads titled `"AIBuilderClubGraphEngineeringClaudeCode chunk NN extract"`
(any retry suffix) to get its attempt count.

- Attempt count < `RETRY_BUDGET` (3): delete the bad page, create ONE retry extract bead
  reusing `source/specs/NN-extract.md` verbatim (`--coder opencode --model
  ollama-rtx/qwen3.8:27b`), record its id.
- Attempt count >= `RETRY_BUDGET`: this chunk has exhausted reprocessing — write that one page
  by hand from `source/chunks/NN.txt`, following the same format contract shown in that
  chunk's own `NN-extract.md` spec file. Do not requeue it.

If any retries were created this round: create ONE successor finalize bead depending on all of
them (same spec file, `--cwd /Users/sergii/.kb --coder claude --model sonnet -p 1 -t task`),
close your own bead with reason `"rearmed as <new-id>: N chunk(s) requeued"`, and stop. If
every bad chunk was handled by hand-writing (nothing requeued), continue to Step 4 in this
same run.

## Step 4: Synthesize the rest of the wiki

Read `kb show summary/get` (Shared Output Conventions section) for the exact file specs, then
produce, reading only the wiki pages (small, 2 of them) and NOT the raw source except to
spot-check quality:

- `index.md` — front-matter with `type: Article`, title, one-sentence description, `generated:
  {by: claude/sonnet, at: <ISO-8601 UTC timestamp>}`, `sources:` with `id: original` (the URL
  above) and `id: local-copy` (`source/article.md`), 2-5 tags (e.g. `[agentic-systems,
  graph-engineering, claude-code, multi-agent, ai-engineering]`). Orientation paragraph, "How
  to work through this" ladder, "Read This Folder" links, wiki table (2 rows, reading order),
  "Original Source" link to `source/article.md`.
- `summary.md` — the A2-template from `summary/get` (Human Readable TL;DR, TL;DR, Problem &
  Motivation, Main Original Ideas, Key Findings, Suggestions & Future Directions, Authors &
  Institutions — attribute to "Shirley, AI Builder Club"). Use `**Article:** [Graph Engineering
  with Claude Code: Anthropic's Agent Graph](https://www.aibuilderclub.com/blog/graph-engineering-with-claude-code)
  — AI Builder Club, July 24 2026 (updated August 3 2026)` as the metadata line. No Figures
  section is needed (no images in this source). Keep under 300 lines (this is a short article —
  summary.md should land well under 100 lines).
- `digest.md` — copy each wiki page's `**In one sentence:**` line and `## Key points` bullets
  verbatim, in order (2 sections), then a short `## The argument in five moves` closing spine
  (5-7 numbered clauses). Target ~30-50 lines given the short source.
- `explainer.md` — plain-language layer per the shared spec: What is this about? / Why does it
  matter? / How does it work? / Where can this be used? / Conclusions & takeaways / Jargon
  decoder (5-8 terms: e.g. node, edge, shared state, orchestrator, subagent, hook, fan-out/
  fan-in, Claude Agent SDK). Target 80-120 lines.
- `questions.md` — 6-8 retrieval-practice questions (this is a short article per the Scaling by
  source size table), at least one per wiki page (so at least 3 per page given 2 pages), mixing
  core recall (e.g. what maps to nodes/edges/shared state in Claude Code; the 90.2%/15x numbers),
  elaboration (e.g. why hand-roll before reaching for the SDK), transfer, and one evaluation
  question drawing on `critical_thinking.md`. Answers ONLY inside collapsed `> [!tip]- Answer`
  callouts.
- `critical_thinking.md` — per the shared spec (Claims vs. evidence, Genuinely new vs.
  repackaged, Weaknesses and blind spots, Applicability with a "Relevance to my work"
  subsection for Sergii's AI/ML engineering and agentic-systems context, What this changes,
  Verdict ending in adopt/trial/watch/skip). Target 60-90 lines given the short source — do not
  pad. Note this source is promotional (an AI Builder Club course upsell embedded in the
  article) and its central evidence (the 90.2%/15x numbers) is borrowed from a different
  Anthropic post rather than original research — weigh that in "genuinely new vs. repackaged."
- `connections.md` — read `/Users/sergii/.kb/ai_papers/index.md` and check
  `/Users/sergii/.kb/papers/` for related entries. Several directly relevant candidates are
  already known to exist: `/Users/sergii/.kb/papers/AIBuilderClubGraphEngineeringGuide2026/`
  (the pillar article this piece links back to), `/Users/sergii/.kb/papers/TuringPostIsGraphEngineeringReal/`,
  `/Users/sergii/.kb/papers/GraphEngineeringVsLoopEngineering/`,
  `/Users/sergii/.kb/papers/LangGraph3YearsGraphEngineering/`,
  `/Users/sergii/.kb/papers/MarkTechPostPromptLoopGraph/` — read their `summary.md` files and
  link the ones genuinely related to this article's specific claims (subagents-as-nodes,
  orchestrator-workers, the same July 2026 X-thread origin story), plus any other 0-4 genuinely
  related entries found. Do not force links beyond what is genuinely related.

## Step 5: Report + close

Write a completion report to
`/Users/sergii/.kb/papers/AIBuilderClubGraphEngineeringClaudeCode/source/delegation_report.md`:
chunks total (2) / passed first try / requeued (how many rounds, if any) / hand-written after
exhausting retries (if any). Then:

`bd close <own-id> --reason "wiki complete"`

No git commands anywhere in this spec — `.kb` auto-syncs.
