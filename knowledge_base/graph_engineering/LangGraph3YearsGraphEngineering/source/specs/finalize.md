# Finalize: verify + synthesize — LangGraph3YearsGraphEngineering

## Problem
Four extract beads have written (or are writing) the wiki pages for the source article "3 Years of Graph Engineering with LangGraph" (Sydney Runkle, Harrison Chase, LangChain blog, July 22, 2026, https://www.langchain.com/blog/3-years-of-graph-engineering-with-langgraph). This bead is the ONLY validation step in the pipeline and must also produce the rest of the KB folder.

Folder: `/Users/sergii/.kb/papers/LangGraph3YearsGraphEngineering/`
Manifest: `source/chunks.json` (chunk file → wiki page → topic mapping)
Extract specs (kept on disk, reusable verbatim for retries): `source/specs/01-extract.md` … `source/specs/04-extract.md`
Expected wiki pages: `wiki/01-modeling-agents-as-graphs.md`, `wiki/02-when-not-to-use-graphs.md`, `wiki/03-lessons-from-three-years.md`, `wiki/04-whats-new-and-the-bigger-idea.md`
Source text (for spot-checks / hand-writing a page as last resort only): `source/article.md`

RETRY_BUDGET = 3 attempts per chunk (initial + 2 retries). WORKER_MODEL = `ollama-rtx/qwen3.8:27b` (`--coder opencode`).

## Step 1: Completeness gate (self-rearm)

List beads matching title `"LangGraph3YearsGraphEngineering chunk"` and `"extract"` (`fleet bd search` or `fleet bd list` + grep) — this also catches retry beads. If ANY matching bead is still open/in-progress, this run is premature:
1. Create a successor finalize bead with the same spec file (`--body-file` = this file's absolute path), `--deps` = the still-open bead id(s).
2. `bd close <own-id> --reason "rearmed as <new-id>: chunks still in flight"`.
3. Stop — do not proceed to Step 2.

## Step 2: Verify every wiki page

For each of the 4 expected pages, check:
- File exists and is non-trivial (>40 lines).
- Matches the format contract in its own `NN-extract.md` spec (backlink line, `# Title`, `**In one sentence:**`, `## Key points` with 4+ real claims, `---`, hierarchical `##` detail, `**Covers:**` footer).
- Covers the WHOLE chunk — read the file's TAIL, not just its length, and confirm the chunk's last topic is actually present (e.g. page 03 must discuss dynamic transitions/`Send`, not just stop after the DAG lesson; page 04 must include "The bigger idea" section, not just "What's actually new").
- No meta-junk (no "as an AI", no echoed instructions, no repetition-loop padding).
- This source has no figures — do not flag missing images as a defect.

Build a BAD list and a GOOD list.

## Step 3: Handle BAD pages

If BAD is empty, go straight to Step 4.

If BAD is non-empty, for each bad chunk NN:
- Count existing beads titled `"LangGraph3YearsGraphEngineering chunk NN extract"` (including any retry suffix) to get its attempt count.
- If attempt count < 3: delete the bad `wiki/NN-*.md` file, create ONE retry extract bead reusing `source/specs/NN-extract.md` verbatim (`--coder opencode --model ollama-rtx/qwen3.8:27b -p 2 -t task --cwd /Users/sergii/.kb`), record its id.
- If attempt count >= 3: this chunk has exhausted its retry budget. Write that one page by hand, reading only `source/chunks/NN.txt`, following the same format contract as its spec file. Do not requeue it.

If any retries were created this round: create ONE successor finalize bead (same spec file) depending on all the new retry bead ids, `bd close <own-id> --reason "rearmed as <new-id>: N chunk(s) requeued"`, and stop.

If every bad chunk was handled by hand-writing (nothing requeued this round), continue to Step 4 in this same run.

## Step 4: Synthesize the rest of the folder

Read the 4 wiki pages (not the raw source, except to spot-check). Produce, per `kb show summary/get` conventions (Article source type, content track, `papers/` base — no date prefix):

- `index.md` — front-matter (`type: Article`), orientation paragraph (2-3 sentences on what the article argues), "How to work through this" ladder, Read This Folder links, wiki table (4 rows, reading order, one-line description each), Original Source link (`source/article.md`, retrieved 2026-08-18).
- `summary.md` — the A2-template: Human Readable TL;DR (analogy-first, zero jargon), technical TL;DR, Problem & Motivation, Main Original Ideas, Key Findings (this is an opinion/lessons-learned article, not an empirical paper — use this section for the three lessons and the deterministic-agentic-scale framing instead of quantitative results), Suggestions & Future Directions, Authors & Institutions (`Sydney Runkle, Harrison Chase — LangChain`). No Figures section (none exist). Metadata line: `**Article:** [3 Years of Graph Engineering with LangGraph](https://www.langchain.com/blog/3-years-of-graph-engineering-with-langgraph) — LangChain blog, 2026-07-22`. Under 300 lines.
- `digest.md` — copy each wiki page's `**In one sentence:**` and `## Key points` verbatim, in order, then a `## The argument in five moves` spine (5-7 numbered steps, one clause each, synthesized fresh).
- `explainer.md` — plain-language layer per the shared spec: What is this about?, Why does it matter?, How does it work?, Where can this be used?, Conclusions & takeaways, Jargon decoder (5-12 terms, e.g. "graph", "node", "edge", "DAG", "state machine", "Send", "map-reduce", "harness"). 80-150 lines.
- `questions.md` — 6-8 retrieval-practice questions (this is a short article: 3-5 wiki pages, 6-8 questions per the Scaling by source size table), at least one per wiki page, answers ONLY inside collapsed `> [!tip]- Answer` callouts, each answer linking its covering wiki page. Mix: about half core recall, a third elaboration ("why does X work?"), rest transfer + one evaluation question.
- `critical_thinking.md` — skeptical-reviewer appraisal: Claims vs. evidence (this is a practitioner opinion piece with no benchmarks — say so plainly; assess claims like "graphs are usually not DAGs" and "Send handles dynamic fan-out" against what is actually demonstrated vs. asserted), Genuinely new vs. repackaged (the article itself claims graph engineering is not new — take that claim seriously and evaluate it), Weaknesses and blind spots (no comparison to non-LangGraph frameworks, no cost/latency data, LangChain has a commercial interest in this framing), Applicability, "Relevance to my work" (Sergii's AI/ML engineering and agentic-systems contexts), What this changes, Verdict ending in adopt/trial/watch/skip. 60-120 lines.
- `connections.md` — read `/Users/sergii/.kb/ai_papers/index.md` and skim 2-3 plausible category files, plus `ls /Users/sergii/.kb/papers/`, for genuinely related entries (agentic systems, multi-agent orchestration, LangGraph/LangChain, loop engineering). Select 2-6 genuinely related entries, or state none found.

Use Obsidian `[[wikilink]]` syntax throughout; every sub-file gets the backlink line `> [[index|Wiki]] | [[summary|Summary]]` (wiki pages already have their own backlink line, already written).

## Step 5: Report and close

Write `source/delegation_report.md`: chunks total (4) / passed first try / requeued (how many rounds, if any) / hand-written after exhausting retries (if any).

`bd close <own-id> --reason "wiki complete"`.

## Scope & constraints
- No git commands — `.kb` auto-syncs.
- Do not run `fleet serve restart` or `fleet run`.
- Working directory: `/Users/sergii/.kb`
- Do not touch any other source's folder under `/Users/sergii/.kb/papers/` or `/Users/sergii/.kb/investment/`.
