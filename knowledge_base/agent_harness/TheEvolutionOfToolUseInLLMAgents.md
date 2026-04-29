# The Evolution of Tool Use in LLM Agents: From Single-Tool Call to Multi-Tool Orchestration

**Paper:** [The Evolution of Tool Use in LLM Agents: From Single-Tool Call to Multi-Tool Orchestration (Xu et al., 2026)](https://arxiv.org/abs/2603.22862)

## Human Readable TL;DR

Imagine you hired an assistant who could use one tool at a time -- a calculator, a search engine, or a calendar. Now imagine upgrading to an assistant who can juggle all those tools simultaneously, pass results between them, and recover when something goes wrong -- like a skilled project manager coordinating a whole team. This paper is the first comprehensive guide to that upgrade, mapping out how AI agents evolved from "one tool at a time" to orchestrating complex multi-tool workflows, and identifying the six key challenges (planning, training, safety, speed, adaptability, and testing) that must be solved to make these advanced assistants reliable in the real world.

## TL;DR

This survey provides the first unified framework for multi-tool orchestration in LLM agents, shifting focus from single-tool call correctness to end-to-end executability of long-horizon, multi-tool chains. The authors organize the literature across six interconnected dimensions -- inference-time reasoning, training, safety, efficiency, capability completeness, and evaluation -- revealing that topology-aware planning, trajectory-level safety guarantees, and dynamic tool expansion are the critical frontiers. The work synthesizes findings across software engineering, enterprise workflows, GUI, and mobile agent domains.

---

## Problem & Motivation

Current LLM agents face tasks that require coordinating multiple tools across long execution horizons -- far beyond simple single-tool invocation. Two gaps motivate this survey:

1. **Conceptual ambiguity:** Terms like "tool use," "tool calling," and "orchestration" are used interchangeably despite referring to fundamentally different capability levels.
2. **Fragmented research:** Planning, training, safety, efficiency, and evaluation are studied in isolation, but deployed agent performance depends critically on their interaction.

The paper aims to unify formulations, distinguish single-call execution from multi-tool orchestration, and provide a cohesive six-dimensional analysis of the field.

---

## Main Original Ideas

1. **Unified single-call vs. orchestration formulation** -- Provides distinct mathematical definitions for single-tool calls (select-and-execute) versus multi-tool orchestration (stateful, cost-aware, multi-step decision-making), clarifying the qualitative complexity jump between the two.

2. **Six-dimensional analytical framework** -- Organizes the entire multi-tool agent literature into six interconnected dimensions (inference, training, safety, efficiency, completeness, evaluation), revealing cross-cutting dependencies that prior surveys treated in isolation.

3. **Orchestration topology abstraction** -- Classifies real-world agent deployments by their execution topology (serial, branching, parallel, nested) and operational constraints (cost, safety, verifiability), providing a unified lens for comparing applications across software engineering, enterprise, GUI, and mobile domains.

4. **Capability completeness as a first-class dimension** -- Elevates the problem of agents recognizing their own tool gaps and autonomously expanding their toolkits (tool creation, composite skill assembly, lifelong adaptation) to a core research dimension alongside planning and safety.

5. **Benchmark evolution taxonomy** -- Maps the progression of evaluation from single-call correctness to topological complexity, temporal scale (10-50+ step horizons), dynamic environments, and state persistence/self-correction testing.

---

## Key Findings

### Inference-Time Reasoning Evolution

| Generation | Approach | Example Systems | Key Advance |
|-----------|----------|-----------------|-------------|
| 1st | Sequential reasoning | ReAct | Linear thought-action loops |
| 2nd | Topological planning | GAP, ToolNet, StructuredAgent | Dependency graphs, AND/OR trees |
| 3rd | Hierarchical + search | HIPLAN, ADaPT, AB-MCTS | Bi-level planning, MCTS-based exploration |
| 4th | Dual-system orchestration | MARS, HuggingGPT | Fast/deliberate reasoning split |

### Training Paradigm Comparison

| Paradigm | Strengths | Limitations |
|---------|-----------|-------------|
| Training-free (ICL) | No parameter updates, flexible | Limited by context window, brittle on long chains |
| SFT | Reliable syntax, tool selection | Myopic imitation, struggles with unseen compositions |
| RL | Optimizes long-horizon decisions | Sparse rewards, credit assignment challenges |

### Safety Landscape
- Multi-tool orchestration expands the attack surface to cross-tool state pollution and cascading propagation
- Defenses evolving from pre-execution constraints to in-execution transaction management (rollback semantics) to post-execution trajectory-level verification
- Long-horizon "Agent Drift" (context pollution, autoregressive errors) identified as a distinct threat class

### Efficiency Strategies
- Parallel execution, asynchronous decoupling, and speculative reasoning reduce latency
- Dynamic tool retrieval and adaptive model routing (FrugalGPT, RouteLLM) control costs
- Semantic caching (GPTCache) and episodic memory (Reflexion, MemGPT) reduce redundant computation

### Benchmark Evolution
- Modern benchmarks test compositional DAG reasoning, 50+ step horizons, stateful interactive simulators, and human-in-the-loop settings
- Self-correction and state persistence now explicitly evaluated (CRITICTOOL, OdysseyBench)

---

## Suggestions & Future Directions

1. **Stateful orchestration abstractions** -- Need better formal models for managing state across parallel and nested tool executions, moving beyond ad-hoc solutions toward principled transaction semantics.

2. **Trajectory-level safety guarantees** -- Single-step filtering is insufficient; the field needs end-to-end safety verification that accounts for cascading effects across multi-step chains.

3. **Unified evaluation protocols** -- Current benchmarks fragment across dimensions; integrated evaluation covering topology, temporal scale, safety, and efficiency simultaneously is needed.

4. **Cost-aware planning** -- Planning algorithms should natively incorporate computational cost, latency budgets, and API pricing as first-class optimization objectives.

5. **Lifelong tool learning** -- Agents need mechanisms for persistent skill accumulation, tool deprecation, and adaptation to evolving APIs and environments without catastrophic forgetting.

6. **Bridging model reasoning and system guarantees** -- Closer integration between neural planning and formal verification methods to provide auditable, production-grade reliability.

---

## Authors & Institutions

Haoyuan Xu*, Chang Li*, Xinyan Ma*, Xianhao Ou* (equal contribution), Zihan Zhang (Harvard University), Tao He, Xiangyu Liu, Zixiang Wang, Jiafeng Liang, Zheng Chu, Runxuan Liu, Rongchuan Mu, Ming Liu (corresponding author), Bing Qin -- all from Harbin Institute of Technology, China, unless otherwise noted.
