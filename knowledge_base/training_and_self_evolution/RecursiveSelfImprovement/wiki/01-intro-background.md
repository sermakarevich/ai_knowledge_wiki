> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Intro, HCI problems, RSI concept

**In one sentence:** Frontier-model scaling has shifted the bottleneck from raw model size to the costly human-coordinated improvement pipeline, so the paper defines recursive self-improvement (RSI) as an autonomous closed loop that retains validated self-changes and reuses them to improve future improvement, motivated by uneven Headroom-Closed Index (HCI) progress where interactive agentic domains lag far behind math/science.

## Key points
- Frontier scale is extreme yet bottlenecked by humans: Kimi K3 (2.8T params) and Qwen3.8-Max (2.4T) with ~1M-token context, and GPT-5.6 development saw 100× internal coding inference and 22× agentic token use, but developers must still decide what to improve, build resources, and validate each change.
- Three development burdens motivate RSI: resource-intensive foundation training (e.g. GPT-5.6 Sol >15% token-gen gain after hundreds of experiments; GDPval 1,320 tasks / ~9,240 expert-hours; Humanity's Last Exam 70,000 attempts → 13,000 reviews → 3,000 questions), costly feedback environments (DeepSeek-V3.2 post-training >10% of pretraining; NVIDIA AIMO-2 3.2M + 1.7M solutions, 540,000 problems), and recurring post-deployment adaptation (agentic workloads 4× tokens, 15× for multi-agent; FBDetect thousands of regressions/week, ~10 engineer-hours each).
- RSI is defined verbatim as the capability to autonomously transform acquired experience and feedback into persistent self-changes (parameters, harnesses, improvement policies) such that these changes affect the mechanisms for generating, evaluating, selecting, and consolidating subsequent improvements, aiming at capability frontier, efficiency, or novel strategies.
- Two lifecycle cases separate RSI from one-off optimization: A-Evolve-Training consolidates post-training outcomes into a revisable research policy (30B Nemotron external score 0.80 → 0.86 over four autonomous rounds vs 0.87 top human), and Ouroboros revises the coding agent itself (tools, context, prompts, implementation) under tests plus human review.
- HCI analysis over 393 model-benchmark observations (2023–Sep 2026, 10 domains) shows uneven progress: by 2026 advanced math 86.4 and graduate science 85.8 vs software engineering 52.6, search/terminal agents 56.8, tool agents 39.9, cybersecurity agents 91.9 — leaving the largest remaining headroom (and illustrative RSI value) in interactive stateful tool-using workflows.
- Credible RSI must pass three checks: safe inheritance (Gödel Agent: 14% of 100 MGSM trials ended below the initial policy), autonomy attribution (Darwin Gödel Machine 20% → 50% on SWE-bench subset but archive/parent-selection stayed fixed), and reliable verification (random-seed cherry-picking, test-label extraction; Red Queen Gödel Machine freezes evaluators per epoch with a ground-truth anchor).
- The survey's unit of analysis is the full improvement loop organized into five autonomy levels — L1 execution, L2 strategy, L3 experience acquisition, L4 environment adaptation, L5 recursive inheritance — applied across four feedback regimes (science, embodied intelligence, software engineering, healthcare) plus industrial practice, and distinguished from continual learning, AutoML, and agentic AI by mechanism revision plus reuse.

---

## 1. Introduction

Recent frontier development shows scaling in both models and the improvement pipeline:

- Kimi K3 and Qwen3.8-Max: 2.8T and 2.4T parameters, each ~1M-token context window.
- Six months before GPT-5.6: share of research compute for internal coding inference grew 100-fold, internal agentic token use grew 22-fold, average daily output tokens per active researcher exceeded 2× the GPT-5.5 peak.

Scale accumulates across training runs, model-assisted experiments, inference, evaluation, and human validation.

## 1.1 Scaling burdens — three development challenges

Despite agentic tools and API automation, developers must still determine what to improve, construct resources, and establish whether each change works. Three lifecycle challenges:

- **Challenge 1: Resource-intensive foundation-model training.** Kimi K3 activates 16 of 896 experts (~2.5× scaling efficiency over Kimi K2); Qwen3.8-Max activates 95B of 2.4T params. Sparse activation helps per-token cost but training still couples routing, parallelism, multimodal integration, long-context optimization, and systems design. GPT-5.6 Sol designed/ran hundreds of speculative-decoding experiments through hardware failures, gaining >15% token-generation efficiency. Data quality: GDPval 1,320 professional tasks ≈ 9,240 expert-hours, contributors averaging >14 years experience; Humanity's Last Exam >70,000 attempts → ~13,000 questions to expert review → 3,000-question benchmark. Architecture search stays expensive; AgentNAS uses an LLM for seed architecture plus search space but selection still needs combinatorial search under an external objective.
- **Challenge 2: Scaling feedback and learning environments.** Synthetic data and RL automate capability development but demand experience-generation infrastructure plus reliable evaluation/retention. DeepSeek-V3.2 post-training budget exceeds 10% of pretraining cost. NVIDIA AIMO-2: 3.2M long-reasoning solutions + 1.7M tool-integrated solutions + 540,000 curated problems.
- **Challenge 3: Recurring adaptation after deployment.** Deployed systems face changing documents, unfamiliar tools, incomplete context, interdependent workflows; engineers manually diagnose, revise retrieval/tools/state, and repeat regression testing per release. Anthropic: agentic workloads ≈ 4× tokens of chat, ≈ 15× for multi-agent systems. Meta FBDetect: thousands of infrastructure regressions per week; one regression diagnosis ≈ 10 engineer-hours.

## 1.2 From development burden to RSI

Burdens arise because improvement remains a sequence of costly, externally coordinated interventions. RSI asks whether part of that coordination can become a persistent capability of the system itself.

Verbatim working definition (Sec. 1.2):

> "recursive self-improvement (RSI) as an autonomous, closed-loop process in which an AI system identifies its own limitations, develops and validates improvements, and uses the resulting capabilities to improve the improvement process itself."

Three evolution dimensions: **autonomy** (from executing prescribed updates to identifying limitations, extracting experience, proposing/validating/retaining successors), **efficiency** (more validated improvement per data/compute/review/rework), **innovation** (search beyond human-prescribed strategies, feeding discoveries into later rounds). RSI targets both task performance and the mechanisms by which later improvements are discovered and implemented — not a single algorithm or one-off result.

- **Case 1: Foundation-model training.** Conventional loop selects a better checkpoint but leaves experiment-selection unchanged. A-Evolve-Training consolidates post-training outcomes into a persistent research policy + discovery log revised by a meta-agent; when dev scores diverged from external gains it redirected toward data rebalancing and checkpoint selection. Four autonomous rounds on a 30B Nemotron: external score 0.80 → 0.86 vs 0.87 top human submission.
- **Case 2: Software-engineering adaptation.** Repairing a repo changes the product but may leave the agent's recurring failures untouched. Ouroboros uses reviewed deployment evidence to propose versioned changes to the agent's tools, context assembly, prompts, and core implementation; candidates pass tests + human review before replacing the runtime.

## 1.3 Challenges for RSI

Persistence can carry errors or obscure control. Three recurring problems:

- **Safe inheritance.** Persistence ≠ sustained gains. Gödel Agent rewrites task policy + improvement logic, yet 14% of 100 MGSM trials ended below initial-policy performance. Needed: transfer tests, version histories, rollback.
- **Autonomy attribution.** Better candidates ≠ improved discovery. Darwin Gödel Machine evolved coding agents 20% → 50% on its SWE-bench subset, but archive maintenance and parent-selection stayed outside self-modification. Must separate AI-controlled decisions from fixed search + human acceptance.
- **Reliable verification.** Repeated evaluator access rewards exploitation: random-seed cherry-picking, attempted test-label extraction via evaluator queries. Red Queen Gödel Machine freezes evaluators within each epoch, validates replacements against an independent ground-truth anchor. Needed: protected evaluation, matched compute budgets.

## 1.4 An autonomy-centered framework (L1–L5)

Separates what the AI changes from which improvement decisions it controls: where the loop closes, what is retained, which decisions stay human. Figure 1 maps systems; Figure 2 shows loop patterns (gray dashed = human-controlled, green dashed = inside RSI loop, orange = newly internalized).

- **L1 Improvement Execution Autonomy.** Humans specify what, how, and success; AI executes candidates. Example: FineWeb-Edu applies human-defined educational-quality labels across a web corpus.
- **L2 Improvement Strategy Autonomy.** Objective, task boundary, and evaluation fixed externally; AI diagnoses weaknesses and decides how to improve. Example: Self-Harness proposes/tests harness edits from execution traces under a fixed benchmark + promotion rule.
- **L3 Learning-Signal / Experience-Acquisition Autonomy.** System also determines experience needed for the next round. Example: SIMA 2 generates practice tasks targeting observed skill weaknesses.
- **L4 Environment Adaptation Autonomy.** Deployment interaction revises persistent state under external acceptance/governance. Example: PANDO admits/demotes reusable rules during long-running interaction based on outcomes.
- **L5 Recursive Inheritance Autonomy.** System persistently revises a mechanism governing subsequent improvement (improver, verifier, successor-generation). Example: A-Evolve-Training revises its research policy after dev/external divergence and directs the next training round with it.

## 1.5 Application domains (S1–S4)

Same loop structure, different feedback regimes (cost/reliability of validation):

- **S1 RSI for Science.** Open-ended exploration, costly experiments, uncertain failure attribution. Focus: hypothesis modules, experimental agents, reflection/improvement mechanisms; do changes support later research beyond the current result?
- **S2 RSI for Embodied Intelligence.** Experience from own actions; failures from interacting perception/planning/control; costly, hard-to-repeat physical trials. Focus: environments/curricula, skills/harnesses, policies/action models, world models/evaluators; validated reusable improvements.
- **S3 RSI for Software Engineering.** Artifact and agent both executably modifiable and testable. Focus: agent implementations/harnesses, development experience/collaboration, the improvement process itself. Key distinction: improves current task vs ability to produce stronger successors vs both.
- **S4 RSI for Healthcare.** Restricted trial-and-error, delayed heterogeneous feedback, population/institution-dependent validity. Focus: clinical memory/knowledge, reasoning strategies, tools/workflows under explicit validation and oversight.

## 1.6 Industrial evidence

Frontier loops often appear first in technical reports, engineering blogs, open-source systems, model docs, and deployed infrastructure — not academic papers. These reveal evaluation pipelines, data flywheels, harnesses, automated experimentation, and deployment feedback under real cost/feedback/human-involvement constraints. Figure 16 (literature by autonomy level and target) and Table 12 (industrial landscape) summarize; analysis distinguishes demonstrated mechanisms from unvalidated recursive visions.

## 1.7 Differences from existing surveys

Four distinctions:

- **Improvement loop as unit of analysis.** Prior surveys organize by evolution stages, update objects, timing, or mechanisms; this survey traces the complete loop — trigger, proposer, validator, what persists, which later decisions use the retained change.
- **Responsibility as autonomy criterion.** Not model capability or count of automated components, but which improvement decisions moved from designers to AI: execution, strategy selection, experience acquisition, environmental adaptation, recursive inheritance.
- **Separate evidence for recursion and performance.** Higher task scores alone do not prove a mechanism was revised, retained, reused. Distinguishes structural recursion (revised mechanism governs a later round) from effective recursion (it produces stronger successors under comparable budgets + independent evaluation).
- **Mechanisms compared across operating conditions.** Same loop questions across science, embodied, software, healthcare, and industry reveal dependence on cheap executable feedback vs repeated interaction vs expert review vs production infrastructure.

## 2. Background and preliminaries

Empirical motivation (uneven HCI progress), operational vocabulary (loop anatomy + RSI definition + neighboring paradigms), and evidentiary scope (academic + industrial sources).

## 2.1 Uneven capability progress (HCI)

Figure 3 plots 393 eligible model-benchmark observations across 10 domains (2023–Sep 2026), each line an annual domain frontier in HCI (Headroom-Closed Index; 0 = entry-year frontier, 100 = perfect score). Dashed cybersecurity segments mark Cybench subset / pass@1 changes. Post-2026 hatched region is illustrative RSI extension.

Method:

- Protocol-link families: same family only if benchmark version + harness stable or overlapping models bridge protocols. Admitted 17 of 33 latest-model-audit results; 16 excluded from trajectories (Terminal-Bench, DeepSWE, CyberGym, ExploitBench, AutomationBench, BrowseComp) but kept as audit records.
- Weighted consensus for same model/benchmark-family/variant/mode (Eq. 1): base weights 3 (benchmark-owner tables), 2.5 (independent common-harness), 2 (combined reports), 1 (model-author tables); first-party values × 0.75.
- HCI normalization (Eq. 2): `H_mbh = 100 × (s̄_mbh − F_b,0) / (100 − F_b,0)`, where `F_b,0` is the 90th-percentile score in the benchmark's entry year.
- Domain trajectory (Eq. 3): `T_d,y = Σ √(n_b,y)·Q_b,y / Σ √(n_b,y)`, with `Q_b,y` the 90th-percentile HCI frontier per benchmark-year and `n_b,y` the contributing model count (square-root weighting).

Three observations:

- **Observation 1: Gains differ in magnitude and timing.** 2026 HCI: advanced math 86.4, graduate science 85.8, broad knowledge 77.2, legal reasoning 64.5, multimodal reasoning 62.2, frontier academic breadth 60.4. Annual increments vary: broad knowledge +32.8/+26.9/+17.6 (steady but slowing); legal +48.2 (2024) → +11.4 → +4.9; math +32.8 (2025) → +53.6 (2026); multimodal +59.7 (2025) → +2.5 (2026). One aggregate benchmark hides this.
- **Observation 2: Interactive capabilities retain larger gaps.** 2026 HCI: software engineering 52.6, search/terminal agents 56.8, tool agents 39.9 (8.2 → 39.9 in 2026 but still lowest) vs graduate science 85.8 — gaps of 33.2, 29.1, 45.9 points. Cybersecurity-agent leader 91.9 (52.0 points above tool agents; caution: changed Cybench subsets/aggregation). Bounded evaluations exercise mainly L1–L2; environment tasks need L2–L3; interactive workflows expose L3–L4 verification, memory, adaptation needs (planning, state tracking, tool selection, revision; errors propagate across trajectories).
- **Observation 3: Remaining headroom concentrates RSI value.** Illustrative endpoint (Eq. 4): `R_d = 100 − 0.22·(100 − T_d,2026)`, i.e. gain `R_d − T_d,2026 = 0.78·(100 − T_d,2026)`. Cybersecurity 91.9 → 98.2; software engineering 52.6 → 89.6; search/terminal 56.8 → 90.5; tool agents 39.9 → 86.8. Hypothesis: repeated experience generation, validation, retention, and regression testing direct more improvement at weak deployment workflows (practice from weaknesses, trajectory-distilled rules/tools, retained harness/code changes).

## 2.2 Conceptual foundations

Predecessors: self-modifying programs, Gödel Machine, AutoML, meta-learning, continual learning, open-ended learning, code/prompt/tool-modifying agents. But automated optimization ≠ self-improvement, persistent learning ≠ autonomy over learning, and AI-generated external artifacts ≠ self-modification. Hence the improvement loop is the unit of analysis.

### 2.2.1 Anatomy of an improvement loop

Verbatim core: "an improvement loop as a recurring process in which an AI system uses experience to propose a modification to a target, evaluates the candidate under an acceptance rule, retains an accepted change in its state, and begins the next round from that updated state."

Components:

- **AI system:** complete entity whose capability state is tracked across cycles (acts, generates modifications, carries results forward).
- **System state:** what is retained at round end and inherited next round (e.g. accepted faster program).
- **Experience:** earlier-interaction information guiding a later modification (test failure, environment outcome, reviewer correction).
- **Target:** object directly modified this round (e.g. sorting function; later the candidate-generation method itself).
- **Improver:** mechanism turning current state + experience into candidates (e.g. model reading code + failure proposing next patch).
- **Strategy:** improver's search/generation method (e.g. prioritize failed-test locations); retainable, hence a future target.
- **Verifier:** evaluates candidates under the acceptance rule (benchmarks, unit tests, reward models, environment outcomes, human feedback, formal/safety constraints, or combinations).
- **Improvement:** candidate passing acceptance, retained, entering next state (accepted + inherited change).
- **Successor:** system inheriting accepted improvements into the next round (e.g. retaining a revised code-search strategy).

Three cross-cutting questions: where does the loop close? what is updated and inherited? which decisions remain external?

### 2.2.2 Definition of RSI (verbatim)

> "recursive self-improvement (RSI) as the capability of an intelligent system, through continued interaction with tasks, environments, or other intelligent agents, to autonomously transform acquired experience and feedback into persistent changes to itself across interaction rounds (e.g., model parameters, agent harnesses, or improvement policies), such that these changes can further affect the mechanisms used to generate, evaluate, select, and consolidate subsequent self-improvements. The improved system is consequently reintroduced into the next round of interaction and improvement with an already changed capability state, allowing the system's capacity for improvement itself to become part of an ongoing recursive process."

Aims: (1) expanding capability frontier, (2) increasing resource efficiency, (3) discovering novel solutions beyond human-prescribed strategies. Industry echoes: OpenAI (automating research workflows/feedback loops), Tencent (early RSI loop feeding experimental results into later development), Alibaba/Liu et al. (improvement mechanism itself modifiable), Anthropic Institute (strongest form: AI autonomously designing/developing its successor).

### 2.2.3 Relation to neighboring paradigms

All automate parts of a loop; differ in target, retained state, and externally fixed decisions.

- **Continual learning:** acquires knowledge across task sequences while limiting forgetting (pre-training, instruction tuning, alignment, replay, parameter-efficient updates, memory). Objective, update rule, schedule, and acceptance usually designer-fixed. Approaches RSI when experience also revises how later adaptations are proposed, evaluated, or consolidated, with reuse.
- **AutoML:** automates data processing, model/architecture selection, hyperparameters, pipelines; LLM agents extend to full pipelines (AutoML-Agent) and agent/workflow search (ADAS, AFlow, AgentSquare); MLE-bench / AI Scientist-v2 evaluate sustained engineering/research. Search spaces, objectives, budgets, evaluators generally pre-supplied. Reaches RSI boundary when search/evaluation procedure becomes persistent improvable state.
- **Agentic AI/ML:** plans multistep work, calls tools, runs experiments, coordinates components, revises intermediate artifacts (MLE-bench, PaperBench, AI Scientist-v2; ADAS/AFlow build the performing agent). May operate within a fixed harness/tools/stopping/acceptance episode. Approaches RSI when validated agent-system changes persist across tasks and affect later improvement generation/selection.

Table 1 — RSI vs neighbors (✓ core, ∘ supporting, × out of scope):

| Characteristic | Continual learning | AutoML | Agentic AI/ML | RSI |
|---|---|---|---|---|
| Cross-round learning | ✓ | ∘ | ∘ | ✓ |
| Persistent retention | ✓ | ∘ | ∘ | ✓ |
| System self-modification | ✓ | ∘ | × | ✓ |
| Candidate proposal | × | ✓ | ✓ | ✓ |
| Update validation | ∘ | ✓ | ∘ | ✓ |
| Successor re-entry | ✓ | × | × | ✓ |
| Mechanism revision | × | ∘ | × | ✓ |
| Mechanism reuse | × | × | ∘ | ✓ |

RSI's distinctive question: whether a persistent improvement loop has formed around the system itself, and how much authority over that loop has become endogenous.

## 2.3 Scope of evidence

Academic-only scope would omit frontier loops first documented in technical/research reports, engineering blogs, open-source repos, model docs, GitHub/Hugging Face releases, and leaderboard/competition records — which expose loop organization, retained artifacts, model-evaluator-tool interaction, and whether a mechanism operates beyond one experiment. Included when they give concrete loop structure/operation evidence, while keeping demonstrated vs inferred mechanisms distinct.

**Covers:** sections 1-2
