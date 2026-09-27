> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Autonomy levels L3-L5 and synthesis

**In one sentence:** L3 gives AI control over what to learn next based on its own weaknesses, L4 lets it decide what deployment experience to keep as lasting memory or skills, L5 makes the improvement procedure itself inheritable so successors reuse a revised improver or evaluator, and higher autonomy does not guarantee better results.

## Key points

- L3 is learner-conditioned future experience acquisition: the system uses current capabilities, failures, and learning history to choose the next learning experience, and the persistent update feeds back into later acquisition decisions.
- Adaptive task generation and self-play keep the curriculum on the learner's moving frontier: SSP ties proposer rewards to solver performance, AZR uses solver-dependent learnability rewards plus a code executor, R-Zero uses Challenger-Solver answer consistency, STP trains conjecturer near the prover's frontier, PSV conditions code-specification generation on solver-derived difficulty, and VisPlay guides visual questions with uncertainty plus diversity rewards.
- Autonomous practice through environment interaction links interaction feedback to future practice goals: VOYAGER couples curriculum to exploration history plus a reusable skill library, SIMA 2 ASKA focuses practice on weaker skills via reward-model evaluation, and SEAgent maintains a persistent software guidebook that conditions later tasks.
- L4 shifts autonomy from selecting experience to deciding which consequences of deployment experience persist: trajectory distillation into text, structured, procedural, or executable artifacts, iterative revision of the agent system itself, and selective retention with validation, library maintenance, and governed release.
- L4 evaluation must separate deployment autonomy from adaptation quality because accepted changes can fail by wrong lesson, wrong scope, non-activation, or forgetting; most studies cover bounded task streams with noisy or endogenous feedback.
- L5 begins when AI persistently modifies a mechanism responsible for future improvements (search procedure, successor evaluator, or research policy) and the revised mechanism governs later rounds; structural L5 (reuse demonstrated) is distinct from effective L5 (better successors under matched budgets and independent assessment).
- Cross-level synthesis: B0→L1 is persistence, L1→L2 is strategy selection, L2→L3 is control of the future learning agenda, L3→L4 is persistent deployment adaptation, L4→L5 is recursive inheritance; higher levels are more domain-dependent and end-to-end L5 evidence is concentrated in bounded prototypes.

---

## 3.4 L3: Autonomy over Future Learning Experience

### Defining property

L3 adds autonomy over what learning experience to acquire next. Whereas L2 concerns how to improve, L3 concerns the learning agenda: the system uses evidence about current capabilities, failures, and learning history to determine what it should learn from next.

Characteristic loop:

`observe learner state → choose learning experience → acquire experience → update persistent state → reshape future experience → repeat`

Defining property is learner-conditioned future experience acquisition. Requirements:

- Evidence about the evolving learner must inform which experience to select, generate, or seek next, and the persistent update must feed back into later acquisition decisions.
- May be a separate curriculum component or integrated into the agent policy. A policy update that incidentally changes visited states does not qualify.
- Experience need not be generated from scratch: selecting from an externally supplied pool counts when selection adapts to the learner in a continuing loop; one-time filtering alone does not.
- Objective, evaluator, update procedure, and selection rules may be human-designed. The test is whether learner feedback autonomously changes the next agenda without a human redesigning it each round.
- Persistent learning may live in parameters or reusable external state (memories, skills).

Figure 5 shows two realizations: adaptive task generation and self-play, and autonomous practice through environment interaction.

### 3.4.1 From Industrial Automation to Experience Autonomy

Modern training-data pipelines automate many operations but execution automation alone is not experience autonomy. From reviewed practices (Soldaini et al. [2024], AI et al. [2025], Yang et al. [2025], Abdin et al. [2024]) the chunk organizes six recurring functions:

1. data-source preparation
2. data labeling
3. data selection
4. data construction
5. data mixture and training orchestration
6. model-feedback diagnosis

These recur across pretraining, supervised fine-tuning, preference optimization, and reinforcement learning. Figure 6 places operations on a manual-led (M) → human-in-the-loop (H) → automated (A) scale as interpretive synthesis, not measured scores.

Key distinction:

- A fixed selection algorithm can still be adaptive if it uses changing learner feedback to choose subsequent experience.
- An automated pipeline that generates and filters data does not establish experience autonomy merely by producing new samples.
- Decisive evidence is a closed dependence: learner state → experience acquisition → persistent learning → later acquisition decisions.

