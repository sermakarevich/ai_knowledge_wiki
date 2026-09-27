# SwarmAgentic: Towards Fully Automated Agentic System Generation via Swarm Intelligence

**Paper:** [SwarmAgentic: Towards Fully Automated Agentic System Generation via Swarm Intelligence (Yao Zhang et al., 2025)](https://arxiv.org/abs/2506.15672)

## Human Readable TL;DR

Imagine you need to plan a complicated group trip with strict budgets, room rules, and dietary needs, but instead of hiring a travel agency you ask a computer to invent the whole agency from nothing — the travel planner, the hotel checker, the restaurant picker, and a quality inspector who reviews everything at the end. SwarmAgentic does exactly that: given only a short job description and a scoring rule, it creates several candidate teams of Artificial Intelligence assistants, tests them, diagnoses what went wrong in plain words, and keeps reshuffling roles and workflows the way a flock of birds collectively searches for food. The result is a specialized, inspectable team that beats hand-built setups, most strikingly on travel planning where it scores far higher than the previous best automated method while obeying far more of the user's strict requirements.

---

## TL;DR

SwarmAgentic is a fully automated framework that constructs multi-agent systems from scratch and jointly optimizes agent functionality and collaboration through language-driven Particle Swarm Optimization (PSO), a gradient-free population-based search method inspired by bird flocking in which each candidate team is treated as a particle guided by its personal best and the swarm's global best. Each system is formalized as a particle encoding an agent set plus a collaborative workflow, where every agent is a triple of identifier, responsibility, and execution policy, and every update cycle runs Large Language Model (LLM)-driven flaw diagnosis followed by a failure-aware velocity update and a position update using Add, Delete, Modify, and Reorder operators. Given only a task description and an objective function, and using 5 particles over 10 iterations with GPT-4o-mini as optimizer, it leads all baselines across TravelPlanner, Natural Plan, Creative Writing, and Multilingual Grade School Math (MGSM), with a headline 261.8% relative gain over Automated Design of Agentic Systems (ADAS) on TravelPlanner.

---

## Problem & Motivation

Existing frameworks for automatically building agentic systems lack full autonomy: none of them invents teams from scratch while simultaneously improving both individual agent behavior and team collaboration. Prior methods depend on hand-written seed agents, fixed templates, frozen interaction patterns, or predefined agent modules, which imposes engineering overhead every time the task changes and breaks down on open-ended exploratory tasks such as long-horizon trip planning under many interacting constraints, where nobody knows the right division of labor in advance. This matters because manual design of roles and coordination strategies is prohibitively complex and hard to scale, so a practical framework must synthesize complete agent instances, refine their internal logic from feedback, and restructure sequencing, dependencies, and coordination without human intervention.

---

## Main Original Ideas

1. **From-scratch generation with joint functionality-collaboration optimization** — SwarmAgentic synthesizes all roles, decision logic, and coordination flows from the task context alone, with no predefined functional modules beyond minimal task-agnostic scaffolding, and refines agent internals and workflow structure together as interdependent components rather than optimizing them separately or freezing collaboration as a static template.

2. **Particle formalization of agentic systems** — Each candidate system is encoded as a particle whose position is the current team configuration and whose velocity is the planned set of textual edits, with fitness scored by the task objective function, so that the numerical PSO update rules for inertia, personal-best attraction, and global-best attraction are reinterpreted as semantic transformations over structured language representations.

3. **Explicit flaw identification before every move** — Unlike classic PSO, which moves on scalar fitness alone, an LLM diagnoses the error set into agent flaws (missing agents, redundant agents, ambiguous policies) and collaborative-structure flaws (missing or redundant steps, incomplete inputs, misaligned outputs), so that every downstream velocity term is conditioned on real bottlenecks and stays interpretable.

4. **Failure-aware velocity update** — The velocity plan fuses three signals: failure-driven adjustments that detect persistent defects by comparing the prior plan against prior and current flaws and prune ineffective corrections, personal-best guidance that extracts transferable improvements from the particle's own history, and global-best guidance that imports swarm-wide excellence, with the latter two forced to quote exact phrases from the reference team so transfer stays grounded.

5. **Shared operator catalog with planning-compilation separation** — All optimizer prompts speak the same edit language of three role operations (Add Role, Modify Role, Delete Role) and five workflow operations (Add Step, Modify Input, Modify Output, Delete Step, Re-order Steps), and the velocity prompt plans the adjustment while a separate position-update prompt compiles it into a refined team, keeping diagnosis, guidance fusion, and code generation inspectable.

---

## Key Findings

| Benchmark (executor GPT-4o unless noted) | SwarmAgentic | Closest baseline (ADAS) |
|---|---|---|
| TravelPlanner delivery rate | 100.0 | 100.0 (tied) |
| TravelPlanner commonsense macro | 92.9 | 82.6 |
| TravelPlanner hard-constraint macro | 56.1 | 34.4 |
| TravelPlanner final-pass macro | 66.7 | 35.0 |
| TravelPlanner final rate | 32.2 | 8.9 |
| Natural Plan trip / meeting / calendar | 13.1 / 56.0 / 82.0 | behind in every column |
| Creative Writing (GPT-3.5 / GPT-4o) | 8.2 / 8.5 | behind in every column |
| MGSM (GPT-3.5 / GPT-4o) | 65.6 / 88.4 | behind in every column |

- The headline claim is a 261.8% relative improvement over ADAS on TravelPlanner, supported by large gaps on the constrained metrics (for example hard-constraint macro 56.1 versus 34.4 and final rate 32.2 versus 8.9), with the authors attributing the ADAS gap partly to its growing archive of past workflows exhausting context and prioritizing novelty over optimization.
- A travel-planning trace shows each guidance signal fixing a distinct defect: global-best guidance adds a Quality Assurance Specialist for final review, personal-best guidance inserts an Accommodation Coordinator cross-verification step checking budget, minimum stays, child suitability, room availability, and room count, and failure-driven adjustment hardens the reviewer into a mandatory checklist with an explicit budget-compliance item after prior cost violations.
- Ablation on 20 Creative Writing instances at 5 particles and 10 iterations scores the full configuration at 8.8 (a 41.9% gain over Direct), dropping to 6.7 without collaborative-structure reconfiguration, 7.3 without agent-level adaptation, and 8.4 without failure-driven adjustments, confirming every mechanism matters and workflow restructuring matters most.
- Cross-model transfer holds: a system discovered with GPT-4o-mini still leads when executed on GPT-4o (8.5), Claude-3.5-sonnet (8.3), DeepSeek-V3 (9.0), and Gemini-1.5-Pro (7.5) on Creative Writing, and the best-discovered systems are published as executable programs (6 steps and 5 roles for MGSM, 10 steps and 10 roles for Creative Writing, 7 steps and 7 roles for meeting scheduling, 8 steps and 5 roles for TravelPlanner ending in a Travel Plan Integrator).
- The ADAS TravelPlanner workflow comparison shows why seeds fail: its team of Itinerary Planner, Budget Manager, Dining Advisor, Activity Coordinator, and Meta Decision Agent has no dedicated accommodation owner, so room type, minimum night stays, occupancy limits, and pet-friendliness are never explicitly enforced and the meta agent cannot integrate locally valid proposals into a globally compliant plan.

---

## Suggestions & Future Directions

1. **Add constraint-guided initialization with domain templates** — The authors acknowledge the system starts with no inductive priors or domain-specific templates that could accelerate convergence on routine structured problems, and propose seeding the swarm with constraint-aware starting points while preserving from-scratch flexibility.
2. **Ground optimization with external knowledge to curb hallucinations** — Because model hallucinations can propagate through the diagnosis and rewriting loop, future work should attach external knowledge sources or verifiers so false diagnoses do not compound across iterations.
3. **Extend beyond text to multimodal and embodied settings** — The current framework operates purely on text with no perception or physical action, so the authors propose integrating multimodal models and embodied agents to bridge the gap to real-world contexts.
4. **Open question of cost and scale** — The paper fixes the main configuration at 5 particles and 10 iterations against a 30-iteration ADAS budget but does not fully characterize inference cost, context growth, or behavior at larger swarm sizes, leaving the cost-versus-quality frontier open.

---

## Authors & Institutions

Yao Zhang (LMU Munich, Munich Center for Machine Learning), Chenyang Lin (Technical University of Munich), Shijie Tang (LMU Munich), Haokun Chen (LMU Munich), Shijie Zhou (Technical University of Munich), Yunpu Ma (LMU Munich, Munich Center for Machine Learning), Volker Tresp (LMU Munich, Munich Center for Machine Learning).
