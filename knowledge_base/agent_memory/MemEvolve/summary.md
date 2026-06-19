# MemEvolve: Meta-Evolution of Agent Memory Systems

**Paper:** [MemEvolve: Meta-Evolution of Agent Memory Systems (OPPO AI Agent Team & LV-NUS lab, 2025)](https://arxiv.org/abs/2512.18746)

## Human Readable TL;DR

Imagine you're trying to get better at studying. Most AI tools improve by building up a bigger notebook of facts and tips over time -- but the notebook format itself stays fixed. MemEvolve changes this: it lets an AI agent not only fill its notebook but also redesign the notebook itself (what to write down, how to organize it, and when to review it) based on what kinds of problems it's solving. A student who switches between memorizing poetry and deriving math formulas needs different study habits -- MemEvolve lets agents develop those different habits automatically, without a human having to redesign the tool for each subject.

## TL;DR

MemEvolve is a meta-evolutionary framework for LLM-based agents that jointly evolves two things: the agent's accumulated experiential knowledge and the architecture of the memory system itself. It decomposes memory systems into four modular components (Encode, Store, Retrieve, Manage) and uses a bilevel optimization loop -- an inner loop for experience accumulation and an outer "diagnose-and-design" loop that identifies architectural bottlenecks and generates improved variants. Evaluated on four benchmarks (GAIA, WebWalkerQA, xBench-DeepSearch, TaskCraft), it achieves up to 17.06% performance gains with strong generalization across tasks, LLMs, and agent frameworks.

---

## Problem & Motivation

Prior self-evolving agent memory systems (e.g., Voyager, ExpeL, SkillWeaver, Mobile-Agent-E) allow agents to accumulate experience in fixed memory structures -- distilling trajectories into skills, tools, or knowledge graphs. The critical limitation: the **memory architecture itself is static**. No single memory design is universally optimal; a system tuned for web browsing degrades on mathematical reasoning and vice versa. Existing agents are "skillful learners" (good at learning with a fixed strategy) but not "adaptive learners" (capable of dynamically changing how they learn). MemEvolve addresses this by meta-evolving the memory architecture, enabling agents to refine not just what they know, but how they learn from experience.

---

## Main Original Ideas

1. **Meta-Evolutionary Memory Framework** -- Rather than treating memory architecture as a fixed design choice, MemEvolve treats it as a mutable genotype that evolves over training. The framework applies a bilevel optimization: the inner loop populates memory via environment interaction; the outer loop modifies the memory architecture based on performance feedback.

2. **Modular Memory Design Space (E, U, R, G)** -- Any memory system is decomposed into four interdependent components: Encode (transform raw trajectories into structured representations), Store (persist encoded experience), Retrieve (recall relevant context for current state), and Manage (offline consolidation, abstraction, or forgetting). This decomposition makes the exponentially large architecture search space tractable and evolvable.

3. **Diagnose-and-Design Outer Loop** -- The meta-evolution operator first generates a "defect profile" for each candidate architecture by inspecting trajectory-level evidence (retrieval failures, encoding mismatches, storage inefficiencies), then constructs descendant architectures conditioned on those specific defects. Changes are constrained to the modular (E, U, R, G) interface, ensuring architectural validity.

4. **Multi-Objective Pareto Selection** -- Candidate architectures are ranked using Pareto-dominance across three objectives -- task performance, API token cost, and execution latency -- so that efficiency is not sacrificed for accuracy during evolution.

5. **EvolveLab -- Unified Codebase and Benchmark** -- A standardized open-source implementation that re-implements twelve representative memory systems within the modular design space via a common `BaseMemoryProvider` interface. Includes evaluation support for GAIA, xBench, WebWalkerQA, and TaskCraft with both online/offline modes and LLM-as-a-Judge evaluation.

---

## Key Findings

| Benchmark | Framework | Baseline | MemEvolve | Gain |
|-----------|-----------|----------|-----------|------|
| xBench-DS | SmolAgent + GPT-5-Mini | 51% | 57% | +6 pp |
| xBench-DS | Flash-Searcher + GPT-5-Mini | 69% | 74% | +5 pp |
| WebWalkerQA | Kimi K2 + MemEvolve | -- | -- | **+17.06%** |
| TaskCraft | Kimi K2 + MemEvolve | -- | -- | **+10.0%** |
| All benchmarks (all configs) | Various | various | various | +3.54% to +5.0% |

- **Consistent improvements:** Unlike prior baselines (e.g., DILU degraded GAIA performance, ExpeL underperformed on new benchmarks), MemEvolve yielded positive gains on every evaluated benchmark without exception.
- **Cross-task generalization:** Memory architectures evolved on TaskCraft (synthetic) transferred directly to WebWalkerQA and xBench-DS with continued gains, indicating task-agnostic principles were learned.
- **Cross-LLM generalization:** Evolution used GPT-5-Mini; evolved memories transferred to Kimi K2 and DeepSeek V3.2 without manual adaptation, achieving the largest relative gains of the study.
- **Cross-framework generalization:** Memories evolved with Flash-Searcher transferred to Cognitive Kernel-Pro (CK-Pro) and OWL multi-agent systems, improving performance despite substantial architectural differences.
- **Resource efficiency:** API costs and execution delays remained comparable to the no-memory baseline -- gains came from architectural quality, not compute scaling.
- **Emergent architecture quality:** Qualitative analysis of the evolutionary trajectory (AgentKB -> Riva -> Cerebra) showed spontaneous development of multi-level abstractions, agent-driven encoding/decoding, hybrid retrieval, and periodic memory maintenance.

---

## Suggestions & Future Directions

1. **Scaling meta-evolution to more components** -- Apply the evolutionary paradigm beyond memory to planning algorithms, tool-use strategies, and reflection mechanisms across the full agent architecture.
2. **Broader benchmark coverage** -- Extend evaluations to scientific reasoning, code generation, and embodied tasks to further validate generalization claims.
3. **Automated evolutionary operators** -- Current diagnose-and-design uses LLMs as the mutation operator; future work could explore gradient-based or symbolic methods for more principled architectural search.
4. **Multi-agent memory co-evolution** -- Investigate how memory architectures evolve when multiple collaborating agents share or specialize their memory systems.
5. **Safety and alignment of evolved memories** -- As memory architectures become more autonomous, ensuring evolved systems remain aligned with human values is flagged as a critical open question.

---

## Authors & Institutions

**Core Contributors:** Guibin Zhang, Haotian Ren -- OPPO AI Agent Team / LV-NUS lab
**Contributors:** Chong Zhan, Zhenhong Zhou, Junhao Wang, He Zhu
**Corresponding Authors:** Wangchunshu Zhou, Shuicheng Yan
**Code:** https://github.com/bingreeky/MemEvolve
