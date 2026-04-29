# Spec-Driven Development (SDD) — Course Summary

*Course by Paul Everitt (JetBrains Developer Advocate), built in partnership with JetBrains and DeepLearning.AI (Andrew Ng)*

---

## 1. What Is Spec-Driven Development?

Spec-Driven Development is a workflow for building serious software with agentic coding assistants. Instead of writing code by hand, you write a **markdown specification** — a detailed description of *what* to build and *why* — and let the coding agent implement it. Your job shifts from writing code to writing context the agent doesn't already have.

**The core idea:** you give the agent a structured spec, it produces code. A single sentence in the spec (e.g., "use SQLite with Prisma ORM") can affect hundreds of lines of code. Change that sentence to "use MongoDB" and the downstream amplification is the same. This makes spec-writing far more efficient than code-writing.

---

## 2. SDD vs. Vibe Coding

| Aspect | Vibe Coding | Spec-Driven Development |
|---|---|---|
| Approach | Short prompts, hope for the best, iterate on mistakes | Detailed upfront spec, structured workflow |
| Artifact | Long disposable chat history (not saved) | Permanent, versioned markdown specifications |
| Scalability | Works for a button, breaks on large projects | Scales to complex, multi-feature projects |
| Technical debt | Mounting, disposable code | Controlled, maintainable code |
| Team alignment | Each developer/agent builds in contradictory ways | Constitution creates shared contract |

**Key analogy:** Compilers convert source code → machine code. SDD guides agents to convert specs → source code. The specs are in human language, making them accessible to stakeholders.

---

## 3. Three Core Benefits of SDD

### 3.1 Amplification — Control Large Code Changes with Small Spec Changes
A few sentences about look-and-feel can translate to hundreds of lines of CSS. This reduces cognitive overhead when working with ultra-fast coding agents.

### 3.2 Context Persistence — Eliminate Context Decay
Agents are stateless. As context windows fill up, agents make more mistakes. Specs persist between sessions *and* between agents, anchoring the agent to the core context needed for the codebase. They are the project's memory.

### 3.3 Intent Fidelity — Get Code That Matches Your Goals
Specs force you to define the problem, success criteria, constraints, and user flows *before* code generation. Without specs, critical architectural decisions are left to the whims of the agent.

---

## 4. The SDD Workflow — Big Picture

```
Constitution → [ Feature Loop ] → [ Feature Loop ] → ... → Delivery
                    ↕
               Replanning
```

### Phase 1: Constitution (Project-Level)
Define immutable project standards — mission, tech stack, roadmap.

### Phase 2: Feature Development Loop (Repeatable)
For each feature:
1. **Plan** — Spec the feature in conversation with the agent
2. **Implement** — Agent writes the code
3. **Validate** — Human-in-the-loop review

### Phase 3: Replanning (Between Features)
Revise the constitution, update the roadmap, improve the process itself.

This workflow supports both **greenfield** (new projects) and **brownfield** (existing codebases).

---

## 5. The Constitution

The constitution is a global set of high-level requirements consisting of three documents:

### 5.1 Mission (`mission.md`)
- The *why* of the project
- Vision, target audience, scope, core idea
- Guides ongoing decisions
- Example: AgentClinic — a parody app where AI agents get relief from their humans (hallucinations, context rot, memory issues)

### 5.2 Tech Stack (`tech-stack.md`)
- Engineering-level decisions: frameworks, languages, databases, deployment
- API pipelines, database schemas, treatment catalogs
- Separates architecture decisions from the mission document
- Example: Next.js backend, React frontend, SQLite, TypeScript

### 5.3 Roadmap (`roadmap.md`)
- A living document with a sequence of phases
- Each phase becomes a feature spec
- Organized in small steps for human-in-the-loop review

### How to Write the Constitution
- **Don't write it alone** — write it in conversation with the agent
- The agent asks great questions: architecture patterns you hadn't considered, existing packages, tradeoffs (speed vs. data fidelity)
- Provide the agent with any existing artifacts (README, TODO files, stakeholder input)
- Use the agent's `AskUserQuestion` tool for structured interviews
- Review, correct, and commit — the constitution is a living, versioned document

