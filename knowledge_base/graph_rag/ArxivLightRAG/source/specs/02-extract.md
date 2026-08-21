# Task: Write wiki page 02 — The LightRAG Architecture

## Context

You are extracting one section of the paper "LightRAG: Simple and Fast Retrieval-Augmented Generation" (arXiv:2410.05779) into one wiki page. This is chunk 2 of 5. Context is tight on this model — **read ONLY the input files listed below, nothing else.** Do NOT read this task's own fleet artifacts/logs (`~/.fleet/tasks/<id>/...`, `events.jsonl`, `task.json`, `PLAN_AND_STATUS.md`, `KNOWLEDGE.md`), and do NOT read sibling wiki pages "for style reference" — the format contract below is the only convention you need. If this is a retry, do not diagnose the prior failure by reading logs — just re-read the input and write directly.

## Input

Read these files only:
- `/Users/sergii/.kb/papers/ArxivLightRAG/source/chunks/02.txt` (the section text)
- `/Users/sergii/.kb/papers/ArxivLightRAG/wiki/images/fig1-architecture-description.md` (a text description of Figure 1, the framework's architecture diagram)

This chunk covers: RAG background (Section 2), and the LightRAG architecture (Section 3): graph-based text indexing (3.1), dual-level retrieval paradigm (3.2), retrieval-augmented answer generation (3.3), and complexity analysis (3.4).

There IS a figure for this chunk: `Figure 1: Overall architecture of the proposed LightRAG framework`. It has already been extracted as an image at `/Users/sergii/.kb/papers/ArxivLightRAG/wiki/images/fig1-architecture.png` — you do not need to view the image yourself; use the description file above to know what it shows, and embed it in the wiki page at the point where Figure 1 is discussed.

## Output

Write the file:
`/Users/sergii/.kb/papers/ArxivLightRAG/wiki/02-lightrag-architecture.md`

**If this file already exists (a retry), overwrite it completely.**

## Format contract (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# The LightRAG Architecture

**In one sentence:** <the chapter's whole argument, in one sentence>

## Key points

- <complete claim, not a topic label>
- <complete claim>
- (5-8 bullets total, each carrying real content — numbers, mechanisms, conclusions, not "discusses X">

---

## <subsection headings mirroring the chunk's own structure, e.g. RAG Background, Graph-Based Text Indexing, Dual-Level Retrieval Paradigm, Retrieval-Augmented Answer Generation, Complexity Analysis>

<hierarchical detail. Include exact numbers, terms, and definitions verbatim from the text where present. Be thorough — no line limit.>

![Overall architecture of the proposed LightRAG framework](images/fig1-architecture.png)

**Covers:** Section 2 (RAG background), Section 3 (LightRAG architecture, including Figure 1)
```

Rules:
- Embed the figure at the point in the detail section that discusses the architecture — image path is `images/fig1-architecture.png` (relative to the `wiki/` folder).
- Every wiki page opens with the backlink line, then `# <Topic>`, then `**In one sentence:**`, then `## Key points` (5-8 bullets that stand alone as this chapter at medium depth), then `---`, then full hierarchical detail, then the `**Covers:**` footer.
- Use Obsidian `[[wikilink]]` syntax for internal links (only the backlink line needs one here).
- No meta-commentary about your own process — only the paper's content.

## Scope

Touch ONLY the one output file listed above. Do not run any fleet commands other than the close command below.

## Done

1. Write the output file.
2. `bd close <own-id> --reason "chunk 02 extracted"`
