# Task: Write wiki page 01 — Introduction and Motivation

## Context

You are extracting one section of the paper "LightRAG: Simple and Fast Retrieval-Augmented Generation" (arXiv:2410.05779) into one wiki page. This is chunk 1 of 5. Context is tight on this model — **read ONLY the input file listed below, nothing else.** Do NOT read this task's own fleet artifacts/logs (`~/.fleet/tasks/<id>/...`, `events.jsonl`, `task.json`, `PLAN_AND_STATUS.md`, `KNOWLEDGE.md`), and do NOT read sibling wiki pages "for style reference" — the format contract below is the only convention you need. If this is a retry, do not diagnose the prior failure by reading logs — just re-read the input and write directly.

## Input

Read this file only:
`/Users/sergii/.kb/papers/ArxivLightRAG/source/chunks/01.txt`

This chunk covers: the paper's title/abstract, introduction, the problem with existing RAG systems, and LightRAG's proposed contributions.

There are no figures for this chunk.

## Output

Write the file:
`/Users/sergii/.kb/papers/ArxivLightRAG/wiki/01-introduction-and-motivation.md`

**If this file already exists (a retry), overwrite it completely.**

## Format contract (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Introduction and Motivation

**In one sentence:** <the chapter's whole argument, in one sentence>

## Key points

- <complete claim, not a topic label>
- <complete claim>
- (5-8 bullets total, each carrying real content — numbers, mechanisms, conclusions, not "discusses X">

---

## <subsection headings mirroring the chunk's own structure>

<hierarchical detail. Include exact numbers, terms, and definitions verbatim from the text where present. Be thorough — no line limit.>

**Covers:** Title/abstract, introduction, problem statement, and proposed contributions (paper pp. 1-2)
```

Rules:
- Every wiki page opens with the backlink line, then `# <Topic>`, then `**In one sentence:**`, then `## Key points` (5-8 bullets that stand alone as this chapter at medium depth), then `---`, then full hierarchical detail, then the `**Covers:**` footer.
- Use Obsidian `[[wikilink]]` syntax for internal links (only the backlink line needs one here).
- No meta-commentary about your own process — only the paper's content.

## Scope

Touch ONLY the one output file listed above. Do not run any fleet commands other than the close command below.

## Done

1. Write the output file.
2. `bd close <own-id> --reason "chunk 01 extracted"`