### Representative L3 loops (Table 5)

| Method | Target | Learner-conditioned mechanism | Externally specified constraints |
|---|---|---|---|
| SSP Lu et al. [2026a] | Search agent | Solver performance shapes proposer rewards and subsequent search tasks | Reward design, training procedure |
| AZR Zhao et al. [2025] | Reasoning model | Solver-dependent learnability rewards guide executable task proposal | Task formats, code executor, update rules |
| R-Zero Huang et al. [2026a] | Reasoning model | Solver answer consistency proxy shapes Challenger tasks | Uncertainty reward, pseudo-label scheme, optimization |
| STP Dong and Ma [2025] | Theorem prover | Conjectures near current prover frontier train conjecturer | Formal domain, proof checking, training rules |
| PSV Wilf et al. [2026] | Coding model | Solver-derived difficulty labels condition specification generation | Formal verifier, difficulty scheme, training recipe |
| VisPlay He et al. [2026a] | Vision-language model | Reasoner answer consistency + diversity rewards guide visual questions | Image source, reward design, optimization |
| VOYAGER Wang et al. [2023] | Embodied agent | Agent state + exploration history guide objectives; skills persist | Minecraft interface, curriculum prompts, skill representation |
| SIMA 2 team et al. [2025] | Embodied agent | In full ASKA setup, evaluation feedback directs practice to weaker skills | Task setter, reward rubric, training procedure |
| SEAgent Sun et al. [2026c] | Computer-use agent | Trajectory feedback updates software guidebook conditioning later tasks | Software interfaces, assessment model, learning procedure |

### 3.4.2 Adaptive Task Generation and Self-Play

A fixed task distribution does not track the moving competence frontier: familiar tasks become uninformative, far-beyond tasks give little signal. Central challenges: obtain an informative signal, translate it into a useful task distribution, maintain validity.

- **SSP:** proposer rewards depend on current solver performance, so the curriculum evolves without manually redesigning each batch.
- **AZR:** single model couples proposal and solution of executable reasoning tasks; solver-dependent learnability reward guides proposal while a code executor validates tasks and checks solutions — separating evaluability from useful difficulty.
- **R-Zero:** Challenger–Solver without external answer labels; Challenger uncertainty reward depends on consistency of multiple Solver responses; a proxy for model-perceived difficulty, not correctness or future gain.
- **STP:** joint conjecturer + prover; conjectures the current prover proves only with difficulty train the conjecturer; proof assistants check correctness, learner-dependent selection picks useful difficulty.
- **PSV:** solver-derived difficulty labels prompt new code specifications; compilability and formal checks required before training; substantial overlap between realized difficulties of easy/medium/hard targets shows partial, not exact, curriculum control.
- **VisPlay:** image-conditioned Questioner + Reasoner; uncertainty reward favoring near-midpoint majority-answer confidence plus diversity penalty; as Reasoner changes, future question rewards change; signal is scalable but can reflect ambiguity as well as productive difficulty.

Shared advance: estimated learning value influences future acquisition, and persistent learning changes that estimate later. Executable/formal checks ground correctness in a setting; consistency estimates difficulty without establishing correctness.

### 3.4.3 Autonomous Practice through Environment Interaction

- **VOYAGER:** automatic curriculum + persistent library of executable Minecraft skills; current state and exploration history inform objectives; successful behaviors become reusable skills; persistence is in external skills, not necessarily language-model parameters.
- **SIMA 2:** fixed-task experiment (self-generated trajectories improve) does not alone establish task-selection autonomy; in full ASKA setup a Gemini-based task setter uses downstream reward-model evaluations to focus practice on weaker skills; autonomy belongs to the coupled system including the setter.
- **SEAgent:** World State Model supplies trajectory judgments + GUI state-change descriptions to a Curriculum Generator, which updates a persistent software guidebook and generates later tasks; Actor learns from collected experience; guidebook carries earlier exploration into later decisions.

Shared risk: unreliable skill construction, inaccurate reward judgments, or erroneous guidebook entries misdirect later effort.

### 3.4.4 Evaluating L3 Experience Autonomy

Experience autonomy and learning quality are distinct: a system may control its agenda yet acquire uninformative, narrow, or mis-evaluated experience. Assessment must establish the mechanism and its benefit: which learner signal, what persistent state changed, how that change affected a later acquisition decision.

