> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Overview and experiment state machine

**In one sentence:** Auto-RecSys extends autonomous research to industry-scale recommenders — where training takes days and infrastructure is fragile — via a harness with distributed asynchronous execution, centralized cross-server memory, and cognitive-procedural separation, plus dual self-evolving loops and a per-idea finite state machine.

## Key points

- Industry-scale recommenders break serial auto-research: a single model change needs days of training and a full cycle (ideation, implementation, validation, training, recovery, analysis) takes 3-7 days, so Auto-RecSys runs multiple ideas concurrently across servers and incorporates results asynchronously.
- System complexity forces recoverable execution: thousands of lines of config plus distributed infra, GPU preemption, checkpoint corruption, stale data, and session/server restarts require persistent, cross-session state and accumulated operational knowledge instead of local reruns.
- The harness has three designs: distributed asynchronous execution tracked by a persistent per-experiment state machine, centralized cross-server memory holding states/playbooks/histories/trajectories, and cognitive-procedural separation where natural-language skills guide LLM reasoning while deterministic scripts enforce state transitions and validation.
- A dual-loop self-evolving architecture improves both dimensions over time: the Execution Evolution Loop crystallizes successful pipelines into model-specific playbooks and retains failures as dead ends, while the Idea Evolution Loop feeds outcomes and conclusions into future ideation to avoid redundancy and track baseline shifts.
- Five design principles govern the system: compose over existing training/submission/version-control/monitoring infra, keep a human in the loop at 4 checkpoints (idea selection, code review, training submission, results review; skipped in autonomous mode), design async, self-evolve procedures and ideas, and treat failure as expected via atomic writes, append-only logs, trajectory logs, and a dead-end catalog.
- Knowledge is tiered in three layers: a shared model-agnostic orchestrator skill (experiment loop, transitions, baselines, analysis), per-model-type playbooks (key files, config conventions, hardware needs, dead ends, proven strategies), and per-iteration state files (commit hashes, job IDs, validation results, verdicts) — so new models onboard with only playbook bootstrapping.
- Each idea moves independently through ideating → implementing → validating → training → analyzing, with a debugging branch on training failure and a loop back to ideating; per-idea state-file isolation allows parallel stages/servers and contains GPU-hour failures, and interactive mode (pauses for approval) graduates to autonomous mode as playbook confidence grows.

---

## Abstract — problem and claimed solution

Auto-research agents can automate hypothesis generation, execution, and iterative refinement, but industry-scale recommendation models add two challenges:

1. Long feedback loops — training can take days, making serial iteration prohibitively slow and requiring parallel exploration.
2. System complexity — large configs, fragile infra dependencies, and multi-day GPU jobs require robust, recoverable execution.

Auto-RecSys answers with three harness designs (distributed async execution, centralized cross-server memory, cognitive-procedural separation) plus a dual-loop self-evolving architecture (Execution Evolution Loop + Idea Evolution Loop). Evaluated on recommendation models, it reduces human time per experiment cycle and improves execution reliability as playbooks mature.

Paper: `Auto-RecSys: Harnessing Autonomous Research Agents for Industry-Scale Recommender Systems`, arXiv:2609.10922v1 [cs.CL], 10 Sep 2026. Authors (Meta, plus UIUC affiliation for Xuying Ning): Ming Li, Dai Li, Xuying Ning, Bo Sun, Rui Li, Yi Zhang, Silvia Gong, Xuan Cao, Rui Li, Cornelia Carapcea, Qunshu Zhang, Zhigang Wang, Yinglong Xia, Xue Feng, Andy Wang.

## 1. Introduction — why industry-scale needs a different design

Prior systems (cited: Chen et al. 2025; Lu et al. 2024; Lyu et al. 2026; Karpathy 2025 AutoResearch; Analemma AI 2025 FARS) show automated research works when experiments are self-contained with feedback in minutes/hours. Industry recommenders differ: one model change may need days of training/monitoring; implementation depends on large configuration stacks, distributed infra, and long GPU jobs; a typical cycle spans ideation → implementation → validation → training → failure recovery → result analysis over 3-7 days, with substantial researcher effort spent managing execution rather than ideas.

### Two challenges

- Challenge 1: Long feedback loops require parallel exploration. Serial propose → evaluate → analyze → repeat throttles throughput at day-scale GPU cost; meaningful velocity needs multiple ideas implemented, trained, and monitored concurrently with async result incorporation.
- Challenge 2: System complexity requires robust and persistent execution. Thousands of config lines, code/infra dependencies, hardware requirements, and failures (preemption, checkpoint corruption, stale data, compatibility) plus terminating sessions, restarting servers, and migrating environments demand recoverability across sessions/servers/failures and preservation of successes, failures, and causes.

### Table 1 — small-scale vs industry-scale auto-research

