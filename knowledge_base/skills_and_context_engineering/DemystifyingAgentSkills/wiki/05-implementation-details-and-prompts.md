> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Implementation Details and Prompts

**In one sentence:** The appendix documents how the paper's four research questions were operationalized — model–framework pairings, benchmarks, the trajectory-labeling and taxonomy pipeline, per-RQ protocols, and retrieval metrics — and supplies the full data tables (arms, manifest coverage, paired-triple sample, taxonomy distributions, baseline success, matched token costs, and complete retrieval/ablation results) that back up the claim that skills work best by distilling prior experience into a compact, actionable SKILL.md artifact.

## Key points

- Evaluation used two agent–model pairings for RQ1–RQ3 (Codex + GPT-5.3-Codex and Gemini CLI + Gemini-3.1-Pro-Preview), and for RQ4 used Codex + GPT-5.4 because GPT-5.3-Codex was no longer available; RQ4 is therefore interpreted only through within-pairing comparisons.
- The trajectory-labeling manifest contains 8,135 trial records across Terminal-Bench 2.0 (3,254), Terminal-Bench-Pro (2,993), and SkillsBench (1,888), with success defined strictly by positive verifier reward, not self-assessment.
- Taxonomy induction used a two-round batched LLM process (batches of ~60 records, then a global merge) starting from 238 valid open-coded labels, yielding a final canonical taxonomy of 12 modes deliberately mixing success and failure categories.
- The paired contrastive sample is 528 triples (SkillsBench 144, TB2 186, TB-Pro 198; 88 triples per mixture setting), each containing all three arms (Raw, Workflow memory, Skill) for the same task.
- On the 528-triple sample, oracle success rates are Raw 59.1%, Workflow memory 55.9%, Skill 61.9%, and the most robust paired delta is Skill vs Workflow memory (+0.0606, 95% bootstrap CI [+0.0076, +0.1136]), not skill vs raw (+0.0284, CI spanning zero).
- The taxonomy shows skills shift outcomes toward skill-guided success (SC1 skill_guided_success: 0.4% in Raw, 61.6% in Skill arm) while introducing their own failure mode (SC3 skill_guidance_misapplied_or_ignored: 0.8% → 1.0% in the Skill arm).
- Lightweight baselines on 26 Terminal-Bench-2 tasks (130 trials) show Skill at 79.2% success versus 62.3% Workflow Memory, 59.2% test-first template, 47.7% short plan, and 50.0% Raw — indicating the skill advantage is not explained by compact procedural text alone.
- On the matched 83-task token intersection, Skill achieves the highest success (69.6%, +5.5 pp over Raw) with lower total tokens than Raw (521.5K vs 555.7K per task) but more tokens than Workflow Memory (426.2K, +0.7 pp success) — an effectiveness–efficiency trade-off.
- Appendix B lists the prompt templates used (skill-creator.md, skill-creator-no-hint.md, trajectory labeling, taxonomy merge), though the prompt bodies are rendered as extracted figures/images in the PDF from which this chunk was pulled and their verbatim text does not survive in the text layer.

---

## Implementation Details (Appendix A)

### A.1 Model–Framework Pairings and Benchmarks

The paper uses controlled comparisons designed to isolate four factors: representation, outcome annotation, cross-framework transfer, and retrieval difficulty. All conditions within an experiment share the same target tasks, benchmark interface, agent framework, model, execution harness, and trial budget unless otherwise stated.

For RQ1 and RQ2, the skill-vs-procedural-memory and no-hint protocols are implemented for two agent–model pairings: **Codex + GPT-5.3-Codex** and **Gemini CLI + Gemini-3.1-Pro-Preview**. RQ3 transfers workflow memories and skills constructed in the primary Codex setting to Gemini CLI with Gemini-3.1-Pro-Preview. RQ4 uses **Qwen3-Embedding-0.6B** for embedding retrieval and evaluates explicit agent selection and end-to-end execution with Gemini CLI + Gemini-3.1-Pro-Preview and Codex + GPT-5.4. Because GPT-5.3-Codex was no longer available under the same evaluation access when RQ4 was conducted, GPT-5.4 was substituted for the Codex pairing; RQ4 is therefore interpreted only through within-pairing comparisons across its three independent experiments, not direct numerical comparison with RQ1–RQ3.

