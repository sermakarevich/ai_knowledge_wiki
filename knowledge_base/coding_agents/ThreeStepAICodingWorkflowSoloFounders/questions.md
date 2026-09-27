---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---

> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Retrieval Practice: A 3-step AI coding workflow for solo founders | Ryan Carson (5x founder)

### Q1. What is the biggest mistake people make with AI coding, and what mental model does Ryan Carson offer for the AI?

> [!tip]- Answer
> The biggest mistake is rushing context: not having the patience to tell the AI what it actually needs to know, so slowing down on the briefing speeds everything up. The mental model is a genius PhD student that misses simple obvious things, so instructions must set the level explicitly and scope requests to a manageable size. See [[wiki/01-three-step-ai-coding-workflow|Three-step AI coding workflow for solo founders]].

### Q2. What are the three Cursor rule files in the workflow, and how are they invoked in the demo?

> [!tip]- Answer
> The three rules are a PRD generator, a task-list generator, and a task-list manager for iterative execution. Each is @-mentioned into Cursor's agent-mode context window and paired with a short instruction, demonstrated on a yacht-club CRM report showing member boat names and email counts. See [[wiki/01-three-step-ai-coding-workflow|Three-step AI coding workflow for solo founders]].

### Q3. How does Step 1 (PRD generation) work, and what two prompt-craft details keep it concrete and answerable?

> [!tip]- Answer
> The user @-includes the PRD rule and gives a one-sentence feature idea, the AI asks clarifying questions (e.g. problem, user, location), and the output is a markdown PRD in a tasks/ folder covering functional requirements, non-goals, and design considerations. The PRD is framed as suitable for a junior developer to implement, and clarifying questions use dot notation (2.1, 2.2) with unanswered ones defaulted to the AI's best judgment. See [[wiki/01-three-step-ai-coding-workflow|Three-step AI coding workflow for solo founders]].

### Q4. How does Step 2 (task-list generation) work, and why does it matter even before any code runs?

> [!tip]- Answer
> The user includes the generate-tasks rule, tags the PRD file, and prompts it to generate tasks, producing a markdown checklist of numbered parent tasks with subtasks, sub-subtasks, and a relevant-files section, pausing for a "go" before expanding subtasks. It matters because breaking a PRD into codebase-correct steps is where engineers and PMs commonly stall, so an explicit plan prevents the agent from going down a rabbit hole. See [[wiki/01-three-step-ai-coding-workflow|Three-step AI coding workflow for solo founders]].

### Q5. What are the execution rules in Step 3, and what commit and review practices surround them?

> [!tip]- Answer
> The manager rule does exactly one subtask at a time, marks it complete immediately, then stops and waits for a short go-ahead (often just "y") before continuing. The user reviews after each step to catch small AI-introduced errors or linter problems, and commits after a parent task only when the app is workable, guided by how painful a revert would be. See [[wiki/01-three-step-ai-coding-workflow|Three-step AI coding workflow for solo founders]].

### Q6. What context and MCP tooling extends the loop, and what does each tool do?

> [!tip]- Answer
> The Postgres MCP answers database questions without hand-written SQL, Browserbase plus Stagehand drive a headless cloud browser from chat for navigation and future front-end testing, and Repo Prompt on Mac gives explicit file-level context control, shrinking a ~395,000-token repo to ~12,000 tokens of XML-tagged context. The task list itself stays as hand-cranked markdown rather than Asana MCP tasks so it is easier to see, edit, and extend. See [[wiki/01-three-step-ai-coding-workflow|Three-step AI coding workflow for solo founders]].

### Q7. (Evaluation) Should a solo founder adopt this slow three-step loop over vibe-coding or a heavier tool like Taskmaster, and why?

> [!tip]- Answer
> Adopt the three-step loop when reliability on large features matters more than raw speed, since one-subtask pacing with human checks reportedly builds ~10,000-line features without reverts, which vibe-coding rarely sustains. Prefer hand-cranked markdown over Taskmaster when control and visibility beat extra power, graduating to heavier tooling only once the simple loop breaks down. See [[wiki/01-three-step-ai-coding-workflow|Three-step AI coding workflow for solo founders]].
