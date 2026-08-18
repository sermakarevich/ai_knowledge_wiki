# Task: finalize wiki for YouTubeWhatIsGraphEngineering (verify + synthesize)

You are the last bead in a chunk-extraction chain for the video "What Is Graph Engineering?" (KGP Talkie, https://www.youtube.com/watch?v=S1vqM0aTRFc). This is the ONLY validation step in the whole pipeline. Work entirely within `/Users/sergii/.kb/papers/YouTubeWhatIsGraphEngineering/`.

## Step 1: Completeness gate (self-rearm)

List all beads whose title matches `"YouTubeWhatIsGraphEngineering chunk" ` + `"extract"` (use `bd search` or `bd list` + grep) — this also catches any retry beads created by an earlier finalize round. If ANY are still open/in-progress, this run is premature:
- Create a successor finalize bead: same spec file (`source/specs/finalize.md`), `--deps <the still-open bead ids>`.
- Close own bead with reason `"rearmed as <new-id>: chunks still in flight"`.
- Stop here.

## Step 2: Verify every wiki page

Expected pages (per `source/chunks.json`):
- `wiki/01-graph-engineering-defined.md`
- `wiki/02-graph-engineering-vs-graphrag.md`
- `wiki/03-when-to-use-graph-engineering.md`

For each: check it exists, is non-trivial (>40 lines... note: these are short conceptual pages, so treat >25 lines as the trivia threshold given the source's brevity — but it MUST have a real `**In one sentence:**` line, a populated `## Key points` block with 5-8 substantive bullets, and populated detail subsections, not placeholder/template text), matches the format contract in the corresponding `source/specs/NN-extract.md` file, covers the WHOLE chunk (check the chunk's closing topic, not just its opening), has no meta-junk (no leftover instructions, no "as an AI" boilerplate), and has no repetition-loop garbage padding the file. Read each file's TAIL, not just its length.

Build a BAD list and a GOOD list.

## Step 3: Handle BAD pages (if any)

If BAD is empty, go straight to Step 4.

If BAD is non-empty: for each bad chunk, count existing extract beads titled `"YouTubeWhatIsGraphEngineering chunk NN extract"` (any retry suffix) to get its attempt count.
- Attempt count < 3 (RETRY_BUDGET): delete the bad page, create ONE retry extract bead reusing `source/specs/NN-extract.md` verbatim (`--coder opencode --model ollama-rtx/qwen3.8:27b`), record its id.
- Attempt count >= 3: this chunk has exhausted reprocessing — write that one page by hand from `source/chunks/NN.txt` (last resort only). Do not requeue it.

If any retries were created this round: create ONE successor finalize bead depending on all of them (same spec file), close own bead with reason `"rearmed as <new-id>: N chunk(s) requeued"`, and stop. If every bad chunk was handled by hand-writing (nothing requeued), continue to Step 4 in this same run.

## Step 4: Synthesize the rest of the wiki

Read the three wiki pages (small) — do not re-read the raw chunk files except to spot-check quality. This is a very short source (~9 minutes, no figures/tables/code), so keep outputs at the low end of normal sizing:

- **`index.md`** — front-matter with `type: Video`, title, one-sentence description, `generated: {by: claude/<model>, at: <ISO-8601 UTC now>}`, `sources: [{id: original, resource: https://www.youtube.com/watch?v=S1vqM0aTRFc}, {id: local-copy, resource: source/transcript.md}]`, `tags: [agentic-ai, graph-engineering, multi-agent, orchestration]`. Orientation paragraph (what the video is, its central claim: graph engineering = multiple coordinated loop-engineering solutions, not a new technique). "How to work through this" ladder (summary → digest → wiki pages). "Read This Folder" links (summary, digest, explainer, critical_thinking, questions, connections — no code sandbox for this source). Wiki table with the 3 pages in reading order. Original Source link to `source/transcript.md`.

- **`summary.md`** — use the Video metadata line: `**Video:** [What Is Graph Engineering?](https://www.youtube.com/watch?v=S1vqM0aTRFc) — KGP Talkie, ~9 min`. Follow the standard summary.md template (Human Readable TL;DR, TL;DR, Problem & Motivation, Main Original Ideas, Key Findings, Suggestions & Future Directions, Authors & Institutions — use "Lakshmikanth, KGP Talkie" for that section). No Figures section (no images).

- **`digest.md`** — copy each wiki page's `**In one sentence:**` line and `## Key points` bullets verbatim, in order, under numbered sections linking to each page. Close with `## The argument in five moves` (5-7 numbered one-clause steps spanning: the technique stack, loop-to-graph composition, the node concept, the GraphRAG distinction, and the cost-based decision rule).

- **`explainer.md`** — plain-language layer per the standard template (What is this about? / Why does it matter? / How does it work? / Where can this be used? / Conclusions & takeaways / Jargon decoder with 5-8 terms: prompt engineering, context engineering, harness engineering, loop engineering, graph engineering, node, GraphRAG). Target the low end, ~80-100 lines given the source's brevity.

- **`questions.md`** — 6 retrieval-practice questions (this is a short article-equivalent source, so 6-8 per the scaling table; use 6 given the thin content — one per wiki page plus 3 more spread across mechanism/transfer/evaluation). Follow the standard format (collapsed `> [!tip]- Answer` callouts, each answer linking its covering wiki page). At least one question per wiki page. Include one evaluation question drawing on `critical_thinking.md`.

- **`critical_thinking.md`** — standard template (Claims vs. evidence, Genuinely new vs. repackaged, Weaknesses and blind spots, Applicability, Relevance to my work — for Sergii's AI/ML engineering and agentic-systems work, What this changes, Verdict with adopt/trial/watch/skip). Be honest: this is a short, informal explainer video with no citations, no benchmarks, and self-reported cost multipliers (4x, 15x) with no methodology given — the critique should reflect that directly rather than treating the numbers as measured facts. Likely verdict is "watch" or similar given it's a terminology/framing piece rather than a technical contribution.

- **`connections.md`** — read `/Users/sergii/.kb/ai_papers/index.md`, then `ls /Users/sergii/.kb/papers/` for related recent entries. This source is one of ~10 sources on graph engineering being ingested together — look specifically for sibling `papers/` entries whose names suggest graph engineering, loop engineering, or agent topology (e.g. any folder with "Graph" or "Loop" or "Agent" in the name) and link 2-6 genuinely related entries with the relationship type (builds-on / contradicts / same-problem-different-method / shares-technique / applies-in-practice). If none found, say so plainly.

## Step 5: Report and close

Write `source/delegation_report.md`: chunks total (3) / passed first try / requeued (how many rounds) / hand-written after exhausting retries.

Then `bd close <own-id> --reason "wiki complete"`.

No git commands anywhere in this task — `.kb` auto-syncs.
