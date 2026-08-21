# Task: Extract wiki page 03 — Experiments and Production Results

## Context is tight on this model

Read ONLY this spec and the one input file listed below. Nothing else. Do NOT read this
task's own fleet artifacts/log/event files (`~/.fleet/tasks/<id>/...`, `events.jsonl`,
`task.json`, `PLAN_AND_STATUS.md`, `KNOWLEDGE.md`), and do NOT read any sibling wiki page
"for style/reference" — the format contract below is the only convention you need.

If this is a retry: do not try to diagnose the previous failure by reading logs. Just
re-read the input file and write the output directly.

## Input

Read this file in full:
`/Users/sergii/.kb/papers/ArxivGraphRAGLinkedInCustomerService/source/chunks/03.txt`

It covers pages 4-5 of the paper: Section 4 Experiment (design, and Result and Analysis with
Table 1 Retrieval Performance and Table 2 Question Answering Performance), Section 5
Production Use Case (Table 3 Customer Support Issue Resolution Time), Section 6 Conclusions
and Future Work, and the Company Portrait / Presenter Bio / References sections (skip the
References list itself — it is not content to summarize, but you may note 1-2 of the most
relevant cited works in passing if directly discussed in the main text, e.g. GPT-4, E5).

## Output

Write the full page to:
`/Users/sergii/.kb/papers/ArxivGraphRAGLinkedInCustomerService/wiki/03-experiments-and-production.md`

If this file already exists (a retry), overwrite it completely.

## Format contract (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Experiments and Production Results

**In one sentence:** <the whole result of this chunk in one sentence>

## Key points

- <complete-claim bullet with the actual numbers, e.g. the 77.6% MRR improvement, the 0.32
  BLEU improvement, the 28.6% median resolution-time reduction>
- <5-8 bullets total>

---

## Experiment Design

<summary of the golden dataset, control vs experimental group setup, same LLM (GPT-4) and
embedding model (E5) used for both, and the retrieval metrics (MRR, Recall@K, NDCG@K) and
generation metrics (BLEU, ROUGE, METEOR) used>

## Results

<reproduce Table 1 (Retrieval Performance: MRR, Recall@K at K=1/3, NDCG@K at K=1/3, baseline
vs experiment) and Table 2 (Question Answering Performance: BLEU, METEOR, ROUGE, baseline vs
experiment) as markdown tables with the exact numbers from the source, plus 1-2 sentences of
interpretation>

## Production Deployment

<summary of Section 5: the LinkedIn customer-service team A/B deployment, and Table 3
(Customer Support Issue Resolution Time: Mean, P50, P90, Tool Not Used vs Tool Used) as a
markdown table with exact numbers>

## Conclusions and Future Work

<summary of Section 6: what the paper concludes, and the three future-work directions named
(automated graph-template extraction, dynamic KG updates from queries, applicability beyond
customer service)>

**Covers:** pages 4-5 (Section 4 Experiment, Section 5 Production Use Case, Section 6
Conclusions and Future Work)
```

Rules:
- Reproduce Table 1, Table 2, and Table 3 as actual markdown tables with the exact numbers
  from the source text — do not paraphrase numeric results into prose only.
- The `## Key points` bullets must carry the concrete numbers, not vague claims.
- Be thorough; no line-count limit.

## Definition of done

1. Output file written at the path above, non-trivial (well over 40 lines), following the
   format contract, with all three tables reproduced with correct numbers.
2. Close this task: `bd close <own-id> --reason "chunk 03 extracted"`

## Scope

Touch ONLY the one output file listed above. Do not run any fleet command other than
`bd close` on your own task id. No git commands.
