# Orchestrate Teams of Claude Code Sessions

**Doc:** [Agent Teams -- Claude Code Documentation](https://code.claude.com/docs/en/agent-teams)

## Human Readable TL;DR

Imagine you're managing a small team of workers on a project. Instead of one person doing everything one step at a time, you hire three specialists -- one for security, one for performance, one for testing -- and they all work in parallel, talk to each other, and hand you a combined report at the end. Claude Agent Teams do exactly this: multiple AI assistants running at the same time, each with its own focus, able to message each other directly and share a to-do list, while you stay in control as the manager.

## TL;DR

Claude Code Agent Teams (v2.1.32+, experimental) enable orchestrating multiple independent Claude instances around a shared task list and inter-agent messaging system. One session acts as team lead; teammates each hold their own context window, claim tasks via file-locked coordination, and communicate directly with each other via a mailbox system. Teams are best suited for parallelizable research, review, and new-feature work; sequential or same-file tasks are better handled by a single session or subagents.

---

## Problem & Motivation

Single-session Claude Code is fundamentally sequential -- one context window, one thread of work. For tasks that benefit from simultaneous exploration (e.g., parallel code review from multiple lenses, debugging competing hypotheses, cross-layer feature development), the bottleneck is the inability of agents to work independently and challenge each other. Agent Teams address this by giving each worker its own context window and direct communication channel.

---

## Main Original Ideas

1. **Team Lead + Teammates architecture** -- One session creates the team, spawns teammates, assigns tasks, and synthesizes results. Each teammate is a fully independent Claude Code session with its own context window, not a sub-call inside the lead.

2. **Shared task list with file-locking** -- Tasks are stored locally in `~/.claude/tasks/{team-name}/`. File locking prevents race conditions when multiple teammates simultaneously try to claim the same task. Tasks have states (pending, in-progress, completed) and can declare dependencies.

3. **Mailbox-based inter-agent messaging** -- Teammates communicate directly by name via a mailbox system. Messages are delivered automatically without polling. Idle notifications are sent automatically when a teammate finishes.

4. **Display modes: in-process vs. split-pane** -- In-process mode runs all teammates inside the main terminal (Shift+Down to cycle); split-pane mode gives each teammate its own tmux or iTerm2 pane. Default is `"auto"` (splits if already in tmux, else in-process).

5. **Plan approval gate** -- Teammates can be spawned in read-only plan mode. The lead reviews and either approves or rejects with feedback before any code is changed. The lead can enforce criteria autonomously (e.g., "only approve plans that include test coverage").

6. **Subagent definitions as teammate roles** -- Existing subagent definitions (project, user, plugin, CLI-scoped) can be referenced by name when spawning teammates. The definition's `tools` allowlist and `model` are honored; team coordination tools (`SendMessage`, task tools) are always available regardless.

7. **Quality gate hooks** -- Three hooks enforce team-wide rules: `TeammateIdle` (intercept idle transitions), `TaskCreated` (block task creation), `TaskCompleted` (block task completion). Exit code 2 sends feedback and keeps the agent working.

---

## Key Findings

### Subagents vs. Agent Teams

| Dimension | Subagents | Agent Teams |
|---|---|---|
| **Context** | Own window; results return to caller | Own window; fully independent |
| **Communication** | Report to main agent only | Teammates message each other directly |
| **Coordination** | Main agent manages all work | Shared task list, self-coordination |
| **Best for** | Focused tasks, result-only return | Complex work needing discussion |
| **Token cost** | Lower (results summarized back) | Higher (each = separate Claude instance) |

### Architecture components

| Component | Role |
|---|---|
| Team lead | Creates team, spawns teammates, synthesizes |
| Teammates | Separate Claude Code instances per task |
| Task list | `~/.claude/tasks/{team-name}/` -- shared, file-locked |
| Mailbox | Direct messaging between named agents |
| Team config | `~/.claude/teams/{team-name}/config.json` -- runtime state, auto-managed |

### Practical sizing guidance

- Start with **3--5 teammates** for most workflows
- **5--6 tasks per teammate** keeps everyone productive without excessive context switching
- Scale up only when tasks are genuinely independent
- Token cost scales linearly with teammate count

### Limitations (current, experimental)

- No session resumption for in-process teammates (`/resume`, `/rewind` don't restore them)
- Task status can lag (teammates may not mark tasks complete)
- Shutdown can be slow (waits for current tool call to finish)
- One team per lead session; no nested teams; lead is fixed at creation
- Split panes not supported in VS Code integrated terminal, Windows Terminal, or Ghostty
- `skills` and `mcpServers` subagent frontmatter fields are ignored when running as a teammate

---

## Suggestions & Future Directions

1. Enable agent teams by default once session resumption, task-status reliability, and shutdown behavior are resolved
2. Support per-teammate permission modes at spawn time (currently all inherit lead's mode)
3. Allow nested teams (teammates spawning sub-teams) for hierarchical task decomposition
4. Support session resumption with in-process teammates
5. Extend split-pane support to VS Code integrated terminal and Windows Terminal

---

## Enable

```json
// settings.json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

Requires Claude Code v2.1.32+.

---

## Best Use Cases

- **Parallel code review** -- security reviewer, performance reviewer, test-coverage reviewer working simultaneously on the same PR
- **Competing hypothesis debugging** -- multiple teammates each owning a different root-cause theory, actively trying to disprove each other
- **Cross-layer feature work** -- frontend, backend, and test teammates each owning separate files
- **Research & exploration** -- multiple perspectives on a design problem without waiting on each other

---

## Authors & Institutions

Anthropic (Claude Code team)
