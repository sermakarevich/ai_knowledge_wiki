---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

# RecursiveSelfImprovement — Retrieval Practice

## Section 1: Intro, HCI problems, RSI concept

### Q1 (core recall): What is the verbatim RSI definition, and what HCI numbers motivate it?

<details>
<summary>Answer</summary>

RSI is the capability to autonomously transform acquired experience and feedback into persistent self-changes (parameters, harnesses, improvement policies) such that these changes affect the mechanisms for generating, evaluating, selecting, and consolidating subsequent improvements. Motivation: HCI analysis over 393 model-benchmark observations (2023–Sep 2026, 10 domains) shows by 2026 advanced math 86.4 and graduate science 85.8 vs software engineering 52.6, search/terminal agents 56.8, tool agents 39.9, cybersecurity agents 91.9 — the largest remaining headroom is in interactive stateful tool-using workflows. Lifecycle proof points: A-Evolve-Training (30B Nemotron external score 0.80 → 0.86 over four autonomous rounds vs 0.87 top human) and Ouroboros (revises coding agent tools, context, prompts, implementation under tests plus human review).

</details>

## Section 2: Autonomy levels B0-L2

### Q2 (elaboration): Why is B0 excluded as non-RSI, and what breaks if you just run more B0 iterations under a fixed verifier?

<details>
<summary>Answer</summary>

B0 changes only the current-task output (Self-Refine, Reflexion, Tree of Thoughts revise/verify/select) with no persistent system change, so nothing accumulates across tasks. Its four hard limits: experience does not accumulate, the procedure stays human-defined, self-generated feedback can reinforce errors (locating the first wrong reasoning step is the bottleneck), and more iterations under a fixed verifier give limited gains. By contrast L1 persists results (receive objective → execute prescribed procedure → update system state → repeat) and L2 autonomously selects the next intervention (observe → diagnose → select how to change → test → retain or revert). More B0 loops cannot cross the persistence boundary into L1 or the strategy-selection boundary into L2.

</details>

## Section 3: Autonomy levels L3-L5 and synthesis

### Q3 (elaboration): Why does higher autonomy not guarantee better results — what distinguishes structural L5 from effective L5?

<details>
<summary>Answer</summary>

Each level adds a new autonomy boundary — B0→L1 persistence, L1→L2 strategy selection, L2→L3 control of the future learning agenda, L3→L4 persistent deployment adaptation, L4→L5 recursive inheritance — but higher levels are more domain-dependent and end-to-end L5 evidence is concentrated in bounded prototypes. L5 begins only when AI persistently modifies a mechanism for future improvements (search procedure, successor evaluator, research policy) and the revised mechanism governs later rounds. Structural L5 means reuse was demonstrated; effective L5 additionally requires better successors under matched budgets and independent assessment. Without the latter, accepted changes can fail by wrong lesson, wrong scope, non-activation, or forgetting.

</details>

## Section 4: RSI across applications

### Q4 (transfer): You must design an RSI loop for a new domain where trials are cheap but feedback is delayed and confounded (e.g. a tutoring agent). Which regime's lessons apply and what loop would you copy?

<details>
<summary>Answer</summary>

Copy the healthcare (S4) pattern, not science (S1) or software (S3): S4 operates under no-unrestricted-trial-and-error, delayed/confounded feedback, and population-dependent validity. Borrow clinical-memory evolution (MedAgent-Zero/Agent Hospital persistent memory, DxEvolve cognition primitives, GSEM dual-layer graph), reasoning-strategy evolution (EvoClinician Diagnose–Grade–Evolve loop), and governed tool/workflow lifecycles (SkeMex Read–Write–Assess–Govern). Expect L2 as the realistic frontier with L4/L5 largely unexplored, and guard the common cross-regime barriers: attribute outcomes to components, scope transfer with provenance/uncertainty and rollback, evaluate whether updates improve future learning (not just current scores), and keep evaluators and deployment gates externally protected.

