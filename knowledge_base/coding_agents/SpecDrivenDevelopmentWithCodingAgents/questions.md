---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: Spec-Driven Development with Coding Agents - DeepLearning.AI

### Q1. How does the course contrast vibe coding with spec-driven development?

> [!tip]- Answer
> Vibe coding is described as fast but unreliable, often producing code that doesn't match what was asked for. Spec-driven development is the disciplined alternative: write a clear markdown spec defining what to build and let the coding agent implement it, which yields better, more maintainable software. The course claims many of the best developers already work this way to stay in control of complex projects. See [[wiki/01-spec-driven-development-with-coding-agents|Spec-Driven Development with Coding Agents]].

### Q2. What is a project constitution, and why does the course have students write one first?

> [!tip]- Answer
> A project constitution defines the project's mission, tech stack, and roadmap, and students write it by collaborating with the agent. It grounds the work and preserves context across agent sessions, improving intent fidelity and reducing cognitive debt. Everything downstream — feature specs, plans, and validation — builds on this shared grounding. See [[wiki/01-spec-driven-development-with-coding-agents|Spec-Driven Development with Coding Agents]].

### Q3. What are the three phases of the plan-implement-verify workflow, and what happens in each?

> [!tip]- Answer
> In plan, features are planned and validated in iterative loops before any code is written. In implement, the agent builds against the spec as its guide. In verify, the human stays in the loop to validate the result, keeping each feature aligned with intent before moving on. See [[wiki/01-spec-driven-development-with-coding-agents|Spec-Driven Development with Coding Agents]].

### Q4. How does the course carry a greenfield project from a first feature to an MVP?

> [!tip]- Answer
> Students plan, implement, and validate a first feature, then replan between features before building a second feature, compounding into an MVP. Replanning keeps the roadmap and specs current as real implementation lessons accumulate. This replan-per-feature cadence is what turns one-off features into a coherent minimum viable product. See [[wiki/01-spec-driven-development-with-coding-agents|Spec-Driven Development with Coding Agents]].

### Q5. How does the course introduce spec-driven development to a legacy codebase?

> [!tip]- Answer
> Instead of starting from a blank constitution, students use the legacy codebase's existing documentation to generate specs. Those bootstrapped specs then feed the same plan-implement-verify loop used for greenfield work. This shows SDD as applicable to existing projects, not only new ones. See [[wiki/01-spec-driven-development-with-coding-agents|Spec-Driven Development with Coding Agents]].

### Q6. What are the course facts a learner should know before enrolling: level, length, lessons, assessment, and prerequisites?

> [!tip]- Answer
> The course is Beginner level, 1h16m long, with 15 video lessons plus setup readings, and assessment via 1 graded assignment and a 10-minute graded quiz. It is built with JetBrains and taught by Paul Everitt, Developer Advocate at JetBrains, with 0 code examples. Basic familiarity with a programming language and experience with LLM-based coding tools is recommended. See [[wiki/01-spec-driven-development-with-coding-agents|Spec-Driven Development with Coding Agents]].

### Q7. Should a developer who already vibe-codes successfully with LLM tools invest 1h16m in this course, and why?

> [!tip]- Answer
> Yes, if their vibe-coded output ever drifts from intent or becomes hard to maintain, since the constitution plus plan-implement-verify loop and portable agent skill directly target those failure modes. The legacy-codebase and replanning lessons add value beyond greenfield prompting habits they likely already have. I would recommend it as a cheap, structured upgrade whenever correctness and reuse across agents and IDEs matter more than raw prototyping speed. See [[wiki/01-spec-driven-development-with-coding-agents|Spec-Driven Development with Coding Agents]].
