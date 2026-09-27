---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: My LLM coding workflow going into 2026 | AddyOsmani.com

### Q1. What is the spec-before-code sequence, and what goes into spec.md and the project plan?

> [!tip]- Answer
> Describe the idea and have the LLM iteratively ask questions until requirements and edge cases are fleshed out, then compile a comprehensive spec.md with requirements, architecture decisions, data models, and testing strategy. Feed that spec into a reasoning-capable model to produce a bite-sized task plan or mini design doc, asking it to critique and refine until coherent and complete. This rapid "waterfall in 15 minutes" aligns human and model before any codegen. See [[wiki/01-start-with-a-clear-plan-specs-before-code|Start with a clear plan (specs before code)]].

### Q2. Why implement one small tested chunk at a time instead of one large generation?

> [!tip]- Answer
> LLMs do best on contained tasks, while huge single-shot requests produce a hard-to-untangle "jumbled mess" with inconsistency and duplication, "like 10 devs worked on it without talking to each other". The fix is to prompt "implement Step 1 from the plan", test it, then move to Step 2, carrying built context forward incrementally, optionally via a structured prompt-plan file executed stepwise by tools like Cursor. Small loops reduce catastrophic errors, allow quick course-correction, and fit test-driven development per piece. See [[wiki/01-start-with-a-clear-plan-specs-before-code|Start with a clear plan (specs before code)]].

### Q3. Contrast CLI coding agents with asynchronous cloud agents, and how must each be grounded?

> [!tip]- Answer
> CLI agents (Claude Code, OpenAI Codex CLI, Google Gemini CLI) chat inside the project directory, reading files, running tests, and performing multi-step fixes from chat commands. Asynchronous agents (Google Jules, GitHub Copilot Agent) clone the repo into a cloud VM, work in the background on tests and fixes, then return a PR with code plus passing tests. Both are power tools needing guidance: supply the plan or to-do list and load spec.md or plan.md into context before executing. See [[wiki/02-leverage-ai-coding-across-the-lifecycle|Leverage AI coding across the lifecycle]].

### Q4. How do you verify AI-generated code, and what role do tests and AI-on-AI review play?

> [!tip]- Answer
> Treat every snippet as junior-developer output from an "over-confident and prone to mistakes" pair programmer and never blindly trust it, since it writes bugs with complete conviction. Instruct the agent to run the test suite after each task in a write-code, run-tests, fix loop, because agents with a good test safety net fly while testless agents claim "sure, all good!" while breaking things. Review line by line with extra scrutiny, optionally having a second session or model critique the first, and only merge or ship code you understand. See [[wiki/02-leverage-ai-coding-across-the-lifecycle|Leverage AI coding across the lifecycle]].

### Q5. How does disciplined version control contain AI missteps?

> [!tip]- Answer
> Commit early and often after each small tested task as "save points in a game", so any sideways AI change can be reverted or cherry-picked without losing hours. Keep commits small with clear messages rather than one giant "AI changes" commit, so you can pinpoint which change broke something, and paste diffs and commit logs into prompts plus use git bisect across the tidy history to find bugs. Isolate experiments in branches or fresh git worktrees per feature so parallel AI sessions do not interfere and failed attempts can be discarded. See [[wiki/02-leverage-ai-coding-across-the-lifecycle|Leverage AI coding across the lifecycle]].

### Q6. How do you tune the AI like a new hire, and how do automation and continuous learning back it up?

> [!tip]- Answer
> Maintain a periodically updated CLAUDE.md (and GEMINI.md) with project style, lint rules, banned functions, and functional-over-OOP preferences, plus short Copilot or Cursor custom instructions, and prime by mimicry by showing an existing implementation or one comment in the desired style. Prepend truthfulness rules ("ask for clarification rather than making up an answer") and explanation rules ("explain reasoning briefly in comments when fixing a bug") for reviewable output. Back heavy AI use with CI on every commit or PR, ESLint and Prettier checks, staging deployments, and feedback loops that route failures and CodeRabbit comments verbatim back as fix prompts, while treating AI as a skill amplifier that rewards fundamentals and risks "Dunning-Kruger on steroids" without them. See [[wiki/03-customize-the-ai-s-behavior-with-rules-and-examples|Customize the AI's behavior with rules and examples]].

### Q7. Your team proposes letting async agents generate and merge whole features unattended to ship faster — should you approve it, and what workflow would you recommend instead? (evaluation)

> [!tip]- Answer
> Reject unattended merging: the workflow is AI-augmented rather than AI-automated engineering, with the human as the accountable senior and director, and the rush-project cautionary case shows unsupervised building produces duplicate logic and incoherent architecture needing painful refactor. Recommend a supervised flow instead: spec and bite-sized plan grounding, one main agent plus a secondary reviewer rather than taxing parallel threads, tests run per task, line-by-line plus AI-on-AI review, and save-point commits with branch or worktree isolation, shipping only understood code. More tests, monitoring, and automation catch what one model misses while keeping velocity without surrendering judgment. See [[wiki/02-leverage-ai-coding-across-the-lifecycle|Leverage AI coding across the lifecycle]] and [[wiki/03-customize-the-ai-s-behavior-with-rules-and-examples|Customize the AI's behavior with rules and examples]].
