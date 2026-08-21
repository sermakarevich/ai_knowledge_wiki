# Task: Extract wiki page 04 — Topic-Specific Analysis, Observations, Case Study & Conclusion

## Context

You are one worker in a pipeline turning an academic paper into a knowledge-base wiki. This task covers ONE chunk of the paper. Context is tight on this model — **read ONLY the chunk file listed below (and the figure description files), nothing else.** Do NOT read this task's own fleet artifacts/log/event files, do NOT read sibling wiki pages "for style/convention reference," and do NOT try to diagnose a prior failure by reading logs — the format contract below is the only convention you need. If this is a retry, just re-read the chunk and write directly.

## Input

Read this file (plain text, extracted from the paper "GraphRAG-Bench: Challenging Domain-Specific Reasoning Benchmark for GraphRAG"):

`/Users/sergii/.kb/papers/ArxivGraphRAGBench/source/chunks/04.txt`

This chunk covers: 4.5 Topic-specific generation accuracy analysis, 4.6 Observation (GraphRAG's differential effect by question type), 4.7 Case Study, and Section 5 Conclusion.

Also read these figure descriptions (vision-model descriptions of Figures 2 and 3, which belong in this chunk):

`/Users/sergii/.kb/papers/ArxivGraphRAGBench/wiki/images/fig2-description.md`
`/Users/sergii/.kb/papers/ArxivGraphRAGBench/wiki/images/fig3-description.md`

The actual image files already exist at `/Users/sergii/.kb/papers/ArxivGraphRAGBench/wiki/images/fig2-accuracy-by-topic.png` and `/Users/sergii/.kb/papers/ArxivGraphRAGBench/wiki/images/fig3-case-study.png` — embed them using the descriptions to write accurate surrounding text; you do not need to view the images yourself.

## Output

Write the wiki page to this exact path (if it already exists — a retry — overwrite it completely):

`/Users/sergii/.kb/papers/ArxivGraphRAGBench/wiki/04-topic-analysis-observations-and-conclusion.md`

## Format contract (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Topic-Specific Analysis, Observations, Case Study & Conclusion

**In one sentence:** <the whole argument of this chunk in one sentence>

## Key points

- <complete claim, not a topic label>
- <5-8 bullets total>

---

## Topic-specific generation accuracy (Section 4.5)

<full detail: GraphRAG degrades accuracy specifically in Mathematics (symbolic/precise reasoning mismatch with retrieved conceptual text), mediocre performance in Ethics (subjective value judgments resist symbolic KG representation), RAPTOR's robustness across most topics>

![Figure 2: Comparison of Generation Accuracy by Topic](images/fig2-accuracy-by-topic.png)

<a sentence or two describing what Figure 2 shows, based on the description file>

## Observations: does GraphRAG help every question type? (Section 4.6)

<full detail on the per-question-type effects: MC accuracy can drop (retrieval noise interferes with LLM's already-strong internal knowledge), TF improves (retrieved evidence helps verify statements), OE improves (external context reduces hallucination and enriches responses), FB and MS are mixed/retrieval-precision-dependent. Also cover the reasoning-capability finding: GraphRAG substantially improves R/AR reasoning scores across question types even where it doesn't always improve raw accuracy, and why (real-world stakes in education/medical scenarios needing explicit rationales)>

## Case study (Section 4.7)

<full detail on the computer-networks case study: the ISN (initial sequence number) question, and why it requires multi-hop synthesis rather than lookup>

![Figure 3: A case study in the topic of computer networks](images/fig3-case-study.png)

<reproduce or closely paraphrase the case study's question, the 3-step multi-hop reasoning chain, and the rationale, based on the description file and any text in the chunk>

## Conclusion (Section 5)

<full detail: paper's closing summary of contributions>

**Covers:** Sections 4.5-4.7 and Section 5 (Conclusion) of GraphRAG-Bench (arXiv:2506.02404)
```

Rules:
- The `## Key points` bullets must stand alone at medium depth — capture the Mathematics/Ethics degradation findings, the per-question-type pattern (MC down, TF/OE up, FB/MS mixed), the reasoning-vs-accuracy distinction, and the case study's core lesson (multi-hop synthesis beats lookup).
- No meta-commentary about your own process. Write only the finished page.
- Be thorough — no line limit.

## Scope & DoD

- Touch ONLY the one output file listed above.
- Do not run any fleet commands other than closing your own bead.
- When the file is written, close your own bead: `bd close <your-bead-id> --reason "chunk 04 extracted"`
