> [[index|Wiki]] | [[summary|Summary]]

# Demystifying Agent Skills: Why They Work-Until They Don't — Digest

The whole source at medium depth: every section's headline claim and key points, in order. ~10 min. Descend into a wiki page only where you need the detail.

## 1. [[wiki/01-introduction-and-related-work|Introduction and Related Work]]

**In one sentence:** Existing skill evaluation only measures aggregate task success, so this work reframes the question from "whether skills work" to "when skills help, why they work, and where they fail" by contrasting matched executions with and without skills and attributing gains and failures to concrete mechanisms along the skill-use pipeline.

- Skills are compact, standardized descriptions of what to do, what to check, and what pitfalls to avoid, and promise three advantages over raw traces or workflow memories: compressing noisy experience into shorter context, stabilizing format, and transferring knowledge across related tasks.
- Skills improve over Workflow Memory by 6.06 points in matched comparisons, with procedural anchoring accounting for 65.7% of skill cases versus 4.5% for explicit knowledge injection.
- The study normalizes 8,135 trial records, open-codes 240 sampled trajectories, and consolidates 238 valid unique labels into a taxonomy of three high-level categories and twelve skill-use modes.
- Retrieval is a separate bottleneck: as skill pools grow from 5 to 100, actual-use precision falls from 29.6% to 3.3%.
- Selecting the correct skill does not guarantee task success, and invoking a related non-ground-truth skill can still provide useful procedural support; confusable distractors impair offline identification yet downstream success remains stable.
- Skills primarily reduce execution-layer failures (environment-setup errors, output-format mismatches, service-lifecycle failures, shell-command corruption), whereas workflow memory preserves useful procedural evidence but also irrelevant exploration, failed branches, and verbose process noise.
- The work organizes itself along four research questions spanning representation, annotation, cross-framework transfer, and retrieval difficulty.
- Skill failure has a lifecycle structure: it happens when distilled guidance is noisy, over-specific, mismatched to the task context, or followed without adaptation.

## 2. [[wiki/02-study-design|Study Design]]

**In one sentence:** The paper frames skill use as a controlled transformation of prior agent experience into procedural knowledge, then designs four research questions plus a battery of contrastive, fixed-experience experiments — including a success/failure trajectory-composition grid, no-hint controls, a cross-framework transfer test, and a three-arm skill-retrieval study with growing distractor pools — to pin down when skills help, why they work, and where they fail.

- The study treats skills not as black-box performance boosts but as a controlled pipeline: prior executions are reused either as direct workflow memories (trace-level execution details) or as distilled skills (trace details compressed into a standardized procedural artifact), and RQ1 asks how that packaging shape is what matters when the underlying trajectories are fixed.
- Four research questions structure the work: RQ1 (representation shape of experience reuse), RQ2 (whether the benefit comes from procedural content or from success/failure outcome labels), RQ3 (whether distilled guidance transfers across agent frameworks), and RQ4 (how skill-pool construction affects retrieval and downstream use).
- RQ1–RQ2 run the same protocol under two agent–model pairings: Codex + GPT-5.3-Codex and Gemini CLI + Gemini-3.1-Pro-Preview; RQ3 builds artifacts from the Codex setting and evaluates them under Gemini CLI + Gemini-3.1-Pro-Preview; RQ4 uses Gemini CLI + Gemini-3.1-Pro-Preview and Codex + GPT-5.4, because GPT-5.3-Codex was no longer available under the same evaluation access when RQ4 was conducted — so RQ4 is interpreted strictly as within-pairing comparisons among its three experiments and not directly against RQ1–RQ3.
- The core RQ1–RQ2 design is a three-condition contrast — Raw (no prior experience), Workflow Memory (cleaned procedural traces from prior executions), and Skill (a standardized SKILL.md distilled from the same workflows) — with both artifact types built from the *same selected trajectories* and evaluated on the *same target tasks*, holding experience constant while varying only its representation.
- A fixed-budget composition grid sweeps source evidence from success-only to failure-only across trajectory mixtures (e.g., 5s0f through 0s5f), and Skill comes in standard (success/failure identities visible to the skill creator) and no-hint (annotations removed, same trajectories and execution protocol) variants to separate procedural content from outcome signals.
- The benchmark suite combines Terminal Bench (Merrill et al., 2026) and SkillsBench (Li et al., 2026); downstream execution follows Harbor's standard evaluation workflow with n = 5 unique trials per task and parallelism of 20 unless otherwise noted, while retrieval-isolation experiments use one query per task–pool setting.
- RQ4 uses a controlled candidate-pool construction shared by all three arms: the task's ground-truth skill set plus distractors, pool size ranging from 5 to 100, with distractors sampled as random, semantically similar, or dissimilar skills; the three arms are Arm 1 (embedding retrieval with Qwen3-Embedding-0.6B), Arm 2 (explicit agent selection), and Arm 3 (full-pool real execution), compared as independent measurements rather than sequential stages.
- The paper characterizes how injected prior experience affects execution with five mechanism labels: procedural_anchor (usable procedure, ordering, checklist, tool sequence, or verification plan), knowledge_injection (concrete domain knowledge the agent otherwise lacked), failure_warning (warns about a pitfall the agent avoids), none (not used in a meaningful way), and counterproductive (misleads the agent or makes the run worse).

