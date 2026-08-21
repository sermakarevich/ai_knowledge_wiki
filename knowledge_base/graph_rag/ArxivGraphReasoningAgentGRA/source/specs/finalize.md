# Task: finalize ArxivGraphReasoningAgentGRA — verify + synthesize

You are the finalize worker for the `summary/get_local` fleet pipeline (`kb show summary/get_local` and `kb show summary/get` describe the full convention — read both before writing anything, since you must produce the same output shape as the interactive skill). This is the ONLY validation step in the whole pipeline.

Paper: "Schema-Agnostic Graph Reasoning Agent for Hybrid Knowledge Graphs" (Marius Dragic, Alexandre Rio, Ruben Ifrah — Oplit R&D, July 2026). Source: https://arxiv.org/abs/2608.15834. Short technical white paper (12 pages), part of an agentic-GraphRAG batch scan.

Folder: `/Users/sergii/.kb/papers/ArxivGraphReasoningAgentGRA/`

## Step 1 — Completeness gate (self-rearm)

List beads matching `"ArxivGraphReasoningAgentGRA chunk" extract` (use `bd search` or `bd list` + grep — this also catches any retry beads a prior finalize round may have created). If ANY are still open/in-progress, this run is premature:
- Create a successor finalize bead with the same spec file (`--body-file` this exact file), `--deps <the still-open bead ids>`.
- Close your own bead: `bd close <own-id> --reason "rearmed as <new-id>: chunks still in flight"`.
- Stop.

## Step 2 — Verify every wiki page

Expected pages (from `/Users/sergii/.kb/papers/ArxivGraphReasoningAgentGRA/source/chunks.json`):
- `wiki/01-gra-agent-design.md` (chunk `source/chunks/01.txt`, spec `source/specs/01-extract.md`)
- `wiki/02-ufkm-benchmark.md` (chunk `source/chunks/02.txt`, spec `source/specs/02-extract.md`)
- `wiki/03-results.md` (chunk `source/chunks/03.txt`, spec `source/specs/03-extract.md`)
- `wiki/04-industrial-deployment.md` (chunk `source/chunks/04.txt`, spec `source/specs/04-extract.md`)

For each: check it exists, is non-trivial (>40 lines), matches the format contract in its spec file (headline sentence → key-points block → full detail), covers the WHOLE chunk (spot-check the chunk's LAST major topic, not just its opening — read the file's TAIL, not just its length; a known local-model failure mode is a repetition loop that pads line count with nonsense), has no meta-junk ("as an AI...", placeholder text), and reproduces the tables the spec calls for. Build a BAD list and a GOOD list.

There are no figure images in this paper (only a discarded company-logo PNG was found; all diagrams are vector/text-based and already in the chunk text) — do not expect or require `![...]()` image embeds on any page.

## Step 3 — Handle BAD pages

If BAD is empty, go straight to Step 4.

If BAD is non-empty, for each bad chunk NN:
- Count existing extract beads titled `"ArxivGraphReasoningAgentGRA chunk NN extract"` (including any retry suffix) to get its attempt count.
- Attempt count < 3 (RETRY_BUDGET): delete the bad page, create ONE retry extract bead reusing `source/specs/NN-extract.md` verbatim (`--coder opencode --model ollama-rtx/qwen3.8:27b`), record its id.
- Attempt count >= 3: this chunk has exhausted reprocessing — write that one wiki page by hand from `source/chunks/NN.txt` yourself (last resort only). Do not requeue it.

If any retries were created this round: create ONE successor finalize bead depending on all of them (same spec file, `--deps <retry-bead-ids>`), close your own bead with reason `"rearmed as <new-id>: N chunk(s) requeued"`, and stop.

If every bad chunk was handled by hand-writing (nothing requeued), continue to Step 4 in this same run.

## Step 4 — Synthesize the full wiki

Follow `kb show summary/get` conventions exactly. Read the four wiki pages (small, already ~10:1 compressed) — not the raw source — except to spot-check quality against `source/full_text.txt` if something looks off.

