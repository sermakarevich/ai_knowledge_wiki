# Task: Write wiki page 05 — Related Work, Conclusion, and Appendix (Prompts and Case Study Details)

## Context

You are extracting one section of the paper "LightRAG: Simple and Fast Retrieval-Augmented Generation" (arXiv:2410.05779) into one wiki page. This is chunk 5 of 5 (the last chunk). Context is tight on this model — **read ONLY the input files listed below, nothing else.** Do NOT read this task's own fleet artifacts/logs (`~/.fleet/tasks/<id>/...`, `events.jsonl`, `task.json`, `PLAN_AND_STATUS.md`, `KNOWLEDGE.md`), and do NOT read sibling wiki pages "for style reference" — the format contract below is the only convention you need. If this is a retry, do not diagnose the prior failure by reading logs — just re-read the input and write directly.

## Input

Read these files only:
- `/Users/sergii/.kb/papers/ArxivLightRAG/source/chunks/05.txt` (the section text)
- `/Users/sergii/.kb/papers/ArxivLightRAG/wiki/images/fig4-graph-construction-prompt-description.md` (description of Figure 4, the graph-construction prompt)
- `/Users/sergii/.kb/papers/ArxivLightRAG/wiki/images/fig5-query-generation-prompt-description.md` (description of Figure 5, the query-generation prompt)
- `/Users/sergii/.kb/papers/ArxivLightRAG/wiki/images/fig6-keyword-extraction-prompt-description.md` (description of Figure 6, the keyword-extraction prompt)
- `/Users/sergii/.kb/papers/ArxivLightRAG/wiki/images/fig7-rag-evaluation-prompt-description.md` (description of Figure 7, the RAG-evaluation prompt)

This chunk covers: related work (Section 5 — 5.1 RAG with LLMs, 5.2 LLMs for graphs), the conclusion (Section 6), and the appendix (7.1 experimental data details, 7.2 case example of retrieval-augmented generation, 7.3 overview of the prompts used in LightRAG, 7.4 case study comparing LightRAG vs. the naive RAG baseline).

There are FOUR figures for this chunk, all already extracted as images:
- `Figure 4: Prompts for Graph Generation` at `/Users/sergii/.kb/papers/ArxivLightRAG/wiki/images/fig4-graph-construction-prompt.png`
- `Figure 5: Prompts for Query Generation` at `/Users/sergii/.kb/papers/ArxivLightRAG/wiki/images/fig5-query-generation-prompt.png`
- `Figure 6: Prompts for Keyword Extraction` at `/Users/sergii/.kb/papers/ArxivLightRAG/wiki/images/fig6-keyword-extraction-prompt.png`
- `Figure 7: Prompts for RAG Evaluation` at `/Users/sergii/.kb/papers/ArxivLightRAG/wiki/images/fig7-rag-evaluation-prompt.png`

You do not need to view the images yourself; use the description files above and embed each image in the wiki page at the point where that figure is discussed.

## Output

Write the file:
`/Users/sergii/.kb/papers/ArxivLightRAG/wiki/05-related-work-conclusion-appendix.md`

**If this file already exists (a retry), overwrite it completely.**

## Format contract (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Related Work, Conclusion, and Appendix

**In one sentence:** <the chapter's whole argument, in one sentence>

## Key points

- <complete claim, not a topic label>
- <complete claim>
- (5-8 bullets total, each carrying real content — numbers, mechanisms, conclusions, not "discusses X">

---

## <subsection headings mirroring the chunk's own structure, e.g. Related Work: RAG with LLMs, Related Work: LLMs for Graphs, Conclusion, Appendix: Experimental Data Details, Appendix: Case Example, Appendix: Prompts Used in LightRAG, Appendix: Case Study vs. Naive RAG>

<hierarchical detail. Include exact numbers, prior-work names, and dataset details verbatim from the text where present. Be thorough — no line limit.>

![Prompts for Graph Generation](images/fig4-graph-construction-prompt.png)

![Prompts for Query Generation](images/fig5-query-generation-prompt.png)

![Prompts for Keyword Extraction](images/fig6-keyword-extraction-prompt.png)

![Prompts for RAG Evaluation](images/fig7-rag-evaluation-prompt.png)

**Covers:** Section 5 (related work), Section 6 (conclusion), Appendix 7.1-7.4, Figures 4-7
```

Rules:
- Embed each figure at the point in the detail section that discusses it — image paths are `images/fig4-graph-construction-prompt.png`, `images/fig5-query-generation-prompt.png`, `images/fig6-keyword-extraction-prompt.png`, `images/fig7-rag-evaluation-prompt.png` (relative to the `wiki/` folder).
- Every wiki page opens with the backlink line, then `# <Topic>`, then `**In one sentence:**`, then `## Key points` (5-8 bullets that stand alone as this chapter at medium depth), then `---`, then full hierarchical detail, then the `**Covers:**` footer.
- Use Obsidian `[[wikilink]]` syntax for internal links (only the backlink line needs one here).
- No meta-commentary about your own process — only the paper's content.

## Scope

Touch ONLY the one output file listed above. Do not run any fleet commands other than the close command below.

## Done

1. Write the output file.
2. `bd close <own-id> --reason "chunk 05 extracted"`
