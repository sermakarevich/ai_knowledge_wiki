# Task: finalize wiki for ArxivGoAgentTopologyGeneration (verify + synthesize)

This is a Claude worker bead — the ONLY validation step in the whole pipeline for this source. Self-contained; you have no memory of how the chunk-extract beads ran.

**Source:** GoAgent: Group-of-Agents Communication Topology Generation for LLM-based Multi-Agent Systems, arXiv:2603.19677 (a `Paper`, routed to `papers/` — no date prefix).
**Folder:** `/Users/sergii/.kb/papers/ArxivGoAgentTopologyGeneration/`
**Manifest:** `source/chunks.json` lists all 4 chunks, their intended wiki pages, and their figures.

## Step 1: Completeness gate (self-rearm)

List all beads matching title `"ArxivGoAgentTopologyGeneration chunk"` extract (`bd search` or `bd list` + grep — includes any retry beads). If ANY are still open/in-progress, this run is premature:
- Create a successor finalize bead: `fleet bd create "ArxivGoAgentTopologyGeneration finalize: verify + synthesize" --cwd /Users/sergii/.kb --coder claude --model sonnet -p 1 -t task --body-file /Users/sergii/.kb/papers/ArxivGoAgentTopologyGeneration/source/specs/finalize.md --deps "<the still-open bead ids>" --silent`
- Close own bead: `bd close <own-id> --reason "rearmed as <new-id>: chunks still in flight"`
- Stop.

## Step 2: Verify every wiki page

Expected pages (from `source/chunks.json`):
- `wiki/01-problem-and-motivation.md`
- `wiki/02-method.md`
- `wiki/03-experiments-and-related-work.md`
- `wiki/04-appendix-and-implementation.md`

For each: check it exists, is non-trivial (>40 lines), matches the format contract in its spec file (`source/specs/NN-extract.md`) — backlink line, `**In one sentence:**`, `## Key points` (5-8 substantive bullets), `---`, hierarchical `##` subsections, footer `**Covers:**` line. Check it covers the WHOLE chunk (spot-check the chunk's LAST major topic per `source/chunks.json`'s "covers" field, not just the opening). Read the file's TAIL, not just line count — a known local-model failure mode is a repetition loop padding line count with nonsense. Confirm named figures are actually embedded (`![...](images/fig*.png)` present, matching `source/chunks.json`'s `images` field for that chunk). Build a BAD list and a GOOD list.

## Step 3: Handle BAD pages

**If BAD is empty**, go straight to Step 4.

**If BAD is non-empty:** for each bad chunk NN, count existing extract beads titled `"ArxivGoAgentTopologyGeneration chunk NN extract"` (any retry suffix) to get its attempt count. Retry budget is 3 attempts (initial + 2 retries).

- Attempt count < 3: delete the bad page, create ONE retry extract bead reusing `source/specs/NN-extract.md` verbatim: `fleet bd create "ArxivGoAgentTopologyGeneration chunk NN extract (retry)" --cwd /Users/sergii/.kb --coder opencode --model ollama-rtx/qwen3.8:27b -p 2 -t task --body-file /Users/sergii/.kb/papers/ArxivGoAgentTopologyGeneration/source/specs/NN-extract.md --silent`. Record its id.
- Attempt count >= 3: this chunk has exhausted reprocessing — write that one page by hand from `source/chunks/NN.txt` (last resort only). Do not requeue it.

If any retries were created this round: create ONE successor finalize bead depending on all of them (same command pattern as Step 1, `--deps` = the new retry bead ids), close own bead with reason `"rearmed as <new-id>: N chunk(s) requeued"`, and stop. If every bad chunk was handled by hand-writing (nothing requeued), continue to Step 4 in this same run.

## Step 4: Synthesize remaining artifacts

Read the 4 wiki pages (small now, ~100-200 lines each) — not the raw source, except to spot-check quality if something looks off. Produce, per `kb show summary/get` conventions:

1. **`index.md`** — front-matter `type: Paper`, orientation paragraph (2-3 sentences on what GoAgent is and why it matters), "How to work through this" ladder, "Read This Folder" links, wiki table (4 rows, reading order, one-line description each), Original Source link (`source/2603.19677.pdf`, retrieved 2026-08-18).
2. **`summary.md`** — per the A2-template: Human Readable TL;DR, TL;DR, Problem & Motivation, Main Original Ideas, Key Findings (include the results table with exact numbers from `wiki/03-experiments-and-related-work.md`), Suggestions & Future Directions, Authors & Institutions (Hangzhou Dianzi University, RMIT University, Griffith University), Figures section (pick 1-2 of the 5 embedded figures that carry the most information — e.g. fig1 and fig3 — with relative paths `wiki/images/...`).
3. **`digest.md`** — copy each wiki page's `**In one sentence:**` line and `## Key points` bullets verbatim, in reading order, then a `## The argument in five moves` synthesis closing section (5-7 numbered steps: the paper's arc from problem to method to results).
4. **`explainer.md`** — plain-language, no ML jargon assumed, 80-150 lines: What is this about / Why does it matter / How does it work / Where can this be used / Conclusions & takeaways / Jargon decoder (5-12 terms, e.g. "multi-agent system", "communication topology", "information bottleneck", "autoregressive generation", "prompt injection attack").
5. **`questions.md`** — 6-8 retrieval-practice questions (this is a short paper, 12 pages), at least one per wiki page, front-matter `type: Retrieval Prompts, last_reviewed: null, review_count: 0`, answers in collapsed `> [!tip]- Answer` callouts linking the covering wiki page. Mix: ~half core recall, ~a third elaboration ("why does X work"), rest transfer + one evaluation question drawing on `critical_thinking.md`.
6. **`critical_thinking.md`** — skeptical review: Claims vs. evidence, Genuinely new vs. repackaged (name prior work: AgentPrune, G-Designer, ARG-Designer, EIB-LEARNER — from Related Work), Weaknesses and blind spots, Applicability, "Relevance to my work" (2-4 bullets for Sergii's AI/ML engineering and agentic-systems contexts), What this changes, Verdict (adopt/trial/watch/skip + strongest reason).
7. **`connections.md`** — read `/Users/sergii/.kb/ai_papers/index.md` and skim 2-3 plausible category files (multi-agent systems, graph-based methods, information bottleneck/regularization), plus `ls /Users/sergii/.kb/papers/` for related unfiled entries (e.g. any other graph-engineering or multi-agent-topology sources ingested around 2026-08-18, such as ArxivGraphAugmentedLLMAgents if it exists). Select 2-6 genuinely related entries; do not force links.

All seven files use `[[wikilink]]` syntax per the Wikilink rules (backlink line at top of every sub-file, `[[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]` style inside `wiki/` pages already written by the extract beads).

## Step 5: Report and close

Write `source/delegation_report.md`: chunks total (4) / passed first try / requeued (how many rounds, if any) / hand-written after exhausting retries (if any).

Then: `bd close <own-id> --reason "wiki complete"`.

No git commands anywhere in this task — `.kb` auto-syncs.
