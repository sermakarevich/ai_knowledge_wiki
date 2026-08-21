# Task: Finalize ArxivLightRAG wiki — verify, retry, and synthesize

## Context

Source: "LightRAG: Simple and Fast Retrieval-Augmented Generation" (arXiv:2410.05779, EMNLP 2025). This is the last bead in a linear fleet chain. Five extract beads (chunk 01-05, local model `ollama-rtx/qwen3.8:27b`) were supposed to each write one wiki page under `/Users/sergii/.kb/papers/ArxivLightRAG/wiki/`. You are the ONLY validation step in this pipeline — read `kb show summary/get` and `kb show summary/get_local` first to recall the full output conventions (folder scaffold, wikilink rules, `index.md`/`digest.md`/`explainer.md`/`questions.md`/`critical_thinking.md`/`connections.md` specs) if you need the exact templates; the essentials are repeated below too.

Folder: `/Users/sergii/.kb/papers/ArxivLightRAG/`
Manifest: `/Users/sergii/.kb/papers/ArxivLightRAG/source/chunks.json` (chunk file → wiki page → images)
Retry budget: 3 attempts per chunk (initial + 2 retries)
Worker model for retries: `ollama-rtx/qwen3.8:27b` via `--coder opencode`

Expected wiki pages (5, per `chunks.json`):
1. `wiki/01-introduction-and-motivation.md`
2. `wiki/02-lightrag-architecture.md`
3. `wiki/03-evaluation-setup-and-main-results.md`
4. `wiki/04-ablation-case-study-cost-analysis.md`
5. `wiki/05-related-work-conclusion-appendix.md`

Extract specs (reused verbatim on retry) live at `source/specs/01-extract.md` through `05-extract.md`. Do not delete them.

## Step 1: Completeness gate (self-rearm if premature)

List all beads matching `"ArxivLightRAG chunk" extract` (use `fleet bd list` or `fleet bd search`, grep the title) — this also catches retry beads from an earlier finalize round. If ANY are still open/in-progress:
- Create a successor finalize bead: `fleet bd create "ArxivLightRAG finalize: verify + synthesize" --cwd /Users/sergii/.kb --coder claude --model sonnet -p 1 -t task --body-file /Users/sergii/.kb/papers/ArxivLightRAG/source/specs/finalize.md --deps "<the still-open bead ids>" --silent`
- Close your own bead: `fleet bd close <own-id> --reason "rearmed as <new-id>: chunks still in flight"`
- Stop.

If none are open/in-progress, continue to Step 2.

## Step 2: Verify every wiki page