Recommended controls:

- Freeze the acquisition mechanism's learner-state input at an earlier checkpoint, or replace adaptive decisions with a learner-independent schedule.
- Match data sources, environments, compute, and interaction budgets including generation/assessment cost; do not hold acquired samples identical (that removes the distributional adaptation under study).
- Distinguish correctness, difficulty, and learning benefit; compare acquisition signals with independent validity checks, realized difficulty, and subsequent gains; check stability as the learner changes.
- **Experience corruption:** defective experience or feedback distorts later learning and acquisition (misleading difficulty proxy, inaccurate judge, wrong persistent memory); effects can propagate across rounds through parameters, skills, memories, or curriculum state.
- Track multi-round performance, validity and diversity of acquired experience, transfer to fresh tasks/environments; separate curriculum-guiding feedback from protected generalization evaluation; watch for collapse onto narrow or easily rewarded examples, or practice stuck on familiar behaviors.

> **Finding: L3 adds autonomy over the future learning agenda.** The system uses evolving capabilities, failures, or learning history to steer which experience is selected, generated, or sought next, with persistent learning feeding back into later decisions. Human-designed objectives, evaluators, and rules may remain; experience autonomy does not guarantee useful or reliable improvement.

## 3.5 L4: Autonomy in Deployment and Environmental Adaptation

At L4, AI uses continued deployment interaction feedback to decide how the operating agent should persistently adapt. L3 centers on what experience to acquire; L4 centers on how operational experience changes memory, skills, or execution components reused in later tasks.

Characteristic loop:

`observe deployment interaction → propose persistent adaptation → revise agent components → validate and retain → reuse in later tasks → collect new feedback and repeat`

Objective, access boundaries, protected evaluation, and release authority remain externally governed. Three mechanisms: trajectory distillation, iterative revision of the agent system, selective retention and deployment (Table 6).

### 3.5.1 Trajectory distillation

Converts interaction histories into compact artifacts that persist across sessions and condition later tasks — more concise and cheaper than raw trajectories.

**Textual experience memory** (natural-language passages retrieved into prompts):

- Dynamic Cheatsheet Suzgun et al. [2026]: frozen model improves across related problems without ground-truth labels; single evolving note of strategies, snippets, pitfalls; consults then curates (add lessons, remove superseded entries).
- ACE Zhang et al. [2026d]: detailed growing memory; short entries with helps/hinders counters; small patches not full rewrites.
- ReasoningBank Ouyang et al. [2026]: learns from failures as well as successes; each judged trajectory distilled into short titled strategy retrieved before later tasks.

**Structured memory** (explicit records/graphs):

- APEX Li et al. [2026e]: strategy map as milestone graph with prerequisite links; episode outcomes propagated back; adds untried promising branches; agent chooses known-good vs untried path at planning time.
- PersonaAgent Zhang et al. [2026e] / PAHF Liang et al. [2026]: memory organized around users; persona prompts, preference entries revised via user clarification.
- MemToolAgent Er et al. [2026]: stores critiques of failed tool calls, adjusts retrieval count per call.

**Procedural skill libraries** (reusable skills/procedures followed directly):

- Trace2Skill Ni et al. [2026]: frozen-agent rollouts; error-focused and success-focused analysts propose skill edits merged into portable skill directory loaded as instructions.
- PRACTICE Bai et al. [2026]: embodied skill library with bounded consistent edits (add/refine/merge/remove); trained from oracle trajectories, failure-awareness via success/failure contrast, distilled toward stronger teacher.
- PANDO Li et al. [2026f]: online web-agent rules preventing repeated failures + parameterized routines replacing multi-step browser subgoals; confidence-scored admission/demotion.
- PILOT Xiao et al. [2026c]: supervisor distills procedures and failure modes from live long-horizon runs.

**Executable artifacts** (experience compiled into callable code):

- Metis Dai et al. [2026]: dual memory — text plans/facts/pitfalls plus code tools; reflector maintains text; reused text plan rewritten as callable tool only after sandbox compile/run checks.
- Evo-Harness Wei et al. [2026a]: whole-harness lessons from failed/negatively evaluated tasks into cross-task patterns + task-specific procedures.
- SHAPER Wang et al. [2026a]: evolves textual planning guidance plus sandboxed Python context-selection function for embodied agents.

