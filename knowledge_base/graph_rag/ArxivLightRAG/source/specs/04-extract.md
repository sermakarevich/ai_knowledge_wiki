# Task: Write wiki page 04 — Ablation Studies, Case Study, and Cost/Adaptability Analysis (RQ2-RQ4)

## Context

You are extracting one section of the paper "LightRAG: Simple and Fast Retrieval-Augmented Generation" (arXiv:2410.05779) into one wiki page. This is chunk 4 of 5. Context is tight on this model — **read ONLY the input files listed below, nothing else.** Do NOT read this task's own fleet artifacts/logs (`~/.fleet/tasks/<id>/...`, `events.jsonl`, `task.json`, `PLAN_AND_STATUS.md`, `KNOWLEDGE.md`), and do NOT read sibling wiki pages "for style reference" — the format contract below is the only convention you need. If this is a retry, do not diagnose the prior failure by reading logs — just re-read the input and write directly.

## Input

Read these files only:
- `/Users/sergii/.kb/papers/ArxivLightRAG/source/chunks/04.txt` (the section text)
- `/Users/sergii/.kb/papers/ArxivLightRAG/wiki/images/fig2-cost-comparison-description.md` (description of Figure 2, a cost-comparison chart)
- `/Users/sergii/.kb/papers/ArxivLightRAG/wiki/images/fig3-retrieval-generation-example-description.md` (description of Figure 3, a worked retrieval-and-generation example)

This chunk covers: ablation studies answering RQ2 (4.3 — impact of the dual-level retrieval paradigm and other components), the case study answering RQ3 (4.4 — a concrete example), and model cost and adaptability analysis answering RQ4 (4.5).

There are TWO figures for this chunk, both already extracted as images:
- `Figure 2: Comparison of Cost in Terms of Tokens` at `/Users/sergii/.kb/papers/ArxivLightRAG/wiki/images/fig2-cost-comparison.png`
- `Figure 3: A retrieval and generation example` at `/Users/sergii/.kb/papers/ArxivLightRAG/wiki/images/fig3-retrieval-generation-example.png`

You do not need to view the images yourself; use the description files above and embed both images in the wiki page at the points where each figure is discussed.

## Output

Write the file:
`/Users/sergii/.kb/papers/ArxivLightRAG/wiki/04-ablation-case-study-cost-analysis.md`

**If this file already exists (a retry), overwrite it completely.**

## Format contract (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Ablation Studies, Case Study, and Cost/Adaptability Analysis (RQ2-RQ4)

**In one sentence:** <the chapter's whole argument, in one sentence>

## Key points

- <complete claim, not a topic label>
- <complete claim>
- (5-8 bullets total, each carrying real content — numbers, mechanisms, conclusions, not "discusses X">

---

## <subsection headings mirroring the chunk's own structure, e.g. Ablation Studies (RQ2), Case Study (RQ3), Model Cost and Adaptability Analysis (RQ4)>

<hierarchical detail. Include exact numbers, ablation variants, and cost figures verbatim from the text where present, as markdown tables where the source has tabular results. Be thorough — no line limit.>

![Comparison of cost in terms of tokens](images/fig2-cost-comparison.png)

![A retrieval and generation example](images/fig3-retrieval-generation-example.png)

**Covers:** 4.3 ablation studies (RQ2), 4.4 case study (RQ3), 4.5 model cost and adaptability analysis (RQ4), Figures 2-3
```

Rules:
- Embed each figure at the point in the detail section that discusses it — image paths are `images/fig2-cost-comparison.png` and `images/fig3-retrieval-generation-example.png` (relative to the `wiki/` folder).
- Every wiki page opens with the backlink line, then `# <Topic>`, then `**In one sentence:**`, then `## Key points` (5-8 bullets that stand alone as this chapter at medium depth), then `---`, then full hierarchical detail, then the `**Covers:**` footer.
- Use Obsidian `[[wikilink]]` syntax for internal links (only the backlink line needs one here).
- No meta-commentary about your own process — only the paper's content.

## Scope

Touch ONLY the one output file listed above. Do not run any fleet commands other than the close command below.

## Done

1. Write the output file.
2. `bd close <own-id> --reason "chunk 04 extracted"`
