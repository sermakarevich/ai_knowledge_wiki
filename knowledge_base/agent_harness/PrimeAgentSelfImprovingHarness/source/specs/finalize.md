# Finalize: verify + synthesize — Prime Agent: A Self-Improving RLM Harness

You are the final bead in a fleet chain that built an LLM-wiki entry for the arXiv paper
"Prime Agent: A Self-Improving RLM Harness" (arXiv:2608.23552) at
`/Users/sergii/.ai/knowledge/research/PrimeAgentSelfImprovingHarness/`. This is the ONLY validation step
in the whole pipeline — read this spec fully before doing anything.

Read `ai show summary/get_local` and `ai show summary/get` for full background on the
conventions referenced below (page format, index.md structure, digest/summary/explainer/
questions/critical_thinking/connections specs, wikilink rules, source-type labels).

## Configuration

- `WORKER_MODEL` = `ollama-rtx/qwen3.8:27b`
- `RETRY_BUDGET` = 3 attempts per chunk (initial + 2 retries)
- Base folder: `/Users/sergii/.ai/knowledge/research/PrimeAgentSelfImprovingHarness/`
- Expected wiki pages (5 total):
  1. `wiki/01-introduction-and-motivation.md`
  2. `wiki/02-prime-agent-architecture.md`
  3. `wiki/03-arc-agi3-and-long-context-evaluation.md`
  4. `wiki/04-autonomous-research-and-programmatic-systems.md`
  5. `wiki/05-persistent-refinement-related-work-conclusion.md`
- Matching extract specs (reuse verbatim on retry, do not regenerate):
  `source/specs/01-extract.md` ... `source/specs/05-extract.md`

## Step 1: Completeness gate (self-rearm)

List all beads matching title pattern `"PrimeAgent chunk"` extract (or search by your own
bead-chain ancestry / `bd list` + grep for the chunk-extract task titles you were created
after). If ANY chunk-extract bead is still open/in-progress, this run is premature: create a
successor finalize bead reusing this same spec file
(`--body-file /Users/sergii/.ai/knowledge/research/PrimeAgentSelfImprovingHarness/source/specs/finalize.md`),
with `--deps` on the still-open bead id(s), close your own bead with reason
`"rearmed as <new-id>: chunks still in flight"`, and stop.

## Step 2: Verify every wiki page

For each of the 5 expected pages, check:
- It exists.
- It is non-trivial (>40 lines).
- It matches the format contract from its extract spec (backlink line, `**In one sentence:**`,
  `## Key points` with 5-8 real-content bullets, `---`, hierarchical `##` detail sections,
  `**Covers:**` footer).
- It covers the WHOLE assigned chunk — spot-check the chunk's LAST major topic (read the tail
  of the corresponding `source/chunks/NN.txt` and confirm that topic appears in the wiki page),
  not just the opening paragraphs.
- No meta-junk (no "as an AI language model", no leftover instructions, no repetition loops —
  read the file's TAIL specifically, a known local-model failure mode pads line count with
  repeated/garbled text at the end).
- Every figure named in its spec is actually embedded with `![...](images/<file>.png)`:
  - Page 02: fig1-overview.png, fig2-state-hierarchy.png, fig3-orchestration-lifecycle.png, fig4-long-horizon-control.png
  - Page 03: fig5-arc-agi3-scaling.png
  - Page 04: fig6-out-of-loop-experimentation.png, fig7-8-emulatorbench-pmpp.png
  - Page 05: fig9-factorio-progress.png, fig10-mazebench.png
  - Page 01: no figures required.

Build a BAD list and a GOOD list.

## Step 3: Handle BAD pages

If BAD is empty, go straight to Step 4.

If BAD is non-empty: for each bad chunk NN, count existing extract beads titled with that
chunk number (any retry suffix) to get its attempt count.
- Attempt count < 3 (`RETRY_BUDGET`): delete the bad `wiki/NN-*.md` page, create ONE retry
  extract bead reusing `source/specs/NN-extract.md` verbatim
  (`--coder opencode --model ollama-rtx/qwen3.8:27b --cwd /Users/sergii/.ai`), record its id.