Source-type metadata for this entry:
- `type: Paper`
- `summary.md` metadata line: `**Paper:** [Schema-Agnostic Graph Reasoning Agent for Hybrid Knowledge Graphs (Dragic et al., 2026)](https://arxiv.org/abs/2608.15834)`
- `sources:` front-matter: `id: original, resource: https://arxiv.org/abs/2608.15834` and `id: local-copy, resource: source/paper.pdf`
- Tags: something like `[graph-rag, llm-agents, knowledge-graphs, tool-use, benchmarks]` (adjust to taste, 2-5 lowercase tags)

Produce, per the shared output conventions in `kb show summary/get`:

1. **`index.md`** — wiki hub with the OKF-style front-matter, orientation (2-3 sentences: GRA is a schema-agnostic graph-navigating agent with 7 generic tools that beats a full-context SQL baseline by 5.1pp on an industrial benchmark while reading under a third of the tokens), reading-ladder guide, and the wiki page table (4 pages).
2. **`summary.md`** — rung 1, whole paper, shallow (~2 min read). Write this yourself, synthesizing across all four wiki pages — do not copy verbatim from wiki/01 alone.
3. **`digest.md`** — rung 2, medium depth (~10 min read). Per the skill's "single source of truth" rule: copy each wiki page's own `**In one sentence:**` line and `## Key points` bullets verbatim into this file, one section per wiki page, in wiki-page order. Do not write digest content that doesn't appear in a wiki page.
4. **`explainer.md`** — plain-language explanation (no jargon), the core analogy (code agents / ls-cat-grep transfers to graph agents), what problem it solves, and why it matters for someone unfamiliar with GraphRAG or agentic tool use.
5. **`questions.md`** — 6-8 retrieval-practice questions (this is a short paper, per the size-scaling table) with answers collapsed (e.g. `<details><summary>Answer</summary>...</details>` or a similar collapsed format used elsewhere in this KB — check an existing `papers/*/questions.md` file for the house convention if unsure, but do NOT read unrelated full papers, just peek at one `questions.md` file's structure). Ensure every one of the 4 wiki pages has at least one question — do not draw all questions from pages 1-2.
6. **`critical_thinking.md`** — critical appraisal: claims vs. evidence (e.g. the paper itself notes GRA vs RSA gap is only +0.3 to +1.9pp — topology contributes little, the gain is mostly "selective access" vs "full context"; the benchmark is synthetic/single-domain; SQA's 17k-token prompt still fits every model's context window so the regime where structured navigation should help most remains untested), applicability, what it changes for someone building a GraphRAG agent, and a verdict.
7. **`connections.md`** — links to related entries in this KB. Search `/Users/sergii/.kb/ai_papers/graph_rag/` (recently created category — several agentic-GraphRAG papers already live there, e.g. `ArxivARESRAGEvaluation`, `ArxivGraphRAGLinkedInCustomerService`, and others from this same batch scan) for related summaries and link them with path-qualified wikilinks per the skill's convention, e.g. `[[ai_papers/graph_rag/SomeOtherPaper/summary|Some Other Paper]]`. Also note the paper's own related-work citations (ReAct, SWE-agent, GraphRAG, Think-on-Graph) as external connections in prose, not as wikilinks (they are not KB entries).

No git commands — `.kb` auto-syncs.

## Step 5 — Report + close

Write a completion report to `/Users/sergii/.kb/papers/ArxivGraphReasoningAgentGRA/source/delegation_report.md`: chunks total (4) / passed first try / requeued (how many rounds) / hand-written after exhausting retries.

Then: `bd close <own-id> --reason "wiki complete"`.

## Scope

Touch only files under `/Users/sergii/.kb/papers/ArxivGraphReasoningAgentGRA/` (all subpaths) and, read-only, files under `/Users/sergii/.kb/ai_papers/graph_rag/` for connections.md linking. Do not touch other papers' folders. Do not run `fleet serve restart` or `fleet run`.
