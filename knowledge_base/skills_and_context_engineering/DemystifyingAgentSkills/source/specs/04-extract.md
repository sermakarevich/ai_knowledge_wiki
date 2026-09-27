# Task: Write one LLM-wiki page from a paper chunk (chunk 04 of 5)

You are extracting ONE wiki page for a knowledge-base entry on the paper
"Demystifying Agent Skills: Why They Work-Until They Don't" (arXiv 2608.14036).

**Context is tight on this model — read ONLY the files listed below, nothing else.**
Do NOT read this task's own fleet artifacts/log/event files
(`~/.fleet/tasks/<id>/...`, `events.jsonl`, `task.json`, `PLAN_AND_STATUS.md`, `KNOWLEDGE.md`),
and do NOT read sibling wiki pages "for style/convention reference" — the format contract
below is the only convention needed. On a retry, do not diagnose the prior failure by reading
logs; just re-read the inputs and write directly.

## Input

Read these files in full:

1. `/Users/sergii/.ai/knowledge/research/DemystifyingAgentSkills/source/chunks/04.txt` — the paper's
   Section 5 "Findings", Section 6 "Conclusion", and Section 7 "Limitations" — extracted from
   the PDF as markdown-ish text with some OCR-style ligature artifacts — read past minor glyph
   noise.
2. `/Users/sergii/.ai/knowledge/research/DemystifyingAgentSkills/wiki/images/03-fig3fig4-results-page8-description.md`
3. `/Users/sergii/.ai/knowledge/research/DemystifyingAgentSkills/wiki/images/04-fig3b-page9-description.md`
4. `/Users/sergii/.ai/knowledge/research/DemystifyingAgentSkills/wiki/images/05-fig5-page10-description.md`

   These three description files cover Figures 3, 4, and 5 (results/ablation plots), which
   belong to this section. Use them to write about the figures without seeing the images.

## Output

Write the page to this exact absolute path:

`/Users/sergii/.ai/knowledge/research/DemystifyingAgentSkills/wiki/04-findings.md`

**If this file already exists (a retry), overwrite it completely.**

## Page format (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Findings, Conclusion, and Limitations

**In one sentence:** <the chunk's whole argument, in one sentence>

## Key points

- <complete claim 1 — a real fact/mechanism/number, not a topic label>
- <complete claim 2>
- ... (6-8 bullets total; this is the paper's results section, so weight this block toward
  the paper's headline numbers: e.g. the 6.06-point improvement over Workflow Memory, the
  65.7% vs 4.5% procedural-anchoring split, the 29.6%->3.3% retrieval precision collapse from
  pool size 5 to 100, and any other exact figures the chunk states)

---

## <subsection per Findings 5.1-5.5, one subsection each, using the chunk's own subsection
titles or close paraphrases>

<full detail per finding, with exact numbers, comparison baselines, and what each finding
means for when/why/where skills work or fail>

## Figures: Results

![Results and ablation figures](images/03-fig3fig4-results-page8.png)

<description drawn from the description file, placed near the finding(s) it supports>

![Additional results figure](images/04-fig3b-page9.png)

<description>

![Additional results figure](images/05-fig5-page10.png)

<description>

## Conclusion

<full detail from Section 6>

## Limitations

<full detail from Section 7 — the paper's own acknowledged limitations, verbatim in substance>

**Covers:** Sections 5 (Findings), 6 (Conclusion), 7 (Limitations) of arXiv 2608.14036,
including Figures 3, 4, 5
```

Write in full prose paragraphs for the detail sections (not just more bullets). This is the
paper's results section — precision matters: preserve every exact number, percentage, and
comparison the chunk states rather than rounding or paraphrasing them away. No line limit — be
thorough; do not compress the whole chunk into the Key points block alone.

## Definition of done

- Output file written at the exact path above, non-trivial (well over 40 lines), covering the
  chunk's ENTIRE content (not just its opening paragraphs, and not skipping Conclusion or
  Limitations), and embedding all three figures exactly as shown above.
- No git commands — do not run git anything. `.ai` auto-syncs on its own.
- Touch ONLY the one output file. Do not run any fleet commands other than closing your own bead.
- When done: `bd close <own-id> --reason "chunk 04 extracted"`
