> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# My LLM coding workflow going into 2026 | AddyOsmani.com — In Plain Language

## What is this about?

This is a practical playbook for coding with an AI assistant without losing control of quality.

The core idea is simple: plan first, then build in small steps, and check everything the AI writes.

Instead of typing a vague wish like "build me an app" and hoping for the best, you first talk through the idea with the AI until you have a written specification (a `spec.md` file) and a short step-by-step project plan.

Then you implement the plan one small piece at a time — code it, test it, save it — before moving on.

Around that loop, the author adds three safety layers: supervised AI helpers, style rules that steer the AI, and automatic checks (tests, linters, staging) that catch mistakes.

The human stays in charge throughout, like a senior developer guiding a fast but inexperienced junior.

## Why does it matter?

AI coding tools are powerful but unreliable in a specific way: they write with total confidence, even when they are wrong.

Without a plan and checks, a big one-shot request produces a tangled mess — duplicated logic, mismatched names, no clear structure — that one developer described as "like 10 devs worked on it without talking to each other."

That mess is painful to untangle and can look finished until it falls apart later.

This workflow matters because it turns the AI from a gamble into a dependable assistant.

Upfront planning is cheap — one quoted developer calls it "a waterfall in 15 minutes" — but it prevents hours of rework by getting the human and the AI onto the same page early.

Small steps plus tests plus frequent saves mean any bad AI suggestion can be spotted, fixed, or undone quickly instead of poisoning the whole project.

## How does it work?

Think of it as five habits that fit together.

**1. Write the spec before any code.**

Describe your idea, then ask the AI to keep asking you questions until the requirements and tricky edge cases are clear.

Save the result as a `spec.md` file: what the software must do, the main design choices, the data shapes, and how you will test it.

Then ask a capable model to turn that spec into a short plan of small tasks, and ask it to critique and improve the plan until it reads sensibly.

**2. Build one small chunk at a time.**

Prompt the AI with something like "let's implement Step 1 from the plan," then code it, run the tests, and only then move to Step 2.

Small requests play to the AI's strength at quick, contained tasks and make errors easy to spot and reverse.

Some teams keep a "prompt plan" file — a numbered list of per-task prompts — so tools execute them one by one.

**3. Use AI helpers, but supervise them.**

Two kinds of helpers appear: chat agents that work inside your project folder (reading files, running tests, fixing bugs step by step), and background agents that clone the repo, work in the cloud, and return later with a pull request.

Give them the plan and spec files for context, watch what they do, and mostly stick to one main worker plus one reviewer — running many agents at once is mentally exhausting.

**4. Verify everything and save often.**

Treat every AI suggestion as draft code from a junior colleague: run the test suite after each task, read the code line by line, and only keep code you actually understand.

A handy trick is to have a second AI session review the first one's code.

Commit after each small working step with a clear message — these are "save points in a game" — and use branches or isolated copies so failed experiments can be thrown away safely.

**5. Teach the AI your style, and let automation check its homework.**

Keep a rules file (such as `CLAUDE.md`) with your project style, lint rules, and things to avoid, plus short instructions for other tools, and show the AI one or two examples to copy.

Add honesty rules like "if you are unsure, ask instead of guessing" and "explain bug fixes briefly in comments."

Then back it all with automatic checks on every change — tests, style checks, a staging copy — and paste any failure messages straight back to the AI so it can fix them.

## Where can this be used?

- Starting a new feature or side project: brainstorm the spec with the AI, agree a bite-sized plan, then build step by step.
- Repetitive coding chores: boilerplate, renames, small refactors, and writing first-draft tests via a supervised agent.
- Bug fixing: ask an agent to reproduce the issue, run the tests, and propose a fix — then review the diff and keep the fix only if the tests pass and you understand it.
- Background improvements: hand a well-described task ("refactor the payment module for X, keep tests green") to a cloud agent and review the resulting pull request later.
- Team consistency: share the rules file and style instructions so every AI suggestion matches house style, and let code-review bots feed comments back as follow-up fix prompts.
- Learning on the job: ask the AI to explain its code, compare design options, or show alternative approaches — like an always-available mentor.

## Conclusions & takeaways

- Plan before you prompt: a written spec plus a small-step plan is the highest-leverage part of the whole workflow.
- Small loops win: one task, one test run, one save — large leaps create large messes.
- The AI accelerates; it does not take responsibility — you remain the accountable engineer who reviews, tests, and understands every line you keep.
- Save points and isolation are cheap insurance: commit often, keep history tidy, and experiment in branches or separate copies.
- Tune the tool and automate the checks: rules files plus tests, linters, and staging catch what tired eyes miss.
- The shorthand for all of this is "AI-augmented, not AI-automated" engineering: classic good habits — design, tests, version control, standards — matter even more when AI writes much of the code, and solid fundamentals plus AI compound while weak fundamentals plus AI just fail faster.

## Jargon decoder

| Term | What it means in plain language |
|---|---|
| Spec (spec.md) | A written description of what the software must do, agreed before coding starts. |
| Project / prompt plan | The ordered list of small tasks (or prompts) that turns the spec into working code. |
| CLI agent | A chat-based AI helper that works inside your project folder: reads files, runs commands, edits code. |
| Async / cloud agent | An AI helper that works in the background on a copy of your code and returns later with proposed changes. |
| Pull request (PR) | A packaged proposal to merge changes into the main code, reviewed before acceptance. |
| Test suite | The collection of automatic checks that verify the code still behaves as expected. |
| Linter (e.g. ESLint, Prettier) | An automatic style-and-error checker that flags formatting and common mistakes. |
| CI / staging | Automatic checks on every change (CI), plus a safe preview copy of the app (staging) for trying things out. |
| Commit / save point | A saved snapshot of the code with a message, so you can undo or compare later. |
| Rules file (e.g. CLAUDE.md) | A short file of house rules and preferences that steers the AI toward your team's style. |
