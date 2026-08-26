# Task: write wiki page 05 for the Meta-Harness paper

Context is tight on this model — read ONLY the one input file listed below (plus the six figure-description files listed), nothing else. Do NOT read this task's own fleet artifacts/log/event files, and do NOT read sibling wiki pages "for style/convention reference" — the format contract below is the only convention needed. If this is a retry, do not diagnose the prior failure by reading logs; just re-read the input and write directly.

## Input

Read this file in full: `/Users/sergii/.kb/papers/MetaHarness/source/chunks/05.txt`

It contains the Appendices of the paper "Meta-Harness: End-to-End Optimization of Model Harnesses" (arXiv 2603.28052):
- **Appendix A** — Qualitative Proposer Behavior: a step-by-step case study of the search trajectory (iterations 1 through 10+), showing how the agentic proposer diagnosed confounds, made regressions, and eventually found the winning candidate and composed improvements.
- **Appendix B** — Discovered Harnesses: concrete descriptions of the discovered harness programs (draft-verification classification harness, label-primed query-anchored classification harness, the math retrieval router, the TerminalBench-2 harness).
- **Appendix C** — Dataset Details (brief — summarize only the dataset counts/sizes, do not enumerate every row).
- **Appendix D** — Practical Implementation Tips.
- **Appendix E** — Extended Related Work (AlphaEvolve/OpenEvolve, prompt orchestration frameworks, etc.).

Also read these six figure-description files and use them to write the parts of the page discussing each figure:

- `/Users/sergii/.kb/papers/MetaHarness/wiki/images/fig4-search-accuracy-description.md` — describes `fig4-search-accuracy.png` (Figure 4: search-set accuracy over evaluations)
- `/Users/sergii/.kb/papers/MetaHarness/wiki/images/fig5-draft-verification-description.md` — describes `fig5-draft-verification.png` (Figure 5: draft-verification classification harness)
- `/Users/sergii/.kb/papers/MetaHarness/wiki/images/fig6-label-primed-query-description.md` — describes `fig6-label-primed-query.png` (Figure 6: label-primed query-anchored classification harness)
- `/Users/sergii/.kb/papers/MetaHarness/wiki/images/fig7-search-vs-test-accuracy-description.md` — describes `fig7-search-vs-test-accuracy.png` (Figure 7: search-set vs. test accuracy per dataset)
- `/Users/sergii/.kb/papers/MetaHarness/wiki/images/fig8-math-retrieval-harness-description.md` — describes `fig8-math-retrieval-harness.png` (Figure 8: discovered math retrieval harness)
- `/Users/sergii/.kb/papers/MetaHarness/wiki/images/fig9-terminalbench-harness-description.md` — describes `fig9-terminalbench-harness.png` (Figure 9: discovered TerminalBench-2 harness)

## Output

Write the file: `/Users/sergii/.kb/papers/MetaHarness/wiki/05-appendix-case-studies.md`

**If this file already exists (a retry), overwrite it completely.**

## Format contract (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Appendix: Case Studies and Discovered Harnesses

**In one sentence:** <the whole argument of the appendices in one sentence>

## Key points

- <5-8 bullets, each a complete standalone claim with real content (the search-trajectory narrative arc, concrete harness mechanisms, key numbers) — not "discusses X">

---

## The search trajectory: a case study (Appendix A)

<narrate the iteration-by-iteration story from the source: early bugfixes confounded by prompt edits, the proposer identifying the confound, direct fixes regressing, the winning candidate, composition, cross-run transfer. Use the source's own iteration numbers and framing.>

![Search-set accuracy over evaluations](images/fig4-search-accuracy.png)

<describe using the figure-description file>

## Discovered classification harnesses (Appendix B)

![Draft-verification classification harness](images/fig5-draft-verification.png)

<describe the draft-verification harness mechanism using the figure-description file and source text>

![Label-primed query-anchored classification harness](images/fig6-label-primed-query.png)

<describe the label-primed query-anchored harness mechanism>

![Search-set vs. test accuracy per dataset](images/fig7-search-vs-test-accuracy.png)

<describe using the figure-description file>

## Discovered math retrieval harness (Appendix B)

![Discovered math retrieval harness](images/fig8-math-retrieval-harness.png)

<describe the router/retrieval mechanism using the figure-description file and source text>

## Discovered TerminalBench-2 harness (Appendix B)

![Discovered TerminalBench-2 harness](images/fig9-terminalbench-harness.png)

<describe the harness structure using the figure-description file and source text>

## Dataset details (Appendix C)

<brief summary of dataset counts/sizes only — do not enumerate every row of any table>

## Practical implementation tips (Appendix D)

<concrete tips given by the authors>

## Extended related work (Appendix E)

<AlphaEvolve/OpenEvolve comparison, prompt orchestration frameworks, and any other related-work threads in this appendix>

**Covers:** Appendices A (Qualitative Proposer Behavior), B (Discovered Harnesses), C (Dataset Details), D (Practical Implementation Tips), E (Extended Related Work)
```

Rules:
- The page must be self-contained (readable without other wiki pages).
- No line limit — be thorough on Appendices A and B (the most substantive); Appendices C-E can be more concise but must still be covered, not silently dropped.
- Embed all six figures at the point in the text where they are discussed, using the vision descriptions to write the caption/description text.
- Use Obsidian `[[wikilink]]` syntax only for the backlink line shown above.

## Done

Write the output file, then run: `bd close <own-id> --reason "chunk 05 extracted"`

Scope: touch ONLY the one output file listed above. Do not run any fleet commands other than the `bd close` above.
