# Task: finalize the Meta-Harness paper wiki (verify + synthesize)

You are the ONLY validation step in this pipeline. Read this whole spec before doing anything.

Paper: "Meta-Harness: End-to-End Optimization of Model Harnesses" (arXiv 2603.28052), authors Yoonho Lee, Roshen Nair, Qizheng Zhang, Kangwook Lee, Omar Khattab, Chelsea Finn (2026-03-30).

Folder: `/Users/sergii/.kb/papers/MetaHarness/`

Expected wiki pages (5 chunks total):
1. `wiki/01-motivation-and-related-work.md` (spec: `source/specs/01-extract.md`)
2. `wiki/02-method.md` (spec: `source/specs/02-extract.md`)
3. `wiki/03-classification-and-reasoning-experiments.md` (spec: `source/specs/03-extract.md`)
4. `wiki/04-coding-experiments-and-discussion.md` (spec: `source/specs/04-extract.md`)
5. `wiki/05-appendix-case-studies.md` (spec: `source/specs/05-extract.md`)

`RETRY_BUDGET` = 3 attempts per chunk (initial + 2 retries). `WORKER_MODEL` = `ollama-rtx/qwen3.8:27b`.

## Step 1: Completeness gate (self-rearm)

Run `bd list` (or `bd search "MetaHarness chunk"`) and find all beads titled `MetaHarness chunk NN extract` (including any retry-suffixed titles). If ANY are still open/in-progress, this run is premature:
- Create a successor finalize bead with the same spec file (this file), `--deps <ids of the still-open beads>`.
- Close your own bead with reason `"rearmed as <new-id>: chunks still in flight"`.
- Stop here.

## Step 2: Verify every wiki page

For each of the 5 expected pages, check:
- It exists.
- It is non-trivial (>40 lines).
- It matches the format contract in its `NN-extract.md` spec (backlink line, `# <Topic>`, `**In one sentence:**`, `## Key points` with 5-8 substantive bullets, `---`, hierarchical `##` detail sections, `**Covers:**` footer).
- It covers the WHOLE chunk — spot-check the chunk's last major topic (read the tail of the corresponding `source/chunks/NN.txt`), not just the opening.
- It has no meta-junk (no leftover instructions, no "I will now..." commentary, no repetition-loop padding — read the file's TAIL specifically, not just its length).
- It embeds every figure assigned to that chunk per `source/chunks.json` (chunk 01: fig1, fig2; chunk 03: fig3; chunk 05: fig4-fig9). A page that names a figure but doesn't embed `![...](images/<file>.png)` is bad.

Build a GOOD list and a BAD list.

## Step 3: Handle BAD pages

If BAD is empty, go straight to Step 4.

If BAD is non-empty, for each bad chunk NN:
- Count existing beads titled `MetaHarness chunk NN extract` (including retries) to get its attempt count.
- If attempt count < 3: delete the bad `wiki/NN-*.md` file, create ONE retry extract bead reusing `source/specs/NN-extract.md` verbatim:
  ```bash
  fleet bd create "MetaHarness chunk NN extract (retry)" --cwd /Users/sergii/.kb \
       --coder opencode --model ollama-rtx/qwen3.8:27b -p 2 -t task \
       --body-file /Users/sergii/.kb/papers/MetaHarness/source/specs/NN-extract.md --silent
  ```
  Record the returned id.
- If attempt count >= 3: this chunk has exhausted retries. Write that one wiki page by hand yourself, reading `source/chunks/NN.txt` directly and following the format contract in `source/specs/NN-extract.md`. Do not requeue it.

If any retries were created this round: create ONE successor finalize bead depending on all of them (same `--body-file` as this bead), close your own bead with reason `"rearmed as <new-id>: N chunk(s) requeued"`, and stop. If every bad chunk was handled by hand-writing (nothing requeued), continue to Step 4 in this same run.

## Step 4: Synthesize the remaining artifacts

Read the 5 wiki pages (small now — do not re-read the raw source except to spot-check a specific quality concern). Produce, per `kb show summary/get` conventions:

- **`summary.md`** — the standard paper template: Human Readable TL;DR, TL;DR, Problem & Motivation, Main Original Ideas, Key Findings (with a results table), Suggestions & Future Directions, Authors & Institutions, Figures section (only if figures add information beyond text — reference `wiki/images/fig1-teaser.png` and `wiki/images/fig2-search-loop.png` as the two most illustrative). Metadata line: `**Paper:** [Meta-Harness: End-to-End Optimization of Model Harnesses (Lee, Nair, Zhang, Lee, Khattab, Finn, 2026)](https://arxiv.org/abs/2603.28052)`. Keep under 300 lines.
- **`digest.md`** — copy each wiki page's `**In one sentence:**` line and `## Key points` bullets verbatim, in reading order (01 through 05), then close with `## The argument in five moves` (5-7 numbered steps synthesizing the paper's overall arc).
- **`index.md`** — OKF-style front-matter (`type: Paper`, title, one-sentence description, `generated: { by: claude/<model-id>, at: <ISO-8601 UTC timestamp> }`, sources (original: `https://arxiv.org/abs/2603.28052`, local-copy: `source/2603.28052.pdf`), 2-5 topical tags e.g. `[llm-agents, prompt-optimization, harness-engineering, agentic-coding]`), orientation paragraph, "How to work through this" ladder, "Read This Folder" links, wiki table (5 rows, reading order), "Original Source" link.
- **`explainer.md`** — plain-language explainer, no jargon, analogies-first, 80-150 lines, 5-12 term jargon decoder. Explain "harness" itself as a jargon term early since the whole paper hinges on it.
- **`questions.md`** — retrieval-practice questions. This is a short paper (<30pp bucket): write 6-8 questions, at least one per wiki page (5 pages → make sure appendix case-study material gets at least one), mixing core recall / elaboration / transfer, plus one evaluation question drawing on `critical_thinking.md`. Answers only inside collapsed `> [!tip]- Answer` callouts.
- **`critical_thinking.md`** — claims vs. evidence (evaluate the 3 headline results: text classification +7.7 pts/4x fewer tokens, math reasoning +4.7 pts avg across 5 models, TerminalBench-2 ranking), genuinely new vs. repackaged (vs. AlphaEvolve/OpenEvolve/TTT-Discover per Appendix E and Related Work), weaknesses/blind spots, applicability, "Relevance to my work" bullets for Sergii's contexts (AI/ML engineering, agentic systems, Elisity data platform — think about whether harness-search techniques could apply to Elisity's own agent tooling), "What this changes", Verdict ending in adopt/trial/watch/skip.
- **`connections.md`** — read `/Users/sergii/.kb/ai_papers/index.md`, skim 2-3 plausible category files, and `ls /Users/sergii/.kb/papers/` for unfiled recent entries (e.g. any GraphRAG / agent-skills papers already ingested). Select 2-6 genuinely related entries (relationship: builds-on / contradicts / same-problem-different-method / shares-technique / applies-in-practice). If nothing is genuinely related, write `_No related entries found in the KB as of <date>._` — do not force links.

Follow the exact templates and rules in `kb show summary/get` (Shared Output Conventions section, and template A2) for anything not spelled out above — run `kb show summary/get` yourself if you need the verbatim template.

## Step 5: Report and close

Write `source/delegation_report.md`: chunks total (5) / passed first try / requeued (how many rounds, if any) / hand-written after exhausting retries (if any).

Then `bd close <own-id> --reason "wiki complete"`.

No git commands anywhere in this task — `.kb` auto-syncs.