The evaluation suite combines **Terminal-Bench** (Merrill et al., 2026) and **SkillsBench** (Li et al., 2026). RQ1–RQ3 use controlled subsets drawn from the public split of Terminal-Bench Pro, Terminal-Bench 2.0, and SkillsBench:

| Benchmark | Size | Notes |
|---|---|---|
| Terminal-Bench Pro | 200-task public split (from 400) | spans 8 domains |
| Terminal-Bench 2.0 | 89 terminal-agent tasks | — |
| SkillsBench | 86 tasks | 11 domains, designed for skill-based procedural reuse |

RQ4 uses SkillsBench because it provides native task–skill annotations needed for retrieval precision/recall. The benchmarks are well suited to this setting because they require multi-step execution, tool use, debugging, service management, output validation, and runtime verification, making many failures procedural rather than purely factual.

Downstream execution follows the **Harbor** standard evaluation workflow (Harbor Framework Team, 2026), with **n = 5 unique trials per task and a parallelism of 20** unless otherwise noted; retrieval-isolation arms use one query per task–pool setting because no benchmark execution is performed. Skills are placed in the agent's execution environment as reusable procedural resources rather than fully inlined into the initial context (Anthropic, 2025). For RQ4, semantic similarity scores for retrieval and distractor construction are computed with Qwen3-Embedding-0.6B (Zhang et al., 2025), a 0.6B-parameter model from the Qwen3 Embedding series.

### A.2 Dive into Skill-Use Mechanisms: Trajectory Labeling and Comparative Analysis

This pipeline answers a mechanism-level question: *when a prior-experience artifact is injected into an agent, what changes in the resulting trajectory and which failure modes are fixed or introduced?* Unlike aggregate success-rate evaluation, each agent run is treated as an executable trace: raw, workflow-memory, and skill-injected executions for the same task are aligned, an LLM judge compares trajectories using a fixed taxonomy, and paired labels are aggregated into mode-level statistics.

**Experimental arms** (Table 5). The agent is evaluated under three execution arms for each selected task:

| Arm | Injected prior experience | Purpose |
|---|---|---|
| Raw | No injected prior trajectory or skill | Baseline behavior of the agent on the task |
| Workflow memory | Cleaned prior workflows appended as procedural memory | Tests whether direct trajectory-like procedural memory improves execution |
| Skill | The same prior workflows distilled into a standardized reusable skill | Tests whether compact skill representation improves over direct workflow memory |

The workflow and skill arms are evaluated under six prior-experience compositions (mixture settings ranging from all successful to all failed trajectories), allowing the analysis to observe how the quality of the underlying experience pool changes downstream failure modes.

**Input artifacts** (Table 6):

| Artifact | Role in the analysis |
|---|---|
| Trial result metadata | Stores task identity, reward, verifier result, exception type, timestamps, token usage, execution phase durations |
| Agent trajectory transcript | Stores the terminal/tool-use trajectory and the agent's reasoning-visible interaction record |
| Task instruction | Defines the task objective and, for workflow-memory arms, may include injected workflow content |
| Skill artifact | Stores the injected skill used in the skill arm |
| Task-side files | Used only as contextual artifacts when present; taxonomy labels are based on execution trajectories and verifier outcomes |

To keep the analysis tractable, pre-processing selectively extracts only the artifacts needed (verifier results, transcripts, task instructions, injected skills, task-side configuration/solution metadata when available), reducing a large raw execution archive to a compact analysis subset. After normalization the manifest contains **8,135 trial records** (Table 7), intentionally preserving records even when auxiliary artifacts are missing; later stages filter to trials with sufficient evidence, especially an available transcript.

**Coverage statistics (Table 7):**

| Dimension | Count |
|---|---|
| Terminal-Bench 2.0 trials | 3,254 |
| Terminal-Bench-Pro trials | 2,993 |
| SkillsBench trials | 1,888 |
| Raw-arm trials | 1,883 |
| Workflow-memory trials | 2,658 |
| Skill-arm trials | 3,594 |
| Successful trials | 4,541 |
| Failed trials | 3,594 |
| Records with available agent transcript | 7,837 |
| Records with available task instruction | 6,210 |
| Skill-arm records with linked skill artifact | 3,570 |

