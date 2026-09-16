> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Problem and Related Work

**In one sentence:** Because agent failures emerge from interactions among model, harness, users, tools, memory, and environment, outcome-level failure labels are insufficient to tell you what to fix — so this paper poses a "repair-assignment problem" and argues that prior agent-failure taxonomies (benchmark-specific, module-based, or flat lists) fail to solve it because none of them names both the interaction where a failure occurred and which endpoint of that interaction is at fault.

## Key points

- The paper frames a **"repair-assignment problem"**: the same visible failure may call for model post-training, harness engineering, environment redesign, or benchmark repair depending on where it originated, and outcome-level labels alone cannot distinguish these cases.
- The canonical illustrating example: in a long-running Claude Code session, an agent may ignore an earlier user instruction either because the harness's context compaction removed it (a harness-level fix) or because the instruction remained available but the model failed to follow it (a model-level fix) — the observed behavior is identical but the required repair differs.
- The paper defines eight agent-system **components** as the vocabulary for localizing faults: Model, Owner, Grader, Third party, Context, Memory, Tool, Local env., and External env. (Table 1); in multi-agent settings a model's counterpart is further typed as **peer** or **subagent**.
- Failures are analyzed at the **interaction between two components** (the "edge"), and the component responsible for the failure is the **"fault side"** — e.g., a tool call that silently succeeds-but-failed is labeled `TOOL — MODEL · fault: TOOL` if the wrapper suppressed the error, versus `TOOL — MODEL · fault: MODEL` if the wrapper reported the error but the model ignored it.
- The taxonomy comprises **41 failure modes**, each assigned to an interaction edge and a fault side; most modes are model-side because the paper's attribution rule assigns fault to the model whenever a more capable model could have avoided or recovered from the failure under the same conditions.
- For trajectories with cascading failures, the paper adopts a fixed rule: trace the causal chain backward from the observed system-level failure and label the **earliest failure from which execution does not recover**, not its downstream symptoms — because an intervention at that earliest point would have changed the outcome.
- The taxonomy claims to be architecture- and modality-agnostic, applying to a single LLM answering a question, coding agents (Claude Code, Codex), long-running personal assistants (OpenClaw, Hermes Agent), and custom multi-agent systems (citing Cemri et al., 2025).
- Related Work positions the paper against five lines of prior work — benchmark-specific taxonomies, multi-agent coordination taxonomies, flat failure-mode lists, module-based taxonomies (Zhu et al., 2025a), and trace-level root-cause localization (Barke et al., 2026; Qiao et al., 2026) — arguing that none of them jointly identifies the interaction edge and the fault-side, which is this paper's specific claimed contribution.
- The paper reports validating the taxonomy's reproducibility with independent LLM judges: across four frontier models, judges recover human labels well above chance, with the strongest judge reaching **Cohen's κ = 0.76** against human labels and the highest pairwise inter-judge agreement reaching **Cohen's κ = 0.84**.

---

## 1 Introduction

### Motivation: the failure surface has outgrown outcome-level labels

The paper opens from the observation that as LLMs are deployed in "increasingly long-running and autonomous settings" (citing Anthropic, 2026c), they interact repeatedly with users, tools, memory, harness, and environment. This broader interaction surface expands the failure surface of the agent system, and "when an agent fails under such complex scenarios, it is often difficult to determine where the failure originated and which component should be repaired" (citing Zhang et al., 2025a; Cemri et al., 2025; Zhu et al., 2025a).

The paper's running example is a long-running **Claude Code** session (Anthropic, 2025a) in which an agent ignores an earlier user instruction. There are two possible causes with the identical visible symptom:
1. The harness's context compaction removed the instruction (a **harness-level** fault).
2. The instruction remained available in context but the model failed to follow it (a **model-level** fault).

The paper states plainly: "The observed behavior is the same, but the first case requires a harness-level fix, whereas the second requires a model-level intervention." This is the crux of why understanding failure modes matters — it is "essential for selecting effective post-hoc interventions, such as model post-training, harness engineering, environment redesign, or benchmark repair."

