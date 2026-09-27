> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Industry landscape, challenges, conclusion

**In one sentence:** Six industrial case studies (Theseus, Lark, Humanlaya, ModelBest, Tencent Hunyuan Hyra, Agent-Native Research Lab) show environment–data–model co-evolution, data-quality loops, and human-gated automation delivering large measured gains, yet sustained recursive self-improvement (RSI, meaning AI systems that iteratively improve themselves) still requires solving eight open problems in diagnosis, experience acquisition, state reuse, governed adaptation, trustworthy meta-improvement, long-horizon evaluation, resource accounting, and reproducible infrastructure.

## Key points

- Theseus demonstrates that workspace/environment quality bounds agent performance: a clean workspace beats a noise-laden one by 21.7–51.6 percentage points across eight frontier model–harness configurations, and a reconstructed environment (Collection Map + Event Log) raises rubric scores by 18.65–39.67 pp across five fixed pairings.
- Lark treats enterprise collaboration data as an evolving RSI substrate: its knowledge-graph pipeline lifts human-rated usability from 52% to 65% (automated: 47% to 56%) over a RAG (retrieval-augmented generation) baseline, and its automated evaluator reaches ~84% agreement with humans (stricter on disagreements), with explicit failure attribution driving fixes.
- Humanlaya implements a delivery-driven two-loop RSI for data quality (inner repair loop + outer system-update loop): four feedback-driven updates (V0→V4) cut key-defect packages from 9.0% to 3.7% on 600 held-out packages and cut human handling time from 48 to 27 minutes per task.
- ModelBest's Forge Engineering automates AI engineering from an empty codebase: ForgeTrain matched Megatron-LM v0.15 on H100 in ~8 hours and reportedly surpassed it in 1.5–2.5 days (vs. 3–5 engineers for 6–12 months), raising MFU (model FLOPs utilization) from 40.1% to 44.1% (0.5B) and 47.0% to 50.9% (8B); ForgeStencil reports 1.15–1.9× kernel speedups (median 1.41× end-to-end).
- Tencent Hunyuan's Hyra uses an Experience Bank of executable traces (code, logs, scores, evaluator feedback) plus evaluator self-revision: it reports 0.9015 vs. 0.9109 validation BPB (bits per byte, lower is better) on NanoChat AutoResearch, 76.4 s vs. 77.5 s on NanoGPT Speedrun, and 0.771 vs. 0.754 mean SOL (speedup over baseline, higher is better) on SOL-ExecBench.
- Agent-Native Research Lab argues RSI needs verifiable infrastructure, not just agents: its Agent-Native Research Artifact (ARA) raises QA accuracy over prior work from 72.4% to 93.7% and RE-Bench reproduction from 57.4% to 64.4%, and on Chip-Bench reports a Level-3 CPU score of 5.8416 — 2.7% faster and 21.5% smaller than standard-agent baselines (97 directed tests + 350 differential programs passed).
- The survey distills eight future directions — cross-component diagnosis, learner-conditioned experience acquisition, persistent-state management, governed domain adaptation, trustworthy evolution of improvement mechanisms, long-horizon evaluation of improvement capacity, resource-aware improvement with human collaboration, and reproducible cross-round infrastructure — all converging on one criterion: inherited changes must demonstrably help later rounds improve faster under explicit resource and authority constraints.

---

## 5.1 Theseus: Environment–Data–Model Co-Evolution

**Premise.** Environments make knowledge accessible and actions verifiable; task execution produces evidence for learning; improved models expand explorable problems. Each round should contribute reusable capabilities to the next, making real-world practice a continuing source of intelligence growth.

**Four-stage loop (Figure 10):**

1. Convert refinement experience into environment-refinement tasks to train an environment-refinement model.
2. Agents use reconstructed environments to identify genuine task-solving difficulties and generate targeted training data.
3. These data train the task model.
4. The stronger model supports further environment iteration and more task generation.

