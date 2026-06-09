# Orchestrate Subagents at Scale with Dynamic Workflows

**Source:** [Claude Code Docs -- Dynamic Workflows](https://code.claude.com/docs/en/workflows)

## Human Readable TL;DR

Imagine you need to send 500 workers to check every room in a giant building at once, then gather all their reports into one summary -- rather than walking room by room yourself. Claude Code's dynamic workflows work the same way: Claude writes a script (a plan on paper) that sends out dozens or hundreds of AI assistants simultaneously to tackle a huge task, while you wait for a single polished result. You can save those scripts and reuse them like saved recipes, and if the job gets interrupted, it can pick up where it left off.

## TL;DR

Dynamic workflows are JavaScript scripts that Claude writes and a runtime executes to orchestrate up to 1,000 subagents per run. Unlike conversational subagents where Claude holds the plan in its context window, workflows move orchestration logic into code -- enabling scale (up to 16 concurrent agents), resumability, and repeatable quality patterns like adversarial cross-checking. Available in Claude Code v2.1.154+ on all paid plans.

---

## Problem & Motivation

Standard subagent and skill approaches break down at scale: every intermediate result lands in Claude's context window, Claude must re-decide what to spawn each turn, and an interruption restarts the whole task. For codebase-wide audits, large migrations (500+ files), or multi-source research requiring cross-validation, a different orchestration layer is needed -- one where the plan lives in code, not Claude's context, and is therefore repeatable, resumable, and scale-independent.

---

## Main Original Ideas

1. **Workflow-as-Script Paradigm** -- The orchestration plan is written as a JavaScript script that the runtime executes autonomously, separate from the conversation. Intermediate results stay in script variables rather than Claude's context window, freeing Claude to respond to other requests while agents work.

2. **Adversarial Cross-Checking** -- Workflows can route independent agents to review each other's outputs before results are reported. For example, `/deep-research` has agents vote on each claim; claims that don't survive cross-checking are filtered from the final report, producing higher-trust output than a single-pass approach.

3. **Ultracode Mode** -- Setting `/effort ultracode` combines `xhigh` reasoning effort with automatic workflow orchestration. Claude proactively plans workflows for every substantive task: one to understand code, one to make changes, one to verify -- without the user needing to request it.

4. **Resumable Runs** -- The runtime tracks each agent's result as it progresses. Stopping and resuming a run returns cached results for completed agents and re-runs only the remaining ones, within the same session.

5. **Saveable Workflow Commands** -- Any workflow script can be saved to `.claude/workflows/` (project-shared) or `~/.claude/workflows/` (personal) and becomes a first-class `/command` available in future sessions alongside bundled commands like `/deep-research`.

---

## Key Findings

| Dimension | Subagents | Skills | Workflows |
|-----------|-----------|--------|-----------|
| Plan owner | Claude, turn by turn | Claude, following prompt | The script |
| Intermediate results | Claude's context | Claude's context | Script variables |
| Scale | A few per turn | Same as subagents | Dozens--hundreds per run |
| Repeatable unit | Worker definition | Instructions | The orchestration itself |
| Interruption behavior | Restarts turn | Restarts turn | Resumable in same session |

- Max 16 concurrent agents (fewer on CPU-limited machines); max 1,000 agents total per run
- Subagents spawned by workflows always run in `acceptEdits` mode and inherit the session's tool allowlist
- In `bypass permissions` / `claude -p` / Agent SDK mode, workflow runs start without any approval prompt
- Project workflows take precedence over same-named personal workflows

---

## Suggestions & Future Directions

1. **Pre-authorize tool allowlists** before long runs to avoid mid-run permission prompts for shell commands, web fetches, and MCP tools.
2. **Route cheap stages to smaller models** -- ask Claude to use a smaller model for stages that don't need the strongest one when describing the task, to control token costs.
3. **Scope large tasks as separate workflow stages** -- for sign-off between stages, run each as its own workflow (mid-run user input is not supported by design).
4. **Organizational governance** -- admins can disable workflows globally via managed settings or the Claude Code admin page, or per-user via `disableWorkflows: true` in settings.

---

## Authors & Institutions

Anthropic (Claude Code documentation team)
