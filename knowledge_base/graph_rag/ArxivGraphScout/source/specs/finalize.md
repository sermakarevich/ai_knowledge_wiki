# Task: Finalize — verify + synthesize the ArxivGraphScout KB wiki

You are the finalize worker for the paper "GraphScout: Empowering Large Language Models with Intrinsic Exploration Ability for Agentic Graph Reasoning" (Ying et al., 2026-03; arXiv:2603.01410). Folder: `/Users/sergii/.kb/papers/ArxivGraphScout/`.

This is the ONLY validation step in the whole pipeline. Follow `kb show summary/get_local` Step 5 exactly; this spec restates it self-contained for this specific paper.

## Step 1: Completeness gate (self-rearm)

List beads matching `"ArxivGraphScout chunk" extract` (`fleet bd list` or `fleet bd search`, grep the title) — this also catches any retry beads created by an earlier finalize round. If ANY are still open/in-progress: this run is premature. Create a successor finalize bead (same spec file `source/specs/finalize.md`, `--deps <the still-open bead ids>`), close your own bead with reason `"rearmed as <new-id>: chunks still in flight"`, and stop.

## Step 2: Verify every wiki page

Check each of these 4 files exists and is good:

- `wiki/01-motivation-and-related-work.md`
- `wiki/02-graphscout-method.md`
- `wiki/03-experiments-and-results.md`
- `wiki/04-implementation-details-and-appendix.md`

For each: exists, non-trivial (>40 lines), matches the format contract in its own `source/specs/NN-extract.md` file (headline sentence, Key points block, full detail sections, footer `**Covers:**` line), covers the WHOLE chunk (spot-check the LAST major topic listed in that page's extract spec, not just the opening), no meta-junk (no "As an AI..." preambles, no leftover instruction text), and embeds the figure(s) listed in its spec (check the `![...](images/...)` markdown actually appears). **Read the file's TAIL, not just line count** — a known local-model failure mode is a repetition loop that pads line count with nonsense near the end.

Build a BAD list and a GOOD list.

## Step 3: Handle BAD pages

If BAD is empty, go straight to Step 4.

If BAD is non-empty: for each bad chunk NN, count existing extract beads titled `"ArxivGraphScout chunk NN extract"` (including any retry-suffixed titles) to get its attempt count. `RETRY_BUDGET` = 3.

- Attempt count < 3: delete the bad `wiki/NN-*.md` page, create ONE retry extract bead reusing `source/specs/NN-extract.md` verbatim (`--coder opencode --model ollama-rtx/qwen3.8:27b`, `--cwd /Users/sergii/.kb`), record its id.
- Attempt count >= 3: exhausted. Write that one page by hand from `source/chunks/NN.txt` (last resort only). Do not requeue it.

If any retries were created this round: create ONE successor finalize bead depending on all of them (`--deps` = comma-joined retry ids, `--body-file source/specs/finalize.md`), close your own bead with reason `"rearmed as <new-id>: N chunk(s) requeued"`, and stop. If every bad chunk was handled by hand-writing (nothing requeued), continue to Step 4 in this same run.

## Step 4: Synthesize the remaining artifacts

Read the 4 wiki pages (small now — do not re-read the raw source chunks except to spot-check quality) and produce, per `kb show summary/get` conventions (Content Track — Paper):

- `summary.md` — the standard paper `summary.md` template (Human Readable TL;DR, TL;DR, Problem & Motivation, Main Original Ideas, Key Findings incl. a results table, Suggestions & Future Directions, Authors & Institutions, Figures section referencing `wiki/images/fig1-motivation-comparison.png` and `wiki/images/fig2-graphscout-architecture.png`). Metadata line: `**Paper:** [GraphScout: Empowering Large Language Models with Intrinsic Exploration Ability for Agentic Graph Reasoning (Ying et al., 2026)](https://arxiv.org/abs/2603.01410)`. Keep under 300 lines.
- `digest.md` — built by copying each wiki page's `**In one sentence:**` line and `## Key points` bullets verbatim, in order (01 -> 04), plus a closing `## The argument in five moves` (5-7 numbered clauses spanning motivation -> method -> training -> results -> positioning).
- `index.md` — front-matter with `type: Paper`, title, one-sentence description, `generated: { by: claude/<model-id>, at: <ISO-8601 UTC timestamp> }`, `sources:` (id: original -> `https://arxiv.org/abs/2603.01410`, id: local-copy -> `source/2603.01410.pdf`), tags (e.g. `[graphrag, agentic-graph-reasoning, knowledge-graphs, llm-post-training, reinforcement-learning]`). Body: orientation paragraph, "How to work through this" ladder, "Read This Folder" links, the 4-row wiki table in reading order, "Original Source" link to `source/2603.01410.pdf`.
- `explainer.md` — plain-language layer per the shared spec (What is this about? / Why does it matter? / How does it work? / Where can this be used? / Conclusions & takeaways / Jargon decoder with 5-12 terms, e.g. "knowledge graph", "GraphRAG", "agentic", "post-training", "GRPO", "ablation", "clue node").
- `questions.md` — 6-8 retrieval-practice questions (this is a ~19-page paper, in the "Article/short paper <30pp" band of the Scaling by source size table), at least one per wiki page, front-matter `type: Retrieval Prompts`, `last_reviewed: null`, `review_count: 0`. Answers ONLY inside collapsed `> [!tip]- Answer` callouts, each linking its covering wiki page. Mix: ~half core recall, ~a third elaboration, rest transfer + one evaluation question drawing on `critical_thinking.md`.
- `critical_thinking.md` — per the shared spec: Claims vs. evidence (the ablation numbers, the 16.7% average margin, the cross-domain heatmap — assess strength of evidence and any missing baselines/comparisons), Genuinely new vs. repackaged (vs. GraphCoT/PolyG/GraphCounselor and vs. general RLHF/GRPO post-training literature), Weaknesses and blind spots (e.g. single training-domain source of the Graph Quizzer's teacher LLM being DeepSeek-Chat rather than a diverse ensemble, GRBENCH-only evaluation, hard-question performance ceiling), Applicability (compute/data prerequisites — RL training infra, curated KG availability), "Relevance to my work" bullets for Sergii's AI/ML engineering + agentic systems + Elisity data-platform context, What this changes, and a Verdict ending in one of adopt/trial/watch/skip with the strongest reason.
- `connections.md` — read `/Users/sergii/.kb/ai_papers/index.md` and skim `ls /Users/sergii/.kb/papers/` plus any `graph_rag` category index for related GraphRAG/agentic-graph-reasoning entries already in the KB (this paper is part of an ongoing agentic-GraphRAG batch-ingestion effort — several sibling papers on the same topic are likely present or in-flight under `/Users/sergii/.kb/papers/` or `/Users/sergii/.kb/graph_rag/`). Select 2-6 genuinely related entries (builds-on / contradicts / same-problem-different-method / shares-technique). If none found, say so in one line with today's date.

Follow Wikilink rules and backlink-line conventions from `kb show summary/get` on every file.

## Step 5: Report + close

Write a completion report to `source/delegation_report.md`: chunks total (4) / passed first try / requeued (how many rounds, if any) / hand-written after exhausting retries (if any). Then:

```
bd close <own-id> --reason "wiki complete"
```

No git commands anywhere in this task — `.kb` auto-syncs.
