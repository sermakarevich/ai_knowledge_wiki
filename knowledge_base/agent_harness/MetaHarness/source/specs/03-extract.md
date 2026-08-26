# Task: write wiki page 03 for the Meta-Harness paper

Context is tight on this model — read ONLY the one input file listed below (plus the one figure-description file listed), nothing else. Do NOT read this task's own fleet artifacts/log/event files, and do NOT read sibling wiki pages "for style/convention reference" — the format contract below is the only convention needed. If this is a retry, do not diagnose the prior failure by reading logs; just re-read the input and write directly.

## Input

Read this file in full: `/Users/sergii/.kb/papers/MetaHarness/source/chunks/03.txt`

It contains Sections 4.1 ("Online Text Classification") and 4.2 ("Harnesses for Retrieval-Augmented Reasoning") of the paper "Meta-Harness: End-to-End Optimization of Model Harnesses" (arXiv 2603.28052). This covers: the text-classification benchmark setup, comparisons against text optimizers (OpenEvolve, TTT-Discover) and hand-designed harnesses (ACE), the accuracy-context tradeoff / Pareto frontier, out-of-distribution evaluation on nine held-out datasets, and the retrieval-augmented math reasoning experiments (200 IMO-level problems, five held-out models).

Also read this figure-description file and use it to write the part of the page discussing the Pareto frontier figure:

- `/Users/sergii/.kb/papers/MetaHarness/wiki/images/fig3-pareto-frontier-description.md` — describes `fig3-pareto-frontier.png` (Figure 3)

## Output

Write the file: `/Users/sergii/.kb/papers/MetaHarness/wiki/03-classification-and-reasoning-experiments.md`

**If this file already exists (a retry), overwrite it completely.**

## Format contract (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Classification and Reasoning Experiments

**In one sentence:** <the whole argument of these two experiment sections in one sentence>

## Key points

- <5-8 bullets, each a complete standalone claim with exact numbers/results — not "discusses X">

---

## Online text classification setup

<benchmark, baselines, evaluation protocol>

## Comparison vs. text optimizers and hand-designed harnesses

<exact numbers: the 7.7-point improvement, 4x fewer context tokens, comparison to OpenEvolve/TTT-Discover/ACE, evaluation-count speedup>

## Accuracy-context tradeoffs

![Pareto frontier of accuracy vs. context cost](images/fig3-pareto-frontier.png)

<describe the Pareto frontier using the figure-description file content, plus the surrounding text>

## Out-of-distribution evaluation

<the nine held-out datasets, generalization results>

## Retrieval-augmented math reasoning

<the 200 IMO-level problems, the discovered harness, the 4.7-point average improvement across five held-out models, any tables of per-model or per-dataset results with exact numbers>

**Covers:** Section 4.1 (Online Text Classification), Section 4.2 (Harnesses for Retrieval-Augmented Reasoning)
```

Rules:
- The page must be self-contained (readable without other wiki pages).
- No line limit — be thorough. Preserve every exact number and result you can find in the chunk (accuracy percentages, point deltas, dataset counts, context-token multipliers).
- Use Obsidian `[[wikilink]]` syntax only for the backlink line shown above.

## Done

Write the output file, then run: `bd close <own-id> --reason "chunk 03 extracted"`

Scope: touch ONLY the one output file listed above. Do not run any fleet commands other than the `bd close` above.
