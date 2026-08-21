# Task: Extract wiki page 05 — Appendix: Prompts and Additional Experiments

## Context is tight on this model

Read ONLY the input files listed below. Nothing else. Do NOT read this task's own fleet artifacts/log/event files (`~/.fleet/tasks/<id>/...`, `events.jsonl`, `task.json`, `PLAN_AND_STATUS.md`, `KNOWLEDGE.md`), and do NOT read sibling wiki pages "for style/convention reference" — the format contract below is the only convention you need. If this is a retry, do NOT diagnose the prior failure by reading logs — just re-read the input and write directly.

## Input

- Source text chunk: `/Users/sergii/.kb/papers/ArxivGraphRAGLocalToGlobal/source/chunks/05.txt`
  (covers Appendices A through G: A - entity/claim extraction prompts and chunk-size/self-reflection trade-offs including Figure 3, B - example community detection including Figure 4, C - context window selection, D - LLM assessment example, E - generation prompts, F - evaluation prompts, G - statistical analysis. This is the longest chunk (~27k chars) — it is dense reference material, not narrative prose; summarize prompt templates rather than reproducing every full prompt verbatim, but keep concrete parameter values, thresholds, and example snippets.)
- Figure descriptions: `/Users/sergii/.kb/papers/ArxivGraphRAGLocalToGlobal/wiki/images/03-hotpotqa-description.md` (for Figure 3) and `/Users/sergii/.kb/papers/ArxivGraphRAGLocalToGlobal/wiki/images/04-communities-description.md` (for Figure 4)
- The figure images already exist at `/Users/sergii/.kb/papers/ArxivGraphRAGLocalToGlobal/wiki/images/03-hotpotqa-figure3.png` and `/Users/sergii/.kb/papers/ArxivGraphRAGLocalToGlobal/wiki/images/04-communities-figure4.png` — do not create or move them, just reference them by relative path in your embeds.

## Output

Write to: `/Users/sergii/.kb/papers/ArxivGraphRAGLocalToGlobal/wiki/05-appendix-prompts-and-additional-experiments.md`

**If this file already exists (a retry), overwrite it completely.**

## Format contract (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Appendix: Prompts and Additional Experiments

**In one sentence:** <what this appendix material adds beyond the main paper — implementation details, prompt engineering choices, and supplementary experiments backing the main claims>

## Key points

- <5-8 bullets covering the most load-bearing facts across the appendices: the chunk-size/recall trade-off finding (Figure 3), the hierarchical community structure example (Figure 4), context window sizing rationale, and any concrete thresholds/parameters mentioned>

---

## Appendix A: Entity and Claim Extraction — Chunk Size Trade-offs

<summarize the recall-precision trade-off with chunk size and self-reflection iterations. Embed Figure 3:>

![Entity references detected vs. chunk size and self-reflection iterations on HotPotQA](images/03-hotpotqa-figure3.png)

<integrate the figure's trend description in prose>

## Appendix B: Example Community Detection

<summarize the hierarchical Leiden community structure example. Embed Figure 4:>

![Graph communities detected via Leiden algorithm, level 0 vs level 1](images/04-communities-figure4.png)

<integrate the figure's description in prose>

## Appendix C: Context Window Selection

<summarize the reasoning/findings if present in this chunk>

## Appendix D: LLM Assessment Example

<summarize if present in this chunk>

## Appendices E-G: Generation Prompts, Evaluation Prompts, Statistical Analysis

<summarize the purpose and structure of these prompt templates and the statistical methodology used — do not reproduce every full prompt verbatim if very long, but preserve key instructions, output formats, and any exact parameter values or thresholds>

---

**Covers:** Appendices A, B, C, D, E, F, G (as present in this chunk), Figures 3 and 4.
```

## Rules

- Cover the WHOLE chunk, start to end — this is the longest chunk; verify the later appendices (E, F, G) got real coverage and are not truncated because you ran out of output length. If truly enormous, prioritize completeness over verbatim reproduction: summarize each prompt's purpose, key instructions, and output format rather than pasting the whole prompt text.
- No meta-commentary about your own process. No "as an AI" disclaimers. Just the page content.
- Both figures must actually be embedded with the markdown image syntax shown above, not just mentioned by name.
- Preserve concrete numbers/thresholds/parameters exactly as they appear.

## Scope

Touch ONLY the one output file listed above. Do not run any fleet commands other than closing your own bead.

## DoD

1. `/Users/sergii/.kb/papers/ArxivGraphRAGLocalToGlobal/wiki/05-appendix-prompts-and-additional-experiments.md` written per the format contract above, covering the entire chunk.
2. `bd close <own-id> --reason "chunk 05 extracted"`
