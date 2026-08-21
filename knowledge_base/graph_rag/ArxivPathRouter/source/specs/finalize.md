# Finalize task: ArxivPathRouter — verify + synthesize

You are the finalize worker for the local-fleet KB ingestion of the paper **"PathRouter: Aligning Rewards with Retrieval Quality in Agentic Graph Retrieval-Augmented Generation"** (arXiv 2606.16409, Wang et al., 2026). Output folder: `/Users/sergii/.kb/papers/ArxivPathRouter/`.

Follow `kb show summary/get` and `kb show summary/get_local` for full conventions (Output structure, Progressive disclosure, Wikilink rules, `index.md` template, `digest.md`/`explainer.md`/`questions.md`/`critical_thinking.md`/`connections.md` templates, Source-type labels). This spec only sequences the finalize-specific steps.

Worker model for retries: `ollama-rtx/qwen3.8:27b` (`--coder opencode --model ollama-rtx/qwen3.8:27b`). RETRY_BUDGET = 3 attempts per chunk.

## Step 1: Completeness gate (self-rearm)

List all beads titled `"ArxivPathRouter chunk NN extract"` (any retry suffix) via `fleet bd list` or `fleet bd search`. If ANY are still open/in-progress, this run is premature:
- Create a successor finalize bead: `fleet bd create "ArxivPathRouter finalize: verify + synthesize" --cwd /Users/sergii/.kb --coder claude --model sonnet -p 1 -t task --body-file /Users/sergii/.kb/papers/ArxivPathRouter/source/specs/finalize.md --deps "<still-open bead ids>" --silent`
- `bd close <own-id> --reason "rearmed as <new-id>: chunks still in flight"`
- Stop.

## Step 2: Verify every wiki page

Expected pages (from `/Users/sergii/.kb/papers/ArxivPathRouter/source/chunks.json`):
1. `wiki/01-introduction-and-related-work.md`
2. `wiki/02-pathrouter-method.md`
3. `wiki/03-distillation-and-training-objective.md`
4. `wiki/04-experiments-and-main-results.md`
5. `wiki/05-limitations-and-appendix.md`

For each: check it exists, is non-trivial (>40 lines), matches the format contract (backlink line, `**In one sentence:**`, `## Key points`, `---`, detail sections, `**Covers:**` footer), covers the WHOLE chunk (spot-check the chunk's last major topic, not just the opening — cross-reference against `source/chunks/NN.txt`), has no meta-junk or repetition loops (read the TAIL of the file, not just line count), and embeds any figures listed in `source/chunks.json` for that chunk (images live in `wiki/images/`).

Build a BAD list and a GOOD list.

## Step 3: Handle BAD pages

If BAD is empty, go straight to Step 4.

For each bad chunk NN: count existing extract beads titled `"ArxivPathRouter chunk NN extract"` (including retries) to get its attempt count.
- Attempt count < 3: delete the bad page, create ONE retry extract bead reusing `source/specs/NN-extract.md` verbatim: `fleet bd create "ArxivPathRouter chunk NN extract (retry)" --cwd /Users/sergii/.kb --coder opencode --model ollama-rtx/qwen3.8:27b -p 2 -t task --body-file /Users/sergii/.kb/papers/ArxivPathRouter/source/specs/NN-extract.md --silent`. Record its id.
- Attempt count >= 3: exhausted — write that one page by hand from `source/chunks/NN.txt` (and its figure descriptions if any), following the same page format contract used in the extract specs. Do not requeue it.

If any retries were created this round: create ONE successor finalize bead depending on all of them (same pattern as Step 1), close own bead with reason `"rearmed as <new-id>: N chunk(s) requeued"`, and stop. If every bad chunk was handled by hand-writing (nothing requeued), continue to Step 4 in this same run.

## Step 4: Synthesize the rest of the folder

Read the (now-verified) wiki pages — not the raw source, except to spot-check quality — and produce, per `kb show summary/get` conventions:

- `index.md` — front-matter with `type: Paper`, `sources: [{id: original, resource: https://arxiv.org/abs/2606.16409}, {id: local-copy, resource: source/source.md}]`, tags e.g. `[graphrag, agentic-rag, reinforcement-learning, retrieval]`, orientation paragraph, "How to work through this" ladder, Read This Folder links, wiki table (5 rows, reading order), Original Source link pointing at `source/source.md` (the PDF binary was not copied — size guard, see `source/source.md`).
- `summary.md` — the A2-template: **Paper:** metadata line with the arXiv URL, Human Readable TL;DR, TL;DR, Problem & Motivation, Main Original Ideas, Key Findings (include a results table drawn from wiki page 04), Suggestions & Future Directions (from Limitations), Authors & Institutions, Figures section (pick 1-2 most illustrative, e.g. Figure 1 and Figure 2).
- `digest.md` — copy each wiki page's `**In one sentence:**` and `## Key points` verbatim, in order, then a `## The argument in five moves` synthesis spine.
- `explainer.md` — plain-language, no-jargon, 80-150 lines, analogies for: agentic GraphRAG, reward aliasing, evidence-path overlap, route-conditioned training, teacher-student KL distillation. Include a jargon decoder (5-12 terms: GRPO, KL divergence, F1, EM, GraphRAG, teacher-student distillation, etc.).
- `questions.md` — 8-12 questions (long-paper bucket), at least one per wiki page, mix of recall/elaboration/transfer/one evaluation question drawing on `critical_thinking.md`. Answers only inside collapsed `> [!tip]- Answer` callouts.
- `critical_thinking.md` — claims vs. evidence (the 4 route-category framing, the teacher-KL ablations, the cross-dataset transfer claim of 95.7%), genuinely new vs. repackaged (compare to Search-R1, Graph-R1, HippoRAG2 mentioned in the paper), weaknesses/blind spots (e.g., single backbone family Qwen2.5, reliance on GPT-4o-mini as judge, added hyperparameter/compute cost acknowledged in Limitations), applicability, "Relevance to my work" bullets for Sergii's AI/ML engineering and agentic-systems context, and a verdict (adopt/trial/watch/skip) with the strongest reason.
- `connections.md` — read `/Users/sergii/.kb/ai_papers/index.md` and skim `ls /Users/sergii/.kb/papers/` for other recently-ingested agentic-GraphRAG papers (e.g. ArxivGraphScout, ArxivGraphReasoningAgentGRA, ArxivWhyNeighborhoodsMatter, and any others filed under `graph_rag`) — select 2-6 genuinely related entries with the relationship type (builds-on, contradicts, same-problem-different-method, shares-technique). If nothing found, say so plainly.

Write each artifact directly (no need for further subagent fan-out — the wiki pages are already small).

## Step 5: Report + close

Write `/Users/sergii/.kb/papers/ArxivPathRouter/source/delegation_report.md`: chunks total (5) / passed first try / requeued (how many rounds) / hand-written after exhausting retries.

Then `bd close <own-id> --reason "wiki complete"`.

No git commands anywhere in this task — `.kb` auto-syncs.
