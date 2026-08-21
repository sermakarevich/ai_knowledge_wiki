# Extract: ARES paper — Appendix Details

## Problem
Write one wiki page summarizing a chunk of an academic paper about ARES, an automated
evaluation framework for Retrieval-Augmented Generation (RAG) systems.

## Context is tight — read ONLY these files, nothing else
- Input chunk: `/Users/sergii/.kb/papers/ArxivARESRAGEvaluation/source/chunks/05.txt`
- Figure description (for Figures 2 and 3, embed it where the chunk text discusses them):
  the figure image file is at `/Users/sergii/.kb/papers/ArxivARESRAGEvaluation/wiki/images/02-fig2-3-nq-eval.png`
  and its description is below — use it to write the surrounding prose, do not just repeat it verbatim:

```
Figures 2 & 3 evaluate RAG systems on the Natural Questions (NQ) benchmark: Figure 2 is
Context Relevance, Figure 3 is Answer Relevance. Each compares three scoring sources per
RAG framework — ARES (blue, with confidence-interval error bars), RAGAS (orange), and
Ground Truth (green). Y-axis: RAG System Accuracy (0.0-1.0). X-axis: RAG framework, a
grid of retriever (BM25, OpenAI, ColBERT) x generator (MPT, GPT-3.5, GPT-4.0), plus a
Facebook RAG baseline. Trends: accuracy rises monotonically from BM25+MPT (lowest,
~0.2-0.4) to ColBERT+GPT-4.0 (highest, ~0.8-0.9); both retriever and generator quality
matter (ColBERT > OpenAI > BM25; GPT-4.0 > GPT-3.5 > MPT). ARES tracks Ground Truth
closely across configurations; RAGAS systematically under-scores relative to Ground
Truth, especially for Context Relevance on BM25 and OpenAI-MPT setups. Confidence
intervals tighten as accuracy rises. Takeaway: ARES is a faithful, low-variance proxy
for human relevance judgments, while RAGAS is a conservative under-estimator.
```

Do NOT read this task's own fleet artifacts/log/event files (`~/.fleet/tasks/<id>/...`,
`events.jsonl`, `task.json`, `PLAN_AND_STATUS.md`, `KNOWLEDGE.md`), and do NOT read
sibling wiki pages "for style/convention reference" — the format contract below is the
only convention needed. On a retry, do not diagnose the prior failure by reading logs;
just re-read the chunk and write directly.

## Fix
Read the chunk file above. It contains the paper's Appendix (sections A.1 through A.7):
fine-tuning configuration for the LLM judges, extended NQ evaluation figures (2 and 3),
a study comparing GPT-4-generated labels vs human labels (Table 4), real-world RAG system
ranking (Table 5), cross-domain judge transfer results (Table 6), few-shot prompts used
for synthetic query/answer generation, and positive/negative evaluation examples
(Table 7).

Write the wiki page to this EXACT path (create parent dirs if needed):
`/Users/sergii/.kb/papers/ArxivARESRAGEvaluation/wiki/05-appendix-details.md`

**If this file already exists (a retry), overwrite it completely.**

### Required format (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Appendix Details

**In one sentence:** <the chunk's whole argument in one sentence — the implementation
and robustness details that support the main paper's claims: fine-tuning specifics,
extended figures, GPT-4-as-labeler feasibility, real-world system ranking, and
cross-domain transfer>

## Key points

- <complete-sentence claim — repeat for 5-8 bullets, e.g. fine-tuning hyperparameters,
  the GPT-4-vs-human-label agreement finding, real-world RAG ranking outcome,
  cross-domain Kendall's tau results, and the synthetic-negative prompting approach>
- ...

---

## Fine-tuning Configuration (A.1)

<full detail: loss function, optimizer, classification head, learning rate schedule,
stopping criterion>

## Extended NQ Evaluation (Figures 2-3)

![RAG systems evaluated on NQ — context and answer relevance](images/02-fig2-3-nq-eval.png)

<1-2 paragraphs describing the figure using the description above plus any surrounding
chunk text>

## GPT-4 Labels vs. Human Labels (Table 4)

<full detail>

## Real-World RAG System Ranking (Table 5)

<full detail>

## Cross-Domain Judge Transfer (Table 6)

<full detail>

## Synthetic Data Generation Prompts and Examples (A.5-A.7, Table 7)

<full detail, covering the chunk through to its final content — do not stop early>

**Covers:** Appendix A.1-A.7 (Tables 4-7, Figures 2-3) — arXiv 2311.09476, pages 10-17
```

Guidance:
- Embed the figure exactly once, in the "Extended NQ Evaluation" section, using the
  markdown image syntax shown above (relative path `images/02-fig2-3-nq-eval.png`).
- Cover the ENTIRE chunk from A.1 through its final tables/examples — this is the
  longest chunk; do not stop after the first one or two subsections.
- Use exact numbers from any tables rendered as plain text.
- No meta-commentary about being an AI or about this task — write only the wiki page
  content itself.

## Tests
- File exists at the output path above.
- File is well over 40 lines.
- Contains the required backlink line, an `**In one sentence:**` line, a `## Key points`
  section with 5-8 bullets, the embedded figure image line, a `---` divider, and a
  `**Covers:**` footer line.

## DoD
1. Output file written to the exact path above.
2. `bd close <own-id> --reason "chunk 05 extracted"`

## Scope & constraints
- Touch ONLY the one output file listed above.
- No git commands at all — `.kb` auto-syncs.
- Do not run fleet commands other than `bd close`.
