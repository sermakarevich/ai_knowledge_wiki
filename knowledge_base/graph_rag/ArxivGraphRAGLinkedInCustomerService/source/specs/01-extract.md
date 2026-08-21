# Task: Extract wiki page 01 — Introduction and Related Work

## Context is tight on this model

Read ONLY this spec and the one input file listed below. Nothing else. Do NOT read this
task's own fleet artifacts/log/event files (`~/.fleet/tasks/<id>/...`, `events.jsonl`,
`task.json`, `PLAN_AND_STATUS.md`, `KNOWLEDGE.md`), and do NOT read any sibling wiki page
"for style/reference" — the format contract below is the only convention you need.

If this is a retry: do not try to diagnose the previous failure by reading logs. Just
re-read the input file and write the output directly.

## Input

Read this file in full:
`/Users/sergii/.kb/papers/ArxivGraphRAGLinkedInCustomerService/source/chunks/01.txt`

It is pages 1–2 of the paper "Retrieval-Augmented Generation with Knowledge Graphs for
Customer Service Question Answering" (LinkedIn, SIGIR '24, arXiv:2404.17723). It contains:
the abstract, the Introduction (with the two limitations of plain-text RAG the paper
addresses), and the Related Work section (KG-QA taxonomy: retrieval-based / template-based
/ semantic-parsing-based, and recent LLM+KG integration work).

## Output

Write the full page to:
`/Users/sergii/.kb/papers/ArxivGraphRAGLinkedInCustomerService/wiki/01-introduction-and-related-work.md`

If this file already exists (a retry), overwrite it completely.

## Format contract (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Introduction and Related Work

**In one sentence:** <the whole argument of this chunk in one sentence>

## Key points

- <complete-claim bullet, not a topic label — include concrete details from the text>
- <5-8 bullets total>

---

## Introduction

<hierarchical summary of the Introduction: the problem, why retrieval matters for customer
service, and BOTH limitations of plain-text chunk-based RAG that the paper identifies
(structure loss, and answer-quality loss from segmentation) — with the concrete Jira
example the paper gives>

## Related Work

<hierarchical summary of the three QA-with-KG method families the paper cites (retrieval-based,
template-based, semantic-parsing-based), and the recent LLM+KG integration work (Think-on-Graph,
Reasoning-on-Graph, Mindmap, etc.) and how this paper positions itself relative to it>

**Covers:** pages 1-2 (Abstract, Section 1 Introduction, Section 2 Related Work)
```

Rules:
- The `## Key points` bullets must be complete, standalone claims with real content (numbers,
  named limitations, named methods) — not "discusses related work".
- No figures in this chunk — do not fabricate any image reference.
- Be thorough; no line-count limit.

## Definition of done

1. Output file written at the path above, non-trivial (well over 40 lines), following the
   format contract, covering the ENTIRE chunk (both the Introduction and the Related Work
   section — not just the abstract).
2. Close this task: `bd close <own-id> --reason "chunk 01 extracted"`

## Scope

Touch ONLY the one output file listed above. Do not run any fleet command other than
`bd close` on your own task id. No git commands.
