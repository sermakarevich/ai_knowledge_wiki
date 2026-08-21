# Extract task: ArxivPathRouter wiki page 04

**Context is tight on this model — read ONLY the input file(s) listed below, nothing else.** Do NOT read this task's own fleet artifacts/log/event files (`~/.fleet/tasks/<id>/...`, `events.jsonl`, `task.json`, `PLAN_AND_STATUS.md`, `KNOWLEDGE.md`), and do NOT read sibling wiki pages "for style/convention reference" — the format contract below is the only convention needed. If this is a retry, do not diagnose the prior failure by reading logs; just re-read the chunk and write directly.

## Input

- `/Users/sergii/.kb/papers/ArxivPathRouter/source/chunks/04.txt` — plain text covering: Section 4.1 Experimental Setup, 4.2 Main Results (with Table 1), 4.3 Ablation Study (with Table 2), 4.4 Routing and Trajectory Quality, 4.5 Teacher Scale Analyze (with Tables 3-4), 4.6 Cross-Dataset Transfer, of the paper "PathRouter: Aligning Rewards with Retrieval Quality in Agentic Graph Retrieval-Augmented Generation" (arXiv 2606.16409). Tables are rendered as plain text in the chunk — reproduce their key numbers as markdown tables.
- Figure descriptions (read these too):
  - `/Users/sergii/.kb/papers/ArxivPathRouter/wiki/images/04-fig3-route-distribution-description.md` — Figure 3, trajectory-category distribution bar charts across six datasets. Embed as `![Figure 3: Route category distribution](images/04-fig3-route-distribution.png)`.
  - `/Users/sergii/.kb/papers/ArxivPathRouter/wiki/images/04-fig4-cross-dataset-ood-description.md` — Figure 4, cross-dataset OOD generalization heatmap. Embed as `![Figure 4: Cross-dataset generalization](images/04-fig4-cross-dataset-ood.png)`.

## Output

Write the full wiki page to: `/Users/sergii/.kb/papers/ArxivPathRouter/wiki/04-experiments-and-main-results.md`

**If this file already exists (a retry), overwrite it completely.**

## Page format (follow exactly)

```markdown
> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Experiments and Main Results

**In one sentence:** <the whole experimental story in one sentence — PathRouter's gains over baselines across benchmarks/model sizes and what the ablations/analyses show>

## Key points

- <5-8 bullets with real content: which benchmarks/model sizes were used, headline F1/G-E gains vs. the strongest baseline (with actual numbers), what the ablation study isolates as most important, what the routing/trajectory-quality analysis shows, what the teacher-scale analysis reveals about capacity, and the cross-dataset transfer result (95.7% average ratio).>

---

## Experimental setup

<full detail: benchmarks (six QA datasets), model sizes/backbones, baselines compared against, metrics used>

## Main results

<full detail from Table 1: reproduce the key comparison as a markdown table (at least PathRouter vs. the strongest baseline per model size, F1/G-E/EM numbers), and the prose analysis of the gains (e.g., F1 gains of 3.1 on 3B and 4.9 on 7B)>

## Ablation study

<full detail from Table 2: what each ablated component does and its effect (path reward, exploration bonus, lazy penalty, timeout/redundancy penalties, teacher KL, selective KL, KL warmup, route scaling, 1D vs 2D routing)>

## Routing and trajectory quality

<full detail on Section 4.4, with the figure>

![Figure 3: Route category distribution](images/04-fig3-route-distribution.png)

## Teacher scale analysis

<full detail on Section 4.5: online vs. frozen teacher, same-size vs. cross-size teacher, the finding that student capacity (not teacher quality) is the bottleneck at small scale>

## Cross-dataset transfer

<full detail on Section 4.6, with the figure>

![Figure 4: Cross-dataset generalization](images/04-fig4-cross-dataset-ood.png)

**Covers:** Section 4.1-4.6 (Experimental Setup through Cross-Dataset Transfer)
```

## Rules

- Reproduce exact numbers from the tables — do not round or approximate beyond what's in the source.
- The page must be self-contained.
- No line limit — be thorough; this is the most content-dense chunk.
- Do not invent content not present in the chunk or figure descriptions.

## Done

1. Write the output file.
2. `bd close <own-id> --reason "chunk 04 extracted"`

## Scope

Touch ONLY `/Users/sergii/.kb/papers/ArxivPathRouter/wiki/04-experiments-and-main-results.md`. Do not run any fleet commands other than `bd close`. No git commands.
