# Task: Finalize — verify + synthesize the ArxivGraphAugmentedLLMAgents wiki

You are the last bead in a chunk-extraction chain for a knowledge-base entry summarizing the academic survey paper "Graph-Augmented Large Language Model Agents: Current Progress and Future Prospects" (arXiv 2507.21407, authors Yixin Liu, Guibin Zhang, Kun Wang, Shiyuan Li, Shirui Pan). This is the ONLY validation step in the whole pipeline.

Folder: `/Users/sergii/.kb/papers/ArxivGraphAugmentedLLMAgents/`

Manifest: `source/chunks.json` lists 5 chunks and their intended wiki pages:
1. `wiki/01-introduction-and-agent-framework.md`
2. `wiki/02-graphs-for-planning.md`
3. `wiki/03-graphs-for-memory-and-tools.md`
4. `wiki/04-graph-augmented-multi-agent-systems.md`
5. `wiki/05-future-directions-and-conclusion.md`

Retry budget per chunk: 3 attempts (initial + 2 retries). Worker model for any retries: `ollama-rtx/qwen3.8:27b` via `--coder opencode`.

## Step 1: Completeness gate (self-rearm)

List all beads matching "ArxivGraphAugmentedLLMAgents chunk" (e.g. `bd search "ArxivGraphAugmentedLLMAgents chunk"` or `bd list` + grep) — this also catches any retry beads created by an earlier finalize round. If ANY are still open/in-progress, this run is premature: create a successor finalize bead (same spec file `source/specs/finalize.md`, `--deps <the still-open bead ids>`), close your own bead with reason `"rearmed as <new-id>: chunks still in flight"`, and stop.

## Step 2: Verify every wiki page

For each of the 5 pages: check it exists, is non-trivial (>40 lines), matches the format contract used in the extract specs (backlink line, `# Title`, `**In one sentence:**`, `## Key points` with 5-8 substantive bullets, `---`, hierarchical `##` subsections with full detail, `**Covers:**` footer), covers the WHOLE chunk it was assigned (spot-check the chunk's last major topic, not just its opening), has no meta-junk (no leftover instructions, no "as an AI" preambles), and embeds any figures listed for it in `chunks.json` (`images: [...]`) as `![...](images/<file>.png)`. **Read the file's TAIL, not just its length** — a known local-model failure mode is a repetition loop that pads line count with nonsense.

Build a BAD list and a GOOD list.

## Step 3: Handle BAD pages

If BAD is empty, go straight to Step 4.

If BAD is non-empty: for each bad chunk, count existing extract beads titled `"ArxivGraphAugmentedLLMAgents chunk NN extract"` (any retry suffix) to get its attempt count.
- Attempt count < 3: delete the bad page, create ONE retry extract bead reusing `source/specs/NN-extract.md` verbatim (`--coder opencode --model ollama-rtx/qwen3.8:27b`), record its id.
- Attempt count >= 3: this chunk has exhausted reprocessing — write that one page by hand from `source/chunks/NN.txt` (last resort only). Do not requeue it.

If any retries were created this round: create ONE successor finalize bead depending on all of them (same spec file), close your own bead with reason `"rearmed as <new-id>: N chunk(s) requeued"`, and stop. If every bad chunk was handled by hand-writing (nothing requeued), continue to Step 4 in this same run.

## Step 4: Synthesize the remaining artifacts

Read the wiki pages (small — 5 pages, not the raw PDF, except to spot-check quality) and produce, following `kb show summary/get` conventions exactly (source-type label: `Paper`):

- `index.md` — front-matter (`type: Paper`, title, description, `generated: {by: claude/<model-id>, at: <ISO-8601 UTC timestamp>}`, `sources:` original arXiv URL `https://arxiv.org/abs/2507.21407` + local-copy path `source/2507.21407.pdf`, 2-5 tags), orientation paragraph, reading ladder, Read This Folder links, wiki table (5 rows, reading order), Original Source link.
- `summary.md` — the A2-template structure (Human Readable TL;DR, TL;DR, Problem & Motivation, Main Original Ideas, Key Findings — this is a survey so "findings" = the taxonomy/synthesis it offers, Suggestions & Future Directions drawn from wiki page 5, Authors & Institutions, Figures section referencing `wiki/images/fig1-agent-framework.png` if it adds information).
- `digest.md` — copy each wiki page's `**In one sentence:**` line and `## Key points` bullets verbatim, in order, then a closing `## The argument in five moves` (5-7 numbered steps, the survey's overall arc).
- `explainer.md` — plain-language layer, 80-150 lines, 5-12 jargon-decoder terms (e.g. "graph neural network", "multi-agent system", "knowledge graph", "topology", "graph foundation model").
- `questions.md` — 6-8 retrieval-practice questions (this is a short/article-length source), at least one per wiki page, mixing core recall / elaboration / transfer / one evaluation question drawing on `critical_thinking.md`.
- `critical_thinking.md` — skeptical-reviewer appraisal: this is a survey/position paper (no new experiments), so focus critique on: is the taxonomy well-motivated and complete, is it actually comprehensive vs. citation-dropping, how much of "Future Directions" is speculative vs. grounded, and a "Relevance to my work" section for Sergii's contexts (AI/ML engineering, agentic systems, Elisity data platform — this paper is directly relevant to graph engineering / multi-agent system design work). End with a one-word adoption call (adopt/trial/watch/skip).
- `connections.md` — read `/Users/sergii/.kb/ai_papers/index.md` and skim 2-3 plausible category files, plus `ls /Users/sergii/.kb/papers/` (note: several existing entries are about "graph engineering" for multi-agent orchestration — e.g. `GraphEngineeringVsLoopEngineering`, `LangGraph3YearsGraphEngineering`, `TuringPostIsGraphEngineeringReal`, `AIBuilderClubGraphEngineeringGuide2026`, `MarkTechPostPromptLoopGraph`, `TrueFoundryGraphEngineeringEnterprise`, `PrefectLoopsVsGraphs` — check if these exist and are genuinely related, since this arXiv paper is an academic survey of the same underlying idea from a different angle). Select 2-6 genuinely related entries; do not force links.

## Step 5: Report + close

Write a completion report to `source/delegation_report.md`: chunks total (5) / passed first try / requeued (how many rounds) / hand-written after exhausting retries. Then `bd close <own-id> --reason "wiki complete"`.

No git commands anywhere in this task — `.kb` auto-syncs.
