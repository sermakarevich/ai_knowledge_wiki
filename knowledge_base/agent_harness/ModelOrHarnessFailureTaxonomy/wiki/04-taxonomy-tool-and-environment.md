> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# Taxonomy: Tool, Multi-Agent, and Environment

**In one sentence:** Across the Model–Tool, Model–Model, and Model–Environment edges of the harness, the taxonomy assigns most failures to the model (bad arguments, bad tool choice, poor delegation, missed cues, failure to recover), reserves a distinct "harness itself" fault (Mistranslation) for defects in the tool's own integration layer, and reserves environment-side fault strictly for cases where the underlying problem was genuinely unrecoverable.

## Key points

- The Model–Tool edge attributes six failure modes to the model — Malformed Arguments, Suboptimal Arguments, Incorrect Tool Selection, Tool Hallucination, Tool Feedback Neglect, and Tool Recovery Failure — and one, Mistranslation, to the tool's own integration layer, establishing the tool-as-middleware as a third fault locus distinct from both model and environment.
- Malformed Arguments and Suboptimal Arguments split syntactic from semantic failure at the same edge: the former is a schema violation that throws an immediate exception (e.g., a `str_replace` edit failing over one missing space), while the latter is structurally valid but low-signal input (e.g., a vague conversational phrase fed to a grep tool) that produces noisy results without crashing.
- Tool Hallucination (model calls an API/command that does not exist in its declared schema, causing an immediate crash) is distinct from Incorrect Tool Selection (model picks a real tool that is either wrong for the task or merely inefficient/brute-force).
- In multi-agent settings, both the Peer and Subagent relationships share the same two failure-mode types — Delegation Failure and Communication Failure — but fault attribution differs: peer failures are jointly MODEL-side (either peer can withhold or fail to use information), while subagent failures split between the FOCAL MODEL (orchestrator omits context, fails to route information, or fails to use subagent output) and the SUBAGENT (fails to report relevant results or constraints back).
- At the Model–External-Environment edge, Service Failure (Liu et al., 2026; Kara et al., 2025) and Stale State Delivery (Mazumder et al., 2026) are environment-side because the problem originates in the external service itself — an outright failed request, or a healthy-looking status code masking silently stale data.
- Recovery Failure (Zhu et al., 2026a) is the model-side counterpart at that same edge: it applies only when recovery remained possible and the model simply failed to retry, diagnose, or reroute around the problem; if recovery was genuinely not possible, the taxonomy attributes the failure to the environment instead.
- The Model–Local-Environment edge mirrors this recoverability logic in-process: Observation Failure (Zhou et al., 2024) is the model overlooking a cue already present in its observation space, and Recovery Failure (Arora et al., 2025) is the model failing to resolve a fixable local condition such as a missing file or broken state — the identical "was it fixable" test used to separate model fault from environment fault.
- Recovery Failure is defined with near-identical wording at both the External-Environment and Local-Environment edges in Appendix B, and in both cases the paper uses recoverability, not the nature of the trigger, as the dispositive criterion for whether the fault lands on the model.

---

## Model — Tool

This edge covers failures in how the model constructs, selects, and reacts to tool calls, plus one failure mode located in the tool's own integration layer rather than in the model or the environment. Neither source chunk supplies literature citations for this edge (the narrative chunk provided did not reach this section, and Appendix B definitions are given without citations).

| Failure Mode | Fault Side | Definition (Appendix B, verbatim) | Citation |
|---|---|---|---|
| Malformed Arguments | MODEL | The model understands what change it wants to execute but lacks the syntactic precision to express it in the tool's rigid schema. This results in an immediate exception (e.g., a codebase str_replace edit that fails entirely because of a single missing space or mismatched indentation). | not given in provided chunks |
| Suboptimal Arguments | MODEL | The model creates structurally valid parameters, but the semantic quality of the input is low-signal (e.g., passing a vague, conversational phrase into a technical search or grep tool), leading to noisy results. | not given in provided chunks |
| Incorrect Tool Selection | MODEL | The model selects a tool that is either completely wrong for the task (causing a functional error or logical dead-end) or fundamentally inefficient. In the case of inefficiency, it opts for a wasteful, brute-force trajectory when an elegant, low-cost path is available. | not given in provided chunks |
| Tool Hallucination | MODEL | The model attempts to call an API, script, or workspace command that does not exist in its provided tool declaration schema, resulting in an immediate execution crash. | not given in provided chunks |
| Tool Feedback Neglect | MODEL | The model fails to act on an explicit signal in a tool's execution response and pushes forward with an unrelated, misaligned plan. | not given in provided chunks |
| Tool Recovery Failure | MODEL | The model fails to dynamically navigate around tool anomalies. When a tool encounters a perturbation, either an explicit failure (e.g., HTTP 503, rate-limit timeout) or an implicit semantic failure (valid format but corrupted data), the model is trapped in a futile trial-and-error retry loop or blindly over-trusts the broken data instead of pivoting to an alternative tool path. | not given in provided chunks |
| Mistranslation | TOOL | A defect in the tool's integration layer (its wrapper, middleware, or marshaling code) rather than in the environment or the model. The environment produces correct information and the model reasons correctly, but the layer that translates data across the model↔environment boundary conveys it unfaithfully, either garbling an observation sent to the model or mis-mapping the model's action onto the environment. | not given in provided chunks |

