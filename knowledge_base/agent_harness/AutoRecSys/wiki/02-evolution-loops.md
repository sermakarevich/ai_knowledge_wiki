> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Execution and idea evolution loops + persistence

**In one sentence:** AutoRecSys scales industry-scale recommender research by pairing an Execution Evolution Loop that distills operational know-how into evolving per-model playbooks with an Idea Evolution Loop that runs a parallel portfolio of architecture-grounded ideas, both backed by a centralized persistent memory store with recovery.

## Key points
- Each model gets a playbook — a human-readable procedural recipe (markdown) plus a machine-readable iteration metadata file — capturing six categories: key files/classes, config-flag discipline, exact validation command and expected output, submission recipe, dead ends, and proven strategies.
- Playbooks evolve by text-space skill optimization: every agent action is logged as a session trajectory, then distilled into dead-end avoidance instructions ("DO NOT" directives), numbered pipeline recipes, and crystallized submission configuration; 31 session transcripts validated that LLMs consume this natural-language form effectively.
- Playbook lifecycle runs interactive bootstrap then evolve: human-guided first iteration, semi-supervised middle iterations with falling failure rates, then reliable autonomous mode; one-shot transfer reuses the first mature playbook's structure as a template so each new model only fills in its own files, flags, commands, and recipes.
- Dead-end recording enables self-healing without manual rules: e.g. defaulting away from an unstable GPU generation, pinning a compatible package layer version, and auto-looking-up the latest valid warm-start checkpoint after an expiry.
- Ideation is grounded in a persistent model context (architecture, task heads, feature inventory, enabled modules) to avoid re-reading thousands of lines per session; candidates come from researcher proposals, external literature mining, and autonomous brainstorming (embeddings, gating, auxiliary losses), then are filtered against experiment history and ranked by metric impact, complexity, regression risk, and novelty.
- Long training feedback (hours to days) is handled by a distributed portfolio: each idea has its own state file, all ideas on a model share one baseline with aligned date ranges for fair A/B comparison, and a global registry prevents conflicts — raising throughput to multiple experiments per week while the researcher manages a portfolio instead of one serial run.
- Persistence is a centralized cross-server memory store with code-guarded structured state (registry, per-idea active/completed JSON, baselines, append-only JSONL experiment history, backlog, playbooks, per-idea markdown, knowledge base, session trajectories) plus a dashboard, append-only corruption isolation, and a recovery protocol that reconstructs context and polls training jobs for seamless multi-server handoff.

---

## 4. Execution Evolution Loop

Addresses Challenge 2 (system complexity and robustness) by building an evolving institutional memory per model. The abstraction is the **playbook**: a per-model pair of files — human-readable procedural recipe + machine-readable iteration metadata.

### 4.1 Why playbooks are necessary at industry scale

Small-scale research operational knowledge is trivial (run script, check loss, repeat). At industry scale it is the bottleneck: a single experiment requires knowing which files hold the config dataclass, encoder, and task heads; flag naming conventions and insertion points; the exact validation command and its successful output; which GPU generation is stable; which package layer versions are compatible with the current revision; which resource entitlements and scheduling tags a training job needs; and which warm-start checkpoint is current and valid. A human accumulates this over weeks; AutoRecSys captures it after one or two interactive iterations and reuses it in all subsequent iterations, including autonomous ones.

### 4.2 Playbook structure

Six categories of operational knowledge:

| # | Category | Contents |
|---|----------|----------|
| 1 | Key files | Config, model, and trainer files with important classes/functions |
| 2 | Config-flag discipline | Naming conventions, guard patterns, insertion points |
| 3 | Validation command | Exact command plus expected successful output |
| 4 | Submission recipe | Hardware type, resource entitlements, scheduling tags, package layer versions, warm-start checkpoint config |
| 5 | Dead ends (scar tissue) | Past errors with root causes and fixes |
| 6 | Proven strategies (muscle memory) | Execution patterns that consistently succeed |

### 4.3 Playbook evolution as text-space skill optimization

Analogous to text-space optimization (Yang et al., 2026; Lee et al., 2026): every agent action during an iteration is logged as a step in the session trajectory; on completion the trajectory is analyzed and distilled into natural-language playbook updates. Three kinds distilled:

- **Dead ends:** error pattern + root cause + successful fix, written as explicit avoidance instructions (e.g. "the runtime batch object exposes a feature under an internal field name that differs from its raw data-warehouse column name"). Pairing error with remedy enables self-heal.
- **Pipeline recipes:** step-by-step procedures for implementing, validating, training, and analyzing — which files to read, commands to run, parameters to set — distilled from successful trajectories.
- **Submission configuration:** infrastructure parameters learned by trial and error (hardware type, entitlements, package version, scheduling tags), thereafter consumed automatically.

Design insight from 31 agent session transcripts: LLM agents consume procedural knowledge effectively as natural language. The playbook is a markdown document read at session start; dead ends are "DO NOT" directives, pipeline steps are numbered procedures. This interface drives the execution improvements in Section 7.

### 4.4 Playbook lifecycle and one-shot transfer across models

**One-shot bootstrap, then evolve:**
1. First interactive iteration — human points to code, notebooks, training configs; system summarizes into initial playbook; error recovery still needs human guidance.
2. Next several iterations — system loads playbook at session start, follows proven patterns; dead ends accumulate, failure rates fall, human reviews at checkpoints but intervenes less.
3. Mature playbook — pipeline recipes stable, submission config crystallized, dead-end catalog comprehensive; autonomous mode reliable, pausing only for the asynchronous training wait.

