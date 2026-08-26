> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]

# The Meta-Harness Method

**In one sentence:** Meta-Harness optimizes task-specific harnesses by repeatedly letting a single coding-agent proposer, given filesystem access to the growing archive of all prior candidates' source code, scores, and execution traces, diagnose past failures from that archive and write new harnesses, until a fixed iteration budget is spent and the Pareto frontier is evaluated on the held-out test set.

## Key points

- Meta-Harness is an outer-loop procedure that repeatedly proposes, evaluates, and logs new harnesses; it is built on the idea that harness optimization works best when a proposer can selectively inspect prior code and execution traces via filesystem access, rather than optimize from lossy summaries or a hand-designed search structure.
- The search uses a **single coding-agent proposer** with access to a growing filesystem `D` that serves as its feedback channel [1]: each evaluated harness contributes a directory containing its source code, scores, and execution traces (prompts, tool calls, model outputs, state updates).
- The filesystem is typically far larger than the proposer's context window, so the proposer queries it through terminal tools such as `grep` and `cat` rather than ingesting it as a single prompt; at each iteration it first inspects prior code, scores, and traces, reasons about likely failure modes, then generates a new harness.
- There is **no parent-selection rule and no predefined mutation operator**: the proposer may inspect *any* prior harness and its execution trace, and its edits range from local changes to retrieval, memory, or prompt-construction logic up to a full program rewrite; starting from a strong prior harness is an emergent strategy, not a hard-coded rule.
- The search runs for a fixed number of iterations, maintains a population `H` plus a Pareto frontier over evaluated harnesses, and performs a final test-set evaluation **only on the Pareto frontier**; the proposer never sees test-set results.
- The proposer's only feedback comes from the **search set** (the subset of task instances used to evaluate candidates during search) and from the execution traces logged during those search runs.
- Searching in code space gives a natural regularization bias: coding models tend to propose coherent algorithms rather than brittle, hard-coded solutions, and the action space aligns with the read–write–execute workflows on which frontier coding assistants are trained.
- In the paper's experiments each harness is a single-file Python program; the proposer `P` is Claude Code [4] with Opus-4.6; a minimal domain-specific skill constrains where new harnesses are written, how to inspect prior harnesses/traces, and which files may and may not be modified; the base model `M` varies by domain and is always frozen; a typical run evaluates roughly **60 harnesses over 20 iterations**.

---

## Objective

A **harness** is a stateful program that wraps a language model and determines what context the model sees at each step. The goal is simple: find the harness that makes the underlying model perform best on the target task distribution. Formally, let `M` denote a fixed language model and `X` a task distribution. For a harness `H` and task instance `x ∼ X`, a rollout trajectory `τ ∼ p_M(H, x)` is produced: the harness constructs prompts for `M`, the model responds, and the harness updates its state after each interaction. A task-specific reward function `r(τ, x)` scores the trajectory. The objective of harness optimization is to find the harness that maximizes the expected final reward:

```
H* = arg max_H  E_{x∼X, τ∼p_M(H,x)}  r(τ, x)
```

When multiple objectives are relevant (e.g., accuracy and context cost), candidates are evaluated under Pareto dominance and the resulting Pareto frontier is reported. In practice, this search has traditionally been carried out by human engineers and researchers, who iteratively refine prompts, context-management rules, and tool-use logic by hand.

A note on terminology: Meta-Harness is itself a harness in the broad sense (hence the name), since it determines what information the proposer model sees during search. Unless otherwise noted, "harness" refers to the task-specific programs being optimized.

## The Meta-Harness search loop

Meta-Harness uses a single **coding-agent proposer** with access to a growing filesystem `D` that serves as its feedback channel [1]. Here a *coding agent* is a language-model-based system that can invoke developer tools and modify code.

The key design difference from prior systems: rather than externalizing the improvement logic in a hand-designed search loop, Meta-Harness delegates diagnosis and proposal to the coding agent itself. The proposer decides which prior artifacts to inspect, which failure modes to address, and whether to make a local edit or a more substantial rewrite. Equivalently, the proposer is not a raw next-token model operating on a fixed prompt assembled by the outer loop; it is an agent that retrieves information, navigates prior artifacts, and edits code as part of the search itself.

Concretely, the loop works as follows:

1. Each evaluated harness contributes a directory to `D` containing its **source code, scores, and execution traces** (prompts, tool calls, model outputs, and state updates).
2. Because `D` is typically far larger than the proposer's context window, the proposer queries it through **terminal tools such as `grep` and `cat`** rather than ingesting it as a single prompt — this is fundamentally different from typical text-optimizer feedback compression, where feedback is reduced to lossy summaries or a hand-designed channel.
3. At each iteration, the proposer first inspects prior code, scores, and execution traces, then reasons about likely failure modes before generating a new harness.

