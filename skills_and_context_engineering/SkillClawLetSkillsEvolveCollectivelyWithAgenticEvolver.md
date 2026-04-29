# SkillClaw: Let Skills Evolve Collectively with Agentic Evolver

**Paper:** [SkillClaw: Let Skills Evolve Collectively with Agentic Evolver (Ma et al., 2026)](https://arxiv.org/abs/2604.08377)

## Human Readable TL;DR

Imagine a company where every employee solves problems independently, but nobody shares what they learned -- so the same mistakes keep happening. SkillClaw is like adding a "lessons learned" system that automatically watches everyone work, figures out what went wrong and what went right, writes better instruction manuals overnight, and distributes them to the whole team the next morning. Over just 6 days, the AI assistants using this system got substantially better at their jobs without anyone manually updating anything.

## TL;DR

SkillClaw introduces a closed-loop framework for collective skill evolution in multi-user LLM agent ecosystems. It aggregates interaction trajectories from diverse users, groups them by skill usage, and employs an autonomous LLM-based "agentic evolver" to refine existing skills or create new ones. A nighttime validation loop ensures only improvements are deployed, achieving monotonic capability growth. Evaluated on WildClawBench over 6 simulated days, SkillClaw yields up to +42.1% gains on controlled tasks and consistent improvements across all benchmark categories.

---

## Problem & Motivation

Current LLM agent skill ecosystems are fundamentally static -- skills are manually installed, maintained, and never updated based on runtime experience. When agents encounter failures (wrong tool arguments, misordered API calls, missing validation), they may discover workarounds through trial and error, but these fixes die with the session. Since users operate in overlapping task spaces with shared tools and failure modes, the same problems get independently rediscovered and resolved over and over. There is no mechanism to convert heterogeneous, cross-user interaction experience into reliable, collective skill improvements. SkillClaw addresses this gap by enabling skills to evolve automatically from aggregated multi-user interactions.

---

## Main Original Ideas

1. **Collective Skill Evolution Pipeline** -- A closed-loop architecture (Interaction -> Evidence -> Evolution -> Validation -> Deployment) that aggregates interaction sessions from multiple concurrent users, enabling cross-user knowledge transfer without any manual curation.

2. **Agentic Evolver** -- An autonomous LLM agent that serves as the evolution engine. Rather than following predefined update rules, it performs open-ended reasoning over grouped session evidence, diagnosing root causes and formulating skill updates through three actions: Refine, Create, or Skip.

3. **Causal Chain Preservation with Skill-Based Grouping** -- Raw interaction sessions are structured to preserve the full causal chain (prompt -> actions -> feedback -> response), then grouped by skill usage (`G(s)` for skill-specific sessions, `G(null)` for unmatched sessions), creating natural ablation studies across users and contexts.

4. **Nighttime Validation Loop** -- Candidate skill updates are not deployed directly. They undergo comparative execution against the original skill under identical conditions during off-peak hours. Only updates demonstrating measurable improvement are accepted, ensuring monotonic capability growth.

5. **Conservative Editing Principles** -- The evolver distinguishes between skill deficiencies, agent misuses, and environmental issues, applying targeted edits over complete rewrites and preserving validated behavior from successful sessions.

---

## Key Findings

### WildClawBench Results Over 6 Days (Qwen3-Max backbone)

| Category             | Day 1 (Baseline) | Day 2   | Day 4   | Day 5   | Day 6   |
|----------------------|:-----------------:|:-------:|:-------:|:-------:|:-------:|
| Social Interaction   | 54.01%            | **60.34%** | 60.34%  | 60.34%  | 60.34%  |
| Search & Retrieval   | 22.73%            | 30.00%  | **34.55%** | 34.55%  | 34.55%  |
| Creative Synthesis   | 11.57%            | **21.80%** | 21.80%  | 21.80%  | 21.80%  |
| Safety & Alignment   | 24.00%            | 24.00%  | 24.00%  | **32.00%** | 32.00%  |

- Controlled validation on custom queries shows an average **+42.1%** gain after a single evolution round
- "Save report" tasks improved from 28.3% to **100.0%**, fully correcting procedural errors around output paths and formats
- "Basic extraction" saw a **+47.8%** gain from capturing recurring execution patterns
- "Deadline parsing" showed a smaller +6.9% improvement, suggesting tasks reliant on nuanced reasoning benefit less from procedural skill updates
- Evolution patterns differ by category: Social Interaction saw rapid early gains from workflow restructuring; Search & Retrieval showed staged improvement (low-level reliability first, then higher-level reasoning); Creative Synthesis resolved environment setup bottlenecks early; Safety & Alignment improved later through execution reliability fixes (e.g., Git fallback strategies)

---

## Suggestions & Future Directions

1. **Scaling users and interaction depth** -- Explore how the framework performs with significantly more concurrent users and longer interaction histories to test the limits of collective learning.

2. **More sophisticated validation conditions** -- Develop richer evaluation criteria beyond task success and execution stability for the accept/reject decision in the validation loop.

3. **Long-term evolution dynamics** -- Investigate how skill quality trajectories behave over extended deployment periods (weeks or months) and whether skills converge, oscillate, or continue improving.

4. **Multi-skill coordination** -- Extend the agentic evolver to reason about interactions between skills and perform coordinated updates across dependent skill chains.

5. **Abstract reasoning over aggregated evidence** -- Develop evolvers capable of higher-order reasoning that can identify systemic patterns across skill groups rather than analyzing skills in isolation.

6. **Reasoning-heavy task limitations** -- The framework is most effective for procedural failures; tasks requiring deep nuanced reasoning (e.g., deadline parsing) show smaller gains, indicating a need for complementary approaches to improve reasoning capabilities.

---

## Authors & Institutions

Ziyu Ma (DreamX Team, equal contribution), Shidong Yang (DreamX Team, equal contribution), Yuxiang Ji (DreamX Team, equal contribution), Xucong Wang (DreamX Team, equal contribution), Yong Wang (DreamX Team, project lead), Yiming Hu (DreamX Team), Tongwen Huang (DreamX Team), Xiangxiang Chu (DreamX Team)