### Gap in prior classification

The paper credits Zhu et al. (2025a) with prior work that "classified agent failures by the internal agent module affected," but argues: "Without an explicit way to distinguish where a failure surfaces from which component caused it, outcome-level failure labels collapse distinct causes together and direct repairs toward the wrong part of the system."

### The component vocabulary (Table 1)

The paper represents an agent system as a set of interacting components. The model is the LLM policy; the owner specifies the task and what counts as success; the grader evaluates the result (usually not visible to the agent); third parties are other actors encountered during execution that do not act on behalf of the owner. The harness manages the model's context, memory, and tool access. The environment covers both the agent's local execution setting and the external services it uses.

| Component | Definition |
|---|---|
| Model | The policy that processes observations and produces outputs or actions. |
| Owner | The human or upstream system that gives the agent its task and defines what counts as success. |
| Grader | The mechanism used to evaluate whether the agent completed the task successfully; usually not visible to the agent. |
| Third party | An actor encountered during execution that does not act on behalf of the owner. Can be human, organization, or agent; the interaction may be adversarial, persuasive, or cooperative. |
| Context | The information available to the model during the current interaction, including instructions, conversation history, observations, and summaries. |
| Memory | A persistent store that outlives the active context, within or across sessions. |
| Tool | The bidirectional interface through which the model exchanges requests, messages, actions, observations, and responses with other components — includes callable tools, communication channels, and relaying wrappers. |
| Local env. | The agent's immediate execution environment: operating system, shell, filesystem, runtimes. |
| External env. | Systems outside the agent's immediate execution environment: remote services, websites, APIs, databases, model-provider infrastructure. |

Note from the table caption: "In multi-agent settings, peer and subagent describe the role of the other model. In subagent interactions, the focal model acts as the orchestrator, while in peer interactions, neither model directs the other."

### Edges and fault sides

Failures are analyzed at the **interaction between two components**; this interaction defines the **edge**, and the component responsible for the failure defines the **fault side**. Worked example given in the text: an agent reports that a tool call succeeded when it actually failed.
- Case 1: the tool wrapper suppresses the error, so the model never observes the failure → labeled `TOOL — MODEL · fault: TOOL`.
- Case 2: the wrapper returns the error, but the model ignores it → labeled `TOOL — MODEL · fault: MODEL`.

"The interaction is the same, but the responsible component differs." This pair of cases is the paper's central didactic illustration of why edge+fault-side (rather than edge alone, or outcome alone) is the right unit of analysis.

### Validating reproducibility via LLM judges

To show these labels "capture shared structure rather than one annotator's intuition," the paper evaluates reproducibility using independent reasoning agents as judges. It motivates this methodologically by noting that "recent advances in the multi-step reasoning and evidence-synthesis capabilities of LLMs have motivated their use as agentic evaluators that independently reconstruct evidence and apply explicit criteria" (citing OpenAI, 2024; Snell et al., 2025; Zhuge et al., 2024). Each judge is treated as an independent analyst; pairwise agreement is measured to test convergence given the same definitions and evidence.

Reported results (previewed in the Introduction, detailed later in the paper):
- Across four frontier-model judges, labels are recovered "well above chance."
- The strongest judge reaches **Cohen's κ = 0.76** against human category labels.
- Judges agree with one another about as strongly as they agree with annotators, with the highest pairwise (judge-judge) agreement reaching **Cohen's κ = 0.84**.

### Handling cascading failures: earliest-unrecoverable-failure rule

"A single trajectory often contains many cascading failures. Without a fixed rule for which one to label, annotators would score the same trace inconsistently." The paper's rule: begin with the observed system-level failure and trace its causal chain backward, labeling "the earliest failure from which execution does not recover, rather than its downstream symptoms" (citing Jorf and Shamout, 2026; Zhu et al., 2026b; Qiao et al., 2026). The justification is counterfactual: "An intervention at this point would have resulted in a different outcome, whereas the later errors may only be consequences of it."

### Scope / generality claims

