> [[index|Wiki]] | [[summary|Summary]]
# Give your agent a laboratory — Digest

## 1. [[wiki/01-give-your-agent-a-laboratory|Give your agent a laboratory]]
**In one sentence:** Coding agents are only as good as their feedback loop, so instead of vague instructions you must give the agent a laboratory — tools and scaffolding to view, measure, and verify its own work.
## Key points
- Coding agents are only as good as their feedback loop: the agent must be able to view and verify its own work rather than asking the human to check it manually.
- If the agent ever asks you to do something manually, stop and think hard about how to give it the tools it needs so it can do the thing by itself.
- Vague prompts like "make it faster… find bugs… refactor the code… simplify the design…" fail because the agent works only a short time ("they're lazy"), keeps asking for verification, or fixes one thing while breaking something elsewhere.
- The performance-laboratory pattern runs in 4 phases — Instrumentation (baseline harness), Diagnosis (top 3–5 bottlenecks with hypotheses), Iteration (one change at a time, re-benchmark, commit each win), Report (HTML before/after with charts).
- The visual-laboratory pattern is: pull the Figma source via Figma MCP, build an expected-wrong first pass, then loop screenshot via Chrome Devtools MCP → compare → list every spacing/color/typography/radius/shadow/border/alignment/responsive difference → fix one by one until no differences remain.
- Useful workflows discovered by prompting should be encoded as reusable skills/commands/subagents in `./claude/skills`, but not formalized too early — get reps first to develop model feel for how much scaffolding a task needs.

## The argument in five moves
1. The core claim reframes prompting: what matters is not wording but giving the agent a verifiable feedback loop so it can view and verify its own work.
2. Vague instructions fail because the agent puts in short effort, keeps asking the human to check, or fixes one thing while breaking another.
3. The performance laboratory answers this with a four-phase loop — instrument a baseline harness, diagnose the top bottlenecks with hypotheses, iterate one change at a time with re-benchmarks and commits, then report before/after.
4. The visual laboratory applies the same loop to design work — pull Figma via MCP, build an expected-wrong first pass, then screenshot, compare, and fix every difference until none remain.
5. Once such workflows prove themselves through reps, encode them as reusable skills/commands/subagents — calibrating verbosity and scaffolding to the job rather than formalizing too early.
