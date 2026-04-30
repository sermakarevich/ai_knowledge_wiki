# AI Planning Framework for LLM-Based Web Agents

**Paper:** [AI Planning Framework for LLM-Based Web Agents (Shahnovsky & Dror, 2025)](https://arxiv.org/abs/2603.12710)

## Human Readable TL;DR

Imagine you're teaching a robot to book a flight online. Some robots figure out each click one at a time, like following a map turn-by-turn. Others make the entire plan before even opening the browser. This paper creates a system to categorize these different "thinking styles" and introduces better report cards to grade not just whether the robot finished the task, but *how well* it navigated along the way -- similar to grading a student's work process, not just their final answer.

## TL;DR

This paper introduces a taxonomy that maps LLM-based web agent architectures to classical AI planning paradigms (step-by-step → BFS, tree search → best-first, full-plan-in-advance → DFS). It proposes five novel trajectory evaluation metrics (Recovery Rate, Repetitiveness Rate, Step Success Rate, Partial Success Rate, Element Accuracy Rate) beyond binary success/failure, and contributes a 794-task human-annotated gold-standard dataset from WebArena. Experiments show step-by-step agents align better with human trajectories (82% vs. 58% Step Success Rate) while full-plan-in-advance agents execute their planned actions more precisely (89.89% vs. 82.45% Element Accuracy Rate).

---

## Problem & Motivation

LLM-based web agents have proliferated rapidly (ReAct, Tree of Thoughts, etc.) without a unified framework connecting them to decades of AI planning theory. Their "black-box" nature makes it hard to diagnose why they fail -- context drift, incoherent decomposition, and repetitive loops go undetected. Existing benchmarks (WebArena, MiniWoB++) only measure binary task success, masking substantial partial progress and hiding qualitative differences in agent behavior.

---

## Main Original Ideas

1. **AI Planning Taxonomy for Web Agents** -- Formally maps three LLM agent architectures to classical planning paradigms using a POMDP formulation: Step-by-Step (BFS/depth-1 search), Tree Search (best-first heuristic traversal), and Full-Plan-in-Advance (DFS, complete trajectory before execution). Provides a principled vocabulary for analysis and failure diagnosis.

2. **Five Novel Trajectory Evaluation Metrics** -- Moves evaluation beyond binary success:
   - *Recovery Rate*: can the agent realign with the human gold path after deviating?
   - *Repetitiveness Rate*: what fraction of actions are non-redundant?
   - *Step Success Rate*: what proportion of human gold steps does the agent fulfill?
   - *Partial Success Rate*: for multi-element tasks, how many required elements are satisfied?
   - *Element Accuracy Rate*: does the agent execute the action it planned?

3. **LLM-as-Judge Evaluation Framework** -- Uses an LLM with chain-of-thought prompting and explicit criteria to perform semantic equivalence judgments between agent and human steps, enabling nuanced trajectory comparison at scale.

4. **Full-Plan-in-Advance Agent Implementation** -- Novel agent that generates a complete numbered action plan before execution, feeds the plan as persistent context in every prompt to resist context drift, and executes via Playwright against accessibility-tree web representations.

5. **Human-Annotated WebArena Dataset** -- 794 tasks from WebArena annotated with complete gold-standard human execution traces (action type + element name per step), enabling reference-based trajectory evaluation.

---

## Key Findings

| Metric | WebArena (Step-by-Step) | Full-Plan-in-Advance |
|---|---|---|
| Overall Success Rate | **38.41%** | 36.29% |
| Step Success Rate | **82%** ± 0.14 | 58% ± 0.29 |
| Element Accuracy Rate | 82.45% ± 0.12 | **89.89%** ± 0.03 |
| Repetitiveness Rate | 79% ± 0.14 | **81%** ± 0.13 |
| Recovery Rate | **36%** ± 0.19 | 31% ± 0.12 |
| Partial Success Rate | **0.22%** ± 0.39 | 0.12% ± 0.27 |
| Avg. trajectory length | 15.02 ± 8.93 steps | 20.21 ± 10.16 steps |

- Human trajectories averaged **7.92 ± 5.18 steps** -- both agents take roughly 2-3× more steps than humans.
- Full-Plan-in-Advance improved on **Reddit (+4%)** and **e-commerce (+4%)** but degraded on CMS, GitLab, and Map domains.
- Full-Plan-in-Advance plans frequently omit essential steps or insert unnecessary ones (e.g., redundant information extraction) because the LLM cannot predict runtime UI elements at plan time.
- Both agents exhibit high early-stop rates (24-28 tasks) due to repeated/invalid actions, not inherent task impossibility.

---

## Suggestions & Future Directions

1. **Hybrid planning agents** -- Combine step-by-step reactivity with global plan constraints to get both high recovery and high element accuracy; neither pure paradigm dominates.
2. **Domain-adaptive planning strategy selection** -- Deploy Full-Plan-in-Advance for structured, predictable environments (SAP, e-commerce, CMS) and Step-by-Step for dynamic, data-dependent ones (social media, cloud consoles).
3. **Richer plan generation** -- Improve the Full-Plan-in-Advance agent's ability to handle unseen runtime UI elements and avoid redundant steps by grounding plan generation in real accessibility trees.
4. **Extend taxonomy to non-web domains** -- The POMDP-based taxonomy generalizes to robotics, GUI automation, and multimodal systems.
5. **Release the dataset** -- The 794-task human-annotated dataset should serve as a community benchmark for trajectory-level evaluation beyond WebArena's binary metrics.
6. **Optimize LLM judge prompts** -- Further validate and refine the LLM-as-judge prompts for each metric to ensure consistency and reduce scoring variance.

---

## Authors & Institutions

Orit Shahnovsky (University of Haifa, Israel), Rotem Dror (University of Haifa, Israel)
