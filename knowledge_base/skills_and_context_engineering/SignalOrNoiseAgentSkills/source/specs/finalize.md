# Finalize: verify chunk extraction + synthesize wiki

This is the ONLY validation step in the whole pipeline. You are a Claude worker running headless.

## Paper

"Signal or Noise? A Benchmark Study of Agent Skills in Web Development" (arXiv:2608.23067), Yang & Ding,
Baidu NLP. A controlled empirical study (WebDev-Skills-Bench) showing that injecting matched Agent Skills
into coding-agent sessions usually reduces Pass@2 while raising token cost, with only a minority of
(Skill, project) pairs benefiting.

Folder: `/Users/sergii/.kb/papers/SignalOrNoiseAgentSkills/`

## Step 1: Completeness gate (self-rearm)

List all beads matching `"SignalOrNoiseAgentSkills chunk" extract` (`bd search` or `bd list` + grep) — this
also catches any retry beads created by an earlier finalize round. If ANY are still open/in-progress, this
run is premature: create a successor finalize bead (same spec file, `--deps <the still-open bead ids>`),
close your own bead with reason `"rearmed as <new-id>: chunks still in flight"`, and stop.

## Step 2: Verify every wiki page

Four expected pages:

- `wiki/01-introduction-and-benchmark-design.md`
- `wiki/02-results-and-mechanisms.md`
- `wiki/03-implications-and-conclusion.md`
- `wiki/04-appendices-worked-examples.md`

For each: check it exists, is non-trivial (>40 lines), matches the format contract (backlink line,
`**In one sentence:**`, `## Key points`, `---`, hierarchical detail, `**Covers:**` footer), covers the
WHOLE chunk (spot-check the chunk's last major topic, not just the opening — cross-reference against
`source/chunks/NN.txt` and `source/chunks.json`), has no meta-junk, and embeds any named figures
(page 02 must embed `images/page10-fig3-slice-contribution.png` and
`images/page10-fig4-example-code-by-model.png`; page 04 must embed
`images/page9-figures1-2-retry-lockin-and-content-win.png`). Read the file's TAIL, not just its length — a
known local-model failure mode is a repetition loop that pads line count with nonsense.

Build a BAD list and a GOOD list.

## Step 3: Handle BAD pages

**If BAD is empty**, go straight to Step 4.

**If BAD is non-empty:** for each bad chunk (identified by its `NN`), count existing extract beads titled
`"SignalOrNoiseAgentSkills chunk NN extract"` (any retry suffix) to get its attempt count. `RETRY_BUDGET` = 3.

- Attempt count < 3: delete the bad page, create ONE retry extract bead reusing
  `source/specs/NN-extract.md` verbatim (`--coder opencode --model ollama-rtx/qwen3.8:27b`), record its id.
- Attempt count >= 3: this chunk has exhausted reprocessing — write that one page by hand from
  `source/chunks/NN.txt` (last resort only). Do not requeue it.

If any retries were created this round: create ONE successor finalize bead depending on all of them, close
your own bead with reason `"rearmed as <new-id>: N chunk(s) requeued"`, and stop. If every bad chunk was
handled by hand-writing (nothing requeued), continue to Step 4 in this same run.

## Step 4: Synthesize the rest of the wiki

Follow `kb show summary/get` conventions (Shared Output Conventions section) for every file below. Read
the wiki pages (small now, ~4 files), not the raw source, except to spot-check quality. This is a Paper
(`type: Paper` in front-matter), routed to `papers/` (not investment).

### `summary.md`

Use the A2-template from `kb show summary/get`:
- `**Paper:** [Signal or Noise? A Benchmark Study of Agent Skills in Web Development (Yang & Ding, 2026)](https://arxiv.org/abs/2608.23067)`
- `**Wiki:** [[index]] | **Digest:** [[digest]]`
- Human Readable TL;DR (analogies, zero jargon), TL;DR (technical), Problem & Motivation, Main Original
  Ideas, Key Findings (include a results table — Table 1's per-model numbers), Suggestions & Future
  Directions, Authors & Institutions (Ziyue Yang, Ding Fan — Baidu NLP, Beijing, China).
- Omit the Figures section (or include the fig3/fig4 chart if it adds value beyond the text).
- Keep under 300 lines.

### `digest.md`

Copy each wiki page's `**In one sentence:**` line and `## Key points` bullets verbatim, in reading order,
then close with `## The argument in five moves` (5-7 numbered steps spanning the whole paper).

### `index.md`

Front-matter (OKF subset): `type: Paper`, `title`, `description`, `generated: {by: claude/<model-id>, at: <ISO-8601 UTC>}`,
`sources: [{id: original, resource: https://arxiv.org/abs/2608.23067}, {id: local-copy, resource: source/2608.23067.pdf}]`,
`tags: [agent-skills, benchmarking, web-development, llm-agents, prompt-engineering]` (adjust as fits).
Orientation paragraph, "How to work through this" ladder, Read This Folder links, wiki table (4 rows,
reading order), Original Source link with retrieval date (today, per `date +%F`).

### `explainer.md`

Plain-language layer per the Shared Output Conventions spec — no background in AI assumed. Explain what an
"Agent Skill" is with an everyday analogy (e.g. a cheat-sheet handed to a new employee before every task),
why prompt length matters, and the core finding (the cheat-sheet often doesn't help and sometimes actively
hurts, especially on tasks the employee already knew how to do). Target 80-150 lines, 5-12 jargon-decoder terms
(Agent Skill, Pass@k, Task Completion Depth, length-matched control, leave-one-out ablation, retry lock-in, etc.).

### `questions.md`

6-8 questions (short paper range per Scaling by source size). At least one per wiki page (4 pages → at
least 4, spread the rest across mechanism/transfer/evaluation). Mix: ~half core recall (e.g. "What is the
average ∆Pass@2 range across the four models?"), ~a third elaboration (e.g. "Why does the loss concentrate
on easy tasks rather than hard ones?"), the rest transfer + one evaluation question drawing on
`critical_thinking.md`. Answers in collapsed `> [!tip]- Answer` callouts only — do not reveal them elsewhere.

### `critical_thinking.md`

Skeptical-reviewer appraisal per the Shared Output Conventions spec. Ground every criticism in something
specific from the paper's own Limitations section and results (e.g. the seed-spread caveat — 4.4pp variance
comparable to headline effect size; the C2 measurement using only 109 unique length-matched runs across 117
pairs; conservative routing meaning off-target deployment is untested; the Skill set being drawn only from
high-visibility public repos; functional-correctness-only metrics via Playwright, missing readability/UX
gains). End with a one-word adoption call (adopt / trial / watch / skip) and the single strongest reason.
Target 60-120 lines.

### `connections.md`

Read `/Users/sergii/.kb/ai_papers/index.md`, skim 2-3 plausible category files, and `ls /Users/sergii/.kb/papers/`
for unfiled recent entries. Specifically check for a prior entry on arXiv 2608.14036 ("Demystifying Agent
Skills: Why They Work-Until They Don't") — if present, this is very likely a genuine connection (same topic,
possibly contradicting or complementary findings). Select 2-6 genuinely related entries; do not force links.

## Step 5: Report + close

Write a completion report to `source/delegation_report.md`: chunks total (4) / passed first try / requeued
(how many rounds) / hand-written after exhausting retries. Then `bd close <own-id> --reason "wiki complete"`.

No git commands anywhere in this task — `.kb` auto-syncs.
