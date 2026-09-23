# Extract wiki page 04 — Autonomous Research and Programmatic Systems

## Context is tight on this model

Read ONLY the input files listed below. Nothing else. Do NOT read this task's own fleet
artifacts/log/event files (`~/.fleet/tasks/<id>/...`, `events.jsonl`, `task.json`,
`PLAN_AND_STATUS.md`, `KNOWLEDGE.md`), and do NOT read sibling wiki pages "for style
reference" — the format contract below is the only convention you need. If this is a retry,
do not try to diagnose the previous failure by reading logs; just re-read the inputs and write
directly.

## Input

- `/Users/sergii/.ai/knowledge/research/PrimeAgentSelfImprovingHarness/source/chunks/04.txt`
  (Subsections 3.3 "Multi-day autonomous research" (nanoGPT speedrun) and 3.4 "Programmatic
  systems construction" (emulators, GPU kernels / PMPP-Hard) from the paper "Prime Agent: A
  Self-Improving RLM Harness", arXiv:2608.23552.)
- Figure descriptions (vision-model text):
  - `/Users/sergii/.ai/knowledge/research/PrimeAgentSelfImprovingHarness/wiki/images/fig6-out-of-loop-experimentation-description.md`
  - `/Users/sergii/.ai/knowledge/research/PrimeAgentSelfImprovingHarness/wiki/images/fig7-8-emulatorbench-pmpp-description.md`
    (this single image page contains BOTH Figure 7 "Selected EmulatorBench runs" and Figure 8
    "PMPP-Hard solve rates" — describe both when captioning)

## Output

Write the full page to:
`/Users/sergii/.ai/knowledge/research/PrimeAgentSelfImprovingHarness/wiki/04-autonomous-research-and-programmatic-systems.md`

**If this file already exists (a retry), overwrite it completely** — do not append or merge.

## Page format contract (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Autonomous Research and Programmatic Systems

**In one sentence:** <the chapter's whole argument, in one sentence>

## Key points

- <complete claim 1 — a real fact/mechanism/number, not "discusses X">
- <complete claim 2>
- ... (5-8 bullets total, each a standalone claim)

---

## Multi-day autonomous research (3.3, nanoGPT speedrun)

...
![Out-of-loop experimentation across harnesses](images/fig6-out-of-loop-experimentation.png)
<one-sentence caption grounded in the figure description file>

## Programmatic systems construction (3.4)

### Emulators

...
![Selected EmulatorBench runs and PMPP-Hard solve rates](images/fig7-8-emulatorbench-pmpp.png)
<one-sentence caption covering BOTH the EmulatorBench and PMPP-Hard results shown in this image>

### GPU kernels (PMPP-Hard)

...

**Covers:** Section 3.3, 3.4, Figures 6, 7, 8
```

Rules:
- Figure 6 MUST be embedded with `![...](images/fig6-out-of-loop-experimentation.png)` in the
  3.3 subsection. Figure 7/8 MUST be embedded with
  `![...](images/fig7-8-emulatorbench-pmpp.png)` in the 3.4 subsection — this is mandatory.
  Use the `-description.md` files' content to write accurate captions; do not guess.
- The `## Key points` bullets must each be a complete, standalone claim with real content
  (numbers, mechanisms, conclusions) — never a vague topic label.
- Use Obsidian `[[wikilink]]` syntax exactly as shown in the backlink line.
- No line limit — be thorough; cover both 3.3 and 3.4 fully, including the GPU-kernels
  paragraphs near the end of the input file — do not stop after the emulators content.
- Do not invent facts not present in the input files.

## Done condition

Output file written to the exact path above. Then `bd close <own-id> --reason "chunk 04 extracted"`.

## Scope

Touch ONLY the one output file listed above. Do not run any fleet/git commands other than
`bd close`. No git commands — `.ai` auto-syncs on its own.
