> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]

# Agent Harness Engineering — In Plain Language

## What is this about?

Think of a talented chef placed in two kitchens. In one kitchen the knives are sharp, the ingredients are labelled, and someone cleans up as they go. In the other, everything is missing or messy. Same chef, very different dinner. The digest says a coding agent works the same way: the model (the clever text-predicting brain) is the chef, and the harness (everything built around the model) is the kitchen.

A coding agent equals the model plus everything around it. The harness is all the non-model parts: the written instructions (system prompts, files like CLAUDE.md or AGENTS.md), the extra knowledge packets called skills, the helper programs and tool connections, the files and folders it works in, the way work is split between helper agents, the automatic checks that run at key moments, and the logs that track cost and speed. The core habit inside that kitchen is the ReAct loop (a short name for Reasoning and Acting): reason about what to do next, call a tool to act, observe the result, then repeat.

The big habit the digest teaches is simple: design backwards from behaviour. Decide what behaviour you want (or what failure you just saw), then add exactly the harness piece that produces it. Nothing extra. And every time the agent slips in real work, permanently build a guard into the harness so the same mistake cannot happen again. That tighten-after-every-slip habit is called the ratchet.

## Why does it matter?

- The kitchen matters more than the chef. Tools like Claude Code, Cursor, Codex, Aider, and Cline share similar underlying models yet behave very differently, because their harness designs differ.
- A decent model with a great harness can beat a great model with a bad harness. On a test called Terminal Bench 2.0, one strong model scored far lower inside one harness than inside a custom-built one.
- Small harness changes can move results a lot. One team moved their coding agent from around the Top 30 to the Top 5 by changing only the harness, not the model.
- Most failures are setup problems, not brain problems. Missing instructions go into AGENTS.md, dangerous commands get automatic blockers, long 40-step jobs get split into a planner plus a doer, and false "I am done" answers get wired to a re-check step.
- Models get used to the kitchen they trained with. The digest calls this post-training coupling: a model is partly shaped by its training harness, so the harness around it in real use matters a great deal.

## How does it work?

1. Start with a goal and a workspace. The agent gets a task plus a folder with code, documents, and data, tracked with Git (a version system that saves history, so you can review progress, undo mistakes, and try side branches).
2. Reason: what is the next small step? The model looks at the goal, the instructions, and what has happened so far, and picks one action.
3. Act with a general tool, usually the shell. Instead of pre-building a button for every possible job, the harness gives the agent Bash (the terminal shell, a text-based way to run commands) plus code execution. The agent is good at the shell, so one flexible tool covers a huge range of jobs.
4. Observe the result. The tool returns text: file contents, an error message, a test result. That observation goes back into the agent's working memory.
5. Repeat the loop. Reason, act, observe, repeat. This ReAct loop is the heartbeat: each round moves one small step closer to the goal.
6. Keep the memory from rotting. Long jobs fill up the model's working memory (called context), and old material degrades (called context rot). The harness fights this four ways: shrink old history into summaries, keep only the head and tail of big outputs in memory while saving full files to disk, give skills that reveal details step by step, or restart with fresh memory plus a hand-off note.
7. Enforce rules quietly. Automatic checks called hooks fire at key moments: before a tool runs, after a file edit, before a save. The rule is "success is silent, failures are loud", so the agent is only interrupted when something is wrong.
8. Verify before claiming done. For longer work the harness uses plan files plus self-checks, and splits judging from doing (one part generates, another part evaluates), because grading your own work skews positive.
9. Stretch long jobs with fresh starts. For very long tasks the digest describes Ralph Loops: when the agent tries to quit, a hook stops the exit, puts the original goal back in with fresh memory, and points at files on disk for state, so work continues until a clear finish line is met.
10. Grow up into a service. As models improve, the scaffolding moves instead of vanishing. The industry is shifting toward Harness-as-a-Service (HaaS, meaning you rent the loop, tools, memory handling, and safety checks as a ready-made runtime): ready kits like the Claude Agent SDK, Codex SDK, and OpenAI Agents SDK (SDK means Software Development Kit, a box of ready-made building blocks). You configure four pillars — instructions, tools, memory handling, and helper agents — starting from a rough first version.

## Where can this be used?

- Everyday coding helpers. Any tool where the model edits code, runs commands, and reads results lives or dies by its harness: instructions, tools, sandbox, and checks.
- Long multi-step jobs. Tasks that take dozens of steps need plan files, fresh-memory restarts, hand-off notes, and split-up roles like planner plus executor.
- Teams that keep tripping on the same mistake. The ratchet pattern fits anywhere: a merged mistake becomes a written rule, an automatic search for the bad pattern, and a reviewer helper that blocks repeats.
- Safe production setups. Sandboxes (isolated work areas), permission gates that block destructive actions, separate memory zones for helper agents, and logs for cost and delay all come from the harness parts list.
- Starting fast without building everything. Instead of hand-building the whole loop, a team can start from a Harness-as-a-Service runtime and configure the four pillars, then improve step by step.

## Conclusions & takeaways

- Behaviour comes mostly from the harness, not the model choice. If results are bad, look at the scaffolding first.
- Every harness piece should earn its place by producing a named behaviour. If you cannot say which behaviour it delivers, remove it.
- Short instructions and few sharp tools win. Keep files like AGENTS.md short (one cited rule of thumb: under 60 lines, and earn each line), and prefer about ten focused tools over fifty overlapping ones.
- Honest limits: scaffolding does not disappear when models get smarter, it just moves. Every harness part bakes in a guess about what the model cannot do alone, so when the model improves, old scaffolding can become dead weight while new gaps (like multi-day memory or coordinating many agents) appear.
- Honest limits, continued: self-checks are weak on their own, history degrades over long runs, and constraints should only be added after a real failure — otherwise the harness fills up with guesses instead of fixes.

## Jargon decoder

| Term | What it means in plain language |
| ---- | ------------------------------- |
| Harness | Everything around the model: instructions, tools, workspace, checks, and logs |
| Harness engineering | The job of tightening that scaffolding after every real failure |
| ReAct loop | The repeat cycle: think, act with a tool, read the result, think again |
| Behaviour-first design | Start from the behaviour you want, then build only the piece that delivers it |
| Ratchet | Add a permanent guard after each real slip, so the same failure never returns |
| Context rot | Working memory filling up and going stale on long jobs |
| Compaction | Shrinking old history into a short summary to free working memory |
| Skill (with progressive disclosure) | An extra knowledge packet that reveals details step by step, only when needed |
| Hook | An automatic check that runs at a key moment, such as before a risky command |
| Ralph Loop | A restart trick for long jobs: fresh memory plus the original goal, state kept in files |
| Generator / evaluator split | One part does the work, a separate part judges it, to avoid self-praise bias |
| Harness-as-a-Service (HaaS) | A ready-made rented runtime that provides the loop, tools, memory handling, and safety checks |