</details>

## Section 5: Industry landscape, challenges, conclusion

### Q5 (core recall): What measured gains do the six industrial cases report?

<details>
<summary>Answer</summary>

Theseus: clean workspace beats noisy by 21.7–51.6 percentage points across eight model–harness configs; reconstructed environment (Collection Map + Event Log) raises rubric scores 18.65–39.67 pp across five pairings. Lark: knowledge-graph pipeline lifts usability 52% → 65% human-rated (47% → 56% automated) over RAG (retrieval-augmented generation) baseline; evaluator ~84% human agreement. Humanlaya: V0→V4 cuts key-defect packages 9.0% → 3.7% on 600 held-out packages, handling time 48 → 27 min/task. ModelBest Forge: matched Megatron-LM v0.15 on H100 in ~8 h, surpassed in 1.5–2.5 days (vs 3–5 engineers for 6–12 months); MFU (model FLOPs utilization) 40.1% → 44.1% (0.5B), 47.0% → 50.9% (8B); ForgeStencil 1.15–1.9× kernel speedups (median 1.41×). Hyra: 0.9015 vs 0.9109 validation BPB (bits per byte, lower better), 76.4 s vs 77.5 s NanoGPT Speedrun, 0.771 vs 0.754 mean SOL (speedup over baseline). ARA: QA accuracy 72.4% → 93.7%, RE-Bench reproduction 57.4% → 64.4%, Chip-Bench Level-3 CPU 5.8416 (2.7% faster, 21.5% smaller).

</details>

## Section 6: Landscape appendices

### Q6 (core recall): What does the evidence base map contain — how many papers, targets, companies, and how are they tagged?

<details>
<summary>Answer</summary>

Appendix A: 491 surveyed papers in Figure 16 as three concentric rings (inner: autonomy L1–L5, middle: primary improvement targets, outer: sub-targets), with percentages by paper count and fractional weights for multi-target papers; Table 11 defines 10 improvement-target categories (Prompt & Context, Memory & Knowledge, Harness/Workflow & Control, Tools & Skills, Model, Trainer/Optimization, Evaluator & Feedback, Data & Environment, External Artifact, Full-system/Co-evolution). Appendix B: 72 companies/teams (September 2026 public-source snapshot), one row per product/work with company, product/work, sub-scenario, improvement target/artifact, AI-controlled part, plus RSI tag B0–L5 (B0 = task-local only). Six archetypes: (A) frontier labs, (B) RSI-native/AI4AI, (C) autonomous R&D/scientific discovery, (D) agent optimization/evaluation/learning infra, (E) embodied/world-model/continual adaptation, (F) persistent memory/personal AI. Tag suffixes: "adj." = adjacent infra, "cand." = plausible but undemonstrated level, "target" = future objective, asterisks = identity/boundary needs verification. Frontier labs: L2 dominant, only two L5 signals (Anthropic "When AI builds itself" as target; Meta HyperAgents, Weco AIDE2, Sakana DGM as candidates).

</details>

## Section 7: Evaluation

### Q7 (evaluation): Per [[critical_thinking|the critical analysis]], which of this survey's claims rests on the weakest evidentiary footing, and what would it take to strengthen it?

<details>
<summary>Answer</summary>

The industry section's quantitative gains (Theseus's 21.7–51.6pp, ModelBest's Megatron-matching timeline, Hyra's BPB/SOL deltas, ARA's QA-accuracy jump) are the weakest-footed strong claims: they come from company-authored case studies the survey did not independently reproduce, unlike the HCI headroom claim (393 observations, cross-checked against the per-regime application review) or the "no end-to-end L5" claim (backed by the survey's own disclosed counter-evidence, e.g. Gödel Agent's 14% below-baseline trials). Strengthening the industry claims would require independent replication or third-party audits of at least a subset of the six case studies, and explicit reporting of matched-budget baselines rather than vendor-favorable framings.

</details>