**Manifest construction and trial normalization.** The first stage converts heterogeneous benchmark outputs into a unified trial table storing benchmark, task name, setting, arm, reward, exception type, model identifier, timestamps, token metrics, and artifact pointers. Success/failure is **derived from the verifier reward, not free-form logs**: a positive numeric verifier reward is treated as success; zero, missing, or non-positive reward as failure — keeping the taxonomy aligned with the benchmark oracle. The manifest builder also resolves the link between injected artifacts and trial outputs (workflow memory may live inside the task instruction; skill artifacts are linked by benchmark, setting, and task), because the LLM judge must see what prior-experience artifact was available, not just what the agent did. Token/duration metadata is recorded when present, but some skill-arm token fields are incomplete, so the analysis relies primarily on trajectory content, verifier outcomes, and paired mode changes.

**Open coding of individual trajectories.** Before applying a fixed taxonomy, the pipeline performs open coding over sampled trajectories to induce a vocabulary from actual execution failures rather than impose a generic one. The sampler draws from cells defined by benchmark, setting, arm, and outcome; the default configuration targets **240 trials**, with a minimum number of examples per cell and a fixed random seed. Each sampled trajectory is passed to **Claude Sonnet 4.6** through a headless CLI with tool use and session persistence disabled, reducing contamination across labeling calls and forcing judgment on prompt-internal evidence only.

The context budget is fixed before labeling: task instruction truncated to **3,000 characters**, skill artifact to **3,000 characters**, trajectory transcript to a **head of 6,000 + tail of 12,000 characters** (the larger tail reflects the observation that final errors, verifier-facing decisions, and timeout behavior concentrate near the end of the trajectory). Each LLM call has a **600-second timeout** and is **cached by trial id** so interrupted or resumed runs do not relabel completed trials. The output schema requests a short explanation, an open-ended primary mode candidate, secondary factors, evidence spans, a skill-effect judgment, and a coarse distinction among missing knowledge, misused knowledge, capability limit, and environmental failure. The open-ended `primary_mode_candidate` field is what lets the initial vocabulary emerge from the data. This stage produced **240 raw-label records, of which 238 were retained as valid unique labels** for taxonomy induction.

**Canonical taxonomy induction.** A single prompt over all open labels would be long and brittle, so the pipeline uses a **two-round batched induction**:

1. Labels are split into **batches of ~60 records**; per batch the LLM proposes a small set of canonical modes (8–14 per batch) and assigns each trajectory to exactly one. The prompt asks for specific procedural patterns, explicitly encouraging coverage of environment failures, API/library misuse, debugging loops, verification mismatches, timeout, skill-specific behavior, workflow-specific behavior, and successful execution.
2. Batch-level modes are **merged into a unified taxonomy**: the merge prompt receives only batch mode names, definitions, and counts and produces a global set of modes (9–14) plus a mapping from every batch mode to one global mode; local code then remaps individual assignments deterministically and validates that every trajectory id is assigned exactly once.

The 8–14 / 9–14 ranges are a design choice to prevent the taxonomy from collapsing into overly broad categories ("wrong answer") while avoiding a one-off-label long tail. **The final merge produced 12 canonical modes**, deliberately mixing success and failure modes: the goal is not only to classify why runs fail, but to distinguish when success is attributable to skill guidance, workflow guidance, or autonomous agent behavior.

**Paired contrastive trajectory labeling.** The main analysis stage compares trajectories matched for the same task: for each benchmark, setting, and task, the pipeline builds a **triple** containing one raw, one workflow-memory, and one skill trajectory whenever all three exist. Raw trials are matched by benchmark and task (raw has no mixture setting); workflow/skill trials by benchmark, task, and setting.

**Paired triple sample (Table 8):**

| Split | Count |
|---|---|
| SkillsBench triples | 144 |
| Terminal-Bench 2.0 triples | 186 |
| Terminal-Bench-Pro triples | 198 |
| Triples per mixture setting | 88 |
| **Total triples** | **528** |

For each arm, the judge receives the task instruction, the v1 taxonomy, the trial outcome, an excerpt of the agent trajectory, and (for the skill arm) the injected skill. The prompt asks for a structured, three-level comparison: (1) a v1 mode per arm with an evidence quote; (2) pairwise comparisons (workflow vs raw, skill vs raw, skill vs workflow), each with a natural-language summary, a categorical net effect, the modes fixed by the treatment, and the modes introduced by it; (3) a mechanism label for how the skill/workflow affected execution. Because the paired prompt must fit up to three trajectories, it uses a shorter budget: task instruction and skill truncated to 3,000 characters each; **each trajectory contributes a 4,000-character head + 8,000-character tail**.

