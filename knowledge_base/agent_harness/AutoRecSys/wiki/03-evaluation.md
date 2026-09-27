> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Evaluation, related work, outlook

**In one sentence:** AutoRecSys cuts hands-on researcher effort per idea from hours/days to minutes and lets parallel portfolios run, while its natural-language playbook drives operational fixes from 4.0 to 0.5 per iteration across 31 iterations and recovers past a baseline shift — positioning it as a persistent, recoverable harness for industry-scale recommendation research rather than rapid small-task iteration.

## Key points

- The operative metric is human bandwidth per idea (hands-on attention from proposal to analyzed result), not wall-clock cycle time, which stays dominated by days-long training plus queueing outside the system's control.
- Two modes trade control for effort: human-in-the-loop keeps idea-selection and implementation-review checkpoints and delegates the rest (minutes of effort); fully autonomous skips checkpoints (minimum effort, only idea selection plus escalations) but risks spending training on weaker ideas, so it is favored once the playbook is mature and ideas are low-risk.
- Across 31 unique iterations on one representative model spanning a baseline shift at iteration 21, major (operational) fixes fell from 4.0 per iteration to 1.3 during stabilization (iterations 5–20), spiked during transition (21–25), then recovered to 0.5 per iteration with 5 of 6 post-transition iterations (26–31) needing zero fixes.
- Errors are categorical, not random: each category (GPU instability, resource tags, build-date conventions, input naming, package-layer mismatches, publish failures) appears in one or two phases, is recorded as a dead end, then disappears; the only post-transition error was a novel graph-compilation type-inference bug no prior experience could prevent.
- The playbook works through natural language (19-entry dead-ends table with "DO NOT" directives, proven-strategies table, pipeline recipes: 6 key files to read, toy-train validation, build-based submission with 9 pinned parameters, metrics-fetch plus baseline-comparison analysis) built from 49 dead ends and 17 error-fix patterns; the agent rarely uses numerical metadata.
- Robustness comes from persistent state: cross-server resume via draft diffs plus trajectory logs, a 970-log-entry / 110-tool-call fully autonomous session (fused-kernel import diagnosis, package-layer rebuild, resubmission), and adaptive workflow edits such as skipping a repeatedly failing publish step.
- Positioning and outlook: unlike AI Scientist, AutoResearch, FARS, and EvoScientist (bounded tasks, fast feedback), AutoRecSys targets days-long industry-scale training with evolving baselines via parallel exploration and recoverable state; future work is proxy models for screening, cross-model transfer, validation-gated playbook updates, adaptive confidence-based human review, and team-scale operation.

---

## 7.1 Human bandwidth per idea

- End-to-end cycle time is the wrong metric: training still takes days however it is launched, and queueing/baseline availability are outside system control.
- Manual baseline: one idea of comparable complexity costs hours to days of active human involvement across implementation, validation, submission, monitoring, failure recovery, and analysis.
- Human-in-the-loop mode: researcher keeps two checkpoints (idea selection, implementation review); system handles validation, submission, monitoring, failure recovery, analysis. Same-complexity idea drops to minutes of hands-on effort.
- Fully autonomous mode: checkpoints skipped; human only selects ideas and answers escalations the system cannot resolve. Minimizes time but risks pursuing weaker ideas and wasting training; preferred only with a mature playbook and low-risk candidates.
- Payoff is throughput per unit of attention: attention that once covered a single idea now covers more than a dozen, and parallel execution makes the distributed portfolio practical.

## 7.2 Playbook evolution and execution reliability

### Setup and metrics

- 31 unique experiment iterations on one representative model, chosen because it underwent a baseline shift mid-evaluation — a natural experiment in learning then re-adapting.
- Metrics from session trajectory logs:

| Metric | Definition |
| --- | --- |
| Session log step | One timestamped agent action per iteration (implementation decision, observation, submission, recovery, analysis result) |
| Major fix step | A log step spent recovering from an operational failure (failed/resubmitted job, wrong hardware or entitlement, package-layer version mismatch, metadata correction, baseline refresh); excludes code-implementation reasoning/debugging, counted as productive work |
| Zero-fix rate | Fraction of iterations completing with zero major fix steps (end-to-end operational reliability) |
| Error category | Failures sharing a root cause (e.g. "GPU hardware instability", "build date parameter conventions"); playbook stores individual dead ends, analysis groups them |