---

## 6. Feature Specification Phase

### 6.1 Planning
- Start with a fresh agent context (`/clear`) — let the agent get what it needs from the constitution
- Create a feature branch
- Engage in a conversation with the agent to produce three documents:
  - **Plan** — approach, sequence of work, task groups
  - **Requirements** — technical constraints, dependencies, versions
  - **Validation/Scorecard** — how to verify success (manual tests, curl commands, automated tests)

### Key Principles
- Pin versions (e.g., Hono version), enforce strict TypeScript
- Don't oversteer — control the process but let the agent handle low-level details
- If something is wrong, ask the agent to fix it (not manually) to keep all artifacts in sync
- Commit the feature spec before implementation

### 6.2 Implementation
- Clear context again before implementation
- Tell the agent to implement all task groups (or one at a time for sensitive areas like security/database)
- Watch the agent's progress in real time
- The developer's role: architect/supervisor ensuring a clear contract

### 6.3 Validation
- Review changes in the commit view
- Focus on **high-level concerns** (does the feature work, does it reflect the spec?) — not low-level details like CSS classes or variable names
- If code doesn't match the spec, ask the agent to fix both spec and implementation
- Run the application and tests
- Use the debugger to step through code as exploration
- **Deep review technique:** Tell the agent to spawn sub-agents for a thorough review of the entire project — they find issues without polluting the main agent's context window
- Commit, then merge

---

## 7. Replanning Phase

Replanning happens between features and serves multiple purposes:

### 7.1 Constitution Updates
- Update tech stack (e.g., add testing framework preferences)
- Tell the agent to propagate constitution changes to existing feature specs and implementation
- Work in a separate branch to track which constitution version produced which code

### 7.2 Responding to Product Changes
- Example: "40% of users are on mobile → emphasize responsive design"
- Small changes can be implemented directly during replanning
- Large changes should be scheduled on the roadmap as their own feature phase

### 7.3 Roadmap Review
- Does the next feature still make sense?
- Can features be combined or reordered?
- Example: Features 2-5 hang together → tackle them in one step

### 7.4 Workflow Improvement
- Write **agent skills** to automate repetitive SDD tasks
- Example: A changelog skill that auto-generates CHANGELOG.md on each merge

---

## 8. Managing AI Fatigue and Cognitive Debt

**AI fatigue** = exhaustion from reviewing massive amounts of agent-generated code.  
**Cognitive debt** = mental load of tracking what code is doing and how it evolved.

### Strategies
- **Clean breaks between features** — start each feature in the right flow state
- **Checklist before starting:** Unfinished work? Last branch merged? Next roadmap item correct? Context cleared?
- **Small steps, frequent commits** — keep review from overloading your brain
- **Avoid nitpicking** — skip variable names, focus on high-level requirements
- **Right level of detail in specs** — treat agent as a capable pair programmer; lots of context on goals, less on low-level implementation details
- **Deep review with sub-agents** — preserves main context window
- **Tests under debugger** — validate understanding, not just correctness

---

## 9. The MVP Experiment

After building a solid constitution and two features, you can attempt a larger implementation:

- Tell the agent to implement the remaining roadmap in one go
- This is an **extreme test of your constitution and specs**
- If the result diverges from intent → you need more rigorous replanning
- Only do this when you're confident in spec quality and can handle the review
- Use the agent to validate specs against the implementation and report gaps
- Share the evaluation with stakeholders for MVP review

---

## 10. Legacy / Brownfield Projects

SDD is not just for greenfield. For existing codebases:

1. **Reverse-engineer the constitution** — The agent explores the codebase (file structure, framework versions, existing docs like README, TODO) and generates mission, tech-stack, and roadmap
2. **Align future changes** — The constitution ensures new agent-generated code is consistent with past developer decisions
3. **Standard feature loop** — From here, the workflow is identical: plan → implement → validate → replan
4. **Expect a richer conversation** — More existing artifacts (code, commits, docs) provide more context
5. **Tune aggressively** — First replanning after adopting SDD will likely uncover many things to adjust