For each of the 5 expected pages, check:
- It exists and is non-trivial (>40 lines).
- It matches the format contract: backlink line `> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]`, `# <Topic>`, `**In one sentence:**`, `## Key points` (5-8 substantive bullets), `---`, hierarchical detail sections, `**Covers:**` footer.
- It covers the WHOLE chunk — spot-check against the chunk's last major topic (read the tail of `source/chunks/NN.txt`), not just the opening.
- No meta-junk (no mention of "as an AI", no leftover instructions, no repetition-loop garbage padding line count — read the file's TAIL, not just its length, to catch this).
- Any figure named in the page text is actually embedded via `![...](images/...)` and the file exists in `wiki/images/`. Per `chunks.json`, chunk 02 must embed `fig1-architecture.png`; chunk 04 must embed `fig2-cost-comparison.png` and `fig3-retrieval-generation-example.png`; chunk 05 must embed all four of `fig4-graph-construction-prompt.png`, `fig5-query-generation-prompt.png`, `fig6-keyword-extraction-prompt.png`, `fig7-rag-evaluation-prompt.png`.

Build a BAD list (page number + reason) and a GOOD list.

## Step 3: Handle BAD pages (if any)

If BAD is empty, skip to Step 4.

For each bad chunk NN:
1. Count existing beads titled `"ArxivLightRAG chunk NN extract"` (including any `-retry` suffixed ones) to get its attempt count.
2. If attempt count < 3: delete the bad `wiki/NN-*.md` file, create ONE retry extract bead reusing `source/specs/NN-extract.md` verbatim:
   `fleet bd create "ArxivLightRAG chunk NN extract retry" --cwd /Users/sergii/.kb --coder opencode --model ollama-rtx/qwen3.8:27b -p 2 -t task --body-file /Users/sergii/.kb/papers/ArxivLightRAG/source/specs/NN-extract.md --silent`
   Record its id.
3. If attempt count >= 3: this chunk has exhausted retries. Write that one wiki page BY HAND from `source/chunks/NN.txt` (and figure descriptions per `chunks.json`), following the same format contract embedded in `source/specs/NN-extract.md`. Do not requeue it.

If any retries were created this round: create ONE successor finalize bead depending on all of them (`fleet bd create "ArxivLightRAG finalize: verify + synthesize" --cwd /Users/sergii/.kb --coder claude --model sonnet -p 1 -t task --body-file /Users/sergii/.kb/papers/ArxivLightRAG/source/specs/finalize.md --deps "<retry-ids-comma-separated>" --silent`), close your own bead with reason `"rearmed as <new-id>: N chunk(s) requeued"`, and stop.

If every bad chunk was handled by hand-writing (nothing requeued), continue to Step 4 in this same run.

## Step 4: Synthesize remaining artifacts

Read the wiki pages (small now — do not re-read the raw source except to spot-check quality). Produce, per `kb show summary/get` conventions:

- **`summary.md`** — the A2-template: title, `**Paper:** [LightRAG: Simple and Fast Retrieval-Augmented Generation (Guo et al., 2024)](https://arxiv.org/abs/2410.05779)`, `**Wiki:** [[index]] | **Digest:** [[digest]]`, Human Readable TL;DR, TL;DR, Problem & Motivation, Main Original Ideas, Key Findings (with a results table), Suggestions & Future Directions, Authors & Institutions, Figures section (embed `wiki/images/fig1-architecture.png` at minimum). Under 300 lines.
- **`digest.md`** — copy each wiki page's `**In one sentence:**` line and `## Key points` bullets verbatim, in order, one `##` section per page, then close with `## The argument in five moves` (5-7 numbered steps, the paper's overall arc). ~60-100 lines.
- **`index.md`** — OKF front-matter (`type: Paper`, `title`, `description`, `generated: {by: claude/sonnet, at: <ISO-8601 UTC>}`, `sources:` with `id: original` → `https://arxiv.org/abs/2410.05779` and `id: local-copy` → `source/2410.05779.pdf`, `tags:`), orientation paragraph, "How to work through this" ladder, "Read This Folder" links, wiki table (5 rows, reading order), "Original Source" link.
- **`explainer.md`** — plain-language layer, 80-150 lines, 5-12 jargon-decoder terms, sections: What is this about? / Why does it matter? / How does it work? / Where can this be used? / Conclusions & takeaways / Jargon decoder.
- **`questions.md`** — 6-8 retrieval-practice questions (short paper, <30pp scaling tier), at least one per wiki page (5 pages → at least 5 questions, pad to 6-8), mix core recall / elaboration / transfer / one evaluation question drawing on `critical_thinking.md`. Answers ONLY inside collapsed `> [!tip]- Answer` callouts, each linking its covering wiki page. Front-matter: `type: Retrieval Prompts`, `last_reviewed: null`, `review_count: 0`.
- **`critical_thinking.md`** — 60-120 lines: Claims vs. evidence, Genuinely new vs. repackaged (name the prior work — e.g. GraphRAG, HippoRAG, naive/vector RAG baselines), Weaknesses and blind spots, Applicability, "Relevance to my work" (2-4 bullets for Sergii's AI/ML engineering and agentic-systems context), What this changes, Verdict (ends with adopt/trial/watch/skip + the single strongest reason).
- **`connections.md`** — read `/Users/sergii/.kb/ai_papers/index.md` and skim 2-3 plausible category files (check especially any `graph_rag` category and `ls /Users/sergii/.kb/papers/` for `ArxivGraphRAGSurvey`, `ArxivHippoRAG`, and any other GraphRAG-collection entries already filed) for 2-6 genuinely related entries (builds-on / contradicts / same-problem-different-method / shares-technique / applies-in-practice). Do not force links.

All sub-files get backlinks: `> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]` inside `wiki/*.md`, and `> [[index|Wiki]] | [[summary|Summary]]` in the top-level files (`digest.md`, `explainer.md`, `questions.md`, `critical_thinking.md`, `connections.md`).

Use Obsidian `[[wikilink]]` syntax throughout. Source type is `Paper` (has authors + arXiv id, not a book).

## Step 5: Report and close

Write `/Users/sergii/.kb/papers/ArxivLightRAG/source/delegation_report.md`:
- Chunks total (5), passed first try (N), requeued (how many rounds), hand-written after exhausting retries (N).
- List of all files created.

No git commands — `.kb` auto-syncs.

Close your bead: `fleet bd close <own-id> --reason "wiki complete"`