## 3. [[wiki/03-skill-use-mechanisms|Skill-Use Mechanisms]]

**In one sentence:** The authors go beyond aggregate success rates by building a human-validated, 3-category / 12-mode taxonomy of skill-use trajectories and comparing matched task triples across raw, workflow-memory, and skill arms to expose *which behaviors* change when prior experience is injected as a workflow versus as a distilled skill.

- A contrastive trajectory-analysis pipeline normalizes the heterogeneous benchmark outputs into a shared manifest of **8,135 trial records** (task identity, execution arm, verifier outcome, injected artifact, and a trajectory transcript when available); **7,837** of those records contain agent transcripts.
- An open-coding pass over **240 sampled trajectories** yields **238 valid unique labels**, which are then merged into a **12-mode canonical taxonomy** organized into **3 top-level Skill-use Categories (SCs)**.
- Both LLM-assisted construction stages are validated by an independent human annotator: **714 trajectory–label checks** (238 labels × 3 supporting trajectories), all confirmed, and a second-stage mapping to the 12 canonical modes achieves **95.8% exact agreement** with the LLM and **Cohen's κ = 0.952** (Table 3).
- The unit of analysis is a **paired triple**: the same task and setting run under three arms (raw execution, workflow-memory injection, skill injection). The authors construct **528 triples** — SkillsBench (**144**), TerminalBench 2.0 (**186**), Terminal-Bench-Pro (**198**) — giving **1,584 arm-level mode assignments**.
- For each triple, an LLM judge assigns each arm a taxonomy mode, records **pairwise changes between arms**, and tags whether the injected artifact acts through **procedural anchoring, knowledge injection, failure warning, no meaningful use, or counterproductive guidance**.
- **SC1 (successful procedural anchoring)**: the agent succeeds autonomously, or prior experience provides useful guidance. Skill arms shift more trajectories into SC1 than workflow memory — **326/528** skill-vs-workflow SC1 assignments vs. **294/528**.
- **SC2 (execution- and verification-layer failures)**: skill arms show fewer of these than raw and workflow memory — **124/528** (skill) vs. **197/528** (raw) and **176/528** (workflow).
- **SC3 (invocation, applicability, and boundary failures)**: guidance is present but misused, overapplied, ignored, or constrained by external limits; skill arms *increase* these — **78/528** (skill) vs. **19/528** (raw).

## 4. [[wiki/04-findings|Findings, Conclusion, and Limitations]]

**In one sentence:** Skills work best as procedural anchors that stabilize execution (outperforming workflow memory built from the same trajectories by +6.06 points), but they cannot repair algorithmic or verification failures, introduce their own invocation/applicability failure surface, and suffer a sharp precision collapse when retrieved from large or semantically confusable pools — even as downstream task success stays remarkably flat.

- Skill-augmented runs achieve the highest oracle-status success rate: 61.9% vs 59.1% raw execution and 55.9% workflow memory; the effect over workflow memory is +6.06 percentage points (95% bootstrap CI [+0.76, +11.36]).
- Mechanism labels show skills work through procedural anchoring, not knowledge injection: procedural_anchor accounts for 65.7% of skill mechanisms vs only 4.5% for explicit knowledge_injection.
- SC2 execution/verification fragility modes fall from 37.3% of raw-arm and 33.3% of workflow-arm labels to only 23.5% for skills; environment/infrastructure failure drops from 5.3% (raw) to 1.7% (workflow) to 0.2% (skills).
- Skills do not fix deep reasoning failures: algorithmic_logic_error stays at 7.4–11.0% across arms and static_verification_without_runtime at 11.7–12.5%.
- Skills create a new failure surface — skill_guidance_misapplied_or_ignored appears in 10.0% of skill-arm cases vs 0.8% raw and 0.4% workflow memory.
- Workflow memory's distinctive penalty is process overload: timeout_budget_exhaustion appears in 10.6% of workflow-memory cases vs 1.7% raw and 4.4% with skills.
- Outcome labels matter most when failed trajectories enter the pool: Gemini on Terminal-Bench-2 at 3s2f reaches 0.7462 with outcome hints vs 0.4000 without.
- Retrieval precision collapses with pool size — averaged actual-use precision falls from 29.6% at pool size 5 to 3.3% at pool size 100 — while downstream success changes only from 36.4% to 39.3%.

