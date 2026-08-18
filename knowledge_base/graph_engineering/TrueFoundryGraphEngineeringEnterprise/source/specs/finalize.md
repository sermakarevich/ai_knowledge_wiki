# Finalize: verify + synthesize — TrueFoundryGraphEngineeringEnterprise

This is the ONLY validation step in the whole pipeline. You are a Claude worker running
headless. Follow this spec fully; it is self-contained.

Folder: `/Users/sergii/.kb/papers/TrueFoundryGraphEngineeringEnterprise/`

Source: TrueFoundry Blog article "Graph Engineering for Multi-Agent Systems: Architecture,
Governance, and Observability" by Boyu Wang, 2026-07-20.
URL: https://www.truefoundry.com/blog/graph-engineering-enterprise-guide

`WORKER_MODEL` = `ollama-rtx/qwen3.8:27b`, `RETRY_BUDGET` = 3 attempts per chunk.

## Step 1: Completeness gate (self-rearm)

List all beads matching "TrueFoundryGraphEngineeringEnterprise chunk * extract" (`fleet bd
search` or `fleet bd list` + grep) — this also catches any retry beads created by an earlier
finalize round. If ANY are still open/in-progress, this run is premature: create a successor
finalize bead (same spec file, `--deps <the still-open bead ids>`), close your own bead with
reason `"rearmed as <new-id>: chunks still in flight"`, and stop.

## Step 2: Verify the wiki page

Expected pages (1 total, one per source chunk — this is a single short blog post):

- `wiki/01-graph-engineering-enterprise-guide.md` — should cover: the definition of graph
  engineering and its distinction from knowledge-graph engineering; the three historical
  roots (dataflow computation, multi-agent systems research, organizational practice) and the
  "naming event" framing; the prompt/context/loop/graph layered hierarchy and why layers
  compose rather than supersede; enterprise governance (identity, gateway policy, tool-level
  restrictions, the four guardrail hooks, cross-agent prompt-injection risk); cost control
  (fan-out/retries, budget/rate-limit rules, the graph_id/node_id correlation pattern with its
  header example); observability (gateway metrics vs. orchestrator traces); structural/human
  approval checkpoints; optimization via node-level attribution; the seven-item enterprise
  checklist; the future-outlook predictions; the closing TrueFoundry perspective; the FAQ;
  the technical metrics (latency, throughput); and the Agent Harness product boundary
  statement.

For this page: check it exists, is non-trivial (this is a short article — treat >20 lines as
the triviality floor here, not the usual >40), matches the format contract (backlink line,
`**In one sentence:**`, `## Key points`, `---`, detail sections, `**Covers:**` footer), and
covers the WHOLE article (not just the opening definition — spot-check that the checklist,
FAQ, and metrics sections near the end are present too). Read the file's TAIL, not just its
length — a known local-model failure mode is a repetition loop that pads line count with
nonsense. Build a BAD list and a GOOD list (of at most one item each).

There are no figures/images for this source (a short text article with no diagrams
extracted) — do not flag missing images as a defect.

## Step 3: Handle a BAD page

If BAD is empty, go straight to Step 4. If BAD is non-empty (the one page failed): count
existing extract beads titled `"TrueFoundryGraphEngineeringEnterprise chunk 01 extract"` (any
retry suffix) to get its attempt count.

- Attempt count < `RETRY_BUDGET` (3): delete the bad page, create ONE retry extract bead
  reusing `source/specs/01-extract.md` verbatim (`--coder opencode --model
  ollama-rtx/qwen3.8:27b`), record its id.
- Attempt count >= `RETRY_BUDGET`: this chunk has exhausted reprocessing — write the page by
  hand from `source/chunks/01.txt`, following the same format contract shown in
  `source/specs/01-extract.md`. Do not requeue it.

If a retry was created this round: create ONE successor finalize bead depending on it (same
spec file, `--cwd /Users/sergii/.kb --coder claude --model sonnet -p 1 -t task`), close your
own bead with reason `"rearmed as <new-id>: chunk requeued"`, and stop. If the bad page was
handled by hand-writing instead, continue to Step 4 in this same run.