The taxonomy is claimed to apply "wherever a model or group of models interacts with users, tools, environments, memory, or other agents." Even the minimal case — a single LLM answering a user's question — involves a model–user interaction. The same vocabulary is claimed to apply to:
- Coding agents: **Claude Code** (Anthropic, 2025a), **Codex** (OpenAI, 2025)
- Long-running personal assistants that read mail, browse the web, execute shell commands, and maintain persistent memory: **OpenClaw** (OpenClaw, 2025), **Hermes Agent** (Nous Research, 2025)
- Custom multi-agent systems (Cemri et al., 2025)

The taxonomy is also described as "modality-agnostic, with several worked examples drawn from multimodal settings."

### Three stated contributions

1. **An interaction-centric taxonomy of 41 agent failure modes**, each assigned to an interaction edge and a fault side (referencing Figure 2, not in this chunk). Most modes are model-side "partly because our attribution rule assigns fault to the model when a more capable model could have avoided or recovered from the failure under the same conditions."
2. **Grounding in worked examples** drawn from public benchmarks, model system cards, published reports, and logged agent trajectories, "covering almost all of the failure modes."
3. **An evaluation of whether independent reasoning agents can consistently recover the human-assigned categories**, as evidence the taxonomy captures reproducible structure rather than annotator idiosyncrasy.

## 2 Related Work

### Framing: existing taxonomies are scoped, not general

"Existing taxonomies typically focus on one part of the agent interaction surface." The paper groups prior taxonomies into three scoping patterns:
- Tied to a particular benchmark (Deng et al., 2025; Zhu et al., 2026a).
- Address a specific setting, such as coordination in multi-agent systems (Cemri et al., 2025; Lin et al., 2025).
- Presented as a flat list of failure modes (Vinay, 2025).

The paper concedes these are "valuable within their intended scope" but argues "none of them indicates which component is at fault, and therefore which kind of intervention a failure calls for." It states the desired property explicitly: "A general framework should map each failure to the intervention it needs, such as model post-training, harness engineering, or environment redesign."

To motivate this, it gives a second illustrative pair: a coarse label such as "Execution Failure" "can conflate an unrecoverable external-service failure with a model giving up after a transient error that it could have retried or routed around. The visible outcome may be identical, but the former requires repairing the external system, whereas the latter requires improving the model's recovery policy." This is structurally the same rhetorical move as the Claude-Code context-compaction example in §1: identical surface symptom, divergent required repair.

### Closest prior work: agent-specific failure taxonomies

**Cemri et al. (2025)** — analyze a large set of multi-agent traces and derive a taxonomy comprising *system-design failures*, *inter-agent misalignment*, and *task-verification failures*. Their inter-agent category further distinguishes mechanisms such as withholding a message, ignoring a message, and losing shared context. The paper characterizes its own relationship to this work as **complementary**: "these failures can occupy the same interaction edge while differing in which endpoint is responsible" — i.e., Cemri et al.'s mechanism-level distinctions (withhold vs. ignore vs. lose) can be re-expressed inside this paper's edge/fault-side schema as different fault-side assignments on the same edge.

**Zhu et al. (2025a)** — divide a single agent into modules: memory, reflection, planning, action, and system-level operations, and classify errors according to the affected module. The paper's point of divergence: "In our framework, planning, reflection, and action selection remain part of the LLM policy. Persistent memory stores, tool interfaces, graders, users, and environments are instead represented as separate components of the agent system." In other words, this paper collapses Zhu et al.'s cognitive-function subdivisions of the model into a single Model component, while promoting what Zhu et al. treat as internal/adjacent concerns (memory, tools, graders, users, environment) into first-class components capable of bearing fault.

### Security-oriented taxonomies

