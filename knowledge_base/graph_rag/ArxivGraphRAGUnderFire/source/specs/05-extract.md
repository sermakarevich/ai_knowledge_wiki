# Task: Extract wiki page 05 — Defenses, Related Work, Conclusion

## Context

You are one worker in a chain that turns the paper "GraphRAG under Fire" (arXiv:2501.14050) into a wiki. Your job is ONLY to write ONE wiki page from ONE chunk of the paper's text. Context is tight on this model — **read ONLY the input file listed below, nothing else.** Do NOT read this task's own fleet artifacts/log/event files (`~/.fleet/tasks/<id>/...`, `events.jsonl`, `task.json`, `PLAN_AND_STATUS.md`, `KNOWLEDGE.md`), and do NOT read sibling wiki pages "for style/convention reference" — the format contract below is the only convention you need. If this is a retry, do NOT diagnose the prior failure by reading logs — just re-read the chunk and write directly.

## Input

- Chunk text: `/Users/sergii/.kb/papers/ArxivGraphRAGUnderFire/source/chunks/05.txt`
- This chunk covers: RQ3 — Potential Defenses (Sec 6: Query Paraphrasing, Knowledge Referencing / LLM knowledge incorporation, Chain-of-Thought consistency, Poisoning Text Identification), Related Work (Sec 7), and the Conclusion (Sec 8).
- No figures in this chunk.

## Output

Write the file: `/Users/sergii/.kb/papers/ArxivGraphRAGUnderFire/wiki/05-defenses-related-work-conclusion.md`

**If this file already exists (a retry), overwrite it completely.**

## Format contract (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Defenses, Related Work, and Conclusion

**In one sentence:** <the chunk's whole argument, in one sentence>

## Key points

- <complete claim, not a topic label>
- <5-8 bullets total, each carrying real content: numbers, mechanisms, conclusions>

---

<## subsections mirroring the chunk's own structure: each defense examined (query
paraphrasing, knowledge referencing, CoT consistency, poisoning text identification)
with its measured effectiveness against GRAGPOISON (reproduce numbers/tables),
Related Work (prior RAG poisoning attacks, knowledge graph attacks, RAG defenses —
name the specific prior works and how this paper differs), and the Conclusion's
summary of contributions and future directions.>

**Covers:** Sec 6 (RQ3: Potential Defenses), Sec 7 (Related Work), Sec 8 (Conclusion)
```

Rules:
- Cover the WHOLE chunk, including its ending.
- No meta-commentary, no repetition loops.
- Reproduce any defense-effectiveness tables as markdown tables with exact numbers.
- No line limit — be thorough.

## Scope & DoD

- Touch ONLY the one output file above.
- Do not run any fleet commands other than closing this task.
- When the file is written: `bd close <own-id> --reason "chunk 05 extracted"`
