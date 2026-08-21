# Task: Extract wiki page 05 — Related Work & Conclusions/Limitations (HippoRAG paper)

Context is tight on this model — read ONLY the chunk file listed below, nothing else. Do NOT read this task's own fleet artifacts/log/event files (`~/.fleet/tasks/<id>/...`, `events.jsonl`, `task.json`, `PLAN_AND_STATUS.md`, `KNOWLEDGE.md`), and do NOT read sibling wiki pages "for style/convention reference" — the format contract below is the only convention needed. If this is a retry, do not diagnose the prior failure by reading logs; just re-read the chunk and write directly.

## Input

- Chunk text (source content to summarize): `/Users/sergii/.kb/papers/ArxivHippoRAG/source/chunks/05.txt`
- No figures in this chunk.

## Output

Write exactly one file: `/Users/sergii/.kb/papers/ArxivHippoRAG/wiki/05-related-work-conclusion.md`

If this file already exists (a retry), overwrite it completely.

## What this chunk covers

Section 6 (Related Work): parametric long-term memory, long-context-as-memory approaches, RAG-as-long-term-memory methods (RAPTOR, MemWalker, GraphRAG), and other graph/hyperlink-based retrieval methods. Section 7 (Conclusions & Limitations): the paper's final claims and acknowledged limitations.

## Wiki page format contract (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Related Work & Conclusions

**In one sentence:** <the whole argument of this section in one sentence>

## Key points

- <complete claim, not a topic label>
- <5-8 bullets total>

---

## Parametric Long-Term Memory

<full detail>

## Long Context as Long-Term Memory

<full detail>

## RAG as Long-Term Memory

<full detail — how HippoRAG relates to/differs from RAPTOR, MemWalker, GraphRAG>

## Conclusions & Limitations

<full detail — final claims, acknowledged limitations, future directions if stated>

**Covers:** Sections 6-7 (Related Work, Conclusions & Limitations), pages 13-15
```

Rules:
- Backlink line, one-sentence headline, and Key points block are mandatory and must come first.
- Be precise about how HippoRAG is positioned relative to each related method named in the chunk.
- No meta-commentary about the extraction process itself. No placeholder text.
- Do not fabricate content not present in the chunk.

## DoD (definition of done)

1. `/Users/sergii/.kb/papers/ArxivHippoRAG/wiki/05-related-work-conclusion.md` is written per the contract above.
2. Run `bd close <own-id> --reason "chunk 05 extracted"`.

## Scope

Touch ONLY the one output file above. Do not run any fleet commands other than the `bd close` above.