- **Microsoft AI Red Team (2025)** — organizes failures by threats and consequences (a security-literature framing, contrasted implicitly with this paper's causal/component framing).
- **Shah et al. (2026)** — distinguish fault types, symptoms, and root causes in open-source agent systems, and "frequently identify causes at producer–consumer boundaries." The paper's stated advance: "Our edge and fault-side representation makes the two endpoints of such a boundary explicit" — i.e., it formalizes what Shah et al. observe informally (that faults cluster at producer-consumer boundaries) into an explicit two-endpoint (edge, fault-side) labeling scheme.

### Failure localization in execution traces

A "complementary line of work studies failure localization in agent execution traces":
- **Barke et al. (2026)** — identify the critical failure as the first unrecoverable event and reconstruct its causal relationship to the terminal outcome.
- **Qiao et al. (2026)** — verify candidate failure hypotheses against the full interaction trace before attributing responsibility.

The paper's positioning: "These approaches address which event in a trajectory should be treated as causal. We adopt this root-cause view to determine which event receives a taxonomic label. Our taxonomy then addresses a separate question by identifying the interaction on which that failure occurred and the component responsible for it." This is an explicit **layering** claim: Barke et al. / Qiao et al. solve "which event is the root cause" (temporal/causal localization within a trace), and this paper's taxonomy solves a downstream, orthogonal question — "which edge and which fault side does that already-identified root-cause event belong to" (structural/componential localization).

### Benchmark-specific failure analyses

The paper acknowledges that "within individual benchmarks, failure analyses are necessarily scoped to the tasks, interfaces, and evaluation procedures under study," and that "this specialization is valuable because it reveals domain-specific failure mechanisms, and provides actionable guidance for improving agents in a particular setting." Examples given:
- Coding benchmarks distinguishing failures visible through tests and diffs, such as an incorrect patch or a missed file (Jimenez et al., 2024; Deng et al., 2025).
- Tool-use benchmarks characterizing malformed calls and failures to recover from tool errors (Kokane et al., 2024; Bandi et al., 2026).

But: "no individual analysis captures the full failure surface of contemporary agents, which increasingly interact with users, context-management systems, persistent memory, tools, graders, local and external environments, and other agents. As this interaction surface expands, practitioners need a rigorous shared taxonomy that complements task-specific analyses and supports consistent diagnosis across systems."

### Summary of the paper's positioning relative to related work

| Prior line of work | What it classifies by | Cited works | Gap relative to this paper |
|---|---|---|---|
| Benchmark-specific taxonomies | Task/interface/evaluation-specific failure modes | Deng et al., 2025; Zhu et al., 2026a; Jimenez et al., 2024; Kokane et al., 2024; Bandi et al., 2026 | Scoped to one benchmark; no cross-system shared structure |
| Multi-agent coordination taxonomies | Coordination/communication mechanisms among agents | Cemri et al., 2025; Lin et al., 2025 | Does not indicate which component is at fault / which intervention is needed |
| Flat failure-mode lists | Enumerated failure modes without structure | Vinay, 2025 | No mapping from failure to intervention |
| Module-based taxonomies | Internal agent module affected (memory, reflection, planning, action, system-level) | Zhu et al., 2025a | Conflates model's internal cognitive functions with genuinely separate components (memory store, tools, graders, users, environment) |
| Security/threat taxonomies | Threats and consequences; fault types/symptoms/root causes at producer-consumer boundaries | Microsoft AI Red Team, 2025; Shah et al., 2026 | Boundaries identified informally; endpoints and fault side not made explicit |
| Trace-level root-cause localization | First unrecoverable event / verified causal hypothesis within a single trajectory | Barke et al., 2026; Qiao et al., 2026 | Identifies *which event* is causal, not *which interaction edge and component* is at fault |

### The paper's closing statement of orthogonality

"Prior work primarily identifies what behavior occurred, which internal module was affected, or which trajectory event was decisive. Our framework is orthogonal: it identifies the causal event, localizes it to interaction between components, and determines where the intervention should be applied. This distinction helps separate failures that call for model post-training from those requiring harness engineering or closer scrutiny of the evaluation setup."

This sentence functions as the section's thesis statement and directly sets up §3 ("The Mechanism Axis"), which follows immediately after this chunk ends.

---

**Covers:** §1 Introduction, §2 Related Work (arXiv:2607.28802)
