# Finalize task: ArxivRAGvsGraphRAG — verify + synthesize

You are the finalize worker for a knowledge-base entry on the paper "RAG vs. GraphRAG: A Systematic Evaluation and Key Insights" (Han et al., 2025, arXiv:2502.11371, source: https://arxiv.org/abs/2502.11371). This is the ONLY validation step in the whole pipeline — no per-chunk validation happened upstream.

Folder: `/Users/sergii/.kb/papers/ArxivRAGvsGraphRAG/`

Read `kb show summary/get` for the shared output conventions (folder scaffold, wikilink rules, index.md/digest.md/explainer.md/questions.md/critical_thinking.md/connections.md specs) before writing the synthesis artifacts. Read `kb show summary/get_local` for the finalize-step contract this spec implements (Step 5).

Config: `WORKER_MODEL=ollama-rtx/qwen3.8:27b`, `RETRY_BUDGET=3` attempts per chunk.

## Step 1: Completeness gate (self-rearm)

List all beads matching `"ArxivRAGvsGraphRAG chunk" extract` (via `fleet bd search` or `fleet bd list` + grep) — this also catches any retry beads created by an earlier finalize round. If ANY are still open/in-progress, this run is premature:
- Create a successor finalize bead: `fleet bd create "ArxivRAGvsGraphRAG finalize: verify + synthesize" --cwd /Users/sergii/.kb --coder claude --model sonnet -p 1 -t task --body-file /Users/sergii/.kb/papers/ArxivRAGvsGraphRAG/source/specs/finalize.md --deps "<the still-open bead ids>" --silent`
- Close own bead: `bd close <own-id> --reason "rearmed as <new-id>: chunks still in flight"`
- Stop.

## Step 2: Verify every wiki page

There are 4 expected wiki pages (see `/Users/sergii/.kb/papers/ArxivRAGvsGraphRAG/source/chunks.json` for the chunk-to-page mapping):

1. `wiki/01-introduction-and-evaluation-framework.md`
2. `wiki/02-question-answering-results.md`
3. `wiki/03-summarization-and-conclusion.md`
4. `wiki/04-appendix-datasets-and-case-studies.md`

For each: check it exists, is non-trivial (>40 lines), matches the format contract (backlink line, `**In one sentence:**`, `## Key points` block, `---`, hierarchical detail, `**Covers:**` footer), covers the WHOLE chunk (spot-check the chunk's last major topic, not just the opening — read the corresponding `source/chunks/NN.txt` tail and confirm it's reflected), has no meta-junk (no "as an AI..." or task commentary), and embeds any figures the spec assigned to it (page 02 needs fig1/fig2/fig3; page 03 needs fig4; page 04 needs fig5/fig6). Read the file's TAIL, not just its length — a known local-model failure mode is a repetition loop that pads line count with nonsense.

Build a BAD list and a GOOD list.

## Step 3: Handle BAD pages (if any)

If BAD is empty, go straight to Step 4.

If BAD is non-empty: for each bad chunk, count existing extract beads titled `"ArxivRAGvsGraphRAG chunk NN extract"` (any retry suffix) to get its attempt count.
- Attempt count < 3: delete the bad wiki page file, create ONE retry extract bead reusing `source/specs/NN-extract.md` verbatim (`--coder opencode --model ollama-rtx/qwen3.8:27b -p 2 -t task`), record its id.
- Attempt count >= 3: this chunk has exhausted reprocessing — write that one wiki page by hand from `source/chunks/NN.txt` (last resort only). Do not requeue it.

If any retries were created this round: create ONE successor finalize bead depending on all of them (same command pattern as Step 1), close own bead with reason `"rearmed as <new-id>: N chunk(s) requeued"`, and stop.

If every bad chunk was handled by hand-writing (nothing requeued), continue to Step 4 in this same run.

## Step 4: Synthesize the remaining artifacts

Once all 4 wiki pages pass, produce, per `kb show summary/get` conventions (reading the wiki pages, not the raw source, except to spot-check quality):

- `index.md` — front-matter (`type: Paper`), orientation paragraph, "How to work through this" ladder, Read This Folder links, wiki table (4 rows, reading order), Original Source link to `source/2502.11371.pdf`.
- `summary.md` — the A2-template structure (Human Readable TL;DR, TL;DR, Problem & Motivation, Main Original Ideas, Key Findings with results table, Suggestions & Future Directions, Authors & Institutions, Figures section referencing the most important 1-2 figures). Metadata line: `**Paper:** [RAG vs. GraphRAG: A Systematic Evaluation and Key Insights (Han et al., 2025)](https://arxiv.org/abs/2502.11371)`.
- `digest.md` — copy each wiki page's `**In one sentence:**` line and `## Key points` bullets verbatim, in order, plus a closing "## The argument in five moves" spine (5-7 numbered steps).
- `explainer.md` — plain-language layer, 80-150 lines, 5-12 jargon-decoder terms (e.g. "RAG", "GraphRAG", "F1 score", "multi-hop QA", "LLM-as-a-Judge", "position bias", "knowledge graph community").
- `questions.md` — 6-8 retrieval-practice questions (this is a short paper, <30pp scaling tier), at least one per wiki page, answers only inside collapsed `> [!tip]- Answer` callouts, mixing core recall / elaboration / transfer / one evaluation question drawing on `critical_thinking.md`.
- `critical_thinking.md` — 60-120 lines: claims vs. evidence, genuinely new vs. repackaged, weaknesses/blind spots, applicability (including a "Relevance to my work" bullet list for Sergii's AI/ML engineering and agentic-systems context), what this changes, and a Verdict ending in one of adopt/trial/watch/skip with the strongest reason.
- `connections.md` — read `/Users/sergii/.kb/ai_papers/index.md` and skim `ls /Users/sergii/.kb/papers/` for related entries (this paper is part of a GraphRAG top-10 collection being ingested in parallel — look for sibling papers like ArxivGraphRAGSurvey, ArxivLightRAG, ArxivGraphRAGLocalToGlobal, HippoRAG if present). Select 2-6 genuinely related entries; if none exist yet, say so plainly (`_No related entries found in the KB as of <date>._`).

Use Obsidian `[[wikilink]]` syntax throughout; every sub-file gets a backlink line to `index` and `summary`.

## Step 5: Report + close

Write a completion report to `/Users/sergii/.kb/papers/ArxivRAGvsGraphRAG/source/delegation_report.md`: chunks total (4) / passed first try / requeued (how many rounds) / hand-written after exhausting retries.

Then `bd close <own-id> --reason "wiki complete"`.

No git commands anywhere in this task — `.kb` auto-syncs.

## Scope

Touch ONLY files under `/Users/sergii/.kb/papers/ArxivRAGvsGraphRAG/` and the beads described above.
