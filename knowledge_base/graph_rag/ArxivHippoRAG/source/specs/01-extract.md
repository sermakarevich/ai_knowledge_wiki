# Task: Extract wiki page 01 — Abstract & Introduction (HippoRAG paper)

Context is tight on this model — read ONLY the chunk file (+ figure description file) listed below, nothing else. Do NOT read this task's own fleet artifacts/log/event files (`~/.fleet/tasks/<id>/...`, `events.jsonl`, `task.json`, `PLAN_AND_STATUS.md`, `KNOWLEDGE.md`), and do NOT read sibling wiki pages "for style/convention reference" — the format contract below is the only convention needed. If this is a retry, do not diagnose the prior failure by reading logs; just re-read the chunk and write directly.

## Input

- Chunk text (source content to summarize): `/Users/sergii/.kb/papers/ArxivHippoRAG/source/chunks/01.txt`
- Figure description (for a figure discussed in this chunk — embed it): `/Users/sergii/.kb/papers/ArxivHippoRAG/wiki/images/figure1-description.md`
- The actual figure image file already exists at: `/Users/sergii/.kb/papers/ArxivHippoRAG/wiki/images/figure1.png`

## Output

Write exactly one file: `/Users/sergii/.kb/papers/ArxivHippoRAG/wiki/01-introduction.md`

If this file already exists (a retry), overwrite it completely.

## What this chunk covers

The paper's abstract and Section 1 (Introduction): the motivation for long-term memory in LLMs, the limitations of standard RAG on multi-hop / knowledge-integration questions, the neurobiological inspiration (hippocampal indexing theory), a high-level description of HippoRAG's three components, and headline results (accuracy gains, cost/speed advantages over IRCoT).

## Wiki page format contract (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Abstract & Introduction

**In one sentence:** <the whole argument of this section in one sentence>

## Key points

- <complete claim, not a topic label — include real numbers/mechanisms/conclusions>
- <5-8 bullets total>

---

## <subsection mirroring the source's structure>

<full detail prose, tables, exact numbers, verbatim key claims>

![Knowledge Integration & RAG (Figure 1)](images/figure1.png)

<embed the figure right next to the passage that discusses "path-finding" multi-hop questions / Figure 1, using the figure description file's content to write an accurate caption and in-text description — do not just paste the description verbatim, integrate it into the prose>

**Covers:** Abstract, Section 1 (Introduction), pages 1-2
```

Rules:
- Backlink line, one-sentence headline, and Key points block are mandatory and must come first.
- Key points bullets must stand alone as this section's substance — a reader who only reads the bullets should have the real content (not "discusses limitations of RAG").
- Embed the figure using the exact path `images/figure1.png` (relative from the wiki/ folder) next to the text that discusses it.
- No meta-commentary about the extraction process itself. No placeholder text.
- Target length: as thorough as the chunk warrants — do not artificially pad or truncate.
- Do not fabricate content not present in the chunk.

## DoD (definition of done)

1. `/Users/sergii/.kb/papers/ArxivHippoRAG/wiki/01-introduction.md` is written per the contract above.
2. Run `bd close <own-id> --reason "chunk 01 extracted"`.

## Scope

Touch ONLY the one output file above. Do not run any fleet commands other than the `bd close` above.