Evaluation protocols: Evo-Memory Wei et al. [2025b] restructures datasets into sequential streams for long-horizon memory reuse; PANDO audits action repetition, step overhead, prompt-cache use; Metis relates quality to execution/construction cost.

### 3.5.2 Iterative revision of the agent system

Revises the system itself — solution skills, judging rubrics, harness, or weights — with fixed acceptance criteria.

- **Co-evolving components:** DecoEvo Chen et al. [2026a] evolves solver skill + rubric-generator skill in text space; solver updated from criterion-level rubric feedback; generator gated by score-independent structural audit (covers requirements) and contrastive audit (discriminates near-ties) with Pareto verification; generator never sees aggregate solver score so it cannot win by making rubrics easier.
- **Benchmarks of self-directed revision:** HarnessDev Wu et al. [2026a] — can models build/improve their own harness from minimal seed; frozen candidates scored on hidden tasks for success + token cost, creator/executor separated. ASPIRE Wu et al. [2026b] — vague-goal self-improvement over weights or harness with score-gated rollback unless verified score improves. S3Gym Shi et al. [2026a] — withholds verifier outcomes; compares raw history vs compressed summaries vs parameter training.
- **Analyses of revision benefit:** Harness Updating Is Not Harness Benefit Lin et al. [2026c] separates producing useful updates from exploiting them at solve time under fixed solve-evolve protocol; updating ability largely independent of base capability (small-model updates comparable to frontier); benefit varies non-monotonically with failures in activation or faithful following; invest in the solver, not just the evolver.

### 3.5.3 Selective retention and deployment of updates

Which proposed changes become persistent and stay available.

- **Candidate validation:** HDSO Shang and Yang [2026] — curator proposes hypothesis + validation plan from compact traces; each candidate tested with paired control (approved repository) vs treatment (candidate added) executions in stages of increasing size plus independent-task confirmation. Metis gates text-plan → executable-code promotion on recurrence plus dependency/compilation checks.
- **Library maintenance:** Library Drift Zhang et al. [2026f] — unbounded accumulation degrades retrieval and stalls progress before task scores show it; append-only evidence log tracks per-skill contribution, retire faded skills, cap active skills so newcomers compete, write under a meta-skill guide; over-aggressive retirement is worse than unguided. Liu et al. [2026e] — careful filtering of skill edits beats repeated rewriting from outcomes.
- **Governed deployment:** Tax AI deployment OpenAI and Thrive Holdings [2026] — production tax-preparation; practitioner corrections as structured field-level evidence; repeated failures grouped into eval targets; coding agent fixes bounded scope (extraction schema, source selection, tax-engine mapper, graders); architecture/product design stays with engineers; each fix is a pull request with targeted + regression evals and human review; unresolvable cases route back to practitioners.

### 3.5.4 Evaluating L4 Deployment Autonomy

Greater adaptation autonomy does not establish reliable improvement. Characteristic risk is persistent update failure: wrong lesson from noisy evidence, sound lesson applied outside valid scope, failure to invoke a relevant update, or new behavior displacing earlier capabilities (Suzgun et al. [2026], Zhang et al. [2026f], Liu et al. [2026e], Lin et al. [2026c]). Final scores alone cannot separate these; evaluation must connect each retained change to its evidence, later use, and effects on new and previously solved tasks.

Further limits: most evaluations cover bounded streams and few model/task/environment combinations; longer studies are costly (Ni et al. [2026], Xiao et al. [2026c], Wu et al. [2026a]); feedback may be noisy or endogenous (changing evaluators, useful artifact never activated). Evaluate adaptation across time and distribution shifts, including when a retained change alters later behavior. L4 stays bounded: agent decides how interaction evidence changes persistent state while humans specify objective, boundaries, protected evaluation, and release authority.

> **Finding: L4 shifts autonomy from selecting experience to deciding which consequences of experience persist in deployment.** The agent converts histories into retained memory, skills, harness, code, or parameter changes affecting later tasks and feedback. Humans retain objective, protected criteria, access boundaries, and final release authority.

## 3.6 L5: From Environmental Adaptation to Meta-Improvement

An improvement process can itself bottleneck: a coding agent repeating failed patches because search discards alternatives, or a research agent overfitting a development score that stopped predicting external performance. Repair requires changing the procedures directing experiments and judging outcomes — costly, since a revision must be assessed through later improvements across tasks and runs (Zelikman et al. [2024], Shi et al. [2026b]).

