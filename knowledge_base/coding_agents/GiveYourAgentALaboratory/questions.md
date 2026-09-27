---
type: Retrieval Prompts
last_reviewed: null
review_count: 0
---
> [[index|Wiki]] | [[summary|Summary]] | [[digest|Digest]]
# Retrieval Practice: Give your agent a laboratory

### Q1. What is the core claim of "Give your agent a laboratory" about what makes a coding agent effective?
> [!tip]- Answer
> A coding agent is only as good as its feedback loop, so prompt wording matters less than giving the agent tools and scaffolding to view, measure, and verify its own work. Without that laboratory, the agent must rely on the human to check everything it does. See [[wiki/01-give-your-agent-a-laboratory|Give your agent a laboratory]].

### Q2. What should you do when the agent asks you to do something manually?
> [!tip]- Answer
> Stop, and think hard about how to give the agent the tools it needs so it can do that thing by itself. Performing the manual step for it leaves the dependency in place instead of fixing the missing capability. See [[wiki/01-give-your-agent-a-laboratory|Give your agent a laboratory]].

### Q3. Why do vague prompts like "make it faster" or "refactor the code" fail?
> [!tip]- Answer
> The agent puts in only short effort, keeps asking the human to check its work, or fixes one thing while breaking something elsewhere. This happens because vague instructions give it no verifiable loop for measuring or confirming its own results. See [[wiki/01-give-your-agent-a-laboratory|Give your agent a laboratory]].

### Q4. What are the four phases of the performance laboratory, and what happens in the first two?
> [!tip]- Answer
> The phases are Instrumentation, Diagnosis, Iteration, and Report. Instrumentation builds a benchmark harness with timing utilities and traces to record baseline numbers, and Diagnosis analyzes benchmarks to identify the top 3–5 bottlenecks with a cause hypothesis and candidate fix for each. See [[wiki/01-give-your-agent-a-laboratory|Give your agent a laboratory]].

### Q5. In the performance laboratory's Iteration and Report phases, what discipline keeps changes safe and reviewable?
> [!tip]- Answer
> Work through hypotheses one change at a time, re-run the benchmark against the baseline, keep only changes that improve performance without breaking tests, and commit after each win. Then generate an HTML report with before/after charts showing where time went and how much was recovered. See [[wiki/01-give-your-agent-a-laboratory|Give your agent a laboratory]].

### Q6. Describe the visual-laboratory loop for implementing a Figma design.
> [!tip]- Answer
> Pull the design via Figma MCP and build a first pass that is expected to be wrong. Then loop until no differences remain: screenshot via Chrome Devtools MCP, compare against the Figma source, and list and fix every spacing, color, typography, radius, shadow, border, alignment, and responsive difference one by one. See [[wiki/01-give-your-agent-a-laboratory|Give your agent a laboratory]].

### Q7. When should you encode a discovered workflow as a reusable skill or subagent, and where does it go?
> [!tip]- Answer
> Encode it only after enough reps to develop a feel for how much scaffolding the task needs, rather than formalizing too early. The skill goes in the `./claude/skills` directory with a clear name and description so the workflow can be rerun. See [[wiki/01-give-your-agent-a-laboratory|Give your agent a laboratory]].

### Q8. A teammate proposes skipping the laboratory and just writing a longer, more detailed prompt for a tricky refactor. Should you agree, and why?
> [!tip]- Answer
> No: verbosity without a verifiable loop still leaves the agent unable to measure or check its own work, so it will likely under-invest effort or break unrelated code. Build the smallest laboratory that fits the job — baseline, verification, and iteration scaffolding — and calibrate prompt length to the task instead. See [[wiki/01-give-your-agent-a-laboratory|Give your agent a laboratory]].
