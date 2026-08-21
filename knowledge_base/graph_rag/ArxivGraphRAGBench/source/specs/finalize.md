# Task: Finalize ArxivGraphRAGBench wiki — verify + synthesize

## Context

You are the last bead in a fleet pipeline that turns the paper "GraphRAG-Bench: Challenging Domain-Specific Reasoning Benchmark for GraphRAG" (arXiv:2506.02404) into an LLM-wiki folder at `/Users/sergii/.kb/papers/ArxivGraphRAGBench/`. Four local-model workers each extracted one wiki page from one chunk of the paper. You are the ONLY validation step in this whole pipeline — no earlier step checked quality. Read `kb show summary/get` for the full output-format spec (front-matter conventions, wikilink rules, file specs for summary.md/digest.md/index.md/explainer.md/questions.md/critical_thinking.md/connections.md) before writing anything — follow it exactly.

Config: `WORKER_MODEL=ollama-rtx/qwen3.8:27b`, `RETRY_BUDGET=3` attempts per chunk.

## Step 1: Completeness gate (self-rearm)

List all beads matching `"ArxivGraphRAGBench chunk" extract` (use `fleet bd search` or `fleet bd list` + grep — this also catches any retry beads a previous finalize round may have created). If ANY are still open/in-progress, this run is premature:
- Create a successor finalize bead: `fleet bd create "ArxivGraphRAGBench finalize: verify + synthesize" --cwd /Users/sergii/.kb --coder claude --model sonnet -p 1 -t task --body-file /Users/sergii/.kb/papers/ArxivGraphRAGBench/source/specs/finalize.md --deps "<the still-open bead ids>" --silent`
- Close your own bead: `bd close <own-id> --reason "rearmed as <new-id>: chunks still in flight"`
- Stop.

## Step 2: Verify every wiki page

Expected pages (see `/Users/sergii/.kb/papers/ArxivGraphRAGBench/source/chunks.json` for the chunk→page mapping):

- `wiki/01-introduction-and-motivation.md` (chunk 01, embeds `images/fig1-overview.png`)
- `wiki/02-benchmark-design.md` (chunk 02, no figures)
- `wiki/03-evaluation-protocol-and-core-results.md` (chunk 03, no figures — but must contain Tables 2-5 reproduced with real numbers)
- `wiki/04-topic-analysis-observations-and-conclusion.md` (chunk 04, embeds `images/fig2-accuracy-by-topic.png` and `images/fig3-case-study.png`)

For each page, check:
1. It exists and is non-trivial (>40 lines).
2. It matches the format contract in its own spec file (`source/specs/NN-extract.md`): backlink line, `# <Topic>`, `**In one sentence:**`, `## Key points` (5-8 substantive bullets), `---`, full detail sections, footer `**Covers:**` line.
3. It covers the WHOLE chunk — spot-check the chunk's LAST major topic (e.g. for chunk 03, does the page actually cover Table 5 / reasoning results, not just stop after Table 2?), not just the opening.
4. No meta-junk (no "As an AI...", no leftover instructions, no repetition loops — **read the file's TAIL, not just its line count**; a known local-model failure mode is a repetition loop that pads line count with nonsense).
5. Any figure named in the page text is actually embedded via `![...](images/...)` — pages 01 and 04 must embed their assigned figures.

Build a BAD list and a GOOD list.

## Step 3: Handle BAD pages

If BAD is empty, go straight to Step 4.

If BAD is non-empty, for each bad chunk NN:
- Count existing extract beads titled `"ArxivGraphRAGBench chunk NN extract"` (including any retry suffix) to get its attempt count.
- Attempt count < 3: delete the bad page file, create ONE retry extract bead reusing `source/specs/NN-extract.md` verbatim: `fleet bd create "ArxivGraphRAGBench chunk NN extract retry" --cwd /Users/sergii/.kb --coder opencode --model ollama-rtx/qwen3.8:27b -p 2 -t task --body-file /Users/sergii/.kb/papers/ArxivGraphRAGBench/source/specs/NN-extract.md --silent`. Record its id.
- Attempt count >= 3: this chunk has exhausted reprocessing — write that one page by hand yourself, reading `source/chunks/NN.txt` directly, following the same format contract as the spec. Do not requeue it.

If any retries were created this round: create ONE successor finalize bead depending on all of them (same command pattern as Step 1), close your own bead with reason `"rearmed as <new-id>: N chunk(s) requeued"`, and stop. If every bad chunk was handled by hand-writing (nothing requeued), continue to Step 4 in this same run.

## Step 4: Synthesize the rest of the wiki folder

Per `kb show summary/get` conventions, read the (now-verified) wiki pages — NOT the raw source, except to spot-check — and produce:

- `index.md` — front-matter (`type: Paper`, title, description, `generated: {by: claude/sonnet, at: <ISO-8601 UTC>}`, sources pointing to the arXiv URL and `source/paper.pdf`, tags), orientation paragraph, reading ladder, wiki table (4 rows, in reading order), original source link.
- `summary.md` — rung 1, whole paper, shallow, ~2 min read. Metadata line: `**Paper:** [GraphRAG-Bench: Challenging Domain-Specific Reasoning Benchmark for GraphRAG (Xiao et al., 2025)](https://arxiv.org/abs/2506.02404)`.
- `digest.md` — rung 2, built by copying each wiki page's `**In one sentence:**` line and `## Key points` bullets verbatim, in order, plus a closing "The argument in five moves" section.
- `explainer.md` — plain-language layer, 80-150 lines, 5-12 jargon-decoder terms (GraphRAG, multi-hop reasoning, RAPTOR, HippoRAG, knowledge graph, rationale/AR metric, etc).
- `questions.md` — 6-8 retrieval-practice questions (short paper range) with collapsed answers, covering all 4 wiki pages evenly (at least one question per page).
- `critical_thinking.md` — claims vs evidence, applicability, what it changes, balanced verdict. E.g.: is a 1,018-question benchmark built from 20 textbooks generalizable claims-wise? Is using an LLM-as-judge for OE/FB accuracy and for the R/AR reasoning score itself a validity concern? Does "9 GraphRAG methods with GPT-4o-mini" generalize to other base LLMs?
- `connections.md` — links to related entries elsewhere in this KB. Search the KB for other GraphRAG-related papers (e.g. `papers/ArxivGraphRAGSurvey`, `papers/ArxivLightRAG`, `papers/ArxivHippoRAG`, or similar — check `/Users/sergii/.kb/papers/` for what actually exists) and link them via `[[papers/<Folder>/summary|<Title>]]` style links per the KB's cross-folder wikilink convention. If nothing directly related exists yet, say so briefly rather than inventing links.

## Step 5: Report + close

Write a completion report to `/Users/sergii/.kb/papers/ArxivGraphRAGBench/source/delegation_report.md`: chunks total (4) / passed first try / requeued (how many rounds) / hand-written after exhausting retries.

Then: `bd close <own-id> --reason "wiki complete"`.

## Constraints

- No git commands anywhere in this task — `.kb` auto-syncs.
- Do not run `fleet serve restart` or `fleet run`.
- Touch only files under `/Users/sergii/.kb/papers/ArxivGraphRAGBench/` and the beads you create/close.
