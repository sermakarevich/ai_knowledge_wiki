# Task: finalize wiki for GraphEngineeringKimiK3 (verify + synthesize + close)

This is the last bead in a chunk-extraction chain for a local X (Twitter) article. You are the
ONLY validation step in the whole pipeline. Work entirely inside
`/Users/sergii/.kb/papers/GraphEngineeringKimiK3/`. No git commands anywhere in this task — `.kb`
auto-syncs on its own.

## Background

Source: X (Twitter) article by Kirill (@kirillk_web3), "Graph Engineering with Kimi K3: Complete
A-Z Guide to the Architecture That Beats Bigger Models" — https://x.com/kirillk_web3/status/2087619214915826155,
published Aug 12, 2026 (~602.9K views). Captured locally (logged-in session required for X).

**Critical terminology note — must appear in `summary.md` and `index.md`:** this article uses
"graph engineering" in the KNOWLEDGE-GRAPH / GraphRAG sense (storing facts as triples — subject,
relation, object — in a graph database and querying relationships directly). This is DIFFERENT
from the agent-topology sense of "graph engineering" (wiring multi-agent loops/pipelines into a
graph of agent calls) used by other sources in the same research batch. State this distinction
explicitly and near the top — do not let a reader confuse the two senses.

Four chunks were extracted to four wiki pages by a local model, one bead per chunk, sequential
chain. The chunk manifest is at `source/chunks.json`. Extract specs (kept for possible retries)
are at `source/specs/01-extract.md` through `04-extract.md`.

## Step 1 — Completeness gate (self-rearm if premature)

List all beads titled `"GraphEngineeringKimiK3 chunk NN extract"` (any retry suffix) via
`fleet bd search` or `fleet bd list` + grep. If ANY are still open/in-progress, this run fired
too early: create a successor finalize bead reusing this same spec file
(`--deps <ids of the still-open beads>`, `--coder claude --model sonnet -t task --cwd /Users/sergii/.kb`),
close your own bead with reason `"rearmed as <new-id>: chunks still in flight"`, and stop.

## Step 2 — Verify every wiki page

The 4 expected pages:

1. `wiki/01-the-problem-and-what-graph-engineering-is.md`
2. `wiki/02-why-kimi-k3-and-the-model-vs-graph-finding.md`
3. `wiki/03-the-8-layer-architecture-and-5-prompts.md`
4. `wiki/04-stack-week-one-plan-and-troubleshooting.md`

For each: check it exists, is non-trivial (>40 lines), matches the format contract (backlink
line, one-sentence headline, Key points block, `---`, full detail subsections, `**Covers:**`
footer), covers the WHOLE chunk (spot-check the chunk's last major topic, not just the opening —
read the TAIL of the file, not just its length; a known local-model failure mode is a repetition
loop that pads line count with nonsense), has no meta-junk (no leftover instructions, no
"as an AI language model" boilerplate), and embeds its named figures (page 01: 3 images; page
02: 1 image; page 03: 1 image; page 04: no images expected). Cross-check page 01 explicitly
notes the graph-vs-agent-topology terminology distinction. Build a BAD list and a GOOD list.

## Step 3 — Handle BAD pages, if any

If BAD is empty, go straight to Step 4.

If BAD is non-empty, for each bad chunk NN:
- Count existing beads titled `"GraphEngineeringKimiK3 chunk NN extract"` (including retries) to
  get its attempt count. Retry budget is 3 attempts total (initial + 2 retries).
- Attempt count < 3: delete the bad wiki page, create ONE retry extract bead reusing
  `source/specs/NN-extract.md` verbatim: `fleet bd create "GraphEngineeringKimiK3 chunk NN extract retry" --cwd /Users/sergii/.kb --coder opencode --model ollama-rtx/qwen3.8:27b -p 2 -t task --body-file /Users/sergii/.kb/papers/GraphEngineeringKimiK3/source/specs/NN-extract.md --silent`. Record its id.
