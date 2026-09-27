> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# Critical Analysis: The Tasteful Agent: Measuring and Improving Taste in Long-Horizon Tasks

## Claims vs. evidence
- Claim: "taste" (good long-horizon direction choice) is measurable from trajectories via hindsight labels. Evidence is strong on construct: forks share an equivalent prefix, differ in judgment, and are labeled by later recorded outcome; human review supports 170/172 mined labels (98.8%, κ = 0.973).
- Claim: frontier models have poor taste (best 59.7% Average, binary choice). Evidence is solid within the benchmark's scoring rule, but the both-orders-correct rule is harsh (random = 25%, always-one-side = 0%), so headline numbers understate single-presentation competence (e.g. student mean-over-orders 62.4% vs 47.9% strict).
- Subset splits add texture: e.g. Claude Opus 5 scores 64.3% research but 46.7% engineering, while GPT-5.6 Sol is more balanced (62.5% / 56.9%) — taste is partly domain- and agent-distribution-specific, not a single scalar.
- Detour forks are harder than parallel forks in both domains, and that gap exceeds the cross-domain gap — self-correction traces carry a different, harder judgment signal than cross-attempt comparisons.
- Filtering yield signals selectivity: 4,657 mined candidates → 1,809 pass the rubric → 729 survive the trivial filter → 502 released (10.8%). The benchmark is the legible tail of a much noisier mining process.
- Distillation detail matters for interpreting the gain: LoRA rank-16 updates (79.7M params, ~2h per fold on one A100) on teacher traces kept at 328/390 and 311/390 per view, with student-both-correct rising 117 → 187 of 390 (+104 gained, −34 lost) — a genuine but uneven improvement, not a uniform uplift.
- Claim: errors concentrate where deciding evidence appears late (62.3% in-prefix → 21.0% more-work) and reasoning budget does not help (null budget×horizon interaction, p ≈ 0.8). Evidence is the paper's strongest: consistent across models, with models spending the most tokens where they score worst.
- Claim: taste distills and transfers end to end (student 47.9% vs 30.0% base held-out; executor 14.6% → 33.7% with student advice on 41 held-out tasks). Evidence is real but small-N: 390 training questions, 41 end-to-end tasks, 98 forks; correct-advice upper bound is 39.0% (McNemar p ≤ 0.004), so the transfer is meaningful yet noisy.
- Claim: Taste-Bench is not end-to-end ability restated (r = +0.63 vs SWE-bench Verified, wider top-end spread). Evidence is moderate: correlation is still substantial (R² = 0.39), and the engineering subset correlation drops to r = +0.37, which cuts both ways — distinct signal, but partly a different task mix.

## Genuinely new vs. repackaged
- Genuinely new: outcome-labeled decision forks mined automatically from existing trajectories (parallel opposite-outcome pairs + in-run detours), evaluated blind with the future hidden — a judgment benchmark without human annotation.
- Genuinely new: the horizon-distance analysis (in-prefix / inferable / next-step / more-work) showing a steep, budget-immune decay — a crisp empirical signature of "taste" failures.
- Repackaged: the distillation recipe is SDPO-style forward-KL over teacher reasoning plus calibration, with an advisor-steers-executor end-to-end test — competent reuse, not a new training paradigm.
- Repackaged framing: much of "taste" overlaps process supervision, process reward models, whole-trajectory judges, and pre-outcome idea judgment; the novelty is the outcome-labeled blind-fork protocol, not the idea that intermediate decisions matter.
- Clever but borrowed machinery: 65k-token prefix rendering with head/tail truncation, dual-presentation position-bias control, and item-bootstrap intervals are solid evaluation craft assembled from standard practice.
- The "taste is trainable" headline echoes advisor-steering and expert-iteration literature; the twist worth keeping is that supervision comes from mined hindsight rather than fresh human labels or environment rollouts.