L5 begins when AI persistently modifies a mechanism responsible for future improvements and the revised mechanism is used in subsequent rounds. Editable mechanism: improver, successor evaluator, search policy, or research-directing procedure. L2 searches interventions; L3 sets the experience agenda; L4 adapts to deployment; L5 makes the later-improvement procedure an object of improvement. Example boundary: retaining new debugging skills via an unchanged procedure is L4; revising and reusing the failure-diagnosis/skill-building procedure can cross into L5.

Loop closes when a revised mechanism returns to govern generation, evaluation, or selection of later successors. Inherited state: accepted code, prompts, evaluators, research policy plus evidence for later revisions. Humans still set mission, protected evaluation, editable components, resource permissions, and may retain veto/deployment authority (partly via fixed infrastructure, not per-iteration approval).

Distinguish structural L5 (AI-directed change persists and controls a later round) from effective L5 (revised mechanism produces/selects better successors under comparable budgets and independent assessment). Self-modifying task code with unchanged revision process is insufficient; an evolved successor evaluator can be structural L5 even with unchanged task-agent code.

### L5 mechanisms (Table 7)

| Work | Loop closes at | Inherited state | External controls |
|---|---|---|---|
| STOP Zelikman et al. [2024] | Next program search | Improver code | Utility, base LM, budget |
| Gödel Agent Yin et al. [2025] | Next self-revision | Task + update code | Task objective, runtime access |
| DGM Zhang et al. [2026b] | Descendant search | Agent code, archive | Parent selection, benchmark |
| HyperAgents Zhang et al. [2026c] | Next agent generation | Task + meta-agent code | Main-study selection, evaluation |
| RQGM Iacob et al. [2026] | Next-epoch selection | Evaluator, agent code | Anchor, replacement schedule |
| A-Evolve-Training Shi et al. [2026b] | Next research round | Search policy, discovery log | Constitution, benchmark, substrate |
| AIRA 2 / AAR | Task experiments | Research artifacts | Research harness, evaluation |
| AIDE 2 Weco Team [2026] | Later research runs | Research-agent harness | Private scores, cost budget |

### 3.6.1 Improving the Search Procedure

- **STOP Zelikman et al. [2024]:** improver is a Python program calling a fixed language model to generate, evaluate via supplied utility, and select code; current improver receives its own source as target; successors scored by downstream-program quality; selected improver runs next round; reported fourth-generation improver beat the seed on all five held-out transfer tasks; task distribution, utility, base model, limits externally fixed; weaker-model runs regressed on average; some programs evaded soft budgets or exploited eval bugs.
- **Gödel Agent Yin et al. [2025]:** shared Python program holds task policy + recursive update logic; execution feedback drives rewrites run in the next recursive call including modified self-update; 14 of 100 MGSM trials ended below initial policy; unrestricted runs could call stronger models — objectives and permissions remain key controls.
- **DGM Zhang et al. [2026b]:** retains coding-agent variants, explores descendants; archive management and parent selection outside self-modification — lineage is a transition case; task gains alone do not prove a better procedure.
- **HyperAgents Zhang et al. [2026c]:** exposes task-agent and meta-agent code; evolved meta-agents build trackers and persistent memory; preprint meta-agents evolved on paper review/robotics improved agents for unseen math grading (procedure transfer); 200-iteration experiment showed no statistically significant final advantage for transferred initialization; parent selection and evaluation fixed.

### 3.6.2 Improving Successor Evaluation

Repeated optimization pressures judge blind spots; frozen judges invite exploitation, unrestricted revision changes standards mid-stream.

- **RQGM Iacob et al. [2026]:** evaluator frozen within an epoch; at scheduled boundary challengers compared against independent ground-truth anchor; winner governs next epoch; incompatible records discarded, affected agents re-evaluated; held-out Polyglot coding 71.7% vs 69.9% for HGM-H with lower search-token use; anchor, schedule, orchestration externally fixed; stability argument holds within frozen epochs only.

### 3.6.3 Revising Research Goals and Policies

