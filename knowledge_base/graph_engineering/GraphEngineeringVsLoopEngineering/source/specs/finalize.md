# Finalize: verify + synthesize -- GraphEngineeringVsLoopEngineering

## Context

This is the last bead in a fleet pipeline (`kb show summary/get_local`) that turns a YouTube
video transcript into an English-language knowledge-base wiki entry at
`/Users/sergii/.kb/papers/GraphEngineeringVsLoopEngineering/`. Six local-model worker tasks
(chunk 01 through chunk 06 extract) each wrote one wiki page from one chunk of the (Chinese)
transcript, translating and synthesizing into English. This bead is the ONLY validation step in
the whole pipeline -- read `kb show summary/get_local` and `kb show summary/get` for full
conventions if anything below is ambiguous.

Video metadata (for `index.md` / `summary.md`):
- Title (English): What Is Graph Engineering? From Loop Engineering to Multi-Agent Orchestration
- Title (original): 什么是图工程 | Graph Engineering | 循环工程 | Loop Engineering | 多智能体 |
  LangGraph | ReAct | 提示词工程 | 工作流编排 | 验证器
- Channel: 最佳拍档 (Zuì Jiā Pāi Dàng), host 大飞 (Dafei)
- URL: https://www.youtube.com/watch?v=8RedSkw1UjE
- Duration: ~20:11
- `type:` Video (see Source-type labels in `kb show summary/get`)
- Metadata line: `**Video:** [What Is Graph Engineering? From Loop Engineering to Multi-Agent Orchestration](https://www.youtube.com/watch?v=8RedSkw1UjE) — 最佳拍档 (大飞), ~20 min`
- Route: `/Users/sergii/.kb/papers/` (AI/agent-engineering topic, not investment-related). No date prefix.
- No figures/images in this source (talking-head commentary video, no charts extracted) -- `wiki/images/` stays empty; do not invent a Figures section.

## Step 1: Completeness gate (self-rearm)

List all beads matching "GraphEngineeringVsLoopEngineering chunk" extract (`bd search` or
`bd list` + grep) -- this also catches any retry beads created by an earlier finalize round. If
ANY are still open/in-progress, this run is premature:
- Create a successor finalize bead: `fleet bd create "GraphEngineeringVsLoopEngineering finalize: verify + synthesize" --cwd /Users/sergii/.kb --coder claude --model sonnet -p 1 -t task --body-file /Users/sergii/.kb/papers/GraphEngineeringVsLoopEngineering/source/specs/finalize.md --deps "<still-open bead ids, comma separated>" --silent`
- Close own bead with reason `"rearmed as <new-id>: chunks still in flight"`.
- Stop.

## Step 2: Verify every wiki page

For each of the 6 expected pages below, check: it exists, is non-trivial (>40 lines), matches
the wiki page format contract (backlink line, `**In one sentence:**`, `## Key points` with 5-8
substantive bullets, `---`, hierarchical detail sections, `**Covers:**` footer), is written in
English (no leftover Chinese text), and covers the WHOLE topic assigned to it -- spot-check the
page's LAST major subsection, not just its opening. Read the file's TAIL, not just its length --
a known local-model failure mode is a repetition loop that pads line count with nonsense.

Expected pages (`wiki/`):
- `01-five-layer-evolution.md` -- prompt/context/harness/loop engineering layers + the five flaws of loops + goal blindness/Goodhart's Law example
- `02-anatomy-of-a-graph.md` -- V/E/S/P formalism, not a flowchart, not a knowledge graph
- `03-graph-topologies.md` -- fan-out/fan-in, orchestrator-workers, pipeline, routing, evaluator-optimizer, simplicity-first, framework abstraction caveat
- `04-verification-and-determinism.md` -- verifier/router, three verification styles, code+reality anchors
- `05-worked-example-loop-vs-graph.md` -- daily research brief case study, costs/tradeoffs
- `06-when-to-graph-frameworks-and-governance.md` -- Anthropic cost data + 3 valid multi-agent use cases, work-graph vs role-graph governance, LangGraph/CrewAI/AutoGen/ADK comparison, durable execution, graph vs ReAct vs old workflows, 3 closing recommendations

Build a BAD list and a GOOD list.

## Step 3: Handle BAD pages

If BAD is empty, go straight to Step 4.

If BAD is non-empty: for each bad page, count existing extract beads titled
"GraphEngineeringVsLoopEngineering chunk NN extract" (any retry suffix) to get its attempt
count.
- Attempt count < 3: delete the bad page, create ONE retry extract bead reusing
  `source/specs/NN-extract.md` verbatim (`--coder opencode --model ollama-rtx/qwen3.8:27b`),
  record its id.
- Attempt count >= 3: this chunk has exhausted reprocessing -- write that one page by hand from
  `source/chunks/NN.txt` (translate + follow the same format contract used in the spec file).
  Do not requeue it.

If any retries were created this round: create ONE successor finalize bead depending on all of
them (same command shape as Step 1), close own bead with reason `"rearmed as <new-id>: N
chunk(s) requeued"`, and stop. If every bad page was handled by hand-writing (nothing requeued),
continue to Step 4 in this same run.

## Step 4: Synthesize

Read the 6 wiki pages (small, already written) -- not the raw transcript, except to spot-check
quality. Produce, per `kb show summary/get` conventions:

- `index.md` -- front-matter (`type: Video`), orientation paragraph, "How to work through this"
  ladder, Read This Folder links, wiki table (6 rows, reading order), Original Source link to
  `source/transcript.md`.
- `summary.md` -- the A2-template structure (Human Readable TL;DR, TL;DR, Problem & Motivation,
  Main Original Ideas, Key Findings, Suggestions & Future Directions, Authors & Institutions --
  use "Presenter" for the video host in place of Authors). Under 300 lines. Use the Video
  metadata line given above.
- `digest.md` -- copy each page's `**In one sentence:**` and `## Key points` verbatim, in
  reading order, then close with `## The argument in five moves` (5-7 numbered steps).
- `explainer.md` -- plain-language layer for a reader with no background (80-150 lines,
  5-12 jargon-decoder terms e.g. "loop engineering", "fan-out/fan-in", "checkpointer",
  "Goodhart's Law", "orchestrator-workers").
- `questions.md` -- 8-12 retrieval-practice questions (Scaling by source size: this is a
  long/dense video), at least one per wiki page, answers only inside collapsed
  `> [!tip]- Answer` callouts, mix of core recall / elaboration / transfer / one evaluation
  question drawing on `critical_thinking.md`.
- `critical_thinking.md` -- skeptical review: e.g. how solid is the 90.2%-with-15x-tokens claim
  (single internal Anthropic eval, no external replication), is "graph engineering" genuinely
  novel vs. LangGraph/AutoGen/ADK practice from 2+ years prior, applicability conditions, ending
  with one of adopt/trial/watch/skip.
- `connections.md` -- read `/Users/sergii/.kb/ai_papers/index.md` and skim 2-3 plausible
  category files, plus `ls /Users/sergii/.kb/papers/` for unfiled recent entries (e.g. any
  agent-skills / agent-harness papers already ingested), and link 2-6 genuinely related entries.
  If none, say so explicitly.

## Step 5: Report + close

Write a completion report to
`/Users/sergii/.kb/papers/GraphEngineeringVsLoopEngineering/source/delegation_report.md`:
chunks total (6) / passed first try / requeued (how many rounds) / hand-written after
exhausting retries.

Then `bd close <own-task-id> --reason "wiki complete"`.

No git commands anywhere in this spec -- `.kb` auto-syncs.