## Weaknesses and blind spots
- Label validity: realized branch outcome conflates judgment quality with execution luck and environment noise; the equivalent-prefix design mitigates this but cannot eliminate it, especially in research tasks with stochastic scores.
- Selection bias from the unanimity filter: a question ships only when all four judges agree given the full record, so the benchmark selects for judge-legible forks — yet judge agreement on released parallel-engineering items is only 51.7%, suggesting the filter keeps what judges can rationalize, not necessarily what is most taste-relevant.
- Narrow trajectory pools: engineering forks come only from GPT-5.4/5.5 agents on SWE-bench Pro; research forks from a handful of Claude/DeepSeek agents — fork distribution reflects those agents' failure modes, not agents in general.
- Forced binary choice with hidden futures is artificial: real taste involves generating directions, gathering information, and hedging — none of which is tested; "more-work" forks may penalize rational under-determination rather than bad judgment.
- Distillation caveat: the teacher sees the supported candidate, so student gains partly reflect learning to rationalize a known answer; the student also loses 34 questions the base got right, and training-fold accuracy (92.9%) hints at memorization headroom.
- End-to-end test is scaffolded: one advice injection per fork into a fixed weak executor (Qwen3.6-27B) on 41 tasks — encouraging, but far from showing that taste-training improves a frontier agent in the wild.
- Generator dependence: a single generator (GPT-5.6 Sol at high effort) proposes all forks, so mining blind spots of that model become benchmark blind spots; excluding it from the judge panel helps but does not remove the proposal bias.
- Truncation and rendering choices (first-25-lines-plus-tail, 700-char output clipping) may drop exactly the early constraint or middle evidence a fork turns on; only two models ever hit the token cap, but silent information loss is unmeasured.
- No cost or calibration analysis: advice-sum log-odds decisions (287/390 student vs 207/390 base) outperform strict accuracy, yet the paper does not report calibration, abstention, or compute cost of the advisor at deployment scale.
- Only one reasoning-budget finding partially cuts the other way: Luna on the research subset improves with budget (43.8% → 54.5%) while everything else is flat — a lone exception worth re-testing rather than a crack in the overall null result.

## Applicability
- The fork-mining method is directly reusable: any team with stored agent trajectories can mine its own taste questions (parallel retries + detour self-corrections) and get a judgment eval for free.
- The horizon annotation is a useful triage lens: if your agent fails mostly at "more-work" forks, buy information-gathering and experiment design, not bigger reasoning budgets.
- The distill-then-advise pattern (small judgment model steering a larger executor) is a cheap production shape worth copying before full policy retraining.
- Rejected-but-instructive: the removed sparse-attack fork (ensemble favored in-prefix at 80% vs 43%, label resting on an unstated time budget) is a good template for an "undecidable" review queue in your own mining pipeline.
- Metric hygiene to copy: dual-presentation scoring plus mean-over-orders reporting, with unparseable counted wrong and bootstrap intervals — adopt this shape for any internal A/B judgment eval.
- **Relevance to my work**
  - AI/ML engineering: mine failed-vs-passing SWE/ML experiment trajectories for fork evals; gate "which hypothesis next" decisions with a small judge model trained on hindsight rationales.
  - Agentic systems: add blind-fork accuracy alongside task success in agent evals; track in-prefix vs more-work splits to decide between prompt, tool, and search-budget interventions.
  - Elisity data platform: apply the detour-mining template to pipeline-agent runs (abandoned query plan → error wall → recovery) to build a data-engineering taste set; use a distilled advisor to steer expensive executor runs and cut wasted compute.

## What this changes
- Shifts part of agent evaluation from "did it finish?" to "did it choose well before the outcome was visible?" — with a concrete, automatable protocol for doing so.
- Weakens the "just add reasoning budget" reflex: on far-horizon judgment, more thinking tokens did not help across two model families and six settings.
  - Practical corollary: when stuck on hard forks, spend the budget on executing discriminating experiments, not on longer deliberation over the same prefix.
- Makes trajectory logs a training asset twice over: first for outcome supervision, second for hindsight-labeled judgment distillation that transfers to unseen tasks and lifts end-to-end success (+19.1 pp in their setup).
  - The transfer used task-disjoint folds and a frozen same-size teacher/student, so the gain is judgment transfer rather than task memorization — a result worth taking seriously despite the small N.
- Sets a bar for future claims: any "better long-horizon agent" should show fork-level judgment gains, not only end-to-end scores that hide lucky recoveries.
  - Concretely: report strict both-orders accuracy alongside mean-over-orders, split by horizon distance, before claiming a taste improvement.

## Verdict
- Useful, well-instrumented, but narrow: the core phenomenon (late-evidence forks resist reasoning scale yet yield to hindsight distillation) is convincing; the generality beyond the authors' trajectory pools and the 41-task transfer is not yet established.
- Next step for a practitioner is replication on own logs, not adoption of their 502 items as a universal taste metric.
  - Mine parallel retries and detour recoveries from your own agent runs, apply the trivial-plus-unanimity filter shape, and check whether your horizon-decay curve matches theirs before investing in distillation.
  - Time-box it: one engineer, one week, one trajectory pool — if no horizon-decay signal appears, park this and move on.
- **trial**