Search structure: Meta-Harness maintains a population `H` and a Pareto frontier over evaluated harnesses, but imposes **no parent-selection rule** — the proposer is free to inspect *any* prior harness and its execution trace when proposing new ones. Evolution is run for a fixed number of iterations, followed by a final test-set evaluation on the Pareto frontier.

This simplicity is deliberate: by leaving diagnosis and edit decisions to the proposer rather than hard-coding search heuristics, Meta-Harness can improve automatically as coding agents become more capable. The proposer never sees test-set results; its only feedback comes from the **search set** — the subset of task instances used to evaluate candidate harnesses during search and generate the feedback signal for improvement — and from execution traces logged during those search runs.

[1] Footnote from the source: based on earlier exploration, the authors believe this workflow only became practical recently, following major improvements in coding-agent capabilities around early 2026.

## Algorithm 1 (outer loop)

Verbatim transcription of Algorithm 1, "Meta-Harness outer loop over harnesses":

```
1:  Input: tasks X, LLM M, proposer P, iterations N
2:  Initialize: population H            ▷ Initial set of valid harnesses
3:  Initialize: filesystem D ← ∅        ▷ stores code, scores, traces
4:  for H ∈ H do
5:      E_H ← Evaluate(H, M, X)
6:      D ← D ∪ { (H, E_H) }
7:  for t = 1 ... N do
8:      Proposer P queries filesystem D     ▷ inspects prior harnesses and scores
9:      Proposer P proposes k new harnesses {H_1, ..., H_k}
10:     for H in {H_1, ..., H_k} do
11:         if H passes interface validation then
12:             D ← D ∪ { (H, Evaluate(H, M, X)) }
13: return Pareto frontier of harnesses stored in D
```

Steps in plain terms:

1. **Input:** tasks `X`, LLM `M`, proposer `P`, iterations `N`.
2. **Initialize:** population `H` (initial set of valid harnesses).
3. **Initialize:** filesystem `D ← ∅` (stores code, scores, traces).
4. For each initial harness `H` in `H`: evaluate it as `E_H ← Evaluate(H, M, X)` and append `(H, E_H)` to `D`.
5. For each iteration `t = 1 ... N`:
    - The proposer `P` queries filesystem `D` (inspects prior harnesses and scores).
    - The proposer `P` proposes `k` new harnesses `{H_1, ..., H_k}`.
    - For each proposed `H` that passes interface validation: append `(H, Evaluate(H, M, X))` to `D`.
6. **Return** the Pareto frontier of harnesses stored in `D`.

## Advantages of code-space search

Per the source, harness optimization in code space differs from the problem in ways that make local search heuristics poorly matched:

- **Long-horizon effects:** small changes to retrieval, memory, or prompt-construction logic can affect behavior many steps later, so local search heuristics are a poor fit.
- **Causal diagnosis from traces:** by inspecting execution traces, the proposer can often infer *why* a harness failed and which earlier design choices likely contributed to the failure, not just *that* it failed (as illustrated by the search trajectories in Appendices A and A.2). There, the proposer reads broadly across prior code and logs, then uses those traces to identify confounded edits, isolate likely causal changes, and shift toward safer modifications after repeated regressions.
- **Algorithmic-structure editing:** the proposer can modify the harness at the level of algorithmic structure — ranging from changes to retrieval, memory, or prompt-construction logic to full program rewrites — rather than filling in templates or applying predefined mutation operators.
- **Emergent seeding from strong priors:** in practice the proposer often starts from a strong prior harness, but this is an emergent strategy rather than a hard-coded rule.
- **Natural regularization bias:** although the search space is large, representing harnesses as programs provides a natural regularization bias — coding models tend to propose coherent algorithms rather than brittle, hard-coded solutions, which biases the search toward reusable context-management procedures.
- **Alignment with training distribution:** the action space is closely aligned with the read–write–execute workflows on which frontier coding assistants are trained.

## Practical implementation

Concrete implementation details given in the source:

- **Harness representation:** in the paper's experiments, each harness is a **single-file Python program** that modifies task-specific prompting, retrieval, memory, and orchestration logic.
- **Proposer identity:** the proposer `P` is **Claude Code [4] with Opus-4.6**.
- **Proposer guidance:** the proposer is guided by a **minimal domain-specific skill** that describes (a) where to write new harnesses, (b) how to inspect previous harnesses and their execution traces, and (c) what files it can and cannot modify.
- **Base model:** the base model `M` varies by domain and is **always frozen** (details deferred to Section 4 of the paper).
- **Typical run scale:** a typical run evaluates roughly **60 harnesses over 20 iterations**.
- **Extension guidance:** additional tips for implementing Meta-Harness in a new domain are provided in Appendix D of the paper.

**Covers:** Section 3 (Meta-Harness: A Harness for Optimizing Harnesses)
