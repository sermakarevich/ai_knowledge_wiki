> [[index|Wiki]] | [[summary|Summary]]
# Spec-Driven Development with Coding Agents - DeepLearning.AI — Digest

## 1. [[wiki/01-spec-driven-development-with-coding-agents|Spec-Driven Development with Coding Agents]]
**In one sentence:** This DeepLearning.AI course built with JetBrains and taught by Paul Everitt teaches spec-driven development as a disciplined alternative to vibe coding, using markdown specs, project constitutions, and a repeatable plan-implement-verify workflow across new and legacy codebases.
## Key points
- Spec-driven development is presented as the disciplined alternative to vibe coding: write a clear markdown spec defining what to build and let the coding agent implement it.
- Vibe coding is described as fast but often producing code that doesn't match what was asked for, while detailed specs lead to better, more maintainable software.
- Students write a project constitution by collaborating with the agent to define mission, tech stack, and roadmap, preserving context across agent sessions.
- The core repeatable workflow is plan-implement-verify: plan and validate features in iterative loops, implement with the spec as guide, then validate while staying human-in-the-loop.
- Specs are claimed to preserve context across agent sessions, reduce cognitive debt, and improve intent fidelity, keeping the agent aligned with intent.
- The course covers both greenfield and legacy codebases, including introducing SDD to a legacy codebase using existing documentation to generate specs.
- Students package their custom workflow into a portable agent skill usable across agents and IDEs, and replan between features to produce an MVP.

## The argument in five moves
1. Vibe coding is fast but unreliable, producing code that drifts from what was asked for, so a disciplined alternative is needed.
2. That alternative is spec-driven development: a clear markdown spec defines what to build and the agent implements it, keeping intent fidelity high.
3. A project constitution (mission, tech stack, roadmap) grounds the work and preserves context across agent sessions, reducing cognitive debt.
4. The repeatable plan-implement-verify loop — plan iteratively, implement against the spec, validate human-in-the-loop — carries each feature to done.
5. Replanning between features compounds into an MVP on greenfield work, while existing docs bootstrap specs for legacy codebases.
6. Packaging the workflow as a portable agent skill makes the discipline reusable across agents and IDEs rather than a one-off habit.
