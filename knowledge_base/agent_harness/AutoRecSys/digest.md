> [[index|Wiki]] | [[summary|Summary]]

# AutoRecSys — Digest

The whole source at medium depth: every chapter's headline claim and key points, in order. ~10 min. Descend into a wiki page only where you need the detail.

## 1. [[wiki/01-overview-state-machine|Overview and experiment state machine]]

**In one sentence:** Auto-RecSys extends autonomous research to industry-scale recommenders — where training takes days and infrastructure is fragile — via a harness with distributed asynchronous execution, centralized cross-server memory, and cognitive-procedural separation, plus dual self-evolving loops and a per-idea finite state machine.

- Industry-scale recommenders break serial auto-research: a single model change needs days of training and a full cycle (ideation, implementation, validation, training, recovery, analysis) takes 3-7 days, so Auto-RecSys runs multiple ideas concurrently across servers and incorporates results asynchronously.
- System complexity forces recoverable execution: thousands of lines of config plus distributed infra, GPU preemption, checkpoint corruption, stale data, and session/server restarts require persistent, cross-session state and accumulated operational knowledge instead of local reruns.
- The harness has three designs: distributed asynchronous execution tracked by a persistent per-experiment state machine, centralized cross-server memory holding states/playbooks/histories/trajectories, and cognitive-procedural separation where natural-language skills guide LLM reasoning while deterministic scripts enforce state transitions and validation.
- A dual-loop self-evolving architecture improves both dimensions over time: the Execution Evolution Loop crystallizes successful pipelines into model-specific playbooks and retains failures as dead ends, while the Idea Evolution Loop feeds outcomes and conclusions into future ideation to avoid redundancy and track baseline shifts.
- Five design principles govern the system: compose over existing training/submission/version-control/monitoring infra, keep a human in the loop at 4 checkpoints (idea selection, code review, training submission, results review; skipped in autonomous mode), design async, self-evolve procedures and ideas, and treat failure as expected via atomic writes, append-only logs, trajectory logs, and a dead-end catalog.
- Knowledge is tiered in three layers: a shared model-agnostic orchestrator skill (experiment loop, transitions, baselines, analysis), per-model-type playbooks (key files, config conventions, hardware needs, dead ends, proven strategies), and per-iteration state files (commit hashes, job IDs, validation results, verdicts) — so new models onboard with only playbook bootstrapping.
- Each idea moves independently through ideating → implementing → validating → training → analyzing, with a debugging branch on training failure and a loop back to ideating; per-idea state-file isolation allows parallel stages/servers and contains GPU-hour failures, and interactive mode (pauses for approval) graduates to autonomous mode as playbook confidence grows.

## 2. [[wiki/02-evolution-loops|Execution and idea evolution loops + persistence]]

**In one sentence:** AutoRecSys scales industry-scale recommender research by pairing an Execution Evolution Loop that distills operational know-how into evolving per-model playbooks with an Idea Evolution Loop that runs a parallel portfolio of architecture-grounded ideas, both backed by a centralized persistent memory store with recovery.

- Each model gets a playbook — a human-readable procedural recipe (markdown) plus a machine-readable iteration metadata file — capturing six categories: key files/classes, config-flag discipline, exact validation command and expected output, submission recipe, dead ends, and proven strategies.
- Playbooks evolve by text-space skill optimization: every agent action is logged as a session trajectory, then distilled into dead-end avoidance instructions ("DO NOT" directives), numbered pipeline recipes, and crystallized submission configuration; 31 session transcripts validated that LLMs consume this natural-language form effectively.
- Playbook lifecycle runs interactive bootstrap then evolve: human-guided first iteration, semi-supervised middle iterations with falling failure rates, then reliable autonomous mode; one-shot transfer reuses the first mature playbook's structure as a template so each new model only fills in its own files, flags, commands, and recipes.
- Dead-end recording enables self-healing without manual rules: e.g. defaulting away from an unstable GPU generation, pinning a compatible package layer version, and auto-looking-up the latest valid warm-start checkpoint after an expiry.
- Ideation is grounded in a persistent model context (architecture, task heads, feature inventory, enabled modules) to avoid re-reading thousands of lines per session; candidates come from researcher proposals, external literature mining, and autonomous brainstorming (embeddings, gating, auxiliary losses), then are filtered against experiment history and ranked by metric impact, complexity, regression risk, and novelty.
- Long training feedback (hours to days) is handled by a distributed portfolio: each idea has its own state file, all ideas on a model share one baseline with aligned date ranges for fair A/B comparison, and a global registry prevents conflicts — raising throughput to multiple experiments per week while the researcher manages a portfolio instead of one serial run.
- Persistence is a centralized cross-server memory store with code-guarded structured state (registry, per-idea active/completed JSON, baselines, append-only JSONL experiment history, backlog, playbooks, per-idea markdown, knowledge base, session trajectories) plus a dashboard, append-only corruption isolation, and a recovery protocol that reconstructs context and polls training jobs for seamless multi-server handoff.

