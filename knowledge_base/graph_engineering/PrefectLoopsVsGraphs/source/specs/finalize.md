# Task: Finalize wiki for "Loops vs. Graphs" (Prefect blog, July 2026)

You are the last bead in a fleet chain that ingested this source into the KB. This is the ONLY validation step in the whole pipeline. Follow this spec exactly and self-contained — you were not part of the earlier planning session.

Folder: `/Users/sergii/.ai/knowledge/research/PrefectLoopsVsGraphs/`
Source: https://www.prefect.io/blog/loops-vs-graphs (article, ~1,500 words, 2 wiki chunks)
`WORKER_MODEL` = `ollama-rtx/qwen3.8:27b`, coder `opencode`. `RETRY_BUDGET` = 3 attempts per chunk.

## Step 1: Completeness gate (self-rearm)

List all beads matching `"PrefectLoopsVsGraphs chunk" extract` (`bd search` or `bd list` + grep) — this also catches any retry beads a prior finalize round may have created. If ANY are still open/in-progress: this run is premature. Create a successor finalize bead (same spec file `source/specs/finalize.md`, `--deps <the still-open bead ids>`, `--coder claude --model sonnet`), close your own bead with reason `"rearmed as <new-id>: chunks still in flight"`, and stop.

## Step 2: Verify every wiki page

Expected pages:
- `wiki/01-directed-agentic-graphs.md`
- `wiki/02-security-humans-and-strategy.md`

For each: check it exists, is non-trivial (>40 lines), matches the format contract (backlink line, `**In one sentence:**`, `## Key points` with 5-8 substantive bullets, `---`, full detail subsections, `**Covers:**` footer), covers the WHOLE chunk (spot-check the chunk's last major section, not just the opening — read the file's TAIL, not just its length, since a known failure mode is a repetition loop that pads line count with nonsense), and has no meta-junk. There are no figures in this source (no images to check). Build a BAD list and a GOOD list.

Source chunks (reuse verbatim if requeuing): `source/chunks/01.txt`, `source/chunks/02.txt`. Extract specs: `source/specs/01-extract.md`, `source/specs/02-extract.md`.

## Step 3: Handle BAD pages

If BAD is empty, go straight to Step 4. If BAD is non-empty, for each bad chunk NN:
- Count existing extract beads titled `"PrefectLoopsVsGraphs chunk NN extract"` (any retry suffix) to get its attempt count.
- Attempt count < 3: delete the bad page, create ONE retry extract bead reusing `source/specs/NN-extract.md` verbatim (`--coder opencode --model ollama-rtx/qwen3.8:27b`), record its id.
- Attempt count >= 3: exhausted retries — write that one page by hand from `source/chunks/NN.txt`, following the same format contract in the spec file. Do not requeue it.
- If any retries were created this round: create ONE successor finalize bead depending on all of them (same spec file, `--coder claude --model sonnet`), close your own bead with reason `"rearmed as <new-id>: N chunk(s) requeued"`, and stop. If every bad chunk was handled by hand-writing (nothing requeued), continue to Step 4 in this same run.

## Step 4: Synthesize remaining artifacts

Read the wiki pages (small, 2 files) — not the raw source, except to spot-check quality. Produce, per `ai show summary/get` conventions (this article routes to `research/`, type `Article`, no date prefix):

- `index.md` — front-matter (`type: Article`, title "Loops vs. Graphs", description, `generated: {by: claude/sonnet, at: <ISO-8601 UTC now>}`, `sources: [{id: original, resource: https://www.prefect.io/blog/loops-vs-graphs}, {id: local-copy, resource: source/page.html}]`, tags e.g. `[agent-engineering, graph-engineering, orchestration, prefect]`), orientation paragraph, "How to work through this" ladder, "Read This Folder" links, wiki table (2 rows), Original Source link.
- `summary.md` — the A2-template structure (Human Readable TL;DR, TL;DR, Problem & Motivation, Main Original Ideas, Key Findings, Suggestions & Future Directions, Authors & Institutions — no Figures section, this source has none). Metadata line: `**Article:** [Loops vs. Graphs](https://www.prefect.io/blog/loops-vs-graphs) — Prefect blog, 2026-07-22`.
- `digest.md` — copy each wiki page's `**In one sentence:**` line and `## Key points` bullets verbatim, in order, plus a closing "## The argument in five moves" (5-7 numbered steps, the article's overall arc).
- `explainer.md` — plain-language layer, 80-150 lines, 5-12 term jargon decoder (terms like "graph", "node", "edge", "DAG", "loop engineering", "Ralph loop", "directed agentic graph", "MCP").
- `questions.md` — retrieval-practice questions, 6-8 questions (article-length source per the Scaling table), at least one per wiki page, collapsed-answer callouts, mixing recall/elaboration/transfer plus one evaluation question drawing on `critical_thinking.md`.
- `critical_thinking.md` — skeptical review: claims vs. evidence (this is a company blog post advocating its own product — flag that explicitly), genuinely new vs. repackaged (compare to LangGraph/Pydantic AI/traditional DAG orchestration, which the source itself discusses), weaknesses/blind spots (no benchmarks, no named customers, no code/API shown), applicability, "Relevance to my work" (Sergii's contexts: AI/ML engineering, agentic systems, Elisity data platform), Verdict (adopt/trial/watch/skip + reason).
- `connections.md` — read `/Users/sergii/.ai/knowledge/research_topics/index.md` and skim 2-3 plausible category files, plus `ls /Users/sergii/.ai/knowledge/research/` for related recent entries (this source is one of several "graph engineering" research sources being ingested — look for sibling entries with similar titles/topics, e.g. anything about LangGraph, loop engineering, prompt engineering, or multi-agent orchestration). Select 2-6 genuinely related entries; if none, say so plainly.

## Step 5: Report and close

Write `source/delegation_report.md`: chunks total (2) / passed first try / requeued (how many rounds) / hand-written after exhausting retries. Then `bd close <own-id> --reason "wiki complete"`.

No git commands anywhere in this task — `.ai` auto-syncs. Do not run `fleet serve restart` or `fleet run`.
