# Task: Finalize ArxivAgentGL — verify extract chunks, synthesize the wiki

You are the last bead in the ArxivAgentGL summarization chain. You are the ONLY validation step in
this whole pipeline. Follow `kb show summary/get` conventions for every artifact you produce.

Folder: `/Users/sergii/.kb/papers/ArxivAgentGL/`

Source: https://arxiv.org/abs/2604.05846 — "AgentGL: Towards Agentic Graph Learning with LLMs via
Reinforcement Learning" (Yuanfu Sun, Kang Li, Dongzhe Fan, Jiajin Liu, Qiaoyu Tan; NYU Shanghai / NYU
/ Tsinghua; 2026-04). Type: `Paper`.

Expected wiki pages (one per chunk):

| Chunk | Wiki page | Spec (reuse verbatim if requeuing) |
|---|---|---|
| 01 | `wiki/01-motivation-and-related-work.md` | `source/specs/01-extract.md` |
| 02 | `wiki/02-agentgl-method.md` | `source/specs/02-extract.md` |
| 03 | `wiki/03-experiments-results-and-conclusion.md` | `source/specs/03-extract.md` |
| 04 | `wiki/04-appendix-datasets-and-implementation.md` | `source/specs/04-extract.md` |

Chunk source texts are at `source/chunks/01.txt` .. `04.txt`. Full manifest: `source/chunks.json`.
Images already extracted: `wiki/images/01-method-overview.png`, `wiki/images/02-ablation-figures.png`
(with vision descriptions `01-description.md`, `02-description.md` alongside).

`RETRY_BUDGET` = 3 attempts per chunk.

## Step 1: Completeness gate (self-rearm)

List all beads matching "ArxivAgentGL chunk" extract (`fleet bd list` or `fleet bd search`, filtering
by title — this also catches retry beads created by an earlier finalize round). If ANY are still
open/in-progress, this run is premature:

- Create a successor finalize bead: same spec file (this file), `--deps <ids of still-open beads>`.
- Close your own bead: `bd close <own-id> --reason "rearmed as <new-id>: chunks still in flight"`.
- Stop.

## Step 2: Verify every wiki page

For each of the 4 expected pages, check:
- It exists and is non-trivial (>40 lines).
- It matches the format contract (backlink line, `# Title`, `**In one sentence:**`, `## Key points`
  with 5-8 substantive bullets, `---`, full-detail subsections, footer `**Covers:**` line).
- It covers the WHOLE chunk — read the file's TAIL, not just the head, and spot-check that the
  chunk's last major topic (e.g. Conclusion/Limitations for chunk 03, Case Study for chunk 04) is
  actually present, not just the opening.
- No repetition-loop garbage (a known local-model failure mode pads line count with nonsense —
  check for repeated near-identical paragraphs).
- Chunks 02 and 03 each embed their one named figure (`images/01-method-overview.png` and
  `images/02-ablation-figures.png` respectively) with a real `![...]` reference; chunks 01 and 04
  have no figures and should have none fabricated.

Build a BAD list and a GOOD list.

## Step 3: Handle BAD chunks

If BAD is empty, go straight to Step 4.

If BAD is non-empty, for each bad chunk:
- Count existing extract beads titled "ArxivAgentGL chunk NN extract" (including retries) to get
  its attempt count.
- Attempt count < 3: delete the bad page, create ONE retry extract bead reusing the chunk's
  `source/specs/NN-extract.md` verbatim (`--coder opencode --model ollama-rtx/qwen3.8:27b`), record
  its id.
- Attempt count >= 3: exhausted. Write that one page by hand from the chunk text (last resort only).
  Do not requeue it.

If any retries were created this round: create ONE successor finalize bead depending on all of
them (same spec file, this file), close your own bead with reason
`"rearmed as <new-id>: N chunk(s) requeued"`, and stop. If every bad chunk was handled by hand-writing
(nothing requeued), continue to Step 4 in this same run.

## Step 4: Synthesize the remaining artifacts

Read the 4 wiki pages (small, already compressed) — not the raw source, except to spot-check quality
or fill a gap the wiki pages leave. Per `kb show summary/get`:

1. **`index.md`** — front-matter (`type: Paper`, title, one-sentence description, `generated: {by:
   claude/<model-id>, at: <ISO-8601 UTC timestamp>}`, sources with `id: original` → the arxiv URL and
   `id: local-copy` → `source/paper.pdf`, 2-5 tags e.g. `[graph-learning, llm-agents, reinforcement-learning,
   graphrag, text-attributed-graphs]`), orientation paragraph, reading ladder, wiki table (in reading
   order: 01→04), original-source line.
2. **`summary.md`** — rung 1, whole paper, shallow (~2 min). Metadata line:
   `**Paper:** [AgentGL: Towards Agentic Graph Learning with LLMs via Reinforcement Learning
   (Sun et al., 2026)](https://arxiv.org/abs/2604.05846)`.
3. **`digest.md`** — rung 2, built by copying each wiki page's `**In one sentence:**` line and
   `## Key points` bullets verbatim, in order, plus a closing "The argument in five moves" (5-7
   numbered clauses).
4. **`explainer.md`** — plain-language: what AgentGL is, why static GraphLLMs/GraphRAG fall short,
   how the RL-trained agent with graph-native search tools works (analogy-first), where this could
   apply beyond the paper's own benchmarks, jargon decoder for terms like TAG, GNS tools, GCCL,
   search-constrained thinking, GRPO.
5. **`questions.md`** — 6-8 retrieval-practice questions with collapsed-callout answers, covering all
   4 wiki pages evenly (at least one question per page).
6. **`critical_thinking.md`** — claims vs. evidence (are the 17.5%/28.4% improvements convincing given
   the baselines and dataset subsampling described in the appendix?), applicability, what this changes,
   a verdict.
7. **`connections.md`** — links to related entries in this KB. Check for existing GraphRAG/agentic-graph
   papers already ingested under `/Users/sergii/.kb/papers/` (e.g. `ArxivGraphScout`,
   `ArxivGraphReasoningAgentGRA`, `ArxivWhyNeighborhoodsMatter`, or a `graph_rag` category folder if one
   exists) and link to them with path-qualified wikilinks; note the specific relationship (e.g. shares
   the GraphRAG-vs-native-topology framing, is a baseline this paper compares against, etc.).

Follow wikilink rules, backlink lines, and source-type-label conventions from `kb show summary/get`
exactly. No git commands — `.kb` auto-syncs.

## Step 5: Report and close

Write a completion report to `source/delegation_report.md`: chunks total / passed first try /
requeued (how many rounds) / hand-written after exhausting retries.

Then: `bd close <own-id> --reason "wiki complete"`.
