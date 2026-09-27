# Spec-driven development with AI: Get started with a new open source toolkit - The GitHub BlogLinkedIn iconInstagram iconYouTube iconX iconTikTok iconTwitch icon

**Article:** [Spec-driven development with AI: Get started with a new open source toolkit](https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/) — The GitHub Blog

## Human Readable TL;DR

Imagine building a house by first agreeing on blueprints with your architect, getting them checked by an engineer, breaking the job into small work orders, and only then laying bricks — that is what Spec Kit does for AI-assisted coding. Instead of asking a coding agent to "just build it" and getting a giant pile of code you cannot review, you write down what you want and why, agree on how it will be built, split the work into bite-sized tasks, and let the agent implement them one at a time while you inspect each step. Your main job shifts from typing code to steering and double-checking, like a head chef who tastes every dish before it leaves the kitchen. The result is smaller, reviewable changes that actually match what you asked for, because the plan was settled before any code was written.

## TL;DR

The article introduces spec-driven development with GitHub's open source Spec Kit as an alternative to free-form "vibe coding": the specification becomes the living, executable center of the engineering process rather than a document written once and forgotten. Development follows a validated four-phase flow — Specify (what and why), Plan (technical how), Tasks (small isolated testable chunks), and Implement (focused changes one by one or in parallel) — with the developer steering and verifying at each checkpoint before proceeding. Supported agents named in the notes include GitHub Copilot, Claude Code, and Gemini CLI, driven through simple commands such as `specify init`, `/specify`, `/plan`, and `/tasks`, with the guiding rule that the AI generates the artifacts while the human ensures they are right.

---

## Problem & Motivation

The piece responds to a familiar failure mode of AI-assisted coding: prompting an agent for a whole feature and receiving a thousand-line code dump that is hard to review, hard to trust, and often misaligned with what was actually wanted. The motivation is to flip the workflow so that intent, constraints, and success criteria are settled and validated up front, giving the agent the what, the how, and the order of work before it writes anything. By making the specification the shared source of truth that the team returns to, refines as complexity grows, and decomposes when tasks feel too large, the process aims to produce changes that are small, reviewable, and traceable to agreed requirements rather than opaque bursts of generated code.

## Main Original Ideas

1. **Spec as living executable center** — the specification is rethought not as a static document but as a living, executable artifact that evolves with the project, drives implementation, checklists, and task breakdowns, and serves as the place you return to whenever something does not make sense.

2. **Validated four-phase flow** — development proceeds through Specify, Plan, Tasks, and Implement with explicit checkpoints, where each phase is fully validated before moving on, and the Tasks phase deliberately decomposes work into small, isolated, testable chunks with a TDD-like validation loop for the agent.

3. **Steer-and-verify developer role** — the human's primary role is reframed as steering while the coding agent does the bulk of the writing, with the crucial addition that the human must verify at every phase by critiquing the spec, plan, and tasks for gaps, omissions, and edge cases before proceeding.

4. **Command-driven workflow** — the whole flow is operationalized through a small set of steering commands, starting with `specify init <PROJECT_NAME>` and continuing with `/specify` for the what-and-why spec, `/plan` for the technical plan under the team's architecture and constraints, and `/tasks` for the actionable list the agent then implements.

## Key Findings

The notes convey that separating the what-and-why (user journeys, experiences, success criteria, with no stack or app-design decisions) from the technical how (stack, architecture, company standards, legacy integrations, compliance, and performance targets, optionally with multiple plan variations) is what makes the downstream work reliable. Because the agent already knows the what, how, and order from the spec, plan, and task list, implementation yields focused changes solving specific problems instead of sprawling dumps. The checkpoint discipline — asking whether the spec captures what is actually wanted, whether the plan accounts for real-world constraints, and what the AI missed — is presented as the mechanism that catches misalignment early, when it is cheap to course-correct.

## Suggestions & Future Directions

The article's implicit suggestion is to adopt the spec-first habit on the reader's own project: initialize Spec Kit, work through the Specify, Plan, and Tasks phases with verification at each step, and only then let the agent implement. The wiki notes record no explicit roadmap, metrics, or follow-up research directions beyond refining the living spec as learning accumulates and splitting tasks further whenever they feel too large.

## Authors & Institutions

The wiki notes do not name an author; the publishing institution is The GitHub Blog (GitHub). The toolkit discussed is GitHub's open source Spec Kit, described as working with coding agents including GitHub Copilot, Claude Code, and Gemini CLI.
