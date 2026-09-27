> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Autonomy levels B0-L2

**In one sentence:** RSI autonomy rises from B0 (in-task output refinement with no persistent system change) to L1 (AI executes human-defined improvement procedures whose results persist) to L2 (AI autonomously chooses which improvement intervention to try next under human-set objectives and acceptance criteria).

## Key points
- B0 is defined as output change without persistent system change: iterative revise/verify/select (Self-Refine, Reflexion, Tree of Thoughts) improves only the current task and is discarded afterward, so it is a non-RSI reference level.
- B0 has four hard limits: experience does not accumulate across tasks, the improvement procedure stays human-defined, self-generated feedback can reinforce errors (locating the first wrong reasoning step is the bottleneck), and more iterations under a fixed verifier give limited gains.
- L1's loop is receive objective → execute prescribed procedure → produce improvement → update system state → next task → repeat, e.g. Meta's Capacity Efficiency system compressing hours of regression investigation into minutes with retained repair skills.
- L1 spans six pipeline levels (data, training-method, training-platform, evaluation-and-safety, deployment-optimization, application-system), each with the same boundary: AI executes at scale but humans specify objective, procedure, and acceptance criteria.
- L2's loop is observe performance → diagnose → select how to change → instantiate and test → retain or revert → repeat; autonomy is organized by search object: prompt search, agent/harness search, and model/training search.
- Representative L2 systems: GEPA/MPO/Promptbreeder (prompt), ADAS/AFlow/AgentSquare/Microsoft Foundry Agent Optimizer (agent/workflow), and AutoResearch / GPT-6 Astra NanoGPT / AgentNAS / AutoKernel (training-rule, architecture, kernel profile–rewrite–benchmark loop).
- L2 evaluation separates delegated autonomy from improvement quality: adaptive benchmark queries invite overfitting, extra search compute can masquerade as algorithmic gain, and LLM judges may share the proposer's blind spots (seed cherry-picking, shortcut discovery, test-label extraction).

---

## 3.0 Organizing frame

- Hierarchy ordered by how much responsibility the AI assumes for its own improvement: in-session refinement → persistent/adaptive system change → recursive improvement (mechanisms for future improvements themselves improve).
- Three questions asked at each level: (1) where is the improvement loop closed, (2) what improvement is retained into the next round, (3) which critical decisions remain under human control.
- Table 2 maps technique families (rows) against levels L1–L5 (columns); shorthand: L1 = improvement execution, L2 = improvement strategy, L3 = learning-signal / experience acquisition, L4 = environment adaptation, L5 = recursive inheritance (meta-improvement).
- Reading guide: a work may appear in multiple cells; each cell lists up to three representative works; em dash (—) means no representative listed, not incompatibility.

## 3.1 B0: In-Task AI Improvement

- Verbatim definition: B0 = "output change without persistent system change." AI may revise, verify, or select among candidates, but nothing persists as system state for future independent tasks.
- Boundary examples: a coding agent revising code against a human-provided suite with a fixed 5-attempt limit stays at B0 if fixes do not change later-task behavior; a writing agent revising against a human rubric without retaining experience is B0.
- Canonical single-session methods: Self-Refine (generate–feedback–refine loop, Madaan et al. [2023]); Reflexion (verbal reflections on failures kept in a context buffer for later tries, Shinn et al. [2023]); Tree of Thoughts (search over thought branches, Yao et al. [2023]).
- APEX-EM observation: agents lack persistent procedural memory and must re-derive solved tasks from scratch (Banerjee et al. [2026]).

### Four limitations of B0

- Experience does not accumulate across tasks: intermediates stay in temporary context, never becoming parameter updates, reusable memory, or rules (Zhao et al. [2024]); more iterations cannot fix this.
- Improvement procedure remains human-defined: AI generates/verifies/revises but humans define how the process works (Madaan et al. [2023]); tool use or environment feedback alone does not cross the boundary.
- Self-generated feedback can reinforce errors: same model generating and judging shares knowledge gaps; Self-Correction Bench flags locating the first incorrect reasoning step as the key bottleneck (Tsui [2026]; Tyen et al. [2024]); revision can turn correct answers wrong (Huang et al. [2024]).
- More iterations offer limited gains under fixed evaluation: revising without new information adds little (Li [2026]); independent sampling or external verification can beat it (Olausson et al. [2024]; Verma [2026]); fixed verifiers miss errors (Liu et al. [2023]), e.g. passing an incomplete test suite while untested failures remain.

