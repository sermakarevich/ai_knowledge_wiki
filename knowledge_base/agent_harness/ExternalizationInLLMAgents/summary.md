# Externalization in LLM Agents: A Unified Review of Memory, Skills, Protocols and Harness Engineering

**Paper:** [Externalization in LLM Agents: A Unified Review of Memory, Skills, Protocols and Harness Engineering (Zhou, Chai, Chen, et al., 2026)](https://arxiv.org/abs/2604.08224)

## Human Readable TL;DR

Think of an LLM as a brilliant but forgetful worker: smart in the moment, but unable to remember past work, keep a tidy toolbox, or follow shared office rules. Instead of making the worker smarter, recent progress comes from building a better "workspace" around them -- notebooks they can re-read (memory), prepared playbooks they can reuse (skills), standard forms for talking with tools and coworkers (protocols), and a kitchen sink that keeps everything tidy (the harness). This paper argues that most of the value in modern AI agents now comes from designing that workspace well, not from a bigger brain.

## TL;DR

This survey introduces **externalization** as the organizing principle behind modern LLM agent design: relocating cognitive burdens out of model weights and prompts into persistent, inspectable runtime structures. The authors unify three externalization axes -- **memory** (state across time), **skills** (procedural expertise), and **protocols** (interaction contracts) -- under the umbrella of **harness engineering**, the infrastructure that coordinates them. They trace a historical progression from a *weights era* to a *context era* to a *harness era*, articulate cross-module interactions, and argue that the next frontier of agent progress depends more on harness engineering than on further model scaling.

---

## Problem & Motivation

Practical LLM agents face three recurrent mismatches that are not fixed by larger models:

1. **Continuity problem** -- finite context windows prevent reliable long-horizon state.
2. **Variance problem** -- complex procedures get rederived on every run rather than executed consistently.
3. **Coordination problem** -- tool and agent interactions are brittle without formal contracts.

Drawing on Norman's theory of cognitive artifacts, the authors argue that external structures do not merely add capacity -- they reshape tasks into forms the model can solve more reliably. Most real-world agent failures stem from poor task representation, not inadequate intelligence.

---

## Main Original Ideas

1. **Externalization as a unifying design principle.** Rather than treating agent progress as a collection of ad-hoc techniques (RAG, tool use, prompting), the paper frames it as one coherent phenomenon: relocating cognitive burden from parametric weights into persistent external structures.

2. **Three-axis taxonomy under one harness.** Memory (state), skills (procedures), and protocols (interaction) are the three externalization axes, each with its own content categories, architectural evolution, and representational transformation. The harness is the operating system that unifies them.

3. **Historical progression from weights to context to harness.** A clear periodization: the *weights era* (pre-2023, capability = parameters), the *context era* (2023-2024, capability = prompting/RAG/chain-of-thought), and the *harness era* (2024+, capability = runtime infrastructure).

4. **Cross-module interaction matrix.** The paper formalizes how memory, skills, and protocols feed each other -- e.g., memory-to-skill distillation, skill-to-memory execution records, protocol-to-skill capability generation. This turns the framework from a static taxonomy into a dynamic architecture.

5. **Representational transformation lens.** Each externalization axis is analyzed in terms of what cognitive burden it transforms: recall -> recognition/retrieval (memory), improvisation -> composition (skills), free-form communication -> verifiable contracts (protocols).

6. **Architectural evolution ladders.** Each axis is traced through concrete stages -- e.g., memory evolves from monolithic context -> retrieval storage -> hierarchical orchestration -> adaptive systems (MemGPT, MemoryOS, MemEvolve, MemRL).

---

## Key Findings

This is a survey/position paper; the contribution is conceptual rather than empirical, so findings are taxonomic and analytical rather than numeric.

- **Harness engineering is now the primary locus of agent improvement.** Most recent capability gains come from better infrastructure, not bigger models.
- **Memory architectures are trending toward hierarchical, tiered systems** with explicit extraction, consolidation, and forgetting policies -- rather than ever-longer monolithic contexts.
- **Skill systems are converging on packaged expertise** (specifications + examples + composition rules) and are acquired through four pathways: authored, distilled, discovered, composed.
- **Protocols are standardizing interaction** (invocation grammar, lifecycle semantics, permission boundaries, discovery metadata) across three surfaces: agent-tool, agent-agent, agent-user.
- **Trade-offs between parametric and externalized capability** are consistent: externalized state wins on update frequency, reusability, and auditability; parametric weights win on latency and integration.
- **Cross-module flows matter more than any single module.** The value of memory depends on skills that consume it; the value of skills depends on protocols that expose them; protocol outputs feed memory. Treating them in isolation misses the architecture.

---

## Suggestions & Future Directions

1. **Expand the externalization frontier** beyond memory/skills/protocols to include planning and goal management, evaluation and verification, orchestration logic itself, and multi-modal externalization.
2. **Borrow from embodied cognition** -- separate high-level deliberation (cerebrum) from learned, repeated action patterns (cerebellum), the latter being a natural externalization target.
3. **Build self-evolving harnesses** that modify their own externalized structures from experience rather than being statically engineered.
4. **Move from per-agent scaffolding to shared infrastructure** -- collective memory, skill libraries, and governance frameworks across agent ecosystems.
5. **Develop measurement frameworks** for "externalization density" and the internal-vs-external capability tradeoff, so the field can compare architectures on principled grounds.
6. **Address open challenges in evaluation, governance, and model-infrastructure co-evolution** -- as harnesses grow more capable, foundation models may evolve to exploit them, reshaping the tradeoff dynamically.

---

## Authors & Institutions

Chenyu Zhou, Huacan Chai, Wenteng Chen, Zihan Guo, Rong Shan, Yuanyi Song, Tianyi Xu, Yingxuan Yang, Aofan Yu, Weiming Zhang, Congming Zheng, Jiachen Zhu, Zeyu Zheng, Zhuosheng Zhang, Xingyu Lou, Changwang Zhang, Zhihui Fu, Jun Wang, Weiwen Liu, Jianghao Lin, Weinan Zhang. Affiliations not explicitly listed on the abstract page.