### Evolution trajectory (Figure 6: per-iteration fixes + 5-iteration rolling average; phase summary)

- Baseline transition at iteration 21: from a standard architecture to a combined configuration (graph-mode compilation + new embedding module + task adapters), requiring different hardware, entitlements, package-layer versions, and upstream revisions.
- Stabilization (iterations 5–20): playbook absorbs hardware choices, submission parameters, build conventions, input-naming rules; major fixes drop from 4.0 to 1.3 per iteration.
- Transition (iterations 21–25): five consecutive iterations need operational recovery — wrong hardware/entitlements for the new config, adapter injection failures, package-layer mismatches, upstream revision conflicts.
- Post-transition (iterations 26–31): 0.5 major fixes per iteration; 5 of 6 iterations need no operational fix, beating pre-transition stabilized performance.
- Pattern: learn, regress, recover centered on the transition.

### Error category analysis

- Errors are categorical: GPU hardware instability, missing resource tags, incorrect build-date parameters, input-naming conventions, package-layer mismatches each appear in one or two phases, get recorded as dead ends, then vanish where the playbook absorbed the fix.
- Transition introduces two new categories (package-layer mismatches, publish infrastructure failures), both absent post-transition.
- Sole post-transition error is genuinely novel: a type-inference failure in graph compilation no prior experience could have prevented.

### How the playbook influences behavior

- All 31 session transcripts show influence primarily via natural language: agent reads playbook markdown at session start and follows it.
- Dead-ends table (19 entries with explicit "DO NOT" directives) prevents known errors; proven-strategies table guides implementation; pipeline recipes specify exact tool sequences.
- Agent seldom queries numerical metadata/scores — it prefers actionable prose (e.g. "the runtime batch object exposes a feature under an internal field name that differs from its raw data-warehouse column name") over a confidence score needing interpretation.
- Crystallized per-stage pipeline: read calls on 6 key files (implementation), toy-train command (validation), build-based submission with 9 pinned parameters (training), metrics-fetching call followed by baseline-comparison call (analysis) — evolved from 49 dead ends and 17 error-fix patterns.

### Five self-evolution mechanisms (46 sessions, 10+ dev servers)

- Dead-end avoidance: three failed jobs taught that one GPU generation caused recurring hardware failures; recorded as dead end, stable generation selected automatically thereafter; later iteration loaded the lesson that flash attention was broken on that hardware and applied a manual fallback.
- Pipeline config crystallization: submission config accumulated hard-won parameters — hardware type, package-layer version, resource entitlements, scheduling tags, resource-partition flags, ownership metadata, build target, model type — each from a specific failure, then reused every iteration.
- Validation-skip pattern: on a GPU-less dev server, playbook guides skipping local toy-train validation straight to remote submission, avoiding a doomed validation and human intervention.
- Self-diagnosed infrastructure improvement: monitor agents died silently after ~3–5 hours because each polling cycle appended tool results until the LLM context window overflowed; system designed a cron-based replacement (each tick a fresh prompt, no accumulation), implemented it, and submitted the orchestrator upgrade.
- Emergent meta-pattern recognition: after the sixth consecutive pre-transition positive failed on the new baseline, the agent synthesized unprompted that the new baseline already captured those features' signals (redundant, even harmful); recorded as a learning, drove pivot to baseline-native experiments.
- Common effect: steadily less redundant exploration and recovery; agent compute is already modest (minutes of reasoning vs. days of training), but trimming waste lowers token cost and frees researcher attention.

## 7.3 Robustness in practice

- Cross-server context recovery: an agent finishes implementing an idea, then crashes when its dev-server lease expires before validation/submission. A different-server agent resumes: detects the missing commit in local history, reads the trajectory log, fetches the prior session's draft diff from shared state via `get_diff_num(idea)`, applies it, validates, submits, and finalizes — no human guidance. Publishing every change as a draft diff (never only a local checkout) makes handoff seamless and avoids regenerating work.
- Autonomous execution depth: most autonomous session ran 970 consecutive log entries (110 tool calls) with zero human intervention — diagnosing failed jobs, tracing root cause to a fused-kernel import in a shared operator library, rebuilding package layers, resubmitting.
- Adaptive workflow modification: after a feature-gating experiment failed four times at publish (ahead-of-time compilation failure in a shared ranking module), the system switched to a training flow skipping the failing publish step; next attempt ran clean first try. The system edits workflows, not just parameters.

