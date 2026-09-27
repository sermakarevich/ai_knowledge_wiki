> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Three-step AI coding workflow for solo founders
**In one sentence:** The biggest mistake with AI coding is rushing context, so slow down and run a PRD → task list → one-subtask-at-a-time execution loop in Cursor to reliably build large features solo.
## Key points
- The core failure mode is impatience with context: not telling the AI what it needs to know to solve the problem.
- The fix is a three-file Cursor-rules loop: a PRD generator rule, a task-list generator rule, and a task-list manager rule for iterative execution.
- The PRD prompt is framed as "suitable for a junior developer to understand and implement," which keeps the AI concrete instead of assuming obvious details.
- PRD clarifying questions use dot notation (e.g. 2.1, 2.2) so answers stay addressable; unanswered questions get "make your best judgment / you pick."
- Generated PRDs go into a `tasks/` folder and task lists use markdown checkboxes with tasks, subtasks, and sub-subtasks plus a "relevant files" section.
- Execution does one subtask at a time, marks it complete immediately, then stops and waits for user go-ahead (often just "y") before continuing.
- Ryan reports building features of ~10,000 lines of code reliably with this loop plus human-in-the-loop checks and commits after workable parent tasks.
---
## 1. The biggest mistake: rushing context
> "I think the biggest mistake that I do that everyone does is they try to rush through the context where you just don't have the patience to tell the AI what it actually needs to know to solve your problem. And I think if we all just slow down a tiny bit and do these two steps, it speeds everything up."

**Covers:** opening thesis on context and patience

- AI coding skill comes from practice: cutting requests down to a manageable amount the AI can actually do by controlling what it sees and what it is asked to do.
- Mental model offered: the AI is like "a genius PhD student" that misses simple obvious things humans know, so instructions must set the level explicitly.
- Companion maxim: "nobody really knows how to do this stuff. The only way you're really going to figure it out is by getting in here and getting your hands dirty and see what works."

## 2. Demo setup: Cursor, yacht-club CRM, three rule files
**Covers:** Cursor intro and workflow overview

| Element | Detail from chunk |
|---|---|
| Tool | Cursor, described as a VS Code fork downloadable free at cursor.com, used in agent mode |
| Demo project | "Stupid little CRM tool for a yacht club" vibe-coded the prior day |
| Example change | "Add a report that shows me all the boat names of members and how many emails they've been sent" |
| Three open-sourced Cursor rules | (1) create PRD, (2) generate tasks ("generate tasks"), (3) iterate task list ("task list" / task-list management) |
| Models mentioned | Claude 3.7 Sonnet in Max mode; default Gemini 2.5 Pro with Max mode (~$300–400/month, "worth it"); "default o3 girl" with fallback to 3.7 when o3 stalls |
| Heavier alternative | Open-source Taskmaster CLI described as a "hyped up version" that was too much; author wanted "less power, more control" |

## 3. Step 1 — PRD: prompt, clarifying questions, output
**Covers:** PRD generation in agent mode

- Flow: @-include (at-mention) the PRD rule file to put it in the context window, then give a one-sentence feature instruction.
- The AI responds with clarifying questions, e.g. "What is the problem this report is trying to solve?", "Who specifically will be using the report?", "Where should this report be accessible?"
- Answers given in the demo: problem = "give visibility into how many emails people are getting"; user = "admins"; location = "you pick"; remainder = "make your best judgment."
- Output is a markdown PRD written into a task folder, with sections including functional requirements, non-goals, and design considerations.
- Prompt-craft tip: force clarifying questions into dot notation (2.1, 2.2) because otherwise the AI bundles multiple questions into one bullet and it becomes hard to answer.

## 4. Step 2 — Task list: explicit process over the PRD
**Covers:** task-list generation

- Flow: include the generate-tasks rule, tag the PRD file, and prompt "please generate tasks for [PRD]."
- The rule specifies: goal ("guide an AI assistant in creating a detailed step-by-step task list"), desired markdown format with checkboxes, process steps, and a pause asking the user to reply "go" before generating subtasks.
- Output includes relevant files, numbered parent tasks (1, 2, 3, 4) with subtasks and sub-subtasks.
- Rule-writing method described: try things, get more specific when they fail, have "a very intelligent LLM write this for me," then edit; stick with one model (e.g. Gemini 2.5 Pro) long enough to learn what it is good and bad at.
- Why it matters even without running the code: "that's a place where so many engineers and product managers get stuck in a loop like who's going to take this PRD and actually break it down in the right steps that are going to work in our codebase."

## 5. Step 3 — Execute one subtask at a time with human in the loop
**Covers:** iterative implementation

- Flow: tag the task-list manager rule plus the task-list file, then prompt "let's start."
- Rules: do one subtask at a time and never all tasks at once; mark each subtask complete immediately; "stop after each subtask and wait for the user's go-ahead."
- Demo: first subtask "define Prisma schema email campaign" reads the existing Prisma file, completes, and checks off 1.1 with Cursor's chime; user replies "yes" (sometimes just "y") to proceed to 1.2.
- Change management: commit after finishing a parent task if the app is in a workable state; otherwise wait until all tasks are done (about half a day of work); decision heuristic is "if I had to revert now how bad would it be / what would I need to undo."
- Caveat: human checking after each task matters because the AI often introduces a small problem or linter error that must be fixed; without the process the speaker ends up "down some rabbit hole" and has to revert.
- Claimed result: "built huge features with this… 10,000 lines of code reliably and almost never had trouble."

## 6. Context and MCP tooling tips
**Covers:** Postgres, Browserbase/Stagehand, Repo Prompt

| Tool | Use stated in chunk |
|---|---|
| Postgres MCP (Vercel-hosted Postgres) | Most-used daily MCP: ask "is this value in this row in the database" instead of writing SQL; also mentions Prisma/SQLite for the play project |
| Browserbase + Stagehand MCPs | Drive a headless cloud browser from Cursor chat in agent mode (demo: "navigate to chatPRD and take a screen grab," "navigate to pricing"); framed as future front-end testing to replace screenshot-paste bug-chasing |
| Repo Prompt (Mac) | Explicit context control versus Cursor's background "magic": select files, drop `generated/`, shrink from ~395,000 tokens (whole repo) / ~324,000 (app folder) to ~12,000 tokens, add prompt ("How can I improve the maintainability of this code?") plus stored "architect" meta-prompt, copy files + instructions as XML-tagged paste into o3/01 Pro/Cursor |
| Markdown over PM tools | Deliberately keeps the task list as a hand-cranked markdown file rather than Asana MCP tasks: easier to see, edit, and add tasks; advice is "start small, start simple… then graduate" |

## 7. Solo-founder payoff and working style
> "Building this new startup I literally feel like I'm able to do all of it now… But I am able for sure to build this company by myself."

**Covers:** closing lightning round and workflow moral

- Comparison: not as good as a dedicated product manager, nor thinking as deeply as a CTO, but able to build the company solo — contrasted with a prior company of ~110 employees with a CTO, VP of Eng, and PMs.
- Getting the AI back on track: politely say "please think harder about this… I believe you can do this," explicitly framed like parenting/coaching rather than scolding.
- Politeness thesis: treat the agent like a human because models are trained on human output, so give the right context and be helpful; "be treat an agent like you would treat a human."
- Coding soundtrack: late-night EDM (Tiësto live set from NYC); joke feature request is AI-generated streaming EDM matched to token pace that ends with a drop instead of the Cursor chime.
