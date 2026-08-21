# Task: Extract wiki page 04 — Discussions (HippoRAG paper)

Context is tight on this model — read ONLY the chunk file listed below, nothing else. Do NOT read this task's own fleet artifacts/log/event files (`~/.fleet/tasks/<id>/...`, `events.jsonl`, `task.json`, `PLAN_AND_STATUS.md`, `KNOWLEDGE.md`), and do NOT read sibling wiki pages "for style/convention reference" — the format contract below is the only convention needed. If this is a retry, do not diagnose the prior failure by reading logs; just re-read the chunk and write directly.

## Input

- Chunk text (source content to summarize): `/Users/sergii/.kb/papers/ArxivHippoRAG/source/chunks/04.txt`
- No figures in this chunk.

## Output

Write exactly one file: `/Users/sergii/.kb/papers/ArxivHippoRAG/wiki/04-discussions.md`

If this file already exists (a retry), overwrite it completely.

## What this chunk covers

Section 5 (Discussions): ablation studies on OpenIE alternatives (e.g. REBEL), PPR alternatives (direct-neighbor baselines), the knowledge-integration advantage of HippoRAG over conventional RAG on path-finding multi-hop questions, and the efficiency comparison against IRCoT (cost/speed of online retrieval).

## Wiki page format contract (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Discussions: Ablations, Integration & Efficiency

**In one sentence:** <the whole argument of this section in one sentence>

## Key points

- <complete claim with real numbers/mechanisms/conclusions>
- <5-8 bullets total>

---

## OpenIE Alternatives

<full detail — what REBEL is, the performance drop observed, exact numbers>

## PPR Alternatives

<full detail — direct-neighbor baseline vs PPR, why PPR wins>

## Knowledge Integration Advantage

<full detail — path-finding vs path-following questions, the birthdate/importance example if present, exact percentage improvements>

## Efficiency

<full detail — exact cost/speed multipliers vs IRCoT>

**Covers:** Section 5 (Discussions), pages 10-13
```

Rules:
- Backlink line, one-sentence headline, and Key points block are mandatory and must come first.
- Preserve exact numbers (percentages, cost/speed multipliers) from the chunk.
- No meta-commentary about the extraction process itself. No placeholder text.
- Do not fabricate content not present in the chunk.

## DoD (definition of done)

1. `/Users/sergii/.kb/papers/ArxivHippoRAG/wiki/04-discussions.md` is written per the contract above.
2. Run `bd close <own-id> --reason "chunk 04 extracted"`.

## Scope

Touch ONLY the one output file above. Do not run any fleet commands other than the `bd close` above.