- Attempt count >= 3: this chunk has exhausted reprocessing. Write that one wiki page by hand
  from `source/chunks/NN.txt` yourself, following the same format contract as the spec file.
  Do not requeue it.
- If any retries were created this round: create ONE successor finalize bead depending on all of
  them (reusing this same spec file), close your own bead with reason
  `"rearmed as <new-id>: N chunk(s) requeued"`, and stop. If every bad chunk was instead handled
  by hand-writing (nothing requeued), continue to Step 4 in this same run.

## Step 4 — Synthesize the remaining artifacts

Read the 4 wiki pages (small — do not re-read the raw source except to spot-check quality or to
hand-write a page per Step 3). Route: this is an AI/graph-engineering article, not investment —
output base is `/Users/sergii/.kb/papers/GraphEngineeringKimiK3/` (already created, no date
prefix). Source-type label: `Article`.

Produce, per `kb show summary/get` conventions (folder scaffold and file specs already in place):

1. **`summary.md`** — rung 1 template (Human Readable TL;DR, TL;DR, Problem & Motivation, Main
   Original Ideas, Key Findings, Suggestions & Future Directions, Authors & Institutions,
   Figures). Metadata line: `**Article:** [Graph Engineering with Kimi K3: Complete A-Z Guide to
   the Architecture That Beats Bigger Models](https://x.com/kirillk_web3/status/2087619214915826155) — X (Twitter), Aug 12, 2026`.
   Include the terminology note prominently (e.g. right after the TL;DR, as a callout or bold
   sentence) — this is the single most important framing fact for this entry.
2. **`digest.md`** — copy each wiki page's `**In one sentence:**` line and `## Key points`
   bullets verbatim, in reading order, then a `## The argument in five moves` closing spine.
3. **`index.md`** — front-matter (`type: Article`), orientation paragraph (include the
   terminology note here too), reading ladder, Read This Folder links, wiki table (4 rows), link
   to `source/article.md`.
4. **`explainer.md`** — plain-language layer (What is this about? / Why does it matter? / How
   does it work? / Where can this be used? / Conclusions & takeaways / Jargon decoder). Explain
   the graph-vs-agent-topology terminology distinction here too in plain terms, since it's an
   easy mix-up for a non-expert reader.
5. **`questions.md`** — 6-8 retrieval-practice questions (this is a short article — see Scaling
   by source size table), at least one per wiki page, answers in collapsed callouts, one
   question specifically testing the terminology distinction (e.g. "what does 'graph engineering'
   mean in THIS article, and how does that differ from the agent-topology sense used elsewhere?").
6. **`critical_thinking.md`** — claims vs evidence (the 26-model finding, the 85%/18% numbers,
   the Arena.ai leaderboard screenshot — note these are marketing-adjacent/promotional claims
   without disclosed methodology, treat skeptically), genuinely new vs repackaged (this is mostly
   a practitioner's synthesis of existing GraphRAG/Microsoft/academic work plus a vendor pitch for
   Kimi K3 — say so plainly), weaknesses/blind spots, applicability, relevance to Sergii's work
   (AI/ML engineering, agentic systems, Elisity data platform), verdict (adopt/trial/watch/skip).
7. **`connections.md`** — read `/Users/sergii/.kb/ai_papers/index.md` and skim 2-3 plausible
   category files, plus `ls /Users/sergii/.kb/papers/` for related entries (especially any other
   GraphRAG / knowledge-graph / agent-graph-topology entries from this same research batch —
   link to them and explicitly name the terminology distinction as the relationship type where
   relevant).

## Step 5 — Report and close

Write a completion report to
`/Users/sergii/.kb/papers/GraphEngineeringKimiK3/source/delegation_report.md`: chunks total (4),
how many passed on first try, how many were requeued (and how many rounds), how many were
hand-written after exhausting retries. Then:

```
bd close <own-id> --reason "wiki complete"
```
