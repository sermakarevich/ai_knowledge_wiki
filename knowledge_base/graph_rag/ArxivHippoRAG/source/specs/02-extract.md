# Task: Extract wiki page 02 — Detailed Methodology (HippoRAG paper)

Context is tight on this model — read ONLY the chunk file (+ figure description file) listed below, nothing else. Do NOT read this task's own fleet artifacts/log/event files (`~/.fleet/tasks/<id>/...`, `events.jsonl`, `task.json`, `PLAN_AND_STATUS.md`, `KNOWLEDGE.md`), and do NOT read sibling wiki pages "for style/convention reference" — the format contract below is the only convention needed. If this is a retry, do not diagnose the prior failure by reading logs; just re-read the chunk and write directly.

## Input

- Chunk text (source content to summarize): `/Users/sergii/.kb/papers/ArxivHippoRAG/source/chunks/02.txt`
- Figure description (for a figure discussed in this chunk — embed it): `/Users/sergii/.kb/papers/ArxivHippoRAG/wiki/images/figure2-description.md`
- The actual figure image file already exists at: `/Users/sergii/.kb/papers/ArxivHippoRAG/wiki/images/figure2.png`

## Output

Write exactly one file: `/Users/sergii/.kb/papers/ArxivHippoRAG/wiki/02-methodology.md`

If this file already exists (a retry), overwrite it completely.

## What this chunk covers

Section 2 (Methodology) in detail: the offline indexing phase (open information extraction / OpenIE via LLM to build a knowledge graph, synonym-detection edges via a retrieval encoder), the online retrieval phase (LLM-based named-entity extraction from the query, linking query entities to graph nodes, running Personalized PageRank over the graph), and node specificity (an inverse-document-frequency-like weighting of graph nodes inspired by neurobiological plausibility).

## Wiki page format contract (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Detailed Methodology

**In one sentence:** <the whole argument/mechanism of this section in one sentence>

## Key points

- <complete claim, not a topic label — include real numbers/mechanisms/conclusions>
- <5-8 bullets total>

---

## Offline Indexing

<full detail: OpenIE process, triple extraction, synonym edges via retrieval encoder, how the knowledge graph is built>

![Detailed HippoRAG Methodology (Figure 2)](images/figure2.png)

<embed the figure next to the passage discussing Figure 2 — integrate the figure description into accurate prose, don't paste verbatim>

## Online Retrieval

<full detail: query NER, node linking, Personalized PageRank mechanics>

## Node Specificity

<full detail: the IDF-like weighting mechanism and its neurobiological motivation>

**Covers:** Section 2 (Methodology), pages 3-6
```

Rules:
- Backlink line, one-sentence headline, and Key points block are mandatory and must come first.
- Key points bullets must stand alone as this section's substance.
- Embed the figure using the exact path `images/figure2.png` next to the text that discusses it.
- Preserve exact terminology (OpenIE, PPR, node specificity) and any formulas/equations present in the chunk.
- No meta-commentary about the extraction process itself. No placeholder text.
- Do not fabricate content not present in the chunk.

## DoD (definition of done)

1. `/Users/sergii/.kb/papers/ArxivHippoRAG/wiki/02-methodology.md` is written per the contract above.
2. Run `bd close <own-id> --reason "chunk 02 extracted"`.

## Scope

Touch ONLY the one output file above. Do not run any fleet commands other than the `bd close` above.