Representative trial selection is **deterministic by default**: when multiple trials exist for the same (task, setting, arm), the first trial under stable trial-id ordering is selected (a seeded random policy is supported for sensitivity checks). The main run uses the deterministic policy for reproducibility. This paired design is the central methodological choice — it asks *what changed when the representation of prior experience changed*, supporting claims like "skill fixed environment-setup failures raw execution encountered" or "skill introduced a misapplication failure absent in raw execution."

**Oracle-status success rates (Table 9):**

| Arm | Success / total | Success rate |
|---|---|---|
| Raw | 312 / 528 | 59.1% |
| Workflow memory | 295 / 528 | 55.9% |
| Skill | 327 / 528 | 61.9% |

**Paired success-rate deltas (Table 10):**

| Comparison | Mean paired delta | 95% bootstrap CI |
|---|---|---|
| WM vs Raw | −0.0322 | [−0.0814, +0.0208] |
| Skill vs Raw | +0.0284 | [−0.0227, +0.0795] |
| Skill vs WM | +0.0606 | [+0.0076, +0.1136] |

**Deterministic aggregation and statistical reporting.** The final stage aggregates paired labels **without additional LLM calls**: per-arm success rates, paired deltas, mode frequencies, mode-level fixed/introduced counts, mechanism distributions, setting- and benchmark-level trends, and token/duration summaries. Paired deltas are computed per triple and summarized with a **1,000-iteration bootstrap CI**. The most robust difference in this sample is **skill vs direct workflow memory, not skill vs raw** — consistent with the paper's broader claim that skills work because they distill prior trajectories into a more compact, actionable form, while workflow memory can preserve too much noisy process.

**The contrastive taxonomy (Table 11)** — over 528 paired triples; percentages are computed within each arm over the same paired-triple sample. *SC* abbreviates *Skill-use Category* (SC1 = successful procedural anchoring, SC2 = execution-layer and verification failures, SC3 = invocation, applicability, and boundary failures):

| SC | Mode | Raw | WF | Skill |
|---|---|---|---|---|
| SC1 | skill_guided_success | 10.4% | 0.4% | 61.6% |
| SC1 | workflow_guided_success | 0.0% | 54.5% | 0.0% |
| SC1 | autonomous_clean_success | 48.7% | 0.8% | 0.2% |
| SC2 | environment_infrastructure_failure | 5.3% | 1.7% | 0.2% |
| SC2 | output_format_schema_mismatch | 7.4% | 3.8% | 3.2% |
| SC2 | background_service_lifecycle_failure | 2.7% | 2.5% | 0.8% |
| SC2 | shell_code_corruption | 1.1% | 1.9% | 0.2% |
| SC2 | algorithmic_logic_error | 8.3% | 11.0% | 7.4% |
| SC2 | static_verification_without_runtime | 12.5% | 12.5% | 11.7% |
| SC3 | timeout_budget_exhaustion | 1.7% | 10.6% | 4.4% |
| SC3 | skill_guidance_misapplied_or_ignored | 0.8% | 0.4% | 1.0% |
| SC3 | capability_or_safety_limit | 1.1% | 0.0% | 0.4% |

**Reproducibility and reliability controls.** The manifest uses deterministic parsing rules for benchmark/setting/arm/task/reward; sampling uses a fixed seed and stratified cells; taxonomy induction caches intermediate LLM outputs and validates every input id is assigned exactly once; the paired-comparison stage caches each task–setting comparison, supports fixed representative-trial selection, and includes a **kill switch** to avoid long runs of invalid labels under rate limits; the final report is deterministic and uses no LLM calls. The judge is constrained by strict JSON schemas and **evidence quotes**, making each mode assignment traceable to trajectory, instruction, result metadata, or skill artifact. The paired prompt also exposes the same task under multiple arms, reducing the risk that the judge attributes a failure to skill use when the same failure also appears in raw execution. Limitations: the v1 taxonomy is induced from 238 valid unique labels then applied to 528 paired triples; although trajectory grounding and taxonomy aggregation are independently human-validated (Table 3), the full paired-triple dataset remains **LLM-assisted rather than exhaustively human-coded**; the representative-trial policy selects one trajectory per arm (not an average over repeated trials); and token metrics are incomplete for some skill-arm runs, so token cost is reported only on the matched same-task intersection with complete metadata (A.9), with mechanism/mode analyses as the primary behavioral evidence.

### A.3 Paired-Trajectory Example