---

## 11. Skills, Tools, and Automation

### 11.1 Agent Skills
- A package of instructions and resources giving the agent new capabilities
- Great for definable, repeatable workflows with project-specific context
- Can be **per-project** or **global** (across all projects)
- Examples: feature spec skill (automates the "start a feature" prompt), changelog skill, validation skill (linting, formatting, test writing, quality checks)
- Use the agent's skill creator to write skills through conversation
- Invoke by naming the skill in your prompt, or have skills call other skills

### 11.2 MCP (Model Context Protocol)
- Universal way to extend agents with external access (APIs, knowledge bases, databases)
- Example: Context7 MCP brings updated package documentation into agent context
- **Trend:** Moving from MCP servers → Skills + CLI tools (less setup, less context usage)

### 11.3 Plugins
- Collections of agent extensions that can be installed and updated
- Growing community of free plugins
- Not yet a cross-agent standard — trust them carefully on install/update

### 11.4 Community Frameworks
- **GitHub Spec Kit** — Formalized SDD workflow with `/commands`: constitution, plan, tasks, implement
- **OpenSpec (Fission AI)** — Propose → Explore → Apply → Archive workflow with canonical patterns for quick features
- Both include branch management, verification scripts, opinionated spec formats

### 11.5 Research Backlog
- When you have an idea mid-feature but don't want to disrupt current work
- Have the agent write a report to a well-known backlog location
- Later, schedule the research on the roadmap with a link to the backlog file

---

## 12. Agent Replaceability and Standards

SDD moves work from *how* to *what and why*, decoupling specs from any specific agent. Key standards:

| Standard | Purpose |
|---|---|
| **MCP** | External tool integration |
| **AGENTS.md** | Rules and conventions for agents |
| **Agent Skills** | Repeatable workflows with extra context |
| **ACP (Agent Client Protocol)** | Connecting agents to editors/clients |

### ACP in Practice
- Plug-and-play between agents and IDEs
- ACP Registry automates finding, installing, and connecting agents
- Example: Install OpenCode from the ACP Registry directly into JetBrains IDE
- Use multiple agents alongside each other in the same editor
- Covers features like Next Edit Suggestion and plan mode
- You can even write your own custom agent and install it locally

### Portability Demo
- Feature spec skill from Claude Code was copied into OpenAI Codex and ran fine
- Switch between agents within the same project while keeping your SDD workflow

---

## 13. Key Principles to Remember

1. **The agent is the muscle, the spec is the brain** — you are the senior architect providing blueprints
2. **Write specs collaboratively** — conversation with the agent produces better specs than writing alone
3. **Small steps, frequent commits** — reduces cognitive debt and AI fatigue
4. **Human-in-the-loop always** — agents generate, you verify
5. **Specs are versioned artifacts** — treat them as seriously as code
6. **Don't oversteer** — provide context the agent doesn't have, let it handle what it knows
7. **Omissions aren't failures** — evolve the spec as you discover new details
8. **Replanning is mandatory** — slow down to run fast
9. **Agent-agnostic specs** — write at a level not tied to any one agent or IDE
10. **The specs you write today become the memory of your projects tomorrow**

---

## 14. The SDD Checklist (Per Feature)

- [ ] Review roadmap — is the next item correct?
- [ ] Clear agent context
- [ ] Create feature branch
- [ ] Interview with agent → produce plan, requirements, validation scorecard
- [ ] Review and correct feature spec
- [ ] Commit feature spec
- [ ] Clear context again
- [ ] Implement (all task groups or incremental)
- [ ] Review changes — high-level focus
- [ ] Run app and tests (debugger for exploration)
- [ ] Optional: deep review with sub-agents
- [ ] Commit implementation
- [ ] Update changelog (via skill)
- [ ] Merge branch
- [ ] Replan: update constitution, review roadmap, improve workflow
