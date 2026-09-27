---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

# AutoRecSys — Retrieval Practice

_One question per wiki section (two per section). Recall from memory, then expand the answer._

## 1. Overview and experiment state machine

### Q1 (core recall): Why does serial auto-research fail for industry-scale recommenders, and what three designs does the AutoRecSys harness use instead?

<details>
<summary>Answer</summary>

Serial auto-research fails because a single model change needs days of training, and a full cycle (ideation, implementation, validation, training, recovery, analysis) takes 3–7 days.

The harness uses three designs: (1) distributed asynchronous execution tracked by a persistent per-experiment state machine, (2) centralized cross-server memory holding states / playbooks / histories / trajectories, (3) cognitive-procedural separation — natural-language skills guide LLM reasoning while deterministic scripts enforce state transitions and validation.

Each idea moves independently through ideating → implementing → validating → training → analyzing, with a debugging branch on training failure.
</details>

### Q2 (elaboration): Why is persistent, cross-session state required — what breaks if the agent just reruns locally after a failure?

<details>
<summary>Answer</summary>

System complexity forces recoverable execution: thousands of lines of config plus distributed infra, GPU preemption, checkpoint corruption, stale data, and session/server restarts.

Without persistent cross-session state and accumulated operational knowledge, a restart loses commit hashes, job IDs, validation results, and verdicts; the agent would repeat dead ends, resubmit with stale checkpoints or data, and cannot hand off across servers. The fix is per-idea state-file isolation, atomic writes, append-only logs, trajectory logs, and a dead-end catalog — so failures are contained instead of losing GPU-days.
</details>

## 2. Execution and idea evolution loops + persistence

### Q3 (core recall): What six categories does each per-model playbook capture, and how does the playbook lifecycle run?

<details>
<summary>Answer</summary>

Six categories: key files/classes, config-flag discipline, exact validation command and expected output, submission recipe, dead ends, and proven strategies. Each playbook is a human-readable procedural recipe (markdown) plus a machine-readable iteration metadata file.

Lifecycle: interactive bootstrap (human-guided first iteration) → semi-supervised middle iterations with falling failure rates → reliable autonomous mode. One-shot transfer reuses the first mature playbook's structure as a template, so each new model only fills in its own files, flags, commands, and recipes. Distillation uses 31 session transcripts: actions logged as trajectories, then distilled into "DO NOT" directives, numbered pipeline recipes, and crystallized submission config.
</details>

### Q4 (elaboration): What breaks if long-training ideas run without a shared aligned baseline and a global registry?

<details>
<summary>Answer</summary>

Training feedback takes hours to days, so ideas run as a distributed portfolio with one shared baseline with aligned date ranges for fair A/B comparison, plus per-idea state files and a global registry.

Without the aligned shared baseline, results are not comparable (baseline shifts, e.g. the observed shift at iteration 21, would be mistaken for idea gains/regressions) and ideation repeats redundant experiments. Without the global registry and per-idea state files, concurrent experiments on multiple servers conflict, and throughput collapses from multiple experiments per week back to one serial run managed step by step.
</details>

## 3. Evaluation, related work, outlook

### Q5 (core recall): What happened to operational fixes across the 31 iterations around the baseline shift at iteration 21?

<details>
<summary>Answer</summary>

Major (operational) fixes fell from 4.0 per iteration to 1.3 during stabilization (iterations 5–20), spiked during transition (iterations 21–25), then recovered to 0.5 per iteration, with 5 of 6 post-transition iterations (26–31) needing zero fixes.

Errors were categorical, not random: each category (GPU instability, resource tags, build-date conventions, input naming, package-layer mismatches, publish failures) appeared in one or two phases, was recorded as a dead end, then disappeared. The only post-transition error was a novel graph-compilation type-inference bug no prior experience could prevent. Built from 49 dead ends and 17 error-fix patterns, including a 19-entry dead-ends table.
</details>

### Q6 (transfer): A new model type must onboard with only playbook bootstrapping, and its cluster uses a different unstable GPU generation plus an expiring warm-start checkpoint. Which playbook mechanisms handle this?

<details>
<summary>Answer</summary>

Apply the Execution Evolution Loop + dead-end self-healing: reuse the first mature playbook's structure as a template (key files, config conventions, hardware needs, validation command, submission recipe), fill in only the new model's files, flags, commands, and recipes, and run interactive bootstrap first.

For the new failure modes, record dead ends so the agent self-heals without manual rules: default away from the unstable GPU generation, pin a compatible package layer version, and auto-look-up the latest valid warm-start checkpoint after expiry — plus cross-server resume via draft diffs, trajectory logs, and polling of training jobs (as in the 970-log-entry / 110-tool-call autonomous session).
</details>

### Q7 (evaluation): What is the weakest link in Auto-RecSys's evidence for its headline claim that hands-on researcher time drops from hours/days to minutes?

<details>
<summary>Answer</summary>

The digest reports a fix-rate trend (4.0 → 0.5 operational fixes per iteration over 31 iterations on one model) and qualitative session logs, but no controlled time-and-motion measurement of actual researcher hours against a human-run baseline on the same set of ideas — the headline efficiency claim is a plausible inference from the fix-rate curve, not a directly measured comparison. It is also evidence from a single representative model at a single organization, so the generalization of the fix-rate pattern to other models and teams is unverified. See [[critical_thinking|Critical Analysis]].
</details>
