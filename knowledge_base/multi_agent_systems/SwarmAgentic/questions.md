> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]] | [[explainer|Explainer]]

# SwarmAgentic — Retrieval practice

## Section 1: SwarmAgentic overview

### Q1: What three autonomy properties does SwarmAgentic satisfy, and which compared frameworks satisfy how many?

<details>
<summary>Answer</summary>
SwarmAgentic is the only compared framework satisfying all three: from-scratch agent generation, self-optimizing agent functionality, and self-optimizing agent collaboration. Solo Performance Prompting satisfies none, Evolutionary Agent and AgentSquare satisfy only functionality, and AutoAgents, AFlow, Agent Symbolic Learning, and Automated Design of Agentic Systems satisfy functionality plus collaboration but not from-scratch generation.
</details>

### Q2: On TravelPlanner with the GPT-4o executor, what scores does SwarmAgentic report, and what is the headline relative gain?

<details>
<summary>Answer</summary>
With GPT-4o reporting, SwarmAgentic reaches 100.0 delivery rate, 92.9 commonsense macro, 56.1 hard-constraint macro, 66.7 final-pass macro, and 32.2 final rate, beating Automated Design of Agentic Systems on every constrained metric. The headline claim is a 261.8% relative gain over Automated Design of Agentic Systems on TravelPlanner.
</details>

### Q3: Why does the framework diagnose explicit flaws before computing each velocity update instead of moving on fitness scores alone?

<details>
<summary>Answer</summary>
Scalar fitness says a team is bad but not what is broken, so arbitrary edits would waste iterations. The flaw diagnosis splits failures into agent flaws (missing, redundant, or vaguely instructed agents) and workflow flaws (missing or redundant steps, incomplete inputs, misaligned outputs), and every velocity term is conditioned on those flaws so fixes target real bottlenecks and stay interpretable.
</details>

### Q4: Suppose you applied SwarmAgentic's joint optimization to Multilingual Grade School Math, a structured task where templates might suffice. What does the paper report, and what does it imply?

<details>
<summary>Answer</summary>
SwarmAgentic still leads with 65.6 / 88.4 on Multilingual Grade School Math and discovers a 6-step 5-role pipeline ending in calculation plus integration specialists. The implication drawn is that full from-scratch autonomy does not trade off template-compatible performance: it wins where templates fail and still wins where templates could work.
</details>

## Section 2: Autonomy criteria, experimental setup, and implementation

### Q5: What are the exact training/evaluation splits for the four benchmark families?

<details>
<summary>Answer</summary>
Multilingual Grade School Math uses 128 train and 800 test; Creative Writing uses 5 train and 95 test out of 100 tasks; Natural Plan uses 8 Trip Planning plus 10 Meeting and 10 Calendar Scheduling training examples with a disjoint 10% held-out validation set; TravelPlanner uses 9 train queries against 180 evaluation queries.
</details>

### Q6: How does SwarmAgentic differ from MODEL SWARMS in objective, search space, and output?

<details>
<summary>Answer</summary>
MODEL SWARMS interpolates pretrained model weights to emit a single opaque adapted model, while SwarmAgentic searches a language design space and constructs executable multi-agent systems from task descriptions alone, using a Failure-Aware Velocity Update that symbolically rewrites roles and workflows into a modular interpretable team.
</details>

### Q7: What breaks if failure-driven learning is removed from the velocity update, and what number quantifies it?

<details>
<summary>Answer</summary>
Without the failure term the optimizer can reintroduce previously failed adjustments and gets stuck re-fixing persistent defects. In the 20-instance Creative Writing ablation at 5 particles and 10 iterations, removing failure-driven adjustments drops the score from the full 8.8 to 8.4, while removing agent-level adaptation drops it to 7.3 and removing collaborative-structure reconfiguration drops it to 6.7.
</details>

### Q8: A colleague proposes seeding the swarm with 7 hand-written agents "to speed things up," as Automated Design of Agentic Systems does. What autonomy property would this sacrifice, and why does the paper argue against it?

<details>
<summary>Answer</summary>
It would sacrifice from-scratch generation, since task-specific reasoning and coordination would come from human templates rather than being synthesized from the task. The paper argues fixed seeds impose structural priors that hinder adaptation to novel open-ended tasks, and attributes part of the ADAS gap to its growing archive of past workflows exhausting context and prioritizing novelty over optimization.
</details>

## Section 3: Optimization prompts, case study, and discovered systems

### Q9: What are the three role operations and five workflow operations shared by all optimizer prompts?

<details>
<summary>Answer</summary>
Role operations are Add Role (name, responsibility, policy), Modify Role (policy refinements within scope), and Delete Role (redundant or conflicting roles). Workflow operations are Add Step (role plus upstream-output input plus expected output), Modify Input, Modify Output, Delete Step, and Re-order Steps without breaking dependencies.
</details>

### Q10: In the travel-planning case study, which distinct fix does each of the three guidance signals contribute?

<details>
<summary>Answer</summary>
Global-best guidance adds a Quality Assurance Specialist for final review; personal-best guidance adds an Accommodation Coordinator cross-verification step between Step 2 and Step 3 checking budget, minimum stays, child suitability, room availability, and room count; failure-driven adjustment hardens the Quality Assurance policy with a mandatory checklist plus explicit budget-compliance item 6 after prior cost violations.
</details>

### Q11: Why does the ADAS TravelPlanner workflow fail on accommodation constraints even though its local proposals look valid?

<details>
<summary>Answer</summary>
Its team of Itinerary Planner, Budget Manager, Dining Advisor, Activity Coordinator, and Meta Decision Agent has no dedicated accommodation owner, so room type, minimum night stays, occupancy limits, and pet-friendliness are never explicitly enforced, and the meta agent cannot integrate locally valid proposals into a globally compliant plan.
</details>

### Q12: You must design a new 8-step travel-planning team for a task with strict pet and budget rules. Which structural lesson from the best-discovered TravelPlanner system would you copy?

<details>
<summary>Answer</summary>
Copy the dedicated ownership plus verification pattern: give accommodation its own coordinator across multiple steps (initial plan, verified details, finalized plan), route dining and attractions off the verified outputs, and end with a Quality Assurance Specialist checklist plus a Travel Plan Integrator that compiles only verified components into the final plan.
</details>

## Section 4: Judgment (see [[critical_thinking|Critical Analysis]])

### Q13: The paper reports a 261.8% relative gain over ADAS on TravelPlanner. What three reasons does the critical analysis give for treating this headline with caution, and what controls would make it durable?

<details>
<summary>Answer</summary>
Relative-gain framing amplifies a small absolute base (final rate 8.9 → 32.2); the comparison pits 5-particle/10-iteration SwarmAgentic against a 30-iteration ADAS budget whose growing workflow archive exhausts context, so part of the gap may come from ADAS search mechanics degrading rather than autonomy alone; and inference cost is never reported, so nothing is normalized by price. The durable version needs matched inference budgets, fixed training subsamples (only 9 TravelPlanner queries drive the search), and non-LLM-judge scoring. See [[critical_thinking|Critical Analysis]].
</details>
