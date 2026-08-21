# Task: Finalize — verify + synthesize ArxivGraphRAGLinkedInCustomerService

You are the last bead in a fleet extraction chain for one KB entry. This is the ONLY
validation step in the whole pipeline — read this spec fully before doing anything.

## Source

Paper: "Retrieval-Augmented Generation with Knowledge Graphs for Customer Service Question
Answering" (Zhentao Xu et al., LinkedIn, SIGIR '24, arXiv:2404.17723v2).
URL: https://arxiv.org/abs/2404.17723

Folder: `/Users/sergii/.kb/papers/ArxivGraphRAGLinkedInCustomerService/`

Manifest: `source/chunks.json` maps each chunk file → intended wiki page → source pages →
figures. There are 3 chunks / 3 wiki pages total (this is a short 5-page SIGIR paper, so a
small wiki is correct — do not treat 3 pages as incomplete).

Local original PDF is NOT saved under `source/` yet — download it yourself if you need to
spot-check anything: `curl -sL -o source/2404.17723.pdf https://arxiv.org/pdf/2404.17723`
(only do this if you need to resolve a genuine ambiguity; the wiki pages should already
carry everything you need).

## Step 1: Completeness gate (self-rearm)

List all beads titled like "ArxivGraphRAGLinkedInCustomerService chunk NN extract" (including
any retry-suffixed ones) via `fleet bd list` / `fleet bd search`. If ANY are still
open/in-progress, this run is premature:
- Create a successor finalize bead: `fleet bd create "ArxivGraphRAGLinkedInCustomerService finalize: verify + synthesize" --cwd /Users/sergii/.kb --coder claude --model sonnet -p 1 -t task --body-file /Users/sergii/.kb/papers/ArxivGraphRAGLinkedInCustomerService/source/specs/finalize.md --deps "<the still-open bead ids>" --silent`
- Close your own bead: `fleet bd close <own-id> --reason "rearmed as <new-id>: chunks still in flight"`
- Stop.

## Step 2: Verify every wiki page

For each of the 3 chunks, check its wiki page (per `source/chunks.json`):
- File exists, is well over 40 lines.
- Follows the format contract: backlink line, `# Title`, `**In one sentence:**`, `## Key points`
  (5-8 real bullets), `---`, full detail sections, footer `**Covers:**` line.
- Covers the WHOLE chunk — read the file's TAIL, not just the head/length, to confirm the
  end of the chunk's material is present (e.g. page 02's page must cover BOTH Section 3.1
  AND 3.2, not just 3.1; page 03's page must include Table 3 and the Conclusions section,
  not stop at Table 1/2).
- No meta-junk (no "As an AI..." preambles, no repeated/looping text).
- Page 02 must have Figure 1 embedded as `![...](images/01-figure1-overview.png)` — check the
  file `wiki/images/01-figure1-overview.png` actually exists on disk. If the page cites the
  figure but the image file is missing, that is a defect.
- Page 03 must contain actual markdown tables (not just prose) reproducing Table 1, Table 2,
  and Table 3 numbers (baseline vs experiment MRR ~0.522 vs ~0.927; BLEU ~0.057 vs ~0.377;
  median resolution time 7h vs 5h P50).

Build a BAD list and a GOOD list.

## Step 3: Handle BAD chunks (if any)

If BAD is empty, go straight to Step 4.

For each bad chunk: count existing extract beads titled
"ArxivGraphRAGLinkedInCustomerService chunk NN extract" (any retry suffix) to get its attempt
count. RETRY_BUDGET = 3.

- Attempt count < 3: delete the bad wiki page file, create ONE retry extract bead reusing
  `source/specs/NN-extract.md` verbatim:
  `fleet bd create "ArxivGraphRAGLinkedInCustomerService chunk NN extract retry" --cwd /Users/sergii/.kb --coder opencode --model ollama-rtx/qwen3.8:27b -p 2 -t task --body-file /Users/sergii/.kb/papers/ArxivGraphRAGLinkedInCustomerService/source/specs/NN-extract.md --silent`
  Record its id.
- Attempt count >= 3: this chunk has exhausted retries. Write that one wiki page by hand
  (read the chunk file yourself and produce a page meeting the format contract in
  `NN-extract.md`). Do not requeue it.

If any retries were created this round: create ONE successor finalize bead depending on all
of them (same `--body-file` as above), close your own bead with reason
`"rearmed as <new-id>: N chunk(s) requeued"`, and stop. If every bad chunk was handled by
hand-writing (nothing requeued), continue to Step 4 in this same run.

## Step 4: Synthesize

Read the (now-verified) wiki pages — not the raw source, except to spot-check — and produce,
following `kb show summary/get` conventions exactly (routing, folder scaffold, wikilink rules,
front-matter, progressive disclosure):

- `summary.md` — rung 1, whole paper, shallow, ~2 min read.
- `digest.md` — rung 2, built AFTER the wiki pages by copying each page's `**In one sentence:**`
  line and `## Key points` bullets verbatim, plus a closing "The argument in five moves"
  section. ~60-80 lines is right for a short paper.
- `index.md` — the wiki hub with front-matter:
  ```yaml
  type: Paper
  title: Retrieval-Augmented Generation with Knowledge Graphs for Customer Service Question Answering
  description: <one sentence>
  generated: { by: claude/sonnet, at: <ISO-8601 UTC timestamp> }
  sources:
    - id: original
      resource: https://arxiv.org/abs/2404.17723
    - id: local-copy
      resource: source/2404.17723.pdf
  tags: [graph-rag, knowledge-graph, customer-service, retrieval, rag]
  ```
  and the standard "Read This Folder" + wiki table + "Original Source" sections. Note in the
  `summary.md` metadata line: `**Paper:** [Retrieval-Augmented Generation with Knowledge
  Graphs for Customer Service Question Answering (Xu et al., 2024)](https://arxiv.org/abs/2404.17723)`.
- `explainer.md` — plain-language explainer (no jargon), 80-150 lines, 5-12 jargon-decoder
  terms (e.g. RAG, knowledge graph, embedding, MRR, Cypher, EBR).
- `questions.md` — 6-8 retrieval-practice questions (short paper range), answers in collapsed
  callouts, even coverage across all 3 wiki pages.
- `critical_thinking.md` — claims vs evidence (note this is an industry short-paper with a
  single internal A/B and no public benchmark/held-out dataset released — flag that the
  "golden dataset" and gains are self-reported and not independently reproducible; note the
  small SIGIR short-paper format constraints), applicability, what it changes, a verdict.
- `connections.md` — search the existing KB (e.g. `/Users/sergii/.kb/papers/`,
  `/Users/sergii/.kb/ai_papers/` if present) for related GraphRAG / RAG entries (e.g.
  ArxivLightRAG, ArxivGraphRAGBench, LangGraph3YearsGraphEngineering if they exist) and link
  them with path-qualified `[[Folder/summary|Title]]` wikilinks; note the specific relation
  (e.g. shares the "structure-aware retrieval beats flat-chunk RAG" thesis with LightRAG,
  contrasts as a production case study vs a benchmark paper).

Also save the PDF to `source/2404.17723.pdf` if not already saved (see the curl command
above) so `index.md`'s local-copy source link is valid.

## Step 5: Report + close

Write `source/delegation_report.md`: chunks total (3) / passed first try / requeued (how many
rounds) / hand-written after exhausting retries.

Then: `fleet bd close <own-id> --reason "wiki complete"`

No git commands anywhere in this task — `.kb` auto-syncs.