## Step 4: Synthesize the rest of the wiki

Read `kb show summary/get` (Shared Output Conventions section) for the exact file specs, then
produce, reading only the wiki page (small, just 1) and NOT the raw source except to
spot-check quality:

- `index.md` — front-matter with `type: Article`, title, one-sentence description,
  `generated: {by: claude/sonnet, at: <ISO-8601 UTC timestamp>}`, `sources:` with
  `id: original` (the URL above) and `id: local-copy` (`source/article.md`), 2-5 tags (e.g.
  `[agentic-systems, graph-engineering, multi-agent-systems, ai-governance, enterprise-ai]`).
  Orientation paragraph, "How to work through this" ladder, "Read This Folder" links, wiki
  table (1 row), "Original Source" link to `source/article.md`.
- `summary.md` — the A2-template from `summary/get` (Human Readable TL;DR, TL;DR, Problem &
  Motivation, Main Original Ideas, Key Findings, Suggestions & Future Directions, Authors &
  Institutions). Use `**Article:** [<Title>](<url>) — TrueFoundry Blog, 2026-07-20` as the
  metadata line. No Figures section (none exist). Keep well under 100 lines (very short
  source).
- `digest.md` — copy the wiki page's `**In one sentence:**` line and `## Key points` bullets
  verbatim, then a short `## The argument in five moves` closing spine (5-7 numbered clauses).
  Target ~30-50 lines given the short source.
- `explainer.md` — plain-language layer per the shared spec: What is this about? / Why does it
  matter? / How does it work? / Where can this be used? / Conclusions & takeaways / Jargon
  decoder (5-8 terms: e.g. graph engineering, node, edge, org graph, work graph, gateway,
  virtual account, guardrail hook). Target 80-120 lines.
- `questions.md` — 6-8 retrieval-practice questions (short article per the Scaling by source
  size table), at least one drawn from each major section (definition, layered hierarchy,
  governance/cost/observability, checklist, FAQ), mixing core recall, elaboration (e.g. "why
  do the four engineering layers compose rather than replace each other?"), transfer, and one
  evaluation question drawing on `critical_thinking.md`. Answers ONLY inside collapsed
  `> [!tip]- Answer` callouts.
- `critical_thinking.md` — per the shared spec (Claims vs. evidence, Genuinely new vs.
  repackaged — note this is a vendor blog post, so weigh how much is genuinely novel
  definitional work vs. marketing for TrueFoundry's own gateway/Agent Harness products,
  Weaknesses and blind spots, Applicability with a "Relevance to my work" subsection for
  Sergii's AI/ML engineering and agentic-systems context, What this changes, Verdict ending in
  adopt/trial/watch/skip). Target 60-90 lines given the short source — do not pad.
- `connections.md` — read `/Users/sergii/.kb/ai_papers/index.md` and check
  `/Users/sergii/.kb/papers/` for related entries. Several directly relevant candidates are
  already known to exist: `/Users/sergii/.kb/papers/TuringPostIsGraphEngineeringReal/`,
  `/Users/sergii/.kb/papers/GraphEngineeringVsLoopEngineering/`,
  `/Users/sergii/.kb/papers/LangGraph3YearsGraphEngineering/`,
  `/Users/sergii/.kb/papers/MarkTechPostPromptLoopGraph/`,
  `/Users/sergii/.kb/papers/AIBuilderClubGraphEngineeringGuide2026/`, and
  `/Users/sergii/.kb/papers/AIBuilderClubGraphEngineeringClaudeCode/` — read their
  `summary.md` files and link the ones genuinely related to this article's specific claims
  (same graph-engineering discourse, or the enterprise-governance angle specifically), plus
  any other 0-4 genuinely related entries found. Do not force links beyond what is genuinely
  related.

## Step 5: Report + close

Write a completion report to
`/Users/sergii/.kb/papers/TrueFoundryGraphEngineeringEnterprise/source/delegation_report.md`:
chunks total (1) / passed first try / requeued (how many rounds, if any) / hand-written after
exhausting retries (if any). Then:

`bd close <own-id> --reason "wiki complete"`

No git commands anywhere in this spec — `.kb` auto-syncs.
