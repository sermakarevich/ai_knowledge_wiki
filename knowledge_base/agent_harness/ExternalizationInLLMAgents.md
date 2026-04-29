# Externalization in LLM Agents: A Unified Review of Memory, Skills, Protocols and Harness Engineering

**Paper:** [Externalization in LLM Agents: A Unified Review of Memory, Skills, Protocols and Harness Engineering (Zhou, Chai, Chen et al., 2025)](https://arxiv.org/abs/2604.08224)

## Human Readable TL;DR

Imagine you are trying to be a great chef, but you can only remember the last few minutes of your life. You would constantly forget recipes, lose track of what is in your pantry, and struggle to coordinate with other cooks. Now imagine someone gives you a recipe book, a labeled pantry, a shared kitchen protocol, and a sous-chef who keeps everything organized. You did not get smarter -- your kitchen just got smarter around you. This paper argues that the same thing is happening with AI agents: instead of making the AI brain bigger, engineers are building better "kitchens" -- external notebooks, procedure manuals, communication standards, and management systems -- that make AI agents dramatically more reliable and capable.

## TL;DR

This survey proposes "externalization" as the unifying transition logic behind recent advances in LLM-based agents. It argues that progress stems not primarily from larger models or better training, but from systematically relocating cognitive burdens -- memory, procedural expertise, and interaction structure -- from the model's internal computation into persistent, inspectable, reusable external infrastructure. The paper provides a comprehensive taxonomy of externalized memory, skills, and protocols, and introduces "harness engineering" as the integrative discipline that orchestrates these components into reliable agent behavior.

---

## Problem & Motivation

LLM agents face three fundamental mismatches that limit their reliability:

- **The Continuity Problem:** Finite context windows and weak session memory make it impossible for LLMs to maintain state, recall past experiences, or track partially completed work across long interactions.
- **The Variance Problem:** LLMs rederive multi-step procedures from scratch each time, leading to inconsistent execution, omitted steps, and unstable tool usage.
- **The Coordination Problem:** Interactions with external tools, services, and other agents are brittle when left to free-form prompting, creating interoperability and safety risks.

Existing surveys treat memory, tool use, and agent architectures as isolated components. This paper argues that a systems-level perspective is missing -- one that explains *why* these architectural shifts are occurring and how they collectively transform what it means to build a capable agent. The authors ground their analysis in cognitive artifact theory (Norman, 1991), which holds that external aids do not merely amplify internal abilities but fundamentally transform the nature of the task itself.

---

## Main Original Ideas

1. **Externalization as Unifying Transition Logic.** The paper identifies a single explanatory principle -- externalization -- that connects otherwise fragmented developments in agent memory, skills, protocols, and orchestration. Rather than treating these as independent engineering choices, the authors show they are all instances of the same cognitive offloading pattern.

2. **Cognitive Artifact Framework for LLM Agents.** Drawing on Norman's cognitive artifact theory and distributed cognition, the paper reframes external infrastructure not as scaffolding that helps a model but as a representational transformation that changes what the model needs to do. This theoretical bridge to cognitive science provides a principled foundation for agent design.

3. **Three-Axis Taxonomy of Externalized Cognition.** The paper decomposes externalization into three orthogonal dimensions -- memory (state across time), skills (procedural expertise), and protocols (interaction structure) -- each with detailed sub-taxonomies of content types, architectural evolution, acquisition mechanisms, and boundary conditions.

4. **Harness Engineering as an Integrative Discipline.** The paper coins and defines "harness engineering" as the practice of designing the runtime environment that orchestrates externalized modules. It identifies six analytical dimensions: agent loop control, sandboxing, human oversight gates, observability, configuration/policy encoding, and context budget management.

5. **Cross-Module Coupling Analysis.** The paper maps six primary interaction flows between memory, skills, and protocols (e.g., memory-to-skill distillation, skill-to-protocol invocation) showing how these form a self-reinforcing cycle, and identifies system-level challenges like context budget competition and timescale mismatches.

6. **Parametric vs. Externalized Capability Trade-off Framework.** The authors formalize the decision of when to keep capability inside model weights versus externalizing it, governed by update frequency, reusability, auditability requirements, and latency constraints.

---

## Key Findings

### Memory Externalization

| Architecture Stage | Description | Key Property |
|---|---|---|
| Monolithic Context | All state in the prompt | Simple but unscalable |
| Retrieval Stores | Context + external search (RAG) | Selective recall |
| Hierarchical Memory | Multi-tier storage with extraction/consolidation/forgetting | Managed lifecycle |
| Adaptive Memory | Dynamic modules with feedback-based optimization | Self-improving |

### Skill Externalization

| Evolution Stage | Description |
|---|---|
| Atomic Primitives | Individual tool invocations |
| Large-Scale Selection | Choosing among many available tools |
| **Packaged Expertise** | **Reusable procedural guidance with specification, discovery, progressive disclosure, execution binding, and composition** |

### Protocol Families

| Protocol Type | Example | Purpose |
|---|---|---|
| Agent-Tool | MCP | Tool discovery and invocation |
| Agent-Agent | A2A | Task delegation and coordination |
| Agent-User | A2UI, AG-UI | UI generation, streaming state |
| Domain-Specific | UCP | Specialized vertical protocols (e.g., commerce) |

### Key Qualitative Findings

- External infrastructure performs a "representational transformation" -- converting hard cognitive tasks (perfect recall, consistent execution) into easier ones (recognition, instruction following, schema filling).
- The historical trajectory moves from weights (pretraining) to context (prompt engineering, RAG) to harness (persistent external infrastructure), with each layer building on the previous.
- Skills face boundary conditions including semantic misalignment, portability issues, staleness, unsafe composition, and context-dependent degradation.
- Current agent benchmarks fail to measure the contributions of externalized infrastructure, calling for new evaluation methodologies.
- The optimal partition between parametric and externalized capability is dynamic and task-dependent, not a fixed architectural choice.

---

## Suggestions & Future Directions

1. **Multi-Modal Externalization.** Extend the framework beyond text to externalize visual, auditory, and spatial memory/skills/protocols for agents operating in richer perceptual environments.

2. **Embodied Agent Integration.** Apply externalization principles to robotics and physical agents where persistent world models, procedural motor skills, and real-time coordination protocols are critical.

3. **Self-Evolving Harnesses.** Develop harness systems that autonomously discover, distill, and refine their own externalized components through feedback loops, reducing reliance on human-authored infrastructure.

4. **Governance of Externalized Components.** Address security, trust, and compliance challenges that arise when skills, memory, and protocols become shared, versioned artifacts across agent ecosystems.

5. **New Evaluation Methodologies.** Design benchmarks that measure not just task completion but the effectiveness, maintainability, transferability, and governance quality of externalized components.

6. **Cognitive Overhead Management.** Investigate the costs of externalization -- retrieval latency, context budget consumption, coordination overhead -- and develop principled strategies for managing them.

7. **From Private Scaffolding to Shared Infrastructure.** Explore the transition from bespoke, per-agent external structures to standardized, composable agent infrastructure that enables interoperability at scale.

8. **Co-Evolution of Models and Infrastructure.** Study how advances in model capabilities and external infrastructure mutually influence each other, potentially informing paths toward more general artificial intelligence.

---

## Authors & Institutions

Chenyu Zhou (SJTU), Huacan Chai (SJTU), Wenteng Chen (SJTU), Zihan Guo (Sun Yat-Sen University / Shanghai Innovation Institute), Rong Shan (SJTU), Yuanyi Song (SJTU), Tianyi Xu (SJTU), Yingxuan Yang (SJTU), Aofan Yu (SJTU), Weiming Zhang (SJTU), Congming Zheng (SJTU), Jiachen Zhu (SJTU), Zeyu Zheng (Carnegie Mellon University), Zhuosheng Zhang (SJTU), Xingyu Lou (OPPO), Changwang Zhang (OPPO), Zhihui Fu (OPPO), Jun Wang (OPPO), Weiwen Liu (SJTU), Jianghao Lin (SJTU), Weinan Zhang (SJTU / Shanghai Innovation Institute)