Note: Mistranslation is the one failure mode on this page not attributed to MODEL or to an environment side — it is attributed to the TOOL itself, i.e., to a defect in the harness's own translation/marshaling layer that sits between a correctly-reasoning model and a correctly-behaving environment.

## Model — Model (Multi-Agent)

This edge covers coordination failures between multiple model instances, split into two roles: Peer (models coordinating as equals) and Subagent (a focal/orchestrator model delegating to a subordinate agent).

### Role: Peer

| Failure Mode | Fault Side | Definition (Appendix B, verbatim) | Citation |
|---|---|---|---|
| Delegation Failure | MODEL | The peer models fail to coordinate how work is divided or to account for dependencies and workspace boundaries between their assigned tasks, leading to incomplete, overlapping, or incompatible execution. | not given in provided chunks |
| Communication Failure | MODEL | The peer models fail to exchange information needed for coordination. One may withhold relevant context or fail to use information supplied by the other. | Cemri et al., 2025; Khatua et al., 2026 |

The narrative chunk describes this Communication Failure as occurring "when a model fails to share information needed by a peer" — consistent with, though slightly narrower in wording than, the Appendix B definition, which also covers a peer failing to *use* information supplied by the other.

### Role: Subagent

| Failure Mode | Fault Side | Definition (Appendix B, verbatim) | Citation |
|---|---|---|---|
| Delegation Failure | FOCAL MODEL | The focal model, acting as orchestrator, assigns a subagent work with incorrect scope, dependencies, or workspace boundaries. | Xiong et al., 2026 |
| Communication Failure | FOCAL MODEL / SUBAGENT | The focal model is at fault when it omits context needed by a subagent, fails to route information between subagents, or fails to use a subagent's output. The subagent is at fault when it fails to report relevant results or constraints to the focal model. | Ruan et al., 2026 |

The narrative framing matches this split exactly: "Delegation Failure (Xiong et al., 2026) occurs when the orchestrator assigns work with incorrect scope or dependencies, while Communication Failure (Ruan et al., 2026) occurs when the orchestrator omits necessary context or fails to use the subagent's output, or when the subagent fails to report relevant results or constraints." Communication Failure is thus the one failure mode on this page with a genuinely dual fault-side label, splitting blame between the orchestrator and the subagent depending on which party dropped the information.

## Model — External Environment

This edge covers failures involving external services (upstream LLM hosts, cloud platforms, remote sites) and the model's response to them.

| Failure Mode | Fault Side | Definition (Appendix B, verbatim) | Citation |
|---|---|---|---|
| Service Failure | ENVIRONMENT | An external service (an upstream LLM host, a cloud platform, a remote site like YouTube) hits an internal error, timeout, or rate limit and fails the request outright, with no way for the agent to recover. | Liu et al., 2026; Kara et al., 2025 |
| Stale State Delivery | ENVIRONMENT | An external service returns a healthy status code but silently serves stale or cached data, with no signal that it is out of date, so the agent acts as if it has the live state. | Mazumder et al., 2026 |
| Recovery Failure | MODEL | The agent fails because of an environment problem that was in fact recoverable. Faced with a transient error, a missing file, or an ambiguous state, the model gives up or acts on a false assumption instead of retrying, diagnosing, routing around it, or asking the user. What separates this from Service Failure and Stale State Delivery is only recoverability: the condition was fixable, so the fault is the model's. | Zhu et al., 2026a |

Both Service Failure and Stale State Delivery "lie on the environment side because the problem originates in the service" itself; Recovery Failure is model-side "when recovery remains possible but the model does not retry, diagnose the problem, or use an alternative route" — and if recovery is *not* possible, the paper attributes the failure to the external environment instead, not to the model.

## Model — Local Environment

This edge covers failures in how the model observes and responds to its local execution environment (e.g., the sandbox, filesystem, or local process state it is operating in).

| Failure Mode | Fault Side | Definition (Appendix B, verbatim) | Citation |
|---|---|---|---|
| Observation Failure | MODEL | A cue the model needs is present in its observation space, but the model overlooks it and acts without resolving the ambiguity that cue would have settled. | Zhou et al., 2024 |
| Recovery Failure | MODEL | The agent fails because of an environment problem that was in fact recoverable. Faced with a transient error, a missing file, or an ambiguous state, the model gives up or acts on a false assumption instead of retrying, diagnosing, routing around it, or asking the user. What separates this from Service Failure and Stale State Delivery is only recoverability: the condition was fixable, so the fault is the model's. | Arora et al., 2025 |

The narrative chunk phrases these more compactly: Observation Failure "occurs when the model overlooks a cue available in its observation space," and Recovery Failure (local) "occurs when the model fails to resolve a fixable local condition, such as a missing file or broken state." Note that Appendix B gives Recovery Failure essentially the same verbatim definition text at both the External-Environment and Local-Environment edges — the taxonomy treats it as one recoverability criterion applied at two different loci (external service vs. local execution context), rather than as two independently-worded failure modes.

---

**Covers:** §5.2 Failure Families — Harness (Tool, Model-Model, External-Environment, Local-Environment edges); Appendix B (relevant definitions) (arXiv:2607.28802)
