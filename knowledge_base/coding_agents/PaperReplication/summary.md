# Coding-agents can replicate scientific machine learning papers

**Paper:** [Coding-agents can replicate scientific machine learning papers (Hans & Bilionis, 2026)](https://arxiv.org/abs/2607.02134)

## Human Readable TL;DR

Imagine handing a lab assistant a stack of physics papers and asking them to redo the experiments -- but instead of just trusting them when they say "done," you make them keep a lab notebook where every measurement, every comparison to the original paper, and every check-off has to be written down and verified before anything counts as reproduced. This paper builds exactly that kind of notebook system, called "Paper-replication," for AI coding agents. Instead of trusting an AI's final "I'm done!" message (which research shows AIs are bad at judging honestly), the system forces the agent to keep persistent files that track which claims it still needs to reproduce, how it built its code, and how its results compare to the paper -- and only lets it declare victory once an outside checklist confirms everything lines up. Tested on four physics/math papers with three independent tries each, the AI always eventually got all the checkboxes filled in, but different tries took wildly different amounts of time and effort to get there.

## TL;DR

The paper introduces *Paper-replication*, a coding-agent skill that formalizes "paper replication" (reconstructing a paper's method and regenerating its results from paper materials alone) as a target-level evidence task rather than a single prompt-following exercise. Each paper claim becomes a *target*; each target requires an *evidence bundle* (candidate result, run record, provenance linking the run to the paper's method, a claim-specific comparison, and report coverage) stored in a persistent workspace, and a formal *completion gate* checks all of this externally before any claim counts as matched. Evaluated with a Codex/GPT-5.4 agent across 12 independent runs (4 SciML papers x 3 runs), all 12 workspaces reach the completion gate with all 158 recorded targets matched -- but repeated runs of the *same* paper differ substantially in how finely they decompose targets, numeric fidelity against paper-reported error thresholds, elapsed time (1.2-13.0 hours), correction/rework volume, and which acceptance-rule type they apply to the same claim.

---

## Problem & Motivation

Scientific machine learning (SciML) papers make computational claims (e.g., "relative L2 error < 5%," "the 95% credible interval covers held-out data") that depend on solvers, differentiable programming, PINNs, sparse system identification, and Bayesian/sampling-based inversion. The reported numbers also depend on data, preprocessing, stochastic training, and implementation choices that are often underspecified or absent from the paper text -- so replicating a paper from its materials alone (no author code, no environment) is harder and less well-defined than rerunning a released, packaged codebase.

Prompting a coding agent to "replicate this paper" does not by itself preserve progress across a long session or verify whether the agent's generated evidence actually supports the paper's claims. Left unmanaged, an agent will often stop after reproducing only part of a paper, lose track of which claim to address next, count copied figures/assets from the paper's own LaTeX source as if they were newly generated evidence, or substitute an easier method and still call it a match. Studies of LLM self-correction show a model cannot reliably judge or repair its own reasoning without external feedback, so a prompt that just asks the agent to "finish" invites premature completion claims. The paper's core thesis: for paper replication, the agent's final chat message is not sufficient evidence -- completion needs to be a property of a persistent, externally-checked workspace instead.

---

## Main Original Ideas

1. **Target-level evidence formalization.** Paper replication is defined as reconstructing a paper's method from text, regenerating the results that support its claims, and recording evidence per claim. Each computational claim selected for reproduction becomes a *target* `t_j` in a finite target set; for each target the agent must produce an *evidence bundle* `E_j = (ŷ_j, R_j, P_j, C_j, G_j)` -- the candidate result, its execution/run record, a provenance record linking the implementation to the paper's method, a claim-specific comparison against the paper's reported quantity, and confirmation the result appears in the final replication report. A target can only be marked MATCHED when every part of this bundle exists and passes external checks -- an output artifact alone (e.g. a generated figure) never counts as evidence on its own.

2. **Persistent workspace as harness engineering, not prompting.** Rather than relying on prompt instructions or the chat transcript, Paper-replication stores agent state in workspace files: a manifest (paper source, hash, author-code policy, compute environment), a *reproduction matrix* (one record per target: status, comparison method, report location), a *task ledger* (the one active target plus open questions/checks), *specification files* (the agent's restatement of the paper's equations/algorithms and assumptions), *run records* + *provenance records* under `artifacts/`, and a *replication report*. This lets the agent resume after interruptions without depending on conversation history, and makes its state auditable by an external validator.

3. **Formal completion gate.** Completion is defined as a Boolean workspace state (Eq. 3): `V_complete = V_spec ∧ V_progress ∧ V_report ∧ (all targets MATCHED) ∧ (no active target) ∧ (report PDF exists)`. Three external checks (specification completeness, progress/evidence consistency, report coverage) plus the target-set conditions must all hold. This deliberately shifts "done" from a statement the agent makes to a state the workspace is in.

4. **Skill implementation with hash-based provenance separation.** Implemented as a two-layer coding-agent skill: instruction layer (`SKILL.md` + Codex/Claude Code adapter prompts) and workspace utilities (`scripts/paper_replication.py`). Paper-provided assets (figures, rendered PDF pages, source files) are hashed and kept strictly separate from agent-generated outputs (`artifacts/figures/`, `artifacts/tables/`, `artifacts/runs/`, `artifacts/provenance/`), so a validation check can detect and reject a "matched" target whose output is actually just a copy of paper-provided material.

5. **Repeated-run case-study methodology for judgment variation.** The authors don't just report pass/fail; they run each of 4 papers 3 independent times and fit Bayesian hierarchical models (Gamma-Poisson for target-count/decomposition variation, a headroom model for scalar numeric fidelity relative to paper-reported accuracy thresholds, a log-normal model for elapsed effort) to characterize how much independent agent runs of the *same* paper vary in decomposition, fidelity, time, and even which type of acceptance rule (numeric vs. distributional vs. structural) they apply to the same claim.

---

## Key Findings

**Overall completion:** All 12 of 12 independent runs (4 papers x 3 runs: PIFT, PINN-I, PINN-II, SINDy) reach the completion gate; all 158 recorded targets across the corpus reach MATCHED with report coverage.

| Paper | Runs | Targets/run | Matched | Elapsed time (h), median [95% CI] | Superseded executions |
|---|---|---|---|---|---|
| PIFT | 3 | 8, 8, 25 | all | 2.2 [1.1, 4.4] | 3 |
| PINN-I | 3 | 8, 8, 8 | all | 5.0 [2.5, 9.9] | 11 |
| PINN-II | 3 | 9, 9, 15 | all | 6.9 [3.0, 13.4] | 10 |
| SINDy | 3 | 20, 20, 20 | all | 1.9 [1.0, 4.3] | 1 |

- **Target decomposition varies even with stable completion.** PINN-I and SINDy show no run-to-run variation in target count (decomposition ratio 1.0); PIFT (ratio 3.1) and PINN-II (ratio 1.7) vary because a single run sometimes records separate targets for sub-panels of a composite figure or splits out appendix inference claims as additional targets.
- **Numeric fidelity vs. paper-reported thresholds:** across 13 standardized scalar anchors (4 PINN-I solution errors, 8 PINN-II coefficient errors, 1 SINDy Lorenz coefficient error) and 39 anchor-run observations, 37/39 fall inside the paper's own reported accuracy-scale threshold. Two do not: a Schrödinger-equation run-3 relative L2 error of 4.8x10^-2 against a 1% threshold, and a Navier-Stokes run-1 coefficient error of 16.4% against a 10% threshold -- both were still recorded MATCHED under their own workspace's acceptance rule but fail the stricter fixed paper-anchored comparison. Average headroom (log10 margin inside the threshold) is **0.51 for PINN-I (~3.2x inside), 1.75 for PINN-II (~57x inside), 0.42 for SINDy (~2.6x inside)**; run-to-run scatter on this scale is largest for PINN-II (posterior median 1.16, 95% CI [0.86, 1.66], ~14x factor across reruns).
- **PIFT has no scalar anchor at all** -- its claims (posterior collapse, bimodality, selective identifiability) are judged through distributional/structural evidence instead, illustrating that "MATCHED" is a claim-specific rather than single-metric standard.
- **Effort is not constant even though completion is.** Elapsed replication time ranges 1.2-13.0 hours across runs. PINN-I and PINN-II (the two PINN papers) take about 2x longer than PIFT and SINDy, with posterior probability 0.947-0.972 that a PINN paper takes longer than a non-PINN paper in any given comparison. 25 of the corpus's tracked executions were later superseded by correction work before final evidence was accepted -- 21 of those 25 occurred in the two PINN papers (11 in PINN-I, 10 in PINN-II), showing most rework happens there.
- **Judgment variation:** run-to-run agreement on which acceptance-rule *type* (numeric/distributional/structural) is applied to the same aligned claim is highest for SINDy (19/20 = 0.95) and lowest for PINN-II (5/11 = 0.46), showing two independently "completed" workspaces can support the same paper claim with different kinds of recorded evidence.
- **Bayesian modeling stack:** all models fit in NumPyro with the No-U-Turn Sampler (NUTS), 4 chains, 2000 retained posterior draws each; target coverage modeled with a Gamma-Poisson hierarchical model, numeric fidelity headroom and elapsed-time effort each modeled with their own hierarchical Normal/log-normal models.

---

## Suggestions & Future Directions

1. The study has **no ablation without the Paper-replication skill** -- it characterizes what the workflow produces relative to itself across runs, not its causal effect size versus an unstructured "just replicate this paper" prompt.
2. Only **4 papers, 3 runs each, one coding-agent/model/reasoning setting** (Codex + GPT-5.4, Extra High reasoning) were tested -- the corpus is too small to draw strong between-paper conclusions, even though within-paper run-to-run comparisons are well supported.
3. Distributional and structural targets (e.g. PIFT's posterior shape, SINDy's trajectory geometry) get **only one recorded comparison per run**; independent, repeated judging of the same generated evidence for these non-scalar target types is left as future work.
4. The **paper-anchored scalar thresholds are an analysis convention** chosen by the authors (e.g. a 10% coefficient-error convention for PINN-II, extrapolated from the source paper's own tolerance discussion) -- a different defensible threshold could change how many anchors fall inside vs. outside the line, though it would not change the observed run-to-run differences themselves.
5. Source papers frequently omit exact reproducibility inputs (sampled training sets, seeds, optimizer/sampler states, noise magnitudes, preprocessing/plotting conventions) -- Paper-replication surfaces these gaps explicitly as recorded assumptions rather than resolving them, leaving "true" replication of some targets (e.g. SINDy's Hopf noise settings, the cylinder-wake preprocessing pipeline) fundamentally underdetermined by the paper text.
6. Code, prompts, and all 12 generated case-study workspaces are released for reuse/extension: https://github.com/PredictiveScienceLab/paper-replication-paper

---

## Authors & Institutions

Atharva Hans (School of Mechanical Engineering, Purdue University, West Lafayette, IN 47907, USA; present affiliation: Eli Lilly and Company, Indianapolis, IN 46285, USA) -- Conceptualization, Methodology, Software, Validation, Formal analysis, Investigation, Visualization, Writing; Ilias Bilionis (School of Mechanical Engineering, Purdue University, West Lafayette, IN 47907, USA) -- Conceptualization, Methodology, Supervision, Funding acquisition, Writing.
