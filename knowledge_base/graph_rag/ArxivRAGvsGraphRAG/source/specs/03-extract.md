# Extract task: chunk 03 — Query-Based Summarization and Conclusion

## Context (tight — read ONLY what is listed below, nothing else)

You are writing ONE wiki page for a knowledge-base entry on the paper "RAG vs. GraphRAG: A Systematic Evaluation and Key Insights" (Han et al., 2025, arXiv:2502.11371).

Context is tight on this model — read ONLY the files listed below. Do NOT read this task's own fleet artifacts/log/event files (`~/.fleet/tasks/<id>/...`, `events.jsonl`, `task.json`, `PLAN_AND_STATUS.md`, `KNOWLEDGE.md`), and do NOT read sibling wiki pages "for style/convention reference" — the format contract below is the only convention needed. If this is a retry, do not diagnose the prior failure by reading logs; just re-read the chunk and write directly.

**Input (read exactly these files, nothing else):**
- `/Users/sergii/.kb/papers/ArxivRAGvsGraphRAG/source/chunks/03.txt` (the section text)
- `/Users/sergii/.kb/papers/ArxivRAGvsGraphRAG/wiki/images/fig4-llm-judge-position-bias-description.md` (description of Figure 4)

This chunk covers: Section 5 (Query-Based Summarization — datasets/metrics, summarization experimental results, position bias in LLM-as-a-Judge evaluation) and Section 6 (Conclusion).

**Output (write exactly this file):**
`/Users/sergii/.kb/papers/ArxivRAGvsGraphRAG/wiki/03-summarization-and-conclusion.md`

If this file already exists (a retry), overwrite it completely.

## Wiki page format contract (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Query-Based Summarization and Conclusion

**In one sentence:** <the section's whole argument, in one sentence>

## Key points

- <complete claim with real content — numbers, mechanisms, conclusions — not "discusses X">
- <5-8 bullets total>

---

<## subsections mirroring the chunk's internal structure: datasets/metrics, summarization results, position bias in LLM-as-a-Judge, and the paper's overall conclusion>
<tables, exact numbers verbatim from the chunk>

![LLM-as-a-Judge position bias comparison](images/fig4-llm-judge-position-bias.png)

<embed fig4 near the position-bias discussion, using the description file's content to write accurate prose — you cannot see the image directly, only its text description>

**Covers:** Sections 5-6 (Query-Based Summarization, Conclusion)
```

Rules:
- Backlink line first, exactly as shown.
- `**In one sentence:**` and `## Key points` near the top, before the `---` divider.
- Embed the figure (`![...](images/fig4-llm-judge-position-bias.png)`) at the point where the chunk discusses position bias in LLM-as-a-Judge evaluation.
- Cover the WHOLE chunk, including the Conclusion section at the end — do not stop after the summarization results.
- No line limit — be thorough, but no filler or repetition.
- No meta-commentary about the task itself; write only the page content.

## Done

1. Write the output file above.
2. `bd close <own-id> --reason "chunk 03 extracted"`

## Scope

Touch ONLY the one output file listed above. Do not run any fleet command other than `bd close`. Do not run git commands.
