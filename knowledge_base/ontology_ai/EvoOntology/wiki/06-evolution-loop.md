> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# The single-level difference isolates the attributed
**In one sentence:** The chunk defines a reciprocal paired score with validation-gated deployment and reports that EvoOntology improves Trajectory-Wise, Insight/Summary, and EX/VES across backbones while static semantic-layer prompts and episodic memory do not match it.
## Key points
- Reciprocal score is defined as `Score = (ScoreA→B + ScoreB→A) / 2`, following two-fold split-and-swap evaluation (Dietterich 1998; Wang et al. 2026).
- Rejected candidates are not deployed; their signatures, interventions, and evaluation outcomes are logged to avoid repeated ineffective updates, while limiting regressions on the validation set.
- All backbones evolve independently from the same initial state L0, so accepted updates reflect backbone-specific interaction patterns.
- On DDR-Bench 10-K, EvoOntology improves Trajectory-Wise accuracy on all six backbones with average gain +17.8 points, ranging from +4.8 on Qwen3.5-Flash to +26.7 on GPT-5.5.
- Baseline + SL as a static prompt does not consistently improve and drops −15.0 Trajectory-Wise points on Claude-Sonnet-5, because a static fragment competes with other instructions and cannot be pruned per turn, whereas EvoOntology exposes content through MCP tools queried per step.
- ReAct + Memory lifts DDR-Bench Trajectory-Wise from 69.5 to 75.8 (+6.3) but remains 13.7 points below EvoOntology at 89.5 (+20.0), because episodic memory only replays what has been done and does not expose typed, composable structure.
- On InsightBench EvoOntology improves overall performance on every backbone with mean gain 1.9 points and largest improvement +6.1 on DeepSeek-V4-Flash; on BIRD under Oracle Knowledge it improves EX by 7.4 and VES by 8.6 points on average, while Baseline + SL shows mixed EX (down to −5.6 on GPT-5.5) with VES rising.
- Initial builder-constructed ontology versus evolved ontology: on DDR-Bench mean Trajectory-Wise rises 12.3 points from Baseline to Initial plus a further 7.7 points from Initial to Evolved, separating builder contribution from self-evolution gain.
---
## Validation gating and reciprocal evaluation
**Covers:** score formula through deployment logging and fold discipline

Verbatim:

> "The single-level difference isolates the attributed hypothesis"
> "Score = (ScoreA→B + ScoreB→A) / 2"
> "while limiting regressions on the validation set. Rejected candidates are not deployed, and their signatures, interventions, and evaluation outcomes are logged to avoid repeated ineffective updates."
> "All backbones evolve independently from the same initial state L0, allowing accepted updates to reflect backbone-specific interaction patterns."
> "This reciprocal design follows two-fold split-and-swap evaluation (Dietterich 1998; Wang et al. 2026). All methods use the same fold assignment and deployment configuration."
> "The same adaptation fold is used for ontology construction and updating across all relevant conditions. The held-out fold is accessed only for final evaluation after the ontology has been frozen, and its answers and evaluator feedback are never used for ontology construction, evolution, or candidate selection."

## Benchmarks and experimental setup
**Covers:** Experiments — Benchmarks through Backbones/scaffold

- Deep Data Research (DDR-Bench) (Liu et al. 2026): open-ended data research across heterogeneous sources; 10-K scenario; Message-Wise accuracy on per-turn interpretation, Trajectory-Wise accuracy on full-history synthesis.
- InsightBench (Sahu et al. 2025): business-analytics benchmark of business-intelligence flags, each paired with CSV dataset and ground-truth insight; reports Insight and Summary scores.
- BIRD (Li et al. 2023): text-to-SQL on natural-language questions across real-world databases, official Oracle Knowledge setting; primary metric Execution Accuracy EX, secondary Valid Efficiency Score VES.
- Backbones: GPT-5.5, GPT-5.6-sol, Claude-Sonnet-5, Claude-Opus-4.8, DeepSeek-V4-Flash, Qwen3.5-Flash; all conditions use same ReAct (Yao et al. 2022) scaffold, raw-data tools, decoding configuration, and interaction budget.

## Main results: DDR-Bench
**Covers:** Main Results — Capability on Multi-Source Data Research, Table 1 and Table 2