| Dimension | Small-Scale Auto-Research | Industry-Scale Auto-RecSys |
|---|---|---|
| Feedback loop | Minutes to hours | Hours to days |
| Iteration strategy | Rapid serial iteration | Distributed parallel exploration |
| Computational cost | Relatively low | High |
| Failure recovery | Local reruns | Persistent recovery across sessions |
| Operational complexity | Self-contained code | Large configurations and infrastructure dependencies |
| Agent lifetime | Single continuous session | Multiple sessions, servers, and asynchronous stages |

### Three harness designs

- Distributed asynchronous execution: multiple ideas proceed concurrently across servers at different lifecycle stages; a persistent state machine tracks each experiment independently across multi-day training without a single continuous session.
- Centralized cross-server memory: experiment states, model-specific playbooks, execution histories, and session trajectories in a shared layer reachable from any dev server; a new session reconstructs context and resumes after termination/restart.
- Cognitive-procedural separation: natural-language skill files guide reasoning while deterministic scripts enforce operational correctness (state transitions, API calls, validation, file ops).

### Dual-loop self-evolving architecture (Figure 1)

- Execution Evolution Loop: distills trajectories into model-specific playbooks (relevant files, validated commands, hardware requirements, recurring failures, successful pipeline configs); failures kept as dead ends, successes crystallized into reusable workflows; reliability grows as playbooks mature.
- Idea Evolution Loop: records outcomes and scientific conclusions so future proposals use prior evidence, avoid redundancy, and adapt to baseline changes.
- Figure 1 caption (from chunk): Idea Evolution Loop feeds outcomes into proposal generation; Execution Evolution Loop distills trajectories into playbooks with validated workflows and known dead ends.

## 2. Auto-RecSys Overview — layered system

Three layers:

- Orchestration layer: drives the finite state machine, routes work to specialists.
- Specialist agent layer: one agent per lifecycle state, from ideation through analysis.
- Persistence layer: experiment state, model playbooks, experiment history in a shared memory store reachable from every dev server.

### 2.1 Design principles (five)

1. Compose rather than reinvent: thin orchestration over proven infra for distributed training, job submission, version control, metric monitoring; matters because infra churns and reliability is non-negotiable.
2. Human in the loop at decision points: interactive mode pauses at four checkpoints — idea selection, code review, training submission, results review; autonomous mode skips them; autonomy gets safer as playbook confidence grows.
3. Asynchronous by design: never assumes the same session or server survives until a multi-day job completes.
4. Self-evolving: procedures and research directions improve via structured feedback, not manual rules; operational knowledge is an appreciating asset.
5. Failure as expected and recoverable: atomic writes prevent state corruption; append-only logs preserve history; trajectory logs enable context recovery; dead-end catalog avoids repeating expensive mistakes.

### 2.2 Harness design (three patterns)

- Cognitive-Procedural Separation (ReAct; SWE-agent; Ning et al. harness duality): natural-language layer = skill files describing what to do, why, and when to escalate (LLM plans/reasons); code layer = deterministic scripts invoked as tools performing state transitions, file writes, API calls with preconditions, input validation, atomic updates. Rationale: LLM reasoning is flexible but imprecise — one wrong JSON field can corrupt a lifecycle.
- Hierarchical Knowledge Architecture (MemGPT tiered memory; Voyager skill library): general orchestrator skill (core loop, transitions, idea selection, baseline management, analysis methodology, shared across model types) → per-model-type playbook (compact natural-language skill artifact: key files, config conventions, hardware requirements, dead ends, proven strategies) → per-iteration state file (ephemeral: commit hashes, job IDs, validation results, analysis verdicts). Benefit: new models onboard fast; only the playbook needs bootstrapping via a few interactive iterations.
- Natural-Language Procedural Memory (Reflexion verbal reflections; SkillOpt portable artifacts; Meta-Harness; Lee et al.): operational knowledge (dead ends, pipeline recipes, submission configs) stored as markdown instructions read at session start; dead-end catalog = rejected-edit buffer, recipes/configs = accepted validated edits. Design validated on 31 agent session transcripts (Section 7 reference); claim: LLMs consume procedural knowledge best in the language they reason in, and full traces beat compressed scalar scores for harness evolution.

## 3. The Experiment State Machine

A finite state machine tracks each idea through: ideating → implementing → validating → training → analyzing, with a branch to debugging on training failure and a loop from analyzing back to ideating for the next iteration. Transitions enforce preconditions and trigger side effects such as recording results to experiment history on finalization and updating playbook dead ends / pipeline recipes.

### 3.1 Per-idea state isolation

Each idea keeps its own state file (not one shared mutable model state). Consequences: multiple ideas on the same model fly simultaneously at different stages and on different servers; failures are contained — an idea failing after hours of GPU time touches only its own file and never blocks or corrupts siblings.

### 3.2 Operating modes

- Interactive mode: pauses at each human checkpoint; for new models, high-risk changes, or tight control.
- Autonomous mode: runs end to end, chaining backlog ideas without pausing; toggleable at any point.
- Maturation path: moving interactive → autonomous is part of the Execution Evolution Loop — as the playbook accumulates dead-end knowledge, autonomous operation becomes increasingly reliable.

**Covers:** sections 1-3