## 3. [[wiki/03-evaluation|Evaluation, related work, outlook]]

**In one sentence:** AutoRecSys cuts hands-on researcher effort per idea from hours/days to minutes and lets parallel portfolios run, while its natural-language playbook drives operational fixes from 4.0 to 0.5 per iteration across 31 iterations and recovers past a baseline shift — positioning it as a persistent, recoverable harness for industry-scale recommendation research rather than rapid small-task iteration.

- The operative metric is human bandwidth per idea (hands-on attention from proposal to analyzed result), not wall-clock cycle time, which stays dominated by days-long training plus queueing outside the system's control.
- Two modes trade control for effort: human-in-the-loop keeps idea-selection and implementation-review checkpoints and delegates the rest (minutes of effort); fully autonomous skips checkpoints (minimum effort, only idea selection plus escalations) but risks spending training on weaker ideas, so it is favored once the playbook is mature and ideas are low-risk.
- Across 31 unique iterations on one representative model spanning a baseline shift at iteration 21, major (operational) fixes fell from 4.0 per iteration to 1.3 during stabilization (iterations 5–20), spiked during transition (21–25), then recovered to 0.5 per iteration with 5 of 6 post-transition iterations (26–31) needing zero fixes.
- Errors are categorical, not random: each category (GPU instability, resource tags, build-date conventions, input naming, package-layer mismatches, publish failures) appears in one or two phases, is recorded as a dead end, then disappears; the only post-transition error was a novel graph-compilation type-inference bug no prior experience could prevent.
- The playbook works through natural language (19-entry dead-ends table with "DO NOT" directives, proven-strategies table, pipeline recipes: 6 key files to read, toy-train validation, build-based submission with 9 pinned parameters, metrics-fetch plus baseline-comparison analysis) built from 49 dead ends and 17 error-fix patterns; the agent rarely uses numerical metadata.
- Robustness comes from persistent state: cross-server resume via draft diffs plus trajectory logs, a 970-log-entry / 110-tool-call fully autonomous session (fused-kernel import diagnosis, package-layer rebuild, resubmission), and adaptive workflow edits such as skipping a repeatedly failing publish step.
- Positioning and outlook: unlike AI Scientist, AutoResearch, FARS, and EvoScientist (bounded tasks, fast feedback), AutoRecSys targets days-long industry-scale training with evolving baselines via parallel exploration and recoverable state; future work is proxy models for screening, cross-model transfer, validation-gated playbook updates, adaptive confidence-based human review, and team-scale operation.

<!-- FIVE_MOVES_START -->
## The argument in five moves

1. Industry-scale recommenders break serial auto-research because each idea costs days of training on fragile distributed infrastructure.
2. AutoRecSys answers with distributed asynchronous execution where each idea moves through its own persistent per-idea state machine.
3. Cognitive-procedural separation lets natural-language skills guide agent reasoning while deterministic scripts enforce transitions and validation.
4. The Execution Evolution Loop distills session trajectories into per-model playbooks and dead-end catalogs that drive operational fixes down over time.
5. The Idea Evolution Loop runs a parallel portfolio of architecture-grounded ideas against one shared baseline to survive days-long feedback delays.
6. Tiered persistent memory enables cross-server recovery plus interactive-to-autonomous bootstrapping and one-shot transfer to new models.
7. Across 31 iterations operational fixes fall from 4.0 to 0.5 per iteration with recovery past a baseline shift, positioning the system as a recoverable harness for industry-scale recommendation research.
<!-- FIVE_MOVES_END -->