The appendix shows Raw, Workflow Memory, and Skill executions for the same SkillsBench task, **react-performance-debugging**, under the **1s4f** mixture setting (workflow memory: reward 0; skill: reward 1). The excerpt text itself is rendered as extracted figures in the PDF and does not survive in the text layer; the surrounding prose notes that unrelated file inspection and repeated build output are omitted.

### A.4 RQ1: Representation of Prior Experience

RQ1 asks whether representing prior experience as a standardized skill differs from injecting the same experience as direct procedural memory. Three conditions are compared: **Raw** (no prior experience), **Workflow Memory** (cleaned procedural memories from prior executions), and **Skill** (the same workflows distilled into a standardized reusable skill). The central control is that **workflow memories and skills are constructed from the same underlying trajectory pool; the only manipulated variable is how that experience is represented and made available.**

Protocol: raw terminal and tool-use trajectories are collected on Terminal-Bench 2.0, SkillsBench, and Terminal-Bench Pro under a fixed execution protocol; within each agent–model pairing the benchmark interface, task definition, model, agent scaffold, and trial budget are constant, instantiated for Codex + GPT-5.3-Codex and Gemini CLI + Gemini-3.1-Pro-Preview. Only tasks whose raw runs contain **both successful and failed trajectories** are retained, and collection continues until each selected task has a balanced trajectory pool with sufficient successful and failed runs for controlled recomposition. This shared pool is the common source for all Workflow Memory and Skill conditions. Workflow memories are built by cleaning and structuring trajectories while preserving procedural flow; skills by distilling the same workflows into a standardized **SKILL.md**. Under a fixed experience budget, the composition of successful and failed trajectories is systematically varied and the tasks rerun under all three conditions, reporting primarily task success rate and token/context cost.

### A.5 RQ2: Outcome Annotation and No-Hint Ablation

RQ2 asks whether skills' benefits come from the underlying experience itself or from explicitly exposing success/failure outcomes. Starting from the same selected tasks and balanced pools as RQ1, the authors construct **standard** and **no-hint** Skill variants: in the standard setting, success/failure identities remain visible to the skill creator; in the no-hint setting, explicit outcome annotations are removed while the underlying trajectories, task pool, experience budget, and execution protocol remain unchanged. The no-hint variant withholds outcome annotations from the skill-construction stage while keeping the same workflow content and standardized skill format; the same tasks are rerun under matched conditions, comparing success rate and token/context cost. This separates the effect of experience content from the effect of explicit outcome annotation during construction.

### A.6 RQ3: Cross-Framework Transfer

RQ3 evaluates whether reusable procedural knowledge is tied to the framework that produced it. Workflow memories and skills are constructed from trajectories collected with **Codex + GPT-5.3-Codex**, then evaluated with those fixed artifacts under **Gemini CLI + Gemini-3.1-Pro-Preview**. Target tasks and source experience are held fixed while the agent framework changes in prompting style, tool interface, and execution loop. Transferred Workflow Memory and Skill are compared against the Gemini raw baseline across the same trajectory-mixture settings; since both artifacts originate from the same Codex trajectories, differences between them reflect how directly preserved workflow traces and distilled skills survive the framework shift. Portability is thus operationalized as **downstream task success under a new agent framework**, not textual similarity between artifacts.

### A.7 RQ4: Skill Retrieval and Downstream Execution

RQ4 comprises **three independent experiments over matched candidate pools** (two offline diagnostics, one downstream execution) on SkillsBench, whose native ground-truth task–skill annotations let the authors compute precision, recall, and F1 without using downstream success as a circular proxy for relevance.

Metrics: for each task *t*, the ground-truth skill set *G_t* is the set of canonical skill identifiers attached by the benchmark's native annotations — never inferred from retrieval outputs, agent success, or experiment-generated skill descriptions. For query/trial *i*, *Ĝ_i* is the set of distinct skills selected by the agent or extracted by the execution-time parser; a skill counts as correct only when its canonical identifier occurs in both sets; a useful distractor not in *G_t* remains a false positive; repeated mentions count once.

