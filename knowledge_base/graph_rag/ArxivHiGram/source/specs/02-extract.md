# Task: Extract wiki page 02 — HiGram experiments and results (chunk 02/02)

Context is tight on this model — read ONLY the chunk file (+ figure description files) listed below, nothing else. Do NOT read this task's own fleet artifacts/log/event files (`~/.fleet/tasks/<id>/...`, `events.jsonl`, `task.json`, `PLAN_AND_STATUS.md`, `KNOWLEDGE.md`), and do NOT read sibling wiki pages "for style/convention reference" — the format contract below is the only convention needed. On a retry, do not diagnose the prior failure by reading logs; just re-read the chunk and write directly.

## Input

- Chunk text: `/Users/sergii/.kb/papers/ArxivHiGram/source/chunks/02.txt`
  (covers the paper's Experiments section: 4.1 Experimental Setup, 4.2 Main Results, 4.3 Analysis, and the Conclusion)
- Figure description: `/Users/sergii/.kb/papers/ArxivHiGram/wiki/images/fig2-description.md`
  (describes `images/fig2-ablation.png`, captioned "Figure 2: Results of ablation of Memory Organization and Evidence Localization")
- Figure description: `/Users/sergii/.kb/papers/ArxivHiGram/wiki/images/fig3-description.md`
  (describes `images/fig3-sensitivity.png`, captioned "Figure 3: Sensitivity analysis of key hyperparameters on LoCoMo")

## Output

Write: `/Users/sergii/.kb/papers/ArxivHiGram/wiki/02-experiments-and-results.md`

If this file already exists (a retry), overwrite it completely.

## Format contract

Write a single self-contained wiki page in this exact structure:

```markdown
[[../index|Wiki]] | [[../summary|Summary]]

# Experiments and Results

**In one sentence:** <one sentence headline capturing the main experimental finding>

## Key points

- <bullet>
- <bullet>
- <bullet>
(4-8 bullets covering benchmarks used, baselines, headline results, and ablation takeaways)

## Full detail

<the full deep-dive content: describe the experimental setup (benchmarks — LoCoMo and
MemConflict — and baselines such as MemOS, LangMem, Letta, Mem0, A-MEM, ReadAgent, MemGPT),
the main results (how HiGram compares on Single-Hop / Multi-Hop / Temporal question
categories, and on the MemConflict dynamic/static/overall metrics), the ablation study
(effect of removing MicroGraph organization vs. removing the support subgraph — both on
answer quality and on token/inference cost), the memory update strategy comparison
(Table 3 — Append Only vs alternatives), and the hyperparameter sensitivity analysis
(K_g = number of retrieved MicroGraphs, K_p = number of candidate paths). Then cover the
Conclusion. Be thorough — this page is one of two that jointly cover the entire paper;
do not leave out details found in the chunk text, including the numeric results reported
in Tables 1-3 (reproduce the key numbers in prose or a small markdown table).>

![Figure 2: Results of ablation of Memory Organization and Evidence Localization](images/fig2-ablation.png)

<embed this figure right after the ablation-study discussion, using the figure description
to write 2-4 sentences of caption/explanation integrated into the prose>

![Figure 3: Sensitivity analysis of key hyperparameters on LoCoMo](images/fig3-sensitivity.png)

<embed this figure right after the hyperparameter-sensitivity discussion, same treatment>
```

Use the figure description files' content to write the explanations around the embedded images — do not just paste the descriptions verbatim, integrate them into the surrounding prose.

The page must cover the WHOLE chunk, including its ending (the Conclusion) — do not stop after the main results table.

## Scope & constraints

- Touch ONLY the one output file listed above.
- No git commands at all — `.kb` auto-syncs.
- Do not run fleet commands other than `bd close`.

## DoD

1. Output file written at the path above, following the format contract, non-trivial (well over 40 lines).
2. `bd close <own-id> --reason "chunk 02 extracted"`
