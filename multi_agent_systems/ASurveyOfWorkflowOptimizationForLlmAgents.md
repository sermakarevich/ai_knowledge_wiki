# A Survey of Workflow Optimization for LLM Agents

**Paper:** [A Survey of Workflow Optimization for LLM Agents (Yue et al., 2026)](https://arxiv.org/abs/2603.22386)

## Human Readable TL;DR

When you ask an AI assistant to do something complex -- like plan a trip or write code -- it doesn't just think once; it follows a series of steps, like a recipe. This paper surveys all the research on how to design and improve those recipes. Think of it like optimizing an assembly line: you can rearrange stations, remove bottlenecks, or swap in better tools. The authors create a shared language for talking about these "workflow recipes" and show when it's best to use a fixed recipe versus one that adapts on the fly, helping engineers build AI systems that are both smarter and cheaper to run.

## TL;DR

This survey introduces the Agentic Computation Graph (ACG) abstraction to unify diverse methods for optimizing LLM agent workflows -- the structured compositions of LLM calls, tool use, retrieval, and verification steps. It categorizes 77 works along static vs. dynamic structure determination, optimization target (node/graph/joint), feedback signals, and update mechanisms. The paper proposes a structure-aware evaluation framework and minimum reporting protocol to improve comparability and reproducibility in the field.

---

## Problem & Motivation

LLM-based systems have evolved from single-prompt interactions to complex, multi-step workflows involving task decomposition, tool use, retrieval, code execution, and verification. While many surveys cover individual aspects (planning, tool learning, multi-agent collaboration), none treat the **workflow structure itself** as the primary optimization target. Research is fragmented across sub-domains with inconsistent terminology, making systematic comparison difficult. Suboptimal workflow structures lead to high costs, fragile control flow, and reduced effectiveness -- even when individual model calls are strong. This survey fills the gap by providing a unified framework, common vocabulary, and reproducible evaluation standard.

---

## Main Original Ideas

1. **Agentic Computation Graph (ACG) Abstraction** -- A unifying formalism where nodes represent atomic actions (LLM calls, tool use, retrieval, validation) and edges encode control, data, or communication dependencies. ACGs subsume pipelines, orchestration graphs, communication graphs, plans, and code-defined agent systems under one representation.

2. **Three-Level Workflow Abstraction** -- A clear distinction between reusable ACG templates (design-time specification), realized graphs (the specific structure deployed for a given input), and execution traces (the actual sequence of states and actions during a run). This separation enables precise analysis of where optimization occurs.

3. **Static vs. Dynamic Structure Determination Taxonomy** -- A primary organizing axis distinguishing methods that fix workflow structure offline (static) from those that construct, select, or edit structure at inference time (dynamic), further refined by Graph Determination Time (GDT) and Graph Plasticity Mode (GPM) descriptors.

4. **Cross-Cutting Synthesis Dimensions** -- Three orthogonal axes for comparing methods: optimization target (node/graph/joint), evidence source (metric/verifier/preference/textual feedback), and update mechanism (search/generation/RL/repair/continuous relaxation).

5. **Structure-Aware Evaluation Framework** -- A proposal to treat workflows as first-class outputs alongside task metrics, measuring graph-level properties (size, depth, communication volume), execution cost, robustness, and structural variance. Includes a minimum reporting protocol (Table 5) for reproducibility.

---

## Key Findings

### Static vs. Dynamic Optimization Landscape

| Aspect | Static Methods | Dynamic Methods |
|---|---|---|
| **When to use** | Repetitive workloads, stable APIs, constrained operator spaces | Heterogeneous tasks, high uncertainty, interactive environments |
| **Strengths** | Pre-deployment verification, lower runtime overhead | Task adaptivity, flexible structure |
| **Weaknesses** | Cannot adapt per-input | Harder to verify, needs budget controls |
| **Examples** | AFlow, ADAS, DSPy, MermaidFlow | DyFlow, AgentConductor, FlowReasoner, Workflow-R1 |

### Key Insights

- **Graph-level optimization often outperforms prompt tuning alone** when failures stem from missing verification steps, redundant communication, or incorrect control flow
- **Joint optimization** (structure + node parameters) tends to be more stable and effective than optimizing either in isolation
- **Verifiers** (unit tests, schema checks) provide the most actionable feedback when they are cheap and semantically meaningful
- **Dynamic selection/pruning** is optimal when tasks vary mainly in difficulty within a known motif library; **pre-execution generation** is better for genuinely different task structures; **in-execution editing** is essential for interactive environments with high uncertainty
- **Preference-based signals** (comparing workflows rather than scoring them absolutely) stabilize optimization when rewards are noisy
- Current evaluation practices over-focus on downstream task metrics while neglecting workflow structure, cost, and robustness -- hindering reproducibility

### Literature Inventory

- **77 in-scope works** surveyed: 39 core, 7 adjacent, 31 background
- **27 evaluation assets**: 20 benchmarks/environments, 7 datasets/validators

---

## Suggestions & Future Directions

1. **Structural Credit Assignment** -- Developing methods to attribute performance gains to specific structural changes (e.g., adding a verification node vs. changing routing) rather than confounding them with prompt or model improvements.

2. **Expressivity vs. Verifiability Trade-off** -- Designing workflow representations that are expressive enough to capture complex behaviors yet constrained enough for automated verification and safety analysis.

3. **Continual Adaptation Under Drift** -- Enabling workflows to adapt when tools, APIs, or environments change over time without full re-optimization from scratch.

4. **Better Data and Benchmarks** -- Creating workflow-specific benchmarks that evaluate structural quality, not just downstream task success, and building larger corpora of annotated workflow designs.

5. **Theoretical Foundations** -- Developing formal theory for workflow optimization, including complexity bounds, convergence guarantees, and principled cost-quality trade-off characterizations.

6. **Standardized Reporting** -- Adopting the proposed minimum reporting protocol to improve cross-study comparability, covering workflow representation, structural setting, model/tool configuration, offline/online costs, trace statistics, and failure analysis.

---

## Authors & Institutions

Ling Yue (RPI), Kushal Raj Bhandari (RPI), Ching-Yun Ko (IBM Research), Dhaval Patel (IBM Research), Shuxin Lin (IBM Research), Nianjun Zhou (IBM Research), Pin-Yu Chen (IBM Research, corresponding), Jianxi Gao (RPI), Shaowu Pan (RPI, corresponding)
