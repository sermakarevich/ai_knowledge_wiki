# A Harness for Every Task: Dynamic Workflows in Claude Code

**Article:** [A harness for every task: dynamic workflows in Claude Code (Thariq Shihipar & Sid Bidasaria, 2026)](https://x.com/trq212/status/2061907337154367865)
**Also available:** [Claude Blog](https://claude.com/blog/a-harness-for-every-task-dynamic-workflows-in-claude-code)

## Human Readable TL;DR

Think of Claude Code like a chef who can now write their own recipe on the spot instead of always following the same cookbook. When you give Claude a big, complex job — like reviewing 50 resumes or auditing your entire codebase for security issues — it can now create a custom plan that spins up multiple "helpers" working in parallel, each with their own focused task. This makes Claude much better at huge, long-running jobs where a single assistant would lose focus or get tired.

## TL;DR

Claude Code now supports dynamic workflows — on-the-fly JavaScript harnesses that Claude writes itself to orchestrate parallel subagents with isolated context windows. This addresses three key single-context failure modes (agentic laziness, self-preferential bias, goal drift) by distributing work across focused agents. Dynamic workflows are triggered via the `ultracode` keyword or explicit prompting, and can be saved, shared via skills, and combined with `/loop` and `/goal` for sustained autonomous operation.

---

## Problem & Motivation

The default Claude Code harness — effective for most coding tasks — breaks down for long-running, massively parallel, or highly structured adversarial tasks. Three failure modes emerge as context grows:

- **Agentic laziness** — Claude stops before completing a complex multi-part task (e.g., addresses 20/50 security review items and declares done)
- **Self-preferential bias** — Claude tends to prefer its own prior results when asked to verify or judge them
- **Goal drift** — original constraints and edge-case requirements erode across compaction cycles

Static workflows (Agent SDK, `claude -p`) partially address this but must be generic. Dynamic workflows let Claude Opus 4.8 write a custom harness tailor-made for the specific task.

---

## Main Original Ideas

1. **Dynamic harness generation** -- Claude writes a JavaScript workflow file on the fly that calls `agent()`, `parallel()`, `pipeline()`, and `phase()` to coordinate subagents. Each subagent gets its own clean context window and focused goal.

2. **Structural prevention of failure modes** -- By spinning up separate Claude instances with disjoint evidence, self-preferential bias is architecturally prevented rather than prompted away.

3. **Resumable workflows** -- If interrupted (user action, terminal quit), resuming the session picks up where it left off — the workflow state persists.

4. **Model and isolation routing** -- Workflows can decide per-agent which model to use and whether subagents run in their own worktree, allowing Claude to choose intelligence level and isolation dynamically.

5. **Composable workflow patterns** -- Six reusable primitives that Claude composes when building harnesses:

   | Pattern | Description |
   |---------|-------------|
   | **Classify-and-act** | Classifier agent routes to specialized agents based on task type |
   | **Fan-out-and-synthesize** | Split into parallel subagents, then synthesize at a barrier |
   | **Adversarial verification** | Each finding agent paired with a dedicated refuter agent |
   | **Generate-and-filter** | Generate many ideas, filter/dedup by rubric |
   | **Tournament** | N agents attempt the same task; pairwise judging selects winner |
   | **Loop until done** | Spawn agents until stop condition (no new findings, no errors) |

---

## Key Findings

### Real-world use cases
- **Migrations & refactors** -- Bun's entire rewrite from Zig to Rust was done using workflows ([Jarred's thread](https://x.com/jarredsumner/status/2060050578026189172))
- **Deep research** -- `/deep-research` skill is a live implementation: fan-out web searches → fetch → adversarial verify → synthesize
- **Deep verification** -- One agent extracts all factual claims; subagents source-check each one; verifier checks source quality
- **Sorting at scale** -- 1000+ support tickets sorted via pairwise-comparison tournament (comparative judgment > absolute scoring)
- **Memory mining** -- Mine session history for recurring corrections; cluster, adversarially verify, distill into `CLAUDE.md` rules
- **Triaging** -- Continuous queue processing with quarantine pattern (untrusted-content readers separated from high-privilege actors)
- **Root-cause investigation** -- Independent agents for logs/files/data generate hypotheses; panel of verifiers and refuters evaluate each
- **Evals** -- Spin off worktree agents to attempt tasks; comparison agents grade against rubric

### Performance characteristics
- Uses significantly more tokens than single-context operation
- Best for tasks that genuinely need parallelism, adversarial verification, or scale beyond one context window
- Regular coding tasks do not benefit from "a panel of 5 reviewers"

---

## Suggestions & Future Directions

1. **Pair with `/loop` and `/goal`** for sustained autonomous operation (e.g., continuous triage, recurring verification at intervals)
2. **Set explicit token budgets** via prompting ("use 10k tokens") to control cost on large workflows
3. **Save and share workflows** via `~/.claude/workflows/` or distribute through skills; treat saved workflows as templates, not verbatim scripts
4. **Quick workflows for small tasks** -- Adversarial review of a single assumption doesn't require a large harness; workflows aren't just for massive jobs
5. **Quarantine pattern for untrusted content** -- Separate read agents from action agents when processing public/external data
6. Best practices are still developing — the community is actively discovering new use cases and patterns

---

## Example Prompts

```
"This test fails maybe 1 in 50 runs. Set up a workflow to reproduce it, form theories and adversarially test them in worktrees /goal don't stop until one theory works."

"Using a workflow, go through my last 50 sessions and mine them for corrections I keep making and turn the recurring ones into CLAUDE.md rules"

"Use a workflow to dig through #incidents in Slack for the past six months and find recurring root causes where nobody has filed a ticket."

"Take my business plan and run a workflow where different agents tear it apart from an investor's, a customer's, and a competitor's perspective."

"Here's a folder of 80 resumes, use a workflow to rank them for the backend role and double-check the top ten."

"Use a workflow to rename our User model to Account everywhere."
```

---

## Authors & Institutions

**Thariq Shihipar** (@trq212) and **Sid Bidasaria** (@sidbid) — Members of Technical Staff at Anthropic, Claude Code team. Published June 2, 2026.