- **Arm 1, embedding-based retrieval:** task instruction and each skill description are encoded with **Qwen3-Embedding-0.6B** and ranked by cosine similarity. The strict setting returns the **single nearest skill (top-1 precision)**; top-k statistics are retained in released artifacts, but the main figure reports the single-skill setting.
- **Arm 2, explicit agent selection:** each task is presented with an `available_skills` candidate pool and the agent must explicitly choose which skills to use; the downstream task is **not executed**. Isolates whether an agent can use task context + skill descriptions to choose helpful skills, without conflating selection with execution failure. Run with Gemini CLI + Gemini-3.1-Pro-Preview and Codex + GPT-5.4.
- **Arm 3, real execution:** the complete candidate pool is placed in the agent's environment and the agent runs the benchmark task **without a preselected skill**; after the run, the trajectory is parsed to identify which skills were actually inspected or invoked, and precision/recall/F1 are computed over parsed skill use together with benchmark success rate. Same pairings as Arm 2.

Precision and recall for record *i* (Eq. 1) are |Ĝ_i ∩ G_t| / |Ĝ_i| and |Ĝ_i ∩ G_t| / |G_t| (an empty predicted set gets P_i = R_i = 0). Aggregation (Eq. 2): P and R are arithmetic means of the per-record values across N valid records; F1 = 2PR/(P+R) is **recomputed from aggregated P and R**, not averaged from per-record F1. Arm 1 and Arm 2 contribute one query record per task–pool setting; Arm 3 one record per task and trial. Task success is the mean of binary verifier outcomes; cross-regime averages are computed from unrounded condition-level values and rounded to one decimal only for presentation.

**Candidate-pool construction (shared by all three experiments):** each pool contains the task's ground-truth skill set plus distractors; **pool size varies over 5, 10, 20, 50, 100**; distractors are sampled under three regimes — **random** (unrelated skills), **similar** (embedding-space near-neighbors), **dissimilar** (far-away skills). Benchmark, task set, ground truth, seed, and pool-size schedule are fixed; only the evaluation procedure and distractor composition change. The three experiments measure offline semantic identification, deliberate selection, and execution-time access under a full pool, and are **not sequential**: correct offline selection is not supplied to the execution run, and execution-time access is not a prerequisite for the diagnostics — correct selection is not guaranteed to produce successful execution, and incorrect exact-ground-truth selection is not always fatal, since related non-ground-truth skills can still provide useful procedural guidance.

### A.8 Lightweight Compact Procedural Baselines

To test whether the skill advantage can be explained by compact procedural text alone, two lightweight baselines are added on the same **26 selected Terminal-Bench-2 tasks** used in the Gemini CLI + Gemini-3.1-Pro-Preview comparison, five trials per task (130 trials):

- **short-plan**: a concise instruction-derived plan with three to five high-level steps.
- **test-first**: a workflow-derived validation template emphasizing success conditions, intermediate checks, and final verification.

Both are injected as **plain procedural text rather than reusable SKILL.md artifacts**.

**Results (Table 12):**

| Condition | Source | Success / total | Success rate |
|---|---|---|---|
| Raw | None | 65 / 130 | 50.0% |
| Short plan | Task instruction | 62 / 130 | 47.7% |
| Test-first template | Workflow | 77 / 130 | 59.2% |
| Workflow Memory | Workflow | 81 / 130 | 62.3% |
| Skill | Workflow | **103 / 130** | **79.2%** |

### A.9 Matched Token-Cost Analysis

Token usage is reported on a **matched intersection of 83 tasks** for which Raw, Workflow Memory, and Skill runs all contain usable token metadata. To avoid over-weighting tasks with more completed trials, success and token usage are first averaged within each task and representation, then averaged across tasks — keeping the task mix fixed.

**Absolute metrics on the matched 83-task intersection:**

| Representation | Success | Input | Output | Total | Δ succ. vs Raw | Cost profile |
|---|---|---|---|---|---|---|
| Raw trajectories | 64.1% | 541.5K | 14.2K | 555.7K | – | Full prior traces give broad evidence but the largest context load |
| Workflow Memory | 64.8% | 417.9K | 8.3K | 426.2K | +0.7 pp | Most token-efficient representation after cleaning trajectory noise |
| Skill | 69.6% | 511.7K | 9.8K | 521.5K | +5.5 pp | Highest success rate; lower tokens than Raw, higher than Workflow Memory |

**Pairwise trade-offs:**

| Comparison | Δ success | Δ input | Δ output | Δ total | Direction | Interpretation |
|---|---|---|---|---|---|---|
| Workflow Memory vs Raw | +0.7 pp | −123.6K | −5.9K | −129.5K | cheaper | Substantially reduces token cost with nearly unchanged success |
| Skill vs Raw | +5.5 pp | −29.8K | −4.4K | −34.2K | better and cheaper | Improves success while still reducing token use relative to Raw |
| Skill vs Workflow Memory | +4.8 pp | +93.8K | +1.5K | +95.3K | better but costlier | Trades additional context for stronger execution performance |

