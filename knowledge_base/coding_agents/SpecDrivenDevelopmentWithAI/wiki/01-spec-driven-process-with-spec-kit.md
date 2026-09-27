> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# What is the spec-driven process with Spec Kit?
**In one sentence:** Spec Kit makes the specification the living center of engineering — a validated four-phase Specify → Plan → Tasks → Implement flow where the developer steers and verifies while the coding agent generates the artifacts.
## Key points
- Spec Kit puts the spec (not the code) at the center: the spec drives implementation, checklists, and task breakdowns instead of being written once and set aside.
- The process has four phases with explicit checkpoints — you do not move to the next phase until the current task is fully validated.
- Specify captures what and why (user journeys, experiences, success criteria), not stacks or app design, and stays a living artifact that evolves with learning.
- Plan captures the technical how: stack, architecture, constraints, legacy/compliance/performance requirements, and can include multiple plan variations and internal-docs patterns.
- Tasks decomposes spec + plan into small, isolated, testable chunks (e.g. "create a user registration endpoint that validates email format" instead of "build authentication").
- Implement produces focused, reviewable changes per task (one by one or in parallel) instead of thousand-line code dumps, because the agent already knows what/how/in-what-order from spec, plan, and tasks.
- The developer's role is to steer and, crucially, to verify at each checkpoint — critiquing the spec, plan, and tasks for gaps, omissions, and edge cases before proceeding.
---
## Spec as executable shared truth
Specs are rethought "not as static documents, but as living, executable artifacts that evolve with the project" — the shared source of truth you return to when something doesn't make sense, refine as complexity grows, and break down when tasks feel too large. Supported agents named in the chunk: GitHub Copilot, Claude Code, and Gemini CLI. Verbatim role split: "Your primary role is to steer; the coding agent does the bulk of the writing."

## The four phases
| Phase | Input (you provide) | Output (agent generates) |
|---|---|---|
| Specify | High-level what + why: who uses it, what problem it solves, how they interact, what outcomes matter | Detailed specification of user journeys, experiences, success criteria |
| Plan | Desired stack, architecture, constraints (company standards, legacy integrations, compliance, performance targets); optionally internal docs and requests for multiple variations | Comprehensive technical plan embedding architectural patterns and standards |
| Tasks | Spec + plan as input | Small, reviewable, isolated tasks, each implementable and testable in isolation (TDD-like validation loop for the agent) |
| Implement | Task list | Focused changes solving specific problems, done one by one or in parallel |

## Verify at each checkpoint
Verbatim: "Crucially, your role isn't just to steer. It's to verify. At each phase, you reflect and refine." Checkpoint questions from the chunk: does the spec capture what you actually want to build; does the plan account for real-world constraints; are there omissions or edge cases the AI missed. The rule: "The AI generates the artifacts; you ensure they're right" — critique, spot gaps, and course-correct before moving forward.

## Steering commands
The chunk describes steering via simple commands: `specify init <PROJECT_NAME>` (via `uvx --from git+https://github.com/github/spec-kit.git`), then `/specify` for the what/why spec, `/plan` for the technical plan under your architecture and constraints, and `/tasks` for the actionable task list the agent then implements.

**Covers:** "What is the spec-driven process with Spec Kit?" section — Specify → Plan → Tasks → Implement phases, checkpoints, and CLI workflow (/specify, /plan, /tasks)
