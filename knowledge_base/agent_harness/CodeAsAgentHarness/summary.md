# Code as Agent Harness

**Paper:** [Code as Agent Harness (Ning et al., 2026)](https://arxiv.org/abs/2605.18747)

## Human Readable TL;DR

Imagine you're running a complex project and instead of just writing reports, you start using spreadsheets, scripts, and automated checklists to actually do the work -- and those tools also verify that the work was done correctly. This paper argues that AI systems should do the same: use code not just as a final deliverable, but as the living "control room" that keeps the AI grounded, organized, and verifiable throughout its whole task. It's a survey that maps out all the ways researchers are already doing this, and lays out a blueprint for making AI agents more trustworthy and capable.

## TL;DR

This survey formalizes "code as agent harness" -- the paradigm where code acts as an executable, inspectable, and stateful operational substrate for LLM-based agents rather than merely a generated artifact. The authors organize the landscape into three layers: (1) the harness interface (code for reasoning, acting, environment modeling), (2) harness mechanisms (planning, memory, tool use, feedback-driven control, optimization), and (3) scaling to multi-agent systems via shared code artifacts. The paper synthesizes hundreds of prior works into a unified taxonomy and identifies open challenges in harness engineering.

---

## Problem & Motivation

LLMs can generate code well, but in agentic settings -- long-horizon tasks, multi-step reasoning, real-world tool use -- pure text-based reasoning is unreliable, unverifiable, and stateless. Existing surveys treat code as an end product; this work repositions it as the infrastructure layer that connects models to tasks. The gap: no unified framework existed to understand how code serves as the operational substrate for agent intelligence across reasoning, acting, environment modeling, and multi-agent coordination.

---

## Main Original Ideas

1. **Code as Agent Harness** -- Formal reframing of code from "what agents produce" to "how agents operate." Code is the executable, inspectable, stateful medium that governs agent reasoning and behavior throughout a task loop.

2. **Three-Layer Taxonomy** -- The survey organizes the field into: (a) Harness Interface -- how code connects agents to reasoning, action, and environments; (b) Harness Mechanisms -- planning, memory, tool use, control loops, and self-optimization; (c) Scaling the Harness -- multi-agent coordination over shared code artifacts.

3. **Agent-Initiated Code Artifacts** -- Distinguishes code objects created and evolved by agents during execution (not pre-built infrastructure, not static outputs) as the central unit of analysis.

4. **Harness Control as Plan-Execute-Verify Loop** -- Reframes debugging as a broader harness control process: plans serve as contracts, execution happens in sandboxes with access controls, verification is deterministic (linters, tests, formal checks).

5. **Agentic Harness Optimization** -- The harness itself can be measured and improved via telemetry, evolution agents, and governed mutations -- treating the agent's operational substrate as a first-class engineering artifact.

6. **Harness Engineering as a Discipline** -- The paper advocates for harness engineering as a distinct research field, distinct from model training, focused on the operational substrates that make agents reliable, verifiable, and adaptable.

---

## Key Findings

| Layer | Mechanism | Representative Methods |
|-------|-----------|----------------------|
| Harness Interface -- Reasoning | Program-delegated reasoning | PAL, Program-of-Thoughts, CodeSteer |
| Harness Interface -- Acting | Programmatic policy generation | Code as Policies, RoboCodeX, Voyager |
| Harness Interface -- Environment | Execution-trace world modeling | Code World Model, WorldCoder, SWE-bench |
| Harness Mechanisms -- Planning | Search-based & orchestration | CodeTree, MapCoder, Self-Planning |
| Harness Mechanisms -- Memory | Working/semantic/experiential memory | Diverse memory taxonomies across agents |
| Harness Mechanisms -- Control | Sandboxed execution + verification | AgentBench, InterCode, SWE-smith |
| Scaling -- Roles | Functional role specialization | ChatDev, MetaGPT, AgentCoder |
| Scaling -- Topology | Adaptive workflow topologies | EvoMAC, FlowReasoner |
| Scaling -- Convergence | Test-gated / security / consensus | AutoSafeCoder, MAGE |

- Code's executability provides objective feedback signals (compiler errors, test pass/fail, fuzzer crashes, static analysis) that purely textual agents cannot access.
- Multi-agent systems benefit from shared code artifacts as a synchronization substrate -- blackboard models offer the closest approximation to a formal shared harness.
- Harness-state convergence criteria matter: correctness (test-gated), security, performance, and consensus are more reliable than implicit termination.
- Application domains validated: coding assistants, GUI/OS agents, embodied agents, scientific discovery, personalization/recommendation.

---

## Suggestions & Future Directions

1. **Harness-level evaluation** -- Metrics beyond final task success; measure reliability, state consistency, and intermediate verification across the execution trace.
2. **Semantic verification under incomplete feedback** -- Most current verification relies on executable tests; extending to semantic correctness without full oracles is an open problem.
3. **Regression-free self-evolving harnesses** -- Agents that improve their own harness without breaking prior capabilities require formal regression guarantees.
4. **Transactional shared state** -- Multi-agent settings lack robust mechanisms for atomic, consistent, isolated, durable updates to shared code state.
5. **Human oversight for safety-critical actions** -- Principled frameworks for when and how to insert human checkpoints into automated harness execution.
6. **Multimodal harness extensions** -- Extending code-as-harness to settings involving images, video, and physical sensor data beyond text-and-code.

---

## Authors & Institutions

Xuying Ning, Katherine Tieu, Dongqi Fu, Tianxin Wei, Zihao Li, Yuanchen Bei (UIUC, core contributors); Jiaru Zou (Stanford); Zikun Cui, Yang Cao, Pan Chen, Dorothy Sun, Ren Chen, Mahesh Srinivasan, Nipun Mathur, Yinglong Xia, Hong Li, Hong Yan (Meta); Lingming Zhang, Tong Zhang, Hanghang Tong, Jingrui He (UIUC); Pan Lu (Stanford). Full list of 30+ authors spanning UIUC, Meta, and Stanford.