(Token counts are per-task averages in thousands; "pp" = percentage points; equal task weighting on the 83-task intersection.) The upshot is an **effectiveness–efficiency trade-off**: Workflow Memory is the most token-efficient representation; Skill is not uniformly cheaper than Workflow Memory but achieves the highest success rate — improving over Raw while reducing token usage, and trading additional context relative to Workflow Memory for stronger execution. The authors interpret Skill as the more **effective** representation and Workflow Memory as the more **token-efficient** one.

## Prompts (Appendix B)

Appendix B of the paper lists four prompt templates by name and role:

| Section | Prompt | Role |
|---|---|---|
| B.1 | **skill-creator.md** ("Experiment 1") — *Skill Creator Prompt* | Constructs the standardized Skill (SKILL.md) from the injected prior-experience pool, with success/failure outcome identities visible to the creator (the "normal" ablation arm of RQ2) |
| B.2 | **skill-creator-no-hint.md** ("Experiment 2") | Same construction pipeline with explicit outcome annotations withheld from the skill-construction stage (the "no-hint" ablation arm of RQ2) |
| B.3 | **Trajectory Labeling Prompt** | The open-coding / paired contrastive labeling prompt used with Claude Sonnet 4.6 (head/tail truncation budgets, fixed 600-second timeout, trial-id caching, strict JSON output schema with evidence quotes) |
| B.3 | **Taxonomy Merge Prompt** | The second-round prompt that merges batch-level mode names/definitions/counts (8–14 per batch) into the global 9–14 global mode set that became the 12-mode canonical taxonomy |

**Note on verbatim text:** in the PDF extraction from which this chunk was drawn, each of these four prompt bodies appears as extracted figure/table images rather than as text — the page contains only the section headers ("B.1 skill-creator.md (Experiment 1)", "B.2 skill-creator-no-hint.md (Experiment 2)", "Trajectory Labeling Prompt", "Taxonomy Merge Prompt") followed by empty content regions (pages 24–26 of the paper). The verbatim prompt text therefore does not survive the text layer, and no prompt body can be quoted here beyond the above names, roles, and the parameterized usage details documented in Appendix A.2 (truncation budgets, tool-use/session-persistence constraints, output schema fields, timeout and caching behavior).

## Complete Results (Appendix C)

The chunk also carries the paper's Appendix C, "Complete Results for Skill Retrieval and Outcome Annotation Ablation," with the full per-pool-size tables that the main text summarizes.

**Table 14 — Complete Arm 1 embedding-retrieval results on SkillsBench** (ranking metrics from Qwen3-Embedding-0.6B on task–skill-description similarity; Top-5 omitted for *k* = 5 because it covers the full pool; P = precision, R = recall, F1):

| Distractor | Pool k | Top-1 P | Top-1 R | Top-1 F1 | Top-3 P | Top-3 R | Top-3 F1 | Top-5 P | Top-5 R | Top-5 F1 |
|---|---|---|---|---|---|---|---|---|---|---|
| Random | 5 | 97.7 | 33.0 | 98.9 | 49.4 | – | – | – | – | – |
| Random | 10 | 95.5 | 32.6 | 97.7 | 48.9 | 19.5 | 97.7 | 32.6 | | |
| Random | 20 | 95.5 | 32.2 | 96.6 | 48.3 | 19.5 | 97.7 | 32.6 | | |
| Random | 50 | 92.0 | 32.2 | 96.6 | 48.3 | 19.5 | 97.7 | 32.6 | | |
| Random | 100 | 84.1 | 30.7 | 92.0 | 46.0 | 19.1 | 95.5 | 31.8 | | |
| Similar | 5 | 70.5 | 31.8 | 95.5 | 47.7 | – | – | – | – | – |
| Similar | 10 | 63.6 | 29.2 | 87.5 | 43.8 | 19.3 | 96.6 | 32.2 | | |
| Similar | 20 | 60.2 | 26.9 | 80.7 | 40.3 | 17.5 | 87.5 | 29.2 | | |
| Similar | 50 | 56.8 | 24.2 | 72.7 | 36.4 | 16.4 | 81.8 | 27.3 | | |
| Similar | 100 | 53.4 | 22.7 | 68.2 | 34.1 | 15.7 | 78.4 | 26.1 | | |
| Dissimilar | 5 | 96.6 | 33.0 | 98.9 | 49.4 | – | – | – | – | – |
| Dissimilar | 10 | 96.6 | 32.2 | 96.6 | 48.3 | 19.8 | 98.9 | 33.0 | | |
| Dissimilar | 20 | 96.6 | 32.2 | 96.6 | 48.3 | 19.5 | 97.7 | 32.6 | | |
| Dissimilar | 50 | 94.3 | 32.2 | 96.6 | 48.3 | 19.5 | 97.7 | 32.6 | | |
| Dissimilar | 100 | 93.2 | 32.2 | 96.6 | 48.3 | 19.3 | 96.6 | 32.2 | | |

