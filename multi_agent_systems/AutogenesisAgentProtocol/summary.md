# Autogenesis: A Self-Evolving Agent Protocol

**Paper:** [Autogenesis: A Self-Evolving Agent Protocol (Wentao Zhang, 2026)](https://arxiv.org/abs/2604.15034)

## Human Readable TL;DR

Imagine a software team where everyone ships monolithic code that's hard to update -- any change risks breaking the whole product. This paper proposes giving AI agents a shared "build system" where every prompt, tool, and memory store is a versioned Lego brick with its own update rules. On top of that, agents get a structured way to propose and test their own improvements, like a pull-request workflow where the agent is both the author and the reviewer, with a full audit trail of what changed and why.

## TL;DR

The paper introduces the **Autogenesis Protocol (AGP)**, a two-layer specification for building self-evolving LLM agent systems. The **Resource Substrate Protocol Layer (RSPL)** registers prompts, agents, tools, environments, and memory as versioned, lifecycle-managed resources -- fixing under-specifications in existing protocols like A2A and MCP. The **Self Evolution Protocol Layer (SEPL)** provides a closed-loop interface for proposing, evaluating, and safely integrating improvements with auditable tracking. The reference **Autogenesis System (AGS)** demonstrates consistent gains over strong baselines on long-horizon planning and tool-use benchmarks.

---

## Problem & Motivation

Current LLM agent protocols (e.g., Agent-to-Agent / A2A, Model Context Protocol / MCP) focus narrowly on message passing and tool invocation but under-specify:

- **Cross-entity lifecycle management** -- how prompts, tools, agents, and memories are created, updated, deprecated
- **Version tracking** -- no first-class notion of which version of a prompt or tool produced which result
- **Evolution-safe update interfaces** -- no structured way to propose and validate changes without breaking downstream consumers
- **Context management across entities** -- shared memory semantics are ad-hoc

The consequence is **monolithic agent compositions and brittle glue code**. Every improvement requires hand-patching bespoke integrations, and there is no auditable record of what changed when. This blocks the larger goal of agents that *continuously self-improve in production* rather than being redeployed from scratch whenever a new skill is needed.

---

## Main Original Ideas

1. **Separation of "what evolves" from "how evolution occurs".** Prior work conflates the thing-being-improved (a prompt, a tool) with the improvement mechanism (fine-tuning, reflection). AGP cleanly splits these into two orthogonal layers, so any resource type in RSPL can be evolved via any mechanism in SEPL.

2. **Resource Substrate Protocol Layer (RSPL).** Treats prompts, agents, tools, environments, and memory as uniformly addressable, versioned resources with a common lifecycle API. This is the "package manager for agent components" -- register, version, depend on, deprecate -- which standard agent protocols lack.

3. **Self Evolution Protocol Layer (SEPL).** A closed-loop control surface sitting above RSPL: agents propose candidate changes (new prompts, refined tools, added skills), the system evaluates them against tasks and safety checks, and accepted proposals are integrated with full audit trails. This makes self-improvement *governable* rather than a black-box side effect.

4. **Auditable, evolution-safe update semantics.** Every change is a tracked event tied to specific resource versions, enabling rollback, attribution (why did this prompt change?), and reproducibility -- properties absent from prompt-chaining frameworks today.

5. **Reference implementation (AGS).** Demonstrates the protocol is implementable and that the abstractions do not come at a cost -- AGS reports consistent improvements over strong baselines on benchmarks requiring long-horizon planning and heterogeneous tool use.

---

## Key Findings

- **Benchmarks evaluated:** long-horizon planning and tool-integration suites including **GAIA**, **GPQA**, and **LeetCode**-style coding tasks.
- **AGS shows consistent performance gains over strong baselines** across these benchmarks (paper reports qualitative "consistent improvement"; specific per-benchmark deltas are in the experimental section of the PDF and were not fully extractable via automated PDF parsing -- see the paper's results tables for exact numbers).
- The gains come without changing the backbone LLM -- they come from better organisation of prompts/tools/memory as versioned resources plus the closed-loop evolution interface.
- Ablations indicate the two layers contribute independently: removing versioning hurts reproducibility and rollback; removing the evolution layer collapses the system to a conventional static agent.

> ⚠️ Note: because the PDF's quantitative tables did not extract cleanly through this automated pass, treat specific percentage figures as "see paper, Section on Experiments." The summary above captures directional claims the author makes, not verbatim numbers.

---

## Suggestions & Future Directions

1. **Skill-quality gating.** Develop better mechanisms for agents to *pre-evaluate* a proposed skill (e.g., simulated rollouts, static analysis of generated tools) before SEPL integrates it.
2. **Safety guardrails for unrestricted self-modification.** The author flags that open-ended self-editing can drift or be adversarially exploited; future work should formalise invariants resources must preserve across versions.
3. **Broader task-portfolio evaluation.** Current results are on coding + reasoning benchmarks; extending to multimodal, embodied, and open-domain tasks is called out as needed.
4. **Skill transfer and sharing.** Explore how resources registered in one AGS instance can be imported/inherited by another -- turning RSPL into a shared ecosystem, not just a local package.
5. **Compute cost amortisation.** Each evolution cycle is expensive (extra LLM calls for propose/evaluate); scheduling, caching, and batching strategies for evolution are open.
6. **Standardisation.** The author positions AGP as a candidate complement to A2A/MCP; advocacy for adoption across frameworks is implied future work.

---

## Authors & Institutions

Wentao Zhang (affiliation not specified on the arXiv landing page).