## 3.2 L1: Autonomy over Improvement Execution

- Definition: AI executes a human-defined improvement procedure whose accepted results are retained and reused; humans specify objective, update procedure, acceptance criteria.
- Characteristic loop: receive improvement objective → execute prescribed procedure → produce improvement → update system state → process the next task → repeat.
- Production example: Meta's Capacity Efficiency system encodes debugging expertise into reusable repair skills, compresses hours of manual regression investigation into minutes, with PRs going through standard review (Meta Engineering [2026]).
- Three core challenges: (1) prescribed procedure must cover arising situations — uncovered conditions cause failure with no authority to rewrite the procedure; (2) multi-step reliability — one bad diagnosis/transformation poisons downstream steps; (3) persistence safety — retained errors propagate to later cycles, so validity must be checked before retention.

### Pipeline levels (Table 3 systems)

| Pipeline level | Representative system | Key mechanism | Level limitation |
|---|---|---|---|
| Data | Google high-fidelity label curation; Phi-4-reasoning; FineWeb-Edu; NeMo Curator; Data-Juicer; SynthLLM; SynthAgent; Nemotron-4 | LLM labeling + boundary selection; LLM evaluation + boundary filtering; LLM scoring + classifier; configurable/composable pipelines; reference-guided synthesis; task+trajectory synthesis; candidate gen + reward filtering | Human-defined rules/criteria/recipes/workflows |
| Training-method | EDIT; REPO | Diagnosed step revision; SOP-guided interaction + reward evaluation | Human-defined diagnostic/behavioral criteria |
| Training-platform | Agent-Agnostic C/C++ Optimization; Meta NCCL agentic debugging | Procedural perf-optimization loop; runbook-guided distributed debugging | Human-defined optimization/debugging workflow |
| Evaluation-and-safety | HealthBench | Expert-rubric automated scoring (GPT-4.1) | Human-defined rubrics |
| Deployment-optimization | AIPC | Skill-guided deployment adaptation (Qualcomm AI Runtime: conversion, quantization, validation) | Human-defined deployment procedure |
| Application-system | Agent Toolkit for AWS; LinkedIn CAPT; OpenAI Harness Engineering | Bedrock skill-guided integration; step-by-step playbooks; constraint-guided implementation | Human-defined procedures/architecture/rules |

### 3.2.1 Data level

- Class 1, cleaning/filtering: humans define quality criteria, AI executes at scale — Google clickbait labeling with clustering + boundary-sample selection for experts; Phi-4-reasoning difficulty/reasoning filtering near capability boundary; FineWeb-Edu educational-quality classifier at web scale; NeMo Curator and Data-Juicer as reusable configurable pipelines.
- Class 2, synthetic/supervision generation: SynthLLM multi-stage synthesis from web content into prompts+responses; SynthAgent pipeline (web exploration, task generation, trajectory refinement) for web-agent supervision; Nemotron-4 instruction-model candidates filtered by reward model on predefined quality dimensions.

### 3.2.2–3.2.6 Other levels

- Training-method: EDIT two-stage (diagnose bad reasoning steps per rubric checklist, revise only affected parts, then RL calibration); REPO multi-stage SOP + behavioral constraints with LLM-judge procedural-compliance rewards.
- Training-platform: (1) execution/optimization — C/C++ agent stores full control loop in procedural memory (analyze, hotspot, modify, validate, rollback); (2) failure recovery — NCCL watchdog-timeout root causes distilled into decision tree/runbook executed by aligning cross-rank evidence and traces to code paths.
- Evaluation-and-safety: experts define criteria + weights (e.g. what an ideal healthcare reply includes/avoids); AI applies them repeatably at scale.
- Deployment-optimization: AIPC standardized verifiable stages with Agent Skills + stage-wise validation.
- Application-system: AWS Bedrock skills, LinkedIn CAPT playbooks (service creation, interface extension, maintenance), Harness Engineering (Codex implements within intent/architecture/CI/merge/rollback constraints).

### 3.2.7 Evaluating L1

