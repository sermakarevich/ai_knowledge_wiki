# Task: Extract wiki pages for SodaMem paper (single chunk, whole paper)

**Context is tight on this model — read ONLY the files listed below, nothing else.**
Do NOT read this task's own fleet artifacts/log/event files (`~/.fleet/tasks/<id>/...`,
`events.jsonl`, `task.json`, `PLAN_AND_STATUS.md`, `KNOWLEDGE.md`), and do NOT read sibling
wiki pages "for style/convention reference" — the format contract below is the only
convention you need. If this is a retry, do NOT diagnose the prior failure by reading logs —
just re-read the chunk and write directly.

## Input (read these, and only these)

- `/Users/sergii/.kb/papers/ArxivSodaMem/source/chunks/01.txt` — the full paper text (9 pages, ~5k words). This is the whole source; it covers everything.
- `/Users/sergii/.kb/papers/ArxivSodaMem/wiki/images/01-description.md` — vision-model description of Figure 1 (system overview diagram, appears after the Introduction, near "We instantiate the stance with SodaMem").
- `/Users/sergii/.kb/papers/ArxivSodaMem/wiki/images/02-description.md` — vision-model description of Figure 2 (cost–accuracy scatter plot, appears in the Experiments/Result Analysis section).

## Output — write ALL THREE files (absolute paths)

1. `/Users/sergii/.kb/papers/ArxivSodaMem/wiki/01-motivation-and-related-work.md`
   — Covers: Abstract, Introduction, Related Work (Benchmarks; External memory and structure;
   Indexing/conflict/controllers), Motivation (currency & multi-signal recall), and the four
   failure modes P1–P4 (Currency/conflict, Temporal structure, Provenance, Association).
2. `/Users/sergii/.kb/papers/ArxivSodaMem/wiki/02-method-sodamem.md`
   — Covers: Preliminaries (Definitions 0.1–0.4: FactEvent, Evidence-grounded answer,
   Supersession, Query temporal intent), Problem Statement, and the full SodaMem method:
   Ingest (Algorithm 1: IngestSession, provenance hard constraint, timeline resolution layer),
   Store (hybrid index, typed edges SUPERSEDES/CONTRADICTS/UPDATES/DERIVED_FROM),
   Retrieve (Algorithm 2: MultiTunnelRetrieve, three tunnels, connection-density fusion,
   validity gate), Answer (Algorithm 3: planner–reader loop), and Implementation Notes.
   Embed Figure 1 here: `![SodaMem architecture overview](images/fig1-overview.png)` placed
   right after you introduce the ingest→store→answer pipeline, using the vision description
   from `01-description.md` to write the surrounding text accurately.
3. `/Users/sergii/.kb/papers/ArxivSodaMem/wiki/03-evaluation-and-results.md`
   — Covers: Experiments (Setup and Cost Protocol, the SodaMem run: 92.8% accuracy /
   464/500 / mean $0.00161 per question / ≈18.3k tokens), Table 1 (reproduce it as a markdown
   table — method, cite, date, model, accuracy, cost/10^3 Q), Result Analysis ("Where SodaMem
   sits", dominated quadrant), Limitations, and Conclusion. Embed Figure 2 here:
   `![Cost vs accuracy on LongMemEval-S](images/fig2-cost-accuracy.png)` right after you
   introduce the cost–accuracy comparison, using the vision description from
   `02-description.md` to write the surrounding text accurately.

**If any of these three files already exists (a retry), overwrite it completely.**

## Wiki page format (apply to EACH of the three files)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# <Topic Title>

**In one sentence:** <the section's whole argument, one sentence>

## Key points

- <5-8 bullets, each a complete standalone claim with real content — numbers,
  mechanisms, named terms, conclusions. Not "discusses X".>

---

## <Subsection headers mirroring the paper's own structure>

<Full detail: exact numbers, definitions, algorithm steps, tables, and named
concepts verbatim from the source. Cite specific values (percentages, dollar
costs, token counts) exactly as given in the text — do not round or invent.>

**Covers:** <one line: which paper sections this page covers>
```

No line limit — be thorough, this is the deep rung of the wiki. Every named figure
(Figure 1, Figure 2) MUST actually be embedded via `![...](images/<file>.png)` in the
page that covers it — do not reference a figure without embedding it.

## Scope

Touch ONLY the three output files listed above. Do not run any fleet commands other than
the final `bd close`. No git commands — this KB repo auto-syncs.

## Done

After all three files are written:
```
bd close <own-bead-id> --reason "chunk 01 extracted: 3 wiki pages written"
```
