---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: Spec-driven development with AI: Get started with a new open source toolkit - The GitHub BlogLinkedIn iconInstagram iconYouTube iconX iconTikTok iconTwitch icon

### Q1. What is spec-driven development with Spec Kit, and what role split does it enforce?

> [!tip]- Answer
> Spec-driven development makes the specification the living, executable center of engineering that drives implementation, checklists, and task breakdowns rather than a static document written once. The developer's primary role is to steer and verify while the coding agent does the bulk of the writing across the Specify → Plan → Tasks → Implement flow. You return to and refine the spec as complexity grows instead of letting code drift from intent. See [[wiki/01-spec-driven-process-with-spec-kit|What is the spec-driven process with Spec Kit?]].

### Q2. What are the four phases of the Spec Kit flow, and what does each phase produce?

> [!tip]- Answer
> Specify turns a high-level what and why into a detailed spec of user journeys, experiences, and success criteria. Plan turns stack, architecture, and constraints into a comprehensive technical plan, and Tasks decomposes spec plus plan into small, isolated, testable chunks. Implement then produces focused, reviewable changes per task, one by one or in parallel, with a checkpoint gate before each next phase. See [[wiki/01-spec-driven-process-with-spec-kit|What is the spec-driven process with Spec Kit?]].

### Q3. What belongs in Specify versus Plan, and why does the order matter?

> [!tip]- Answer
> Specify captures only the what and why — who uses it, what problem it solves, how they interact, and what outcomes matter — with no stack or app-design decisions. Plan then captures the technical how: stack, architecture, company standards, legacy integrations, compliance, and performance targets, optionally with multiple variations or internal-docs patterns. Keeping this order prevents premature technical commitments from distorting the user outcomes the spec must first nail down. See [[wiki/01-spec-driven-process-with-spec-kit|What is the spec-driven process with Spec Kit?]].

### Q4. What makes a good Tasks breakdown, and how does Implement differ from a typical AI code dump?

> [!tip]- Answer
> Good tasks are small, reviewable, and isolated, each implementable and testable in isolation — for example "create a user registration endpoint that validates email format" rather than "build authentication". This enables a TDD-like validation loop for the agent instead of one unreviewable thousand-line dump. Implement then works through that list task by task because the agent already knows the what, how, and order from the spec, plan, and tasks. See [[wiki/01-spec-driven-process-with-spec-kit|What is the spec-driven process with Spec Kit?]].

### Q5. What does the developer verify at each checkpoint before advancing phases?

> [!tip]- Answer
> At each phase the developer reflects and refines rather than just steering: does the spec capture what you actually want to build, does the plan account for real-world constraints, and are there omissions or edge cases the AI missed. The rule is "the AI generates the artifacts; you ensure they're right," so you critique gaps and course-correct before moving forward. Skipping verification lets spec errors compound into plan and task errors downstream. See [[wiki/01-spec-driven-process-with-spec-kit|What is the spec-driven process with Spec Kit?]].

### Q6. What steering commands drive the Spec Kit workflow, and which agents are named as supported?

> [!tip]- Answer
> You initialize with `specify init <PROJECT_NAME>` via `uvx --from git+https://github.com/github/spec-kit.git`, then use `/specify` for the what/why spec, `/plan` for the technical plan under your constraints, and `/tasks` for the actionable list the agent implements. The chunk names GitHub Copilot, Claude Code, and Gemini CLI as supported agents for this loop. These commands keep each phase's input explicit so the agent generates the right artifact at the right time. See [[wiki/01-spec-driven-process-with-spec-kit|What is the spec-driven process with Spec Kit?]].

### Q7. What substantive claims can you draw from the related-posts and page-context chunk?

> [!tip]- Answer
> None: the chunk holds only related-post teasers and newsletter signup boilerplate, so it supports no claims about mechanisms, numbers, or arguments. The "Should you read the code, is RAG dead, and did Skills kill MCP?" heading appears solely as a podcast teaser, and the Copilot-to-Rust rewrite appears only as a related-post blurb. Any summary citing this chunk for RAG, Skills-vs-MCP, or reading-code positions would be fabricating content. See [[wiki/02-related-posts-and-context|Related posts and page context]].

### Q8. Should a team with vague requirements and legacy constraints adopt the Spec Kit flow, and why?

> [!tip]- Answer
> Yes, that is the strongest case: forcing Specify first turns vague asks into validated user journeys and success criteria, while Plan explicitly surfaces legacy, compliance, and performance constraints before tasks are cut. The checkpoint discipline and small testable tasks then catch AI-generated gaps early instead of in one giant unreviewable diff. I would recommend it over freeform prompting whenever correctness and reviewability matter more than a quick prototype. See [[wiki/01-spec-driven-process-with-spec-kit|What is the spec-driven process with Spec Kit?]].