- **A-Evolve-Training Shi et al. [2026b]:** autonomous post-training of a 30B model over four rounds; workers return recipe changes, evaluations, failures; collector consolidates; meta-agent revises next-round search policy (standing recipe, promoted/retired directions, registry of failures); when dev scores rose without external gains, revised policy targeted external improvements despite lowering the proxy; final leaderboard 0.86 vs 0.87 top human; inheritance in policy + discovery log; worker substrate and constitution fixed. Supports policy-level L5 within human-defined objective, not autonomous objective revision.
- General rule: next goal should name a testable gap, preserve established capabilities, justify cost; goal revision alone is weak evidence — must show the revised policy changed subsequent research and improved outcomes.

### 3.6.4 Industrial Practice

- **Research infrastructure:** Meta AIRA 2 Hambardzumyan et al. [2026] (async experimentation, hidden consistent evaluation); Anthropic Automated Alignment Researchers Chen et al. [2026c] (generate/test mitigations for specified alignment failures) — automate execution within researcher-designed workflows; no established inherited changes to the research procedures themselves.
- **Research-agent revision:** Weco AIDE 2 Weco Team [2026] — research agent improves a research-agent harness under private scoring + fixed cost budget; accepted versions retained; separate experiment installs evolved harness as outer improver; seven accepted improvements over 100 unattended steps plus external transfer; stronger test of faster outer search found no significant efficiency gain. Supports bounded harness improvement; reliable acceleration of successive improvers unestablished.
- Savings must account for evaluator design, failure investigation, and code maintenance; task performance or unattended runtime alone cannot quantify reduced human effort.

### 3.6.5 Evaluating L5 Recursive Improvement

Must distinguish a stronger current agent from a procedure that reliably produces stronger successors. SEA-Eval Jiang et al. [2026] and SEAGym Zheng et al. [2026a] add trajectory assessment.

Table 8 — Evaluating recursive improvement:

| Dimension | Measurements | Purpose |
|---|---|---|
| Adaptivity | Gain, improvement trajectory, time to target | Detect progress and plateaus |
| Retention | Replay loss, tasks fixed or broken | Detect displaced capabilities |
| Transfer | Held-out gains within/across domains | Test reuse beyond update tasks |
| Efficiency | Tokens, time, cost per validated gain | Account for improvement expense |
| Stability | Harmful updates, largest temporary decline | Expose unreliable trajectories |
| Meta-recursion | Mechanism reuse, successor quality; goal and stopping decisions | Test inherited improvement capacity |

Mechanism audit: identify revised artifact, record motivating evidence, verify invocation in a later round. Effectiveness: original vs revised mechanisms from comparable agents/evidence under matched budgets including mechanism-evaluation cost; hold revised mechanism fixed in transfer tests (as HyperAgents does). Goal selection: adaptive frontier tasks for next-challenge identification, protected reference tasks for comparability and forgetting/reward-hacking detection, private undisclosed-rule tasks for discovery, plus record whether the system stops when expected benefit falls below cost/risk. Current results support bounded meta-improvement with some cross-task transfer; statistically reliable accumulation across generations under comparable resources remains open (Zhang et al. [2026c], Weco Team [2026]).

> **Finding: L5 makes the improvement procedure inheritable.** The loop closes through reuse of a revised improver, evaluator, or research policy. Successors inherit that procedure and supporting evidence; humans retain overall objective, protected acceptance criteria, and resource authority.

## 3.7 Cross-Level Synthesis

Across B0–L5 the hierarchy is a progressive transfer of responsibility over the improvement loop — differing in which decisions AI internalizes, what state persists, and which acceptance conditions stay externally protected.

Compact boundaries:

- B0 → L1: **persistence** — an accepted change must survive the current task.
- L1 → L2: **strategy selection** — AI decides which intervention to attempt, not merely executes a prescribed one.
- L2 → L3: **future learning agenda** — the evolving learner influences what experience is acquired next.
- L3 → L4: **persistent deployment and environmental interaction** — changes must remain useful under changing operational conditions.
- L4 → L5: **recursive inheritance** — the mechanism for later improvement itself becomes an inherited improvement target.

Higher autonomy does not imply better improvement: delegated authority can coexist with inefficient search, unreliable feedback, regression, evaluator exploitation, or poor transfer. Scope of responsibility is separated from quality/efficiency. Evidence is broadest at lower and intermediate levels; L3–L4 remain more domain-dependent; end-to-end L5 is concentrated in bounded prototypes and emerging industrial/research systems.

**Covers:** section 3.4-3.7
