# Task: Extract wiki page 03 — Experimental Setup & Retrieval/QA Results (HippoRAG paper)

Context is tight on this model — read ONLY the chunk file listed below, nothing else. Do NOT read this task's own fleet artifacts/log/event files (`~/.fleet/tasks/<id>/...`, `events.jsonl`, `task.json`, `PLAN_AND_STATUS.md`, `KNOWLEDGE.md`), and do NOT read sibling wiki pages "for style/convention reference" — the format contract below is the only convention needed. If this is a retry, do not diagnose the prior failure by reading logs; just re-read the chunk and write directly.

## Input

- Chunk text (source content to summarize): `/Users/sergii/.kb/papers/ArxivHippoRAG/source/chunks/03.txt`
- No figures in this chunk.

## Output

Write exactly one file: `/Users/sergii/.kb/papers/ArxivHippoRAG/wiki/03-experiments-results.md`

If this file already exists (a retry), overwrite it completely.

## What this chunk covers

Section 3 (Experimental Setup): datasets (MuSiQue, 2WikiMultiHopQA, HotpotQA), baselines (BM25, Contriever, ColBERTv2, IRCoT), evaluation protocol. Section 4 (Results): single-step retrieval results, multi-step retrieval results, question-answering results — with exact numbers/tables.

## Wiki page format contract (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Experimental Setup & Retrieval/QA Results

**In one sentence:** <the whole argument of this section in one sentence>

## Key points

- <complete claim with real numbers — e.g. specific accuracy/recall gains over baselines>
- <5-8 bullets total>

---

## Experimental Setup

<datasets, baselines, evaluation protocol — as tables where the source has tables>

## Single-Step Retrieval Results

<full detail with exact numbers from the source's tables>

## Multi-Step Retrieval Results

<full detail with exact numbers>

## Question Answering Results

<full detail with exact numbers>

**Covers:** Sections 3-4 (Experimental Setup, Results), pages 7-10
```

Rules:
- Backlink line, one-sentence headline, and Key points block are mandatory and must come first.
- Reproduce exact numbers and table structure from the chunk (as markdown tables) — this section is numbers-heavy, precision matters.
- No meta-commentary about the extraction process itself. No placeholder text.
- Do not fabricate content not present in the chunk.

## DoD (definition of done)

1. `/Users/sergii/.kb/papers/ArxivHippoRAG/wiki/03-experiments-results.md` is written per the contract above.
2. Run `bd close <own-id> --reason "chunk 03 extracted"`.

## Scope

Touch ONLY the one output file above. Do not run any fleet commands other than the `bd close` above.
