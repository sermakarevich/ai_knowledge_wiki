# Automating Skill Acquisition through Large-Scale Mining of Open-Source Agentic Repositories

**Paper:** [Automating Skill Acquisition through Large-Scale Mining of Open-Source Agentic Repositories: A Framework for Multi-Agent Procedural Knowledge Extraction (Bi et al., 2025)](https://arxiv.org/abs/2603.11808)

## Human Readable TL;DR

Imagine you want to teach a robot new tricks, but instead of programming each one from scratch, you let it watch how other skilled robots work and learn their techniques automatically. This paper does exactly that for AI agents -- it builds a system that reads through thousands of open-source coding projects on GitHub, identifies the clever workflows and step-by-step procedures buried in the code, and packages them into reusable "skill cards" that any AI agent can pick up and use. The result is like creating a universal recipe book from the best chefs' kitchens, so any new chef can cook expert-level dishes without years of training.

## TL;DR

This paper presents a multi-stage framework for automated extraction of procedural knowledge from open-source agentic repositories, formalizing skills as four-tuples (conditions, policy, termination, interface) and standardizing them into the SKILL.md specification. Applied to TheoremExplainAgent and Code2Video repositories, the framework demonstrates a 40% gain in knowledge transfer efficiency over baselines, introduces SkillNet for ontological skill consolidation (30% fewer execution steps), and identifies that 26.1% of community-distributed skills contain security vulnerabilities -- motivating a four-stage verification pipeline.

---

## Problem & Motivation

Large language models possess broad declarative knowledge but lack specialized procedural expertise needed for autonomous real-world task execution. Current approaches to bridging this gap -- manual skill authoring by domain experts and autonomous discovery methods -- face scalability and quality challenges respectively.

Open-source repositories on GitHub encode significant domain expertise in functional code, but this procedural knowledge remains implicit and project-specific. The paper is motivated by the need for a systematic, automated method to extract this latent procedural intelligence, standardize it into reusable skill artifacts, and enable agents to dynamically extend their capabilities without costly retraining or fine-tuning.

---

## Main Original Ideas

1. **Formal Paradigm of Agentic Skills** -- Skills are rigorously defined as a four-tuple S = (C, pi, T, R) representing applicability conditions, policy (procedural logic), termination criteria, and interface. This formalism distinguishes skills from atomic tools (lacking complex logic) and episodic memories (lacking callable interfaces).

2. **Multi-Stage Extraction Pipeline** -- A three-phase approach: (1) repository structural analysis using tools like repo2AI to map directory hierarchies and identify orchestration patterns, (2) semantic skill identification through dense retrieval with bi-encoders and cross-encoder ranking to find reusable procedural patterns, and (3) translation into the standardized SKILL.md format with progressive disclosure architecture.

3. **Progressive Disclosure SKILL.md Architecture** -- A three-level specification where Level 1 metadata (30-100 tokens) is pre-loaded at startup, Level 2 instructions (200-5,000 tokens) are loaded on activation, and Level 3 resources are loaded on-demand -- minimizing context window consumption while supporting unbounded skill complexity.

4. **SkillNet Ontological Framework** -- An approach to organizing extracted skills into relational knowledge graphs with relationships like "is-a-subset-of" and "requires-output-from," enabling automated detection of redundant skills and optimized skill composition for complex tasks.

5. **Four-Stage Security Verification Pipeline (G1-G4)** -- A tiered security framework comprising static analysis, semantic classification, behavioral sandboxing, and permission validation to address the significant vulnerability risks in skills extracted from public repositories.

6. **Visual Anchor Prompting** -- Derived from Code2Video's Critic agent, a technique that overlays a 10x10 grid on rendered frames to enable Vision-Language Models to reason about spatial layout and generate precise refactoring suggestions for visual element positioning.

---

## Key Findings

| Metric | Result | Context |
|--------|--------|---------|
| Knowledge transfer efficiency | **+40%** vs baseline | Agent-generated educational videos using Code2Video skills |
| TheoremExplainBench score | **0.77** | o3-mini agent for multimodal scientific reasoning |
| Execution step reduction | **-30%** | SkillNet ontological skill composition |
| Task reward improvement | **+40%** | SkillNet across diverse backbone models |
| Vulnerable community skills | **26.1%** | Security survey of distributed skill artifacts |

- Agent-generated educational content in certain categories surpasses human-crafted tutorials in knowledge transfer metrics
- The SKILL.md progressive disclosure architecture enables agents to be aware of numerous skills with minimal token overhead (30-100 tokens per skill at Level 1)
- Dense retrieval with bi-encoder + cross-encoder ranking effectively identifies reusable procedural patterns within complex codebases
- The extraction framework successfully generalizes across different repository architectures (two-agent TEA vs. tri-agent Code2Video)

---

## Suggestions & Future Directions

1. **Evolution Agents** -- The authors envision agents that continuously refine skills by mining interaction logs and performance feedback, creating self-improving skill ecosystems rather than static skill libraries.

2. **Agentic Stack Architecture** -- A layered architecture integrating Agent Skills with the Model Context Protocol (MCP), positioning skills as a foundational component in a broader agent infrastructure for production environments.

3. **Expanded Domain Coverage** -- While demonstrated on visualization and educational content generation, the framework is designed for generalization to other domains such as data analysis, DevOps automation, and scientific computing.

4. **Enhanced Security Governance** -- The 26.1% vulnerability rate in community skills demands continued development of verification pipelines and trust frameworks, particularly as skill ecosystems scale.

5. **Skill Interoperability Standards** -- Further development of the SKILL.md specification and SkillNet ontology to enable cross-platform skill sharing and composition across heterogeneous agent implementations.

6. **Hybrid Acquisition Methods** -- Combining repository mining with autonomous discovery and expert authoring to maximize both quality and coverage of skill libraries.

---

## Authors & Institutions

Shuzhen Bi (Shanghai Innovation Institute, University of Science and Technology of China), Mengsong Wu (East China Normal University, Shanghai Innovation Institute), Hao Hao (East China Normal University), Keqian Li (East China Normal University), Wentao Liu (East China Normal University, Shanghai Innovation Institute), Siyu Song (East China Normal University), Hongbo Zhao (East China Normal University), Aimin Zhou (East China Normal University, Shanghai Innovation Institute -- corresponding author)
