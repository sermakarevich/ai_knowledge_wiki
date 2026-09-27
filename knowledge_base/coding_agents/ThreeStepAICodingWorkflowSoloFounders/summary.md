# A 3-step AI coding workflow for solo founders | Ryan Carson (5x founder)

**Video:** [A 3-step AI coding workflow for solo founders | Ryan Carson (5x founder)](https://www.youtube.com/watch?v=fD4ktSkNCw4) — YouTube

## Human Readable TL;DR

The core message is to stop rushing the AI and instead treat it like a brilliant but literal-minded junior hire who needs careful briefing before touching any code. The workflow works like writing a recipe before cooking: first you agree on exactly what dish you want, then you break it into small numbered steps, and only then do you cook one step at a time while tasting as you go. Done this way, a solo founder can act like a whole product team, steadily building very large features without getting lost or having to throw everything away.

## TL;DR

The video argues that the dominant failure mode in AI-assisted coding is impatience with context, and presents a deliberately slow, controlled three-step loop run in Cursor's agent mode that trades raw speed for reliability. A PRD-generator rule turns a one-sentence feature idea into a concrete product requirements document through clarifying questions, a task-list generator rule breaks that PRD into checked-off parent tasks, subtasks, and relevant files, and a task-list manager rule then implements exactly one subtask at a time, marking it complete and pausing for human approval before continuing. The surrounding practice includes committing after workable parent tasks, checking each step for small AI-introduced errors, explicitly controlling context with tools like Repo Prompt, and using MCP integrations for database questions and browser automation, which together are claimed to support building features on the order of ten thousand lines of code as a solo founder.

---

## Problem & Motivation

The problem the video addresses is that solo builders and small teams routinely stall or spiral when they hand large, vague requests to coding agents, ending up down some rabbit hole of compounding mistakes that eventually forces a revert. The motivation is practical and personal: as a repeat founder now building a startup alone, the speaker wants a repeatable way to get the leverage of product managers and engineers without hiring them, and finds that the missing ingredient is not a smarter model but better process. This leads to a broader reflection on how AI coding skill actually develops, namely through practice at scoping requests to a manageable size and deliberately managing what the model sees and is asked to do, rather than expecting Cursor's background magic to infer intent on its own.

## Main Original Ideas

1. **Slow down on context to speed up overall.** The central thesis is that taking extra time to brief the AI pays back many times over, because an underspecified request practically guarantees rework while a well-specified one lets the agent proceed steadily through a large feature.

2. **The three-file Cursor-rules loop.** The concrete contribution is a set of three open-sourced, @-mentioned rule files that structure the whole build: a PRD rule that forces clarifying questions and writes its output into a tasks folder, a generate-tasks rule that converts the PRD into a markdown checklist of tasks, subtasks, and relevant files with an explicit pause before expanding subtasks, and a task-list manager rule that executes strictly one subtask at a time, marks it done immediately, and waits for a short go-ahead before proceeding.

3. **Junior-developer framing and addressable clarifying questions.** Two prompt-craft details carry much of the weight: pitching the PRD as documentation suitable for a junior developer to implement, which keeps the model concrete about requirements, non-goals, and design considerations instead of glossing over the obvious, and forcing clarifying questions into dot notation so each answer stays individually addressable, with explicit permission for the model to use its best judgment on anything the user defers.

4. **Human-in-the-loop pacing with revert-aware commits.** Rather than letting the agent run through the whole list, the workflow commits after a parent task only when the app is in a workable state, guided by the heuristic of how painful a revert would be, and treats human review after each step as the place where small model-introduced problems and linter errors get caught before they compound.

## Key Findings

The demo, built around adding a member boat-name and email-count report to a small yacht-club CRM, shows the loop working end to end from a single sentence through clarifying answers about the problem, the admin audience, and placement toward a checked-off Prisma schema subtask advanced one short confirmation at a time. The speaker reports that this same loop has reliably produced very large features without major trouble, in contrast with heavier alternatives such as the Taskmaster CLI, which felt overpowered relative to the control offered by a hand-cranked markdown checklist. Supporting observations include sticking with one model long enough to learn its strengths, iterating on the rule files themselves whenever they fail, keeping task tracking in plain markdown rather than graduating early to project-management integrations, and leaning on a Postgres MCP for everyday database questions, Browserbase and Stagehand MCPs for driving a cloud browser from chat, and Repo Prompt on the Mac for shrinking a hundreds-of-thousands-token repository down to a small curated context bundle before asking architectural questions.

## Suggestions & Future Directions

The video's advice to practitioners is to start small and simple with markdown task lists and only graduate to richer tooling once the basic loop is working, to refine rule files empirically whenever the agent misbehaves, and to treat the agent the way one would treat a person by giving it the right context and polite, coaching-style redirection when it stalls. Looking ahead, the speaker points toward front-end testing driven from the editor through headless-browser MCPs as a replacement for pasting screenshots back and forth while chasing bugs, alongside tighter explicit context control as repositories grow. The closing stance is cultural as much as technical: nobody fully knows how to do this yet, so progress comes from hands-on experimentation, steady iteration on prompts and process, and accepting a workflow that is not quite a dedicated product manager or CTO but is sufficient for one person to build a company alone.

## Authors & Institutions

The presenter is Ryan Carson, described in the title as a five-time founder and in the material as a solo founder drawing on prior experience running a company of around one hundred employees with dedicated product and engineering leadership. No separate paper authors or research institution are involved; the artifact is a practitioner video demonstrating a Cursor-based workflow with open-sourced rule files and commercially available models and integrations.
