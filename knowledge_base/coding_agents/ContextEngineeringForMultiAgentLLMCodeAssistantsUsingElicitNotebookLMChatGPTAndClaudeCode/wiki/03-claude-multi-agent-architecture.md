> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Claude Multi-Agent Architecture: Specialist Sub-Agents, Isolated Contexts, and Delegation Loop
**In one sentence:** Claude Code uses an orchestrator that delegates to role-specialist sub-agents (e.g. backend-architect) with isolated context windows plus shared CLAUDE.md memory, layered context inputs, and a plan–delegate–test–review loop that completed 4/5 tasks (80%) versus 2/5 (40%) for a single-agent baseline.
## Key points
- The backend-architect profile is defined as `name: backend-architect`, `description: Design RESTful APIs, microservice boundaries, and database schemas`, `model: sonnet`, `tools: Read, Write, Edit, Bash`, and doubles as planner for backend-heavy tasks.
- Each sub-agent runs with an isolated context window containing only task-relevant information plus persistent project context, preventing cross-contamination between workflow phases.
- Shared background (architectural overviews such as the Figure 3 system design, coding style guidelines, known bugs and previous solutions for RainMakerz) is preloaded from a persistent CLAUDE.md file into every agent's context.
- Context is layered L1–L5 into each agent prompt: L1 Task Specification (Intent Translator), L2 External Knowledge (Elicit & NotebookLM), L3 Project Memory (CLAUDE.md, internal docs), L4 Retrieved Code Context (Vector DB, grep), L5 Execution Artifacts (diffs, logs, test results).
- The orchestration loop runs Planning → Task Delegation → Iterative Coding and Validation (`npm test` feedback, simple re-try rather than multi-trajectory branching as in DARS [4]) → Code Review and Refinement → Output and Deployment (unified diff, GitHub Actions CI, possible auto-merge).
- Dividing work reduces prompt tokens per agent and preserves coherence on large tasks; execution is currently sequential with parallel spawning of independent sub-tasks possible per Anthropic multi-agent research [7], unused here because steps had dependencies.
- On 5 RainMakerz tasks the multi-agent system achieved 4/5 single-shot successes (80%) with no human corrections versus 2/5 (40%) for the single-agent baseline, every generated function/class existed in the repo (e.g. correctly using `renewSession()` instead of hallucinated `refreshToken()`), and the one failure still made partial progress by identifying a misconfigured library.
---
## Backend-architect sub-agent spec
**Covers:** chunk header — agent profile definition

| Field | Value (verbatim) |
|---|---|
| name | backend-architect |
| description | Design RESTful APIs, microservice boundaries, and database schemas |
| model | sonnet |
| tools | Read, Write, Edit, Bash |

> "You are a senior backend architect specializing in scalable system design"

The Planner agent is "often used the backend-architect profile as planner if the task was backend-heavy, or a specialized Planner agent".
## Isolated contexts with shared CLAUDE.md memory
**Covers:** isolated context windows; RainMakerz CLAUDE.md contents

- "Each subagent operates with an isolated context window. This means that when the orchestrator invokes (for example) the backend-architect agent to handle a task, that agent receives only the information relevant to its task (plus any persistent project context) and does not see the entire dialogue history or unrelated data."
- Purpose: "it prevents cross-contamination between different phases of the workflow and keeps each agent focused."
- "Common background information that all agents should know (coding conventions, project architecture notes, etc.) is provided via a persistent context file (CLAUDE.md), which is preloaded into each agent's context."
- "The CLAUDE.md for RainMakerz included high-level architectural overviews (such as the system design shown in Figure 3), coding style guidelines, and a summary of known bugs and previous solutions."
- Pattern: shared base of project knowledge + orchestrator-augmented specific instructions and data per step.
## Context layering (Figure 4)
**Covers:** Figure 4 — structured inputs flow into each agent's prompt

| Layer | Content |
|---|---|
| L1 | Task Specification (Intent Translator) |
| L2 | External Knowledge (Elicit & NotebookLM) |
| L3 | Project Memory (CLAUDE.md, internal docs) |
| L4 | Retrieved Code Context (Vector DB, grep) |
| L5 | Execution Artifacts (diffs, logs, test results) |

Figure caption (verbatim): "Figure 4: Context layering: structured inputs flow into each agent's prompt."
"Throughout this process, the structured layering of context is key (see Figure 4). At any given time, an agent is working with a manageable slice of information: its role-specific prompt + CLAUDE.md context + task-specific instructions + relevant code/knowledge snippets."
## Agent orchestration flow (Section 4.2, Figure 5)
**Covers:** Section 4.2 — Plan → Retrieve Context → Delegate → Edit/Implement → Run Tests → Review → Integrate/PR loop