Successive rounds yield both new task-training data and new environment-refinement experience, linking progress in solving tasks to progress in constructing conditions for future learning.

**Early workspace-stage evidence (30 workspace tasks adapted from Workspace-Bench):**

| Study | Setup | Result |
|---|---|---|
| Clean-vs-noise pilot (Table 9a): 8 frontier model–harness configs, 1,280 rubrics | Clean vs. noise-laden workspace | Clean wins by +21.7 to +51.6 pp in every configuration (e.g. DeepSeek-V4-Pro +51.6 pp: 98.2% vs. 46.6%; GPT-5.6-Luna +46.5 pp: 84.6% vs. 38.1%; smallest gain Grok-4.6 +21.7 pp) |
| Productivity study (Table 9b): 5 fixed harness–model pairings, 547 rubrics | Bare workspace vs. reconstructed environment (Collection Map + Event Log) | Reconstructed wins by +18.65 to +39.67 pp (best: PI + GPT-5.6-Sol +39.67 pp, 50.27%→89.95%, 23/2/5 task W/D/L, 240/15 rubric flips; smallest: Claude Code + DeepSeek-V4-Flash +18.65 pp). Task-level wins dominate (22–24 wins each) but a few scope-creep regressions occur (agents change more than required) |

The team also completed a reusable file-verification module. These are first steps; successive rounds extend reconstruction, data generation, and model training into a compounding cycle.

## 5.2 Lark: Data Foundation for Enterprise RSI

**Loop (Figure 11).** Collaboration data (documents, messages, meetings, tasks) are continuously structured, evaluated, and refined into knowledge and training signals; real-world agent usage feeds new evidence back. Objective is not more data but fresh experience per iteration, reliable progress criteria, and fine-grained diagnostics. Currently human-gated: agents do repetitive processing/evaluation; humans define standards, review critical samples, approve important changes.

**Enterprise Knowledge Graph.** Links scattered sources into entities, events, people, temporal relations for cross-source reasoning. Graph errors propagate downstream, so construction is itself an iterative data-quality problem (batched construction, delegated authorization checks, continuous retrieval-ablation checks). Internal evaluation vs. RAG baseline: human-rated usability 52%→65%; automated usability 47%→56%.

**Automated Data-Quality Evaluation.** Two-stage: absolute judgments filter clearly unusable outputs, then comparative GSB (good–same–bad) evaluation decides promotion. Coupled with explicit failure attribution (e.g. temporal inconsistency, distorted queries, poor source quality), each mapping to a fix — e.g. query-time filtering blocks future information for time-sensitive questions; low-quality synthetic queries are rewritten before re-entering the pipeline. Initial evaluator: ~84% agreement with humans; most disagreements because the automated judge was stricter — a concrete calibration signal.

## 5.3 Humanlaya: Delivery-Driven RSI for Data Quality Assurance

**Setting.** Produces training/evaluation data for foundation-model developers: complex multi-file task packages (descriptions, attachments, reference answers, scoring rubrics, executable/procedural verification). Failures are subtle cross-component inconsistencies; fixing samples one by one does not scale, so the quality-control system itself (rules, prompts, few-shot examples, skills) is the persistent improvement target.

**Inner loop (data-centric, within batch).** Quality Checker (content + cross-component consistency) → Refiner (repairs confirmed defects) → Delivery Checker (formatting, structure, delivery constraints), with repeated localize–revise–reverify on failure. Example: several independently gradable results merged into one coarse rubric item → checker flags rubric as insufficiently atomic, demands restructuring. Improves the artifact, not the system.

**Outer loop (improvement-centric, across batches; the RSI mechanism, Figure 12).** After delivery, aggregate internal review, customer feedback, downstream usage → agent diagnoses recurrent causes → proposes versioned modifications (Refiner instructions, prompts, few-shots, skills) → candidates evaluated on held-out task packages not involved in producing the modification + human review → approved version promoted for subsequent batches → new tasks generate new evidence.