**One-shot transfer across models:** the structure learned on the first model (categories of operational knowledge and their organization) is model-agnostic even though contents are not. Onboarding a later model is still interactive on its first run, but instead of rediscovering the structure the system reuses the first model's mature playbook as a template and fills its slots with the new model's key files, config conventions, validation command, submission recipe, and likely dead ends. Each transferred playbook then evolves independently.

Together: per-model complexity is handled by capturing model-specific knowledge, and cross-model scale is handled by transferring structure so every new model starts from a proven scaffold.

### 4.5 Self-healing through dead end avoidance

When an error occurs, both the error and its fix are recorded; a later similar pattern applies the known fix automatically instead of escalating. Examples: defaulting to a more stable GPU generation after recurring hardware job failures; recording and reusing the compatible package layer version after a mismatch; looking up the latest valid checkpoint on its own after hitting an expiry. No manual rule authoring — emerges from dead-end recording plus the agent's ability to follow natural-language fix instructions. Because each entry records why and how-fixed, not just that-it-occurred, the system reasons about causes instead of symptoms.

## 5. Idea Evolution Loop

### 5.1 Ideation grounded in model architecture

Centralized memory maintains a model context: model architecture, task heads, feature inventory, enabled modules, among others. Two benefits: correctness amid complex non-obvious component interactions, and token efficiency — reusing memorized context and refreshing only changed parts instead of re-reading thousands of lines of code/config each session, freeing token budget for ideation.

Candidate sources (cf. Figure 1):
- Researcher proposals (e.g. a design document describing a change to evaluate).
- External literature mining (adapting recent-paper techniques to the model at hand).
- Autonomous brainstorming from the model knowledge base (architecture gaps + common patterns such as embedding strategies, gating mechanisms, auxiliary losses applied to unexploited signals, missing component interactions, underutilized modules).

All candidates pass through one pipeline: filter against experiment history (what worked, failed, how to avoid repeats, how to build on partial successes), then rank by expected metric impact, implementation complexity, regression risk, and novelty vs. prior experiments.

Every idea is specified concretely — testable hypothesis, knowledge-base references, target files to modify, etc. This makes each idea directly actionable for the execution agent and supports human oversight: resource-intensive experiments are recorded in organized human-readable markdown for expert review before training resources are committed.

### 5.2 Parallel idea execution: the distributed portfolio

Hours-to-days training makes serial iteration impractical. Multiple ideas run in parallel as a distributed experiment portfolio (cf. Figure 3): simultaneous ideas at different lifecycle stages synchronized through the centralized memory store, preserving shared learning and centralized oversight despite multi-day cycles.

- Each idea maintains its own state file — no contention between parallel ideas.
- All ideas on the same model share a common baseline with aligned training date ranges — fair A/B comparison.
- Global registry tracks which agent session works on which idea — prevents conflicts, feeds a unified dashboard view.

Throughput effect: each experiment still takes days, but the system processes multiple experiments per week; the researcher shifts from executing one idea at a time to managing a concurrent portfolio.

### 5.3 Learning from outcomes

On experiment completion, analysis computes performance deltas vs. baseline and assigns a verdict: positive, neutral, or negative. Verdict plus structured lessons learned is appended to the model's experiment history — an append-only log, the long-term memory of the Idea Evolution Loop. Later ideation queries this history to deduplicate tried ideas, combine partial successes into stronger compound ideas (e.g. pairing two independently helpful features), prune consistently failing categories, and target unexplored regions.

## 6. Persistence and robustness

Robustness is a hard requirement: one agent session may consume large token counts, one training job hundreds of GPU-hours. Losing a failed experiment's context or repeating a known-broken configuration wastes productive exploration. Hence a dedicated persistence architecture.

### 6.1 Centralized memory store

All system state lives on a centralized memory store accessible from each development server: automatic cross-server sync, human-readable state files (JSON/JSONL), natural backup via storage-provider infrastructure.

Storage layout (per-model, per-idea isolation):

```text
state/
  registry.json                 # Global: active ideas across servers
  <model>/
    active/<idea>.json          # In-flight idea state (mutable)
    completed/<idea>.json       # Archived (read-only)
    baselines.json              # Shared baselines with lifecycle
    experiment_history.jsonl    # Append-only log
    idea_backlog.json           # Ranked queue
  playbooks/
    <model>.md                  # Human-readable recipe
    <model>_meta.json           # Iteration metadata
  ideas/
    <model>/<idea>.md           # Per-idea details
  knowledge_base/
    <model>/feature.md
    <model>/arch.md             # Model-specific knowledge
  sessions/
    index.json                  # Session -> model/idea lookup
    <session_id>.jsonl          # Trajectory backup
```

Reliability rule: code is the harness for operationally sensitive state. Deterministic scripts read/write registry, per-idea state files, and history through fixed-schema structured formats rather than letting the LLM edit freely — precision where exactness matters, vs. natural-language playbooks and knowledge base where the agent reasons.

Observability: machine-readable state renders directly into a centralized dashboard — every model, every in-flight idea and its state, every training job across servers — turning multi-day distributed portfolio oversight into straightforward monitoring.

Loss guards: experiment history is append-only JSONL (each line independently parseable, one corrupt entry cannot affect others); every agent action is logged to a session trajectory file so a new session, possibly on another server, can reconstruct prior work — the primary post-failure recovery mechanism.

### 6.2 Session recovery and multi-server handoff

On start, the orchestrator runs a recovery protocol: read the global registry to discover every active idea across servers; read each active idea's state file for the target model; if the current session id differs from the one on record, read the previous session's trajectory log to reconstruct context; for any idea in training state, immediately poll the remote job; present a concise summary and route to the next action.

This enables seamless handoff: start an experiment on one server, submit training, close the session, resume analysis on another server the next day — the system detects the change, reads the trajectory, polls the completed job, and continues analysis without the researcher recalling prior steps.

**Covers:** sections 4-6
