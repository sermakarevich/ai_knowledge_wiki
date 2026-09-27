# Task: Finalize the DemystifyingAgentSkills KB entry (verify + synthesize)

You are the finalize bead for a `ai show summary/get_local` run on the paper "Demystifying
Agent Skills: Why They Work-Until They Don't" (arXiv 2608.14036, Jiang et al. 2026). This is
the ONLY validation step in the whole pipeline. Read `ai show summary/get_local` and
`ai show summary/get` if you need the full conventions (front-matter format, wikilink rules,
digest/explainer/questions/critical_thinking/connections specs) — this spec summarizes the
essentials but those are the source of truth for exact formatting.

Base folder: `/Users/sergii/.ai/knowledge/research/DemystifyingAgentSkills/`
Manifest: `/Users/sergii/.ai/knowledge/research/DemystifyingAgentSkills/source/chunks.json` (5 chunks, one
wiki page each, listed with their intended filenames)

## Step 1: Completeness gate (self-rearm)

List all beads matching "DemystifyingAgentSkills chunk" extract (`bd search` or `bd list` +
grep) — this also catches any retry beads created by an earlier finalize round. If ANY are
still open/in-progress, this run is premature: create a successor finalize bead (same spec
file, i.e. this file, `--deps <the still-open bead ids>`), close your own bead with reason
"rearmed as <new-id>: chunks still in flight", and stop.

## Step 2: Verify every wiki page

For each of the 5 wiki pages listed in `chunks.json`, check:
- It exists at the expected path under `wiki/`.
- It is non-trivial (>40 lines).
- It matches the format contract: backlink line, `# <Topic>`, `**In one sentence:**`,
  `## Key points` (5-8 substantive bullets), `---`, then full-detail `##` subsections, a
  `**Covers:**` footer line.
- It covers the WHOLE assigned chunk — spot-check the chunk's LAST major topic (read the tail
  of both the chunk file and the wiki page), not just the opening. This matters especially for
  `wiki/05-implementation-details-and-prompts.md` (chunk 05 is the largest — verify Appendix B
  prompts actually got covered, not just Appendix A).
- No meta-junk (no "I have written the page" commentary, no repetition-loop padding — read the
  TAIL of the file, not just its line count, since a known local-model failure mode is a
  repetition loop that pads line count with nonsense).
- Named figures are embedded: page 02 must embed `images/01-fig1-overview-page2.png`, page 03
  must embed `images/02-fig2-taxonomy-page3.png`, page 04 must embed all three of
  `images/03-fig3fig4-results-page8.png`, `images/04-fig3b-page9.png`, `images/05-fig5-page10.png`.

Build a BAD list and a GOOD list.

## Step 3: Handle BAD pages

If BAD is empty, go straight to Step 4.

If BAD is non-empty: for each bad chunk NN, count existing extract beads titled
"DemystifyingAgentSkills chunk NN extract" (any retry suffix) to get its attempt count.
- Attempt count < 3 (RETRY_BUDGET): delete the bad wiki page, create ONE retry extract bead
  reusing `source/specs/NN-extract.md` verbatim (`--coder opencode --model ollama-rtx/qwen3.8:27b`),
  record its id.
- Attempt count >= 3: this chunk has exhausted reprocessing — write that one wiki page by hand
  from `source/chunks/NN.txt` yourself (last resort only). Do not requeue it.

If any retries were created this round: create ONE successor finalize bead depending on all of
them (same spec file, i.e. this file), close your own bead with reason "rearmed as <new-id>:
N chunk(s) requeued", and stop. If every bad chunk was handled by hand-writing (nothing
requeued), continue to Step 4 in this same run.

## Step 4: Synthesize the remaining artifacts

Read the 5 wiki pages (small now — do not re-read the raw source except to spot-check quality
already done in Step 2) and produce, per `ai show summary/get` conventions:

- `index.md` — front-matter (`type: Paper`), orientation paragraph, "How to work through this"
  ladder, "Read This Folder" links, wiki table (5 rows, reading order), Original Source link.
- `summary.md` — the A2-template: Human Readable TL;DR, TL;DR, Problem & Motivation, Main
  Original Ideas, Key Findings (include a results table — the paper has plenty of numbers:
  6.06-point improvement over Workflow Memory, 65.7% vs 4.5% procedural anchoring, 29.6%->3.3%
  retrieval precision collapse, etc.), Suggestions & Future Directions, Authors & Institutions
  (Zhiyuan Jiang, Fangrui Huang, Hanwen Xing, Xander Wu, Yipeng Gao, Rui Cao, Mengdi Wang,
  Shilong Liu, Yijiang Li — Princeton, UC San Diego, Stanford, USC, Johns Hopkins), Figures
  section (reference 1-2 of the most informative figures with `wiki/images/...` paths).
  Metadata line: `**Paper:** [Demystifying Agent Skills: Why They Work-Until They Don't (Jiang et al., 2026)](https://arxiv.org/abs/2608.14036)`.
  Keep under 300 lines.
- `digest.md` — copy each wiki page's `**In one sentence:**` line and `## Key points` bullets
  verbatim, in order, then a `## The argument in five moves` spine (5-7 numbered steps).
  ~60-100 lines (this is a ~28-page paper, so treat it as a long paper: 5-8 wiki pages,
  8-12 questions per the Scaling table — 5 pages and this range of questions is correct here).
- `explainer.md` — plain-language layer (What is this about? / Why does it matter? / How does
  it work? / Where can this be used? / Conclusions & takeaways / Jargon decoder with 5-12
  terms e.g. "skill", "procedural anchoring", "Workflow Memory", "trajectory", "Hit@1",
  "open coding"). Target 80-150 lines.
- `questions.md` — 8-12 retrieval-practice questions, at least one per wiki page (5 pages ->
  at least 5, aim for 8-12), collapsed `> [!tip]- Answer` callouts, mixed core-recall /
  elaboration / transfer / one evaluation question drawing on `critical_thinking.md`.
- `critical_thinking.md` — claims vs. evidence, genuinely new vs. repackaged (name prior
  memory-reuse-in-LLM-agents work the paper itself cites and contrasts against), weaknesses
  and blind spots, applicability, "Relevance to my work" (2-4 bullets for Sergii's contexts:
  AI/ML engineering, agentic systems, Elisity data platform — this paper is directly relevant
  to any skill/procedural-memory system for coding agents), What this changes, Verdict ending
  in adopt/trial/watch/skip. Target 60-120 lines.
- `connections.md` — read `/Users/sergii/.ai/knowledge/research_topics/index.md`, then check
  `/Users/sergii/.ai/knowledge/research/AgentSkillsCanBeHarmful/`, `/Users/sergii/.ai/knowledge/research/BeyondDomainsWebSkills/`,
  and `/Users/sergii/.ai/knowledge/research/MSCEMemorySkillCoEvolution/` (existing KB entries on closely
  related "agent skills" topics — `ls /Users/sergii/.ai/knowledge/research/` for other candidates too).
  Select 2-6 genuinely related entries; do not force links.

Follow `ai show summary/get`'s exact templates/section order for each file — do not invent a
different structure.

## Step 5: Report and close

Write a completion report to
`/Users/sergii/.ai/knowledge/research/DemystifyingAgentSkills/source/delegation_report.md`: chunks total
(5) / passed first try / requeued (how many rounds) / hand-written after exhausting retries.

Then `bd close <own-id> --reason "wiki complete"`.

No git commands anywhere in this task — `.ai` auto-syncs on its own.