**Representative case.** A clear three-page scanned PDF failed extraction; the Quality Checker marked the attachment unusable, conflating extraction failure with poor document quality. Fix: new decision rule + few-shot examples distinguishing the two; incorporated after held-out validation and human review.

**Measured improvement.** Same base model, tools, budget; 600 held-out packages; V0 vs. V4 after four updates: key-defect rate 9.0%→3.7%; mean human handling time 48→27 min/task. Practical scaffold-level RSI with human oversight (humans supply partial ground truth, review, final approval) rather than an unconstrained loop.

## 5.4 ModelBest: Zero-Human Industrial AI Engineering

**Forge Engineering (Figure 13).** Premise: AI engineering becomes autonomous earlier than open-ended research because execution gives cheap objective feedback. Input: target model + hardware platform + parallelism requirements; output: production-ready implementation from an initially empty codebase. Two-level loop: within-project optimization + cross-project experience reuse.

**Within-project loop.** Humans + AI maintain a knowledge base (specs, evaluation criteria, accumulated experience). Agent sets a high-level architecture constraining the search space; an AutoResearch loop generates implementations, measures correctness/performance, diagnoses failures, repairs bottlenecks. Wins (e.g. GEMM, FlashAttention kernels) merge into the main path — stable global constraints, aggressive local optimization.

**Cross-project loop.** Successes and failures (measurements, strategies, reference implementations, failure rules) are written back to the shared base and seed later projects across models, hardware, and workloads. Reported coverage: pre-training frameworks, operator libraries, RL (reinforcement learning) infrastructure, inference engines, fine-tuning, compression, quantization, edge deployment, several hardware ecosystems.

**Measured improvement.** From empty directory + reference scripts/specs, ForgeTrain generated a pre-training framework matching Megatron-LM v0.15 on H100 in ~8 h, reportedly surpassing it in 1.5–2.5 days (manual estimate: 3–5 engineers, 6–12 months). MFU 40.1%→44.1% (MiniCPM4-0.5B) and 47.0%→50.9% (8B). ForgeStencil (scientific kernels): 1.15–1.9× over public SOTA (state of the art), median 1.41× end-to-end.

## 5.5 Tencent Hunyuan: Experience-Driven Self-Improvement (Hyra)

**Loop (Figure 14).** Lightweight philosophy: broad solution space + repeated experimental evidence rather than elaborate hand-designed workflows. Task → explore until self-termination or budget exhaustion → return best solution found.

**Experience Bank + agents.** Bank retains rich state: solution code, artifacts, execution logs, scores, evaluator feedback. A Context Agent recombines evidence into diverse inspiration contexts; multiple Proposal Agents asynchronously consume contexts, build solutions, execute in fresh isolated sandboxes; outcomes are written back for reuse/combination/avoidance by later proposals.

**Evaluator self-revision.** For open-ended tasks with incomplete/exploitable evaluators, accumulated search experience revises the evaluation mechanism itself (finer granularity, stronger baselines, closed reward-hacking loopholes) before search continues — the persistent update is a better judge, not just a better solution.

**Measured improvement (Table 10, Recursive vs. hyra-1.0):**

| Benchmark | Task | Metric | Recursive | hyra-1.0 |
|---|---|---|---|---|
| NanoChat AutoResearch | Model training | Validation BPB ↓ | 0.9109 | 0.9015 |
| NanoGPT Speedrun | Training acceleration | Time to 3.28 loss ↓ | 77.5 s | 76.4 s |
| SOL-ExecBench | GPU kernel optimization | Mean SOL ↑ | 0.754 | 0.771 |

Takeaway: retain executable experience, not just final answers.

## 5.6 Agent-Native Research Lab: Verifiable Infrastructure

**Claim.** Sustained RSI needs infrastructure for recording, verifying, inheriting, and reusing research experience across generations (Figure 15: guided exploration + deterministic verification + knowledge inheritance + next-generation learning).

