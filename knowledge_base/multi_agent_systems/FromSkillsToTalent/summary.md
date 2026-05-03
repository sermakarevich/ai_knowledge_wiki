# From Skills to Talent: Organising Heterogeneous Agents as a Real-World Company

**Paper:** [From Skills to Talent: Organising Heterogeneous Agents as a Real-World Company (Yu et al., 2025)](https://arxiv.org/abs/2604.22446)

## Human Readable TL;DR

Imagine you need to run a company with robot employees who each have different skills -- some are great coders, some are researchers, some are writers. The problem is these robots all speak different "programming languages" and can't naturally work together. This paper builds a management system that acts like a real company: it hires the right robots for each project from a talent marketplace, assigns them tasks in an organized way with proper review steps, and lets both individual robots and the company as a whole learn and improve over time. The result is an AI system that can complete complex multi-step projects across wildly different domains -- software, games, audiobooks, research surveys -- from a single high-level instruction.

## TL;DR

OneManCompany (OMC) is a multi-agent framework that introduces a principled organizational abstraction -- decoupling agent identities (Talents) from execution environments (Containers) -- enabling heterogeneous agents (LangGraph, Claude Code, scripts) to interoperate via typed interfaces. Project execution is formalized as an Explore-Execute-Review (E2R) tree search with DAG-based task decomposition and formal termination guarantees. On PRDBench (50 software dev tasks), OMC achieves 84.67% success rate, +15.48 pp over state of the art, while also demonstrating cross-domain capability in content generation, game dev, audiobooks, and research surveys.

---

## Problem & Motivation

Existing multi-agent systems suffer from: fixed team structures brittle to novel projects, tightly coupled coordination logic without convergence guarantees, incompatible runtimes preventing agent interoperability, and session-bound learning that prevents persistent organizational improvement. No prior work provides a unifying organizational abstraction that decouples workforce management and evolution from individual agent capabilities. OMC addresses this by modeling AI agent teams as structured companies with lifecycle management, dynamic hiring, and experience-driven evolution.

---

## Main Original Ideas

1. **Talent--Container Architecture** -- An agent's cognitive identity (prompts, role, skills, tools) is packaged as a portable "Talent" that can be deployed on any "Container" (runtime: LangGraph, Claude Code, script). Six typed interfaces (Execution, Task, Event, Storage, Context, Lifecycle) mediate all agent-platform interactions, enabling identity-substrate separation and multi-tenancy.

2. **Digital Talent Market** -- A community-driven marketplace of verified, benchmark-validated agent Talents. An HR agent autonomously queries the market, shortlists candidates, gets CEO approval, and provisions new employees on demand. Talents can be community-contributed, AI-assembled from web skills, or internally promoted.

3. **Explore-Execute-Review (E2R) Tree Search** -- Project execution is formalized as MCTS-inspired search over a DAG of tasks. The three-stage loop (Explore: decompose & assign; Execute: run via Containers; Review: accept/reject with quality signal) provides structured iteration with formal guarantees: DAG acyclicity, mutual exclusion, review termination, deadlock freedom.

4. **FSM-based Task Lifecycle** -- Each task node follows a finite state machine (pending → processing → completed → accepted / failed). The mandatory `completed → accepted` review gate prevents unreviewed outputs from propagating. Bounded retry paths and circuit breakers (time/cost/round limits) ensure practical termination.

5. **Dual-Level Self-Evolution** -- Individual evolution: agents maintain persistent profiles and working principles updated via CEO one-on-ones and post-task self-reflection. Organizational evolution: project retrospectives distill lessons into updated SOPs injected into future agent contexts; HR conducts performance reviews with automated offboarding for persistent underperformers.

---

## Key Findings

| System | PRDBench Success Rate | Notes |
|--------|----------------------|-------|
| **OMC (this work)** | **84.67%** | Heterogeneous team, zero-shot |
| Minimal Claude-4.5 | 69.19% | +15.48 pp gap |
| Commercial CodeX | 62.09% | |

**Cross-domain case studies:**

- **Content Generation:** Recruited Researcher (GPT-4o) + Writer (Claude Sonnet 4); produced verified GitHub AI-agent trend report + email in <10 min, $4.48
- **Game Development:** Recruited Game Developer + Art Designer (Gemini 2.5); autonomously extended agent skills mid-project to fix sprite segmentation issue; delivered street-fighting web game
- **Audiobook Production:** Recruited Novel Writer + AV Producer (Gemini 3.1 Pro); orchestrated script, image gen, voice synthesis, video assembly for 2 episodes, $1.57
- **Research Survey:** Recruited 3 specialists (Claude Sonnet 4.6 × 2 + self-hosted); generated 17 documents, 70-node mind map, 35+ papers surveyed, 3 novel research proposals in <1 hour, $16.26

Key drivers of performance: dynamic task tree adaptation, enforced review gate (`completed→accepted`), and Talent--Container separation enabling heterogeneous recruitment.

---

## Suggestions & Future Directions

1. **Cost transparency benchmarking** -- Report per-task costs for baselines to enable cost-efficiency comparisons (current paper only reports OMC's own costs).
2. **Talent Market scaling** -- Expand the community ecosystem of verified Talents beyond the initial set; develop automated quality validation pipelines for contributed agents.
3. **Security and trust** -- Investigate sandboxing, access control, and trust hierarchies within OMC organizations, especially for externally recruited Talents.
4. **Adaptive dispatch optimization** -- Extend the simple-task bypass mode (avoiding full multi-agent coordination for trivial subtasks) with learned routing policies.
5. **Foundation model independence** -- Evaluate OMC with smaller/open-source models to assess whether the organizational layer can compensate for weaker individual agents.
6. **Formal verification of SOPs** -- As organizational SOPs evolve through retrospectives, develop methods to verify they remain consistent and non-contradictory.

---

## Authors & Institutions

Zhengxu Yu (HUAWEI Noah's Ark Lab), Yu Fu (HUAWEI Noah's Ark Lab), Zhiyuan He (HUAWEI Noah's Ark Lab), Lee Ka Yiu (HUAWEI Noah's Ark Lab), Weilin Luo (HUAWEI Noah's Ark Lab), Yuxuan Huang (University of Liverpool), Meng Fang (University of Liverpool), Jun Wang (University College London)