Figure 5 caption (verbatim): "Figure 5: Claude orchestrator state machine with feedback from tests and code review."
State labels in figure: Plan, Retrieve Context, Delegate, Edit/Implement, failures, Done, Integrate/PR, Review, Run Tests, changes.
1. **Planning:** orchestrator invokes the Planner agent with the structured task specification and knowledge summary to produce a concrete implementation plan (sequence of steps mapped to files/components), e.g. "1. Update CalendarAPI to provide events data; 2. Create CalendarWidget component in frontend; 3. Integrate widget into SchedulePage; 4. Write unit tests for new component"; the orchestrator examines this plan.
2. **Task Delegation:** per plan step the orchestrator selects an agent (frontend steps to frontend-specialist, server-side to backend-architect) and supplies (a) the relevant plan excerpt (or whole plan), (b) pertinent retrieved code snippets from vector DB search, (c) specific instructions; the agent executes, most often via the Edit tool (e.g. frontend agent opens SchedulePage.jsx to insert calendar widget code).
3. **Iterative Coding and Validation:** after a step, the orchestrator or coding agent triggers tests via shell tool (configured `npm test` for the Node.js environment); failures/build errors are captured and fed back to the responsible or a dedicated debugging agent for a fix — "resembles the feedback loop in DARS [4], although in our implementation the branching is simple re-try rather than multiple simultaneous trajectories."
4. **Code Review and Refinement:** after all steps pass, the code-reviewer agent reads the diff against a comprehensive checklist (type safety, performance, security); suggestions are "either applied automatically by an editing agent or presented for a human to confirm, depending on the confidence level."
5. **Output and Deployment:** orchestrator consolidates a summary plus unified diff; in production changes could be pushed to a branch or opened as pull request; integrated with GitHub Actions CI that re-runs tests after Claude's changes and "could auto-merge the changes if all checks passed."
- Coherence/token note: "dividing the work among agents reduced prompt tokens per agent, which mitigates context window issues."
- Sequential vs parallel: "currently executes largely in a sequential manner (one sub-task at a time), it is straightforward to parallelize independent sub-tasks by spawning agents concurrently – an approach suggested by Anthropic's experiments with multi-agent research systems [7]"; parallelism deprioritized because "many steps had inherent dependencies (you can't test before code is written, etc.)".
## Results on RainMakerz tasks (Section 5, in-chunk portion)
**Covers:** Section 5 intro; CustomBlock case study; context adherence; 4/5 vs 2/5 single-shot rate

- Evaluation: "several non-trivial development tasks in the RainMakerz codebase. Table 1 provides a summary of outcomes on a sample of 5 tasks, comparing our system to a baseline single-agent Claude (with only a CLAUDE.md context and direct user prompts)."
- Summary claim: "our multi-agent approach succeeded in more tasks and required fewer iterations. It often produced working solutions on the first attempt, whereas the baseline frequently needed follow-up prompts or developer intervention."
- **Case study — CustomBlock in pitch-deck module** (analogous to a new content-block type in a presentation; spanned React component, options UI, TypeScript types, manager registration): Planner broke it into 4 steps; Frontend specialist created component and options popup following existing-block patterns via retrieved code context; Backend agent updated data model/API endpoints where needed and double-checked persistence needs; first test run failed because the new block type was missing from a serialization whitelist, so the orchestrator tasked the Backend agent to update the serialization config and the second run passed all unit and integration tests; Reviewer suggested refactoring a hard-coded string into a constant, applied; "entire feature was completed in one automated session."
- Baseline contrast on same task (single Claude with project README plus similar-block excerpt): "produced only the React component and forgot to update the registry and type definitions, resulting in runtime errors" — attributed to planning plus retrieving scattered context.
- **Improved Context Adherence:** "far less prone to hallucinating irrelevant code or inventing functions. Every function or class used by the generated code existed in the repository, which we attribute to the semantic code retrieval providing real definitions"; baseline "often guessed function or variable names (e.g. referring to a non-existent getEvents() API)"; auth bug-fix example: baseline tried nonexistent `refreshToken()` while the system used existing `renewSession()` via project docs/CLAUDE.md context and AllianceCoder-like retrieval plus code index.
- **Single-Shot Success Rate:** "Out of 5 tasks attempted ... our system achieved a successful outcome (defined by passing all tests and meeting the acceptance criteria) on 4 tasks (80%) without any human corrections. The single-agent baseline succeeded on only 2 tasks (40%)"; "aligns with the qualitative improvements noted in prior multi-agent studies (e.g., DARS and HyperAgent)"; on the one non-success the system "made partial progress and identified an environmental issue (a misconfigured library) that a developer then easily fixed before re-running the agent."
**Covers:** chunk 03-name-backend-a-r-c-h (agent spec through Section 5 results as contained in chunk); planned coverage: Claude orchestrator design — specialist sub-agents, isolated contexts, CLAUDE.md memory, layering, and delegation loop.
