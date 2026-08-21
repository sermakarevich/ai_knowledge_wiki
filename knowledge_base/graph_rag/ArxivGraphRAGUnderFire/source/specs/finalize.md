# Task: Finalize ArxivGraphRAGUnderFire wiki (verify + synthesize)

## Context

This is the last bead in a fleet chain that turns the paper "GraphRAG under Fire" (arXiv:2501.14050) into an LLM-wiki folder at `/Users/sergii/.kb/papers/ArxivGraphRAGUnderFire/`. Six local-model workers each extracted one wiki page from one chunk of the paper. You are the ONLY validation step in the whole pipeline — read `kb show summary/get_local` (Step 5) for the full protocol this spec implements, and `kb show summary/get` for the output conventions (index.md, digest.md, explainer.md, questions.md, critical_thinking.md, connections.md formats) referenced below.

Expected wiki pages (from `source/chunks.json`):
1. `wiki/01-introduction-and-threat-model.md`
2. `wiki/02-rq1-existing-attacks-fail.md`
3. `wiki/03-gragpoison-design.md`
4. `wiki/04-evaluation-results.md`
5. `wiki/05-defenses-related-work-conclusion.md`
6. `wiki/06-appendix-notations-and-attack-examples.md`

Extract spec files (reused verbatim for retries) live in `source/specs/NN-extract.md`. Worker model for retries: `ollama-rtx/qwen3.8:27b` via `--coder opencode --model ollama-rtx/qwen3.8:27b`. Retry budget: 3 attempts per chunk (initial + 2 retries).

## Step 1: Completeness gate (self-rearm)

List beads matching `ArxivGraphRAGUnderFire chunk` extract (`fleet bd list` or `fleet bd search`, grep by title) — this also catches retry beads from an earlier finalize round. If ANY are still open/in-progress: this run is premature. Create a successor finalize bead (same spec file `source/specs/finalize.md`, `--deps <the still-open bead ids>`), close your own bead with reason `"rearmed as <new-id>: chunks still in flight"`, and stop.

## Step 2: Verify every wiki page

For each of the 6 wiki pages: check it exists, is non-trivial (>40 lines), matches the format contract in the corresponding `source/specs/NN-extract.md` (backlink line, `**In one sentence:**`, `## Key points`, `---`, hierarchical detail, `**Covers:**` footer), covers the WHOLE chunk (spot-check the chunk's last major topic, not just the opening), has no meta-junk or repetition-loop padding (read the file's TAIL, not just its line count), and embeds any figures named in its extract spec. Build a BAD list and a GOOD list.

## Step 3: Handle BAD pages

If BAD is empty, go straight to Step 4.

If BAD is non-empty, for each bad chunk NN:
- Count existing extract beads titled `"ArxivGraphRAGUnderFire chunk NN extract"` (any retry suffix) to get its attempt count.
- Attempt count < 3: delete the bad page, create ONE retry extract bead reusing `source/specs/NN-extract.md` verbatim (`fleet bd create ... --coder opencode --model ollama-rtx/qwen3.8:27b -p 2 -t task --body-file source/specs/NN-extract.md --silent`), record its id.
- Attempt count >= 3: this chunk has exhausted reprocessing. Write that one page by hand from `source/chunks/NN.txt`, following the same format contract as in `source/specs/NN-extract.md`. Do not requeue it.

If any retries were created this round: create ONE successor finalize bead depending on all of them (`--deps <retry-id-1>,<retry-id-2>,...`), close your own bead with reason `"rearmed as <new-id>: N chunk(s) requeued"`, and stop. If every bad chunk was handled by hand-writing (nothing requeued), continue to Step 4 in this same run.

## Step 4: Synthesize the remaining artifacts

Follow `kb show summary/get` conventions exactly (Content track, Paper source-type). Read the wiki pages (small now), not the raw source, except to spot-check quality against `source/chunks/*.txt` if something looks off. Note: this is arXiv paper 2501.14050, "GraphRAG under Fire" by Jiacheng Liang, Yuhui Wang, Changjiang Li, Rongyi Zhu, Tanqiu Jiang, Neil Gong, Ting Wang (Stony Brook University, Duke University), 2025.

Produce, in `/Users/sergii/.kb/papers/ArxivGraphRAGUnderFire/`:

1. **`index.md`** — front-matter (`type: Paper`), orientation paragraph, "How to work through this" ladder, "Read This Folder" links, wiki table (6 rows, reading order), "Original Source" link to `source/2501.14050.pdf`.
2. **`summary.md`** — the A2-template structure from `kb show summary/get` (Human Readable TL;DR, TL;DR, Problem & Motivation, Main Original Ideas, Key Findings with a results table, Suggestions & Future Directions, Authors & Institutions, Figures section referencing `wiki/images/fig1-overview.png`). Metadata line: `**Paper:** [GraphRAG under Fire (Liang et al., 2025)](https://arxiv.org/abs/2501.14050)`. Keep under 300 lines.
3. **`digest.md`** — copy each wiki page's `**In one sentence:**` line and `## Key points` bullets verbatim, in order, then a `## The argument in five moves` spine.
4. **`explainer.md`** — plain-language layer per the spec (What is this about? / Why does it matter? / How does it work? / Where can this be used? / Conclusions & takeaways / Jargon decoder with 5-12 terms). Target 80-150 lines.
5. **`questions.md`** — 10 retrieval-practice questions (per the "Long paper" scaling row: 30-100pp -> 8-12 questions; this paper is 24pp so 10 is a good midpoint), at least one per wiki page, answers ONLY in collapsed `> [!tip]- Answer` callouts, mix of recall/elaboration/transfer plus one evaluation question drawing on `critical_thinking.md`.
6. **`critical_thinking.md`** — skeptical expert review: Claims vs. evidence, Genuinely new vs. repackaged, Weaknesses and blind spots, Applicability, "Relevance to my work" (Sergii's contexts: AI/ML engineering, agentic systems, Elisity data platform — this paper is directly relevant to anyone building GraphRAG-based retrieval), What this changes, Verdict (adopt/trial/watch/skip). Target 60-120 lines.
7. **`connections.md`** — read `/Users/sergii/.kb/ai_papers/index.md` and `ls /Users/sergii/.kb/papers/` for related GraphRAG/RAG-security entries already in the KB (e.g. any ArxivGraphRAGBench, ArxivHippoRAG, ArxivLightRAG, ArxivRAGvsGraphRAG folders present) and pick 2-6 genuinely related entries with the relationship type. If nothing is related, say so in one line.

## Step 5: Report and close

Write `source/delegation_report.md`: chunks total (6) / passed first try / requeued (how many rounds) / hand-written after exhausting retries. Then `fleet bd close <own-id> --reason "wiki complete"`.

## Scope & constraints

- Touch ONLY files under `/Users/sergii/.kb/papers/ArxivGraphRAGUnderFire/` and the beads you create/close.
- No git operations — `.kb` auto-syncs.
- Do not run `fleet serve restart` or `fleet run`.