**(1) Agent-Native Research Artifact (ARA).** Conventional papers discard what successor agents need (failed experiments, intermediate evidence, executable specs, implementation details), weakening cross-generation accumulation. ARA jointly preserves scientific logic, executable code/specs, exploration graph (successful + abandoned branches), and raw evidence. Reported: QA accuracy over prior work 93.7% (ARA) vs. 72.4% (papers); RE-Bench reproduction 64.4% vs. 57.4%. Contribution is a richer inheritance substrate.

**(2) Deterministic verification (rit protocol).** At machine-speed generation, verification is the bottleneck. Empirical claims are anchored to execution traces (results re-extracted from logs); analytical claims checked via formal systems such as Lean 4. Only passing claims enter shared research state, blocking hallucinated results from recursive amplification. Sparse outcome rewards are augmented with epistemic-progress guidance and structured priors from human scientific reasoning (prefer uncertainty-reducing experiments over naive hill-climbing on familiar parameters).

**Silicon-design instantiation.** Agents generate synthesizable SystemVerilog, testbenches, microarchitectural modifications; industrial EDA (electronic design automation) tools evaluate synthesis, place-and-route, timing, formal equivalence. Invalid designs filtered automatically; verified implementations, traces, failed branches, superior PPA (power-performance-area) trajectories retained. Chip-Bench Level-3 CPU score 5.8416: 2.7% faster, 21.5% smaller than standard-agent baselines on the same foundation, passing all 97 directed tests and 350 random differential programs.

## 6 Challenges and Future Directions

Three motivating bottlenecks remain only partially resolved: (a) foundation-model development needs heavy resources/coordination; (b) scalable learning needs useful experience + reliable verification; (c) deployed systems need continuing diagnosis, validation, and release effort. Autonomy, durable gains, and better improvement processes are distinct properties. Eight directions:

**1. Cross-component diagnosis and coordinated improvement.** L1→L2 exposes attribution: a wrong answer could come from data, context, tools, model, or evaluator (cf. Humanlaya's extraction-vs-quality conflation); fixes to one component can invalidate another's assumptions. Agenda: testable intervention hypotheses, controlled comparisons, selective freezing, targeted ablations, dependency records; allocate effort across data/models/harnesses/environments as constraints shift (cf. Theseus separating environment vs. task-model gains). Goal: know which intervention helps the whole system, when, and whether the knowledge transfers.

**2. Learner-conditioned experience acquisition and reliable learning signals.** L3: experience must be valid, appropriately difficult, and durably beneficial. AZR pairs executable checks with learner-dependent proposals; R-Zero uses solver consistency as a difficulty proxy — neither proves learning value. Adaptive curricula can chase ambiguity, reinforce evaluator errors, or over-concentrate on measurable regions, poisoning learner and future experience. Agenda: multi-round learning-value estimation preserving validity/diversity/coverage; decide when expensive verification is worth it; match budgets and data access in evaluation; ablate learner-conditioning (freeze acquisition input or use learner-independent schedules) to test transfer beyond extra training.

**3. Persistent-state management and reliable reuse.** L4: inheriting parameters, memories, skills, tools, harness code ≠ later benefit. Failures in activation (never retrieved) and execution (retrieved but misfollowed); Library Drift (growing libraries degrade retrieval, stall improvement) vs. over-aggressive retirement. Agenda: attach evidence, applicability conditions, dependencies, observed effects to artifacts; admission tests (e.g. HDSO paired evaluations) plus continuing revalidation as tasks/executors/systems drift; separately measure update quality, activation, faithful use, downstream benefit; decide merge/revise/retire/revalidate; study cross-model reuse (author-useful ≠ executor-useful).

**4. Governed adaptation under domain-specific feedback.** Each regime needs different validation: science (hypothesis vs. protocol vs. instrument; retain assumptions/uncertainty), embodied AI (policy shapes observations; physical trials costly/irreversible), software (tests conditional on spec/coverage), healthcare (delayed, confounded outcomes; poor cross-site transfer). Agenda: update policies distinguishing transient failures from recurring limits; staged validation (simulation, replay, sandbox → supervised/staged deployment); persistence monitoring under shifting requirements/populations/tools/environments; explicit human authority over consequential releases, permissions, safety. Checkpoints cannot undo physical/clinical harm — pre-release validation is essential.

**5. Trustworthy evolution of improvement mechanisms.** At L5, changing improver/evaluator/policy couples validation: stronger solvers expose evaluator flaws, but evaluator changes break score comparability and invite exploitation. RQGM's partial fix: freeze evaluator within an epoch, validate replacements against an independent anchor, revisit affected scores; Hyra's evaluator refinement raises the same credibility question. Agenda: separate editable internal feedback from independently maintained acceptance criteria; preserve mechanism-revision→decision evidence links; separately compare candidate-generation vs. evaluation changes (cf. A-Evolve-Training policy inheritance within fixed objectives — transfer beyond origin untested); detect coordinated proposer–evaluator errors; reversible harmful changes. Revising research priorities need not transfer mission authority.

**6. Long-horizon evaluation of inherited improvement capacity.** Distinguish structural L5 (mechanism inherited and invoked) from effective L5 (it produces/selects better subsequent improvements) — an empirical gap (e.g. AIDE 2's evolved harness showed no significant efficiency gain as outer improver; lineage studies show weaker variants can enable later progress). Agenda: compare original vs. revised mechanisms from matched starts under matched total budgets (including mechanism-development cost); freeze evolved mechanisms on fresh tasks to test transfer (cf. HyperAgents); report full trajectories (rejected updates, regressions, recovery, retained capabilities, resource use); protected reference tasks for comparability + fresh tasks/constraints for transfer/discovery. Establish whether gains alter improvement capacity, when they plateau, and whether acceleration survives full cost accounting.

**7. Resource-aware improvement and human collaboration.** Efficiency demands whole-process accounting: candidate generation, evaluation, infra maintenance, human review (cf. Meta's retained engineering review; Humanlaya's handling-time reporting). Stronger base models and parallelism confound strategy comparisons. Agenda: budget allocation across diagnosis, acquisition, search, verification, monitoring; cheap screening calibrated against independent outcomes; count maintenance cost of reused tools/failures; report time + total cost to validated capability plus review effort and rework; adaptive stopping (expected learning value vs. uncertainty; explicit pause/escalate/terminate conditions).

**8. Reproducible infrastructure for cross-round inheritance.** Successors need how an improvement was obtained: failed alternatives, evidence conditions. Industrial complements: Lark (temporal grounding, failure attribution), Humanlaya (versioned system updates), Hyra (executable experience), Agent-Native Lab (artifacts with code, specs, history, traces); longitudinal benefit still unproven. Agenda: artifact format linking parent state → change → evidence → eval config → acceptance → subsequent use; versioned data/environments/evaluators for replay and valid comparisons; deterministic re-extraction + formal verification (neither proves the experiment captures the intended capability); pair inspectable artifacts with replay studies; report provenance, availability, independent replication separately; for confidential data, shareable subsets + controlled replay interfaces.

**Unifying criterion.** Genuine RSI = repeated, attributable, transferable improvements in the capacity to improve: inherited changes help later rounds acquire more useful experience, discover better interventions, or validate successors more effectively under explicit resource and authority constraints.

## 7 Conclusion

The report presents an autonomy-centered RSI roadmap spanning five stages — improvement execution, strategy selection, experience acquisition, environmental adaptation, recursive meta-improvement — using the improvement loop as unit of analysis to clarify what changes, what successors inherit, and what stays human-controlled. It connects the roadmap to scientific discovery, embodied intelligence, software engineering, and healthcare, showing how feedback availability, verification cost, and deployment constraints shape each domain's path; grounds it in industrial practices and preliminary empirical results with current limitations; and calls for long-horizon evaluation of transferable gains under resource constraints and human oversight. The promise: each generation of AI makes future improvement more reliable, efficient, and conducive to novel discovery.

**Covers:** sections 5-7