**Table 15** ("Complete Arm 2 and Arm 3 retrieval results on SkillsBench") is present in the extraction but its data cells did not survive the PDF→text conversion: row/column headers (Agent/Model, pool *k*, and P/R/F1/Succ. columns) are followed by empty cells. Its caption: rows correspond to agent–model, distractor regime, and pool size; Arm 2 reports explicit-selection precision, recall, and F1; Arm 3 reports parsed actual-use precision, recall, F1, and downstream success; dashes indicate excluded entries.

**Table 16 — Complete numerical results for the outcome-annotation ablation** (downstream success for skills constructed under the indicated trajectory mixture; *normal* exposes source-trajectory outcomes during construction, *no-hint* withholds them; Terminal-Bench-Pro entries use 130 trials per condition, with missing or infrastructure-error trials counted as failures):

| Agent + Model | Benchmark | Creator | 5s0f | 4s1f | 3s2f | 2s3f | 1s4f | 0s5f |
|---|---|---|---|---|---|---|---|---|
| Codex GPT-5.3-Codex | TB2 | normal | 0.7548 | 0.7290 | 0.7806 | 0.6839 | 0.7097 | 0.5161 |
| Codex GPT-5.3-Codex | TB2 | no-hint | 0.7677 | 0.7355 | 0.5871 | 0.4968 | 0.5548 | 0.3871 |
| Gemini CLI Gemini-3.1-Pro-Preview | SB | normal | 0.7250 | 0.6167 | 0.6250 | 0.7083 | 0.6167 | 0.4500 |
| Gemini CLI Gemini-3.1-Pro-Preview | SB | no-hint | 0.6667 | 0.6417 | 0.5583 | 0.5000 | 0.5083 | 0.3500 |
| Codex GPT-5.3-Codex | TB-Pro | normal | 0.7455 | 0.7939 | 0.7333 | 0.6667 | 0.5818 | 0.4303 |
| Codex GPT-5.3-Codex | TB-Pro | no-hint | 0.8364 | 0.6606 | 0.5758 | 0.5152 | 0.4848 | 0.3758 |
| Gemini CLI Gemini-3.1-Pro-Preview | TB2 | normal | 0.7923 | 0.7615 | 0.7462 | 0.7000 | 0.6923 | 0.4769 |
| Gemini CLI Gemini-3.1-Pro-Preview | TB2 | no-hint | 0.4231 | 0.4923 | 0.4000 | 0.3692 | 0.5231 | 0.4308 |
| Codex GPT-5.3-Codex | SB | normal | 0.7429 | 0.6190 | 0.6667 | 0.6762 | 0.6000 | 0.4095 |
| Codex GPT-5.3-Codex | SB | no-hint | 0.6190 | 0.5143 | 0.4095 | 0.4190 | 0.4095 | 0.4000 |
| Gemini CLI Gemini-3.1-Pro-Preview | TB-Pro | normal | 0.6692 | 0.6308 | 0.5462 | 0.5077 | 0.5692 | 0.4615 |
| Gemini CLI Gemini-3.1-Pro-Preview | TB-Pro | no-hint | 0.6154 | 0.5769 | 0.6385 | 0.5923 | 0.5692 | 0.5154 |

Note: the extraction does not indicate which agent–model pairing each TB-Pro/SB row belongs to beyond the row ordering; where the pairing was unattributable in the source cells, it is listed in the order they appear (TB2 rows first under each pairing, then SB, then TB-Pro).

**Covers:** Appendix A (Implementation Details), Appendix B (Prompts), and Appendix C (Complete Results — Tables 14–16) of arXiv 2608.14036
