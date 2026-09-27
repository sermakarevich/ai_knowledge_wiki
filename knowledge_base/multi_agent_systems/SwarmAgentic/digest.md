> [[index|Wiki]] | [[summary|Summary]]

# SwarmAgentic — Digest

The whole source at medium depth: every chapter's headline claim and key points, in order. ~10 min. Descend into a wiki page only where you need the detail.

## 1. [[wiki/01-swarmagentic-overview|SwarmAgentic Overview: Fully Automated Generation via Swarm Intelligence]]

**In one sentence:** SwarmAgentic is a fully automated framework that generates agentic systems from scratch and jointly optimizes agent functionality and collaboration through language-driven Particle Swarm Optimization, achieving a 261.8% relative gain over Automated Design of Agentic Systems on TravelPlanner with only a task description and objective function as input.

- SwarmAgentic is the only framework in the Table 1 comparison satisfying all three autonomy criteria, namely from-scratch agent generation, self-optimizing agent functionality, and self-optimizing agent collaboration, while Solo Performance Prompting satisfies none and Evolutionary Agent, AgentSquare, AutoAgents, AFlow, Agent Symbolic Learning, and Automated Design of Agentic Systems satisfy only subsets.
- Each agentic system is formalized as a particle encoding an agent set and a collaborative structure, where each agent is a triple of identifier, responsibility, and execution policy, and fitness is scored by a task objective function.
- Optimization reinterprets Particle Swarm Optimization in language space with Large Language Model-driven flaw identification, failure-aware velocity updates combining failure-driven adjustments with personal-best and global-best guidance, and position updates applying Add, Delete, Modify, and Reorder operators.
- On TravelPlanner with GPT-3.5 / GPT-4o executor reporting, SwarmAgentic reaches 100.0 / 100.0 delivery rate, 70.9 / 92.9 commonsense micro/macro, 12.8 / 56.1 hard-constraint micro/macro, 21.0 / 66.7 final-pass micro/macro, and 3.3 / 32.2 final rate, beating Automated Design of Agentic Systems on every constrained metric.
- Across Natural Plan trip planning, meeting planning, and calendar scheduling plus Creative Writing and Multilingual Grade School Math, SwarmAgentic leads all baselines, for example 13.1 / 13.1 on trip planning, 23.0 / 56.0 on meeting planning, 28.0 / 82.0 on calendar scheduling, 8.2 / 8.5 on Creative Writing, and 65.6 / 88.4 on Multilingual Grade School Math.
- Ablation on 20 Creative Writing instances shows the full 5-particle 10-iteration configuration scoring 8.8 for a 41.9% gain over Direct, with removal of collaborative-structure reconfiguration dropping to 6.7, removal of agent-level adaptation dropping to 7.3, and removal of failure-driven adjustments dropping to 8.4, while cross-model transfer from GPT-4o-mini to GPT-4o, Claude-3.5-sonnet, DeepSeek-V3, and Gemini-1.5-Pro preserves the lead in every case.

## 2. [[wiki/02-autonomy-setup-and-implementation|Autonomy Criteria, Experimental Setup, and SwarmAgentic Implementation]]

**In one sentence:** This chunk defines three autonomy properties and scores seven prior frameworks against them, distinguishes SwarmAgentic from MODEL SWARMS, fixes exact dataset splits and metrics, and publishes the Role and Team code, the Particle Swarm Optimization pseudocode, and the full prompt repository that drives generation and optimization.

