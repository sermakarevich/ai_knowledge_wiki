# Task: Extract wiki page 01 — Introduction and Background

## Context is tight on this model

Read ONLY the two input files listed below. Nothing else. Do NOT read this task's own fleet artifacts/log/event files (`~/.fleet/tasks/<id>/...`, `events.jsonl`, `task.json`, `PLAN_AND_STATUS.md`, `KNOWLEDGE.md`), and do NOT read sibling wiki pages "for style/convention reference" — the format contract below is the only convention you need. If this is a retry, do NOT diagnose the prior failure by reading logs — just re-read the input and write directly.

## Input

- Source text chunk: `/Users/sergii/.kb/papers/ArxivGraphRAGLocalToGlobal/source/chunks/01.txt`
  (covers: title/authors, Abstract, Section 1 Introduction, Section 2 Background — RAG approaches, knowledge graphs with LLMs, RAG evaluation criteria, and Figure 1's caption/pipeline diagram)
- Figure description (read and use when writing about Figure 1): `/Users/sergii/.kb/papers/ArxivGraphRAGLocalToGlobal/wiki/images/01-pipeline-description.md`
- The figure image itself already exists at `/Users/sergii/.kb/papers/ArxivGraphRAGLocalToGlobal/wiki/images/01-pipeline-figure1.png` — do not create or move it, just reference it by relative path `images/01-pipeline-figure1.png` in your embed.

## Output

Write to: `/Users/sergii/.kb/papers/ArxivGraphRAGLocalToGlobal/wiki/01-introduction-and-background.md`

**If this file already exists (a retry), overwrite it completely.**

## Format contract (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Introduction and Background

**In one sentence:** <the whole argument of this chunk in one sentence — what problem RAG has with global sensemaking questions and how GraphRAG is positioned to solve it>

## Key points

- <5-8 bullets, each a complete standalone claim with real content (numbers, mechanisms, definitions) — not "discusses X". Someone reading only these bullets should have the substance of this section.>

---

## <subsections mirroring the source's own structure, e.g. "The Sensemaking Problem", "Vector RAG and Its Limits", "GraphRAG's Approach", "Related Work on Knowledge Graphs with LLMs and RAG">

<full detail prose, hierarchical, covering the ENTIRE chunk — do not stop after the introduction and skip the Background section. Include exact terms, definitions, and citations as they appear (e.g. "Lewis et al., 2020" for RAG). Embed the figure inline near where it's discussed:>

![GraphRAG pipeline: indexing time and query time stages](images/01-pipeline-figure1.png)

<describe the figure in words using the figure description file content, integrated into the prose — do not just paste the description file verbatim, weave it in>

---

**Covers:** Title/Abstract, Section 1 (Introduction), Section 2 (Background: 2.1 RAG Approaches and Systems, 2.2 Using Knowledge Graphs with LLMs and RAG), Figure 1.
```

## Rules

- Cover the WHOLE chunk — check the end of the chunk (Background section) got real coverage, not just the Introduction at the top.
- No meta-commentary about your own process. No "as an AI" disclaimers. Just the page content.
- Use exact numbers, definitions, and terminology from the source text — do not paraphrase away specifics.
- The figure must actually be embedded with the markdown image syntax shown above (relative path `images/01-pipeline-figure1.png`), not just mentioned by name.

## Scope

Touch ONLY the one output file listed above. Do not run any fleet commands other than closing your own bead.

## DoD

1. `/Users/sergii/.kb/papers/ArxivGraphRAGLocalToGlobal/wiki/01-introduction-and-background.md` written per the format contract above, covering the entire chunk.
2. `bd close <own-id> --reason "chunk 01 extracted"`
