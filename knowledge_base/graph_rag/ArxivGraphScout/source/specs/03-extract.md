# Task: Extract wiki page 03 — Experiments and Results — GraphScout paper

You are writing ONE page of an LLM-wiki for the paper "GraphScout: Empowering Large Language Models with Intrinsic Exploration Ability for Agentic Graph Reasoning" (Ying et al., 2026).

**Context is tight on this model — read ONLY the two files listed below, nothing else.** Do NOT read this task's own fleet artifacts/log/event files (`~/.fleet/tasks/<id>/...`, `events.jsonl`, `task.json`, `PLAN_AND_STATUS.md`, `KNOWLEDGE.md`), and do NOT read sibling wiki pages "for style/convention reference" — the format contract below is the only convention needed. If this is a retry, do not diagnose the prior failure by reading logs; just re-read the chunk and write directly.

## Input files (read exactly these, in full)

1. `/Users/sergii/.kb/papers/ArxivGraphScout/source/chunks/03.txt` — the source text for this page (covers Section 4 Experiment: setup, overall accuracy, cross-domain generalization, ablation, difficulty-level and efficiency analysis; Section 5 Discussion — positioning GraphScout against Document-Centric vs Native-KG-Reasoning GraphRAG settings; and Section 6 Conclusion).
2. `/Users/sergii/.kb/papers/ArxivGraphScout/wiki/images/descriptions.md` — read only the two entries titled `fig3-cross-domain-heatmap.png (Figure 3 + Table 2)` and `fig456-difficulty-and-efficiency.png (Figures 4, 5, 6)`; ignore the other entries in that file.

## Output file

Write to: `/Users/sergii/.kb/papers/ArxivGraphScout/wiki/03-experiments-and-results.md`

**If this file already exists (a retry), overwrite it completely.**

## Required page format (fill this in from the chunk text — do not invent facts not in the chunk)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Experiments and Results

**In one sentence:** <the chapter's whole argument: GraphScout, evaluated on GRBENCH across 5 domains against multiple LLM backbones/baselines, achieves the strongest results while using far fewer tokens and generalizing across domains>

## Key points

- <5-8 bullets with exact numbers — e.g. the 16.7% average margin, specific QwenScore/F1 numbers, ablation deltas, cross-domain transfer results, token-efficiency figures>

---

## Experimental setup

<GRBENCH dataset description, the five domains, baselines compared (BaseLLM, TextRAG, GraphRAG, Cypher, GraphCoT, PolyG, GraphCounselor) and the LLM backbones used for them, evaluation metrics (QwenScore, F1), model variants and training settings (Qwen3-4B-Instruct-2507, Qwen3-8B, DeepSeek-Chat for Graph Quizzer, verl framework, GRPO, 400 optimization steps)>

## Overall accuracy

<Table 1 results as described in the chunk text — GraphScout vs baselines across domains, using exact numbers from the text>

## Cross-domain generalization

<Figure 3 heatmap findings: training on one domain, testing on all five; the magnitude of degradation and what it implies about learning transferable exploration behavior>

## Ablation analysis

<Table 2 findings: effect of removing Graph Solver, removing the Code Interpreter tool, removing the clue-based/evidence reward, and replacing Graph Quizzer with random-walk-based question generation — with the exact numbers from the chunk>

## Performance by difficulty level

<Figure 4 findings: Easy/Medium/Hard breakdown, why Hard questions are less improved (recommendation-style reasoning, less structured graph traversal), Healthcare having no hard questions>

## Efficiency analysis

<Figures 5-6 findings: token consumption and tool-call counts across difficulty and domain, and how GraphScout compares to GraphCoT/GraphCounselor/PolyG on token cost>

![Figure 3: Cross-domain generalization heatmap and ablation study](images/fig3-cross-domain-heatmap.png)

![Figures 4-6: Performance by difficulty level and token efficiency](images/fig456-difficulty-and-efficiency.png)

## Discussion: Document-Centric vs. Native-KG Reasoning

<Section 5's positioning of GraphScout: the two GraphRAG settings (Document-Centric — graphs built on-the-fly from text, e.g. HippoRAG, HyperGraphRAG, Graph-R1 — vs Native-KG Reasoning — reasoning over pre-existing curated graphs, e.g. GraphCoT, GraphCounselor, GraphScout), how their bottlenecks and goals differ, and why the paper's empirical comparisons focus on the Native-KG setting>

## Conclusion

<the paper's own conclusion paragraph, in the chunk text, restated>

**Covers:** Section 4 Experiment (4.1, 4.2 incl. sub-analyses), Section 5 Discussion, Section 6 Conclusion
```

## Rules

- Preserve exact numbers/percentages/table values as they appear in the chunk — this page lives or dies on precision of numbers.
- The `## Key points` block must stand alone as the chapter at medium depth — write real claims with numbers, not topic labels.
- Do not fabricate content beyond what's in the chunk text and the two figure descriptions you read.
- No git commands. No fleet commands other than the close command below.
- Touch ONLY the one output file listed above.

## Done

Once the file is written: `bd close <own-id> --reason "chunk 03 extracted"`
