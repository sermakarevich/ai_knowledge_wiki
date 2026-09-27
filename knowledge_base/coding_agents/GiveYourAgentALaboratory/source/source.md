# Give your agent a laboratory
> PDF location (no local source.pdf): https://brianlovin.com/writing/give-your-agent-a-laboratory-jH5ryjC
Source: https://brianlovin.com/writing/give-your-agent-a-laboratory-jH5ryjC
Kind: article
Fetched: 2026-09-24T04:59:08.322663+00:00
Tool: urllib
Topic: coding_agents

Give your agent a laboratory

Brian Lovin

/

Writing

Jan 14, 2026

# Give your agent a laboratory

2

4

3

Also read: Give your agent a stopwatch

This is where we are in January 2026: coding agents are only as good as their feedback loop.

You must give your agent the ability to view and verify its own work.

If the agent ever asks you to do something manually, you should 1) stop 2) think really really hard about how to give the agent the tools it needs so it can do the thing by itself.

If you are still typing things like “make it faster…find bugs…refactor the code…simplify the design…” you’re in for a bad time. Your agent will only work for a short time (they’re lazy!). Or it might keep asking you to check its work. Or it might fix one thing but break something else in another part of the code base.

Below are some prompting examples. The words aren’t as important as showing you how to reorient your mental model for what makes an effective prompt.

## Example 1

Before:

The app is really slow. Do a complete audit of the codebase and make it faster.

After:

Your job is to make this app faster. Before you touch any code, you need to build yourself a laboratory.

Phase 1 — Instrumentation: Build a benchmark harness that measures the current state. For scripts, create timing utilities. For browser code, use the Chrome Devtools MCP to add console.time markers and capture performance traces. Record baseline numbers for the critical paths.

Phase 2 — Diagnosis: Analyze the benchmarks. Identify the top 3-5 bottlenecks. For each one, write a hypothesis about what's causing it and what fix you'd try. Use web search to check for known gotchas with the specific libraries/patterns involved.

Phase 3 — Iteration: Work through each hypothesis one at a time. Make the change, re-run the benchmark, compare to baseline. Keep changes that improve performance without breaking tests. Commit after each successful change so we can cherry-pick later.

Phase 4 — Report: When you're done, generate an HTML report with before/after comparisons—charts showing where time went and how much you recovered.

If you hit something that requires a larger architectural change, flag it and move on. Ask me questions when you're blocked.

## Example 2

Before:

Use the Figma MCP to implement this design: {figma url}

After:

Implement this design: {figma url}

First, pull the design using the Figma MCP and study it—understand the layout, components, and visual details before writing code.

Then build a first pass. It will be wrong. That's expected.

Now run a refinement loop:

Screenshot your implementation via Chrome Devtools MCP and inspect the properties directly

Compare it to the Figma source

List every difference you spot: spacing, color, typography, radius, shadows, borders, alignment, responsive behavior

Fix them one by one, verifying each fix in the browser

Keep looping until you can't find any differences. Be obsessive about the details—the gap between "close enough" and "correct" is where polish lives.

If something in the design is ambiguous or impossible to implement as spec'd, ask me rather than guessing.

## Notes

As models improve, the need for verbose prompting will decline. In the meantime, using a dictation app like Monologue will save you time.

Not every prompt needs to be as long as these examples. It depends on the rigor required for the job at hand. Iterate until you develop intuition for how much scaffolding a task actually needs.

Learn how your agent handles skills/commands/subagents so you can encode workflows—but don't formalize too early. You need reps to develop model feel first.

Prompting is subjective. If you spot ways to improve these examples, DM me.

Pro tip: when you've prompted your way to a useful workflow, tell the agent: "Take everything we learned from this conversation, including my prompts over time as well as your approach to solving the problem, and create a new skill for this in the ./claude/skills directory with a clear name and description that will help you rerun this exact workflow again in the future."

## Read next

Use the ✦ Hyper key

Grok Bot first impressions

Caching API routes with Next.js + Now

On working nights and weekends

Typing fast is a high-leverage skill
