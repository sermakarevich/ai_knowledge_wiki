# Finalize: verify wiki chunks + synthesize full KB entry

## Context
This is the last bead in a `ai show summary/get_local` pipeline for the paper
**"Training AI Scientists to Replicate Research"** (arXiv 2608.13331v1, the Replica /
Faraday paper). Seven extract beads (chunk 01-07, titles `TrainingAIScientistsToReplicateResearch
chunk NN extract`) ran on a local model and each should have written one wiki page under:

`/Users/sergii/.ai/knowledge/research/TrainingAIScientistsToReplicateResearch/wiki/`

Expected pages (topic order = reading order):
1. `01-introduction-motivation.md`
2. `02-related-work.md`
3. `03-methods-replica-and-faraday.md`
4. `04-results.md`
5. `05-discussion.md`
6. `06-appendix-task-and-judge-design.md`
7. `07-appendix-example-tasks-and-rubrics.md`

Chunk source text: `source/chunks/NN.txt`. Extract specs (reusable verbatim for retries):
`source/specs/NN-extract.md`. Figure descriptions: `wiki/images/*-description.md`. Manifest:
`source/chunks.json`.

You (this bead) are the ONLY validation step in the whole pipeline. Read
`ai show summary/get_local` first if you want the full background on this architecture, but the
steps below are self-contained.

## Step 1: Completeness gate (self-rearm if chunks still in flight)

Run `bd list` / `bd search "TrainingAIScientistsToReplicateResearch chunk"` (or equivalent) to
find all beads titled `TrainingAIScientistsToReplicateResearch chunk NN extract` (including any
retry beads created by an earlier finalize round). If ANY are still open/in-progress:
- Create a successor finalize bead reusing this same spec file
  (`fleet bd create "TrainingAIScientistsToReplicateResearch finalize: verify + synthesize"
  --cwd /Users/sergii/.ai --coder claude --model sonnet -p 1 -t task
  --body-file /Users/sergii/.ai/knowledge/research/TrainingAIScientistsToReplicateResearch/source/specs/finalize.md
  --deps "<the still-open bead ids>" --silent`)
- Close your own bead: `bd close <own-id> --reason "rearmed as <new-id>: chunks still in flight"`
- Stop here.

## Step 2: Verify every wiki page

For each of the 7 expected pages, check:
- It exists and is well over 40 lines.
- It follows the format contract: backlink line, `# Title`, `**In one sentence:**`, `## Key
  points` (5-8 substantive bullets), `---`, then full detail with `##` subsections.
- It covers the WHOLE chunk, not just the opening -- read the file's TAIL, not just its length
  or first screen. A known local-model failure mode is a repetition loop that pads line count
  with nonsense near the end; catch that here.
- No meta-junk ("Here is the wiki page...", leftover instructions, etc).
- Chunk 03 should embed `images/fig1.png`; chunk 04 should embed `images/fig2.png`,
  `images/fig3.png`, `images/fig4-figC2.png`, and `images/fig5.png` (all 5 images already
  exist in `wiki/images/`, extracted from the PDF).

Build a BAD list and a GOOD list.

## Step 3: Handle BAD pages

If BAD is empty, go straight to Step 4.

If BAD is non-empty, for each bad chunk NN:
- Count existing beads titled `TrainingAIScientistsToReplicateResearch chunk NN extract` (any
  retry suffix) to get its attempt count.
- Attempt count < 3: delete the bad page, create ONE retry extract bead reusing
  `source/specs/NN-extract.md` verbatim: `fleet bd create "TrainingAIScientistsToReplicateResearch
  chunk NN extract (retry)" --cwd /Users/sergii/.ai --coder opencode --model ollama-rtx/qwen3.8:27b
  -p 2 -t task --body-file source/specs/NN-extract.md --silent`. Record its id.
- Attempt count >= 3: exhausted retries -- write that one page by hand from
  `source/chunks/NN.txt` (last resort only). Do not requeue it.

If any retries were created this round: create ONE successor finalize bead depending on all of
them (same command pattern as Step 1), close your own bead with reason "rearmed as <new-id>: N
chunk(s) requeued", and stop. If every bad chunk was handled by hand-writing (nothing requeued),
continue to Step 4 in this same run.

## Step 4: Synthesize the rest of the KB entry

Read `ai show summary/get` for the exact format of every file below (index.md front-matter,
digest.md structure, source-type labels table, wikilink rules, etc) and follow it precisely.
Read the wiki pages (small, ~7 files), NOT the raw source, except to spot-check quality.

Route: this is an AI/ML research paper -> base path
`/Users/sergii/.ai/knowledge/research/TrainingAIScientistsToReplicateResearch/` (already correct, no date
prefix -- this is not an investment source).

Produce, at the folder root:
- `summary.md` -- rung 1, whole paper shallow (~2 min read). Source-type label: `**Paper:**
  [Training AI Scientists to Replicate Research (Falck, Sabri, Surina, Foster, Sims, Devlin,
  Rogers, Collins, Aleksiev, Kirsch, Hughes, 2026)](https://arxiv.org/abs/2608.13331)`.
- `digest.md` -- rung 2, built by copying each wiki page's "In one sentence" line + key points
  verbatim, in reading order (01 through 07), plus a closing "The argument in five moves"
  section synthesizing the paper's overall arc.
- `index.md` -- the wiki hub, front-matter `type: Paper`, links to all 7 wiki pages in order,
  links to summary/digest/explainer/critical_thinking/questions/connections.
- `explainer.md` -- plain-language explainer (80-150 lines): what Replica/Faraday are, why
  paper replication matters as an AI-agent benchmark, how the rubric judge and post-training
  work in plain terms, where this could be applied, jargon decoder (RL post-training, rubric
  judge, coding-agent-as-tool / CAT, rollout, in-distribution vs held-out, etc).
- `questions.md` -- 8-12 retrieval-practice questions with collapsed answers, spread evenly
  across all 7 wiki pages (not clustered on the intro).
- `critical_thinking.md` -- claims vs evidence (is "surpasses Claude Opus 4.8 and GPT-5.5"
  well-supported given the paper's own held-out/in-distribution splits?), applicability,
  limitations the authors admit, what changes if this is right, a verdict.
- `connections.md` -- search the rest of the KB (`kb search`, `kb topics`) for related entries
  (agentic coding, RL post-training, LLM-as-judge / rubric-based reward, AI-for-science, prior
  "AI Scientist" papers) and link them with path-qualified wikilinks. If nothing closely
  related exists yet, say so briefly rather than forcing a weak link.

## Step 5: Report + close

Write a completion report to
`/Users/sergii/.ai/knowledge/research/TrainingAIScientistsToReplicateResearch/source/delegation_report.md`:
chunks total (7) / passed first try / requeued (how many rounds) / hand-written after
exhausting retries.

No git commands anywhere in this task -- `.ai` auto-syncs itself.

Then: `bd close <own-id> --reason "wiki complete"`.
