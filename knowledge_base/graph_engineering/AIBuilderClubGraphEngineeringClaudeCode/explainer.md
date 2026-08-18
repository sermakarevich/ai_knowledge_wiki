> [[index|Wiki]] | [[summary|Summary]]

# Graph Engineering with Claude Code — In Plain Language

## What is this about?

Imagine you hired one very capable assistant to handle an entire project alone — research it, write it up, check their own work, fix mistakes, ship it. That works for small jobs, but for bigger ones it helps to split the work across a small team instead: one person researches, one writes, one reviews. "Graph engineering" is the fancy name for designing that team — who does what, who hands work to whom, and what information passes between them.

This article's point is simple: if you use Claude Code (Anthropic's coding assistant tool), you can already build that team without installing any new software. Claude Code lets you define separate helper assistants ("subagents"), have a main assistant decide which helper to call and when, and pass results between them. Those three things — helpers, decisions, and passed-along results — are exactly what a "graph" is, just under different names.

## Why does it matter?

A lot of online chatter in mid-2026 made "graph engineering" sound like a brand-new skill or product category you had to go learn from scratch. That confusion wastes time: builders start hunting for a framework to install when what they actually need is already sitting in the tool they use every day. This article cuts through that by showing the mapping directly, so someone can start building a small agent team today instead of shopping for a framework.

## How does it work?

Picture a factory floor analogy:

1. **A single worker on a loop** is one assistant doing everything itself, looping through: figure out what to do, do it, check the result, repeat until done. That is the simplest possible "graph" — one station with a rework line to itself.
2. **Nodes** are the individual workers/stations — in Claude Code, each is a "subagent": a separate assistant with its own instructions and its own limited set of tools (a reviewer, for instance, might be allowed to read but not to edit files).
3. **Edges** are the decisions about which station gets the work next. In Claude Code, the main assistant (the "orchestrator") makes those calls live, based on what just happened — so the wiring is decided on the fly rather than drawn out ahead of time like a flowchart.
4. **Shared state** is the paperwork that moves down the line — each worker's finished output becomes the input the next worker receives.
5. To build this, Claude Code gives you three tools, roughly in order of how much you commit to the setup:
   - **Subagent files** — small text files describing each helper's job. Fastest to set up.
   - **Hooks** — a way to force a step to always happen (e.g. "always run the tests before the writer hands off"), instead of hoping the assistant remembers.
   - **The Claude Agent SDK** — a way to write the whole team's logic in code, for when the setup needs to run unattended or be tested like software.
6. The recommended order: build the team by hand first inside Claude Code, watch how it behaves, and only translate it into code (the SDK) once you understand the shape of the team you built.

## Where can this be used?

- **Content pipelines**: a researcher subagent gathers sources, a writer drafts, a reviewer checks and can send the draft back for revisions.
- **Software development**: a coder subagent implements a change, a test-runner (or hook) always runs the test suite, a reviewer subagent checks the diff.
- **Any "produce, then check" job**: as long as one part of the work can be judged independently of the part that produced it, splitting the two into separate helpers tends to work better than one assistant doing both.
- It is not just for coding tools — the same pattern (isolated workers, a decision-maker routing between them, results passed along) is the same idea behind many multi-agent AI systems, including Anthropic's own internal research tool.

## Conclusions & takeaways

- You do not need a new framework to start building a small team of AI helpers — Claude Code's existing features already cover the basics.
- More helpers is not automatically better: Anthropic's own numbers show a real team of helpers beat one assistant by a large margin (90.2%) but also cost roughly 15 times more computing resources than a normal single-assistant conversation — and an early version of their system wastefully spun up helpers for questions that did not need a team at all.
- Building a team of unreliable helpers just produces more unreliable output, faster and more expensively. Get each helper working well solo first, then wire them together.
- Start small: a handful of clearly-named helpers whose hand-offs you fully understand beats a large, complicated team you cannot reason about.

## Jargon decoder

| Term | Plain meaning |
|------|---------------|
| Node | One worker/step in the team — in Claude Code, a subagent doing one focused job. |
| Edge | The decision about which worker goes next — in Claude Code, the main assistant's live routing choice. |
| Shared state | The information passed from one worker to the next — a subagent's finished result. |
| Orchestrator | The main assistant that decides which helper to call, when, and with what instructions. |
| Subagent | A separate helper assistant with its own instructions and its own limited toolset, spun up by the main assistant. |
| Hook | A rule that forces a step to happen every time (not just "usually"), e.g. always run tests before handoff. |
| Fan-out / fan-in | Splitting a job across several helpers running at once (fan-out), then gathering their results back together (fan-in). |
| Claude Agent SDK | A programming toolkit for defining the same helpers-and-routing setup in code, for automated or unattended use. |
