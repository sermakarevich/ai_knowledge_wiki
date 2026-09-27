> [[index|Wiki]] | [[summary|Summary]]

# My LLM coding workflow going into 2026 | AddyOsmani.com — Digest

## 1. [[wiki/01-start-with-a-clear-plan-specs-before-code|Start with a clear plan (specs before code)]]

**In one sentence:** Before any code generation, iteratively brainstorm a comprehensive spec.md with the LLM and refine an AI-generated bite-sized project plan, then implement it one small tested chunk at a time to keep human and model aligned and avoid wasted cycles.

## Key points

- Don't dive into codegen on a vague prompt; first define the problem and plan the solution with the AI, treating the LLM as a pair programmer needing clear direction, context, and oversight rather than autonomous judgment.
- Describe the idea and ask the LLM to iteratively ask questions until requirements and edge cases are fleshed out, then compile a comprehensive spec.md containing requirements, architecture decisions, data models, and testing strategy.
- Feed the spec into a reasoning-capable model to generate a project plan of logical, bite-sized tasks or milestones (a mini "design doc"), iterating and asking the AI to critique or refine it until coherent and complete before coding.
- Upfront planning pays off enormously: as Les Orchard put it, it's like doing a "waterfall in 15 minutes" — a rapid structured phase that makes subsequent coding much smoother and forces human and AI onto the same page.
- Implement one focused piece at a time (e.g. prompt "Okay, let's implement Step 1 from the plan", test it, then move to Step 2), since LLMs do best on contained tasks and large monolithic requests produce confusion or a "jumbled mess".
- Asking for huge swaths of an app at once yields inconsistency and duplication — "like 10 devs worked on it without talking to each other" — so stop, back up, and split the problem, carrying forward built context incrementally, which also fits test-driven development (tests generated per piece).
- Use a structured "prompt plan" file with a sequence of per-task prompts (executable one by one by tools like Cursor) to enforce small loops, reduce catastrophic errors, and allow quick course-correction.

## 2. [[wiki/02-leverage-ai-coding-across-the-lifecycle|Leverage AI coding across the lifecycle]]

**In one sentence:** Use CLI and asynchronous AI coding agents in a supervised way across the SDLC — grounding them with plans/specs, verifying everything with tests and reviews, and containing their output with ultra-granular version control.

## Key points

- CLI agents (Claude Code, OpenAI Codex CLI, Google Gemini CLI) work inside the project directory, reading files, running tests, and performing multi-step fixes from chat commands.
- Asynchronous agents (Google Jules, GitHub Copilot Agent) clone the repo into a cloud VM, work in the background writing tests and fixing bugs, then open a PR — e.g. "refactor the payment module for X" returns later as a PR with code plus passing tests.
- Agents accelerate mechanical work (boilerplate, repetitive changes, automatic test runs) but need guidance: supply the plan/to-do list and load `spec.md` or `plan.md` into context before telling them to execute.
- Supervised use is the rule, not unattended full-feature generation: let agents generate and run code while watching each step; orchestration tools like Conductor can run 3–4 agents in parallel, but the author mostly sticks to one main agent plus a secondary reviewer because parallel threads are mentally taxing.
- Treat every AI snippet as junior-developer output and test it: instruct the agent to run the test suite after each task and debug failures, since agents with a good test suite as a safety net "fly" while agents without tests blithely claim "sure, all good!" while breaking things.
- Review AI code line by line with extra scrutiny, optionally spawning a second AI session or different model to critique the first (e.g. "Can you review this function for any errors or improvements?"), and only merge or ship code you understand — asking for explanatory comments or rewriting convoluted output.
- Commit early and often with clear messages as "save points in a game": finish task, run tests, commit, so any sideways AI change can be reverted or cherry-picked; small per-chunk commits (never one giant "AI changes" commit) make it possible to pinpoint which change broke something.
- Use git history and isolation to steer and sandbox AI work: paste diffs/commit logs into prompts and let the agent parse diffs and use `git bisect` across a tidy history, and spin up branches or fresh git worktrees per feature so parallel AI sessions don't interfere and failed experiments can be discarded.

## 3. [[wiki/03-customize-the-ai-s-behavior-with-rules-and-examples|Customize the AI's behavior with rules and examples]]

**In one sentence:** Tune the AI like a new hire — with rules files, custom instructions, and examples — and back it with automated tests and continuous learning so its output matches your conventions and gets caught when it doesn't.

## Key points

- Maintain a periodically updated `CLAUDE.md` (and `GEMINI.md` for Gemini CLI) with process rules and preferences — project style, lint rules, banned functions, functional-over-OOP — and feed it at session start to keep the model on track and reduce off-script patterns.
- Configure global project behavior in GitHub Copilot and Cursor with a short style paragraph (e.g. 4-space indent, no arrow functions in React, descriptive names, must pass ESLint) so suggestions match team idioms.
- Prime the model by mimicry: show a similar existing function ("Here's how we implemented X, use a similar approach for Y") or write one comment in the desired style and ask it to continue in that vein.
- Prepend truthfulness rules to prompts, e.g. "If you are unsure about something or the codebase context is missing, ask for clarification rather than making up an answer," plus explanation rules such as "Always explain your reasoning briefly in comments when fixing a bug," yielding reviewable comments like "// Fixed: Changed X to Y to prevent Z (as per spec)."
- Run heavy-AI repos with CI on every commit/PR, enforced style checks (ESLint, Prettier), and a staging deployment, then feed failures back verbatim ("The integration tests failed with XYZ, let's debug this" / paste linter errors plus "please address these issues") and route reviewer comments (e.g. CodeRabbit) back as refactor prompts.
- Treat AI use as a skill amplifier: solid fundamentals, clear specs, tests, and reviews become more powerful, while weak foundations risk "Dunning-Kruger on steroids"; deliberately review AI code, ask it to explain rationale and compare trade-offs, and periodically code without AI.

## The argument in five moves

1. Start with specs before code: iteratively build a comprehensive spec.md and a bite-sized plan with the LLM so human and model align before any generation.
2. Implement in small tested chunks rather than monolithic generations to avoid confusion, duplication, and costly untangling.
3. Deploy CLI and asynchronous agents across the lifecycle for mechanical work, but keep them supervised, grounded in plans/specs, and limited to one main thread plus a reviewer.
4. Verify everything as the accountable senior: run tests per task, review line by line (including AI-on-AI review), and contain output with save-point commits, tidy history, and isolated branches/worktrees.
5. Tune the model like a new hire with rules files, custom instructions, examples, and truthfulness/explanation rules so output matches team conventions.
6. Back heavy AI use with automation and continuous learning: CI, linters, staging, feedback loops for failures, plus deliberate study of AI output — AI-augmented, not AI-automated, engineering with the human as director.
