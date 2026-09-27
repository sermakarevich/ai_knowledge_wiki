# Task: finalize wiki — verify + synthesize

`<Name>` = `ContextCompressionInteractionCosts`
Folder: `/Users/sergii/.ai/knowledge/research/ContextCompressionInteractionCosts/`

This is the ONLY validation step in the whole pipeline. Do everything below yourself; there
is no separate validate task.

## Step 1: Completeness gate (self-rearm)

List all beads matching `"ContextCompressionInteractionCosts chunk" extract` (`bd search` or
`bd list` + grep) — this also catches any retry beads created by an earlier finalize round.
If ANY are still open/in-progress, this run is premature:
- Create a successor finalize bead (same spec file, `--body-file
  /Users/sergii/.ai/knowledge/research/ContextCompressionInteractionCosts/source/specs/finalize.md`,
  `--deps <the still-open bead ids>`, `--coder claude --model sonnet -p 1 -t task --cwd
  /Users/sergii/.ai --silent`).
- Close own bead with reason `"rearmed as <new-id>: chunks still in flight"`.
- Stop.

## Step 2: Verify every wiki page

Chunks: 01 (Introduction & Related Work), 02 (Method, embeds Figure 1), 03 (Experiments &
Results, embeds Figures 2-6), 04 (Discussion & Limitations).

For each of `wiki/01-introduction-and-related-work.md`, `wiki/02-method.md`,
`wiki/03-experiments-and-results.md`, `wiki/04-discussion-and-limitations.md`:
- Exists, is non-trivial (>40 lines).
- Matches the format contract: backlink line, `# <Topic>`, `**In one sentence:**`, `##
  Key points` (5-8 substantive bullets), `---`, hierarchical detail sections, `**Covers:**`
  footer.
- Covers the WHOLE chunk — spot-check the chunk's last major topic (read the file's TAIL,
  not just its length; a known local-model failure mode is a repetition loop that pads line
  count with nonsense).
- No meta-junk (no "as an AI...", no commentary about being an extraction task).
- Page 02 embeds `images/02-fig1-measurement-protocol.png`. Page 03 embeds all five of
  `images/03-fig2-reacquisition-cost.png`, `images/03-fig3-two-axes.png`,
  `images/03-fig4-retention-interventions.png`, `images/03-fig5-external-environment.png`,
  `images/03-fig6-oracle-conditions.png`.

Build a BAD list and a GOOD list.

## Step 3: Handle BAD pages

**If BAD is empty**, go straight to Step 4.

**If BAD is non-empty:** for each bad chunk NN, count existing extract beads titled
`"ContextCompressionInteractionCosts chunk NN extract"` (any retry suffix) to get its attempt
count. `RETRY_BUDGET` = 3.

- Attempt count < 3: delete the bad page (`wiki/NN-*.md`), create ONE retry extract bead
  reusing `source/specs/NN-extract.md` verbatim (`--coder opencode --model
  ollama-rtx/qwen3.8:27b -p 2 -t task --cwd /Users/sergii/.ai --silent`), record its id.
- Attempt count >= 3: this chunk has exhausted reprocessing — write that one page by hand
  from `source/chunks/NN.txt`, following the same format contract in `source/specs/NN-extract.md`.
  Do not requeue it.

If any retries were created this round: create ONE successor finalize bead (same spec file,
`--deps` = all the new retry bead ids, `--coder claude --model sonnet -p 1 -t task --cwd
/Users/sergii/.ai --silent`), close own bead with reason `"rearmed as <new-id>: N chunk(s)
requeued"`, and stop.

If every bad chunk was handled by hand-writing (nothing requeued), continue to Step 4 in this
same run.

## Step 4: Synthesize

Read `ai show summary/get` (via the `ai` CLI) for the exact specs of these files, then
produce them per that convention, reading the wiki pages (small now) — not the raw source,
except to spot-check quality:

- `summary.md` — content track A2-template. `type: Paper`. Metadata line:
  `**Paper:** [What Does Context Compression Cost an Agent? Interaction Costs Unrevealed by
  Task-Completion Metrics (Liu, 2026)](https://arxiv.org/abs/2608.16370)`
- `digest.md` — copies each wiki page's `**In one sentence:**` and `## Key points` verbatim,
  in reading order, then a closing `## The argument in five moves`.
- `index.md` — OKF front-matter (`type: Paper`), orientation paragraph, "How to work through
  this" ladder, Read This Folder links, wiki table (4 rows, reading order), Original Source
  link to `source/2608.16370.pdf`.
- `explainer.md` — plain-language layer, 80-150 lines, 5-12 jargon-decoder terms (e.g.
  "context compression", "reacquisition cost", "sliding operator", "fact-preserving
  operator", "Holm correction", "oracle intervention", "bounded-horizon agent").
- `questions.md` — 6-8 retrieval-practice questions (this is a ~24pp paper, short-paper
  bucket), at least one per wiki page, answers in collapsed `> [!tip]- Answer` callouts,
  never revealed elsewhere. Include one evaluation question drawing on `critical_thinking.md`.
- `critical_thinking.md` — skeptical appraisal per the Shared Output Conventions spec
  (claims vs. evidence, genuinely new vs. repackaged, weaknesses/blind spots, applicability,
  relevance to Sergii's work — AI/ML engineering, agentic systems, Elisity data platform —
  what this changes, verdict ending in adopt/trial/watch/skip).
- `connections.md` — read `/Users/sergii/.ai/knowledge/research_topics/index.md`, skim 2-3 plausible
  category files (likely `agent_harness`, `memory`, or similar — this paper is about agent
  context management and evaluation methodology), and `ls /Users/sergii/.ai/knowledge/research/` for
  unfiled recent entries. Select 2-6 genuinely related entries (e.g. anything about context
  compression, memory, agent evaluation, or interaction cost). If nothing is related, say so
  plainly.

Note: this paper has a single author (Shuyu Liu) — do not invent additional authors.

## Step 5: Report + close

Write a completion report to
`/Users/sergii/.ai/knowledge/research/ContextCompressionInteractionCosts/source/delegation_report.md`:
chunks total (4) / passed first try / requeued (how many rounds) / hand-written after
exhausting retries.

Then `bd close <own-id> --reason "wiki complete"`.

## Scope & constraints

No git commands anywhere in this task — `.ai` auto-syncs. Do not run `fleet serve restart` /
`fleet run`. Do not touch `source/2608.16370.pdf`, `source/chunks/`, or `wiki/images/*.png`
(only create new `.md` files as specified above).