## 8 Related work

- Autonomous research systems: AI Scientist (Lu et al., 2024) on end-to-end discovery; AutoResearch (Karpathy, 2025) on rapid serial small-scale experiments; FARS (Analemma AI, 2025) on research artifacts for self-contained academic tasks; EvoScientist (Lyu et al., 2026) and Dr. Claw on literature-to-paper workflows. All assume bounded experiments with fast feedback. AutoRecSys differs: hours-to-days industry-scale training, complex infrastructure, continuously evolving baselines — hence parallel exploration, persistent state, cross-session/server recovery.
- Agent harnesses and orchestration: ReAct (Yao et al., 2023) interleaves reasoning and acting; SWE-agent (Yang et al., 2024) shows the agent–computer interface matters; DSPy (Khattab et al., 2023) composes/optimizes LM pipelines; Ning et al. (2026) define code-as-harness (executability, verifiability, statefulness) and flag harness evolution as open; Meta-Harness (Lee et al., 2026) optimizes harness configs from traces; ADAS (Hu et al., 2024) meta-searches agent designs. AutoRecSys extends this from inference-time tasks to the full long-running experiment lifecycle — scheduling parallel runs, preserving state across failures, accumulating reusable execution knowledge — and unlike run-tracking platforms, it executes, recovers, and steers next actions.
- Procedural memory, skills, self-improvement: Reflexion (Shinn et al., 2023) verbal episodic feedback; Voyager (Wang et al., 2023) growing skill library; MemGPT (Packer et al., 2023) tiered memory; AWM (Wang et al., 2024) reusable workflows from trajectories (closest to AutoRecSys pipeline recipes); Evo-Memory (Wei et al., 2025) test-time memory evolution; skills-as-artifacts (Li et al., 2026; Jiang et al., 2026); Trace2Skill (Ni et al., 2026), EvoSkill (Alzubi et al., 2026), SkillOpt (Yang et al., 2026) with validation/rejected-edit gates; GEPA (Agrawal et al., 2025) reflective instruction evolution. AutoRecSys couples two memories at system scale — playbooks improve how experiments run, research history improves what is tried next — on persistent multi-server orchestration over multi-day industry-scale runs, beyond single-episode or benchmark streams.

## 9 Discussion and future work

- Proxy models for screening: smaller-scale replicas for rapid idea screening; if small-scale transfers reliably to full-scale, screen dozens of ideas fast and full-train only the best — approaching AutoResearch-style serial speed while keeping industry-scale rigor for finalists.
- Cross-model knowledge transfer: today each model has independent playbooks/histories; transferable insights (e.g. gating helps multi-task models; embedding-dim sweeps diminish above 128) could warm-start new models and cut playbook cold-start.
- Validation-gated playbook updates: unlike SkillOpt, no formal gate — updates accepted on agent judgment. No regressions observed (dead ends record actual failures, hence correct by construction), but a lightweight check (e.g. new dead end must not conflict with proven strategies) would harden growing playbooks.
- Adaptive human-in-the-loop: replace the binary interactive/autonomous toggle with confidence-gated review — high-confidence, low-cost decisions go autonomous; novel or high-impact ones (first run on a new model, high regression risk) trigger human review.
- Team scale: current design serves one researcher over a model portfolio; multi-researcher use needs shared backlogs, collaborative history, and multi-user conflict resolution, with per-model isolation as the starting point.

## 10 Conclusion

- AutoRecSys is an autonomous research harness for industry-scale recommendation innovation: a centralized memory substrate supports distributed execution, persistent state, cross-server recovery, and knowledge reuse.
- Dual evolution improves execution (Execution Evolution Loop → model-specific natural-language playbooks) and research direction (Idea Evolution Loop → parallel exploration steered by outcomes).
- Evaluation: far less human effort per cycle; major fixes fall 4.0 → 0.5 per iteration over 31 iterations with fast adaptation to a new baseline architecture — showing autonomous research extends beyond small fast tasks to complex industry-scale systems given a robust, persistent, evolving harness.

**Covers:** sections 7-10
