# Factory Missions: Building Multi-Agent Systems for Long-Running Software Development

**Talk:** [Factory Missions: Agent Teams for Software Dev (Luke, Factory, 2025)](https://youtu.be/ow1we5PzK-o)

## Human Readable TL;DR

Imagine you have 50 tasks on your to-do list but can only personally supervise 5 things at once. Factory's "Missions" system is like hiring a well-organized team where one person plans the project, many specialists do the work one step at a time, and dedicated inspectors check everything -- all while you sleep. The inspectors don't just read the work; they actually use the finished product like a real user would, clicking buttons and filling out forms to confirm it works. The longest mission ran for 16 days without a human driving it.

## TL;DR

Factory's Missions is a multi-agent software development system combining four coordination patterns (delegation, creator-verifier, broadcast, negotiation) into a three-role architecture: orchestrator, workers, and validators. Crucially, workers run serially (one at a time) to avoid conflicts, validation is always done by agents with fresh context (adversarial by design), and a pre-written "validation contract" defines correctness before any code is written. Production missions have run for up to 16 days, targeting 30+ workstreams per 5-engineer team.

---

## Problem & Motivation

The bottleneck in modern software engineering is no longer model intelligence -- it is human attention. Even the best engineers can only drive a few tasks forward per day because every task requires their oversight and every commit needs their review. Today's models are capable enough to handle far more tasks simultaneously, but there is insufficient human bandwidth to supervise their implementation. Missions asks: what if a human decides *what* to build, and the system figures out *how*?

---

## Main Original Ideas

1. **Five Multi-Agent Coordination Primitives** -- The speaker proposes a taxonomy of five frontier patterns: *delegation* (agent spawns sub-agent), *creator-verifier* (builder + independent checker), *direct communication* (peer-to-peer between agents), *negotiation* (agents coordinate over shared resources), and *broadcast* (one-to-many status/context distribution). Missions combines four of these (excluding direct communication) into one system.

2. **Validation Contracts Written Before Code** -- A validation contract is produced by the orchestrator during planning, before any implementation begins. It defines hundreds of behavioral assertions that the final system must satisfy, independently of any implementation choices. This prevents the common failure mode where tests are "shaped by the code rather than by what the code was meant to do."

3. **Two-Stage Adversarial Validation** -- After each milestone, two validator types run with fresh, context-free agents: (a) *Scrutiny Validator* -- runs test suite, type checking, lint, and spawns dedicated code review agents per feature; (b) *User Testing Validator* -- spawns the live application, interacts via computer use (clicks, form fills, page renders), and validates end-to-end functional flows. Neither validator has seen the implementation code.

4. **Serial Execution with Targeted Internal Parallelization** -- Counter-intuitively, workers run one at a time (not in parallel) to prevent conflicts, duplicate work, and inconsistent architectural decisions. Parallelism is used only within a feature for read-only operations (e.g., codebase search, API research) and within validation for code review. This trades raw speed for dramatically lower error rates that compound over multi-day runs.

5. **Structured Handoffs for Self-Healing** -- When a worker finishes a feature it produces a structured handoff: what was completed, what was left undone, which commands were run and their exit codes, what issues were discovered, and whether the worker followed orchestrator-defined procedures. The orchestrator uses this at milestone boundaries to detect drift and scope corrective work, enabling multi-day continuity without accumulated context loss.

6. **"Droid Whispering" -- Model Composition as a Skill** -- Assigning the right model to each role is treated as a first-class engineering skill. Planning benefits from slow careful reasoning, implementation from fast code fluency, validation from precise instruction following. No single model excels at all three. Using multiple providers for validation also reduces confirmation bias from shared training data.

7. **Prompt-Driven Architecture (Bitter Lesson Resistant)** -- Orchestration logic lives in ~700 lines of prompts and skills rather than hard-coded state machines. Four sentences of prompt change can dramatically alter execution strategy. This ensures Missions improves automatically with every model capability advance rather than becoming obsolete.

---

## Key Findings

| Metric | Value |
|--------|-------|
| Longest mission duration | **16 days** (targeting 30 days) |
| Time spent on implementation | **60%** of wall-clock and tokens |
| Proportion of final code that is tests | **~50%** |
| Test coverage achieved | **~90%** |
| First-pass validation success rate | **Rarely** -- follow-up features almost always required |
| Most wall-clock time spent | Waiting for **user testing validator** (live app interaction) |

- Prompt caching is used heavily to offset the cost of long-running tasks
- Missions most expensive time sink is not token generation but real-world execution in the user testing validator
- Enterprise use cases: overnight feature prototyping, internal tools, large refactors/migrations, ML research pipelines, codebase modernization for agent productivity
- Target impact: scale from ~10 workstreams to ~30 per 5-engineer team

---

## Suggestions & Future Directions

1. **Further parallelization of missions** -- Current serial-worker design is correct but slow; open question is how to safely parallelize at a higher level while preserving correctness guarantees.
2. **Meta-orchestration -- missions orchestrating missions** -- Composing Missions into larger workflows for even more complex multi-sprint projects.
3. **Customizing model assignments per project** -- Encourages teams to treat model selection as project-specific tuning rather than a global default.
4. **Open-weight model support** -- Validation contracts and milestone checkpoints compensate for sub-frontier models, making Missions viable without requiring frontier APIs.
5. **Agent ecosystem thinking as a skill** -- The speaker frames the ability to mentally model how different LLMs compose under pressure as the key human skill for the next generation of software development.

---

## Authors & Institutions

Luke (last name not stated), engineering lead for core agent harness at **Factory** (formerly built **Goose** coding agent at Block, now donated to the AI Agentic AI Foundation). Talk delivered at an AI conference (venue not stated in transcript).
