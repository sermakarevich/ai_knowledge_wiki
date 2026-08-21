# Extract task: chunk 04 — Appendix: datasets, case studies, prompts

## Context (tight — read ONLY what is listed below, nothing else)

You are writing ONE wiki page for a knowledge-base entry on the paper "RAG vs. GraphRAG: A Systematic Evaluation and Key Insights" (Han et al., 2025, arXiv:2502.11371).

Context is tight on this model — read ONLY the files listed below. Do NOT read this task's own fleet artifacts/log/event files (`~/.fleet/tasks/<id>/...`, `events.jsonl`, `task.json`, `PLAN_AND_STATUS.md`, `KNOWLEDGE.md`), and do NOT read sibling wiki pages "for style/convention reference" — the format contract below is the only convention needed. If this is a retry, do not diagnose the prior failure by reading logs; just re-read the chunk and write directly.

**Input (read exactly these files, nothing else):**
- `/Users/sergii/.kb/papers/ArxivRAGvsGraphRAG/source/chunks/04.txt` (the appendix text — dataset statistics, extended QA breakdowns, case studies, prompt templates, extra evaluations)
- `/Users/sergii/.kb/papers/ArxivRAGvsGraphRAG/wiki/images/fig5-case-study-hotpot-1-description.md` (description of Figure 5)
- `/Users/sergii/.kb/papers/ArxivRAGvsGraphRAG/wiki/images/fig6-case-study-hotpot-2-description.md` (description of Figure 6)

This chunk covers the paper's Appendix: dataset details (Appendix A), extended experimental breakdowns, two concrete case studies (Case 1 and Case 2 from the Hotpot dataset, illustrated by Figures 5 and 6) showing where RAG fails and GraphRAG succeeds (and vice versa), the query-classification and LLM-as-a-Judge prompt templates, and any additional comparison results.

**Output (write exactly this file):**
`/Users/sergii/.kb/papers/ArxivRAGvsGraphRAG/wiki/04-appendix-datasets-and-case-studies.md`

If this file already exists (a retry), overwrite it completely.

## Wiki page format contract (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Appendix: Datasets and Case Studies

**In one sentence:** <the appendix's whole contribution — concrete evidence and detail backing the main paper's claims, in one sentence>

## Key points

- <complete claim with real content — numbers, mechanisms, conclusions — not "discusses X">
- <5-8 bullets total; prioritize the two case studies and any dataset statistics with real numbers>

---

<## subsections mirroring the chunk's internal structure: dataset statistics, extended results, case study 1, case study 2, prompt templates>
<tables, exact numbers verbatim from the chunk>

![Case 1 from Hotpot dataset: RAG fails, GraphRAG succeeds via community-level summarization](images/fig5-case-study-hotpot-1.png)

<embed fig5 in the Case 1 subsection>

![Case 2 from Hotpot dataset](images/fig6-case-study-hotpot-2.png)

<embed fig6 in the Case 2 subsection>

**Covers:** Appendix (datasets, case studies, prompt templates)
```

Rules:
- Backlink line first, exactly as shown.
- `**In one sentence:**` and `## Key points` near the top, before the `---` divider.
- Embed both figures at the point where the chunk discusses that specific case study, using the corresponding description file's content to write accurate prose — you cannot see the images directly, only their text descriptions.
- Cover the WHOLE chunk — both case studies, plus dataset/prompt material even if briefer.
- No line limit — be thorough, but no filler or repetition.
- No meta-commentary about the task itself; write only the page content.

## Done

1. Write the output file above.
2. `bd close <own-id> --reason "chunk 04 extracted"`

## Scope

Touch ONLY the one output file listed above. Do not run any fleet command other than `bd close`. Do not run git commands.