- Attempt count >= 3: this chunk has exhausted reprocessing — write that one page by hand from
  `source/chunks/NN.txt` (last resort only), following the same format contract in its
  `NN-extract.md` spec.

If any retries were created this round: create ONE successor finalize bead (same spec file,
`--deps` on all new retry bead ids), close your own bead with reason
`"rearmed as <new-id>: N chunk(s) requeued"`, and stop.

If every bad chunk was handled by hand-writing (nothing requeued), continue to Step 4 in this
same run.

## Step 4: Synthesize the rest of the wiki

Once all 5 wiki pages pass, produce (read the wiki pages, not the raw source — except to
spot-check quality):

1. **`index.md`** — OKF-style front-matter: `type: Paper`, `title: Prime Agent: A
   Self-Improving RLM Harness`, `description:`, `generated: { by: claude/<model-id>, at:
   <ISO-8601 UTC> }`, `sources:` (id: original → `https://arxiv.org/abs/2608.23552`, id:
   local-copy → `source/2608.23552.pdf`), `tags:` (e.g. `[agents, llm-harness, rlm,
   long-horizon, benchmarks]`). Body: orientation paragraph, "How to work through this" ladder,
   "Read This Folder" links, wiki table (5 rows, reading order), "Original Source" link.
2. **`summary.md`** — the A2-template from `ai show summary/get` (Paper metadata line:
   `**Paper:** [Prime Agent: A Self-Improving RLM Harness (Karten et al., 2026)](https://arxiv.org/abs/2608.23552)`,
   Human Readable TL;DR, TL;DR, Problem & Motivation, Main Original Ideas, Key Findings,
   Suggestions & Future Directions, Authors & Institutions, optional Figures section). Under
   300 lines.
3. **`digest.md`** — derived from the 5 wiki pages: copy each page's `**In one sentence:**` and
   `## Key points` verbatim, in reading order, then a closing "The argument in five moves"
   spine (5-7 numbered steps).
4. **`explainer.md`** — plain-language, no jargon, 80-150 lines, with a jargon decoder table
   (RLM, REPL, Continual Harness, subagent, verifier, etc.).
5. **`questions.md`** — 6-8 retrieval-practice questions (this is a short paper, 16 pages —
   use the low end of the scaling table), at least one per wiki page, answers only inside
   collapsed `> [!tip]- Answer` callouts, one evaluation question drawing on
   `critical_thinking.md`.
6. **`critical_thinking.md`** — skeptical appraisal: claims vs. evidence (test-time scaling
   claims, the ARC-AGI-3 result, the harness-vs-model-capability distinction), genuinely new
   vs. repackaged (vs. other RLM/agent-harness work referenced in Related Work), weaknesses and
   blind spots, applicability, "Relevance to my work" (Sergii's contexts: AI/ML engineering,
   agentic systems, Elisity data platform), what this changes, and a Verdict ending in one of
   adopt / trial / watch / skip. 60-120 lines.
7. **`connections.md`** — read `/Users/sergii/.ai/knowledge/structured_papers/index.md`, skim 2-3 plausible
   category files, and `ls /Users/sergii/.ai/knowledge/research/` for related recent entries (agentic
   harnesses, RLM/recursive-agent papers, long-horizon evaluation work already in the KB).
   Select 2-6 genuinely related entries; if none, say so plainly.

All files use Obsidian `[[wikilink]]` syntax and start with the required backlink line (except
`index.md` and `summary.md`, per the shared conventions).

## Step 5: Report and close

Write `source/delegation_report.md`: chunks total (5) / passed first try / requeued (how many
rounds) / hand-written after exhausting retries. Then
`bd close <own-id> --reason "wiki complete"`.

## Constraints

- No git commands anywhere in this task — `.ai` auto-syncs on its own.
- Do not run `fleet serve restart` / `fleet run`.
- Do not delete `source/chunks/*.txt`, `source/specs/*.md`, or `wiki/images/*` — they are
  reused on retries and referenced by the wiki pages.