Table 1 DDR-Bench 10-K (%, gain over Baseline in parentheses; selected Trajectory-Wise):

| Backbone | Baseline Traj-Wise | Baseline + SL Traj-Wise | EvoOntology Traj-Wise |
|---|---|---|---|
| GPT-5.5 | 64.2 | 63.9 (−0.3) | 90.9 (+26.7) |
| GPT-5.6-sol | 68.5 | 65.5 (−3.0) | 93.5 (+25.0) |
| Claude-Sonnet-5 | 72.5 | 57.5 (−15.0) | 81.3 (+8.8) |
| Claude-Opus-4.8 | 73.0 | 71.4 (−1.6) | 92.3 (+19.3) |
| DeepSeek-V4-Flash | 30.3 | 31.7 (+1.4) | 52.3 (+22.0) |
| Qwen3.5-Flash | 14.3 | 13.3 (−1.0) | 19.1 (+4.8) |

Table 2 memory baseline on DDR-Bench, averaged across four backbones:

| Method | Traj-Wise (%, ↑) | ∆ |
|---|---|---|
| Baseline (ReAct) | 69.5 | – |
| ReAct + Memory | 75.8 | +6.3 |
| EvoOntology | 89.5 | +20.0 |

Verbatim: `"ReAct + Memory" stores past trajectories as retrievable episodes and injects the top-k into the prompt.` / `memory-based persistence lifts Trajectory-Wise from 69.5 to 75.8 but remains 13.7 points below EvoOntology, because episodic memory only replays what has been done and does not expose typed, composable structure.`

## Main results: InsightBench and BIRD
**Covers:** Capability on Insight Mining (Table 3) through Capability on Data Retrieval (Table 4)

Table 3 InsightBench Overall gain highlights from chunk:

| Backbone | Baseline Overall | EvoOntology Overall gain |
|---|---|---|
| GPT-5.5 | 50.3 | 51.0 (+0.8) |
| GPT-5.6-sol | 50.5 | 52.1 (+1.6) |
| Claude-Sonnet-5 | 52.3 | 53.0 (+0.7) |
| Claude-Opus-4.8 | 52.4 | 53.2 (+0.8) |
| DeepSeek-V4-Flash | 39.8 | 45.9 (+6.1) |
| Qwen3.5-Flash | 31.9 | 33.4 (+1.6) |

Chunk claims:

- `Overall performance on every backbone, with a mean gain of 1.9 points and the largest improvement on DeepSeek-V4-Flash (+6.1).`
- `The gains are smaller than DDR-Bench because Insight is graded on short reference-style findings and saturates once the answer aligns with the reference.`
- `Baseline + SL recovers most of the Insight gain on InsightBench, but drops by −3.3 on Claude-Sonnet-5 Summary, whereas EvoOntology improves both Insight and Summary on all four backbones by exposing the same content through queryable tools instead of a static prompt.`
- BIRD: `EvoOntology improves both EX and VES for every backbone, with average gains of 7.4 and 8.6 points.` / `Baseline + SL shows a mixed pattern: EX drops by up to −5.6 (GPT-5.5) while VES rises across all backbones, indicating that a static semantic layer improves SQL well-formedness but distracts from producing correct queries.`

## Effect of ontology layer: Baseline vs Initial vs Evolved
**Covers:** Effect of Ontology Layer through Figure 3 description

- Three settings: Baseline uses no ontology layer, Initial uses builder-constructed ontology before evolution, Evolved uses final ontology after self-evolution.
- Figure 3 reports per-backbone performance under the three settings; means average primary-metric scores across four backbones per benchmark.
- `The initial ontology establishes a strong improvement over the no-ontology baseline, while self-evolution consistently extends this gain across all three benchmarks.`
- `On DDR-Bench, the mean Trajectory-Wise score increases by 12.3 percentage points from Baseline to Initial, followed by a further improvement of 7.7 percentage points from Initial to Evolved.`
- `On InsightBench, the mean Insight score first` [chunk truncates here].

**Covers:** chunk file `06-the-single-level-difference-isolates-the-attribu.md` lines 1–131, from reciprocal Score formula and validation gating through DDR-Bench / InsightBench / BIRD main results to Baseline / Initial / Evolved comparison; Table 4 body and Figure 3 values beyond the extracted lines are truncated in the chunk and not covered.
