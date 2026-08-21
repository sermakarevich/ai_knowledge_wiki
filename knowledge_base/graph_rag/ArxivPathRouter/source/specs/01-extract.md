# Extract task: ArxivPathRouter wiki page 01

**Context is tight on this model — read ONLY the input file(s) listed below, nothing else.** Do NOT read this task's own fleet artifacts/log/event files (`~/.fleet/tasks/<id>/...`, `events.jsonl`, `task.json`, `PLAN_AND_STATUS.md`, `KNOWLEDGE.md`), and do NOT read sibling wiki pages "for style/convention reference" — the format contract below is the only convention needed. If this is a retry, do not diagnose the prior failure by reading logs; just re-read the chunk and write directly.

## Input

- `/Users/sergii/.kb/papers/ArxivPathRouter/source/chunks/01.txt` — plain text covering: Abstract, Section 1 Introduction, Section 2 Related Work of the paper "PathRouter: Aligning Rewards with Retrieval Quality in Agentic Graph Retrieval-Augmented Generation" (arXiv 2606.16409).
- Figure description (read this too): `/Users/sergii/.kb/papers/ArxivPathRouter/wiki/images/01-fig1-failure-modes-description.md` — describes Figure 1, which must be embedded in your page as `![Figure 1: Two failure modes](images/01-fig1-failure-modes.png)` at the point where the text discusses the two failure modes (reasoning failure and shortcut failure).

## Output

Write the full wiki page to: `/Users/sergii/.kb/papers/ArxivPathRouter/wiki/01-introduction-and-related-work.md`

**If this file already exists (a retry), overwrite it completely.**

## Page format (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Introduction and Related Work

**In one sentence:** <the whole argument of this section in one sentence — what problem the paper identifies and how prior GraphRAG/agentic-RAG work falls short of solving it>

## Key points

- <5-8 bullets, each a complete, standalone claim with real content (numbers, mechanisms, named failure modes) — not "discusses X". A reader who reads only these bullets should have the section's substance.>

---

## Problem: answer-path reward aliasing and search-update ambiguity

<full detail: explain both failure modes precisely, using the paper's own terms and Figure 1>

![Figure 1: Two failure modes](images/01-fig1-failure-modes.png)

<continue with full detail on the failure modes, using the figure description provided>

## Related work

<hierarchical subsections mirroring the source: chunk-based RAG, graph-structured RAG (entity-relation graphs), agentic/RL-trained retrieval approaches. Name specific prior methods mentioned in the text and how PathRouter differs.>

**Covers:** Abstract, Section 1 (Introduction), Section 2 (Related Work)
```

## Rules

- The page must be self-contained (readable without other pages).
- No line limit — be thorough, include all relevant details, terms, and named prior methods from the chunk.
- Use exact numbers/terms from the source (e.g., "answer-path reward aliasing", "search-update ambiguity", "evidence-path overlap (EO)").
- Do not invent content not present in the chunk or figure description.

## Done

1. Write the output file.
2. `bd close <own-id> --reason "chunk 01 extracted"`

## Scope

Touch ONLY `/Users/sergii/.kb/papers/ArxivPathRouter/wiki/01-introduction-and-related-work.md`. Do not run any fleet commands other than `bd close`. No git commands.