## 5. [[wiki/05-implementation-details-and-prompts|Implementation Details and Prompts]]

**In one sentence:** The appendix documents how the paper's four research questions were operationalized — model–framework pairings, benchmarks, the trajectory-labeling and taxonomy pipeline, per-RQ protocols, and retrieval metrics — and supplies the full data tables (arms, manifest coverage, paired-triple sample, taxonomy distributions, baseline success, matched token costs, and complete retrieval/ablation results) that back up the claim that skills work best by distilling prior experience into a compact, actionable SKILL.md artifact.

- Evaluation used two agent–model pairings for RQ1–RQ3 (Codex + GPT-5.3-Codex and Gemini CLI + Gemini-3.1-Pro-Preview), and for RQ4 used Codex + GPT-5.4 because GPT-5.3-Codex was no longer available; RQ4 is therefore interpreted only through within-pairing comparisons.
- The trajectory-labeling manifest contains 8,135 trial records across Terminal-Bench 2.0 (3,254), Terminal-Bench-Pro (2,993), and SkillsBench (1,888), with success defined strictly by positive verifier reward, not self-assessment.
- Taxonomy induction used a two-round batched LLM process (batches of ~60 records, then a global merge) starting from 238 valid open-coded labels, yielding a final canonical taxonomy of 12 modes deliberately mixing success and failure categories.
- The paired contrastive sample is 528 triples (SkillsBench 144, TB2 186, TB-Pro 198; 88 triples per mixture setting), each containing all three arms (Raw, Workflow memory, Skill) for the same task.
- On the 528-triple sample, oracle success rates are Raw 59.1%, Workflow memory 55.9%, Skill 61.9%, and the most robust paired delta is Skill vs Workflow memory (+0.0606, 95% bootstrap CI [+0.0076, +0.1136]), not skill vs raw (+0.0284, CI spanning zero).
- The taxonomy shows skills shift outcomes toward skill-guided success (SC1 skill_guided_success: 0.4% in Raw, 61.6% in Skill arm) while introducing their own failure mode (SC3 skill_guidance_misapplied_or_ignored: 0.8% → 1.0% in the Skill arm).
- Lightweight baselines on 26 Terminal-Bench-2 tasks (130 trials) show Skill at 79.2% success versus 62.3% Workflow Memory, 59.2% test-first template, 47.7% short plan, and 50.0% Raw — indicating the skill advantage is not explained by compact procedural text alone.
- On the matched 83-task token intersection, Skill achieves the highest success (69.6%, +5.5 pp over Raw) with lower total tokens than Raw (521.5K vs 555.7K per task) but more tokens than Workflow Memory (426.2K, +0.7 pp success) — an effectiveness–efficiency trade-off.
- Appendix B lists the prompt templates used (skill-creator.md, skill-creator-no-hint.md, trajectory labeling, taxonomy merge), though the prompt bodies are rendered as extracted figures/images in the PDF from which this chunk was pulled and their verbatim text does not survive in the text layer.

## The argument in five moves

1. Skill evaluation to date only checks whether task success went up — it can't say *why*, so the authors design a contrastive pipeline that holds the underlying prior experience fixed and varies only its representation (Raw / Workflow Memory / Skill).
2. A human-validated 3-category / 12-mode taxonomy, built by open-coding 240 trajectories and confirmed at κ = 0.952 agreement, turns "did it succeed" into "which specific behavior changed" across 528 matched triples.
3. The taxonomy shows skills win primarily by acting as procedural anchors (65.7% of mechanism labels) rather than by injecting facts (4.5%) — this is the paper's central mechanistic claim, and it is what explains the +6.06-point edge over workflow memory built from the same traces.
4. That same distillation trades one failure class for another: execution/verification failures fall sharply (SC2), but a new invocation-layer failure mode emerges (SC3, skill_guidance_misapplied_or_ignored, up to 10.0% of skill-arm cases) — so skills relocate rather than eliminate failure.
5. A separate but complementary problem lives upstream of invocation: as the skill library available at retrieval time grows from 5 to 100 candidates, actual-use precision collapses from 29.6% to 3.3%, driven mainly by semantically similar distractors rather than raw pool size.
6. Despite that collapse, downstream task success barely moves (36.4%→39.3%), showing that exact ground-truth skill matching is neither necessary nor sufficient for task completion — related non-ground-truth skills can still supply usable procedural support.
7. The unifying conclusion: skill utility is a lifecycle property spanning representation, retrieval, and invocation, not a single memory-injection event — so building better self-improving agents means improving all three stages, not just accumulating more skills.
