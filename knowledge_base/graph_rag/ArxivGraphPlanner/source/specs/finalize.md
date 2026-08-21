# Task: Finalize ArxivGraphPlanner KB wiki (verify + synthesize)

You are the finalize worker for the paper **GraphPlanner: Graph Memory-Augmented Agentic Routing for Multi-Agent LLMs** (Feng, Zhang, Lei, Han, You; ICLR 2026; arXiv 2604.23626). Output folder: `/Users/sergii/.kb/papers/ArxivGraphPlanner/`. This is the ONLY validation step in the whole pipeline — be thorough.

Config: `WORKER_MODEL=ollama-rtx/qwen3.8:27b`, `RETRY_BUDGET=3` attempts per chunk, `--coder opencode` for retries.

## Step 1: Completeness gate (self-rearm if premature)

List all beads titled like `"ArxivGraphPlanner chunk NN extract"` (`fleet bd list` or `fleet bd search`, grep for the title pattern — this also catches any retry beads from an earlier finalize round). If ANY are still open/in-progress:
- Create a successor finalize bead: `fleet bd create "ArxivGraphPlanner finalize: verify + synthesize" --cwd /Users/sergii/.kb --coder claude --model sonnet -p 1 -t task --body-file /Users/sergii/.kb/papers/ArxivGraphPlanner/source/specs/finalize.md --deps "<the still-open bead ids, comma-separated>" --silent`
- Close your own bead: `bd close <own-id> --reason "rearmed as <new-id>: chunks still in flight"`
- Stop here.

## Step 2: Verify every wiki page

Expected pages (all under `/Users/sergii/.kb/papers/ArxivGraphPlanner/wiki/`):
1. `01-problem-and-preliminaries.md`
2. `02-graphplanner-method.md`
3. `03-experiments-and-results.md`
4. `04-related-work-and-implementation.md`
5. `05-additional-ablations-and-generalization.md`
6. `06-prompt-templates-and-examples.md`

For each: check it exists, is non-trivial (>40 lines), follows the format contract (backlink line, `**In one sentence:**`, `## Key points` with 5-8 real bullets, `---`, detailed subsections, footer `**Covers:**` line), covers the WHOLE assigned chunk (spot-check the chunk's LAST major topic per `source/chunks.json`, not just the opening), has no meta-junk about "extraction process", and embeds any figures it's supposed to (page 01 → `fig1-router-comparison.png`; page 02 → `fig2-graphplanner-mdp-overview.png`; page 03 → `fig3-phase1-evaluation.png`, `fig4-pareto-frontier.png`, `fig5-generalization-ablation.png`; page 05 → `fig6-illustrative-workflow-examples.png`). Read each file's TAIL, not just wc -l — a known local-model failure mode is a repetition loop that pads line count with nonsense near the end.

Build a BAD list and a GOOD list.

## Step 3: Handle BAD pages

**If BAD is empty**, go straight to Step 4.

**If BAD is non-empty:** for each bad page, count existing beads titled `"ArxivGraphPlanner chunk NN extract"` (including any retry suffixes) to get its attempt count.
- Attempt count < 3: delete the bad wiki page file, create ONE retry extract bead reusing the corresponding `source/specs/NN-extract.md` file verbatim: `fleet bd create "ArxivGraphPlanner chunk NN extract retry" --cwd /Users/sergii/.kb --coder opencode --model ollama-rtx/qwen3.8:27b -p 2 -t task --body-file /Users/sergii/.kb/papers/ArxivGraphPlanner/source/specs/NN-extract.md --silent`. Record its id.
- Attempt count >= 3: this chunk exhausted its retry budget. Write that one wiki page BY HAND, directly from `source/chunks/NN.txt` text, following the same format contract as the spec (this is a last resort, not the default path). Do not requeue it.

If any retries were created this round: create ONE successor finalize bead depending on all of them (`--deps "<retry-id-1>,<retry-id-2>,..."`), close your own bead with reason `"rearmed as <new-id>: N chunk(s) requeued"`, and stop. If every bad page was instead hand-written (nothing requeued), continue to Step 4 in this same run.

## Step 4: Synthesize the remaining artifacts

Read the (now-good) wiki pages — not the raw source, except to spot-check quality — and per `kb show summary/get` conventions produce:

- **`summary.md`** — the A2-template: Human Readable TL;DR, TL;DR, Problem & Motivation, Main Original Ideas, Key Findings (with a results table), Suggestions & Future Directions, Authors & Institutions (Tao Feng, Haozhen Zhang, Zijie Lei, Peixuan Han, Jiaxuan You), Figures section. Metadata line: `**Paper:** [GraphPlanner: Graph Memory-Augmented Agentic Routing for Multi-Agent LLMs (Feng et al., 2026)](https://arxiv.org/abs/2604.23626)`. Keep under 300 lines.
- **`digest.md`** — copy each wiki page's `**In one sentence:**` and `## Key points` bullets verbatim, in order (01→06), end with `## The argument in five moves`.
- **`index.md`** — front-matter with `type: Paper`, title, one-sentence description, `generated: { by: claude/sonnet, at: <ISO-8601 UTC timestamp> }`, `sources: [{id: original, resource: https://arxiv.org/abs/2604.23626}, {id: local-copy, resource: source/2604.23626.pdf}]`, tags (e.g. `[agentic-graphrag, multi-agent-llm, llm-routing, reinforcement-learning, graph-neural-network]`); orientation paragraph; "How to work through this" ladder; Read This Folder links; wiki table (6 rows, reading order); Original Source link.
- **`explainer.md`** — plain-language layer per the shared spec (What is this about / Why does it matter / How does it work / Where can this be used / Conclusions & takeaways / Jargon decoder with 5-12 terms). 80-150 lines.
- **`questions.md`** — 8-12 retrieval-practice questions (this is a long paper, 30-100pp range), at least one per wiki page, mixing core recall / elaboration / transfer / one evaluation question drawing on `critical_thinking.md`. Answers ONLY inside collapsed `> [!tip]- Answer` callouts.
- **`critical_thinking.md`** — Claims vs. evidence, Genuinely new vs. repackaged, Weaknesses and blind spots, Applicability, Relevance to my work (Sergii's AI/ML engineering + agentic systems + Elisity data platform contexts), What this changes, Verdict (end with one of adopt/trial/watch/skip). 60-120 lines.
- **`connections.md`** — read `/Users/sergii/.kb/ai_papers/index.md`, skim the graph_rag category and `ls /Users/sergii/.kb/papers/` for related recently-ingested agentic-GraphRAG / multi-agent-routing papers; select 2-6 genuinely related entries with the relationship type (builds-on, contradicts, same-problem-different-method, shares-technique, applies-in-practice). If none, say so in one line.

All internal links use Obsidian `[[wikilink]]` syntax; every sub-file has a backlink line to `index` and `summary`.

## Step 5: Report and close

Write `/Users/sergii/.kb/papers/ArxivGraphPlanner/source/delegation_report.md`:
- Chunks total (6) / passed first try / requeued (how many rounds, which chunks) / hand-written after exhausting retries.

Then: `bd close <own-id> --reason "wiki complete"`

No git commands anywhere in this task — `.kb` auto-syncs on its own.