- Autonomy is judged on three properties, namely from-scratch agent generation without predefined modules, self-optimizing agent functionality that rewrites an agent's own behavior from feedback, and self-optimizing agent collaboration that restructures sequencing, dependencies, and coordination, with only SwarmAgentic satisfying all three.
- Solo Performance Prompting fails all three properties while Evolutionary Agent and AgentSquare satisfy only functionality, and AutoAgents, AFlow, Agent Symbolic Learning, and Automated Design of Agentic Systems satisfy functionality plus collaboration but fail from-scratch generation.
- MODEL SWARMS optimizes pretrained model weights by interpolation to emit one opaque model, whereas SwarmAgentic constructs executable multi-agent systems from task descriptions with a Failure-Aware Velocity Update that symbolically rewrites roles and workflows.
- Training and evaluation splits are fixed as 128 train and 800 test for Multilingual Grade School Math, 5 train and 95 test out of 100 tasks for Creative Writing, 8 Trip Planning plus 10 Meeting and Calendar Scheduling examples for Natural Plan with a disjoint 10% held-out validation set, and 9 train queries against 180 evaluation queries for TravelPlanner.
- Baselines comprise Direct, Chain-of-Thought, Self-Refine, Solo Performance Prompting, Evolutionary Agent, and Automated Design of Agentic Systems with 7 hand-written seed agents, with prompt wording adapted per task but no extra search beyond each original algorithm.
- The implementation encodes each particle as a Team of Role objects plus generated forward code, searched by Algorithm 1 over at most T iterations with swarm size N, fitness function J, and Large Language Model operators for initialization, evaluation, flaw diagnosis, velocity, and position updates.
- Every velocity step fuses failure-driven learning that must not repeat documented failed adjustments with personal-best and global-best guidance, and every position step applies Add, Modify, Delete, and Reorder operations to roles and to workflow steps including inputs, outputs, and order.

## 3. [[wiki/03-optimization-prompts-case-study-and-discovered-systems|Optimization Prompts, Case Study and Best-Discovered Systems]]

**In one sentence:** This chunk publishes the verbatim global-best, personal-best, velocity-update and position-update prompts that drive SwarmAgentic refinement, walks through a travel-planning case study where each guidance signal fixes a distinct defect, and presents the final best-discovered executable systems for four tasks alongside a detailed comparison showing why the Automated Design of Agentic Systems workflow fails on accommodation constraints.

- Role refinement uses three operations, namely Add Role with name, responsibility and policy when a subtask overburdens existing roles, Modify Role for manageable policy refinements within scope, and Delete Role for redundant or conflicting roles.
- Workflow refinement uses five operations, namely Add Step with role plus upstream-output input plus expected output, Modify Input to incorporate prior outputs, Modify Output to align deliverables with downstream needs, Delete Step for redundant steps, and Re-order Steps to fix sequencing without breaking dependencies.
- Global-best learning with LLMglob and personal-best learning with LLMpers both force a four-part response per flaw of Identified Flaw, Thought, Comparative Insights with explicit quoted phrases, and Proposed Adjustment that reuses only quoted elements or says None.
- The illustrative travel-planning run shows global-best guidance adding a Quality Assurance Specialist for final review, personal-best guidance adding an Accommodation Coordinator cross-verification step between Step 2 and Step 3, and failure-driven adjustment hardening the Quality Assurance policy with a mandatory checklist plus explicit budget-compliance item 6.
- Best-discovered systems are published as executable forward code with 6 steps and 5 roles for Multilingual Grade School Math, 10 steps and 10 roles for Creative Writing, 7 steps and 7 roles for Meeting Scheduling, and 8 steps with 5 roles for TravelPlanner ending in a Travel Plan Integrator.
- The Automated Design of Agentic Systems TravelPlanner workflow uses Itinerary Planner, Budget Manager, Dining Advisor, Activity Coordinator and Meta Decision Agent with collaborative negotiation but no dedicated accommodation agent, so it cannot reliably enforce room type, minimum night stays, occupancy limits or pet-friendliness and often violates global requirements despite locally valid proposals.
- The chunk attributes Automated Design of Agentic Systems search difficulty to an ever-growing archive of full workflow definitions that exhausts context, accumulates irrelevant detail, and prioritizes novelty over optimization so truly optimal workflows are hard to identify.

## The argument in five moves

1. Existing agent-building frameworks lack full autonomy because none invents teams from scratch while self-optimizing both behavior and collaboration.
2. SwarmAgentic formalizes each candidate team as a particle and reinterprets swarm search as language-model-driven diagnosis plus failure-aware velocity and position edits.
3. Fixed dataset splits, metrics, baselines, and a published Role/Team codebase with eleven operators make the setup reproducible and the edits inspectable.
4. A travel-planning trace plus the best-discovered runnable systems show each guidance signal fixing a distinct defect that seed-based ADAS workflows miss.
5. Across TravelPlanner, Natural Plan, Creative Writing, and MGSM the swarm leads every column with transferable, ablatable gains, so full autonomy wins without sacrificing structured tasks.