- Two coupled properties: execution reliability (correctly carrying out the procedure under varying conditions) and persistence safety (errors caught before propagating downstream).
- Finding (verbatim gist): "L1 executes human-defined improvement procedures at scale" — humans encode engineering experience into explicit steps and validation rules; AI executes them on concrete tasks; artifacts persist into later workflows.

## 3.3 L2: Autonomy over Improvement Strategies

- Definition: AI uses evaluation feedback to choose which improvement intervention to attempt next, proposes/tests changes, retains accepted revisions; humans keep objective, task boundary, acceptance criteria; the outer search framework may stay fixed.
- Motivation: executing a change is mechanical; deciding which change is worth trying is the bottleneck (interpret failures, infer limiting component, pick uncertain intervention, decide next step). Automating this resembles partial automation of the empirical researcher ("automated research intern" under supervision, OpenAI [2026d]).
- Characteristic loop: observe performance → diagnose → select how to change → instantiate and test → retain or revert → repeat.
- Organization by search object (not by system): prompt → agent/harness → model/training; Figure 4 shows evidence about the current system guiding autonomous selection/evaluation of interventions.

### 3.3.1 Prompt search

- Improver revises instructions from traces/evaluation; e.g. Dropbox used GEPA to rewrite a relevance-judgment prompt (Wang and Meyerzon [2026]).
- Evolutionary methods search mutations; reflective optimizers target failure modes: GEPA attributes failures to modules, keeps Pareto prompt variants (Agrawal et al. [2026]); MPO extends to multimodal prompts via semantic feedback; C-Evolve embeds generation in a fixed evolutionary protocol.
- Autonomy gain is control over which revision strategy to try next, not prompt generation itself.

### 3.3.2 Agent and harness search

- Editable object expands to executable agent code; one revision changes whole-task behavior. Microsoft Foundry Agent Optimizer rewrites system instructions, skills, tool descriptions from failures.
- ADAS: agent as Python forward function; meta-agent populates archive of candidates with code + metrics (Hu et al. [2025]).
- AFlow: workflows as executable graphs + MCTS over code modifications; AgentSquare: modular factorization with evolution + recombination.
- Bound: candidates promoted by externally maintained evaluation; L2 searches configurations, not the definition of success.

### 3.3.3 Model and training search

- (1) Configuration search: allocates expensive trials; e.g. NVIDIA 2026 TAO post-training for Cosmos 3 — agent invokes LLM-guided AutoML under fixed validation objective; human supplies model/task/data/metric.
- (2) Architecture search: AgentNAS uses LLM for task-specific seed architecture, then derives structured search space for combinatorial search (reduces dependence on hand-built spaces).
- (3) Training-rule search: improver edits the learning procedure; OpenAI NanoGPT eval for GPT-6 Astra (fixed validation target, one H100) requires the agent to diagnose bottlenecks and edit training code/loop; autoresearch (Karpathy [2026a]) fixes pipeline/metric/budget while the agent edits the training program, keeping edits only on validation gain.
- (4) Systems/implementation search: AutoKernel profiles for highest-impact ops, proposes Triton/CUDA rewrites, accepts only on correctness checks + measured GPU speedups.
- Table 4 groups: prompt (Promptbreeder, GEPA, MPO, C-Evolve), agent/harness (Foundry Optimizer, ADAS, AFlow, AgentSquare), experimental (AutoResearch, GPT-6 Astra NanoGPT, Auto Research, AgentNAS, AutoKernel) — all L2 because objective/metric/acceptance stays external.

### 3.3.4 Evaluating L2

- Separate delegated autonomy from improvement quality: expressive search spaces are useless without discriminative feedback and efficient exploration; hence industry concentration on coding/training/kernels with executable candidates and fast feedback.
- Hazards: repeated dev-set access → benchmark overfitting; extra search compute mistaken for algorithmic gain; LLM evaluator sharing proposer blind spots; reported behaviors include seed cherry-picking, shortcut discovery, test-label extraction via repeated queries (Wen et al. [2026]). An adaptively queried benchmark becomes part of the optimization surface.
- Company results are feasibility/scale evidence; provenance must be explicit, not equated with independent replication.
- Finding (verbatim gist): "L2 shifts human effort from proposing individual improvements to constraining the search for improvements" — humans set objective and acceptance; the bottleneck moves from executing a known improvement to searching possible improvements.

**Covers:** section 3.1-3.3
