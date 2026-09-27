> [[../index|Wiki]] | [[../summary|Summary]] | [[../digest|Digest]]
# Give your agent a laboratory
**In one sentence:** Coding agents are only as good as their feedback loop, so instead of vague instructions you must give the agent a laboratory — tools and scaffolding to view, measure, and verify its own work.
## Key points
- Coding agents are only as good as their feedback loop: the agent must be able to view and verify its own work rather than asking the human to check it manually.
- If the agent ever asks you to do something manually, stop and think hard about how to give it the tools it needs so it can do the thing by itself.
- Vague prompts like "make it faster… find bugs… refactor the code… simplify the design…" fail because the agent works only a short time ("they're lazy"), keeps asking for verification, or fixes one thing while breaking something elsewhere.
- The performance-laboratory pattern runs in 4 phases — Instrumentation (baseline harness), Diagnosis (top 3–5 bottlenecks with hypotheses), Iteration (one change at a time, re-benchmark, commit each win), Report (HTML before/after with charts).
- The visual-laboratory pattern is: pull the Figma source via Figma MCP, build an expected-wrong first pass, then loop screenshot via Chrome Devtools MCP → compare → list every spacing/color/typography/radius/shadow/border/alignment/responsive difference → fix one by one until no differences remain.
- Useful workflows discovered by prompting should be encoded as reusable skills/commands/subagents in `./claude/skills`, but not formalized too early — get reps first to develop model feel for how much scaffolding a task needs.
---
## Core claim: feedback loop over wording
The words in a prompt matter less than reorienting your mental model toward what makes an effective prompt: a verifiable loop.

Verbatim rules from the chunk:

> "This is where we are in January 2026: coding agents are only as good as their feedback loop."

> "You must give your agent the ability to view and verify its own work."

> "If the agent ever asks you to do something manually, you should 1) stop 2) think really really hard about how to give the agent the tools it needs so it can do the thing by itself."

Failure mode of vague prompting (`"make it faster…find bugs…refactor the code…simplify the design…"`): short effort, repeated requests to check work, or fixing one thing while breaking another part of the codebase.

**Covers:** Core claim section (lines 27–35 of chunk)

## Example 1 — performance laboratory
Before:

> "The app is really slow. Do a complete audit of the codebase and make it faster."

After — build the laboratory before touching code:

| Phase | Mechanism |
|---|---|
| 1 — Instrumentation | Build a benchmark harness measuring the current state; timing utilities for scripts; Chrome Devtools MCP `console.time` markers plus performance traces for browser code; record baseline numbers for the critical paths |
| 2 — Diagnosis | Analyze benchmarks; identify the top 3–5 bottlenecks; for each, write a hypothesis about cause and candidate fix; use web search for known gotchas with the specific libraries/patterns |
| 3 — Iteration | Work through hypotheses one at a time: make the change, re-run the benchmark, compare to baseline; keep changes that improve performance without breaking tests; commit after each successful change for later cherry-picking |
| 4 — Report | Generate an HTML report with before/after comparisons — charts showing where time went and how much was recovered |

Boundary rule: flag anything requiring a larger architectural change and move on; ask questions when blocked.

**Covers:** Example 1 section of chunk

## Example 2 — Figma visual refinement loop
Before:

> "Use the Figma MCP to implement this design: {figma url}"

After:

> "Implement this design: {figma url}"

Steps:

1. Pull the design using the Figma MCP and study layout, components, and visual details before writing code.
2. Build a first pass — "It will be wrong. That's expected."
3. Run a refinement loop:
   - Screenshot the implementation via Chrome Devtools MCP and inspect properties directly.
   - Compare it to the Figma source.
   - List every difference: spacing, color, typography, radius, shadows, borders, alignment, responsive behavior.
   - Fix them one by one, verifying each fix in the browser.
   - Keep looping until no differences can be found.
4. Standard: "Be obsessive about the details—the gap between 'close enough' and 'correct' is where polish lives."
5. If something is ambiguous or impossible to implement as spec'd, ask rather than guessing.

**Covers:** Example 2 section of chunk

## Notes: verbosity, reps, and skills
- As models improve, the need for verbose prompting will decline; in the meantime a dictation app like Monologue saves time.
- Not every prompt needs to be as long as these examples — rigor depends on the job; iterate until intuition develops for how much scaffolding a task needs.
- Learn how the agent handles skills/commands/subagents to encode workflows, but don't formalize too early — reps are needed to develop model feel first.
- Pro tip, verbatim instruction to give the agent:

> "Take everything we learned from this conversation, including my prompts over time as well as your approach to solving the problem, and create a new skill for this in the ./claude/skills directory with a clear name and description that will help you rerun this exact workflow again in the future."

**Covers:** Notes section through end of chunk (Brian Lovin, Writing, Jan 14, 2026; Also read: Give your agent a stopwatch)
